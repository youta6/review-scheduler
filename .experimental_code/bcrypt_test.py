from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

"""
※※※BcryptはArgon2より安全性が低いため不採用※※※
"""


# パスワード
password = "ABCD"

# bcryptでハッシュ化
pwd_context = PasswordHash([BcryptHasher()])

hashed_password=pwd_context.hash(password)

print(hashed_password)  # $2b$12$z.naKl6my1frvLHWVwEpXuGpmmbFDrdebDtBcTi0Fk6it7qxAjeHi


# ログイン時の検証
if pwd_context.verify("ABCD", hashed_password):
    print("OK")  # OK
else:
    print("NG")




import bcrypt

# パスワードをバイト列に変換
password = b"ABCD"

# ソルトを生成し、bcryptでハッシュ化
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed)  # b'$2b$12$O.PqoHzeQkecYnz1qHXwg.GiM2qZ9nDSWHi4TLK9krG5O.USKvVuW'

# ログイン時の検証
if bcrypt.checkpw(b"ABCD", hashed):
    print("OK")  # OK
else:
    print("NG")