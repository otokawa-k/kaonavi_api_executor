import pandas as pd
from typing import Any, Dict


class SheetsMemberDataFlattener:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def flatten(self) -> pd.DataFrame:
        rows = [
            {
                "code": member["code"],
                **{
                    field["name"]: field["values"][0] if field.get("values") else None
                    for field in record.get("custom_fields", [])
                },
            }
            for member in self.data.get("member_data", [])
            for record in member.get("records", [])
        ]
        return pd.DataFrame(rows)
