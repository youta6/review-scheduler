from sqlalchemy import func, select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.models import User, Review, ReviewManagement
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from itertools import groupby
from app.schemas import ReviewGetResponse, ReviewScheduleWithDoneFlag

# pwd_context = PasswordHash([BcryptHasher()])

"""
===ユーザー作成===
設計書：review-scheduler\設計書\CLUD\ユーザー操作\ユーザー作成.md
"""
def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    admin_flag: bool = False
) -> User:
    # 1. 現在日時取得
    today = datetime.now(timezone.utc)

    # 2. ユーザー情報登録
    # 2.(1) USERテーブルに登録
    new_user = User(
        username=username,
        hashed_password=hashed_password,
        admin_flag=admin_flag,
        created_at=today,
        updated_at=today
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. 返り値を設定
    return User(
        username=username,
        created_at=today
    )


"""
===ユーザー情報更新===
設計書：review-scheduler\設計書\CLUD\ユーザー操作\ユーザー情報更新.md
"""
def update_user(
    db: Session,
    user_name_before: str,
    hashed_password_before: str,
    user_name_after: str = None,
    hashed_password_after: str = None,
) -> User:
    # 1. 現在日時取得
    today = datetime.now(timezone.utc)

    # 2. ユーザー情報更新
    # 2. (1) USERテーブルを更新
    user = db.query(User).filter(
        User.user_name == user_name_before,
        User.hashed_password == hashed_password_before
    ).first()
    if not user:
        # 3. 返り値を設定
        return None  # ユーザーが見つからない場合はNoneを返す
    if user_name_after:
        user.user_name = user_name_after
    if hashed_password_after:
        user.hashed_password = hashed_password_after
    user.updated_at = today
    db.commit()
    db.refresh(user)

    # 3. 返り値を設定
    return User(
        user_name=user.user_name,
        updated_at=today
    )


"""
===ユーザー情報削除===
設計書：review-scheduler\設計書\CLUD\ユーザー操作\ユーザー情報削除.md
"""
def delete_user(db: Session, user_name: str, hashed_password: str) -> User:
    # 1. 現在日時取得
    today = datetime.now(timezone.utc)

    # 2. ユーザー情報削除
    # 2.(1) USERテーブルを更新
    user = db.query(User).filter(
        User.user_name == user_name,
        User.hashed_password == hashed_password
    ).first()
    if not user:
        return None  # ユーザーが見つからない場合はNoneを返す
    user.delete_flag = True
    user.updated_at = today
    db.commit()
    db.refresh(user)

    # 3. 返り値を設定
    return User(
        user_name=user.user_name,
        updated_at=today
    )


"""
===ユーザー情報取得===
設計書：review-scheduler\設計書\CLUD\ユーザー操作\ユーザー情報取得.md
"""
def get_user(db: Session, user_name: str) -> User:
    return db.query(User).filter(
        User.user_name == user_name,
        User.delete_flag == False
    ).first()


"""
===全ユーザー情報取得===
設計書：review-scheduler\設計書\CLUD\ユーザー操作\全ユーザー情報取得.md
"""
def get_users(db: Session) -> list[User]:
    # 1. 全ユーザー情報取得
    # 2. 返り値を設定
    return db.query(User).all()


"""
===復習情報作成===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習情報作成.md
"""
def create_review(
    db: Session,
    user_id: int,
    review_item: str,
    study_date: datetime,
    today: datetime,
    description: str = None
) -> Review:
    # 1. 復習ID採番
    # 1.(1) 復習項目ID最大値取得
    new_review_id = db.query(func.max(Review.id)).scalar() + 1 if db.query(Review).count() > 0 else 1

    # 2. 復習情報登録
    # 2.(1) REVIEWテーブルに登録
    new_review = Review(
        user_id=user_id,
        review_id=new_review_id,
        review=review_item,
        description=description,
        study_date=study_date,
        created_at=today,
        updated_at=today
    )

    # コミットとリフレッシュは呼び出し元で行う

    # 3. 返り値を設定
    return new_review



"""
===復習管理情報作成===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習管理情報作成.md
"""
def create_review_management(
    db: Session,
    user_id: int,
    review_id: int,
    review_time_list: list[int],
    review_date_list: list[datetime],
    today: datetime
) -> list[ReviewManagement]:
    # 1. 復習管理情報登録
    # 1.(1) REVIEW_MANAGEMENTテーブルに登録
    # ※メモ：sqlalchemy.coreを使うと高速化できるらしい
    new_review_managements = [ReviewManagement(
        user_id=user_id,
        review_id=review_id,
        review_time=review_time,
        review_date=review_date_list[review_time],
        done_flag=False,
        created_at=today,
        updated_at=today
    ) for review_time in review_time_list]

    # コミットとリフレッシュは呼び出し元で行う

    # 2. 返り値を設定
    return new_review_managements


"""
===復習情報更新===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習情報更新.md
"""
def update_review(
    db: Session,
    user_id: int,
    review_id: int,
    today: datetime,
    review_item: str = None,
    description: str = None,
) -> Review | None:
    # 1. 復習情報更新
    # 1.(1) REVIEWテーブルを更新
    review = db.query(Review).filter(
        Review.user_id == user_id,
        Review.review_id == review_id
    ).first()

    if not review:
        # 2. 返り値を設定
        return None # ユーザーが見つからない場合はNoneを返す
    
    # 1.(1) REVIEWテーブルを更新（つづき）
    if review:
        review.review_item = review_item
    if description:
        review.description = description
    review.updated_at = today

    # コミットとリフレッシュは呼び出し元で行う

    # 2. 返り値を設定
    return review


"""
===復習管理情報更新===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習管理情報更新.md
"""
def update_review_management(
    db: Session,
    user_id: int,
    review_id: int,
    review_time: int,
    done_flag: bool,
    today: datetime
) -> ReviewManagement | None:
    # 1. 復習管理情報更新
    # 1.(1) REVIEW_MANAGEMENTテーブルを更新
    review_management = db.query(ReviewManagement).filter(
        ReviewManagement.user_id == user_id,
        ReviewManagement.review_id == review_id,
        ReviewManagement.review_time == review_time
    ).first()

    if not review_management:
        # 2. 返り値を設定
        return None # ユーザーが見つからない場合はNoneを返す
    
    # 1.(1) REVIEW_MANAGEMENTテーブルを更新（つづき）
    review_management.done_flag = done_flag
    review_management.updated_at = today

    # コミットとリフレッシュは呼び出し元で行う

    # 2. 返り値を設定
    return review_management


"""
===復習管理情報一括更新===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習管理情報一括更新.md
"""
def update_all_review_management(
    db: Session,
    user_id: int,
    review_id: int,
    done_flag: bool,
    today: datetime
) -> list[ReviewManagement] | None:
    # 1. 復習管理情報更新
    # 1.(1) REVIEW_MANAGEMENTテーブルを更新
    review_managements = db.query(ReviewManagement).filter(
        ReviewManagement.user_id == user_id,
        ReviewManagement.review_id == review_id
    ).all()

    if not review_managements:
        # 2. 返り値を設定
        return None # ユーザーが見つからない場合はNoneを返す
    
    # 1.(1) REVIEW_MANAGEMENTテーブルを更新（つづき）
    for review_management in review_managements:
        review_management.done_flag = done_flag
        review_management.updated_at = today

    # コミットとリフレッシュは呼び出し元で行う

    # 2. 返り値を設定
    return review_managements


"""
===復習情報削除===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習情報削除.md
"""
def delete_review(
    db: Session,
    user_id: int,
    review_id: int
) -> int | None:
    # 1. 復習情報削除
    # 1.(1) REVIEWテーブルを更新
    count = db.query(Review).filter(
        Review.user_id == user_id,
        Review.review_id == review_id
    ).delete()

    # コミットは呼び出し元で行う

    # 2. 返り値を設定
    if count == 0:
        return None # 復習情報が見つからない場合はNoneを返す
    return count


"""
===復習管理情報削除===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習管理情報削除.md
"""
def delete_review_management(
    db: Session,
    user_id: int,
    review_id: int
) -> int | None:
    # 1. 復習管理情報削除
    # 1.(1) REVIEW_MANAGEMENTテーブルを更新
    count = db.query(ReviewManagement).filter(
        ReviewManagement.user_id == user_id,
        ReviewManagement.review_id == review_id
    ).delete()

    # コミットは呼び出し元で行う

    # 2. 返り値を設定
    if count == 0:
        return None # 復習管理情報が見つからない場合はNoneを返す
    return count


"""
===復習項目取得===
設計書：review-scheduler\設計書\CLUD\復習項目操作\復習項目取得.md
"""
def get_reviews(db: Session, user_id: int) -> list[ReviewGetResponse] | None:
    # 1. 復習項目取得
    # 1.(1) REVIEWテーブル、REVIEW_MANAGEMENTテーブルを結合して取得
    stmt = select(Review).join(
        ReviewManagement,
        (Review.user_id == ReviewManagement.user_id) &
        (Review.review_id == ReviewManagement.review_id)
    ).where(Review.user_id == user_id)
    results = db.execute(stmt).all()

    if not results:
        # 2. 返り値を設定
        return None # 取得できない場合はNoneを返す
    
    # ソートしてからグループ化
    sorted_results = sorted(results, key=lambda x: x[0].review_id)

    # 2. 返り値を設定
    response_list = []
    for _, group in groupby(sorted_results, key=lambda x: x[0].review_id):
        group_list = list(group)
        review = group_list[0][0]
        response_list.append(
            ReviewGetResponse(
                review_item=review.review_item,
                description=review.description,
                study_date=review.study_date,
                review_schedule_with_done_flag_list=
                [
                    ReviewScheduleWithDoneFlag(
                        review_time=row[1].review_time,
                        review_date=row[1].review_date,
                        done_status="済" if row[1].done_flag else "未済"
                    ) for row in group_list
                ]
            )
        )
    return response_list
