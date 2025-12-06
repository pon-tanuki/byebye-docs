# コーディング規約

## 概要

本ドキュメントはプロジェクトで適用するコーディング規約を定義する。人間およびAIエージェントの両方がこの規約に従う。

---

## 言語別コーディング規約

### Python

#### スタイルガイド

- **基準**: PEP 8
- **最大行長**: 88文字（Black準拠）
- **インデント**: スペース4つ

#### 命名規則

| 種別 | 規則 | 例 |
|------|------|-----|
| モジュール | snake_case | `user_service.py` |
| クラス | PascalCase | `UserService` |
| 関数/メソッド | snake_case | `get_user_by_id` |
| 変数 | snake_case | `user_name` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| プライベート | 先頭アンダースコア | `_internal_method` |

#### ドキュメンテーション

```python
def calculate_total(items: list[Item], tax_rate: float = 0.1) -> float:
    """
    商品リストの合計金額を計算する。

    Args:
        items: 商品リスト
        tax_rate: 税率（デフォルト: 10%）

    Returns:
        税込み合計金額

    Raises:
        ValueError: itemsが空の場合
    """
    pass
```

---

### TypeScript / JavaScript

#### スタイルガイド

- **基準**: Airbnb JavaScript Style Guide
- **最大行長**: 100文字
- **インデント**: スペース2つ
- **セミコロン**: 使用する

#### 命名規則

| 種別 | 規則 | 例 |
|------|------|-----|
| ファイル | camelCase / kebab-case | `userService.ts` |
| クラス | PascalCase | `UserService` |
| 関数 | camelCase | `getUserById` |
| 変数 | camelCase | `userName` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| インターフェース | PascalCase (I接頭辞なし) | `User` |
| 型 | PascalCase | `UserResponse` |

#### ドキュメンテーション

```typescript
/**
 * ユーザーIDからユーザー情報を取得する
 *
 * @param userId - ユーザーの一意識別子
 * @returns ユーザー情報、見つからない場合はnull
 * @throws {NotFoundError} ユーザーが存在しない場合
 */
async function getUserById(userId: string): Promise<User | null> {
  // ...
}
```

---

### Go

#### スタイルガイド

- **基準**: Effective Go, Go Code Review Comments
- **フォーマッタ**: gofmt / goimports

#### 命名規則

| 種別 | 規則 | 例 |
|------|------|-----|
| パッケージ | lowercase | `userservice` |
| エクスポート | PascalCase | `GetUserByID` |
| 非エクスポート | camelCase | `getUserByID` |
| インターフェース | 動詞+er | `Reader`, `UserFinder` |
| 頭字語 | 全て大文字 | `HTTPHandler`, `userID` |

#### ドキュメンテーション

```go
// UserService provides user-related operations.
type UserService struct {
    repo UserRepository
}

// GetByID retrieves a user by their unique identifier.
// Returns ErrNotFound if the user does not exist.
func (s *UserService) GetByID(ctx context.Context, id string) (*User, error) {
    // ...
}
```

---

## 共通規約

### コメント

1. **必須コメント**
   - 公開API/関数のドキュメンテーション
   - 複雑なアルゴリズムの説明
   - TODO/FIXME（担当者と期限を明記）

2. **避けるべきコメント**
   - コードの内容を繰り返すだけのコメント
   - 古い・メンテナンスされていないコメント
   - コメントアウトされたコード

### エラー処理

1. **例外/エラーの使い分け**
   - 回復可能なエラー → エラー値の返却
   - 回復不可能なエラー → 例外/パニック

2. **エラーメッセージ**
   - 具体的で actionable な内容
   - コンテキスト情報を含める
   - ユーザー向けと開発者向けを分ける

### セキュリティ

1. **必須事項**
   - 入力値の検証
   - SQLインジェクション対策（パラメータ化クエリ）
   - XSS対策（エスケープ処理）
   - 機密情報のログ出力禁止

2. **禁止事項**
   - 認証情報のハードコーディング
   - 暗号化なしの機密データ送信
   - `eval()` などの動的コード実行

---

## Lint/Formatter の使用基準

### 必須ツール

| 言語 | Linter | Formatter |
|------|--------|-----------|
| Python | ruff, mypy | black, isort |
| TypeScript | ESLint | Prettier |
| JavaScript | ESLint | Prettier |
| Go | golangci-lint | gofmt, goimports |

### 設定ファイル

プロジェクトルートに以下の設定ファイルを配置：

```
project_root/
├── .eslintrc.js        # ESLint設定
├── .prettierrc         # Prettier設定
├── pyproject.toml      # Python設定（black, ruff, mypy）
├── .golangci.yml       # golangci-lint設定
└── .editorconfig       # エディタ共通設定
```

### CI/CD統合

1. **Pre-commit Hook**
   - Lint/Format チェックを実行
   - 違反があればコミット拒否

2. **CI Pipeline**
   - 全ファイルに対するLint実行
   - フォーマット差分チェック

### AIエージェント向け指示

- コード生成時は必ず Formatter を適用
- Lint エラーは生成段階で解消
- 型アノテーションを必ず付与
- ドキュメンテーションを自動生成

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
