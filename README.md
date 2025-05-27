# Kaonavi API Executor

## Overview
A Python library for executing Kaonavi APIs.
It obtains an access token for Kaonavi API v2 and executes APIs based on API models.

## Main Features
- Obtain access token for Kaonavi API v2: [AccessToken](./src/kaonavi_api_executor/auth/access_token.py)
- Execute Kaonavi API v2 based on API models: [ApiExecutor](./src/kaonavi_api_executor/api_executor.py)
  - Retrieve member list: [GetMembersApi](./src/kaonavi_api_executor/api/get_members_api.py)
  - Retrieve sheet information: [GetSheetsApi](./src/kaonavi_api_executor/api/get_sheets_api.py)
- Convert member_data from member list to pandas.DataFrame: [MembersMemberDataFlattener](./src/kaonavi_api_executor/transformers/members_member_data_flattener.py)
- Convert member_data from sheet information to pandas.DataFrame: [SheetsMemberDataFlattener](./src/kaonavi_api_executor/transformers/sheets_member_data_flattener.py)

## Module Structure
- `api_executor.py`: API execution class
- `auth/`: Authentication related
- `api/`: API model definitions
- `transformers/`: Data transformation
- `http_client/`: HTTP communication
- `types/`: Type definitions

## Installation

### Build from source
1. Build the package
    ```bash
    uv pip install build
    uv build
    ```

2. Install the built package
    ```bash
    uv pip install dist/kaonavi_api_executor-<version>-py3-none-any.whl
    ```

### Install from GitHub Release
1. Download the latest .whl file from the GitHub [Releases page](../../releases)

2. Install the downloaded package
    ```bash
    uv pip install kaonavi_api_executor-<version>-py3-none-any.whl
    ```

## Usage Example
Before running, set the following environment variables:

| Variable Name           | Description                               |
| ----------------------- | ----------------------------------------- |
| KAONAVI_CONSUMER_KEY    | Consumer Key for Kaonavi Public API v2    |
| KAONAVI_CONSUMER_SECRET | Consumer Secret for Kaonavi Public API v2 |

```python
from kaonavi_api_executor.auth.access_token import AccessToken
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_members_api import GetMembersApi
from kaonavi_api_executor.http_client.http_methods import Post
from kaonavi_api_executor.transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)

async def main() -> None:
    # Retrieve member information
    access_token = AccessToken(http_method=Post())
    api = GetMembersApi()
    members_api_executor = ApiExecutor(access_token=access_token, api=api)
    result = await members_api_executor.execute()

    # Transform member information
    flattener = MembersMemberDataFlattener(result)
    df_main, df_sub = flattener.flatten() # df_main: DataFrame of member info, df_sub: DataFrame of concurrent positions
```

## For Developers
1. Clone the repository
    ```bash
    git clone <repository-url>
    cd kaonavi_api_executor
    ```

2. Set up the development environment
    ```bash
    # Install uv (Windows PowerShell)
    irm https://astral.sh/uv/install.ps1 | iex
    # Or (Ubuntu)
    curl -sSfL https://astral.sh/uv/install.sh | sh
    ```

3. Run tests
    ```bash
    # Run unit tests
    uv run pytest tests/unit
    # Run integration tests
    uv run pytest tests/integration
    ```

## License
This project is licensed under the [MIT License](./LICENSE).
