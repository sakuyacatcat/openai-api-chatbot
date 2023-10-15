# OpenAI GPT-3 Chatbot with Flask

## Overview

このプロジェクトは OpenAI の GPT-3 モデルを使ったシンプルなチャットボットの例です。Flask で Web API として実装しています。

## Prerequisites

- Docker
- Docker Compose

## Setup

### Environment Variables

環境変数の設定は `.env` ファイルに記載します。サンプルとして `.env.example` がプロジェクトに含まれています。

```bash
cp .env.example .env
```

その後、`.env` ファイルを開き `API_KEY` の値を適切な OpenAI の API キーに置き換えてください。

### Build and Run

Docker Compose を使ってアプリケーションと依存関係をビルドおよび実行します。

```bash
docker-compose down
docker-compose build
docker-compose up
```

アプリケーションは [http://localhost:3000](http://localhost:3000) でアクセス可能です。

## Usage

### Chat API

チャットエンドポイントには POST リクエストを使ってアクセスします。以下は `curl` コマンドの例です。

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"user_input":"Hello, how are you?"}' \
     http://localhost:3000/chat
```

このリクエストに対して、GPT-3 から生成されたテキストが JSON 形式で返されます。

## License

このプロジェクトは MIT ライセンスの下で公開されています。詳細は `LICENSE` ファイルを参照してください。
