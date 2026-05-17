from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import User, Review, ReviewManagement
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

pwd_context = PasswordHash([BcryptHasher()])

"""
ユーザー作成
"""
def create_user(db: Session, username: str, password: str) -> User:
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

"""
全ユーザーを取得
"""
def get_users(db: Session):
    return db.query(User).all()

"""
特定のユーザーを取得
"""
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

"""
ユーザー情報更新
"""
def update_user(db: Session, user_id: int, username: str = None, password: str = None) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  # ユーザーが見つからない場合はNoneを返す
    if username:
        user.username = username
    if password:
        user.hashed_password = pwd_context.hash(password)
    db.commit()
    db.refresh(user)
    return user

"""
ユーザー情報削除
"""
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False  # ユーザーが見つからない場合はFalseを返す
    db.delete(user)
    db.commit()
    return True

"""
復習項目を作成
"""
# 復習項目を作成(REVIEWテーブルに追加)
def create_review(db: Session, user_id: int, review: str, description: str = None) -> Review:
    new_review = Review(user_id=user_id, review=review, description=description)
    db.add(new_review)
    # コミットとリフレッシュは呼び出し元で行う
    return new_review

# エビングハウスの忘却曲線を基にした復習日を計算する関数
def _calc_next_review_date(review_time: int) -> datetime:
    days = 2 ** review_time - 1
    return datetime.now() + timedelta(days=days)

# 復習項目を作成(REVIEW_MANAGEMENTテーブルに追加)
def create_review_management(
    db: Session, user_id: int,
    review_id: int,
) -> ReviewManagement:
    for i in range(1, 6):
        review_date = _calc_next_review_date(i)
        new_review_management = ReviewManagement(user_id=user_id, review_id=review_id, review_date=review_date, review_time=i)
        db.add(new_review_management)
    # コミットとリフレッシュは呼び出し元で行う
    return new_review_management


"""
復習項目を取得
"""
def get_reviews(db: Session, user_id: int) -> list[Review]:
    return db.query(Review).filter(Review.user_id == user_id).all()

"""
復習項目を更新
"""
# 復習項目を更新(REVIEWテーブルの更新)
def update_review(
    db: Session,
    user_id: int,
    review_id: int,
    review: str = None,
    description: str = None,
) -> Review | None:
    review = db.query(Review).filter(Review.user_id == user_id, Review.id == review_id).first()
    if not review:
        return None
    if review:
        review.review = review
    if description:
        review.description = description
    # コミットとリフレッシュは呼び出し元で行う
    return review

# 復習項目を更新(REVIEW_MANAGEMENTテーブルの更新)
def update_review_management(
    db: Session,
    user_id: int,
    review_id: int,
    review_time: int,
    done_flag: bool = None
) -> ReviewManagement | None:
    review_management = db.query(ReviewManagement).filter(ReviewManagement.user_id == user_id, ReviewManagement.review_id == review_id, ReviewManagement.review_time == review_time).first()
    if not review_management:
        return None
    if done_flag is not None:
        review_management.done_flag = done_flag
    # コミットとリフレッシュは呼び出し元で行う
    return review_management

"""
復習項目を削除
"""
# 復習項目を削除(REVIEWテーブルの削除)
def delete_review(db: Session, user_id: int, review_id: int) -> Review | None:
    review = db.query(Review).filter(Review.user_id == user_id, Review.id == review_id).first()
    if not review:
        return None
    # 削除は呼び出し元で行う
    return review

# 復習項目を削除(REVIEW_MANAGEMENTテーブルの削除)
def delete_review_management(db: Session, user_id: int, review_id: int) -> ReviewManagement | None:
    review_managements = db.query(ReviewManagement).filter(ReviewManagement.user_id == user_id, ReviewManagement.review_id == review_id).all()
    if not review_managements:
        return None
    # 削除は呼び出し元で行う
    return review_managements