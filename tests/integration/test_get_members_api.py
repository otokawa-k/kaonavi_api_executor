import pytest
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_members_api import GetMembersApi
from kaonavi_api_executor.http_client.http_methods import Post


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
