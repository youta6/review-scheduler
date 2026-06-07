from datetime import datetime, timezone
from itertools import groupby

from sqlalchemy import create_engine, select, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship

# --- DB設定（メモリ上に作成） ---
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# --- モデル定義 ---
class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_name:Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255))
    delete_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    admin_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    reviews = relationship("Review", back_populates="owner")

class Review(Base):
    __tablename__ = "reviews"
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review_id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    review_item:Mapped[str] = mapped_column(String)
    description:Mapped[str] = mapped_column(String, nullable=True)
    study_date:Mapped[datetime] = mapped_column(DateTime)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner = relationship("User", back_populates="reviews")

class ReviewManagement(Base):
    __tablename__ = "review_management"
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    review_id:Mapped[int] = mapped_column(Integer, ForeignKey("reviews.review_id"), primary_key=True)
    review_time:Mapped[int] = mapped_column(Integer, primary_key=True)
    review_date:Mapped[datetime] = mapped_column(DateTime)
    done_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    review = relationship("Review")



# --- テーブル作成 ---
Base.metadata.create_all(bind=engine)

# --- 仮データ作成 ---
db = SessionLocal()
today = datetime(2026, 5, 1, tzinfo=timezone.utc)

user = User(user_name="alice", hashed_password="hashed")
db.add(user)
db.flush()

db.add_all([
    Review(user_id=user.id, review_id=1, review_item="Python基礎", description="変数、関数など", study_date=today),
    Review(user_id=user.id, review_id=2, review_item="FastAPI入門", description=None, study_date=today),
])
db.flush()

db.add_all([
    ReviewManagement(user_id=user.id, review_id=1, review_time=1, review_date=datetime(2026, 5, 2), done_flag=False),
    ReviewManagement(user_id=user.id, review_id=1, review_time=2, review_date=datetime(2026, 5, 4), done_flag=False),
    ReviewManagement(user_id=user.id, review_id=1, review_time=3, review_date=datetime(2026, 5, 8), done_flag=True),
    ReviewManagement(user_id=user.id, review_id=2, review_time=1, review_date=datetime(2026, 5, 2), done_flag=False),
    ReviewManagement(user_id=user.id, review_id=2, review_time=2, review_date=datetime(2026, 5, 4), done_flag=False),
    ReviewManagement(user_id=user.id, review_id=2, review_time=3, review_date=datetime(2026, 5, 8), done_flag=False),
])
db.commit()

# --- SQLAlchemyのjoinで取得 ---
stmt = select(Review, ReviewManagement).join(
    ReviewManagement,
    (Review.user_id == ReviewManagement.user_id) &
    (Review.review_id == ReviewManagement.review_id)
).where(Review.user_id == user.id)

results = db.execute(stmt).all()

print("=== joinの生の結果 ===")
for review, mgmt in results:
    print(f"review_id={review.review_id}, review_item={review.review_item}, review_time={mgmt.review_time}")

# --- ソートしてグループ化 ---
sorted_results = sorted(results, key=lambda x: x[0].review_id)

print("\n=== グループ化後 ===")
for review_id, group in groupby(sorted_results, key=lambda x: x[0].review_id):
    group_list = list(group)
    # print(type(group_list[0]))     # → Row (タプル全体)
    # print(type(group_list[0][0]))  # → Review
    # print(type(group_list[0][1]))  # → ReviewManagement
    first_review = group_list[0][0]
    print(f"\nreview_id={review_id}, review_item={first_review.review_item}")
    for _, mgmt in group_list:
        print(f"  review_time={mgmt.review_time}, review_date={mgmt.review_date}, done_flag={mgmt.done_flag}")

db.close()
