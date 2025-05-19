from .http_client import HttpClient
from typing import Any, Dict, Optional
from httpx import AsyncClient, Response, Auth
import hashlib
import json
import os
import time


def build_request_args(
    url: str,
    data: Optional[Any] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[Auth] = None,
) -> Dict[str, Any]:
    args: Dict[str, Any] = {"url": url}
    if data is not None:
        args["data"] = data
    if params is not None:
        args["params"] = params
    if headers is not None:
        args["headers"] = headers
    if auth is not None:
        args["auth"] = auth
    return args


class Post(HttpClient):
    def __init__(self) -> None:
        super().__init__()
        self._cache: dict[str, tuple[float, Response]] = {}

    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
        # キャッシュキー生成
        key_dict = {
            "url": url,
            "data": data,
            "headers": headers,
            "auth": str(auth) if auth is not None else None,
        }
        key = hashlib.sha256(
            json.dumps(key_dict, sort_keys=True, default=str).encode()
        ).hexdigest()
        ttl_minutes = int(os.environ.get("KAONAVI_API_CACHE_TTL_MINUTES", "10"))
        ttl_seconds = ttl_minutes * 60
        now = time.time()
        cached = self._cache.get(key)
        if cached is not None:
            cached_time, cached_response = cached
            if now - cached_time < ttl_seconds:
                return cached_response
            del self._cache[key]
        async with AsyncClient() as client:
            response = await client.post(
                **build_request_args(
                    url=url,
                    data=data,
                    params=params,
                    headers=headers,
                    auth=auth,
                )
            )
            self._cache[key] = (now, response)
            return response


class Get(HttpClient):
    def __init__(self) -> None:
        super().__init__()
        self._cache: dict[str, tuple[float, Response]] = {}

    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
        # キャッシュキー生成
        key_dict = {
            "url": url,
            "params": params,
            "headers": headers,
            "auth": str(auth) if auth is not None else None,
        }
        key = hashlib.sha256(
            json.dumps(key_dict, sort_keys=True, default=str).encode()
        ).hexdigest()
        ttl_minutes = int(os.environ.get("KAONAVI_API_CACHE_TTL_MINUTES", "10"))
        ttl_seconds = ttl_minutes * 60
        now = time.time()
        cached = self._cache.get(key)
        if cached is not None:
            cached_time, cached_response = cached
            if now - cached_time < ttl_seconds:
                return cached_response
            del self._cache[key]
        async with AsyncClient() as client:
            response = await client.get(
                **build_request_args(
                    url=url,
                    params=params,
                    headers=headers,
                    auth=auth,
                )
            )
            self._cache[key] = (now, response)
            return response
