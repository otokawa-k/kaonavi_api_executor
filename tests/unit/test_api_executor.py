import pytest
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.auth.access_token import AccessToken
from .mocks.mock_http_method import MockHttpMethod, MockResponse
from .mocks.mock_api_model import MockApiModel


@pytest.mark.asyncio
async def test_api_executor() -> None:
    mock_response = MockResponse(
        status_code=200,
        json_data={
            "access_token": "mocked-token",
            "token_type": "Bearer",
            "expire_in": 3600,
        },
    )
    access_token = AccessToken(http_method=MockHttpMethod([mock_response]))
    mock_api = MockApiModel()
    api_executor = ApiExecutor(access_token=access_token, api=mock_api)
    result = await api_executor.execute()

    assert result.id == "12345"
    assert result.name == "テスト名称"


@pytest.mark.asyncio
async def test_api_executor_no_cache() -> None:
    mock_response = MockResponse(
        status_code=200,
        json_data={
            "access_token": "mocked-token",
            "token_type": "Bearer",
            "expire_in": 3600,
        },
    )
    access_token = AccessToken(http_method=MockHttpMethod([mock_response]))
    mock_api = MockApiModel()
    api_executor = ApiExecutor(access_token=access_token, api=mock_api)
    result = await api_executor.execute(no_cache=True)

    assert result.id == "12345"
    assert result.name == "テスト名称"
