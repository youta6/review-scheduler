"""
==================================================
復習項目取得
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：get_reviews_endpoint
テスト仕様書：test_specification/integration_test_specification/復習項目操作/復習項目取得_結合テスト仕様書.md
==================================================
"""


def _create_review(client, token, review_item="テスト復習項目", description=None):
    body = {"review_item": review_item}
    if description is not None:
        body["description"] = description
    return client.post(
        "/users/1/reviews",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
    )


"""
===結合テストNo.1===
復習項目が存在する場合、HTTP 200 と ReviewGetResponse のリストが返却されること
"""
def test_get_reviews_endpoint_001_get_review_list(client, make_token):
    token = make_token("testuser", "testpass")
    _create_review(client, token, "Pythonの型ヒント", description="型ヒントの基礎")

    response = client.get(
        "/users/1/reviews",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    review = body[0]
    assert review["review_id"] == 1
    assert review["review_item"] == "Pythonの型ヒント"
    assert review["description"] == "型ヒントの基礎"
    assert review["study_date"] is not None
    assert isinstance(review["review_schedule_with_done_flag_list"], list)
    assert len(review["review_schedule_with_done_flag_list"]) == 5
    for schedule in review["review_schedule_with_done_flag_list"]:
        assert schedule["review_time"] in [1, 2, 3, 4, 5]
        assert schedule["review_date"] is not None
        assert schedule["done_status"] == "未済"


"""
===結合テストNo.2===
復習項目が存在しない場合、HTTP 404 が返却されること
"""
def test_get_reviews_endpoint_002_no_reviews(client, make_token):
    token = make_token("testuser", "testpass")

    response = client.get(
        "/users/1/reviews",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "復習項目が見つかりませんでした"}


"""
===結合テストNo.3===
異なる user_id を URL に指定しても認証ユーザー自身の復習項目のみ返却されること
"""
def test_get_reviews_endpoint_003_url_user_id_is_ignored(client, make_token):
    token = make_token("testuser", "testpass")
    user2_token = make_token("user2", "user2pass")
    _create_review(client, token, "testuser の復習項目")
    _create_review(client, user2_token, "user2 の復習項目")

    response = client.get(
        "/users/2/reviews",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    review_items = [r["review_item"] for r in body]
    assert "testuser の復習項目" in review_items
    assert "user2 の復習項目" not in review_items
