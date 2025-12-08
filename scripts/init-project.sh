#!/bin/bash
# byebye-docs プロジェクト初期化スクリプト
# 使用方法: ./init-project.sh [target_directory]

set -e

TARGET_DIR="${1:-.}"
REPO_URL="https://github.com/pon-tanuki/byebye-docs"

echo "=== byebye-docs プロジェクト初期化 ==="
echo "対象ディレクトリ: $TARGET_DIR"
echo ""

# ディレクトリが存在することを確認
if [ ! -d "$TARGET_DIR" ]; then
    echo "エラー: ディレクトリが存在しません: $TARGET_DIR"
    exit 1
fi

# byebye-docs-mcp をインストール
echo "[1/4] byebye-docs-mcp をインストール中..."
if command -v uv &> /dev/null; then
    uv tool install byebye-docs-mcp 2>/dev/null || uv tool install byebye-docs-mcp --force
else
    pip install byebye-docs-mcp
fi

# テンプレートをダウンロード
echo "[2/4] テンプレートをダウンロード中..."
TEMP_DIR=$(mktemp -d)
curl -sL "${REPO_URL}/archive/main.tar.gz" | tar xz -C "$TEMP_DIR"

# .agent/ ディレクトリをコピー
echo "[3/4] .agent/ ディレクトリをコピー中..."
if [ -d "$TARGET_DIR/.agent" ]; then
    echo "  警告: .agent/ が既に存在します。バックアップを作成します。"
    mv "$TARGET_DIR/.agent" "$TARGET_DIR/.agent.backup.$(date +%Y%m%d%H%M%S)"
fi
cp -r "$TEMP_DIR/byebye-docs-main/.agent" "$TARGET_DIR/"

# CLAUDE.md をコピー
if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
    cp "$TEMP_DIR/byebye-docs-main/CLAUDE.md" "$TARGET_DIR/"
else
    echo "  スキップ: CLAUDE.md は既に存在します"
fi

# .mcp.json を作成
echo "[4/4] .mcp.json を作成中..."
if [ ! -f "$TARGET_DIR/.mcp.json" ]; then
    cat > "$TARGET_DIR/.mcp.json" << 'EOF'
{
  "mcpServers": {
    "byebye-docs": {
      "command": "byebye-docs",
      "env": {
        "BYEBYE_DOCS_PROJECT_PATH": "."
      }
    }
  }
}
EOF
else
    echo "  スキップ: .mcp.json は既に存在します"
fi

# クリーンアップ
rm -rf "$TEMP_DIR"

echo ""
echo "=== 初期化完了 ==="
echo ""
echo "次のステップ:"
echo "  1. .agent/ 内のYAMLファイルをプロジェクトに合わせて編集"
echo "  2. Claude Code または Claude Desktop で MCP サーバーを有効化"
echo ""
echo "MCPサーバーの更新:"
echo "  pip install --upgrade byebye-docs-mcp"
echo "  # または"
echo "  uv tool install byebye-docs-mcp --force"
