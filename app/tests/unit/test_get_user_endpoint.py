import pytest
from fastapi import HTTPException

from app.main import get_user_endpoint

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
URL の user_id がログインユーザーと一致する場合、DBアクセスなしで自身の情報を返すこと
"""
def test_get_user_endpoint_001_self(mocker, make_auth):
    auth = make_auth(user_id=1, user_name="login_user")
    get_user_by_id_mock = mocker.patch("app.main.get_user_by_id")

    response = get_user_endpoint(user_id=1, auth=auth, db=mocker.MagicMock())

    get_user_by_id_mock.assert_not_called()
    assert response.user_name == "login_user"

"""
===単体テストNo.2===
URL の user_id が他者かつ admin ユーザーの場合、他者の情報を返すこと
"""
def test_get_user_endpoint_002_other_by_admin(mocker, make_auth, make_user):
    auth = make_auth(user_id=1, user_name="admin_user", admin_flag=True)
    other_user = make_user(user_name="other_user")
    get_user_by_id_mock = mocker.patch("app.main.get_user_by_id", return_value=other_user)

    response = get_user_endpoint(user_id=2, auth=auth, db=mocker.MagicMock())

    assert get_user_by_id_mock.call_args.kwargs["user_id"] == 2
    assert response.user_name == "other_user"

"""
===単体テストNo.3===
URL の user_id が他者かつ非 admin ユーザーの場合に 401 エラーが発生すること
"""
def test_get_user_endpoint_003_other_by_non_admin(mocker, make_auth):
    auth = make_auth(user_id=1, user_name="login_user")

    with pytest.raises(HTTPException) as exc_info:
        get_user_endpoint(user_id=2, auth=auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "他者のユーザー情報は取得できません"

"""
===単体テストNo.4===
get_user_by_id が None を返した場合に 404 エラーが発生すること
"""
def test_get_user_endpoint_004_not_found(mocker, make_auth):
    auth = make_auth(user_id=1, user_name="admin_user", admin_flag=True)
    mocker.patch("app.main.get_user_by_id", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        get_user_endpoint(user_id=999, auth=auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"
