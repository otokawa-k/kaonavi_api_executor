from .http_client import HttpClient
from typing import Any, Dict, Optional
from requests.auth import AuthBase
from requests import Response
import requests


class Post(HttpClient):
    def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> Response:
        return requests.post(url, data=data, headers=headers, auth=auth)


class Get(HttpClient):
    def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> Response:
        return requests.get(url, params=params, headers=headers, auth=auth)
