import time
import pytest
from tests.unit.mocks.mock_http_method import MockHttpMethod, MockResponse
from kaonavi_api_executor.auth.access_token import AccessToken


@pytest.mark.asyncio
async def test_no_cache_parameter_is_passed_correctly() -> None:
    mock_response = MockResponse(
        status_code=200,
        json_data={
            "access_token": "test_token",
            "token_type": "Bearer",
            "expire_in": 3600,
        },
    )
    http_method = MockHttpMethod([mock_response])
    access_token = AccessToken(http_method=http_method)

    # トークンを取得
    await access_token.get()

    # no_cacheがTrueで呼び出されたことを確認
    assert http_method.last_call_args.no_cache is True


@pytest.mark.asyncio
async def test_get_returns_token_and_refreshes_on_expiry() -> None:
    # 1回目と2回目で異なるトークンを返すようにする
    mock_responses = [
        MockResponse(
            status_code=200,
            json_data={
                "access_token": "token_1",
                "token_type": "Bearer",
                "expire_in": 3600,
            },
        ),
        MockResponse(
            status_code=200,
            json_data={
                "access_token": "token_2",
                "token_type": "Bearer",
                "expire_in": 3600,
            },
        ),
    ]
    http_method = MockHttpMethod(mock_responses)
    access_token = AccessToken(http_method=http_method)

    # 初回取得
    assert await access_token.get() == "token_1"

    # 有効期限内は再取得しない
    assert await access_token.get() == "token_1"

    # 有効期限切れ後は再取得される（有効期限を強制的に過去に）
    access_token._expires_at = int(time.time()) - 1
    assert await access_token.get() == "token_2"


@pytest.mark.asyncio
async def test_token_is_refetched_if_never_fetched() -> None:
    mock_response = MockResponse(
        status_code=200,
        json_data={
            "access_token": "token_1",
            "token_type": "Bearer",
            "expire_in": 3600,
        },
    )
    http_method = MockHttpMethod([mock_response])
    access_token = AccessToken(http_method=http_method)
    assert await access_token.get() == "token_1"
