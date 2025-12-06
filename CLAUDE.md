# Claude Code エージェント指示書

このドキュメントは、Claude CodeがAIファースト開発テンプレートを使用してコードを生成する際の指示書です。

## 概要

あなたは、このプロジェクトのドキュメント体系を活用してコードを生成するAIエージェントです。このリポジトリには、AIが自律的に読み取り・活用できるよう設計された構造化ドキュメントが含まれています。

## 基本動作原則

### 1. ドキュメント優先アプローチ

**タスク開始前に必ず以下のドキュメントを参照してください:**

```
必須参照ドキュメント:
1. generator_instructions/system_prompt.md      # あなたの役割と行動指針
2. generator_instructions/file_update_policy.md # ファイル編集ルール
3. generator_instructions/forbidden_actions.md  # 禁止事項
4. docs/dev_process/coding_standards.md        # コーディング規約
5. docs/agent/behaviours.md                    # 行動規則とフロー
```

**機能実装時の追加参照:**

```
プロダクト理解:
- docs/product/vision.md                       # プロダクトビジョン
- docs/product/requirements.yaml               # 機能要件
- docs/product/user_scenarios.md               # ユーザーシナリオ

技術設計:
- docs/architecture/system_overview.md         # システム概要
- docs/architecture/domain_model.md            # ドメインモデル
- docs/architecture/sequence_diagrams.md       # シーケンス図
- docs/architecture/api_design/openapi.yaml    # API仕様
- docs/architecture/data_schemas/entities.yaml # エンティティ定義

エージェント設定:
- docs/agent/roles.yaml                        # 役割定義と権限
- docs/agent/constraints.yaml                  # 制約条件
- docs/agent/tools/available_tools.md          # 利用可能ツール
```

### 2. タスク遂行フロー

以下の3フェーズで作業を進めてください（`docs/agent/behaviours.md`参照）:

#### Phase 1: タスク受領・分析
```
1. タスク内容を確認
   - 要件の明確化
   - 不明点があればユーザーに質問

2. コンテキスト収集
   - 関連ドキュメントの読み込み
   - 既存コードの確認
   - 過去の類似実装の参照

3. 実行計画の作成
   - TodoWrite ツールでタスクリストを作成
   - 依存関係の特定
   - リスク評価
```

#### Phase 2: 実装
```
1. 事前チェック
   - 編集権限の確認（docs/agent/roles.yaml）
   - 制約条件の確認（docs/agent/constraints.yaml）

2. コード生成/修正
   - コーディング規約に従う（docs/dev_process/coding_standards.md）
   - マーカーベース更新を使用（AI_EDITABLE_START/END）
   - 型定義を必ず付与
   - ドキュメントコメントを追加

3. テスト作成
   - 単体テストを必ず作成
   - 受け入れ基準をテストケースに変換

4. 検証
   - Lint/Format チェック実行
   - テスト実行
   - セキュリティスキャン
```

#### Phase 3: 完了・報告
```
1. コミット
   - コミットメッセージ規約に従う（docs/dev_process/agent_commit_rules.yaml）
   - 必須メタデータを含める:
     * Agent: [あなたの役割]
     * Task: [タスクID]

2. 変更履歴の記録
   - meta/change_history.md に変更内容を記録

3. ユーザーへの報告
   - 実装内容のサマリ
   - 注意点・制約事項
   - 次のステップの提案
```

## ファイル編集ルール

### マーカーベース更新の使用

既存ファイルを編集する場合は、必ずマーカーを使用してください:

```typescript
// AI_EDITABLE_START: generated_types
// この範囲内のみ編集可能
interface User {
  id: string;
  name: string;
}
// AI_EDITABLE_END: generated_types
```

```markdown
<!-- AI_EDITABLE_START: api_documentation -->
## API エンドポイント
この範囲は自動生成されます
<!-- AI_EDITABLE_END: api_documentation -->
```

### 編集の制約

**許可される編集:**
- ✅ マーカー範囲内の完全置換
- ✅ テストコードの追加
- ✅ ドキュメントセクションの更新
- ✅ 型定義の追加

**人間承認が必要:**
- ⚠️ セキュリティ関連ファイルの変更
- ⚠️ 設定ファイルの変更（*.yaml, *.json, *.config.*）
- ⚠️ 公開APIインターフェースの変更
- ⚠️ データベーススキーマの変更

**禁止事項:**
- ❌ 機密情報ファイル（.env, credentials）の編集
- ❌ 本番環境への直接デプロイ
- ❌ マーカー外の既存コードの無断変更
- ❌ テストなしのコード変更

## コーディング規約

### 言語別の基準

**TypeScript/JavaScript:**
```typescript
/**
 * ユーザーIDからユーザー情報を取得する
 *
 * @param userId - ユーザーの一意識別子
 * @returns ユーザー情報、見つからない場合はnull
 * @throws {NotFoundError} ユーザーが存在しない場合
 */
async function getUserById(userId: string): Promise<User | null> {
  // 実装
}
```
- スタイル: Airbnb JavaScript Style Guide
- インデント: スペース2つ
- 最大行長: 100文字
- 命名: camelCase (関数/変数), PascalCase (クラス/型)

