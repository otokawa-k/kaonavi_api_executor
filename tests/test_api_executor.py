import pytest
import os
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_member_api import GetMemberApi
from .mocks.mock_api_model import MockApiModel


def test_api_executor():
    mock_api = MockApiModel(token="mocked-token")
    api_executor = ApiExecutor(mock_api)

    result = api_executor.execute()

    assert result.id == "12345"
    assert result.name == "テスト名称"

@pytest.mark.online
def test_api_executor_online():
    token = os.getenv('KAONAVI_AUTH_TOKEN')
    api = GetMemberApi(token=token)
    api_executor = ApiExecutor(api)

    result = api_executor.execute()

    assert result.updated_at is not None, "updated_at should not be None"
    assert result.member_data is not None, "member_data should not be None"
    assert isinstance(result.member_data, list), "member_data should be a list"