import pytest
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_member_api import GetMemberApi
from kaonavi_api_executor.http_client.http_methods import Post
from .mocks.mock_api_model import MockApiModel


@pytest.mark.asyncio
async def test_api_executor() -> None:
    mock_api = MockApiModel(token="mocked-token")
    api_executor = ApiExecutor(mock_api)

    result = await api_executor.execute()

    assert result.id == "12345"
    assert result.name == "テスト名称"


@pytest.mark.online
@pytest.mark.asyncio
async def test_api_executor_online() -> None:
    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    api = GetMemberApi(token=token)
    api_executor = ApiExecutor(api)

    result = await api_executor.execute()

    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"
