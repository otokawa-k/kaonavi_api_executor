from typing import Any, Dict, List
import pandas as pd
import pytest
from kaonavi_api_executor.api.get_sheets_api import SheetsResponse
from kaonavi_api_executor.transformers.sheets_member_data_flattener import (
    SheetsMemberDataFlattener,
)


test_cases: List[tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = [
    (
        [
            {
                "code": "A0001",
                "records": [
                    {
                        "custom_fields": [
                            {
                                "id": 1000,
                                "name": "住所",
                                "values": ["東京都渋谷区1-1-1"],
                            },
                            {
                                "id": 1001,
                                "name": "電話番号",
                                "values": ["03-1234-5678"],
                            },
                        ]
                    },
                    {
                        "custom_fields": [
                            {
                                "id": 1000,
                                "name": "住所",
                                "values": ["大阪府大阪市2-2-2"],
                            }
                        ]
                    },
                ],
            },
            {
                "code": "A0002",
                "records": [
                    {
                        "custom_fields": [
                            {
                                "id": 1000,
                                "name": "住所",
                                "values": ["神戸市中央区3-3-3"],
                            },
                            {
                                "id": 1001,
                                "name": "電話番号",
                                "values": ["078-1234-5678"],
                            },
                            {
                                "id": 1002,
                                "name": "FAX番号",
                                "values": ["078-9876-5432"],
                            },
                        ]
                    }
                ],
            },
        ],
        [
            {
                "code": "A0001",
                "住所": "東京都渋谷区1-1-1",
                "電話番号": "03-1234-5678",
                "FAX番号": None,
            },
            {
                "code": "A0001",
                "住所": "大阪府大阪市2-2-2",
                "電話番号": None,
                "FAX番号": None,
            },
            {
                "code": "A0002",
                "住所": "神戸市中央区3-3-3",
                "電話番号": "078-1234-5678",
                "FAX番号": "078-9876-5432",
            },
        ],
    ),
]


@pytest.mark.parametrize("member_data, expected_rows", test_cases)
def test_flatten_returns_dataframe(
    member_data: List[Dict[str, Any]], expected_rows: List[Dict[str, Any]]
) -> None:
    input_data = SheetsResponse(
        id=1,
        name="テスト名称",
        record_type=1,
        updated_at="2023-10-01T00:00:00Z",
        member_data=member_data,
    )
    flattener = SheetsMemberDataFlattener(input_data)
    df = flattener.flatten()
    actual = df.fillna(value=pd.NA).to_dict(orient="records")
    assert actual == expected_rows
