import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
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
    UserDeleteRequest,
    UserDeleteResponse,
    UserGetRequest,
    UserGetResponse,
    ReviewCreateRequest,
    ReviewCreateResponse,
    ReviewSchedule,
    ReviewUpdateRequest,
    ReviewUpdateResponse,
    ReviewScheduleWithDoneFlag,
    ReviewDeleteRequest,
    ReviewDeleteResponse,
)
from app.models import ReviewManagement
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
    update_all_review_management,
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

'''
===ユーザー削除===
設計書：review-scheduler\設計書\サーバー処理（main）\ユーザー操作\ユーザー情報削除.md
'''
@app.delete("/users/{user_id}")
def delete_user_endpoint(
    user_delete_request: UserDeleteRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
)-> UserDeleteResponse:
    # 1. 削除対象ユーザー設定
    # 1.(1) ログインユーザー検証結果と入力値により処理分岐
    if user_delete_request.user_name is None\
        or user_delete_request.user_name == auth.user_name:
        user_name = auth.user_name
        hashed_password = auth.hashed_password
    else:
        if auth.admin_flag == True:
            user_name = user_delete_request.user_name
            hashed_password = pwd_context.hash(user_delete_request.password)
        else:
            # 1.(2) 例外処理
            raise HTTPException(status_code=401, detail="他者のユーザー情報は変更できません")

    # 2. ユーザー情報削除
    # 2.(1) メソッド呼び出し
    user = delete_user(db, user_name=user_name, hashed_password=hashed_password)

    # 2.(2) 例外処理
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    
    # 3. 返り値を設定
    return UserDeleteResponse(
        user_name=user.user_name,
        updated_at=user.updated_at
    )


'''
===ユーザー情報取得===
設計書：review-scheduler\設計書\サーバー処理（main）\ユーザー操作\ユーザー情報取得.md
'''
@app.get("/users/{user_id}")
def read_user_endpoint(
    user_get_request: UserGetRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
)-> UserGetResponse:
    # 1. ユーザー情報取得
    # 1.(1) ログインユーザー検証結果と入力値により処理分岐
    if user_get_request.user_name is None\
        or user_get_request.user_name == auth.user_name:
        # ログインユーザー検証．レスポンスを取得対象ユーザーとしてレスポンス
        return UserGetResponse(
            user_id=auth.user_id,
            user_name=auth.user_name,
            delete_flag=auth.delete_flag,
            user_kind="管理者" if auth.admin_flag else "一般",
            created_at=auth.updated_at,
            updated_at=auth.updated_at
        )
    else:
        if auth.admin_flag == True:
            user_name = user_get_request.user_name
        else:
            # 1.(2) 例外処理
            raise HTTPException(status_code=401, detail="他者のユーザー情報は取得できません")
    
    # 1.(3) ユーザー情報取得
    user = get_user(db, user_name=user_name)

    # 1.(4) 例外処理
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    
    # 2. 返り値を設定
    return UserGetResponse(
        user_id=user.id,
        user_name=user.user_name,
        delete_flag=user.delete_flag,
        user_kind="管理者" if user.admin_flag else "一般",
        created_at=user.created_at,
        updated_at=user.updated_at
    )

'''
===全ユーザー情報取得===
設計書：review-scheduler\設計書\サーバー処理（main）\ユーザー操作\全ユーザー情報取得.md
'''
@app.get("/users")
def get_all_user_endpoint(
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
) -> list[UserGetResponse]:
    # 1. ユーザー情報取得
    # 1.(1) ログインユーザー検証．管理者フラグ=Trueの場合、全ユーザーを取得
    if auth.admin_flag == True:
        # 1.(1)① メソッド呼び出し
        users = get_users(db)

        # 1.(1)② 例外処理
        if not users:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
        
        # 2. 返り値を設定
        return [
            UserGetResponse(
                user_id=user.id,
                user_name=user.user_name,
                delete_flag=user.delete_flag,
                user_kind="管理者" if user.admin_flag else "一般",
                created_at=user.created_at,
                updated_at=user.updated_at
            ) for user in users
        ]
    
    # 1.(2) ログインユーザー検証．管理者フラグ=Falseの場合、ログインユーザー検証．レスポンスを返り値に設定する
    else:
        
        # 2. 返り値を設定
        return [
            UserGetResponse(
                user_id=auth.user_id,
                user_name=auth.user_name,
                delete_flag=auth.delete_flag,
                user_kind="管理者" if auth.admin_flag else "一般",
                created_at=auth.created_at,
                updated_at=auth.updated_at
            )
        ]


