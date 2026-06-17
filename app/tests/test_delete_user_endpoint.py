from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.main import delete_user_endpoint
from app.schemas import UserDeleteRequest

"""
==================================================
ユーザー情報削除
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：delete_user_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/ユーザー操作/ユーザー情報削除_単体テスト仕様書.md
==================================================
"""

"""
===単体テストNo.1===
削除対象ユーザー名がNoneの場合、ログインユーザー自身を削除対象とすること
"""
def test_delete_user_endpoint_001_self_none(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    # UserDeleteRequest.user_nameはstr必須のため、None指定はmodel_constructで検証を回避する
    request = UserDeleteRequest.model_construct(user_name=None, password="any_password")
    deleted_user = mocker.MagicMock(user_name="login_user", updated_at=datetime.now(timezone.utc))
    delete_user_mock = mocker.patch("app.main.delete_user", return_value=deleted_user)

    response = delete_user_endpoint(request, auth, db=mocker.MagicMock())

    assert delete_user_mock.call_args.kwargs["user_name"] == "login_user"
    assert response.user_name == "login_user"

"""
===単体テストNo.2===
削除対象ユーザー名がログインユーザーと一致する場合、自身を削除対象とすること
"""
def test_delete_user_endpoint_002_self_named(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    request = UserDeleteRequest(user_name="login_user", password="any_password")
    deleted_user = mocker.MagicMock(user_name="login_user", updated_at=datetime.now(timezone.utc))
    delete_user_mock = mocker.patch("app.main.delete_user", return_value=deleted_user)

    response = delete_user_endpoint(request, auth, db=mocker.MagicMock())

    assert delete_user_mock.call_args.kwargs["user_name"] == "login_user"
    assert response.user_name == "login_user"

"""
===単体テストNo.3===
削除対象ユーザー名が他者かつadminユーザーの場合、他者を削除対象とすること
"""
def test_delete_user_endpoint_003_other_by_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user", admin_flag=True)
    request = UserDeleteRequest(user_name="other_user", password="any_password")
    deleted_user = mocker.MagicMock(user_name="other_user", updated_at=datetime.now(timezone.utc))
    delete_user_mock = mocker.patch("app.main.delete_user", return_value=deleted_user)

    response = delete_user_endpoint(request, auth, db=mocker.MagicMock())

    assert delete_user_mock.call_args.kwargs["user_name"] == "other_user"
    assert response.user_name == "other_user"

"""
===単体テストNo.4===
削除対象ユーザー名が他者かつ非adminユーザーの場合に401エラーが発生すること
"""
def test_delete_user_endpoint_004_other_by_non_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user", admin_flag=False)
    request = UserDeleteRequest(user_name="other_user", password="any_password")

    with pytest.raises(HTTPException) as exc_info:
        delete_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "他者のユーザー情報は変更できません"

"""
===単体テストNo.5===
delete_userがNoneを返した場合に404エラーが発生すること
"""
def test_delete_user_endpoint_005_not_found(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    request = UserDeleteRequest(user_name="login_user", password="any_password")
    mocker.patch("app.main.delete_user", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        delete_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"
