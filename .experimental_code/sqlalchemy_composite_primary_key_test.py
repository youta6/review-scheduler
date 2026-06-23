"""
SQLAlchemy における複合主キーの解説

■ 発見の経緯
  復習項目取得 結合テスト No.3 実施中、複数ユーザーがそれぞれ復習項目を作成すると
  IntegrityError: UNIQUE constraint failed: reviews.review_id が発生した。

■ 原因
  app/models.py の Review モデルで review_id が単独の primary_key=True になっているため、
  異なるユーザー間でも review_id の一意性が強制される。

  設計上 review_id はユーザーごとに採番（1, 2, 3...）されるため、
  主キーを (user_id, review_id) の複合主キーにすべきだった。

■ 正しい設計
  user_id と review_id の両方を primary_key=True にする（複合主キー）。
  SQLAlchemy は同じテーブル内で複数の primary_key=True があると自動的に複合主キーと解釈する。
"""

from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# NG パターン：review_id が単独主キー
# ============================================================
class UserNG(Base):
    __tablename__ = "users_ng"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))


class ReviewNG(Base):
    __tablename__ = "reviews_ng"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_ng.id"))
    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)  # ← 単独主キー
    review_item: Mapped[str] = mapped_column(String)


# ============================================================
# OK パターン：(user_id, review_id) の複合主キー
# ============================================================
class UserOK(Base):
    __tablename__ = "users_ok"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))


class ReviewOK(Base):
    __tablename__ = "reviews_ok"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_ok.id"), primary_key=True)  # ← 複合主キーの一部
    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    review_item: Mapped[str] = mapped_column(String)


Base.metadata.create_all(bind=engine)


# ============================================================
# NG パターンの動作確認
# ============================================================
print("=" * 60)
print("NG パターン：review_id が単独主キーの場合")
print("=" * 60)

db = SessionLocal()
user1 = UserNG(user_name="alice")
user2 = UserNG(user_name="bob")
db.add_all([user1, user2])
db.flush()

db.add(ReviewNG(user_id=user1.id, review_id=1, review_item="alice の復習項目"))
db.flush()
print(f"alice の review_id=1 の登録: OK")

try:
    db.add(ReviewNG(user_id=user2.id, review_id=1, review_item="bob の復習項目"))
    db.flush()
    print(f"bob の review_id=1 の登録: OK（ここには到達しない）")
except IntegrityError as e:
    db.rollback()
    print(f"bob の review_id=1 の登録: IntegrityError が発生!")
    print(f"  → UNIQUE constraint failed: reviews_ng.review_id")
    print(f"  → review_id=1 は alice がすでに使っているため bob は登録できない")

db.close()

print()

# ============================================================
# OK パターンの動作確認
# ============================================================
print("=" * 60)
print("OK パターン：(user_id, review_id) が複合主キーの場合")
print("=" * 60)

db = SessionLocal()
user1 = UserOK(user_name="alice")
user2 = UserOK(user_name="bob")
db.add_all([user1, user2])
db.flush()

db.add(ReviewOK(user_id=user1.id, review_id=1, review_item="alice の復習項目"))
db.flush()
print(f"alice の review_id=1 の登録: OK")

db.add(ReviewOK(user_id=user2.id, review_id=1, review_item="bob の復習項目"))
db.flush()
print(f"bob の review_id=1 の登録: OK  ← ユーザーが違えば同じ review_id を持てる")

db.add(ReviewOK(user_id=user1.id, review_id=2, review_item="alice の2件目"))
db.flush()
print(f"alice の review_id=2 の登録: OK")

db.commit()

reviews = db.query(ReviewOK).order_by(ReviewOK.user_id, ReviewOK.review_id).all()
print()
print("登録結果：")
for r in reviews:
    print(f"  user_id={r.user_id}, review_id={r.review_id}, review_item={r.review_item}")

db.close()

print()
print("=" * 60)
print("まとめ")
print("=" * 60)
print("単独主キー：review_id はテーブル全体で一意")
print("            → 異なるユーザーが同じ review_id を持てない")
print()
print("複合主キー：(user_id, review_id) の組み合わせが一意")
print("            → 同じ review_id でもユーザーが違えば登録できる")
print("            → 設定方法：両カラムに primary_key=True を付ける")
