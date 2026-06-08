from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

"""
==================================================
テーブル定義
設計書：review-scheduler\設計書\テーブル定義（models）.md
==================================================
"""

"""
テーブル論理名：ユーザー情報
テーブル物理名：USER
"""
class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer(2), primary_key=True, index=True)
    user_name:Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255))
    delete_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    admin_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)

    reviews = relationship("Review", back_populates="owner")

"""
テーブル論理名：復習情報
テーブル物理名：REVIEW
"""
class Review(Base):
    __tablename__ = "reviews"
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review_id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    review_item:Mapped[str] = mapped_column(String)
    description:Mapped[str] = mapped_column(String, nullable=True)
    study_date:Mapped[datetime] = mapped_column(DateTime)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)

    owner = relationship("User", back_populates="reviews")

"""
テーブル論理名：復習管理情報
テーブル物理名：REVIEW_MANAGEMENT
"""
class ReviewManagement(Base):
    __tablename__ = "review_management"
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    review_id:Mapped[int] = mapped_column(Integer, ForeignKey("reviews.review_id"), primary_key=True)
    review_time:Mapped[int] = mapped_column(Integer, primary_key=True)
    review_date:Mapped[datetime] = mapped_column(DateTime)
    done_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)

    review = relationship("Review")
