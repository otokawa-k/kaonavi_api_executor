import os
from requests.auth import HTTPBasicAuth
from ..http_client.http_client import HttpClient


class ApiAccessTokenFetcher:
    def __init__(self, client: HttpClient):
        self.client = client
        self.consumer_key = os.getenv('KAONAVI_CONSUMER_KEY')
        self.consumer_secret = os.getenv('KAONAVI_CONSUMER_SECRET')
        url = os.getenv('KAONAVI_API_URL', 'https://api.kaonavi.jp/api/v2.0')
        self.url = f"{url}/token"
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError(
                "Consumer key and secret must be set in environment variables.")

    def fetch_access_token(self) -> str:
        response = self.client.send(
            url=self.url,
            data='grant_type=client_credentials',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )
        # responseをjson形式で取得
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch access token: {response.status_code} {response.text}")
        # responseをjson形式で取得
        response_json = response.json()
        # access_tokenを取得
        access_token = response_json.get('access_token')
        if not access_token:
            raise Exception("Access token not found in response.")
        return access_token
