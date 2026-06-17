from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.main import update_user_endpoint
from app.schemas import UserUpdateRequest

"""
==================================================
ユーザー情報更新
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：update_user_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/ユーザー操作/ユーザー情報更新_単体テスト仕様書.md
==================================================
"""

"""
===単体テストNo.1===
変更後ユーザー名・変更後パスワードがともに未入力の場合、DBアクセスせずに現在のユーザー情報を返すこと
"""
def test_update_user_endpoint_001_no_change(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    update_user_mock = mocker.patch("app.main.update_user")
    request = UserUpdateRequest()

    response = update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert response.user_name == auth.user_name
    assert response.updated_at == auth.updated_at
    update_user_mock.assert_not_called()

"""
===単体テストNo.2===
変更前ユーザー名がNoneの場合、ログインユーザー自身を更新対象とすること
"""
def test_update_user_endpoint_002_self_before_none(mocker, make_auth):
    auth = make_auth(user_name="login_user", hashed_password="login_user_hashed_password")
    updated_user = mocker.MagicMock(user_name="new_name", updated_at=datetime.now(timezone.utc))
    update_user_mock = mocker.patch("app.main.update_user", return_value=updated_user)
    request = UserUpdateRequest(user_name_after="new_name")

    response = update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert update_user_mock.call_args.kwargs["user_name_before"] == auth.user_name
    assert response.user_name == "new_name"

"""
===単体テストNo.3===
変更前ユーザー名がログインユーザーと一致する場合、自身を更新対象とすること
"""
def test_update_user_endpoint_003_self_before_matches(mocker, make_auth):
    auth = make_auth(user_name="login_user", hashed_password="login_user_hashed_password")
    updated_user = mocker.MagicMock(user_name="new_name", updated_at=datetime.now(timezone.utc))
    update_user_mock = mocker.patch("app.main.update_user", return_value=updated_user)
    request = UserUpdateRequest(user_name_before="login_user", user_name_after="new_name")

    response = update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert update_user_mock.call_args.kwargs["user_name_before"] == auth.user_name
    assert response.user_name == "new_name"

"""
===単体テストNo.4===
変更前ユーザー名が他者かつadminユーザーの場合、他者を更新対象とすること
"""
def test_update_user_endpoint_004_other_by_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user", admin_flag=True)
    updated_user = mocker.MagicMock(user_name="new_name", updated_at=datetime.now(timezone.utc))
    update_user_mock = mocker.patch("app.main.update_user", return_value=updated_user)
    request = UserUpdateRequest(
        user_name_before="other_user",
        password_before="other_password",
        user_name_after="new_name",
    )

    response = update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert update_user_mock.call_args.kwargs["user_name_before"] == "other_user"
    assert response.user_name == "new_name"

"""
===単体テストNo.5===
変更前ユーザー名が他者かつ非adminユーザーの場合に401エラーが発生すること
"""
def test_update_user_endpoint_005_other_by_non_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    request = UserUpdateRequest(
        user_name_before="other_user",
        password_before="other_password",
        user_name_after="new_name",
    )

    with pytest.raises(HTTPException) as exc_info:
        update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "他者のユーザー情報は変更できません"

"""
===単体テストNo.6===
update_userがNoneを返した場合に404エラーが発生すること
"""
def test_update_user_endpoint_006_user_not_found(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    mocker.patch("app.main.update_user", return_value=None)
    request = UserUpdateRequest(user_name_before=None, user_name_after="new_name")

    with pytest.raises(HTTPException) as exc_info:
        update_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"
