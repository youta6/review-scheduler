"""
==================================================
トークン発行
テスト対象ファイル：auth.py
テスト対象クラス：-
テスト対象メソッド：generate_token
テスト仕様書：test_specification/integration_test_specification/認証・認可/トークン発行_結合テスト仕様書.md
==================================================
"""

"""
===結合テストNo.1===
登録済みユーザーの正しいユーザー名とパスワードでトークンを取得できること
"""
def test_generate_token_endpoint_001_valid_credentials(client):
    client.post("/users", json={"user_name": "testuser", "password": "testpass"})

    response = client.post("/token", data={"username": "testuser", "password": "testpass"})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


"""
===結合テストNo.2===
存在しないユーザー名で POST /token を実行した場合、HTTP 401 が返却されること
"""
def test_generate_token_endpoint_002_nonexistent_user(client):
    response = client.post("/token", data={"username": "noexist", "password": "testpass"})

    assert response.status_code == 401
    assert response.json()["detail"] == "ユーザー名かパスワードが間違っています。"


"""
===結合テストNo.3===
パスワードが不一致の場合、HTTP 401 が返却されること
"""
def test_generate_token_endpoint_003_wrong_password(client):
    client.post("/users", json={"user_name": "testuser", "password": "testpass"})

    response = client.post("/token", data={"username": "testuser", "password": "wrongpass"})

    assert response.status_code == 401
    assert response.json()["detail"] == "ユーザー名かパスワードが間違っています。"
