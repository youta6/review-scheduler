# 復習項目作成 結合テスト実施 — SQLAlchemy select で複数モデル指定漏れ

作成日：2026/6/23

対象実装ファイル：`app/crud.py`（get_reviews 関数）

参照指摘表：
- `レビュー指摘表/結合テスト工程/テスト実施中/復習項目操作/復習項目作成_v0.1_レビュー指摘表.md`（No.2）

---

## バグ：get_reviews の select(Review) で JOIN 先の ReviewManagement が取得できなかった

### 発生した問題

復習項目作成 結合テスト No.3・No.5 実施時、作成後に GET /users/{user_id}/reviews を呼び出したところ HTTP 500 が返却された。

サーバーログを確認すると `IndexError: tuple index out of range` が発生していた。原因は `crud.py` の `get_reviews` 関数において、JOIN クエリのセレクト対象を `select(Review)` のみにしていたことだった。

```python
# 誤（バグあり）
results = db.execute(
    select(Review).join(
        ReviewManagement,
        (Review.user_id == ReviewManagement.user_id) &
        (Review.review_id == ReviewManagement.review_id)
    ).where(Review.user_id == user_id)
).all()

# 正（修正後）
results = db.execute(
    select(Review, ReviewManagement).join(
        ReviewManagement,
        (Review.user_id == ReviewManagement.user_id) &
        (Review.review_id == ReviewManagement.review_id)
    ).where(Review.user_id == user_id)
).all()
```

`select(Review)` のみを指定した場合、`db.execute(...).all()` の各 row は `Review` 1列のみのタプルになる。そのため後続で `row[1]`（ReviewManagement）にアクセスしようとすると `IndexError` が発生する。

`select(Review, ReviewManagement)` を指定することで、各 row が `(Review, ReviewManagement)` の2要素タプルとなり、`row[0]` = Review、`row[1]` = ReviewManagement として正しくアクセスできる。

### 本来どの工程で発見すべきだったか

**単体テスト工程**（get_reviews の単体テスト実施時）に発見すべきだった。

`get_reviews` の単体テストで JOIN 後の結果から `row[1]` へのアクセスを検証していれば、結合テストより前に発見できた。

### 見落とした理由

SQLAlchemy において `select(Model)` と `select(Model1, Model2)` では戻り値のタプル構造が異なる。`select(Review)` でも JOIN 構文は書けるため構文エラーにはならず、実行時にのみエラーが顕在化する。JOIN クエリを書いた際に「JOIN は実行するが SELECT は Review だけ」という状態になることを見落としていた。

### 教訓

- SQLAlchemy で複数テーブルを JOIN して両テーブルの列を使用する場合は、`select(ModelA, ModelB)` のように全モデルを明示する
- JOIN クエリを実装した際は「SELECT 対象」と「JOIN 対象」が一致しているかを必ず確認する
- 複数テーブルをまたぐ取得処理は単体テストで `row[0]`・`row[1]` のアクセスまで検証する
