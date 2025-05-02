from typing import Any, Dict
from pydantic import BaseModel
from kaonavi_api_executor.api.api_model import ApiModel
from kaonavi_api_executor.http_client.http_client import HttpClient
from .mock_http_method import MockResponse, MockHttpMethod


class MockApiResponse(BaseModel):
    id: str
    name: str


class MockApiModel(ApiModel[MockApiResponse]):
    def __init__(self) -> None:
        self.url = "https://example.com"
        self.params = None
        self.headers = {"Authorization": "mocked-token"}
        self.auth = None
        self.data = None

    @property
    def method(self) -> HttpClient:
        return MockHttpMethod(
            MockResponse(
                status_code=200, json_data={"id": "12345", "name": "テスト名称"}
            )
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> MockApiResponse:
        return MockApiResponse.model_validate(raw_json)
