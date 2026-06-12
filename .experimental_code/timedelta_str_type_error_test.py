"""
指摘再現テスト：auth/トークン発行 指摘No.2

os.getenv() で取得した文字列をそのまま timedelta(minutes=...) に渡すと
TypeError が発生することを確認する。
"""
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# os.getenv() は常に str を返す（環境変数が設定されていなくてもデフォルト値は str）
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

print(f"ACCESS_TOKEN_EXPIRE_MINUTES の型:  {type(ACCESS_TOKEN_EXPIRE_MINUTES)}")
print(f"ACCESS_TOKEN_EXPIRE_MINUTES の値:  {ACCESS_TOKEN_EXPIRE_MINUTES!r}")
print()

print("=" * 60)
print("テスト1：str のまま timedelta に渡す（バグあり）")
print("=" * 60)

try:
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(f"[NG] エラーが発生しなかった: {delta}")
except TypeError as e:
    print(f"[OK] TypeError が発生した（バグ再現）: {e}")

print()
print("=" * 60)
print("テスト2：int() にキャストして渡す（修正後）")
print("=" * 60)

try:
    delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    print(f"[OK] エラーなく完了した: timedelta = {delta}")
except Exception as e:
    print(f"[NG] エラーが発生した: {type(e).__name__}: {e}")
