import time
from typing import Any, Dict, List, Optional
from httpx import Auth, Response
import pytest
from tests.unit.mocks.mock_http_method import MockHttpMethod, MockResponse
from kaonavi_api_executor.auth.access_token import AccessToken


class SwitchableMockHttpMethod(MockHttpMethod):
    responses: List[MockResponse]
    call_count: int

    def __init__(self, responses: list[MockResponse]) -> None:
        super().__init__(mock_response=responses[0])
        self.responses = responses
        self.call_count = 0

    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
        idx = min(self.call_count, len(self.responses) - 1)
        self._mock_response = self.responses[idx]
        self.call_count += 1
        return self._mock_response._to_response()


@pytest.mark.asyncio
async def test_get_returns_token_and_refreshes_on_expiry() -> None:
    # 1回目と2回目で異なるトークンを返すようにする
    responses = [
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
    http_method = SwitchableMockHttpMethod(responses)
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
    response = MockResponse(
        status_code=200,
        json_data={
            "access_token": "token_1",
            "token_type": "Bearer",
            "expire_in": 2,
        },
    )
    http_method = MockHttpMethod(mock_response=response)
    access_token = AccessToken(http_method=http_method)
    assert await access_token.get() == "token_1"
