# ブランチ戦略

## 概要

本ドキュメントはプロジェクトで採用するGitブランチ戦略を定義する。

---

## Git フロー

### 採用モデル: GitHub Flow（拡張版）

```
main ─────●─────●─────●─────●─────●─────●─────●──────────────────>
           \     \     ↑     \     ↑     \     ↑
            \     \    │      \    │      \    │
feature/     ●──●──●───┘       │   │       │   │
                               │   │       │   │
fix/                     ●──●──┘   │       │   │
                                   │       │   │
agent/                       ●──●──┘       │   │
                                           │   │
release/                             ●──●──┘   │
                                               │
hotfix/                                  ●─────┘
```

### ブランチ種別

| ブランチ | 命名規則 | 用途 | マージ先 |
|---------|---------|------|---------|
| main | `main` | 本番リリース可能な状態 | - |
| feature | `feature/{issue-id}-{description}` | 新機能開発 | main |
| fix | `fix/{issue-id}-{description}` | バグ修正 | main |
| agent | `agent/{agent-id}-{task-id}` | AIエージェント作業用 | main or feature |
| release | `release/v{major}.{minor}.{patch}` | リリース準備 | main |
| hotfix | `hotfix/{issue-id}-{description}` | 緊急修正 | main |

### ブランチ命名例

```
feature/123-add-user-authentication
fix/456-login-validation-error
agent/dev-agent-789-implement-api
release/v1.2.0
hotfix/999-critical-security-fix
```

---

## Trunk-Based Development の採用可否

### 現在の方針: ハイブリッドアプローチ

完全な Trunk-Based ではなく、以下の理由から GitHub Flow 拡張版を採用：

| 観点 | Trunk-Based | GitHub Flow（拡張） | 採用理由 |
|------|------------|-------------------|---------|
| ブランチ寿命 | 数時間〜1日 | 数日 | AIエージェントの作業単位に合わせる |
| マージ頻度 | 非常に高い | 高い | レビュープロセスを確保 |
| フィーチャーフラグ | 必須 | 推奨 | 段階的に導入 |
| CI/CD | 必須 | 必須 | 同等に重視 |

### 将来的な移行検討

以下の条件が整えば Trunk-Based への移行を検討：

- [ ] フィーチャーフラグ基盤の整備
- [ ] 自動テストカバレッジ 80% 以上
- [ ] AIエージェントの自律性向上
- [ ] デプロイ自動化の成熟

---

## ブランチ運用ルール

### 1. ブランチ作成

```bash
# 機能開発
git checkout main
git pull origin main
git checkout -b feature/123-add-user-auth

# AIエージェント作業
git checkout main
git pull origin main
git checkout -b agent/dev-agent-task-456
```

### 2. コミット規約

#### フォーマット

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 一覧

| Type | 説明 |
|------|------|
| feat | 新機能 |
| fix | バグ修正 |
| docs | ドキュメントのみ |
| style | フォーマット変更（機能影響なし） |
| refactor | リファクタリング |
| test | テスト追加・修正 |
| chore | ビルド・ツール変更 |
| agent | AIエージェントによる変更 |

#### 例

```
feat(auth): add JWT token validation

- Implement token verification middleware
- Add token refresh endpoint
- Update authentication flow

Closes #123
Agent: dev-agent
```

### 3. マージルール

#### Pull Request 必須条件

- [ ] CIパイプライン成功
- [ ] コードレビュー承認（1名以上）
- [ ] セキュリティスキャン合格
- [ ] コンフリクト解消済み

#### AIエージェントブランチの追加条件

- [ ] 人間によるレビュー（セキュリティ関連の場合）
- [ ] テストカバレッジ維持または向上
- [ ] ドキュメント更新（必要な場合）

### 4. ブランチ保護

#### main ブランチ

```yaml
protection_rules:
  require_pull_request: true
  required_reviews: 1
  require_status_checks: true
  required_checks:
    - ci/build
    - ci/test
    - ci/lint
    - security/scan
  restrict_push: true
  allowed_pushers:
    - release-bot
```

#### release ブランチ

```yaml
protection_rules:
  require_pull_request: true
  required_reviews: 2
  require_status_checks: true
  restrict_push: true
```

---

## AIエージェント向けブランチルール

### 許可される操作

| 操作 | 条件 |
|------|------|
| ブランチ作成 | `agent/*`, `feature/*`, `fix/*` |
| コミット | 割り当てられたブランチのみ |
| プッシュ | 割り当てられたブランチのみ |
| PR作成 | main へのマージ |

### 禁止される操作

| 操作 | 理由 |
|------|------|
| main への直接プッシュ | ブランチ保護 |
| force push | 履歴の保護 |
| ブランチ削除（他者の） | 安全性 |
| release ブランチ作成 | 人間の判断が必要 |

### 自動化フロー

```
1. タスク割り当て
   ↓
2. agent/* ブランチ自動作成
   ↓
3. コード生成・コミット
   ↓
4. テスト実行
   ↓
5. PR自動作成
   ↓
6. レビュー依頼通知
   ↓
7. 承認後マージ
   ↓
8. ブランチ自動削除
```

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
