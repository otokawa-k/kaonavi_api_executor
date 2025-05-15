import re
from typing import Any, Dict
import pandas as pd
from kaonavi_api_executor.api.get_sheets_api import SheetsResponse


class SheetsMemberDataFlattener:
    def __init__(self, data: SheetsResponse):
        self.member_data = data.member_data or []

    def flatten(self) -> pd.DataFrame:
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

        rows = [
            {
                "code": member["code"],
                "row_index": i,
                **extract_custom_fields(record.get("custom_fields", [])),
            }
            for member in self.member_data
            for i, record in enumerate(member.get("records", []))
        ]

        df = pd.DataFrame(rows)

        # dfのcustom_fieldをリストから文字列に変換
        # ただし、複数値を持つフィールドはカンマ区切りの文字列に変換
        for col, is_multi in custom_field_has_multiple_values.items():
            if not is_multi:
                df[col] = df[col].apply(lambda v: v[0] if isinstance(v, list) else v)
            else:
                df[col] = df[col].apply(
                    lambda v: ",".join(f'"{x}"' for x in v)
                    if isinstance(v, list)
                    else v
                )

        return df.fillna(value=pd.NA)
