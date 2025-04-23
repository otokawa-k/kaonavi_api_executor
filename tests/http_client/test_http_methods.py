from kaonavi_api_executor.http_client.http_methods import Post, Get
from unittest.mock import patch, MagicMock


def test_post():
    post_client = Post()

    with patch("kaonavi_api_executor.http_client.http_methods.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_post.return_value = mock_response

        url = "https://example.com"
        data = {"key": "value"}
        headers = {"Content-Type": "application/json"}
        auth = MagicMock()

        response = post_client.send(url=url, data=data, headers=headers, auth=auth)

        mock_post.assert_called_once_with(
            url, data=data, headers=headers, auth=auth)
        assert response == mock_response

def test_get():
    get_client = Get()

    with patch("kaonavi_api_executor.http_client.http_methods.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        url = "https://example.com"
        params = {"query": "value"}
        headers = {"Content-Type": "application/json"}
        auth = MagicMock()

        response = get_client.send(url=url, params=params, headers=headers, auth=auth)

        mock_get.assert_called_once_with(
            url, params=params, headers=headers, auth=auth)
        assert response == mock_response