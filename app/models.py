from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String)
    deleted_flag:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)

    reviews = relationship("Review", back_populates="owner")

class Review(Base):
    __tablename__ = "reviews"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review:Mapped[str] = mapped_column(String)
    description:Mapped[str] = mapped_column(String, nullable=True)
    study_date:Mapped[datetime] = mapped_column(DateTime)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=func.now)

    owner = relationship("User", back_populates="reviews")

class ReviewManagement(Base):
    __tablename__ = "review_management"
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    review_id:Mapped[int] = mapped_column(Integer, ForeignKey("reviews.id"), primary_key=True)
    review_time:Mapped[int] = mapped_column(Integer)  # 復習回数
    review_date:Mapped[datetime] = mapped_column(DateTime)
    done_flag:Mapped[bool] = mapped_column(Boolean, default=False)

    review = relationship("Review")
