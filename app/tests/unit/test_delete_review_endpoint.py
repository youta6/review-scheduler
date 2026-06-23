import pytest
from fastapi import HTTPException

from app.main import delete_review_endpoint

"""
==================================================
復習項目削除
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：delete_review_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/復習項目操作/復習項目削除_単体テスト仕様書.md
==================================================
"""

"""
===単体テストNo.1===
有効なユーザーが review_id=1 を指定した場合、ReviewDeleteResponse(status=True) が返ること
"""
def test_delete_review_endpoint_001_success(mocker, make_auth):
    auth = make_auth(delete_flag=False)
    mocker.patch("app.main.delete_review", return_value=1)
    mocker.patch("app.main.delete_review_management", return_value=1)

    response = delete_review_endpoint(review_id=1, auth=auth, db=mocker.MagicMock())

    assert response.status == True

"""
===単体テストNo.2===
delete_review・delete_review_management がいずれも None を返した場合に 404 エラーが発生すること
"""
def test_delete_review_endpoint_002_not_found(mocker, make_auth):
    auth = make_auth(delete_flag=False)
    mocker.patch("app.main.delete_review", return_value=None)
    mocker.patch("app.main.delete_review_management", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        delete_review_endpoint(review_id=999, auth=auth, db=mocker.MagicMock())

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "対象の復習項目は存在しません"
