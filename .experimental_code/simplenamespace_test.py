"""
動作確認：types.SimpleNamespace

参照元：app/tests/test_generate_token.py の
  _make_form_data(username, password)
    return SimpleNamespace(username=username, password=password)
が「何をやっているのか」を初学者向けに確かめる。

実行方法：
  uv run python .experimental_code/simplenamespace_test.py
"""
from types import SimpleNamespace


# ============================================================
# パート1：SimpleNamespace は「属性を持つだけの空っぽの箱」
# ============================================================
print("=" * 60)
print("パート1：SimpleNamespace とは何か")
print("=" * 60)

# SimpleNamespace(キーワード引数...) と書くと、
# 渡したキーワード引数がそのまま「属性（.username のようにドットでアクセスできるもの）」になる。
form_data = SimpleNamespace(username="login_user", password="secret123")

print(f"form_data            : {form_data}")
print(f"form_data.username   : {form_data.username}")
print(f"form_data.password   : {form_data.password}")
print()

# 辞書(dict)とよく比較される。違いは「. でアクセスできるか、[ ] でアクセスできるか」だけ。
form_data_dict = {"username": "login_user", "password": "secret123"}
print(f"dict版               : {form_data_dict}")
print(f"dict版アクセス         : {form_data_dict['username']}")
print("→ SimpleNamespace は dict と同じ情報を持てるが、 .username のように")
print("  クラスのインスタンスっぽくアクセスできるのが違い")
print()


# ============================================================
# パート2：なぜテストで SimpleNamespace を使うのか
# ============================================================
print("=" * 60)
print("パート2：なぜ本物のクラスではなく SimpleNamespace を使うのか")
print("=" * 60)


def extract_username(form_data) -> str:
    """generate_token の中で実際にやっていることに似せた処理
    （form_data.username という「属性アクセス」しかしていない点に注目）
    """
    return form_data.username


# 本物のクラスを使った場合
class RealFormData:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


real = RealFormData("login_user", "secret123")
print(f"本物のクラスでも       : {extract_username(real)}")

# SimpleNamespaceを使った場合
fake = SimpleNamespace(username="login_user", password="secret123")
print(f"SimpleNamespace でも  : {extract_username(fake)}")

print()
print("→ extract_username（≒ generate_token）は .username が取れさえすればよく、")
print("  RealFormData のような本物のクラスである必要はない。")
print("  テストのためだけに本物のクラス（FastAPIのOAuth2PasswordRequestFormなど）を")
print("  正しい手順で組み立てるのは大変なので、")
print("  「必要な属性だけを持つ最小限の代用品」として SimpleNamespace を使っている。")
