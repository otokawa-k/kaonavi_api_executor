import os
from typing import Any, Dict
from pydantic import BaseModel
from .api_model import ApiModel
from ..http_client.http_client import HttpClient
from ..http_client.http_methods import Get


class SheetsResponse(BaseModel):
    id: int
    name: str
    record_type: int
    updated_at: str
    member_data: list[Dict[str, Any]]


class GetSheetsApi(ApiModel[SheetsResponse]):
    def __init__(self, sheet_id: int) -> None:
        super().__init__()

        url = os.getenv("KAONAVI_API_URL", "https://api.kaonavi.jp/api/v2.0")
        self.url = f"{url}/sheets/{str(sheet_id)}"

    @property
    def http_method(self) -> HttpClient:
        return Get()

    def parse_response(self, raw_json: Dict[str, Any]) -> SheetsResponse:
        return SheetsResponse.model_validate(raw_json)
