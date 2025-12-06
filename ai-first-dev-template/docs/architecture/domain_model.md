# ドメインモデル

## エンティティ一覧

### 概要図

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │──1:N──│   Project   │──1:N──│    Task     │
└─────────────┘       └─────────────┘       └─────────────┘
      │                     │                     │
      │                     │                     │
      │1:N                  │1:N                  │1:N
      ▼                     ▼                     ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  AIAgent    │       │  Document   │       │   Commit    │
└─────────────┘       └─────────────┘       └─────────────┘
```

## 属性定義

### User（ユーザー）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| email | String | Yes | メールアドレス |
| name | String | Yes | 表示名 |
| role | Enum | Yes | 役割 (admin/developer/viewer) |
| created_at | DateTime | Yes | 作成日時 |
| updated_at | DateTime | Yes | 更新日時 |

### Project（プロジェクト）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| name | String | Yes | プロジェクト名 |
| description | Text | No | 説明 |
| owner_id | UUID | Yes | オーナーユーザーID (FK: User) |
| status | Enum | Yes | 状態 (active/archived/deleted) |
| repository_url | String | No | リポジトリURL |
| created_at | DateTime | Yes | 作成日時 |
| updated_at | DateTime | Yes | 更新日時 |

### Task（タスク）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| project_id | UUID | Yes | プロジェクトID (FK: Project) |
| title | String | Yes | タイトル |
| description | Text | No | 詳細説明 |
| status | Enum | Yes | 状態 (todo/in_progress/review/done) |
| priority | Enum | Yes | 優先度 (high/medium/low) |
| assignee_type | Enum | Yes | 担当種別 (human/ai_agent) |
| assignee_id | UUID | No | 担当者ID |
| due_date | Date | No | 期限 |
| created_at | DateTime | Yes | 作成日時 |
| updated_at | DateTime | Yes | 更新日時 |

### AIAgent（AIエージェント）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| name | String | Yes | エージェント名 |
| role | Enum | Yes | 役割 (developer/reviewer/tester) |
| owner_id | UUID | Yes | 管理ユーザーID (FK: User) |
| config | JSON | No | 設定情報 |
| status | Enum | Yes | 状態 (active/paused/disabled) |
| last_active_at | DateTime | No | 最終活動日時 |
| created_at | DateTime | Yes | 作成日時 |

### Document（ドキュメント）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| project_id | UUID | Yes | プロジェクトID (FK: Project) |
| title | String | Yes | タイトル |
| content | Text | Yes | 内容 |
| type | Enum | Yes | 種別 (spec/design/api/guide) |
| version | Integer | Yes | バージョン番号 |
| author_type | Enum | Yes | 作成者種別 (human/ai_agent) |
| author_id | UUID | Yes | 作成者ID |
| created_at | DateTime | Yes | 作成日時 |
| updated_at | DateTime | Yes | 更新日時 |

### Commit（コミット）

| 属性名 | 型 | 必須 | 説明 |
|--------|-----|------|------|
| id | UUID | Yes | 一意識別子 |
| task_id | UUID | Yes | タスクID (FK: Task) |
| hash | String | Yes | コミットハッシュ |
| message | String | Yes | コミットメッセージ |
| author_type | Enum | Yes | 作成者種別 (human/ai_agent) |
| author_id | UUID | Yes | 作成者ID |
| files_changed | Integer | Yes | 変更ファイル数 |
| additions | Integer | Yes | 追加行数 |
| deletions | Integer | Yes | 削除行数 |
| created_at | DateTime | Yes | 作成日時 |

## 関係性の記述

### User - Project（1:N）

- 1人のユーザーは複数のプロジェクトを所有できる
- プロジェクトは必ず1人のオーナーを持つ

### Project - Task（1:N）

- 1つのプロジェクトは複数のタスクを持つ
- タスクは必ず1つのプロジェクトに属する

### Task - Commit（1:N）

- 1つのタスクに対して複数のコミットが関連付く
- コミットは必ず1つのタスクに紐づく

### User - AIAgent（1:N）

- 1人のユーザーは複数のAIエージェントを管理できる
- AIエージェントは必ず1人の管理者を持つ

### Project - Document（1:N）

- 1つのプロジェクトは複数のドキュメントを持つ
- ドキュメントは必ず1つのプロジェクトに属する

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
