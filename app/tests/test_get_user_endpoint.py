import pytest
from fastapi import HTTPException

from app.main import get_user_endpoint
from app.schemas import UserGetRequest

"""
==================================================
ユーザー情報取得
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：get_user_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/ユーザー操作/ユーザー情報取得_単体テスト仕様書.md
==================================================
"""

"""
===単体テストNo.1===
取得対象ユーザー名がNoneの場合、ログインユーザー自身の情報を返すこと
"""
def test_get_user_endpoint_001_self_none(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    # UserGetRequest.user_nameはstr必須のため、None指定はmodel_constructで検証を回避する
    request = UserGetRequest.model_construct(user_name=None)
    get_user_mock = mocker.patch("app.main.get_user")

    response = get_user_endpoint(request, auth, db=mocker.MagicMock())

    get_user_mock.assert_not_called()
    assert response.user_name == "login_user"

"""
===単体テストNo.2===
取得対象ユーザー名がログインユーザーと一致する場合、ログインユーザー自身の情報を返すこと
"""
def test_get_user_endpoint_002_self_named(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    request = UserGetRequest(user_name="login_user")
    get_user_mock = mocker.patch("app.main.get_user")

    response = get_user_endpoint(request, auth, db=mocker.MagicMock())

    get_user_mock.assert_not_called()
    assert response.user_name == "login_user"

"""
===単体テストNo.3===
取得対象ユーザー名が他者かつadminユーザーの場合、他者の情報を返すこと
"""
def test_get_user_endpoint_003_other_by_admin(mocker, make_auth, make_user):
    auth = make_auth(user_name="login_user", admin_flag=True)
    request = UserGetRequest(user_name="other_user")
    other_user = make_user(user_name="other_user")
    get_user_mock = mocker.patch("app.main.get_user", return_value=other_user)

    response = get_user_endpoint(request, auth, db=mocker.MagicMock())

    assert get_user_mock.call_args.kwargs["user_name"] == "other_user"
    assert response.user_name == "other_user"

"""
===単体テストNo.4===
取得対象ユーザー名が他者かつ非adminユーザーの場合に401エラーが発生すること
"""
def test_get_user_endpoint_004_other_by_non_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    request = UserGetRequest(user_name="other_user")

    with pytest.raises(HTTPException) as exc_info:
        get_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "他者のユーザー情報は取得できません"

"""
===単体テストNo.5===
get_userがNoneを返した場合に404エラーが発生すること
"""
def test_get_user_endpoint_005_not_found(mocker, make_auth):
    auth = make_auth(user_name="login_user", admin_flag=True)
    request = UserGetRequest(user_name="other_user")
    mocker.patch("app.main.get_user", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        get_user_endpoint(request, auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"
