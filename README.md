# Kaonavi API Executor

## 概要
カオナビのAPIを実行するためのPythonライブラリです。
カオナビAPIv2のアクセストークンを取得し、APIモデルに基づいてAPIを実行します。

## 主な機能
- カオナビAPIv2のアクセストークンを取得: [ApiAccessTokenFetcher](./src/kaonavi_api_executor/auth/api_access_token_fetcher.py)
- カオナビAPIv2をAPIモデルに基づいて実行: [ApiExecutor](./src/kaonavi_api_executor/api_executor.py)
  - メンバー一覧の取得: [GetMembersApi](./src/kaonavi_api_executor/api/get_members_api.py)
  - シート情報の取得: [GetSheetsApi](./src/kaonavi_api_executor/api/get_sheets_api.py)
- メンバー一覧のmember_dataをpandas.DataFrameに変換: [MembersMemberDataFlattener](./src/kaonavi_api_executor/transformers/members_member_data_flattener.py)
- シート情報のmember_dataをpandas.DataFrameに変換: [SheetsMemberDataFlattener](./src/kaonavi_api_executor/transformers/sheets_member_data_flattener.py)

## モジュール構成
- `api_executor.py`: API実行クラス
- `auth/`: 認証関連
- `api/`: APIモデル定義
- `transformers/`: データ変換
- `http_client/`: HTTP通信
- `types/`: 型定義

## インストール方法

### ソースからビルドする場合
1. パッケージのビルド
```bash
uv pip install build
uv build
```

2. ビルドされたパッケージのインストール
```bash
uv pip install dist/kaonavi_api_executor-<version>-py3-none-any.whl
```

### GitHubリリースからインストールする場合
1. GitHub[リリースページ](../../releases)から最新の.whlファイルをダウンロード

2. ダウンロードしたパッケージのインストール
```bash
uv pip install kaonavi_api_executor-<version>-py3-none-any.whl
```

## 使用例
実行前に、以下の環境変数を事前に設定してください：

| 変数名                  | 説明                               |
| ----------------------- | ---------------------------------- |
| KAONAVI_CONSUMER_KEY    | カオナビ公開APIv2のConsumer Key    |
| KAONAVI_CONSUMER_SECRET | カオナビ公開APIv2のConsumer Secret |

```python
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_members_api import GetMembersApi
from kaonavi_api_executor.http_client.http_methods import Post
from kaonavi_api_executor.transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)

async def main() -> None:
    # アクセストークンの取得
    fetcher = ApiAccessTokenFetcher(Post())
    token = await fetcher.fetch_access_token()

    # メンバー情報の取得
    api = GetMembersApi(token=token)
    api_executor = ApiExecutor(api)
    result = await api_executor.execute()

    # メンバー情報の変換
    flattener = MembersMemberDataFlattener(result)
    df = flattener.flatten()
```

## 開発者向け
1. リポジトリのクローン
```bash
git clone <repository-url>
cd kaonavi_api_executor
```

2. 開発環境のセットアップ
```bash
# uvのインストール (Windows PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
# または (Ubuntu)
curl -sSfL https://astral.sh/uv/install.sh | sh
```

3. テスト実行
```bash
# UTを実行する場合
uv run pytest tests/unit
# ITを実行する場合
uv run pytest tests/integration
```

## License
This project is licensed under the [MIT License](./LICENSE).
