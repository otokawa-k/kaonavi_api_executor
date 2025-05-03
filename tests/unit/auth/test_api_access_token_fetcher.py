from typing import Any
import pytest
from ..mocks.mock_http_method import MockHttpMethod
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher


@pytest.mark.asyncio
async def test_fetch_access_token(monkeypatch: Any) -> None:
    monkeypatch.setenv("KAONAVI_CONSUMER_KEY", "test_consumer_key")
    monkeypatch.setenv("KAONAVI_CONSUMER_SECRET", "test_consumer_secret")
    api_access_token_fetcher = ApiAccessTokenFetcher(client=MockHttpMethod())
    access_token = await api_access_token_fetcher.fetch_access_token()
    assert access_token == "mocked-token", "Access token should be 'mocked-token'"
