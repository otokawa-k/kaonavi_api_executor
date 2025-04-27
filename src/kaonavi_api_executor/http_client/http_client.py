from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from httpx import Response, Auth


class HttpClient(ABC):
    @abstractmethod
    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
        pass
