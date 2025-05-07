from typing import Set
import pandas as pd
from kaonavi_api_executor.api.get_sheets_api import SheetsResponse


class SheetsMemberDataFlattener:
    def __init__(self, data: SheetsResponse):
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
                "code": member["code"],
                "row_index": i,
                # custom_fieldsを展開（name: values）
                **{
                    field["name"]: extract_values(field["name"], field["values"])
                    for field in record.get("custom_fields", [])
                },
            }
            for member in self.member_data
            for i, record in enumerate(member.get("records", []))
        ]

        df = pd.DataFrame(rows)
        # multi_value_fieldsに含まれるカラムをリスト化
        for col in multi_value_fields:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda v: v if isinstance(v, list) or pd.isna(v) else [v]
                )
        return df.fillna(value=pd.NA)
