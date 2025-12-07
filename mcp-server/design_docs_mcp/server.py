"""Design Docs MCP Server implementation."""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)

# Template structure definition
TEMPLATE_STRUCTURE = {
    "docs": {
        "product": {
            "vision.md": {"required": True, "description": "プロダクトビジョン"},
            "requirements.yaml": {"required": True, "description": "機能要件定義"},
            "nonfunctional_requirements.yaml": {
                "required": False,
                "description": "非機能要件",
            },
            "user_scenarios.md": {"required": False, "description": "ユーザーシナリオ"},
        },
        "architecture": {
            "system_overview.md": {"required": True, "description": "システム概要"},
            "domain_model.md": {"required": False, "description": "ドメインモデル"},
            "sequence_diagrams.md": {"required": False, "description": "シーケンス図"},
            "api_design/openapi.yaml": {"required": False, "description": "API設計"},
            "data_schemas/entities.yaml": {"required": False, "description": "エンティティ定義"},
            "data_schemas/validation_rules.yaml": {
                "required": False,
                "description": "バリデーションルール",
            },
        },
        "dev_process": {
            "coding_standards.md": {"required": True, "description": "コーディング規約"},
            "branch_strategy.md": {"required": False, "description": "ブランチ戦略"},
            "review_guidelines.md": {"required": False, "description": "レビューガイドライン"},
            "agent_commit_rules.yaml": {"required": False, "description": "エージェントコミットルール"},
        },
        "agent": {
            "roles.yaml": {"required": True, "description": "役割定義"},
            "constraints.yaml": {"required": True, "description": "制約条件"},
            "behaviours.md": {"required": False, "description": "行動規則"},
            "tools/available_tools.md": {"required": False, "description": "利用可能ツール"},
            "tools/tool_schemas.yaml": {"required": False, "description": "ツールスキーマ"},
        },
        "ops": {
            "ci_cd_pipeline.md": {"required": False, "description": "CI/CDパイプライン"},
            "monitoring_plan.md": {"required": False, "description": "監視計画"},
            "logs_schema.yaml": {"required": False, "description": "ログスキーマ"},
        },
    },
    "generator_instructions": {
        "system_prompt.md": {"required": True, "description": "システムプロンプト"},
        "file_update_policy.md": {"required": True, "description": "ファイル更新ポリシー"},
        "forbidden_actions.md": {"required": True, "description": "禁止事項"},
        "generation_rules.yaml": {"required": False, "description": "生成ルール"},
    },
    "meta": {
        "change_history.md": {"required": False, "description": "変更履歴"},
    },
}

# Document schemas for validation
DOCUMENT_SCHEMAS = {
    "requirements.yaml": {
        "type": "object",
        "required": ["features"],
        "properties": {
            "features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name", "description"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                        "status": {"type": "string"},
                    },
                },
            }
        },
    },
    "roles.yaml": {
        "type": "object",
        "required": ["roles"],
        "properties": {
            "roles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name", "permissions"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "permissions": {"type": "array", "items": {"type": "string"}},
                    },
                },
            }
        },
    },
    "constraints.yaml": {
        "type": "object",
        "required": ["constraints"],
        "properties": {
            "constraints": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "description"],
                    "properties": {
                        "id": {"type": "string"},
                        "description": {"type": "string"},
                        "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                    },
                },
            }
        },
    },
}


def get_project_root() -> Path:
    """Get the project root directory from environment or current directory."""
    env_path = os.environ.get("DESIGN_DOCS_PROJECT_PATH")
    if env_path:
        return Path(env_path)
    return Path.cwd()


def flatten_structure(
    structure: dict[str, Any], prefix: str = ""
) -> list[dict[str, Any]]:
    """Flatten nested structure into a list of file entries."""
    result = []
    for key, value in structure.items():
        path = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict) and "required" in value:
            result.append({"path": path, **value})
        elif isinstance(value, dict):
            result.extend(flatten_structure(value, path))
    return result


