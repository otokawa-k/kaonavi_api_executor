from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from requests.auth import AuthBase
from requests import Response


class HttpClient(ABC):
    @abstractmethod
    def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> Response:
        pass
