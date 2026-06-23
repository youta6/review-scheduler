from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.main import delete_user_endpoint

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
URL の user_id がログインユーザーと一致する場合、自身を削除対象とすること
"""
def test_delete_user_endpoint_001_self(mocker, make_auth):
    auth = make_auth(user_id=1)
    deleted_user = mocker.MagicMock(user_name="login_user", updated_at=datetime.now(timezone.utc))
    delete_user_mock = mocker.patch("app.main.delete_user", return_value=deleted_user)

    response = delete_user_endpoint(user_id=1, auth=auth, db=mocker.MagicMock())

    assert delete_user_mock.call_args.kwargs["user_id"] == 1
    assert response.user_name == "login_user"

"""
===単体テストNo.2===
URL の user_id が他者かつ admin ユーザーの場合、他者を削除対象とすること
"""
def test_delete_user_endpoint_002_other_by_admin(mocker, make_auth):
    auth = make_auth(user_id=1, admin_flag=True)
    deleted_user = mocker.MagicMock(user_name="other_user", updated_at=datetime.now(timezone.utc))
    delete_user_mock = mocker.patch("app.main.delete_user", return_value=deleted_user)

    response = delete_user_endpoint(user_id=2, auth=auth, db=mocker.MagicMock())

    assert delete_user_mock.call_args.kwargs["user_id"] == 2
    assert response.user_name == "other_user"

"""
===単体テストNo.3===
URL の user_id が他者かつ非 admin ユーザーの場合に 401 エラーが発生すること
"""
def test_delete_user_endpoint_003_other_by_non_admin(mocker, make_auth):
    auth = make_auth(user_id=1, admin_flag=False)

    with pytest.raises(HTTPException) as exc_info:
        delete_user_endpoint(user_id=2, auth=auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "他者のユーザー情報は変更できません"

"""
===単体テストNo.4===
delete_user が None を返した場合に 404 エラーが発生すること
"""
def test_delete_user_endpoint_004_not_found(mocker, make_auth):
    auth = make_auth(user_id=1)
    mocker.patch("app.main.delete_user", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        delete_user_endpoint(user_id=1, auth=auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ユーザーが見つかりませんでした"
