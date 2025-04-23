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

## 使用例
1. リポジトリのクローン
```bash
git clone <repository-url>
cd kaonavi_api_executor
```
2. uvのインストール
```bash
# Windows PowerShellを使用している場合
irm https://astral.sh/uv/install.ps1 | iex
# Ubuntuを使用している場合
curl -sSfL https://astral.sh/uv/install.sh | sh
```
3. 実行
```bash
uv run python -m src.kaonavi_api_executor.main 
```

## License

This project is licensed under the [MIT License](./LICENSE).

