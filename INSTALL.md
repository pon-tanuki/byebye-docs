# インストールガイド

AI-First Development Templateを使用して新しいプロジェクトを開始する方法を説明します。

## 前提条件

以下のツールがインストールされていることを確認してください：

- `curl` または `wget`（ファイルダウンロード用）
- `bash`（セットアップスクリプト実行用）
- `git`（オプション、バージョン管理用）

## インストール方法

### 方法1: ワンライナーでのセットアップ（最も簡単）

```bash
curl -fsSL https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh | bash -s my-awesome-project
```

この1行で、`my-awesome-project`ディレクトリが作成され、すべてのテンプレートファイルがセットアップされます。

### 方法2: スクリプトをダウンロードして実行

```bash
# スクリプトをダウンロード
curl -O https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh

# 実行権限を付与
chmod +x setup.sh

# セットアップ実行
./setup.sh my-project-name
```

### 方法3: Gitクローン（開発者向け）

テンプレート自体をカスタマイズしたい場合：

```bash
# リポジトリをクローン
git clone https://github.com/pon-tanuki/design-docs-for-ai-driven-development.git my-project

cd my-project

# テンプレートのGit履歴を削除
rm -rf .git

# 新しいGitリポジトリとして初期化
git init
git add .
git commit -m "feat: initialize project with AI-first development template"
```

## セットアップオプション

### Gitリポジトリ初期化をスキップ

既存のGitリポジトリに追加する場合や、後でGitを初期化したい場合：

```bash
./setup.sh --no-git my-project
```

### バージョン確認

```bash
./setup.sh --version
```

### ヘルプ表示

```bash
./setup.sh --help
```

## セットアップ後の確認

セットアップが成功すると、以下のような構造が作成されます：

```
my-project/
├── CLAUDE.md                      # Claude Code用指示書
├── PROJECT_README.md              # プロジェクト固有のREADME
├── .gitignore                     # Git除外設定
├── .editorconfig                  # エディタ設定
├── .template-metadata.json        # テンプレートメタデータ
├── docs/                          # ドキュメント
│   ├── product/                   # プロダクト定義
│   ├── architecture/              # アーキテクチャ
│   ├── agent/                     # AIエージェント設定
│   ├── dev_process/               # 開発プロセス
│   └── ops/                       # 運用
├── generator_instructions/        # AIエージェント指示
├── meta/                          # メタ情報
└── project/                       # プロジェクト管理
```

## 次のステップ

1. **プロジェクトディレクトリに移動**
   ```bash
   cd my-project
   ```

2. **プロジェクトREADMEを確認**
   ```bash
   cat PROJECT_README.md
   ```

3. **プロダクト情報を更新**
   ```bash
   # ビジョンを記述
   $EDITOR docs/product/vision.md

   # 機能要件を定義
   $EDITOR docs/product/requirements.yaml

   # システム概要を設計
   $EDITOR docs/architecture/system_overview.md
   ```

4. **AI開発を開始**

   Claude Codeを起動し、以下のように指示：
   ```
   ユーザー認証機能を実装して
   ```

   AIが自動的に：
   - `CLAUDE.md` を参照
   - `docs/` 配下のドキュメントを読み込み
   - コーディング規約に従ってコード生成
   - テストを作成
   - 適切なコミットメッセージで保存

## トラブルシューティング

### エラー: ディレクトリが既に存在します

```bash
Directory 'my-project' already exists!
```

**解決方法:**
- 別のプロジェクト名を使用する
- 既存ディレクトリを削除してから再実行: `rm -rf my-project`
- 既存ディレクトリにマージする（上級者向け）

### エラー: curl/wgetが見つかりません

```bash
Neither curl nor wget is available
```

**解決方法:**
```bash
# macOS (Homebrew)
brew install curl

# Ubuntu/Debian
sudo apt-get install curl

# CentOS/RHEL
sudo yum install curl
```

### ダウンロードが失敗する

ネットワーク接続を確認するか、方法3（Gitクローン）を試してください。

### Gitコミットが失敗する

Gitがインストールされていない場合は`--no-git`オプションを使用：
```bash
./setup.sh --no-git my-project
```

後でGitを手動で初期化：
```bash
cd my-project
git init
git add .
git commit -m "feat: initialize project"
```

## アンインストール

プロジェクトディレクトリを削除するだけです：

```bash
rm -rf my-project
```

## サポート

問題が発生した場合：

1. [GitHub Issues](https://github.com/pon-tanuki/design-docs-for-ai-driven-development/issues)で報告
2. [README.md](README.md)のドキュメントを確認
3. セットアップスクリプトのヘルプを確認: `./setup.sh --help`

## 参考リンク

- [プロジェクトリポジトリ](https://github.com/pon-tanuki/design-docs-for-ai-driven-development)
- [CLAUDE.md](CLAUDE.md) - AIエージェント向け指示書
- [テンプレートの設計方針](README.md#aiエージェント向け設計方針)
