"""
==================================================
全ユーザー情報取得
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：get_all_user_endpoint
テスト仕様書：test_specification/integration_test_specification/ユーザー操作/全ユーザー情報取得_結合テスト仕様書.md
==================================================
"""


"""
===結合テストNo.1===
管理者が GET /users した場合、HTTP 200 と全登録ユーザーのリストが返却されること
"""
def test_get_all_user_endpoint_001_admin_gets_all(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    admin_token = make_token("admin", "adminpass")
    make_token("testuser", "testpass")

    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
    testuser = next(u for u in body if u["user_name"] == "testuser")
    assert testuser["user_id"] == 2
    assert testuser["user_name"] == "testuser"
    assert testuser["delete_flag"] == False
    assert testuser["user_kind"] == "一般"
    assert testuser["created_at"] is not None
    assert testuser["updated_at"] is not None


"""
===結合テストNo.2===
一般ユーザーが GET /users した場合、HTTP 200 と自分のみを含む1件のリストが返却されること
"""
def test_get_all_user_endpoint_002_regular_user_gets_self_only(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    make_token("admin", "adminpass")
    token = make_token("testuser", "testpass")

    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["user_id"] == 2
    assert body[0]["user_name"] == "testuser"
    assert body[0]["delete_flag"] == False
    assert body[0]["user_kind"] == "一般"
    assert body[0]["created_at"] is not None
    assert body[0]["updated_at"] is not None
