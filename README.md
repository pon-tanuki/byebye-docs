# 👋 byebye-docs

**人間の皆さん、ようこそ！** ここはAIエージェントの楽園です。

> 「人間が読みやすいドキュメント？そんなの捨てちまえ！」
> — byebye-docs の設計思想

## 🎯 What's This?

AIエージェントが**爆速**でコードを書くためのテンプレートです。

従来のドキュメント構造（22ファイル、8000行超）を、AIが一瞬で理解できる**7ファイル**に圧縮しました。人間の可読性？ごめん、それ優先度低いわ。

```
Before: 📚📚📚📚📚📚📚📚📚📚 (22 files, 8269 lines)
After:  📄📄📄📄📄📄📄 (7 files, ~2500 lines)

Token消費: -62% 🔥
```

## 🗂️ ディレクトリ構造

```
your-project/
├── .agent/                   # 🤖 AIの脳みそ（触るな危険）
│   ├── manifest.yaml         # タスクルーティング表
│   ├── context.yaml          # プロダクト情報
│   ├── architecture.yaml     # システム設計
│   ├── constraints.yaml      # ⚠️ やっちゃダメなこと
│   ├── codegen.yaml          # コーディングルール
│   └── schemas/
│       ├── api.yaml          # OpenAPI
│       └── entities.yaml     # DB設計
│
├── CLAUDE.md                 # AIへの指令書（16行）
├── mcp-server/               # おまけ機能
└── README.md                 # 👋 あなたが今読んでるやつ
```

## 🚀 Let's Vibe!!!

### 🆕 新規プロジェクトの場合

#### Step 1: クローンしてGit履歴を消す

```bash
git clone https://github.com/pon-tanuki/byebye-docs.git my-awesome-project
cd my-awesome-project
rm -rf .git && git init
```

#### Step 2: YAMLを編集

`.agent/` 配下のYAMLファイルを自分のプロジェクトに合わせて編集。

| ファイル | 何書く？ |
|---------|---------|
| `context.yaml` | プロダクトのビジョンとか要件とか |
| `architecture.yaml` | システム構成図的なやつ |
| `constraints.yaml` | AIにやらせたくないこと |
| `codegen.yaml` | コーディング規約 |

#### Step 3: AIに丸投げ

```
あなた: 「ユーザー認証機能を実装して」
AI: *manifest.yaml を読む* → *必要なファイルだけ読む* → *実装する*
あなた: 😎
```

---

### 📦 既存プロジェクトに適用する場合

すでにコードがあるプロジェクトにこのテンプレートを導入したい？簡単だよ。

#### Step 1: `.agent/` をコピー

```bash
# このリポジトリをクローン（一時的）
git clone https://github.com/pon-tanuki/byebye-docs.git /tmp/byebye-docs

# 既存プロジェクトに .agent/ と CLAUDE.md をコピー
cp -r /tmp/byebye-docs/.agent /path/to/your-project/
cp /tmp/byebye-docs/CLAUDE.md /path/to/your-project/

# お掃除
rm -rf /tmp/byebye-docs
```

#### Step 2: プロジェクトに合わせてYAMLを編集

```bash
cd /path/to/your-project
```

**最低限これだけ編集すればOK:**

| ファイル | やること |
|---------|---------|
| `context.yaml` | `product.name` と `product.vision` を書き換え |
| `architecture.yaml` | `system.name` と `system.type` を書き換え |
| `constraints.yaml` | `file_policy.editable` を実際のソースパスに変更 |
| `codegen.yaml` | 使う言語だけ残す（不要な言語は削除） |

**Pro tip:** AIに「このプロジェクトの構成を分析して `.agent/` を埋めて」って頼むのもアリ。

#### Step 3: .gitignore に追加（任意）

```bash
# AIの設定を共有したくない場合
echo ".agent/" >> .gitignore
```

#### Step 4: コミット

```bash
git add .agent/ CLAUDE.md
git commit -m "feat: byebye-docsを導入"
```

これで既存プロジェクトがAI効率特化に進化！🚀

## 🧠 AIはこう動く

```
.agent/manifest.yaml
    │
    ├─ implement_feature → context + architecture + codegen 読む
    ├─ fix_bug          → architecture + codegen + constraints 読む
    ├─ add_api          → schemas/api + schemas/entities + codegen 読む
    └─ security_review  → constraints だけ読む
```

無駄なファイル読まない。だから速い。シンプル。

## 📝 ファイルの中身チラ見せ

### constraints.yaml（AIへの「やるな」リスト）

```yaml
security:
  critical:
    - id: SEC001
      action: deny
      pattern: "**/.env*"    # 環境変数ファイル触るな

file_policy:
  forbidden:
    - ".env*"
    - "credentials.*"        # 認証情報も触るな

escalation:
  mandatory:
    - database_schema_change  # DB変更は人間に聞け
    - public_api_change       # API変更も聞け
```

### codegen.yaml（コードの書き方）

```yaml
languages:
  typescript:
    style: airbnb
    indent: 2              # スペース2つな

testing:
  required: true           # テスト書けよ
  coverage_min: 80         # カバレッジ80%以上な

commit:
  format: "<type>(<scope>): <subject>"
  types: [feat, fix, docs, refactor, test, chore]
```

## 🔌 MCPサーバー

Claude CodeやClaude Desktopと連携できるMCPサーバー付き。

### インストール

```bash
pip install byebye-docs-mcp
# または
uv tool install byebye-docs-mcp
```

### 設定

`.mcp.json` をプロジェクトルートに置いて：

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

### 機能

| ツール | 説明 |
|--------|------|
| `diff_code_docs` | コードとドキュメント間の差分を検出 |
| `extract_from_code` | コードからAPI/エンティティ情報を抽出 |
| `auto_sync` | コード変更をドキュメントに自動反映 |

詳細は [mcp-server/README.md](mcp-server/README.md) を参照。

## 📜 旧ドキュメント

「人間が読めるドキュメントが欲しい...」という方へ：

```bash
git checkout legacy/human-readable-docs
```

22ファイルのMarkdownとYAMLが待ってます。お好きにどうぞ。

## 🤝 コントリビュート

PR歓迎！でもこのテンプレートの思想は「AI効率最優先」なので、人間の可読性を上げる提案は却下するかも。ごめんね。

## 📄 ライセンス

MIT — 好きに使って、好きに改造して、好きにAIに読ませて。

---

**Happy Vibe Coding!** 🎉

*人間がドキュメント読む時代は終わった。これからはAIの時代だ。*
