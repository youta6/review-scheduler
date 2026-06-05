from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: str


class ReviewBase(BaseModel):
    review_item: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)


class ReviewScheduleWithDoneFlag(BaseModel):
    review_time = int | None = Field(default=None, min_length=1, max_length=1)
    review_date = datetime
    done_status = str


class ReviewScheduleWithDoneFlagBase(ReviewBase):
    review_schedule_with_done_flag_list = list[ReviewScheduleWithDoneFlag]


class ReviewCreateRequest(BaseModel):
    review_item: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    study_date: datetime | None = None

class ReviewSchedule(BaseModel):
    review_time: str | None = Field(default=None, min_length=1, max_length=1)
    review_date: datetime | None = None

class ReviewCreateResponse(BaseModel):
    review_item: str | None = Field(default=None, min_length=1, max_length=200)
    study_date: datetime | None = None
    review_schedule_list: List[ReviewSchedule] | None = None

class ReviewUpdateRequest(ReviewBase):
    review_id: int = Field(default=None, min_length=1, max_length=3)
    review_time: int | None = Field(default=None, min_length=1, max_length=1)
    done_flag: bool | None = None


class ReviewUpdateResponse(ReviewScheduleWithDoneFlagBase):
    pass



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