def list_existing_docs(project_root: Path) -> list[dict[str, Any]]:
    """List all existing documentation files in the project."""
    docs = []
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        return docs

    for file_path in docs_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in (".md", ".yaml", ".yml"):
            rel_path = file_path.relative_to(project_root)
            stat = file_path.stat()
            docs.append({
                "path": str(rel_path),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })

    # Also check generator_instructions and meta directories
    for dir_name in ["generator_instructions", "meta"]:
        extra_dir = project_root / dir_name
        if extra_dir.exists():
            for file_path in extra_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix in (".md", ".yaml", ".yml"):
                    rel_path = file_path.relative_to(project_root)
                    stat = file_path.stat()
                    docs.append({
                        "path": str(rel_path),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    })

    return sorted(docs, key=lambda x: x["path"])


def get_project_info(project_root: Path) -> dict[str, Any]:
    """Get current project information."""
    info = {
        "root": str(project_root),
        "exists": project_root.exists(),
        "docs_count": 0,
        "has_claude_md": False,
        "categories": [],
    }

    if not project_root.exists():
        return info

    # Check for CLAUDE.md
    info["has_claude_md"] = (project_root / "CLAUDE.md").exists()

    # Count docs and identify categories
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        categories = set()
        for item in docs_dir.iterdir():
            if item.is_dir():
                categories.add(item.name)
        info["categories"] = sorted(categories)
        info["docs_count"] = len(list(docs_dir.rglob("*")))

    return info


def read_document_content(project_root: Path, doc_path: str) -> str | None:
    """Read content of a document file."""
    full_path = project_root / doc_path
    if full_path.exists() and full_path.is_file():
        return full_path.read_text(encoding="utf-8")
    return None


def extract_section(content: str, section_name: str) -> str | None:
    """Extract a specific section from markdown content."""
    # Pattern to match markdown headers
    pattern = rf"^##\s+{re.escape(section_name)}\s*$"
    lines = content.split("\n")

    in_section = False
    section_lines = []

    for line in lines:
        if re.match(pattern, line, re.IGNORECASE):
            in_section = True
            section_lines.append(line)
        elif in_section:
            if re.match(r"^##\s+", line):
                break
            section_lines.append(line)

    if section_lines:
        return "\n".join(section_lines).strip()
    return None


def validate_yaml_document(
    content: str, schema_name: str
) -> dict[str, Any]:
    """Validate a YAML document against its schema."""
    result = {"valid": True, "errors": [], "warnings": []}

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        result["valid"] = False
        result["errors"].append(f"YAML parse error: {e}")
        return result

    if schema_name not in DOCUMENT_SCHEMAS:
        result["warnings"].append(f"No schema defined for {schema_name}")
        return result

    schema = DOCUMENT_SCHEMAS[schema_name]

    # Basic validation
    if schema.get("type") == "object" and not isinstance(data, dict):
        result["valid"] = False
        result["errors"].append("Document must be an object")
        return result

    for required_field in schema.get("required", []):
        if required_field not in data:
            result["valid"] = False
            result["errors"].append(f"Missing required field: {required_field}")

    return result


def validate_markdown_document(content: str, doc_type: str) -> dict[str, Any]:
    """Validate a markdown document structure."""
    result = {"valid": True, "errors": [], "warnings": []}

    # Check for required sections based on doc type
    required_sections = {
        "vision.md": ["プロダクトの目的", "解決したい課題", "ターゲットユーザー"],
        "system_overview.md": ["システム全体図", "コンポーネント構成"],
        "coding_standards.md": ["言語別の基準"],
    }

    if doc_type in required_sections:
        for section in required_sections[doc_type]:
            if section not in content:
                result["warnings"].append(f"Missing section: {section}")

    # Check for update metadata
    if "_最終更新日:" not in content:
        result["warnings"].append("Missing update date metadata")

    return result


