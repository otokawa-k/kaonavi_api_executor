from typing import Any, Dict, Tuple
import re
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
        custom_field_has_multiple_values: Dict[str, bool] = {}

        # nameの置換処理（英数字・日本語・_ 以外の文字を _ に変換）
        def replace_name(name: str) -> str:
            name = re.sub(r"[^\w]", "_", name)
            name = re.sub(r"_+", "_", name)
            return name.strip("_")

        # custom_fieldsを展開（name: values）
        def extract_custom_fields(
            custom_fields: list[Dict[str, Any]],
        ) -> Dict[str, list[str]]:
            result = {}
            for field in custom_fields:
                name = replace_name(field["name"])
                values = field["values"]
                # custom_fieldsが複数値を持つかどうかを判定
                if name not in custom_field_has_multiple_values:
                    custom_field_has_multiple_values[name] = False
                if isinstance(values, list) and len(values) > 1:
                    custom_field_has_multiple_values[name] = True
                result[name] = values
            return result

        main_rows = []
        sub_rows = []
        for member in self.member_data:
            main_rows.append(
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
                    "所属名_階層別": ",".join(
                        f'"{x}"' for x in member["department"]["names"]
                    ),
                    "顔写真更新日時": (member.get("face_image") or {}).get(
                        "updated_at"
                    ),
                    # custom_fieldsを統合
                    **extract_custom_fields(member.get("custom_fields", [])),
                }
            )

            # 兼務情報を展開
            sub_rows.extend(
                [
                    {
                        "社員番号": member["code"],
                        "所属コード": sub_department["code"],
                        "所属名": sub_department["name"],
                        "所属名_階層別": ",".join(
                            f'"{x}"' for x in sub_department["names"]
                        ),
                    }
                    for sub_department in member.get("sub_departments", [])
                ]
            )

        main_df = pd.DataFrame(main_rows)
        sub_df = pd.DataFrame(sub_rows)

        # main_dfのcustom_fieldをリストから文字列に変換
        # ただし、複数値を持つフィールドはカンマ区切りの文字列に変換
        for col, is_multi in custom_field_has_multiple_values.items():
            if not is_multi:
                main_df[col] = main_df[col].apply(
                    lambda v: v[0] if isinstance(v, list) else v
                )
            else:
                main_df[col] = main_df[col].apply(
                    lambda v: ",".join(f'"{x}"' for x in v)
                    if isinstance(v, list)
                    else v
                )

        return main_df.fillna(value=pd.NA), sub_df.fillna(value=pd.NA)
