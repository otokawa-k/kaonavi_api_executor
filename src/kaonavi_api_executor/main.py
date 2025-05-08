import asyncio

from .auth.api_access_token_fetcher import ApiAccessTokenFetcher
from .api_executor import ApiExecutor
from .api.get_members_api import GetMembersApi
from .http_client.http_methods import Post
from .transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)


async def main() -> None:
    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    api = GetMembersApi(token=token)
    api_executor = ApiExecutor(api)
    result = await api_executor.execute()

    flattener = MembersMemberDataFlattener(result)
    df = flattener.flatten()

    print(df.head())


if __name__ == "__main__":
    asyncio.run(main())
