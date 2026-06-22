"""
==================================================
復習項目削除
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：delete_review_endpoint
テスト仕様書：test_specification/integration_test_specification/復習項目操作/復習項目削除_結合テスト仕様書.md
==================================================
"""


def _create_review(client, token: str) -> None:
    client.post(
        "/users/1/reviews",
        json={"review_item": "テスト復習項目"},
        headers={"Authorization": f"Bearer {token}"},
    )


"""
===結合テストNo.1===
review_id を URL に指定して DELETE した場合、HTTP 200 と status=true が返却されること
"""
def test_delete_review_endpoint_001_delete_review(client, make_token):
    token = make_token("testuser", "testpass")
    _create_review(client, token)

    response = client.delete(
        "/users/1/reviews/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == True


"""
===結合テストNo.2===
削除済みの review_id を URL に指定して DELETE した場合、HTTP 404 が返却されること
"""
def test_delete_review_endpoint_002_already_deleted(client, make_token):
    token = make_token("testuser", "testpass")
    _create_review(client, token)
    client.delete(
        "/users/1/reviews/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.delete(
        "/users/1/reviews/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "対象の復習項目は存在しません"


"""
===結合テストNo.3===
review_id に整数以外の値を指定した場合、HTTP 422 が返却されること
"""
def test_delete_review_endpoint_003_invalid_review_id(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.delete(
        "/users/1/reviews/abc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


"""
===結合テストNo.4===
ログイン後に管理者によって削除されたユーザーが有効期限内のトークンで DELETE した場合、HTTP 401 が返却されること
"""
def test_delete_review_endpoint_004_deleted_user(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    token = make_token("testuser", "testpass")
    _create_review(client, token)

    admin_token = make_token("admin", "adminpass")
    client.delete("/users/1", headers={"Authorization": f"Bearer {admin_token}"})

    response = client.delete(
        "/users/1/reviews/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