'''
===復習項目作成===
設計書：review-scheduler\設計書\サーバー処理（main）\復習項目操作\復習項目作成.md
'''
@app.post("/users/{user_id}/reviews")
def create_review_endpoint(
    review_create_request: ReviewCreateRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
    ) -> ReviewCreateResponse:
    # 1. 現在日時取得
    today = datetime.now(timezone.utc)

    # 2. 学習日設定
    # 2.(1) 入力値．学習日が未設定の場合、学習日に入力値．現在日時を設定する
    if review_create_request.study_date is None\
        or review_create_request.study_date == "":
        study_date = today
    # 2.(2) 入力値．学習日が設定済みの場合、学習日に入力値．学習日を設定する
    else:
        study_date = review_create_request.study_date

    # 3. 復習情報作成
    # 3.(1) メソッド呼び出し
    new_review = create_review(
        db,
        user_id=auth.user_id,
        review_item=review_create_request.review_item,
        study_date=study_date,
        today=today,
        description=review_create_request.description
    )

    # 4. 復習予定日算出
    # 4.(1) 復習回をn（1～5）とし、5回分の復習予定日を算出する
    review_time_list = []
    review_date_list = []
    for review_time in range(1, 6):
        review_time_list.append(review_time)
        review_date_list.append(today + timedelta(days=2 ** review_time - 1))

    # 5. 復習管理情報作成
    # 5.(1) メソッド呼び出し
    new_review_managements = create_review_management(
        db,
        user_id=auth.user_id,
        review_id=new_review.review_id,
        review_time_list=review_time_list,
        review_date_list=review_date_list,
        today=today
    )

    db.add(new_review)
    db.add_all(new_review_managements)
    db.commit()
    db.refresh(new_review)
    for new_review_management in new_review_managements:
        db.refresh(new_review_management)

    # 6. 返り値を設定
    return ReviewCreateResponse(
        review_item=new_review.review_item,
        study_date=new_review.study_date,
        review_schedule_list=[
            ReviewSchedule(
                review_time=new_review_management.review_time,
                review_date=new_review_management.review_date
            )for new_review_management in new_review_managements
        ]
    )


