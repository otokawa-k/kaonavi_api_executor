# カオナビAPI実行ツール

## 概要
カオナビのAPIを簡単に実行するためのPythonライブラリです。

## 主な機能
- メンバー情報の取得

## モジュール構成
- `auth/`: 認証関連
- `api/`: APIモデル定義
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
1. GitHubリリースページから最新の.whlファイルをダウンロード

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

# アクセストークンの取得
fetcher = ApiAccessTokenFetcher(Post())
token = fetcher.fetch_access_token()

# メンバー情報の取得
api = GetMembersApi(token=token)
api_executor = ApiExecutor(api)
response = api_executor.execute()
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
uv run pytest
# APIを実行せずにテストする場合
uv run pytest -m "not online"
```

## License
This project is licensed under the [MIT License](./LICENSE).
