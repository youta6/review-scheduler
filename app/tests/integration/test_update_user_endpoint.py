"""
==================================================
ユーザー情報更新
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：update_user_endpoint
テスト仕様書：test_specification/integration_test_specification/ユーザー操作/ユーザー情報更新_結合テスト仕様書.md
==================================================
"""

"""
===結合テストNo.1===
自分のユーザー名を変更した場合、HTTP 200 と変更後のユーザー名が返却されること
"""
def test_update_user_endpoint_001_update_own_username(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.put(
        "/users/1",
        json={"user_name_after": "testuser_new"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "testuser_new"
    assert "updated_at" in body


"""
===結合テストNo.2===
自分のパスワードを変更した場合、HTTP 200 が返却され変更後のパスワードで POST /token が成功すること
"""
def test_update_user_endpoint_002_update_own_password(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.put(
        "/users/1",
        json={"password_after": "newpass123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["user_name"] == "testuser"
    assert "updated_at" in response.json()

    # 変更後のパスワードで POST /token が成功すること
    token_response = client.post("/token", data={"username": "testuser", "password": "newpass123"})
    assert token_response.status_code == 200


"""
===結合テストNo.3===
変更項目なし（空リクエスト）の場合、HTTP 200 と現在のユーザー名が返却されること
"""
def test_update_user_endpoint_003_no_changes(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.put(
        "/users/1",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "testuser"
    assert "updated_at" in body


"""
===結合テストNo.4===
管理者が他ユーザーのユーザー名を変更した場合、HTTP 200 と変更後のユーザー名が返却されること
"""
def test_update_user_endpoint_004_admin_updates_other_user(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    admin_token = make_token("admin", "adminpass")
    make_token("testuser", "testpass")

    response = client.put(
        "/users/1",
        json={"user_name_before": "testuser", "user_name_after": "testuser_renamed"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["user_name"] == "testuser_renamed"


"""
===結合テストNo.5===
一般ユーザーが他ユーザーを更新しようとした場合、HTTP 401 が返却されること
"""
def test_update_user_endpoint_005_regular_user_updates_other(client, make_token):
    make_token("testuser", "testpass")
    token2 = make_token("testuser2", "testpass2")

    response = client.put(
        "/users/1",
        json={"user_name_before": "testuser", "user_name_after": "testuser_new"},
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "他者のユーザー情報は変更できません"


"""
===結合テストNo.6===
存在しないユーザーを更新しようとした場合（管理者）、HTTP 404 が返却されること
"""
def test_update_user_endpoint_006_admin_updates_nonexistent_user(client, make_token, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    admin_token = make_token("admin", "adminpass")

    response = client.put(
        "/users/1",
        json={"user_name_before": "nonexistent", "user_name_after": "newname"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ユーザーが見つかりませんでした"


"""
===結合テストNo.7===
URL の user_id と異なるユーザーのトークンで更新した場合、認証ユーザー自身が更新対象となること
"""
def test_update_user_endpoint_007_url_user_id_is_ignored(client, make_token):
    token_testuser = make_token("testuser", "testpass")
    make_token("user2", "testpass2")

    response = client.put(
        "/users/2",
        json={"user_name_after": "testuser_updated"},
        headers={"Authorization": f"Bearer {token_testuser}"},
    )

    assert response.status_code == 200
    assert response.json()["user_name"] == "testuser_updated"
