from typing import Generic
from .http_client.http_client import HttpClient
from .api.api_model import ApiModel
from .types.typevars import TResponse


class ApiExecutor(Generic[TResponse]):
    def __init__(self, api: ApiModel[TResponse]):
        self.api = api
        self.client: HttpClient = self.api.method

    async def execute(self) -> TResponse:
        if not self.api.url:
            raise ValueError("API URL is not set.")

        response = await self.client.send(
            url=self.api.url,
            params=self.api.params,
            headers=self.api.headers,
            auth=self.api.auth,
            data=self.api.data,
        )

        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

        return self.api.parse_response(response.json())
