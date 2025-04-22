from ..mocks.mock_http_client import MockHttpClient
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher


def test_fetch_access_token():
    api_access_token_fetcher = ApiAccessTokenFetcher(client=MockHttpClient())
    access_token = api_access_token_fetcher.fetch_access_token()
    assert access_token == "mocked-token", "Access token should be 'mocked-token'"
