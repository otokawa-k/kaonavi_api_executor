from typing import Generator, Tuple
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import os
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


@pytest.mark.asyncio
async def test_get_caches_response(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    """
    同一リクエスト内容の場合、2回目以降はAPIを実行せずキャッシュを返却することを確認するテスト
    """
    mock_client, mock_response = mock_async_client
    get_client = Get()

    url = "https://mocked-url.com"
    params = {"query": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    # 1回目: API呼び出し
    response1 = await get_client.send(
        url=url, params=params, headers=headers, auth=auth
    )
    # 2回目: キャッシュ返却（API呼び出しなしを期待）
    response2 = await get_client.send(
        url=url, params=params, headers=headers, auth=auth
    )

    # 1回目は呼ばれる
    assert mock_client.__aenter__.return_value.get.call_count == 1
    # 2回目は呼ばれない（キャッシュ返却）
    assert response1 == response2


@pytest.mark.asyncio
async def test_post_caches_response(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    """
    同一リクエスト内容の場合、2回目以降はAPIを実行せずキャッシュを返却することを確認するテスト
    """
    mock_client, mock_response = mock_async_client
    post_client = Post()

    url = "https://mocked-url.com"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    # 1回目: API呼び出し
    response1 = await post_client.send(url=url, data=data, headers=headers, auth=auth)
    # 2回目: キャッシュ返却（API呼び出しなしを期待）
    response2 = await post_client.send(url=url, data=data, headers=headers, auth=auth)

    # 1回目は呼ばれる
    assert mock_client.__aenter__.return_value.post.call_count == 1
    # 2回目は呼ばれない（キャッシュ返却）
    assert response1 == response2


@pytest.mark.asyncio
async def test_get_cache_expires_after_default_ttl(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    get_client = Get()

    url = "https://mocked-url.com"
    params = {"query": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
        # 開始時刻
        mock_time.time.return_value = 1000
        response1 = await get_client.send(
            url=url, params=params, headers=headers, auth=auth
        )
        # 10分以内（+599秒）はキャッシュ
        mock_time.time.return_value = 1000 + 599
        response2 = await get_client.send(
            url=url, params=params, headers=headers, auth=auth
        )
        assert response1 == response2
        # 10分後（+601秒）はキャッシュ切れ
        mock_time.time.return_value = 1000 + 601
        response3 = await get_client.send(
            url=url, params=params, headers=headers, auth=auth
        )
        # 2回目のAPI呼び出しが発生する
        assert mock_client.__aenter__.return_value.get.call_count == 2
        assert response3 == mock_response


@pytest.mark.asyncio
async def test_get_cache_ttl_can_be_set_by_env(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    get_client = Get()

    url = "https://mocked-url.com"
    params = {"query": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch.dict(os.environ, {"KAONAVI_API_CACHE_TTL_MINUTES": "2"}):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            mock_time.time.return_value = 1000
            response1 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            # 2分以内（+119秒）はキャッシュ
            mock_time.time.return_value = 1000 + 119
            response2 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            assert response1 == response2
            # 2分経過後（+121秒）はキャッシュ切れ
            mock_time.time.return_value = 1000 + 121
            response3 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            assert mock_client.__aenter__.return_value.get.call_count == 2
            assert response3 == mock_response


@pytest.mark.asyncio
async def test_get_cache_ttl_env_default_10min(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    get_client = Get()

    url = "https://mocked-url.com"
    params = {"query": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch.dict(os.environ, {}, clear=True):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            # 開始時刻
            mock_time.time.return_value = 1000
            response1 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            # 10分以内（+599秒）はキャッシュ
            mock_time.time.return_value = 1000 + 599
            response2 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            assert response1 == response2
            # 10分後（+601秒）はキャッシュ切れ
            mock_time.time.return_value = 1000 + 601
            response3 = await get_client.send(
                url=url, params=params, headers=headers, auth=auth
            )
            # 2回目のAPI呼び出しが発生する
            assert mock_client.__aenter__.return_value.get.call_count == 2
            assert response3 == mock_response


@pytest.mark.asyncio
async def test_post_cache_expires_after_default_ttl(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    post_client = Post()

    url = "https://mocked-url.com"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
        # 開始時刻
        mock_time.time.return_value = 1000
        response1 = await post_client.send(
            url=url, data=data, headers=headers, auth=auth
        )
        # 10分以内（+599秒）はキャッシュ
        mock_time.time.return_value = 1000 + 599
        response2 = await post_client.send(
            url=url, data=data, headers=headers, auth=auth
        )
        assert response1 == response2
        # 10分後（+601秒）はキャッシュ切れ
        mock_time.time.return_value = 1000 + 601
        response3 = await post_client.send(
            url=url, data=data, headers=headers, auth=auth
        )
        # 2回目のAPI呼び出しが発生する
        assert mock_client.__aenter__.return_value.post.call_count == 2
        assert response3 == mock_response


@pytest.mark.asyncio
async def test_post_cache_ttl_can_be_set_by_env(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    post_client = Post()

    url = "https://mocked-url.com"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch.dict(os.environ, {"KAONAVI_API_CACHE_TTL_MINUTES": "2"}):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            # 開始時刻
            mock_time.time.return_value = 1000
            response1 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            # 2分以内（+119秒）はキャッシュ
            mock_time.time.return_value = 1000 + 119
            response2 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            assert response1 == response2
            # 2分経過後（+121秒）はキャッシュ切れ
            mock_time.time.return_value = 1000 + 121
            response3 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            # 2回目のAPI呼び出しが発生する
            assert mock_client.__aenter__.return_value.post.call_count == 2
            assert response3 == mock_response


@pytest.mark.asyncio
async def test_post_cache_ttl_env_default_10min(
    mock_async_client: Tuple[MagicMock, AsyncMock],
) -> None:
    mock_client, mock_response = mock_async_client
    post_client = Post()

    url = "https://mocked-url.com"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    auth = None

    with patch.dict(os.environ, {}, clear=True):
        with patch("kaonavi_api_executor.http_client.http_methods.time") as mock_time:
            # 開始時刻
            mock_time.time.return_value = 1000
            response1 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            # 10分以内（+599秒）はキャッシュ
            mock_time.time.return_value = 1000 + 599
            response2 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            assert response1 == response2
            # 10分後（+601秒）はキャッシュ切れ
            mock_time.time.return_value = 1000 + 601
            response3 = await post_client.send(
                url=url, data=data, headers=headers, auth=auth
            )
            # 2回目のAPI呼び出しが発生する
            assert mock_client.__aenter__.return_value.post.call_count == 2
            assert response3 == mock_response
