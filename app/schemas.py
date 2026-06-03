from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


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
    user_name: str = Field(min_length=1, max_length=50)


class UserCreateRequest(UserBase):
    password: str = Field(min_length=1, max_length=32)

class UserCreateResponse(UserBase):
    user_kind: str
    created_at: datetime

class UserUpdateRequest(BaseModel):
    user_name_before: str | None = Field(default=None, min_length=1, max_length=50)
    password_before: str | None = Field(default=None, min_length=1, max_length=32)
    user_name_after: str | None = Field(default=None, min_length=1, max_length=50)
    password_after: str | None = Field(default=None, min_length=1, max_length=32)

class UserUpdateResponse(UserBase):
    updated_at: datetime

class UserDeleteRequest(UserBase):
    password: str = Field(min_length=1, max_length=32)

class UserDeleteResponse(UserBase):
    updated_at: datetime

class UserGetRequest(UserBase):
    pass

class UserGetResponse(UserBase):
    user_id: int
    user_name: str
    delete_flag: bool
    user_kind: str
    created_at: datetime
    updated_at: datetime

class TokenRequest(UserCreateRequest):
    pass

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserValidationResponse(BaseModel):
    user_id: int
    user_name: str
    hashed_password: str
    delete_flag: bool
    admin_flag: bool
    created_at: datetime
    updated_at: datetime