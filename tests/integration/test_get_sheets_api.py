import os
import pytest
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_sheets_api import GetSheetsApi
from kaonavi_api_executor.transformers.sheets_member_data_flattener import (
    SheetsMemberDataFlattener,
)


@pytest.mark.asyncio
async def test_get_sheets_api() -> None:
    api_executor = ApiExecutor()

    sheet_id = os.getenv("SHEET_ID")
    if sheet_id is None:
        raise Exception("SHEET_ID environment variable is not set.")
    api = GetSheetsApi(sheet_id=int(sheet_id))
    result = await api_executor.execute(api)

    assert result.id == int(sheet_id), f"id should be {sheet_id}"
    assert result.name is not None, "name should not be None"
    assert result.record_type is not None, "record_type should not be None"
    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"

    flattener = SheetsMemberDataFlattener(result)
    df = flattener.flatten()
    assert df is not None, "DataFrame should not be None"
    assert not df.empty, "DataFrame should not be empty"
