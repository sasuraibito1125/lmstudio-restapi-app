# lmstudio-restapi-app

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen?logo=python&logoColor=white)
![LM Studio](https://img.shields.io/badge/LM%20Studio-AI%20Model%20Interface-blue?logo=opensourceinitiative&logoColor=white)
![Google Antigravity](https://img.shields.io/badge/Google%20Antigravity-Developer%20Tool-lightgrey?logo=google&logoColor=white)

[LM Studio](https://lmstudio.ai/)のローカルサーバにLM Studio APIのREST APIでアクセスするサンプルアプリケーションです。

## ディレクトリ構成
<details>
<summary>ディレクトリ構成</summary>

```text
.
│  .env.example
│  .gitignore
│  config.py
│  LICENSE
│  main.py
│  README.md
│  requirements.txt
│  start_app.sh
│  start_ut.sh
│  
├─.agents
│  ├─rules
│  │      coding.md
│  │      common.md
│  │      python.md
│  │      test-python.md
│  │      
│  ├─skills
│  │  ├─code-review
│  │  │      SKILL.md
│  │  │      
│  │  ├─design-review
│  │  │      SKILL.md
│  │  │      
│  │  └─python-review
│  │          SKILL.md
│  │          
│  └─workflows
│          design.md
│          dev.md
│          init.md
│          review.md
│          test.md
│          
├─docs
│      Creating LM Studio REST App.md
│      implementation_plan.md
│      task.md
│      walkthrough.md
│      
├─images
│      Developer Docs.png
│      
└─tests
        requirements-dev.txt
        test_config.py
        test_main.py
```
</details>

## アプリケーションの開発について

ほとんどの実装を[Google Antigravity](https://antigravity.google/)のエージェント機能で生成しました。

### エージェント

グローバルな設定ファイル（`~/.gemini`配下の各種ファイル）がありますが，開発以外のドキュメント作成と共有できるかなり汎用的な設定ファイルです（「回答は日本語優先する」など）。

開発については実質的にこのフォルダの[`.agents`](.agents/)の各種設定でAntigravityのエージェントが動作しました。

※実際には`.agents`はそれらの親フォルダに配置して開発しています。

前提として同じ構成のOpenAI SDKアプリとLM Studio SDK（`lmstudio-python`）アプリを開発しており，エージェントにはその構成を参考にするように指示しています（詳細は「[チャット履歴のエクスポート](docs/Creating%20LM%20Studio%20REST%20App.md)」を参照）。

※元々のフォルダ名は`restapi-app`で，Githubにアップロードする際に`lmstudio-restapi-app`に変更しました。そのため，チャット履歴では元のフォルダ名となっています。

Antigravityで利用したエージェントは以下のとおりです。

- Conversation Mode
  - Planning
- Model
  - Gemini 3.1 Pro(High)

### エージェント関連のドキュメント

- [チャット履歴のエクスポート](docs/Creating%20LM%20Studio%20REST%20App.md) 
  - このアプリでの全やり取り
- [実装計画](docs/implementation_plan.md)
- [タスク](docs/task.md)
- [ウォークスルー](docs/walkthrough.md)

## アプリケーションの実行について

## LM Studio

### モデルのダウンロード

あらかじめいくつかのLLMモデルをダウンロードしておきます。

※動作確認では[`google/gemma-3-27b`](https://lmstudio.ai/models/google/gemma-3-27b)を使用しました。

### ローカルサーバの起動

LM Studioでローカルサーバを起動しておきます。

詳細についてはLM StudioのDeveloper Docs（下記イメージ参照）または[LM Studioのドキュメント](https://lmstudio.ai/docs/developer/core/server)を参照。

<details>
<summary>LM StudioのDeveloper Docs画面</summary>

![LM StudioのDeveloper Docs画面](./images/Developer%20Docs.png)
</details>

### APIトークンの生成

LM StudioでAPIトークンを生成します。

詳細についてはLM StudioのDeveloper Docsまたは公式サイト文書の[Authentication](https://lmstudio.ai/docs/developer/core/authentication)を参照。

## 環境変数の設定

`.env.example`をコピーして`.env`を作成し、環境変数を設定します。

```bash
cp .env.example .env
```

前の手順で生成したAPIトークンも設定します。

## UT

UTを実行します。

```bash
./start_ut.sh
```

## 実行方法

1. アプリケーションを実行します。

```bash
./start_app.sh
```

2. モデル選択画面が表示されるので、モデルを選択します。

3. メッセージ入力のプロンプトが表示されるので、メッセージを入力します。
