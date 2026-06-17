import asyncio
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException

from app.auth import ALGORITHM, SECRET_KEY, get_current_active_user

"""
==================================================
トークン発行
テスト対象ファイル：auth.py
テスト対象クラス：-
テスト対象メソッド：get_current_active_user
テスト仕様書：テスト仕様書/単体テスト仕様書/認証・認可/有効ユーザー検証_単体テスト仕様書.md
==================================================
"""

def _call_get_current_active_user(token: str, db=None):
    return asyncio.run(get_current_active_user(token, db))


def _encode(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _valid_payload(sub: str = "login_user") -> dict:
    return {"sub": sub, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}

"""
===単体テストNo.1===
有効なJWTトークンかつDBにユーザーが存在する場合にUserValidationResponseが返ること
"""
def test_get_current_active_user_001_valid(mocker, make_user):
    user = make_user(user_name="login_user")
    mocker.patch("app.auth.get_user", return_value=user)
    token = _encode(_valid_payload("login_user"))

    response = _call_get_current_active_user(token)

    assert response.user_name == "login_user"

"""
===単体テストNo.2===
不正な文字列をトークンとして渡した場合に401エラーが発生すること
"""
def test_get_current_active_user_002_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        _call_get_current_active_user("invalid_token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "資格情報を検証できませんでした"

"""
===単体テストNo.3===
JWTペイロードにsubが含まれない場合に401エラーが発生すること
"""
def test_get_current_active_user_003_sub_missing():
    token = _encode({"exp": datetime.now(timezone.utc) + timedelta(minutes=15)})

    with pytest.raises(HTTPException) as exc_info:
        _call_get_current_active_user(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "資格情報を検証できませんでした"

"""
===単体テストNo.4===
DBにユーザーが存在しない場合に401エラーが発生すること
"""
def test_get_current_active_user_004_user_not_found(mocker):
    mocker.patch("app.auth.get_user", return_value=None)
    token = _encode(_valid_payload("login_user"))

    with pytest.raises(HTTPException) as exc_info:
        _call_get_current_active_user(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "資格情報を検証できませんでした"

"""
===単体テストNo.5===
delete_flag=Trueのユーザーで認証した場合に400エラーが発生すること
"""
def test_get_current_active_user_005_deleted_user(mocker, make_user):
    user = make_user(user_name="login_user", delete_flag=True)
    mocker.patch("app.auth.get_user", return_value=user)
    token = _encode(_valid_payload("login_user"))

    with pytest.raises(HTTPException) as exc_info:
        _call_get_current_active_user(token)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "削除済みのユーザーです"
