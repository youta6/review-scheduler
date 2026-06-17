import pytest
from fastapi import HTTPException

from app.main import get_all_user_endpoint

"""
==================================================
全ユーザー情報取得
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：get_all_user_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/ユーザー操作/全ユーザー情報取得_単体テスト仕様書.md
==================================================
"""

"""
===単体テストNo.1===
adminユーザーでログインした場合に全ユーザーリストが返ること
"""
def test_get_all_user_endpoint_001_admin_with_users(mocker, make_auth, make_user):
    auth = make_auth(admin_flag=True)
    users = [make_user(id=1, user_name="user_a"), make_user(id=2, user_name="user_b")]
    get_users_mock = mocker.patch("app.main.get_users", return_value=users)

    response = get_all_user_endpoint(auth, db=mocker.MagicMock())

    get_users_mock.assert_called_once()
    assert [user.user_name for user in response] == ["user_a", "user_b"]

"""
===単体テストNo.2===
adminユーザーでログインしてDBにユーザーが存在しない場合に404エラーが発生すること
"""
def test_get_all_user_endpoint_002_admin_no_users(mocker, make_auth):
    auth = make_auth(admin_flag=True)
    mocker.patch("app.main.get_users", return_value=[])

    with pytest.raises(HTTPException) as exc_info:
        get_all_user_endpoint(auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"

"""
===単体テストNo.3===
非adminユーザーでログインした場合にログインユーザーのみのリストが返ること
"""
def test_get_all_user_endpoint_003_non_admin(mocker, make_auth):
    auth = make_auth(user_name="login_user")
    get_users_mock = mocker.patch("app.main.get_users")

    response = get_all_user_endpoint(auth, db=mocker.MagicMock())

    get_users_mock.assert_not_called()
    assert len(response) == 1
    assert response[0].user_name == "login_user"
