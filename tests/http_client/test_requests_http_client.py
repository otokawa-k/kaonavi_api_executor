from kaonavi_api_executor.http_client.requests_http_client import RequestsHttpClient
from unittest.mock import patch, MagicMock


def test_requests_http_client_post():
    client = RequestsHttpClient()

    with patch("src.kaonavi_api_executor.http_client.requests_http_client.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_post.return_value = mock_response

        url = "https://example.com"
        data = {"key": "value"}
        headers = {"Content-Type": "application/json"}
        auth = MagicMock()

        response = client.post(url=url, data=data, headers=headers, auth=auth)

        mock_post.assert_called_once_with(
            url, data=data, headers=headers, auth=auth)
        assert response == mock_response


def test_requests_http_client_get():
    client = RequestsHttpClient()

    with patch("src.kaonavi_api_executor.http_client.requests_http_client.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        url = "https://example.com"
        params = {"key": "value"}
        headers = {"Content-Type": "application/json"}
        auth = MagicMock()

        response = client.get(url=url, params=params,
                              headers=headers, auth=auth)

        mock_get.assert_called_once_with(
            url, params=params, headers=headers, auth=auth)
        assert response == mock_response
