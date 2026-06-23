"""
==================================================
ユーザー情報取得
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：get_user_endpoint
テスト仕様書：test_specification/integration_test_specification/ユーザー操作/ユーザー情報取得_結合テスト仕様書.md
==================================================
"""


"""
===結合テストNo.1===
自分の user_id を URL に指定して GET した場合、HTTP 200 と自身の情報が返却されること
"""
def test_get_user_endpoint_001_get_self(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 1
    assert body["user_name"] == "testuser"
    assert body["delete_flag"] == False
    assert body["user_kind"] == "一般"
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


"""
===結合テストNo.2===
管理者が他ユーザーの user_id を URL に指定して GET した場合、HTTP 200 と対象ユーザーの情報が返却されること
"""
def test_get_user_endpoint_002_admin_gets_other_user(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    admin_token = make_token("admin", "adminpass")
    make_token("testuser", "testpass")

    response = client.get(
        "/users/2",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "testuser"
    assert body["user_kind"] == "一般"


"""
===結合テストNo.3===
一般ユーザーが他ユーザーの user_id を URL に指定して GET した場合、HTTP 401 が返却されること
"""
def test_get_user_endpoint_003_regular_user_gets_other(client, make_token):
    make_token("testuser", "testpass")
    token2 = make_token("testuser2", "testpass2")

    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "他者のユーザー情報は取得できません"


"""
===結合テストNo.4===
存在しない user_id を URL に指定して GET した場合（管理者）、HTTP 404 が返却されること
"""
def test_get_user_endpoint_004_admin_gets_nonexistent_user(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    admin_token = make_token("admin", "adminpass")

    response = client.get(
        "/users/999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ユーザーが見つかりませんでした"


"""
===結合テストNo.5===
user_id に整数以外の値を指定した場合、HTTP 422 が返却されること
"""
def test_get_user_endpoint_005_invalid_user_id(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.get(
        "/users/abc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
