import pytest
from kaonavi_api_executor.api_executor import ApiExecutor
from .mocks.mock_api_model import MockApiModel


@pytest.mark.asyncio
async def test_api_executor() -> None:
    api_executor = ApiExecutor()

    mock_api = MockApiModel()
    result = await api_executor.execute(mock_api)

    assert result.id == "12345"
    assert result.name == "テスト名称"
