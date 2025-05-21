from typing import Any, Dict
from pydantic import BaseModel
from kaonavi_api_executor.api.api_model import ApiModel
from kaonavi_api_executor.http_client.http_client import HttpClient
from .mock_http_method import MockResponse, MockHttpMethod


class EmptyRequest(BaseModel):
    pass


class MockApiResponse(BaseModel):
    id: str
    name: str


class MockApiModel(ApiModel[EmptyRequest, MockApiResponse]):
    def __init__(self) -> None:
        super().__init__()

        self.url = "https://example.com"

    @property
    def http_method(self) -> HttpClient:
        return MockHttpMethod(
            MockResponse(
                status_code=200, json_data={"id": "12345", "name": "テスト名称"}
            )
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> MockApiResponse:
        return MockApiResponse.model_validate(raw_json)