"""
===復習項目を更新===
設計書：review-scheduler\設計書\サーバー処理（main）\復習項目操作\復習項目更新.md
"""
@app.patch("/users/{user_id}/reviews/{review_id}")
def update_review_endpoint(
    review_update_request: ReviewUpdateRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
)-> list[ReviewUpdateResponse]:
    # 1. ユーザー存在チェック
    if auth.delete_flag:
        raise HTTPException(status_code=403, detail="削除済みユーザーのため更新できません")
    
    # 2. 入力値チェック
    # 復習項目、復習内容詳細、復習回のいずれも設定されていない
    if (review_update_request.review_item is None or review_update_request.review_item == "")\
        and (review_update_request.description is None or review_update_request.description == "")\
        and review_update_request.review_time is None:
            raise HTTPException(status_code=422, detail="復習項目、復習内容詳細、復習回のいずれかに入力必須です。")
    # 復習回が設定され、対応済みフラグが未設定
    if review_update_request.review_time\
        and review_update_request.done_flag is None:
            raise HTTPException(status_code=422, detail="復習回を指定する場合、対応状況も指定してください。")

    # 3. 現在日時取得
    today = datetime.now(timezone.utc)

    # 4. 復習情報更新
    # 4.(1) 復習項目、復習内容詳細のいずれかが設定されている場合、メソッド呼び出し
    if (review_update_request.review_item is not None and review_update_request.review_item != "")\
        or (review_update_request.description is not None and review_update_request.description != ""):
        updated_review = update_review(
            db,
            user_id=auth.user_id,
            review_id=review_update_request.review_id,
            today=today,
            review_item=review_update_request.review_item,
            description=review_update_request.description
        )
        # 4.(2) 例外処理
        if updated_review is None:
            raise HTTPException(status_code=404, detail="対象の復習項目が見つかりませんでした")
        
    # 5. 復習管理情報更新
    # 5.(1) 復習回、対応済みフラグが設定されている場合、以下メソッド呼び出し
    updated_review_management_list: list[ReviewManagement] = []
    update_review_management_flag = False
    if review_update_request.review_time is not None\
        and review_update_request.done_flag is not None:
        updated_review_management_list = update_review_management(
            db,
            user_id=auth.user_id,
            review_id=review_update_request.review_id,
            review_time=review_update_request.review_time,
            done_flag=review_update_request.done_flag
        )
        update_review_management_flag = True

    # 5.(2) 復習回が未設定、対応済みフラグが設定されている場合、以下メソッド呼び出し
    update_all_review_management_flag = False
    if review_update_request.review_time is None\
        and review_update_request.done_flag is not None:
        updated_review_management_list = update_all_review_management(
            db,
            user_id=auth.user_id,
            review_id=review_update_request.review_id,
            done_flag=review_update_request.done_flag
        )
        update_all_review_management_flag = True
    
    # 5.(3) 例外処理
    if updated_review_management_list is None:
        raise HTTPException(status_code=404, detail="対象の復習項目が見つかりませんでした")

    db.commit()
    db.refresh(updated_review)
    if update_review_management_flag:
        db.refresh(updated_review_management)
    if update_all_review_management_flag:
        for updated_review_management in updated_review_management_list:
            db.refresh(updated_review_management)

    # 6. 返り値を設定
    return [
        ReviewUpdateResponse(
            review_item=updated_review.review_item,
            description=updated_review.description,
            review_schedule_with_done_flag_list=[
                ReviewScheduleWithDoneFlag(
                    review_time=updated_review_management.review_time,
                    review_date=updated_review_management.review_date,
                    done_status="済" if updated_review_management.done_flag else "未済"
                ) for updated_review_management in updated_review_management_list
            ]
        )
    ]


"""
===復習項目削除===
設計書：review-scheduler\設計書\サーバー処理（main）\復習項目操作\復習項目削除.md
"""
@app.delete("/users/{user_id}/reviews/{review_id}")
def delete_review_endpoint(
    review_delete_request: ReviewDeleteRequest,
    auth: Annotated[schemas.UserValidationResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
) -> ReviewDeleteResponse:
    # 1. ユーザー存在チェック
    if auth.delete_flag:
        raise HTTPException(status_code=403, detail="削除済みユーザーのため更新できません")

    # 2. 復習項目を削除
    # 2.(1) 復習情報削除メソッド呼び出し
    deleted_review_count = delete_review(
        db,
        user_id=auth.user_id,
        review_id=review_delete_request.review_id
    )

    # 2.(2) 復習管理情報削除メソッド呼び出し
    deleted_review_management_count = delete_review_management(
        db,
        user_id=auth.user_id,
        review_id=review_delete_request.review_id
    )

    # 2.(3) 例外処理
    if deleted_review_count is None and deleted_review_management_count is None:
        raise HTTPException(status_code=404, detail="復習項目は既に削除済みです")
    
    db.commit()

    # 3. 返り値を設定
    return ReviewDeleteResponse(status=True)


# 復習項目を取得
@app.get("/users/{user_id}/reviews")
def read_reviews_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        reviews = get_reviews(db, user_id=user_id)
        return [{"id": review.id, "review": review.review, "description": review.description} for review in reviews]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