def get_template_for_doc(doc_type: str) -> str | None:
    """Get a template for creating a new document."""
    templates = {
        "vision.md": """# プロダクトビジョン

## プロダクトの目的

<!-- このプロダクトが存在する理由を記述 -->

- 目的: [プロダクトの主要な目的を記述]
- ミッション: [達成したいミッションを記述]

## 解決したい課題

<!-- プロダクトが解決する具体的な課題 -->

1. **課題1**: [課題の詳細説明]
   - 現状: [現在の状況]
   - 影響: [課題による影響]

## ターゲットユーザー

<!-- 主要なユーザーセグメント -->

| ユーザー種別 | 特徴 | ニーズ |
|-------------|------|--------|
| プライマリユーザー | [特徴] | [ニーズ] |

## 成功指標（KPI）

<!-- 測定可能な成功指標 -->

| 指標名 | 現在値 | 目標値 | 測定方法 |
|--------|--------|--------|----------|
| KPI-1 | - | - | [測定方法] |

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
""",
        "requirements.yaml": """# 機能要件定義
version: "1.0"
last_updated: YYYY-MM-DD

features:
  - id: F001
    name: "[機能名]"
    description: "[機能の説明]"
    priority: high  # high, medium, low
    status: draft   # draft, approved, implemented
    acceptance_criteria:
      - "[受け入れ基準1]"
      - "[受け入れ基準2]"
    dependencies: []
""",
        "roles.yaml": """# AIエージェント役割定義
version: "1.0"
last_updated: YYYY-MM-DD

roles:
  - id: developer
    name: "開発エージェント"
    description: "コード生成・修正を担当"
    permissions:
      - "read:all"
      - "write:code"
      - "write:tests"
      - "execute:lint"
      - "execute:test"
    restrictions:
      - "no-production-deploy"
      - "no-security-config-changes"
""",
        "constraints.yaml": """# AIエージェント制約条件
version: "1.0"
last_updated: YYYY-MM-DD

constraints:
  - id: C001
    description: "機密情報を含むファイルの編集禁止"
    severity: critical
    scope:
      - ".env*"
      - "**/credentials*"
      - "**/secrets*"

  - id: C002
    description: "本番環境への直接デプロイ禁止"
    severity: critical
    action: escalate_to_human
""",
        "system_overview.md": """# システム概要

## システム全体図

```
[システム構成図をここに記述]
```

## コンポーネント構成

### 1. フロントエンド

| コンポーネント | 説明 | 技術スタック |
|---------------|------|-------------|
| [コンポーネント名] | [説明] | [技術] |

### 2. バックエンド

| サービス | 責務 | 通信方式 |
|---------|------|---------|
| [サービス名] | [責務] | [通信方式] |

### 3. データ層

| コンポーネント | 用途 | 技術 |
|---------------|------|------|
| [コンポーネント名] | [用途] | [技術] |

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
""",
    }

    return templates.get(doc_type)


