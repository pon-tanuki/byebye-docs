# byebye-docs MCP Server

byebye-docs用のMCPサーバーです。
Claude CodeやClaude Desktopと連携して、`.agent/` ドキュメントの作成・更新・検証をサポートします。

## 機能

### Resources（リソース）

| URI | 説明 |
|-----|------|
| `template://structure` | テンプレートの構造情報（どのセクションがあるか、必須項目は何か） |
| `template://schema` | 各ドキュメントの検証スキーマ |
| `project://current` | 現在のプロジェクト情報 |
| `docs://list` | プロジェクト内の既存ドキュメント一覧 |

### Tools（ツール）

| ツール名 | 説明 |
|---------|------|
| `list_templates` | 利用可能なテンプレート一覧を取得 |
| `create_document` | テンプレートから新規ドキュメントを作成 |
| `get_section` | ドキュメントの特定セクションの内容を取得 |
| `update_section` | ドキュメントの特定セクションを更新（マーカーベース） |
| `validate_document` | ドキュメントが規定の構造に従っているか検証 |
| `fill_metadata` | プロジェクト情報からメタデータを自動入力 |

### Prompts（プロンプト）

| プロンプト名 | 説明 |
|-------------|------|
| `design-review` | 設計レビュー用のワークフロー |
| `update-architecture` | アーキテクチャ図更新のガイド |
| `sync-with-code` | コードとの整合性チェック |

## インストール

### 前提条件

- Python 3.10以上
- uv（推奨）または pip

### uvを使用する場合

```bash
cd mcp-server
uv sync
```

### pipを使用する場合

```bash
cd mcp-server
pip install -e .
```

## Claude Codeでの設定

`claude_desktop_config.json`（または同等の設定ファイル）に以下を追加:

```json
{
  "mcpServers": {
    "byebye-docs": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "./mcp-server",
        "run",
        "byebye-docs"
      ],
      "env": {
        "BYEBYE_DOCS_PROJECT_PATH": "."
      }
    }
  }
}
```

### 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `BYEBYE_DOCS_PROJECT_PATH` | 対象プロジェクトのルートパス | カレントディレクトリ |

## 使用例

### テンプレート一覧の取得

```
list_templates(category="product")
```

### 新規ドキュメントの作成

```
create_document(
    template_type="vision.md",
    output_path="docs/product/vision.md",
    metadata={
        "project_name": "My Project",
        "author": "Claude Agent"
    }
)
```

### ドキュメントの検証

```
validate_document(document_path="docs/product/requirements.yaml")
```

### セクションの更新

マーカーを使用したセクション更新:

```markdown
<!-- AI_EDITABLE_START: features -->
現在の機能一覧
<!-- AI_EDITABLE_END: features -->
```

```
update_section(
    document_path="docs/product/vision.md",
    section_name="features",
    new_content="新しい機能一覧の内容"
)
```

## 開発

### テストの実行

```bash
cd mcp-server
uv run pytest
```

### Lintの実行

```bash
cd mcp-server
uv run ruff check .
uv run ruff format .
```

## 対応テンプレート

### Product（プロダクト）

- `vision.md` - プロダクトビジョン（必須）
- `requirements.yaml` - 機能要件定義（必須）
- `nonfunctional_requirements.yaml` - 非機能要件
- `user_scenarios.md` - ユーザーシナリオ

### Architecture（アーキテクチャ）

- `system_overview.md` - システム概要（必須）
- `domain_model.md` - ドメインモデル
- `sequence_diagrams.md` - シーケンス図
- `api_design/openapi.yaml` - API設計
- `data_schemas/entities.yaml` - エンティティ定義

### Agent（エージェント）

- `roles.yaml` - 役割定義（必須）
- `constraints.yaml` - 制約条件（必須）
- `behaviours.md` - 行動規則
- `tools/available_tools.md` - 利用可能ツール

### Dev Process（開発プロセス）

- `coding_standards.md` - コーディング規約（必須）
- `branch_strategy.md` - ブランチ戦略
- `review_guidelines.md` - レビューガイドライン

### Ops（運用）

- `ci_cd_pipeline.md` - CI/CDパイプライン
- `monitoring_plan.md` - 監視計画
- `logs_schema.yaml` - ログスキーマ

## ライセンス

MIT License
