from datetime import datetime, timezone

from pwdlib import PasswordHash

from app.models import User

"""
==================================================
ユーザー作成
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：create_user_endpoint
テスト仕様書：テスト仕様書/結合テスト仕様書/ユーザー操作/ユーザー作成_結合テスト仕様書.md
==================================================
"""

password_hash = PasswordHash.recommended()

"""
===結合テストNo.1===
一般ユーザーとして登録した場合、user_kindが「一般」で返却されること
"""
def test_create_user_endpoint_001_create_general_user(client):
    response = client.post("/users", json={"user_name": "testuser", "password": "testpass"})

    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "testuser"
    assert body["user_kind"] == "一般"
    assert "created_at" in body


"""
===結合テストNo.2===
管理者のユーザー名とパスワードで登録した場合、user_kindが「管理者」で返却されること
"""
def test_create_user_endpoint_002_create_admin_user(client, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "adminuser")
    monkeypatch.setenv("ADMIN_SECRET_KEY_PASSWORD", "adminpass")

    response = client.post("/users", json={"user_name": "adminuser", "password": "adminpass"})

    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "adminuser"
    assert body["user_kind"] == "管理者"
    assert "created_at" in body


"""
===結合テストNo.3===
既に登録済みのユーザー名で登録した場合、HTTP 409が返却されること
"""
def test_create_user_endpoint_003_duplicate_username(client):
    client.post("/users", json={"user_name": "testuser", "password": "testpass"})

    response = client.post("/users", json={"user_name": "testuser", "password": "otherpass"})

    assert response.status_code == 409
    assert response.json()["detail"] == "入力したユーザー名は既に登録されています"


"""
===結合テストNo.4===
user_nameを指定しない場合、HTTP 422が返却されること
"""
def test_create_user_endpoint_004_missing_user_name(client):
    response = client.post("/users", json={"password": "testpass"})

    assert response.status_code == 422


"""
===結合テストNo.5===
passwordを指定しない場合、HTTP 422が返却されること
"""
def test_create_user_endpoint_005_missing_password(client):
    response = client.post("/users", json={"user_name": "testuser"})

    assert response.status_code == 422


"""
===結合テストNo.6===
登録ユーザー数が99件以上の場合、HTTP 409が返却されること
"""
def test_create_user_endpoint_006_user_limit_exceeded(client, db_session):
    now = datetime.now(timezone.utc)
    for i in range(99):
        user = User(
            user_name=f"user_{i:03d}",
            hashed_password=password_hash.hash("testpass"),
            admin_flag=False,
            created_at=now,
            updated_at=now,
        )
        db_session.add(user)
    db_session.commit()

    response = client.post("/users", json={"user_name": "newuser", "password": "testpass"})

    assert response.status_code == 409
    assert response.json()["detail"] == "登録可能ユーザーが上限に達しました。"
