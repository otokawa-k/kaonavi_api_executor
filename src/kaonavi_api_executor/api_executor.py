from typing import Generic

from .http_client.http_methods import Post
from .auth.access_token import AccessToken
from .api.api_model import ApiModel
from .types.typevars import TResponse


class ApiExecutor:
    def __init__(self) -> None:
        self.access_token = AccessToken(http_method=Post())

    async def execute(self, api: ApiModel[TResponse]) -> TResponse:
        if not api.url:
            raise ValueError("API URL is not set.")

        headers = {
            **api.headers,
            "Content-Type": "application/json",
            "Kaonavi-Token": await self.access_token.get(),
        }

        response = await api.http_method.send(
            url=api.url,
            params=api.params,
            headers=headers,
            auth=api.auth,
            data=api.data,
        )

        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

        return api.parse_response(response.json())
