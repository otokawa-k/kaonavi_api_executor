import pytest
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_members_api import GetMembersApi
from kaonavi_api_executor.auth.access_token import AccessToken
from kaonavi_api_executor.http_client.http_methods import Post
from kaonavi_api_executor.transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)


@pytest.mark.asyncio
async def test_get_members_api() -> None:
    access_token = AccessToken(http_method=Post())
    api = GetMembersApi()
    members_api_executor = ApiExecutor(access_token=access_token, api=api)
    result = await members_api_executor.execute()

    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"

    flattener = MembersMemberDataFlattener(result)
    df_main, df_sub = flattener.flatten()
    assert df_main is not None, "df_main should not be None"
    assert df_sub is not None, "df_sub should not be None"
    assert not df_main.empty, "df_main should not be empty"
    assert not df_sub.empty, "df_sub should not be empty"
