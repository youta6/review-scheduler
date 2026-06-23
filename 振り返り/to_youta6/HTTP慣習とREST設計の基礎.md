# HTTP慣習と REST 設計の基礎

作成日：2026/6/22  
作成者：Claude Sonnet 4.6

---

## 1. なぜ GET・DELETE にリクエストボディを持たせてはいけないのか

### 1-1. HTTP メソッドの役割

HTTP メソッドにはそれぞれ決まった意味（セマンティクス）があります。

| メソッド | 役割 | ボディ |
|---|---|---|
| GET | リソースの取得 | 持たせない |
| POST | リソースの作成 | 持たせる（作成データ） |
| PUT | リソースの全置き換え | 持たせる（更新データ） |
| PATCH | リソースの部分更新 | 持たせる（更新データ） |
| DELETE | リソースの削除 | 持たせない |

### 1-2. RFC 9110 の規定

HTTP の公式仕様書 **RFC 9110「HTTP Semantics」（2022年）** には次の記載があります。

**GET（Section 9.3.1）**

> A client SHOULD NOT generate content in a GET request unless it is made directly to an origin server that has previously indicated, in or out of band, that such a request has a purpose and will be adequately supported.

意訳：クライアントは、サーバーが事前にサポートを明示していない限り、**GET リクエストにボディを含めるべきではない（SHOULD NOT）**。

**DELETE（Section 9.3.5）**

> A payload within a DELETE request message has no defined semantics; sending a payload body on a DELETE request might cause some existing implementations to reject the request.

意訳：DELETE リクエストのペイロード（ボディ）には**定義されたセマンティクスがない**。ボディを持つ DELETE リクエストは、既存の実装によっては拒否される可能性がある。

### 1-3. 実際に何が困るのか

GET・DELETE にボディを持たせると、以下の問題が発生します。

**① 多くの HTTP クライアントが対応していない**

```
# NG: curl はデフォルトで GET のボディを無視する
curl -X GET http://api.example.com/users/1 -d '{"user_name": "testuser"}'

# OK: クエリパラメータは全クライアントで動作する
curl http://api.example.com/users/1?user_name=testuser
```

**② OpenAPI (Swagger) が GET の requestBody を禁止している**

API ドキュメントの標準仕様である OpenAPI Specification 3.x では、GET に `requestBody` を記述することが禁止されています。Swagger UI などのツールで正しく表示・テストできなくなります。

**③ REST の設計原則に反する**

REST では「リソースは URL で識別する」というルールがあります。削除対象や取得対象を URL で表現することで、API の意図がひと目で分かるようになります。

```
# NG: URL を見ても何を取得・削除するか分からない
GET /users/1  + body: {"user_name": "testuser"}
DELETE /users/1/reviews/999  + body: {"review_id": 2}

# OK: URL だけで意図が分かる
GET /users/1
DELETE /users/1/reviews/2
```

### 1-4. 今回のケースでの正しい設計

| エンドポイント | 修正前 | 修正後 |
|---|---|---|
| ユーザー情報取得 | `GET /users/{user_id}` + body `user_name` | `GET /users/{user_id}` パスパラメータのみ |
| 復習項目削除 | `DELETE /users/{user_id}/reviews/{review_id}` + body `review_id` | `DELETE /users/{user_id}/reviews/{review_id}` パスパラメータのみ |

---

## 2. なぜ `get_user` と `get_user_by_id` を分けるのか

### 2-1. 問題の背景

今回の修正で「ユーザー情報取得エンドポイントを `user_name` ではなく `user_id` で検索する」ように変えました。しかし、crud.py の `get_user` 関数は `auth.py` でも使われています。

```python
# auth.py（認証処理）
user = get_user(db, user_name=user_name)  # ログイン時にユーザー名で検索

# main.py（エンドポイント）
user = get_user(db, user_name=user_name)  # ← これを user_id に変えたい
```

`get_user` の引数を `user_id` に変えると、`auth.py` が壊れます。

### 2-2. なぜ共通化しないのか

2つの「ユーザー検索」は**目的が根本的に異なります**。

| 項目 | 認証用（auth.py） | エンドポイント用（main.py） |
|---|---|---|
| **何を探すか** | ログインしてきた人 | URLで指定されたリソース |
| **検索キー** | `user_name`（ログイン識別子） | `user_id`（リソース識別子） |
| **使われる場面** | パスワード認証時 | REST API レスポンス生成時 |
| **変更頻度** | 認証方式が変わる時 | REST 設計が変わる時 |

認証は「このユーザー名・パスワードで来た人は誰か」を確認するため、ユーザー名で検索します。これは今後も変わりません。

REST エンドポイントは「URL で指定されたリソース（user_id）を返す」ため、user_id で検索します。

### 2-3. 単一責任の原則（SRP）

ソフトウェア設計の基本原則に**単一責任の原則（Single Responsibility Principle）**があります。

> 1つの関数・クラスは、1つのことだけに責任を持つべきである。

`get_user` に `user_name` と `user_id` の両方を持たせると、1つの関数が「2種類の検索方法」を担うことになり、責任が分散します。将来どちらかを変更する際に、もう一方に影響が出るリスクが生まれます。

```python
# NG: 1つの関数に2つの責任を持たせる（避けるべき）
def get_user(db, user_name=None, user_id=None):
    if user_name:
        return db.scalar(select(User).where(User.user_name == user_name, ...))
    elif user_id:
        return db.scalar(select(User).where(User.id == user_id))

# OK: 目的ごとに関数を分ける
def get_user(db, user_name: str):        # 認証用（auth.py から使う）
    ...

def get_user_by_id(db, user_id: int):    # エンドポイント用（main.py から使う）
    ...
```

### 2-4. 影響範囲を最小化する

認証（auth.py）は、ユーザー削除やユーザー情報取得とは独立した重要な処理です。エンドポイントの設計変更が認証ロジックに波及しないよう、関数を分けることで**変更の影響範囲を最小化**できます。

---

## 3. まとめ

| トピック | ルール | 理由 |
|---|---|---|
| GET のボディ | 使わない | RFC 9110 SHOULD NOT / クライアント非対応 |
| DELETE のボディ | 使わない | RFC 9110 セマンティクス未定義 / 実装によっては拒否 |
| リソース識別 | URL パスパラメータ | REST の原則「リソースは URL で識別する」 |
| 関数の責任 | 1関数1目的 | 単一責任の原則（SRP） |

---

## 参考文献

| 文書 | 内容 | URL |
|---|---|---|
| **RFC 9110** HTTP Semantics（2022年） | HTTP メソッドのセマンティクス（GET/DELETE のボディ規定） | https://www.rfc-editor.org/rfc/rfc9110 |
| **RFC 7231** HTTP/1.1 Semantics and Content（2014年） | RFC 9110 の前身。同様の規定あり（Section 4.3.1, 4.3.5） | https://www.rfc-editor.org/rfc/rfc7231 |
| **OpenAPI Specification 3.x** | GET に requestBody を記述することを禁止 | https://spec.openapis.org/oas/v3.1.0 |
| **Roy Fielding「Architectural Styles and the Design of Network-based Software Architectures」（2000年）** | REST の提唱論文。リソース識別に URI を使う原則の出典 | https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm |
| **単一責任の原則（SRP）** | Robert C. Martin「Clean Code」（2008年） | 書籍（ISBN: 9780132350884） |
