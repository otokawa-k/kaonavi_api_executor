from typing import Generator, Tuple, Type, Dict, Any
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import os
from kaonavi_api_executor.http_client.http_methods import Post, Get
from kaonavi_api_executor.http_client.http_client import HttpClient


@pytest.fixture
def test_data() -> Dict[str, Any]:
    return {
        "url": "https://mocked-url.com",
        "headers": {"Content-Type": "application/json"},
        "auth": None,
        "params": {"query": "value"},
        "data": {"key": "value"},
    }


@pytest.fixture
def mock_async_client() -> Generator[Tuple[MagicMock, AsyncMock], None, None]:
    with patch(
        "kaonavi_api_executor.http_client.http_methods.AsyncClient"
    ) as async_client:
        mock_client = MagicMock()
        mock_response = AsyncMock()

        # Mocking all HTTP methods
        mock_session = MagicMock()
        for method in ["post", "get", "put", "delete"]:
            setattr(mock_session, method, AsyncMock(return_value=mock_response))

        mock_client.__aenter__.return_value = mock_session
        async_client.return_value = mock_client

        yield mock_client, mock_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_cls, method, req_args",
    [
        (Post, "post", {"data": "data"}),
        (Get, "get", {"params": "params"}),
    ],
)
async def test_send(
    client_cls: Type[HttpClient],
    method: str,
    req_args: Dict[str, str],
    mock_async_client: Tuple[MagicMock, AsyncMock],
    test_data: Dict[str, Any],
) -> None:
    mock_client, mock_response = mock_async_client
    client = client_cls()
    args = {
        "url": test_data["url"],
        "headers": test_data["headers"],
        "auth": test_data["auth"],
    }
    if "data" in req_args:
        args["data"] = test_data["data"]
    if "params" in req_args:
        args["params"] = test_data["params"]

    response = await client.send(**args)
    getattr(mock_client.__aenter__.return_value, method).assert_called_once_with(
        url=test_data["url"],
        **({req_args["data"]: test_data["data"]} if "data" in req_args else {}),
        **({req_args["params"]: test_data["params"]} if "params" in req_args else {}),
        headers=test_data["headers"],
    )
    assert response == mock_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_cls, method, req_args",
    [
        (Get, "get", {"params": "params"}),
        (Post, "post", {"data": "data"}),
    ],
)
async def test_cache_response(
    client_cls: Type[HttpClient],
    method: str,
    req_args: Dict[str, str],
    mock_async_client: Tuple[MagicMock, AsyncMock],
    test_data: Dict[str, Any],
) -> None:
    mock_client, _ = mock_async_client
    client = client_cls()
    args = {
        "url": test_data["url"],
        "headers": test_data["headers"],
        "auth": test_data["auth"],
    }
    if "data" in req_args:
        args["data"] = test_data["data"]
    if "params" in req_args:
        args["params"] = test_data["params"]

    response1 = await client.send(**args)
    response2 = await client.send(**args)
    assert getattr(mock_client.__aenter__.return_value, method).call_count == 1
    assert response1 == response2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_cls, method, req_args",
    [
        (Get, "get", {"params": "params"}),
        (Post, "post", {"data": "data"}),
    ],
)
async def test_cache_expires_after_default_ttl(
    client_cls: Type[HttpClient],
    method: str,
    req_args: Dict[str, str],
    mock_async_client: Tuple[MagicMock, AsyncMock],
    test_data: Dict[str, Any],
) -> None:
    mock_client, mock_response = mock_async_client
    client = client_cls()
    args = {
        "url": test_data["url"],
        "headers": test_data["headers"],
        "auth": test_data["auth"],
    }
    if "data" in req_args:
        args["data"] = test_data["data"]
    if "params" in req_args:
        args["params"] = test_data["params"]

    with patch.dict(os.environ, {}, clear=True):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            mock_time.time.return_value = 1000
            response1 = await client.send(**args)
            mock_time.time.return_value = 1000 + 599
            response2 = await client.send(**args)
            assert response1 == response2
            mock_time.time.return_value = 1000 + 601
            response3 = await client.send(**args)
            assert getattr(mock_client.__aenter__.return_value, method).call_count == 2
            assert response3 == mock_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_cls, method, req_args",
    [
        (Get, "get", {"params": "params"}),
        (Post, "post", {"data": "data"}),
    ],
)
async def test_cache_ttl_can_be_set_by_env(
    client_cls: Type[HttpClient],
    method: str,
    req_args: Dict[str, str],
    mock_async_client: Tuple[MagicMock, AsyncMock],
    test_data: Dict[str, Any],
) -> None:
    mock_client, mock_response = mock_async_client
    client = client_cls()
    args = {
        "url": test_data["url"],
        "headers": test_data["headers"],
        "auth": test_data["auth"],
    }
    if "data" in req_args:
        args["data"] = test_data["data"]
    if "params" in req_args:
        args["params"] = test_data["params"]

    with patch.dict(os.environ, {"KAONAVI_API_CACHE_TTL_MINUTES": "2"}):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            mock_time.time.return_value = 1000
            response1 = await client.send(**args)
            mock_time.time.return_value = 1000 + 119
            response2 = await client.send(**args)
            assert response1 == response2
            mock_time.time.return_value = 1000 + 121
            response3 = await client.send(**args)
            assert getattr(mock_client.__aenter__.return_value, method).call_count == 2
            assert response3 == mock_response
