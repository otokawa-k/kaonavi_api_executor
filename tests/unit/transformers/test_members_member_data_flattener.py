from typing import Any, Dict, List
import pandas as pd
import pytest
from kaonavi_api_executor.api.get_members_api import MembersResponse
from kaonavi_api_executor.transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)


test_cases: List[tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = [
]


@pytest.mark.parametrize("member_data, expected_rows", test_cases)
def test_flatten_returns_dataframe(
    member_data: List[Dict[str, Any]], expected_rows: List[Dict[str, Any]]
) -> None:
    input_data =MembersResponse(
        updated_at="2023-10-01T00:00:00Z",
        member_data=member_data,
    )
    flattener = MembersMemberDataFlattener(input_data)
    df = flattener.flatten()
    actual = df.fillna(value=pd.NA).to_dict(orient="records")
    assert actual == expected_rows
