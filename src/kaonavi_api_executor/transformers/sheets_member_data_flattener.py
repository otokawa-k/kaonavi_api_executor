import pandas as pd
from kaonavi_api_executor.api.get_sheets_api import SheetsResponse


class SheetsMemberDataFlattener:
    def __init__(self, data: SheetsResponse):
        self.member_data = data.member_data or []

    def flatten(self) -> pd.DataFrame:
        rows = [
            {
                "code": member["code"],
                **{
                    field["name"]: field["values"][0] if field.get("values") else None
                    for field in record.get("custom_fields", [])
                },
            }
            for member in self.member_data
            for record in member.get("records", [])
        ]
        return pd.DataFrame(rows)
