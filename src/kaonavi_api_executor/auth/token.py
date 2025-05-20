import os
import time
from typing import Optional
from httpx import BasicAuth
from ..http_client.http_client import HttpClient


class Token:
    def __init__(self, http_method: HttpClient) -> None:
        self._http_method = http_method
        self.consumer_key = os.getenv("KAONAVI_CONSUMER_KEY")
        self.consumer_secret = os.getenv("KAONAVI_CONSUMER_SECRET")
        url = os.getenv("KAONAVI_API_URL", "https://api.kaonavi.jp/api/v2.0")
        self.url = f"{url}/token"
        self._token: Optional[str] = None
        self._expires_at: int = int(time.time()) - 60

    async def get(self) -> str:
        now = int(time.time())
        if self._token is None or now >= self._expires_at:
            await self._fetch_token()
            if self._token is None:
                raise ValueError("Token is None after fetching.")
        return self._token

    async def _fetch_token(self) -> None:
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError(
                "Consumer key and secret must be set in environment variables."
            )

        response = await self._http_method.send(
            url=self.url,
            data="grant_type=client_credentials",
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
            auth=BasicAuth(self.consumer_key, self.consumer_secret),
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch access token: {response.status_code} {response.text}"
            )

        response_json = response.json()
        token = response_json.get("access_token")
        expire_in = response_json.get("expire_in")
        if token is None:
            raise Exception("Access token not found in response.")
        self._token = token
        self._expires_at = int(time.time()) + int(expire_in) - 60
