import os
import pytest
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_members_api import GetMembersApi
from kaonavi_api_executor.api.get_sheets_api import GetSheetsApi
from kaonavi_api_executor.http_client.http_methods import Post
from .mocks.mock_api_model import MockApiModel


@pytest.mark.asyncio
async def test_api_executor() -> None:
    mock_api = MockApiModel()
    api_executor = ApiExecutor(mock_api)

    result = await api_executor.execute()

    assert result.id == "12345"
    assert result.name == "テスト名称"


@pytest.mark.online
@pytest.mark.asyncio
async def test_get_members_api() -> None:
    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    api = GetMembersApi(token=token)
    api_executor = ApiExecutor(api)

    result = await api_executor.execute()

    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"


@pytest.mark.online
@pytest.mark.asyncio
async def test_get_sheets_api() -> None:
    sheet_id = os.getenv("SHEET_ID")
    if sheet_id is None:
        raise Exception("SHEET_ID environment variable is not set.")

    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    api = GetSheetsApi(token=token, sheet_id=int(sheet_id))
    api_executor = ApiExecutor(api)

    result = await api_executor.execute()

    assert result.id == int(sheet_id), f"id should be {sheet_id}"
    assert result.name is not None, "name should not be None"
    assert result.record_type is not None, "record_type should not be None"
    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"
