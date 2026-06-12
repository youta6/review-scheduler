from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: str

"""
==================================================
ユーザー操作スキーマ
- ユーザーベース
- ユーザー作成リクエスト
- ユーザー作成レスポンス
- ユーザー情報更新リクエスト
- ユーザー情報更新レスポンス
- ユーザー情報削除リクエスト
- ユーザー情報削除レスポンス
- ユーザー情報取得リクエスト
- ユーザー情報取得レスポンス

設計書：review-scheduler\設計書\スキーマ（schemas）\ユーザー操作.md
==================================================
"""

"""
スキーマ論理名：ユーザーベース
"""
class UserBase(BaseModel):
    user_name: str = Field(min_length=1, max_length=50)

"""
スキーマ論理名：ユーザー作成リクエスト
"""
class UserCreateRequest(UserBase):
    password: str = Field(min_length=1, max_length=32)

"""
スキーマ論理名：ユーザー作成レスポンス
"""
class UserCreateResponse(UserBase):
    user_kind: str
    created_at: datetime


"""
スキーマ論理名：ユーザー情報更新リクエスト
"""
class UserUpdateRequest(BaseModel):
    user_name_before: str | None = Field(default=None, min_length=1, max_length=50)
    password_before: str | None = Field(default=None, min_length=1, max_length=32)
    user_name_after: str | None = Field(default=None, min_length=1, max_length=50)
    password_after: str | None = Field(default=None, min_length=1, max_length=32)

"""
スキーマ論理名：ユーザー情報更新レスポンス
"""
class UserUpdateResponse(UserBase):
    updated_at: datetime

"""
スキーマ論理名：ユーザー情報削除リクエスト
"""
class UserDeleteRequest(UserBase):
    password: str = Field(min_length=1, max_length=32)

"""
スキーマ論理名：ユーザー情報削除レスポンス
"""
class UserDeleteResponse(UserBase):
    updated_at: datetime

"""
スキーマ論理名：ユーザー情報取得リクエスト
"""
class UserGetRequest(UserBase):
    pass

"""
スキーマ論理名：ユーザー情報取得レスポンス
"""
class UserGetResponse(UserBase):
    user_id: int
    user_name: str
    delete_flag: bool
    user_kind: str
    created_at: datetime
    updated_at: datetime


"""
==================================================
認証・認可スキーマ
- トークン発行レスポンス
- 有効ユーザー検証レスポンス

設計書：review-scheduler\設計書\スキーマ（schemas）\認証・認可.md
==================================================
"""

"""
スキーマ論理名：トークン発行レスポンス
"""
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

"""
スキーマ論理名：有効ユーザー検証レスポンス
"""
class UserValidationResponse(BaseModel):
    user_id: int
    user_name: str
    hashed_password: str
    delete_flag: bool
    admin_flag: bool
    created_at: datetime
    updated_at: datetime


"""
==================================================
復習項目操作スキーマ
- 復習項目ベース
- 対応状況付き復習スケジュール
- 対応状況付き復習スケジュールベース
- 復習項目作成リクエスト
- 復習スケジュール
- 復習項目作成レスポンス
- 復習項目更新リクエスト
- 復習項目更新レスポンス
- 復習項目削除リクエスト
- 復習項目削除レスポンス
- 復習項目取得レスポンス

設計書：review-scheduler\設計書\スキーマ（schemas）\復習項目操作.md
==================================================
"""

"""
スキーマ論理名：復習項目ベース
"""
class ReviewBase(BaseModel):
    review_item: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)

"""
スキーマ論理名：対応状況付き復習スケジュール
"""
class ReviewScheduleWithDoneFlag(BaseModel):
    review_time: int | None = Field(default=None, min_length=1, max_length=1)
    review_date: datetime
    done_status: str

"""
スキーマ論理名：対応状況付き復習スケジュールベース
"""
class ReviewScheduleWithDoneFlagBase(ReviewBase):
    review_schedule_with_done_flag_list = list[ReviewScheduleWithDoneFlag]

"""
スキーマ論理名：復習項目作成リクエスト
"""
class ReviewCreateRequest(BaseModel):
    review_item: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    study_date: datetime | None = None

"""
スキーマ論理名：復習スケジュール
"""
class ReviewSchedule(BaseModel):
    review_time: str | None = Field(default=None, min_length=1, max_length=1)
    review_date: datetime | None = None

"""
スキーマ論理名：復習項目作成レスポンス
"""
class ReviewCreateResponse(BaseModel):
    review_item: str | None = Field(default=None, min_length=1, max_length=200)
    study_date: datetime | None = None
    review_schedule_list: List[ReviewSchedule] | None = None

"""
スキーマ論理名：復習項目更新リクエスト
"""
class ReviewUpdateRequest(ReviewBase):
    review_id: int = Field(default=None, min_length=1, max_length=3)
    review_time: int | None = Field(default=None, min_length=1, max_length=1)
    done_flag: bool | None = None

"""
スキーマ論理名：復習項目更新レスポンス
"""
class ReviewUpdateResponse(ReviewScheduleWithDoneFlagBase):
    pass

"""
スキーマ論理名：復習項目削除リクエスト
"""
class ReviewDeleteRequest(BaseModel):
    review_id: int = Field(min_length=1, max_length=3)

"""
スキーマ論理名：復習項目削除レスポンス
"""
class ReviewDeleteResponse(BaseModel):
    status: bool | None = None

"""
スキーマ論理名：復習項目取得レスポンス
"""
class ReviewGetResponse(ReviewScheduleWithDoneFlagBase):
    study_date: datetime | None = None