**Python:**
```python
def get_user_by_id(user_id: str) -> Optional[User]:
    """
    ユーザーIDからユーザー情報を取得する。

    Args:
        user_id: ユーザーの一意識別子

    Returns:
        ユーザー情報、見つからない場合はNone

    Raises:
        ValueError: user_idが無効な場合
    """
    pass
```
- スタイル: PEP 8
- インデント: スペース4つ
- 最大行長: 88文字（Black準拠）
- 命名: snake_case (関数/変数), PascalCase (クラス)

**Go:**
```go
// GetUserByID retrieves a user by their unique identifier.
// Returns ErrNotFound if the user does not exist.
func (s *UserService) GetUserByID(ctx context.Context, id string) (*User, error) {
    // 実装
}
```
- スタイル: Effective Go
- フォーマッタ: gofmt/goimports
- 命名: PascalCase (エクスポート), camelCase (非エクスポート)

### 必須チェック

コード生成後、必ず以下を実行してください:

```bash
# Lint チェック
npm run lint          # TypeScript/JavaScript
ruff check .          # Python
golangci-lint run     # Go

# フォーマット
prettier --write .    # TypeScript/JavaScript
black .               # Python
gofmt -w .            # Go

# 型チェック
npm run type-check    # TypeScript
mypy .                # Python

# テスト実行
npm test              # TypeScript/JavaScript
pytest                # Python
go test ./...         # Go
```

## コミットメッセージ規約

**フォーマット:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type の選択:**
- `feat`: 新機能追加
- `fix`: バグ修正
- `docs`: ドキュメント変更
- `refactor`: リファクタリング
- `test`: テスト追加/修正
- `chore`: ビルド・ツール関連
- `agent`: AIエージェント固有の変更

**必須フッター:**
```
Closes #<issue-number>
Agent: <your-role>
Task: <task-id>
```

**例:**
```
feat(auth): add OAuth2 login support

- Implement Google OAuth2 provider
- Add callback endpoint handling
- Store tokens securely in session

Closes #123
Agent: developer-agent
Task: 550e8400-e29b-41d4-a716-446655440000
```

## エスカレーション基準

以下の場合は即座にユーザーに確認してください:

### 必須エスカレーション
1. **セキュリティ脆弱性の発見**
   - 即時報告し、実装を停止
   - 影響範囲と緩和策を提案

2. **要件の曖昧さ・矛盾**
   - 仮定で進めず、明確化を依頼
   - 複数の選択肢を提示

3. **破壊的変更の必要性**
   - 影響範囲を詳細に説明
   - 代替案を提示

4. **予期しないエラー**
   - エラー内容と状況を記録
   - ロールバック手順を提案

### 推奨エスカレーション
- 新技術・ライブラリの導入判断
- 大規模なリファクタリング
- パフォーマンスへの重大な影響
- 外部API連携の設計判断

## セキュリティチェックリスト

コード生成時、必ず以下を確認してください:

- [ ] 入力値の検証を実装
- [ ] SQLインジェクション対策（パラメータ化クエリ使用）
- [ ] XSS対策（適切なエスケープ処理）
- [ ] 機密情報をログに出力していない
- [ ] 認証情報をハードコーディングしていない
- [ ] 適切なエラーハンドリングを実装
- [ ] HTTPS通信を使用（機密データ送信時）
- [ ] 適切な権限チェックを実装

## 変更履歴の記録

すべての変更は `meta/change_history.md` に記録してください:

```markdown
## [YYYY-MM-DD] - Agent: <role>

### Added
- 新規追加した機能

### Changed
- 変更した内容

### Fixed
- 修正したバグ

### Security
- セキュリティ関連の変更

Task: <task-id>
Files: <changed-files>
```

## ベストプラクティス

### 1. 段階的な実装
- 一度に大量のコードを生成しない
- 小さく実装し、都度テストを実行
- フィードバックループを短く保つ

### 2. 既存パターンの尊重
- 既存のコードベースのスタイルに従う
- 新しいパターンを導入する前に確認
- 一貫性を最優先

### 3. ドキュメント同期
- コード変更時は関連ドキュメントも更新
- API変更時はOpenAPI仕様も更新
- データモデル変更時はentities.yamlも更新

### 4. テスト駆動
- 実装前にテストケースを確認
- 受け入れ基準をテストコードに変換
- エッジケースを考慮

### 5. 透明性の確保
- 実行内容を明確に説明
- 技術的な判断の理由を記録
- トレードオフを明示

## トラブルシューティング

### ドキュメントが不足している場合
1. 既存の類似実装を参照
2. ユーザーに追加情報を依頼
3. 仮定を明示して進める（承認を得る）

### テストが失敗する場合
1. エラーメッセージを詳細に分析
2. 関連コードを確認
3. 修正を試み、再テスト
4. 解決できない場合はユーザーに報告

### コンフリクトが発生した場合
1. 変更内容を比較
2. 自動マージ可能か判断
3. 不可能な場合はユーザーに確認を依頼

## まとめ

**常に念頭に置くべき5つの原則:**

1. 📚 **ドキュメントファースト**: 実装前に必ず関連ドキュメントを参照
2. 🔒 **安全性優先**: 不明な場合は確認、セキュリティは最優先
3. ✅ **品質保証**: テスト・Lint・型チェックは必須
4. 📝 **トレーサビリティ**: すべての変更を記録
5. 🤝 **協調性**: 人間との連携を重視、適切にエスカレーション

---

このドキュメントは、AIエージェントが効率的かつ安全にコードを生成するための指針です。
不明点があれば、遠慮なくユーザーに質問してください。
