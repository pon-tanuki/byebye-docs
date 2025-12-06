# 用語集

## 概要

本ドキュメントはプロジェクトで使用する用語と、プロジェクト固有の定義を記載する。

---

## 一般用語

### A

| 用語 | 定義 |
|------|------|
| **Agent (エージェント)** | 自律的にタスクを実行するAIシステム。人間の介入なしに判断・行動できる。 |
| **API (Application Programming Interface)** | ソフトウェア間でデータや機能をやり取りするためのインターフェース。 |
| **Artifact (成果物)** | ビルドプロセスで生成されるファイルやパッケージ。 |

### B

| 用語 | 定義 |
|------|------|
| **Backlog (バックログ)** | 実装予定の機能やタスクの優先順位付きリスト。 |
| **Branch (ブランチ)** | Gitにおける開発の分岐点。並行開発を可能にする。 |

### C

| 用語 | 定義 |
|------|------|
| **CI/CD** | Continuous Integration / Continuous Deployment。継続的インテグレーション・デプロイメント。 |
| **Commit (コミット)** | Gitにおける変更の記録単位。 |
| **Coverage (カバレッジ)** | テストによってカバーされるコードの割合。 |

### D

| 用語 | 定義 |
|------|------|
| **Deploy (デプロイ)** | アプリケーションを実行環境に配置すること。 |
| **Domain Model (ドメインモデル)** | ビジネスロジックを表現するデータ構造と振る舞いの定義。 |

### E

| 用語 | 定義 |
|------|------|
| **Endpoint (エンドポイント)** | APIの特定のURLパス。 |
| **Entity (エンティティ)** | ビジネスドメインにおける識別可能なオブジェクト。 |
| **Escalation (エスカレーション)** | 問題を上位者または専門チームに報告すること。 |

### F-L

| 用語 | 定義 |
|------|------|
| **Feature Flag (フィーチャーフラグ)** | 機能の有効/無効を動的に切り替える仕組み。 |
| **Lint (リント)** | ソースコードの静的解析によるエラー・スタイル問題の検出。 |

### M-P

| 用語 | 定義 |
|------|------|
| **Merge (マージ)** | ブランチの変更を統合すること。 |
| **Pipeline (パイプライン)** | 自動化されたビルド・テスト・デプロイのプロセス。 |
| **PR (Pull Request)** | コード変更のレビュー・マージ依頼。 |

### R-S

| 用語 | 定義 |
|------|------|
| **Repository (リポジトリ)** | ソースコードとその履歴を管理する保管場所。 |
| **Schema (スキーマ)** | データ構造の定義。 |
| **Sprint (スプリント)** | アジャイル開発における固定期間の開発サイクル。 |

### T-Z

| 用語 | 定義 |
|------|------|
| **Test (テスト)** | コードの正確性を検証するプログラム。 |
| **Token (トークン)** | 認証・認可に使用される識別子。 |

---

## プロジェクト固有の定義

### AIエージェント関連

| 用語 | 定義 |
|------|------|
| **Developer Agent** | コード生成・実装を担当するAIエージェント。 |
| **Reviewer Agent** | コードレビューを担当するAIエージェント。 |
| **QA Agent** | テスト・品質保証を担当するAIエージェント。 |
| **Architect Agent** | 設計・アーキテクチャを担当するAIエージェント。 |
| **Agent Orchestrator** | 複数のエージェントを制御・調整するシステム。 |

### プロセス関連

| 用語 | 定義 |
|------|------|
| **Human-in-the-Loop** | 重要な判断ポイントで人間が介入するプロセス。 |
| **Auto-Repair (自動修復)** | CI/CD失敗時にAIエージェントが自動で修正するプロセス。 |
| **Autonomous Mode (自律モード)** | 人間の承認なしにエージェントがタスクを完了するモード。 |
| **Supervised Mode (監視モード)** | 人間の承認を必要とするモード。 |

### ドキュメント関連

| 用語 | 定義 |
|------|------|
| **TAML** | Text-based Application Markup Language。本プロジェクトで使用するYAML風の構造化形式。 |
| **AI_EDITABLE マーカー** | AIエージェントが編集可能なセクションを示すコメントマーカー。 |

---

## 略語一覧

| 略語 | 正式名称 | 意味 |
|------|---------|------|
| AI | Artificial Intelligence | 人工知能 |
| API | Application Programming Interface | アプリケーションプログラミングインターフェース |
| CI | Continuous Integration | 継続的インテグレーション |
| CD | Continuous Deployment | 継続的デプロイメント |
| CRUD | Create, Read, Update, Delete | 基本的なデータ操作 |
| DTO | Data Transfer Object | データ転送オブジェクト |
| JWT | JSON Web Token | JSON形式の認証トークン |
| MVP | Minimum Viable Product | 実用最小限の製品 |
| ORM | Object-Relational Mapping | オブジェクト関係マッピング |
| PII | Personally Identifiable Information | 個人識別情報 |
| RBAC | Role-Based Access Control | ロールベースアクセス制御 |
| REST | Representational State Transfer | RESTアーキテクチャスタイル |
| SLA | Service Level Agreement | サービスレベル合意 |
| SSO | Single Sign-On | シングルサインオン |
| UUID | Universally Unique Identifier | 汎用一意識別子 |

---

## 用語追加ガイドライン

新しい用語を追加する場合：

1. 適切なカテゴリに配置
2. 簡潔で明確な定義を記載
3. 必要に応じて例を追加
4. 変更履歴に記録

---

_最終更新日: YYYY-MM-DD_
_更新者: [担当者/AIエージェント名]_
