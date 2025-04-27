import pytest
from ..mocks.mock_http_method import MockHttpMethod
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.http_client.http_methods import Post


@pytest.mark.asyncio
async def test_fetch_access_token() -> None:
    api_access_token_fetcher = ApiAccessTokenFetcher(client=MockHttpMethod())
    access_token = await api_access_token_fetcher.fetch_access_token()
    assert access_token == "mocked-token", "Access token should be 'mocked-token'"


@pytest.mark.online
@pytest.mark.asyncio
async def test_fetch_access_token_online() -> None:
    api_access_token_fetcher = ApiAccessTokenFetcher(client=Post())
    access_token = await api_access_token_fetcher.fetch_access_token()
    assert access_token is not None, "Access token should not be None"
    assert isinstance(access_token, str), "Access token should be a string"
