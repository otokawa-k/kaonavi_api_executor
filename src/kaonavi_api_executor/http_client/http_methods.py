from .http_client import HttpClient
from typing import Any, Dict, Optional
from httpx import AsyncClient, Response, Auth
import hashlib
import json
import os
import time


def _build_request_args(
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


def _make_cache_key(key_dict: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(key_dict, sort_keys=True, default=str).encode()
    ).hexdigest()


def _get_cache(
    cache: dict[str, tuple[float, Response]], key: str
) -> Optional[Response]:
    ttl_seconds = int(os.environ.get("KAONAVI_API_CACHE_TTL_MINUTES", "10")) * 60
    now = time.time()
    cached = cache.get(key)
    if cached is not None:
        cached_time, cached_response = cached
        if now - cached_time < ttl_seconds:
            return cached_response
        del cache[key]
    return None


def _set_cache(
    cache: dict[str, tuple[float, Response]], key: str, response: Response
) -> None:
    cache[key] = (time.time(), response)


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
        no_cache: bool = False,
    ) -> Response:
        key_dict: dict[str, Any] = {
            "url": url,
            "data": data,
            "headers": headers,
            "auth": str(auth) if auth is not None else None,
        }
        key = _make_cache_key(key_dict)
        cached_response = None
        if not no_cache:
            cached_response = _get_cache(self._cache, key)
        if cached_response is not None:
            return cached_response
        async with AsyncClient() as client:
            response = await client.post(
                **_build_request_args(
                    url=url,
                    data=data,
                    params=params,
                    headers=headers,
                    auth=auth,
                )
            )
            _set_cache(self._cache, key, response)
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
        no_cache: bool = False,
    ) -> Response:
        key_dict: dict[str, Any] = {
            "url": url,
            "params": params,
            "headers": headers,
            "auth": str(auth) if auth is not None else None,
        }
        key = _make_cache_key(key_dict)
        cached_response = None
        if not no_cache:
            cached_response = _get_cache(self._cache, key)
        if cached_response is not None:
            return cached_response
        async with AsyncClient() as client:
            response = await client.get(
                **_build_request_args(
                    url=url,
                    params=params,
                    headers=headers,
                    auth=auth,
                )
            )
            _set_cache(self._cache, key, response)
            return response
