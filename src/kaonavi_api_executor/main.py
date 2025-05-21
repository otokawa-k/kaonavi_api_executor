import asyncio

from .auth.access_token import AccessToken
from .api_executor import ApiExecutor
from .api.get_members_api import GetMembersApi
from .http_client.http_methods import Post
from .transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)


async def main() -> None:
    access_token = AccessToken(http_method=Post())
    api = GetMembersApi()
    members_api_executor = ApiExecutor(access_token=access_token, api=api)
    result = await members_api_executor.execute()

    flattener = MembersMemberDataFlattener(result)
    df_main, df_sub = flattener.flatten()

    print(df_main.head())
    print(df_sub.head())


if __name__ == "__main__":
    asyncio.run(main())
