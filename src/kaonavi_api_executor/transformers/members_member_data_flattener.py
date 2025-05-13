from typing import Tuple
import re
from typing import Set
import pandas as pd
from kaonavi_api_executor.api.get_members_api import MembersResponse


class MembersMemberDataFlattener:
    def __init__(self, data: MembersResponse):
        self.member_data = data.member_data or []

    def flatten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        メンバー情報をフラット化したDataFrameに変換する。

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                - 第1要素: メンバー情報のDataFrame
                - 第2要素: 兼務情報のDataFrame
        """
        multi_value_fields: Set[str] = set()

        # valuesの抽出処理
        def extract_values(name: str, values: list[str]) -> str | list[str]:
            if len(values) > 1:
                multi_value_fields.add(name)
                return values
            return values[0]

        # nameの置換処理（英数字・日本語・_ 以外の文字を _ に変換）
        def replace_name(name: str) -> str:
            name = re.sub(r"[^\w]", "_", name)
            name = re.sub(r"_+", "_", name)
            return name.strip("_")

        # 兼務情報以外を展開
        rows = [
            {
                "社員番号": member["code"],
                "氏名": member["name"],
                "フリガナ": member["name_kana"],
                "メールアドレス": member["mail"],
                "入社日": member["entered_date"],
                "退職日": member["retired_date"],
                "性別": member["gender"],
                "生年月日": member["birthday"],
                "年齢": member["age"],
                "勤続年数": member["years_of_service"],
                "所属コード": member["department"]["code"],
                "所属名": member["department"]["name"],
                "所属名_階層別": member["department"]["names"],
                "顔写真更新日時": member.get("face_image"),
                # custom_fieldsを展開（name: values）
                **{
                    (name := replace_name(field["name"])): extract_values(
                        name, field["values"]
                    )
                    for field in member.get("custom_fields", [])
                },
            }
            for member in self.member_data
        ]

        main_df = pd.DataFrame(rows)
        # multi_value_fieldsに含まれるカラムをリスト化
        for col in multi_value_fields:
            if col in main_df.columns:
                main_df[col] = main_df[col].apply(
                    lambda v: v if isinstance(v, list) or pd.isna(v) else [v]
                )

        # 兼務情報を展開
        rows = [
            {
                "社員番号": member["code"],
                "所属コード": sub_department["code"],
                "所属名": sub_department["name"],
                "所属名_階層別": sub_department["names"],
            }
            for member in self.member_data
            for sub_department in member.get("sub_departments", [])
        ]
        sub_df = pd.DataFrame(rows)

        return main_df.fillna(value=pd.NA), sub_df.fillna(value=pd.NA)
