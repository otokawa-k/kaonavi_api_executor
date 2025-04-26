import pytest
from kaonavi_api_executor.http_client.http_methods import Post, Get
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_post():
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response

    async with Post(session=mock_session) as client:
        response = await client.send(
            url="https://example.com",
            data={"key": "value"},
            headers={"Content-Type": "application/json"},
            auth=None,
        )

    mock_session.post.assert_called_once_with(
        "https://example.com",
        data={"key": "value"},
        params=None,
        headers={"Content-Type": "application/json"},
        auth=None,
    )
    assert response == mock_response


@pytest.mark.asyncio
async def test_get():
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response

    async with Get(session=mock_session) as get_client:
        url = "https://example.com"
        params = {"query": "value"}
        headers = {"Content-Type": "application/json"}
        auth = MagicMock()

        response = await get_client.send(
            url=url,
            params=params,
            headers=headers,
            auth=auth,
        )

    mock_session.get.assert_called_once_with(
        url,
        params=params,
        headers=headers,
        auth=auth,
    )
    assert response == mock_response
