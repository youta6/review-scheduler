import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.schemas import TokenResponse, UserValidationResponse
from app.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

password_hash = PasswordHash.recommended()

DUMMY_HASH = os.getenv("DUMMY_HASH")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# 入力されたパスワードとDBに保存されているハッシュ済みパスワードを比較する関数
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

# ユーザー情報をDBから取得する関数
def get_user_for_auth(db: Session, user_name: str) -> UserValidationResponse | None:
    user = db.query(UserValidationResponse).filter(UserValidationResponse.user_name == user_name).first()
    return user


"""
==================================================
認証・認可
- 有効ユーザー検証
- トークン発行

設計書：review-scheduler\設計書\認証・認可（auth）
==================================================
"""

"""
===有効ユーザー検証===
設計書：review-scheduler\設計書\認証・認可（auth）\有効ユーザー検証.md
"""
async def get_current_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
)-> UserValidationResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="資格情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Bearerトークンの検証
        # 1.(1) Bearerトークンデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 1.(2) トークンのユーザー名検証
        # 1.(2)① デコードされたトークン（ペイロード）から、ユーザー名を取得する
        user_name = payload.get("sub")
        # 1.(2)② 例外処理
        if user_name is None:
            raise credentials_exception
        token_data = UserValidationResponse(user_name=user_name)
    except InvalidTokenError:
        raise credentials_exception
    
    # 2. 登録ユーザー取得
    # 2.(1) ユーザー情報をDBから取得する
    user = get_user_for_auth(db, user_name=token_data.user_name)
    # 2.(2) 例外処理
    if user is None:
        raise credentials_exception

    # 3. 削除済みユーザー確認
    if user.delete_flag:
        # 3.(1) 例外処理
        raise HTTPException(status_code=400, detail="削除済みのユーザーです")
    return user

"""
===トークン発行===
設計書：review-scheduler\設計書\認証・認可（auth）\トークン発行.md
"""
@app.post("/token")
async def generate_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenResponse:
    # 1. ユーザー認証
    # 1.(1) 登録されているユーザーかどうかを確認する
    # 1.(1)① ユーザー情報をDBから取得する
    user = get_user_for_auth(db, form_data.username)

    # 1.(1)② 入力値．ユーザー名とUSER．ユーザー名を比較し、
    # ユーザーが登録されていない場合、ダミーのハッシュ済みパスワードで認証する。
    if not user:
        verify_password(form_data.password, DUMMY_HASH)
        user = False
    
    # 1.(1) ③ 入力されたパスワードのハッシュ結果が
    # 登録済みのハッシュ済みパスワードと一致することを確認する。
    if not verify_password(form_data.password, user.hashed_password):
        user = False
    
    # 1.(2) 登録されていないユーザーの場合、例外処理
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名かパスワードが間違っています。",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. アクセストークンの発行
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.user_name}.copy()
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # 2.(1) JWTのエンコードを行う。
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # 3. 返り値を設定
    return TokenResponse(access_token=encoded_jwt, token_type="bearer")