# Create MCP server
server = Server("design-docs-mcp")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="template://structure",
            name="Template Structure",
            description="テンプレートの構造情報（どのセクションがあるか、必須項目は何か）",
            mimeType="application/json",
        ),
        Resource(
            uri="template://schema",
            name="Document Schemas",
            description="各ドキュメントの検証スキーマ",
            mimeType="application/json",
        ),
        Resource(
            uri="project://current",
            name="Current Project",
            description="現在のプロジェクト情報",
            mimeType="application/json",
        ),
        Resource(
            uri="docs://list",
            name="Document List",
            description="プロジェクト内の既存ドキュメント一覧",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    project_root = get_project_root()

    if uri == "template://structure":
        flat_structure = flatten_structure(TEMPLATE_STRUCTURE)
        return json.dumps(flat_structure, indent=2, ensure_ascii=False)

    elif uri == "template://schema":
        return json.dumps(DOCUMENT_SCHEMAS, indent=2, ensure_ascii=False)

    elif uri == "project://current":
        info = get_project_info(project_root)
        return json.dumps(info, indent=2, ensure_ascii=False)

    elif uri == "docs://list":
        docs = list_existing_docs(project_root)
        return json.dumps(docs, indent=2, ensure_ascii=False)

    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_templates",
            description="利用可能なテンプレート一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "フィルタするカテゴリ（product, architecture, dev_process, agent, ops）",
                    }
                },
            },
        ),
        Tool(
            name="create_document",
            description="テンプレートから新規ドキュメントを作成",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "description": "テンプレートタイプ（vision.md, requirements.yaml, roles.yaml など）",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "出力先パス（docs/ からの相対パス）",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "自動入力するメタデータ",
                        "properties": {
                            "project_name": {"type": "string"},
                            "author": {"type": "string"},
                            "date": {"type": "string"},
                        },
                    },
                },
                "required": ["template_type", "output_path"],
            },
        ),
        Tool(
            name="get_section",
            description="ドキュメントの特定セクションの内容を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "ドキュメントのパス",
                    },
                    "section_name": {
                        "type": "string",
                        "description": "セクション名（markdownの場合はヘッダー名）",
                    },
                },
                "required": ["document_path", "section_name"],
            },
        ),
        Tool(
            name="update_section",
            description="ドキュメントの特定セクションを更新（マーカーベース）",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "ドキュメントのパス",
                    },
                    "section_name": {
                        "type": "string",
                        "description": "セクション名（AI_EDITABLE マーカー名）",
                    },
                    "new_content": {
                        "type": "string",
                        "description": "新しいセクション内容",
                    },
                },
                "required": ["document_path", "section_name", "new_content"],
            },
        ),
        Tool(
            name="validate_document",
            description="ドキュメントが規定の構造に従っているか検証",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "検証するドキュメントのパス",
                    },
                },
                "required": ["document_path"],
            },
        ),
        Tool(
            name="fill_metadata",
            description="プロジェクト情報からメタデータを自動入力",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description": "メタデータを入力するドキュメントのパス",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "入力するメタデータ",
                        "properties": {
                            "date": {"type": "string"},
                            "author": {"type": "string"},
                            "version": {"type": "string"},
                        },
                    },
                },
                "required": ["document_path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    project_root = get_project_root()

    if name == "list_templates":
        category = arguments.get("category")
        flat_structure = flatten_structure(TEMPLATE_STRUCTURE)

        if category:
            flat_structure = [
                item for item in flat_structure
                if item["path"].startswith(f"docs/{category}/") or
                   item["path"].startswith(f"{category}/")
            ]

        return [TextContent(
            type="text",
            text=json.dumps(flat_structure, indent=2, ensure_ascii=False),
        )]

    elif name == "create_document":
        template_type = arguments["template_type"]
        output_path = arguments["output_path"]
        metadata = arguments.get("metadata", {})

        template = get_template_for_doc(template_type)
        if not template:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Unknown template type: {template_type}",
                }),
            )]

        # Fill in metadata
        today = datetime.now().strftime("%Y-%m-%d")
        template = template.replace("YYYY-MM-DD", metadata.get("date", today))
        if "author" in metadata:
            template = template.replace("[担当者/AIエージェント名]", metadata["author"])

        # Write file
        full_path = project_root / output_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(template, encoding="utf-8")

        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "path": str(full_path),
                "template_type": template_type,
            }, ensure_ascii=False),
        )]

    elif name == "get_section":
        doc_path = arguments["document_path"]
        section_name = arguments["section_name"]

        content = read_document_content(project_root, doc_path)
        if content is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        section = extract_section(content, section_name)
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "section": section,
            }, ensure_ascii=False),
        )]

    elif name == "update_section":
        doc_path = arguments["document_path"]
        section_name = arguments["section_name"]
        new_content = arguments["new_content"]

        full_path = project_root / doc_path
        if not full_path.exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        content = full_path.read_text(encoding="utf-8")

        # Look for AI_EDITABLE markers
        marker_start = f"<!-- AI_EDITABLE_START: {section_name} -->"
        marker_end = f"<!-- AI_EDITABLE_END: {section_name} -->"

        if marker_start in content and marker_end in content:
            # Replace content between markers
            pattern = re.compile(
                rf"{re.escape(marker_start)}.*?{re.escape(marker_end)}",
                re.DOTALL,
            )
            replacement = f"{marker_start}\n{new_content}\n{marker_end}"
            new_full_content = pattern.sub(replacement, content)
            full_path.write_text(new_full_content, encoding="utf-8")

            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "message": f"Section '{section_name}' updated successfully",
                }, ensure_ascii=False),
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"AI_EDITABLE markers not found for section: {section_name}",
                }),
            )]

    elif name == "validate_document":
        doc_path = arguments["document_path"]

        content = read_document_content(project_root, doc_path)
        if content is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        doc_name = Path(doc_path).name

        if doc_path.endswith((".yaml", ".yml")):
            result = validate_yaml_document(content, doc_name)
        else:
            result = validate_markdown_document(content, doc_name)

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False),
        )]

    elif name == "fill_metadata":
        doc_path = arguments["document_path"]
        metadata = arguments.get("metadata", {})

        full_path = project_root / doc_path
        if not full_path.exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Document not found: {doc_path}",
                }),
            )]

        content = full_path.read_text(encoding="utf-8")

        # Fill in metadata fields
        today = datetime.now().strftime("%Y-%m-%d")
        content = content.replace("YYYY-MM-DD", metadata.get("date", today))

        if "author" in metadata:
            content = content.replace("[担当者/AIエージェント名]", metadata["author"])

        if "version" in metadata:
            content = re.sub(
                r'version:\s*"[^"]*"',
                f'version: "{metadata["version"]}"',
                content,
            )

        full_path.write_text(content, encoding="utf-8")

        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "message": "Metadata filled successfully",
            }, ensure_ascii=False),
        )]

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"}),
        )]


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="design-review",
            description="設計レビュー用のワークフロー",
            arguments=[
                PromptArgument(
                    name="document_path",
                    description="レビュー対象のドキュメントパス",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="update-architecture",
            description="アーキテクチャ図更新のガイド",
            arguments=[
                PromptArgument(
                    name="change_description",
                    description="変更内容の説明",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="sync-with-code",
            description="コードとの整合性チェック",
            arguments=[
                PromptArgument(
                    name="code_path",
                    description="チェック対象のコードパス",
                    required=False,
                ),
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific prompt."""
    if name == "design-review":
        doc_path = arguments.get("document_path", "") if arguments else ""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""設計ドキュメントのレビューを行います。

対象ドキュメント: {doc_path}

以下の観点でレビューしてください：

1. **完全性チェック**
   - 必須セクションが全て記載されているか
   - 各セクションに十分な情報があるか

2. **整合性チェック**
   - 他のドキュメントとの矛盾がないか
   - 用語が統一されているか

3. **実現可能性チェック**
   - 技術的に実現可能か
   - リソース制約を考慮しているか

4. **セキュリティチェック**
   - セキュリティ上の問題点はないか
   - 機密情報の取り扱いは適切か

5. **改善提案**
   - より良い設計の提案
   - 不足している考慮事項

レビュー結果を構造化して報告してください。
""",
                    ),
                ),
            ],
        )

    elif name == "update-architecture":
        change_desc = arguments.get("change_description", "") if arguments else ""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""アーキテクチャドキュメントの更新を行います。

変更内容: {change_desc}

以下の手順で更新してください：

1. **現状の確認**
   - docs/architecture/system_overview.md を読み込む
   - 関連するシーケンス図やドメインモデルを確認

2. **影響範囲の特定**
   - 変更が影響するコンポーネントを特定
   - 依存関係を確認

3. **ドキュメント更新**
   - システム概要図を更新
   - 必要に応じてシーケンス図を更新
   - コンポーネント表を更新

4. **整合性確認**
   - 他のドキュメントとの整合性を確認
   - API仕様との整合性を確認

5. **変更履歴の記録**
   - meta/change_history.md に変更を記録

更新後、変更サマリを報告してください。
""",
                    ),
                ),
            ],
        )

    elif name == "sync-with-code":
        code_path = arguments.get("code_path", "src/") if arguments else "src/"
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"""コードとドキュメントの整合性をチェックします。

対象コードパス: {code_path}

以下の観点でチェックしてください：

1. **API整合性**
   - docs/architecture/api_design/openapi.yaml と実装コードの比較
   - エンドポイント、パラメータ、レスポンス型の一致確認

2. **データモデル整合性**
   - docs/architecture/data_schemas/entities.yaml と実装の比較
   - エンティティ定義、フィールド、型の一致確認

3. **ドメインモデル整合性**
   - docs/architecture/domain_model.md と実装の比較
   - ドメインオブジェクト、関係性の一致確認

4. **不整合の報告**
   - 発見した不整合を一覧化
   - 修正が必要な箇所を特定

5. **修正提案**
   - ドキュメント側の修正案
   - またはコード側の修正案

整合性チェック結果を報告してください。
""",
                    ),
                ),
            ],
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    """Main entry point."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
