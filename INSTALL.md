# インストールガイド

byebye-docsをプロジェクトに導入する方法を説明します。

## 方法1: 初期化スクリプト（推奨）

```bash
curl -sL https://raw.githubusercontent.com/pon-tanuki/byebye-docs/main/scripts/init-project.sh | bash -s /path/to/your-project
```

これで以下が自動的に行われます：
1. MCPサーバー (`byebye-docs-mcp`) のインストール
2. `.agent/` ディレクトリのコピー
3. `CLAUDE.md` のコピー
4. `.mcp.json` の作成

## 方法2: 手動セットアップ

### Step 1: MCPサーバーをインストール

```bash
pip install byebye-docs-mcp
# または
uv tool install byebye-docs-mcp
```

### Step 2: テンプレートをコピー

```bash
git clone --depth 1 https://github.com/pon-tanuki/byebye-docs.git /tmp/byebye-docs
cp -r /tmp/byebye-docs/.agent /path/to/your-project/
cp /tmp/byebye-docs/CLAUDE.md /path/to/your-project/
rm -rf /tmp/byebye-docs
```

### Step 3: MCP設定を作成

プロジェクトルートに `.mcp.json` を作成：

```json
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
```

## 方法3: リポジトリをクローン（新規プロジェクト）

```bash
git clone https://github.com/pon-tanuki/byebye-docs.git my-project
cd my-project
rm -rf .git && git init
```

## 次のステップ

1. `.agent/` 配下のYAMLファイルをプロジェクトに合わせて編集
2. Claude Code または Claude Desktop でMCPサーバーを有効化
3. AIに「ユーザー認証機能を実装して」とか言ってみる

## MCPサーバーの更新

```bash
pip install --upgrade byebye-docs-mcp
# または
uv tool install byebye-docs-mcp --force
```

## アンインストール

```bash
# MCPサーバーを削除
pip uninstall byebye-docs-mcp

# プロジェクトからテンプレートを削除
rm -rf .agent/ CLAUDE.md .mcp.json
```

## サポート

- [GitHub Issues](https://github.com/pon-tanuki/byebye-docs/issues)
- [README.md](README.md)
