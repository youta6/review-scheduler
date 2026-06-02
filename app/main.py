import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app import schemas
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.database import get_db, create_tables
from app.auth import get_current_active_user
from app.schemas import(
    UserCreateRequest,
    UserCreateResponse,
    UserUpdateRequest,
    UserUpdateResponse,
)
from app.crud import(
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
    create_review,
    get_reviews,
    update_review,
    delete_review,
    create_review_management,
    update_review_management,
    delete_review_management,
)

app = FastAPI()

pwd_context = PasswordHash([BcryptHasher()])

# サーバー起動時にテーブル作成
create_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# ヘルスチェック
@app.get("/health-check", response_model=schemas.HealthCheck)
def health_check(db: Session = Depends(get_db)) -> schemas.HealthCheck:
    return schemas.HealthCheck(status="ok")

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: str | None = None):
#    return {"item_id": item_id, "q": q}

'''
===ユーザー作成===
設計書：review-scheduler\設計書\サーバー処理（main）\ユーザー操作\ユーザー作成.md
'''
@app.post("/users")
def create_user_endpoint(
    user_create_request: UserCreateRequest,
    db: Session = Depends(get_db)
) -> UserCreateResponse:
    # 1. 管理者確認
    load_dotenv()
    ADMIN_SECRET_KEY_NAME = os.getenv("ADMIN_SECRET_KEY_NAME")
    ADMIN_SECRET_KEY_PASSWORD = os.getenv("ADMIN_SECRET_KEY_PASSWORD")
    admin_flag = False
    if user_create_request.user_name == ADMIN_SECRET_KEY_NAME and user_create_request.password == ADMIN_SECRET_KEY_PASSWORD:
        admin_flag = True

    try:
        # 2. ユーザー登録
        # 2.(1) メソッド呼び出し
        user = create_user(
            db,
            username=user_create_request.user_name,
            hashed_password=pwd_context.hash(user_create_request.password),
            admin_flag=admin_flag
        )

        # 3. 返り値を設定
        return UserCreateResponse(
            user_name=user.user_name,
            user_kind="管理者" if admin_flag else "一般",
            created_at=user.created_at
        )
    
    # 2.(2) 例外処理
    except Exception:
        raise HTTPException(status_code=409, detail="入力したユーザー名は既に登録されています")

'''
===ユーザー情報更新===
設計書：review-scheduler\設計書\サーバー処理（main）\ユーザー操作\ユーザー情報更新.md
'''
@app.put("/users/{user_id}")
def update_user_endpoint(
    user_update_request: UserUpdateRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
)-> UserUpdateResponse:
    # 1. 入力値チェック
    # 1.(1) 入力値．変更後ユーザー名、入力値．変更後パスワードがともに未入力の場合、
    # ログインユーザー検証．レスポンスを基に返り値を設定
    if user_update_request.user_name_after is None\
        and user_update_request.password_after is None:
        # 4. 返り値を設定
        return UserUpdateResponse(
            user_name=auth.user_name,
            updated_at=auth.updated_at
        )
    
    # 2. 更新対象ユーザー設定
    # 2.(1) ログインユーザー検証結果と入力値により処理分岐
    if user_update_request.user_name_before is None\
            or user_update_request.user_name_before == auth.user_name:
            user_name_before = auth.user_name
            if user_update_request.user_name_before is None\
                and user_update_request.password_before is None:
                hashed_password_before = auth.hashed_password
            else:
                hashed_password_before = pwd_context.hash(user_update_request.password_before)
    else:
        if auth.admin_flag == True:
            user_name_before = user_update_request.user_name_before
            hashed_password_before = pwd_context.hash(user_update_request.password_before)
        else:
            # 2.(2) 例外処理
            raise HTTPException(status_code=401, detail="他者のユーザー情報は変更できません")
    if user_update_request.user_name_after is None:
        user_name_after = auth.user_name
    else:
        user_name_after = user_update_request.user_name_after
    if user_update_request.password_after is None:
        hashed_password_after = auth.hashed_password
    else:
        hashed_password_after = pwd_context.hash(user_update_request.password_after)
    
    # 3. ユーザー情報更新
    # 3.(1) メソッド呼び出し
    user = update_user(
        db,
        user_name_before=user_name_before,
        hashed_password_before=hashed_password_before,
        user_name_after=user_name_after,
        hashed_password_after=hashed_password_after
    )

    # 3.(2) 例外処理
    if user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    
    # 4. 返り値を設定
    return UserUpdateResponse(
        user_name=user.user_name,
        updated_at=user.updated_at
    )


# 全ユーザーを取得
@app.get("/users")
def read_users_endpoint(db: Session = Depends(get_db)):
    users = get_users(db)
    return [{"id": user.id, "username": user.username} for user in users]

# 特定のユーザーを取得
@app.get("/users/{user_id}")
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username}

# ユーザー削除
@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    # ユーザーを削除
    try:
        result = delete_user(db, user_id)
        if not result:
            # 見つからない場合はエラーを返す
            raise HTTPException(status_code=404, detail="User not found")
        # 見つかった場合は削除
        return "delete success"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 復習項目を作成
@app.post("/users/{user_id}/reviews")
def create_review_endpoint(
    user_id: int,
    review: str,
    description: str = None,
    db: Session = Depends(get_db)
    ):
    try:
        new_review = create_review(db, user_id=user_id, review=review, description=description)
        new_review_management = create_review_management(db, user_id=user_id, review_id=new_review.id)
        db.commit()
        db.refresh(new_review)
        db.refresh(new_review_management)
        return {"id": new_review.id, "review": new_review.review, "description": new_review.description}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 復習項目を取得
@app.get("/users/{user_id}/reviews")
def read_reviews_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        reviews = get_reviews(db, user_id=user_id)
        return [{"id": review.id, "review": review.review, "description": review.description} for review in reviews]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 復習項目を更新
@app.put("/users/{user_id}/reviews/{review_id}")
def update_review_endpoint(review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    try:
        updated_review = update_review(db, user_id=review.user_id, review_id=review.review_id, review=review.review, description=review.description)
        if updated_review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        if review.review_time is not None and review.done_flag is not None:
            updated_review_management = update_review_management(db, user_id=review.user_id, review_id=review.review_id, review_time=review.review_time, done_flag=review.done_flag)
        db.commit()
        db.refresh(updated_review)
        db.refresh(updated_review_management)
        if review.review_time is not None and review.done_flag is not None:
            return {"id": updated_review.id, "review": updated_review.review, "description": updated_review.description, "review_time": updated_review_management.review_time, "done_flag": updated_review_management.done_flag}
        else:
            return {"id": updated_review.id, "review": updated_review.review, "description": updated_review.description}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 復習項目を削除
@app.delete("/users/{user_id}/reviews/{review_id}")
def delete_review_endpoint(user_id: int, review_id: int, db: Session = Depends(get_db)):
    try:
        deleted_review = delete_review(db, user_id=user_id, review_id=review_id)
        deleted_review_managements = delete_review_management(db, user_id=user_id, review_id=review_id)
        if deleted_review is None and deleted_review_managements is None:
            raise HTTPException(status_code=404, detail="Review not found")
        if deleted_review is not None:
            db.delete(deleted_review)
        if deleted_review_managements is not None:
            for deleted_review_management in deleted_review_managements:
                db.delete(deleted_review_management)
        db.commit()
        # 削除されたレビューを返す
        return {"id": deleted_review.id, "review": deleted_review.review, "description": deleted_review.description}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))