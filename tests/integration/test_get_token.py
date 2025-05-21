import pytest
from kaonavi_api_executor.auth.access_token import AccessToken
from kaonavi_api_executor.http_client.http_methods import Post


@pytest.mark.asyncio
async def test_fetch_access_token() -> None:
    access_token = AccessToken(http_method=Post())
    token = await access_token.get()
    assert token is not None, "Access token should not be None"
    assert isinstance(token, str), "Access token should be a string"
