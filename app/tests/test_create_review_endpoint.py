from datetime import datetime, timedelta, timezone

from app.main import create_review_endpoint
from app.schemas import ReviewCreateRequest

"""
==================================================
復習項目作成
テスト対象ファイル：main.py
テスト対象クラス：-
テスト対象メソッド：create_review_endpoint
テスト仕様書：テスト仕様書/単体テスト仕様書/サーバー処理/復習項目操作/復習項目作成_単体テスト仕様書.md
==================================================
"""

def _make_review_managements(mocker, today: datetime):
    return [
        mocker.MagicMock(review_time=review_time, review_date=today + timedelta(days=2 ** review_time - 1))
        for review_time in range(1, 6)
    ]

"""
===単体テストNo.1===
学習日がNoneの場合、現在日時を学習日として設定すること
"""
def test_create_review_endpoint_001_study_date_none(mocker, make_auth):
    fixed_now = datetime(2026, 6, 16, tzinfo=timezone.utc)
    mocker.patch("app.main.datetime").now.return_value = fixed_now
    auth = make_auth()
    new_review = mocker.MagicMock(review_item="review_item", study_date=fixed_now)
    create_review_mock = mocker.patch("app.main.create_review", return_value=new_review)
    mocker.patch("app.main.create_review_management", return_value=_make_review_managements(mocker, fixed_now))
    request = ReviewCreateRequest(review_item="review_item", study_date=None)

    create_review_endpoint(request, auth, db=mocker.MagicMock())

    assert create_review_mock.call_args.kwargs["study_date"] == fixed_now

"""
===単体テストNo.2===
学習日が空文字の場合、現在日時を学習日として設定すること

※このテストケースは削除。
  学習日の空文字チェックはpydanticではじかれるためデッドロジックとなっている。
"""
# def test_create_review_endpoint_002_study_date_empty(mocker, make_auth):
#     fixed_now = datetime(2026, 6, 16, tzinfo=timezone.utc)
#     mocker.patch("app.main.datetime").now.return_value = fixed_now
#     auth = make_auth()
#     new_review = mocker.MagicMock(review_item="review_item", study_date=fixed_now)
#     create_review_mock = mocker.patch("app.main.create_review", return_value=new_review)
#     mocker.patch("app.main.create_review_management", return_value=_make_review_managements(mocker, fixed_now))
#     # study_date=""はdatetime型と矛盾するため、model_constructで検証を回避する
#     request = ReviewCreateRequest.model_construct(review_item="review_item", description=None, study_date="")

#     create_review_endpoint(request, auth, db=mocker.MagicMock())

#     assert create_review_mock.call_args.kwargs["study_date"] == fixed_now

"""
===単体テストNo.3===
学習日が指定されている場合、指定の学習日を設定すること
"""
def test_create_review_endpoint_003_study_date_specified(mocker, make_auth):
    specified_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    auth = make_auth()
    new_review = mocker.MagicMock(review_item="review_item", study_date=specified_date)
    create_review_mock = mocker.patch("app.main.create_review", return_value=new_review)
    mocker.patch(
        "app.main.create_review_management",
        return_value=_make_review_managements(mocker, datetime.now(timezone.utc)),
    )
    request = ReviewCreateRequest(review_item="review_item", study_date=specified_date)

    create_review_endpoint(request, auth, db=mocker.MagicMock())

    assert create_review_mock.call_args.kwargs["study_date"] == specified_date

"""
===単体テストNo.4===
復習回n（1〜5）に対して復習予定日がtoday+2^n-1日で算出されること
"""
def test_create_review_endpoint_004_review_date_calculation(mocker, make_auth):
    fixed_now = datetime(2026, 6, 16, tzinfo=timezone.utc)
    mocker.patch("app.main.datetime").now.return_value = fixed_now
    auth = make_auth()
    new_review = mocker.MagicMock(review_item="review_item", study_date=fixed_now)
    mocker.patch("app.main.create_review", return_value=new_review)
    create_review_management_mock = mocker.patch(
        "app.main.create_review_management",
        return_value=_make_review_managements(mocker, fixed_now),
    )
    request = ReviewCreateRequest(review_item="review_item", study_date=None)

    create_review_endpoint(request, auth, db=mocker.MagicMock())

    expected_dates = [fixed_now + timedelta(days=2 ** n - 1) for n in range(1, 6)]
    assert create_review_management_mock.call_args.kwargs["review_date_list"] == expected_dates

"""
===単体テストNo.5===
正常なリクエストでReviewCreateResponseが返ること
"""
def test_create_review_endpoint_005_response_shape(mocker, make_auth):
    fixed_now = datetime(2026, 6, 16, tzinfo=timezone.utc)
    mocker.patch("app.main.datetime").now.return_value = fixed_now
    auth = make_auth()
    new_review = mocker.MagicMock(review_item="review_item", study_date=fixed_now)
    mocker.patch("app.main.create_review", return_value=new_review)
    mocker.patch(
        "app.main.create_review_management",
        return_value=_make_review_managements(mocker, fixed_now),
    )
    request = ReviewCreateRequest(review_item="review_item", study_date=None)

    response = create_review_endpoint(request, auth, db=mocker.MagicMock())

    assert len(response.review_schedule_list) == 5
