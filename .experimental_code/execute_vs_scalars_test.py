from datetime import datetime
from sqlalchemy import create_engine, select, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))


class Review(Base):
    __tablename__ = "reviews"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    review_item: Mapped[str] = mapped_column(String)


Base.metadata.create_all(bind=engine)

db = SessionLocal()

user = User(user_name="alice")
db.add(user)
db.flush()

db.add_all([
    Review(user_id=user.id, review_id=1, review_item="Python基礎"),
    Review(user_id=user.id, review_id=2, review_item="FastAPI入門"),
])
db.commit()


print("=" * 50)
print("単一エンティティ：execute() vs scalars()")
print("=" * 50)
print()

execute_result = db.execute(select(User)).all()
print(f"execute().all() の型:    {type(execute_result[0])}")
print(f"execute().all() の中身:  {execute_result}")
print(f"要素へのアクセス:        execute_result[0][0].user_name = {execute_result[0][0].user_name}")
print()

scalars_result = db.scalars(select(User)).all()
print(f"scalars().all() の型:    {type(scalars_result[0])}")
print(f"scalars().all() の中身:  {scalars_result}")
print(f"要素へのアクセス:        scalars_result[0].user_name = {scalars_result[0].user_name}")
print()


print("=" * 50)
print("複数エンティティ（JOIN）：execute() vs scalars()")
print("=" * 50)
print()

stmt = select(User, Review).join(Review, User.id == Review.user_id)

execute_result = db.execute(stmt).all()
print(f"execute().all() の型:    {type(execute_result[0])}")
print(f"execute().all() の中身:  {execute_result}")
print(f"[0][0] = {type(execute_result[0][0]).__name__}, user_name={execute_result[0][0].user_name}")
print(f"[0][1] = {type(execute_result[0][1]).__name__}, review_item={execute_result[0][1].review_item}")
print()

scalars_result = db.scalars(stmt).all()
print(f"scalars().all() の型:    {type(scalars_result[0])}")
print(f"scalars().all() の中身:  {scalars_result}")
print(f"※ ReviewManagement が消える: scalars_result[0].user_name = {scalars_result[0].user_name}")

db.close()
