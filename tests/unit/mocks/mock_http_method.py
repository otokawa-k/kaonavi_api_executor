from dataclasses import dataclass
from kaonavi_api_executor.http_client.http_client import HttpClient
from typing import Any, Dict, Optional
from httpx import Response, Auth, Request
import httpx


class MockResponse:
    def __init__(
        self,
        status_code: int = 200,
        json_data: Optional[Dict[Any, Any]] = None,
        text: str = "",
    ):
        self.status_code = status_code
        self._json_data = json_data or {}
        self._text = text

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise httpx.HTTPStatusError(
                f"HTTP Error {self.status_code}",
                request=Request(method="GET", url="https://mocked-url.com"),
                response=self.to_response(),
            )

    def json(self) -> Dict[str, Any]:
        return self._json_data

    def text(self) -> str:
        return self._text

    def to_response(self) -> Response:
        return Response(
            status_code=self.status_code,
            json=self._json_data,
            request=Request(method="GET", url="https://mocked-url.com"),
        )


@dataclass
class CallArgs:
    url: str = ""
    data: Optional[Any] = None
    params: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    auth: Optional[Auth] = None
    no_cache: bool = False


class MockHttpMethod(HttpClient):
    def __init__(self, mock_responses: list[MockResponse]) -> None:
        self._mock_responses = mock_responses
        self._call_count = 0
        self.last_call_args: CallArgs = CallArgs()

    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
        no_cache: bool = False,
    ) -> Response:
        self.last_call_args = CallArgs(
            url=url,
            data=data,
            params=params,
            headers=headers,
            auth=auth,
            no_cache=no_cache,
        )

        idx = min(self._call_count, len(self._mock_responses) - 1)
        self._call_count += 1
        return self._mock_responses[idx].to_response()
