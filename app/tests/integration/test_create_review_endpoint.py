"""
==================================================
復習項目作成
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：create_review_endpoint
テスト仕様書：test_specification/integration_test_specification/復習項目操作/復習項目作成_結合テスト仕様書.md
==================================================
"""


"""
===結合テストNo.1===
study_date 未指定で POST した場合、HTTP 200 と review_id・review_item・study_date・5件の review_schedule_list が返却されること
"""
def test_create_review_endpoint_001_create_without_study_date(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.post(
        "/users/1/reviews",
        json={"review_item": "Pythonの型ヒント"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["review_id"] is not None
    assert body["review_item"] == "Pythonの型ヒント"
    assert body["study_date"] is not None
    assert isinstance(body["review_schedule_list"], list)
    assert len(body["review_schedule_list"]) == 5
    for schedule in body["review_schedule_list"]:
        assert schedule["review_time"] in [1, 2, 3, 4, 5]
        assert schedule["review_date"] is not None


"""
===結合テストNo.2===
study_date を指定して POST した場合、HTTP 200 と指定した study_date が返却されること
"""
def test_create_review_endpoint_002_create_with_study_date(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.post(
        "/users/1/reviews",
        json={"review_item": "FastAPIのルーティング", "study_date": "2026-06-01T00:00:00"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["study_date"].startswith("2026-06-01T00:00:00")


"""
===結合テストNo.3===
description を指定して POST した場合、HTTP 200 が返却され、GET で description が取得できること
"""
def test_create_review_endpoint_003_create_with_description(client, make_token):
    token = make_token("testuser", "testpass")

    client.post(
        "/users/1/reviews",
        json={"review_item": "SQLAlchemy ORM", "description": "セッション管理の基礎"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/users/1/reviews",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    reviews = response.json()
    target = next((r for r in reviews if r["review_item"] == "SQLAlchemy ORM"), None)
    assert target is not None
    assert target["description"] == "セッション管理の基礎"


"""
===結合テストNo.4===
review_item が未入力の場合、HTTP 422 が返却されること
"""
def test_create_review_endpoint_004_missing_review_item(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.post(
        "/users/1/reviews",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


"""
===結合テストNo.5===
URL の user_id に他ユーザーの ID を指定しても、認証ユーザー自身の復習項目として作成されること
"""
def test_create_review_endpoint_005_url_user_id_is_ignored(client, make_token):
    token = make_token("testuser", "testpass")
    make_token("user2", "user2pass")

    response = client.post(
        "/users/2/reviews",
        json={"review_item": "URLパス確認テスト"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    review_id = response.json()["review_id"]

    get_response = client.get(
        "/users/1/reviews",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 200
    review_ids = [r["review_id"] for r in get_response.json()]
    assert review_id in review_ids
