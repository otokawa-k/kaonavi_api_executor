from typing import Generator, Tuple
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from kaonavi_api_executor.http_client.http_methods import Post, Get


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
async def test_post(mock_async_client: Tuple[MagicMock, AsyncMock]) -> None:
    mock_client, mock_response = mock_async_client

    post_client = Post()

    url = "https://mocked-url.com"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    response = await post_client.send(url=url, data=data, headers=headers, auth=auth)

    mock_client.__aenter__.return_value.post.assert_called_once_with(
        url=url,
        data=data,
        headers=headers,
    )
    assert response == mock_response


@pytest.mark.asyncio
async def test_get(mock_async_client: Tuple[MagicMock, AsyncMock]) -> None:
    mock_client, mock_response = mock_async_client

    get_client = Get()

    url = "https://mocked-url.com"
    params = {"query": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    response = await get_client.send(url=url, params=params, headers=headers, auth=auth)

    mock_client.__aenter__.return_value.get.assert_called_once_with(
        url=url,
        params=params,
        headers=headers,
    )
    assert response == mock_response
