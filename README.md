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

## ライセンス
MIT License

Copyright (c) 2025 Your Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
