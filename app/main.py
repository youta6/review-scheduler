from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.crud import create_user, get_user, get_users, update_user, delete_user, create_review, get_reviews, update_review, delete_review, create_review_management, update_review_management, delete_review_management
from app import schemas

app = FastAPI()

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

# ユーザー作成
@app.post("/users")
def create_user_endpoint(username: str, password: str, db: Session = Depends(get_db)):
    try:
        user = create_user(db, username=username, password=password)
        return {"id": user.id, "username": user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

# ユーザー情報更新
@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, username: str, password: str, db: Session = Depends(get_db)):
    try:
        user = update_user(db, user_id=user_id, username=username, password=password)
        if user is None:
            # 見つからない場合はエラーを返す
            raise HTTPException(status_code=404, detail="User not found")
        # 見つかった場合は、更新
        return {"id": user.id, "username": user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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