import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import jwt
import pytest
from fastapi import HTTPException

from app.auth import ALGORITHM, SECRET_KEY, generate_token, get_password_hash

"""
==================================================
トークン発行
テスト対象ファイル：auth.py
テスト対象クラス：-
テスト対象メソッド：generate_token
テスト仕様書：テスト仕様書/単体テスト仕様書/認証・認可/トークン発行_単体テスト仕様書.md
==================================================
"""

def _call_generate_token(form_data, db=None):
    return asyncio.run(generate_token(form_data, db))


def _make_form_data(username: str, password: str) -> SimpleNamespace:
    return SimpleNamespace(username=username, password=password)

"""
===単体テストNo.1===
get_userがNoneを返す場合に401エラーが発生すること
"""
def test_generate_token_001_user_not_found(mocker):
    mocker.patch("app.auth.get_user", return_value=None)
    form_data = _make_form_data("unknown_user", "any_password")

    with pytest.raises(HTTPException) as exc_info:
        _call_generate_token(form_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "ユーザー名かパスワードが間違っています。"

"""
===単体テストNo.2===
入力パスワードとハッシュ済みパスワードが一致しない場合に401エラーが発生すること
"""
def test_generate_token_002_password_mismatch(mocker):
    hashed_password = get_password_hash("correct_password")
    user = SimpleNamespace(user_name="login_user", hashed_password=hashed_password)
    mocker.patch("app.auth.get_user", return_value=user)
    form_data = _make_form_data("login_user", "wrong_password")

    with pytest.raises(HTTPException) as exc_info:
        _call_generate_token(form_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "ユーザー名かパスワードが間違っています。"

"""
===単体テストNo.3===
ユーザー認証成功時にTokenResponseが返ること
"""
def test_generate_token_003_token_response(mocker):
    hashed_password = get_password_hash("correct_password")
    user = SimpleNamespace(user_name="login_user", hashed_password=hashed_password)
    mocker.patch("app.auth.get_user", return_value=user)
    form_data = _make_form_data("login_user", "correct_password")

    response = _call_generate_token(form_data)

    assert isinstance(response.access_token, str)
    assert response.token_type == "bearer"

"""
===単体テストNo.4===
発行されたJWTのペイロードにユーザー名が設定されていること
"""
def test_generate_token_004_payload_sub(mocker):
    hashed_password = get_password_hash("correct_password")
    user = SimpleNamespace(user_name="login_user", hashed_password=hashed_password)
    mocker.patch("app.auth.get_user", return_value=user)
    form_data = _make_form_data("login_user", "correct_password")

    response = _call_generate_token(form_data)
    payload = jwt.decode(response.access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == "login_user"

"""
===単体テストNo.5===
発行されたJWTのペイロードに有効期限が設定されていること
"""
def test_generate_token_005_payload_exp(mocker):
    hashed_password = get_password_hash("correct_password")
    user = SimpleNamespace(user_name="login_user", hashed_password=hashed_password)
    mocker.patch("app.auth.get_user", return_value=user)
    form_data = _make_form_data("login_user", "correct_password")

    response = _call_generate_token(form_data)
    payload = jwt.decode(response.access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(timezone.utc)
