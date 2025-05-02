import pytest
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.http_client.http_methods import Post


@pytest.mark.asyncio
async def test_fetch_access_token() -> None:
    api_access_token_fetcher = ApiAccessTokenFetcher(client=Post())
    access_token = await api_access_token_fetcher.fetch_access_token()
    assert access_token is not None, "Access token should not be None"
    assert isinstance(access_token, str), "Access token should be a string"
