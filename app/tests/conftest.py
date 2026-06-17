from datetime import datetime, timezone
from typing import Callable

import pytest

from ..models import User
from ..schemas import UserValidationResponse


def _default_datetime() -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc)


@pytest.fixture()
def make_auth() -> Callable[..., UserValidationResponse]:
    """単体テスト用のログインユーザー（有効ユーザー検証．レスポンス）を生成するファクトリ"""
    def _make_auth(**overrides) -> UserValidationResponse:
        defaults = dict(
            user_id=1,
            user_name="login_user",
            hashed_password="login_user_hashed_password",
            delete_flag=False,
            admin_flag=False,
            created_at=_default_datetime(),
            updated_at=_default_datetime(),
        )
        defaults.update(overrides)
        return UserValidationResponse(**defaults)
    return _make_auth


@pytest.fixture()
def make_user() -> Callable[..., User]:
    """単体テスト用のUSERレコード（モデルインスタンス）を生成するファクトリ"""
    def _make_user(**overrides) -> User:
        defaults = dict(
            id=1,
            user_name="other_user",
            hashed_password="other_user_hashed_password",
            delete_flag=False,
            admin_flag=False,
            created_at=_default_datetime(),
            updated_at=_default_datetime(),
        )
        defaults.update(overrides)
        return User(**defaults)
    return _make_user