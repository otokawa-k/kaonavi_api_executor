from typing import Any, Dict, Optional
from requests.auth import AuthBase
from requests import Response


class MockResponse:
    def __init__(self, status_code: int = 200, json_data: dict = None, text: str = ""):
        self.status_code = status_code
        self.json_data = json_data or {}
        self.text = text

    def raise_for_status(self): pass

    def json(self):
        return self.json_data


class MockHttpMethod:
    def __init__(self, mock_response: MockResponse = None):
        self._mock_response = mock_response or MockResponse(
            status_code=200,
            json_data={"access_token": "mocked-token"},
        )

    def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> Response:
        return self._mock_response
