from .http_client import HttpClient
from typing import Any, Dict, Optional
from httpx import AsyncClient, Response, Auth


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
    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
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
            return response


class Get(HttpClient):
    async def send(
        self,
        url: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Auth] = None,
    ) -> Response:
        async with AsyncClient() as client:
            response = await client.get(
                **build_request_args(
                    url=url,
                    params=params,
                    headers=headers,
                    auth=auth,
                )
            )
            return response
