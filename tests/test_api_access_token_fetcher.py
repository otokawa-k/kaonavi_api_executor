from src.kaonavi_api_executor.api_access_token_fetcher import ApiAccessTokenFetcher


def test_fetch_access_token():
    api_access_token_fetcher = ApiAccessTokenFetcher()
    access_token = api_access_token_fetcher.fetch_access_token()
    assert access_token is not None, "Access token should not be None"
    assert isinstance(access_token, str), "Access token should be a string"
    assert len(access_token) > 0, "Access token should not be empty"
