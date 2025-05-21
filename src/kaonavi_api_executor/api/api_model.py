from abc import ABC, abstractmethod
from typing import Dict, Generic, Optional, Any

from httpx import Auth
from ..types.typevars import TRequest, TResponse
from ..http_client.http_client import HttpClient


class ApiModel(ABC, Generic[TRequest, TResponse]):
    def __init__(self) -> None:
        self.url: Optional[str] = None
        self._data: Optional[TRequest] = None
        self.params: Optional[Dict[str, Any]] = None
        self.headers: Dict[str, str] = {}
        self.auth: Optional[Auth] = None

    @property
    def data(self) -> Optional[Any]:
        if self._data is None:
            return None
        return self.prepare_request(self._data)

    @data.setter
    def data(self, value: TRequest) -> None:
        self._data = value

    def prepare_request(self, request: TRequest) -> Any:
        return request

    @property
    @abstractmethod
    def http_method(self) -> HttpClient:
        pass

    @abstractmethod
    def parse_response(self, raw_json: Dict[str, Any]) -> TResponse:
        pass
