from abc import ABC, abstractmethod
from typing import Dict, Generic, Optional, Any

from httpx import Auth
from ..types.typevars import TResponse
from ..http_client.http_client import HttpClient


class ApiModel(ABC, Generic[TResponse]):
    def __init__(self) -> None:
        self.url: Optional[str] = None
        self.data: Optional[Any] = None
        self.params: Optional[Dict[str, Any]] = None
        self.headers: Optional[Dict[str, str]] = None
        self.auth: Optional[Auth] = None

    @property
    @abstractmethod
    def method(self) -> HttpClient:
        pass

    @abstractmethod
    def parse_response(self, raw_json: Dict[str, Any]) -> TResponse:
        pass
