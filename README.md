# review-scheduler

エビングハウスの忘却曲線に基づいた復習スケジューラー API。
復習項目を登録すると、忘却曲線の理論に基づき5回分の復習予定日を自動生成する。

---

## 機能

- ユーザー登録・ログイン・更新・削除
- 復習情報の登録・取得・更新・削除
- 復習スケジュールの自動生成（学習日 +1, +3, +7, +15, +31日）
- 管理者による全ユーザー情報の管理

## 技術スタック

| 区分 | 技術 |
|---|---|
| 言語 | Python 3.13 |
| フレームワーク | FastAPI 0.137 |
| ORM | SQLAlchemy 2.0 |
| バリデーション | Pydantic 2.x |
| 認証 | JWT（PyJWT） |
| パスワードハッシュ | pwdlib 0.3（Argon2） |
| DB（本番） | PostgreSQL |
| DB（開発） | SQLite |
| コンテナ | Docker |
| クラウド | AWS |

---

## セットアップ

### 1. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成する。

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DUMMY_HASH=your_dummy_hash
ADMIN_SECRET_KEY_NAME=your_admin_name
ADMIN_SECRET_KEY_PASSWORD=your_admin_password
```

> **注意**: `.env` のクォートは不要。`KEY=value` 形式で記述する。

### 2. Docker で起動

```bash
# イメージのビルド
docker build -t review-scheduler-image .

# コンテナの起動
docker run -d --name review-scheduler-container --env-file .env -p 80:80 review-scheduler-image
```

起動後、`http://localhost/docs` で Swagger UI にアクセスできる。

### 3. ローカル（uv）で起動

```bash
uv sync
uv run fastapi dev app/main.py
```

起動後、`http://localhost:8000/docs` で Swagger UI にアクセスできる。

---

## API エンドポイント

| 機能 | HTTPメソッド | エンドポイント | 認証 |
|---|---|---|---|
| ホーム | GET | / | 不要 |
| ヘルスチェック | GET | /health-check | 不要 |
| トークン発行（ログイン） | POST | /token | 不要 |
| ユーザー作成 | POST | /users | 不要 |
| 全ユーザー取得 | GET | /users | 要（管理者のみ） |
| ユーザー情報取得 | GET | /users/{user_id} | 要 |
| ユーザー情報更新 | PUT | /users/{user_id} | 要 |
| ユーザー削除 | DELETE | /users/{user_id} | 要 |
| 復習項目作成 | POST | /users/{user_id}/reviews | 要 |
| 復習項目取得 | GET | /users/{user_id}/reviews | 要 |
| 復習項目更新 | PATCH | /users/{user_id}/reviews/{review_id} | 要 |
| 復習項目削除 | DELETE | /users/{user_id}/reviews/{review_id} | 要 |

認証が必要なエンドポイントは、`POST /token` で取得した Bearer トークンを Authorization ヘッダーに付与する。

---

## テスト

### 単体テスト

```bash
uv run pytest app/tests/unit
```

### 結合テスト

```bash
uv run pytest app/tests/integration
```

### 全テスト

```bash
uv run pytest
```

---

## プロジェクト構成

```
review-scheduler/
├── app/
│   ├── main.py          # エンドポイント定義
│   ├── auth.py          # JWT認証・有効ユーザー検証
│   ├── crud.py          # DB操作
│   ├── models.py        # テーブル定義
│   ├── schemas.py       # リクエスト・レスポンススキーマ
│   ├── database.py      # DB接続設定
│   └── tests/
│       ├── unit/        # 単体テスト
│       └── integration/ # 結合テスト
├── Dockerfile
├── requirements.txt
└── .env                 # 環境変数（Gitに含めない）
```
