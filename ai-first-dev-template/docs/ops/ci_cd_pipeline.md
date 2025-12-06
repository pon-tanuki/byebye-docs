# CI/CD パイプライン

## 概要

本ドキュメントはCI/CDパイプラインの構成と、AIエージェントによる自動修復プロセスを定義する。

---

## パイプライン構成

### 全体フロー

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Build  │──>│  Test   │──>│  Lint   │──>│ Security│──>│ Deploy  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
     │             │             │             │             │
     ▼             ▼             ▼             ▼             ▼
 [失敗時]      [失敗時]      [失敗時]      [失敗時]      [失敗時]
     │             │             │             │             │
     ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AIエージェント自動修復                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Build ステージ

### 目的
ソースコードのコンパイル・ビルドを実行

### 実行内容

```yaml
build:
  stages:
    - name: "依存関係インストール"
      command: "npm ci"
      cache:
        key: "node-modules-${hash:package-lock.json}"
        paths:
          - node_modules/

    - name: "TypeScriptコンパイル"
      command: "npm run build"
      artifacts:
        paths:
          - dist/
        expire_in: "1 day"

    - name: "Dockerイメージビルド"
      command: "docker build -t app:${CI_COMMIT_SHA} ."
      condition: "branch == main || tag"
```

### 失敗時の対応

| エラー種別 | 自動修復 | 対応 |
|-----------|---------|------|
| 依存関係エラー | 可 | lockファイル再生成 |
| コンパイルエラー | 可 | AIエージェントが修正 |
| メモリ不足 | 不可 | アラート発報 |

---

## Test ステージ

### 目的
単体テスト・統合テストを実行

### 実行内容

```yaml
test:
  parallel:
    - name: "単体テスト"
      command: "npm run test:unit"
      coverage:
        minimum: 80%
        report: "coverage/lcov.info"

    - name: "統合テスト"
      command: "npm run test:integration"
      services:
        - postgres:14
        - redis:7

    - name: "E2Eテスト"
      command: "npm run test:e2e"
      condition: "branch == main"
      services:
        - selenium
```

### 失敗時の対応

| エラー種別 | 自動修復 | 対応 |
|-----------|---------|------|
| テスト失敗 | 可 | AIエージェントがコード修正 |
| カバレッジ不足 | 可 | テスト追加 |
| タイムアウト | 部分的 | 分析後判断 |
| 環境エラー | 不可 | アラート発報 |

---

## Lint ステージ

### 目的
コード品質チェックを実行

### 実行内容

```yaml
lint:
  parallel:
    - name: "ESLint"
      command: "npm run lint"
      allow_failure: false

    - name: "Prettier"
      command: "npm run format:check"
      allow_failure: false

    - name: "TypeScript型チェック"
      command: "npm run type-check"
      allow_failure: false

    - name: "コミットメッセージ"
      command: "commitlint --from=HEAD~1"
      allow_failure: true
```

### 失敗時の対応

| エラー種別 | 自動修復 | 対応 |
|-----------|---------|------|
| Lint違反 | 可 | 自動修正コミット |
| フォーマット違反 | 可 | 自動フォーマット |
| 型エラー | 可 | AIエージェントが修正 |

---

## Security ステージ

### 目的
セキュリティ脆弱性をスキャン

### 実行内容

```yaml
security:
  stages:
    - name: "依存関係スキャン"
      command: "npm audit --production"
      severity_threshold: "high"

    - name: "SASTスキャン"
      command: "semgrep --config=p/security-audit ."
      allow_failure: false

    - name: "シークレットスキャン"
      command: "gitleaks detect --source=."
      allow_failure: false

    - name: "コンテナスキャン"
      command: "trivy image app:${CI_COMMIT_SHA}"
      condition: "has_docker_image"
```

### 失敗時の対応

| エラー種別 | 自動修復 | 対応 |
|-----------|---------|------|
| 依存関係の脆弱性 | 部分的 | パッチバージョン更新 |
| コードの脆弱性 | 可 | AIエージェントが修正 |
| シークレット検出 | 不可 | 即時ブロック＋通知 |

---

## Deploy ステージ

### 目的
アプリケーションをデプロイ

### 実行内容

```yaml
deploy:
  stages:
    - name: "ステージング"
      environment: staging
      command: "kubectl apply -f k8s/staging/"
      condition: "branch == main"
      auto: true

    - name: "本番"
      environment: production
      command: "kubectl apply -f k8s/production/"
      condition: "tag =~ /^v[0-9]+/"
      auto: false  # 手動承認必須
      approval:
        required: 2
        timeout: "24h"
```

### デプロイ戦略

| 環境 | 戦略 | ロールバック |
|------|------|-------------|
| 開発 | Recreate | 即時 |
| ステージング | Rolling Update | 自動（失敗時） |
| 本番 | Blue-Green / Canary | 手動トリガー |

---

## AIエージェントによる自動修復

### 自動修復フロー

```
┌─────────────────┐
│ パイプライン失敗 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 失敗原因分析    │
│ (AI Agent)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
[修復可能]  [修復不可]
    │         │
    ▼         ▼
┌─────────┐ ┌─────────┐
│自動修正  │ │エスカレ │
│&再実行   │ │ーション │
└────┬────┘ └─────────┘
     │
     ▼
┌─────────────────┐
│ 修正コミット     │
│ & PR作成        │
└─────────────────┘
```

### 修復ポリシー

```yaml
auto_repair_policy:
  max_attempts: 3
  cooldown_between_attempts: "5m"

  enabled_for:
    - type: "lint_error"
      action: "auto_fix"
      require_review: false

    - type: "test_failure"
      action: "analyze_and_fix"
      require_review: true
      max_lines_changed: 50

    - type: "build_error"
      action: "analyze_and_fix"
      require_review: true

    - type: "type_error"
      action: "auto_fix"
      require_review: false

  disabled_for:
    - type: "security_vulnerability"
      action: "alert_only"
      notify: ["security-team"]

    - type: "infrastructure_error"
      action: "alert_only"
      notify: ["ops-team"]
```

### 修復レポート

修復実行後、以下の情報を記録：

```yaml
repair_report:
  pipeline_id: "<pipeline-id>"
  failure_type: "<type>"
  repair_agent: "<agent-id>"
  actions_taken:
    - description: "..."
      files_modified: [...]
      commit_hash: "<hash>"
  success: true/false
  duration: "<time>"
  next_steps: [...]
```

---

## 通知設定

### 通知ルール

| イベント | チャンネル | 対象 |
|---------|-----------|------|
| パイプライン成功 | Slack | #ci-notifications |
| パイプライン失敗 | Slack + Email | 担当者 |
| 自動修復成功 | Slack | #ci-notifications |
| 自動修復失敗 | Slack + PagerDuty | オンコール |
| 本番デプロイ | Slack + Email | 全員 |

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
