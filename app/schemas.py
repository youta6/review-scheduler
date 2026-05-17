from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    status: str


class ReviewBase(BaseModel):
    review: str
    description: str | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    user_id: int
    review_id: int
    done_flag: bool | None = None
    update_date: datetime | None = None


class Review(ReviewBase):
    id: int
    owner_id: int
    done_flag: bool
    created_at: datetime
    update_date: datetime | None = None

    # model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    token: str
    reviews: List[Review] = []

    # model_config = ConfigDict(from_attributes=True)
