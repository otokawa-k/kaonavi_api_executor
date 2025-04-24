# カオナビAPI実行ツール

## 概要
カオナビのAPIを簡単に実行するためのPythonライブラリです。

## 主な機能
- アクセストークンの取得
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
# pipを使用する場合
pip install build
python -m build

# uvを使用する場合
uv pip install build
python -m build
```

2. ビルドされたパッケージのインストール
```bash
# pipを使用する場合
pip install dist/*.whl

# uvを使用する場合
uv pip install dist/*.whl
```

### GitHubリリースからインストールする場合

1. [GitHubリリースページ](https://github.com/[username]/kaonavi-api-executor/releases)から最新の.whlファイルをダウンロード

2. ダウンロードしたパッケージのインストール
```bash
# pipを使用する場合
pip install kaonavi_api_executor-0.1.0-py3-none-any.whl

# uvを使用する場合
uv pip install kaonavi_api_executor-0.1.0-py3-none-any.whl
```

## 使用例

```python
from kaonavi_api_executor.auth.api_access_token_fetcher import ApiAccessTokenFetcher
from kaonavi_api_executor.api_executor import ApiExecutor
from kaonavi_api_executor.api.get_member_api import GetMemberApi
from kaonavi_api_executor.http_client.http_methods import Post

# アクセストークンの取得
fetcher = ApiAccessTokenFetcher(Post())
token = fetcher.fetch_access_token()

# メンバー情報の取得
api_model = GetMemberApi(token=token)
api_executor = ApiExecutor(api_model)
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

# 開発用依存関係のインストール
uv pip install -e ".[dev]"
```

3. テスト実行
```bash
pytest
```

## License

This project is licensed under the [MIT License](./LICENSE).
