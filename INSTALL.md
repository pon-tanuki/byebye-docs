# 🛠️ インストールガイド

byebye-docsをプロジェクトに導入する方法。簡単だよ。

## 🚀 方法1: ワンライナー（最速）

```bash
curl -sL https://raw.githubusercontent.com/pon-tanuki/byebye-docs/main/scripts/init-project.sh | bash -s /path/to/your-project
```

これだけで：
1. MCPサーバー (`byebye-docs-mcp`) インストール
2. `.agent/` コピー
3. `CLAUDE.md` コピー
4. `.mcp.json` 作成

全部やってくれる。楽ちん。

## 🔧 方法2: 手動セットアップ

ワンライナーが怖い人向け。

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

プロジェクトルートに `.mcp.json` を置く：

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

## 🆕 方法3: 新規プロジェクト

ゼロから始める？こっち：

```bash
git clone https://github.com/pon-tanuki/byebye-docs.git my-project
cd my-project
rm -rf .git && git init
```

Git履歴消して、自分のプロジェクトとして使う。

## ✅ 次のステップ

1. `.agent/` 配下のYAMLを自分のプロジェクトに合わせて編集
2. Claude Code または Claude Desktop 起動
3. 「ユーザー認証機能を実装して」とか言ってみる
4. AIがいい感じにやってくれる 🎉

## 🔄 MCPサーバーの更新

新機能が出たらこれで更新：

```bash
pip install --upgrade byebye-docs-mcp
# または
uv tool install byebye-docs-mcp --force
```

## 🗑️ アンインストール

やっぱいらないわ、って時：

```bash
# MCPサーバーを削除
pip uninstall byebye-docs-mcp

# プロジェクトからテンプレートを削除
rm -rf .agent/ CLAUDE.md .mcp.json
```

## 🆘 困ったら

- [GitHub Issues](https://github.com/pon-tanuki/byebye-docs/issues) で報告
- [README.md](README.md) を読む
