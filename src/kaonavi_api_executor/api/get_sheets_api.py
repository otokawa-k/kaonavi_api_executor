import os
from typing import Any, Dict, Optional
from pydantic import BaseModel
from .api_model import ApiModel
from ..http_client.http_client import HttpClient
from ..http_client.http_methods import Get


class EmptyRequest(BaseModel):
    pass


class SheetsResponse(BaseModel):
    id: int
    name: str
    record_type: int
    updated_at: str
    member_data: list[Dict[str, Any]]


class GetSheetsApi(ApiModel[EmptyRequest, SheetsResponse]):
    def __init__(self, sheet_id: Optional[int] = None) -> None:
        super().__init__()
        self._base_url = os.getenv("KAONAVI_API_URL", "https://api.kaonavi.jp/api/v2.0")
        self._sheet_id = sheet_id
        self._update_url()

    def set_sheet_id(self, sheet_id: int) -> None:
        self._sheet_id = sheet_id
        self._update_url()

    def _update_url(self) -> None:
        if self._sheet_id is not None:
            self.url = f"{self._base_url}/sheets/{str(self._sheet_id)}"
        else:
            self.url = None

    @property
    def http_method(self) -> HttpClient:
        return Get()

    def parse_response(self, raw_json: Dict[str, Any]) -> SheetsResponse:
        return SheetsResponse.model_validate(raw_json)
