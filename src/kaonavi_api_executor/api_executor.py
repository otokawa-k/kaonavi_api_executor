from typing import Generic

from .auth.access_token import AccessToken
from .api.api_model import ApiModel
from .types.typevars import TResponse


class ApiExecutor(Generic[TResponse]):
    def __init__(self, access_token: AccessToken, api: ApiModel[TResponse]) -> None:
        self.access_token = access_token
        self.api = api

    async def execute(self) -> TResponse:
        if not self.api.url:
            raise ValueError("API URL is not set.")

        headers = {
            **self.api.headers,
            "Content-Type": "application/json",
            "Kaonavi-Token": await self.access_token.get(),
        }

        response = await self.api.http_method.send(
            url=self.api.url,
            params=self.api.params,
            headers=headers,
            auth=self.api.auth,
            data=self.api.data,
        )

        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

        return self.api.parse_response(response.json())
