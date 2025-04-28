import asyncio
from .auth.api_access_token_fetcher import ApiAccessTokenFetcher
from .api_executor import ApiExecutor
from .api.get_members_api import GetMembersApi
from .http_client.http_methods import Post


async def main() -> None:
    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    api = GetMembersApi(token=token)
    api_executor = ApiExecutor(api)
    response = await api_executor.execute()
    print(response.updated_at)


if __name__ == "__main__":
    asyncio.run(main())
