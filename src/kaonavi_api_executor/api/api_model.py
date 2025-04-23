from abc import ABC, abstractmethod
from typing import Generic, Optional
from ..types.typevars import TResponse
from ..http_client.http_client import HttpClient


class ApiModel(ABC, Generic[TResponse]):
    def __init__(self, token: Optional[str] = None):
        self.url: Optional[str] = None
        self.params: Optional[dict] = None
        self.data: Optional[dict] = None
        self.headers: Optional[dict] = None
        self.auth: Optional[any] = None
        self.token = token

    @property
    @abstractmethod
    def method(self) -> HttpClient:
        pass

    @abstractmethod
    def parse_response(self, raw_json: dict) -> TResponse:
        pass
