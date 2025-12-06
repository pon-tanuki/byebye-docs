# AI-First Development Template

AIエージェントが自律的に読み取り・活用できるよう設計された、AI駆動開発のためのドキュメントテンプレート集です。

## 概要

本テンプレートは、AIエージェントと人間が協調してソフトウェア開発を行う「AIファースト開発」を支援するために設計されています。厳密な構造と明確な規約により、AIエージェントが自律的にドキュメントを理解し、タスクを遂行できます。

## ディレクトリ構造

```
ai-first-dev-template/
├── docs/                          # ドキュメント
│   ├── product/                   # プロダクト定義
│   │   ├── vision.md              # ビジョン・目的
│   │   ├── requirements.yaml      # 機能要件
│   │   ├── user_scenarios.md      # ユーザーシナリオ
│   │   └── nonfunctional_requirements.yaml  # 非機能要件
│   │
│   ├── architecture/              # アーキテクチャ
│   │   ├── system_overview.md     # システム概要
│   │   ├── domain_model.md        # ドメインモデル
│   │   ├── sequence_diagrams.md   # シーケンス図
│   │   ├── api_design/
│   │   │   └── openapi.yaml       # API定義
│   │   └── data_schemas/
│   │       ├── entities.yaml      # エンティティ定義
│   │       └── validation_rules.yaml  # バリデーションルール
│   │
│   ├── agent/                     # AIエージェント設定
│   │   ├── roles.yaml             # 役割定義
│   │   ├── behaviours.md          # 行動規則
│   │   ├── constraints.yaml       # 制約条件
│   │   └── tools/
│   │       ├── available_tools.md # 利用可能ツール
│   │       └── tool_schemas.yaml  # ツールスキーマ
│   │
│   ├── dev_process/               # 開発プロセス
│   │   ├── coding_standards.md    # コーディング規約
│   │   ├── branch_strategy.md     # ブランチ戦略
│   │   ├── agent_commit_rules.yaml  # コミットルール
│   │   └── review_guidelines.md   # レビューガイドライン
│   │
│   └── ops/                       # 運用
│       ├── ci_cd_pipeline.md      # CI/CDパイプライン
│       ├── monitoring_plan.md     # モニタリング計画
│       └── logs_schema.yaml       # ログスキーマ
│
├── project/                       # プロジェクト管理
│   ├── roadmap.md                 # ロードマップ
│   └── tasks/
│       └── initial_backlog.yaml   # 初期バックログ
│
├── generator_instructions/        # AIエージェント指示
│   ├── system_prompt.md           # システムプロンプト
│   ├── generation_rules.yaml      # 生成ルール
│   ├── file_update_policy.md      # ファイル更新ポリシー
│   └── forbidden_actions.md       # 禁止行動
│
└── meta/                          # メタ情報
    ├── glossary.md                # 用語集
    ├── dependencies.md            # 依存関係
    ├── risks.md                   # リスク管理
    └── change_history.md          # 変更履歴
```

## クイックスタート

### 自動セットアップ（推奨）

セットアップスクリプトを使用して、新しいプロジェクトを数秒で開始できます：

```bash
# curlを使用してダウンロード＆実行
curl -fsSL https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh | bash -s my-project

# または、スクリプトをダウンロードしてから実行
curl -O https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh
chmod +x setup.sh
./setup.sh my-project
```

**オプション:**
```bash
# Gitリポジトリの初期化をスキップ
./setup.sh --no-git my-project

# ヘルプを表示
./setup.sh --help
```

セットアップスクリプトは以下を自動的に実行します：
- ✅ ディレクトリ構造の作成
- ✅ すべてのテンプレートファイルのダウンロード
- ✅ プロジェクト固有ファイルの生成（.gitignore, .editorconfig等）
- ✅ Gitリポジトリの初期化（オプション）
- ✅ 初期コミットの作成

### 手動セットアップ

リポジトリをクローンして使用することもできます：

```bash
# リポジトリをクローン
git clone https://github.com/pon-tanuki/design-docs-for-ai-driven-development.git your-project-name
cd your-project-name

# テンプレートのGit履歴を削除して新規プロジェクトとして開始
rm -rf .git
git init
git add .
git commit -m "feat: initialize project with AI-first development template"
```

## 使い方

### 1. プロジェクト情報の更新

以下のファイルをプロジェクトに合わせて更新してください：

1. `docs/product/vision.md` - プロダクトビジョンの定義
2. `docs/product/requirements.yaml` - 機能要件の記述
3. `docs/architecture/system_overview.md` - システム構成の設計
4. `generator_instructions/system_prompt.md` - AIエージェントの設定

### 3. AIエージェント（Claude Code等）の使用

このテンプレートには `CLAUDE.md` が含まれており、Claude Codeやその他のAIアシスタントが自動的に参照します。

**AIエージェントが参照する主要ファイル：**
- `CLAUDE.md` - AIエージェント向け包括的指示書
- `generator_instructions/` - 行動規則と制約
- `docs/agent/` - 役割とツール定義
- `docs/dev_process/` - 開発規約

**AIエージェントでの開発開始：**
1. プロジェクトディレクトリで Claude Code を起動
2. 「機能XXXを実装して」のように指示
3. AIが自動的にドキュメントを参照し、規約に従ってコード生成

## AIエージェント向け設計方針

### 構造化されたフォーマット

- **YAML**: 機械可読なデータ定義
- **Markdown**: 人間とAI双方が読める説明文
- **一貫した命名規則**: ファイル名とセクション名の統一

### 明確な境界定義

- 許可される操作と禁止される操作の明示
- エスカレーションルールの定義
- 人間承認が必要なケースの特定

### トレーサビリティ

- 変更履歴の自動記録
- タスクとコミットの紐付け
- 意思決定プロセスのログ

## ファイル形式

| 拡張子 | 用途 |
|--------|------|
| `.md` | 説明文、ガイドライン、ドキュメント |
| `.yaml` | 構造化データ、設定、スキーマ定義 |

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更を行う場合は、まずIssueで議論してください。
