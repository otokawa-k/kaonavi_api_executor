import os
from typing import Optional
from pydantic import BaseModel
from .api_model import ApiModel
from ..http_client.http_client import HttpClient
from ..http_client.http_methods import Get


class MemberResponse(BaseModel):
    updated_at: str
    member_data: list[dict]


class GetMemberApi(ApiModel[MemberResponse]):
    def __init__(self, token: Optional[str] = None):
        super().__init__(token)
        url = os.getenv('KAONAVI_API_URL', 'https://api.kaonavi.jp/api/v2.0')
        self.url = f"{url}/members"
        self.headers = {'Content-Type': 'application/json', 'Kaonavi-Token': self.token}

    @property
    def method(self) -> HttpClient:
        return Get()

    def parse_response(self, raw_json: dict) -> MemberResponse:
        return MemberResponse.model_validate(raw_json)
