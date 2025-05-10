from typing import Set
import pandas as pd
from kaonavi_api_executor.api.get_members_api import MembersResponse


class MembersMemberDataFlattener:
    def __init__(self, data: MembersResponse):
        self.member_data = data.member_data or []

    def flatten(self) -> pd.DataFrame:
        multi_value_fields: Set[str] = set()

        # valuesの抽出処理
        def extract_values(name: str, values: list[str]) -> str | list[str]:
            if len(values) > 1:
                multi_value_fields.add(name)
                return values
            return values[0]

        rows = [
            {
                "id": member["id"],
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
                "兼務情報": [
                    {
                        "所属コード": d["code"],
                        "所属名": d["name"],
                        "所属名_階層別": d["names"],
                    }
                    for d in member.get("sub_departments", [])
                ],
                "顔写真更新日時": member.get("face_image"),
                # custom_fieldsを展開（name: values）
                **{
                    field["name"]: extract_values(field["name"], field["values"])
                    for field in member.get("custom_fields", [])
                },
            }
            for member in self.member_data
        ]

        df = pd.DataFrame(rows)
        # multi_value_fieldsに含まれるカラムをリスト化
        for col in multi_value_fields:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda v: v if isinstance(v, list) or pd.isna(v) else [v]
                )
        return df.fillna(value=pd.NA)
