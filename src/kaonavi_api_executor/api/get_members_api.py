import os
from typing import Any, Dict
from pydantic import BaseModel
from .api_model import ApiModel
from ..http_client.http_client import HttpClient
from ..http_client.http_methods import Get


class MembersResponse(BaseModel):
    updated_at: str
    member_data: list[Dict[str, Any]]


class GetMembersApi(ApiModel[MembersResponse]):
    def __init__(self) -> None:
        super().__init__()

        url = os.getenv("KAONAVI_API_URL", "https://api.kaonavi.jp/api/v2.0")
        self.url = f"{url}/members"

    @property
    def http_method(self) -> HttpClient:
        return Get()

    def parse_response(self, raw_json: Dict[str, Any]) -> MembersResponse:
        return MembersResponse.model_validate(raw_json)
