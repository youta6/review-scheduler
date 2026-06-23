"""
結合テスト conftest.py で発生した問題の再現と解決

【問題】
sqlite:///:memory: を使った結合テストで「no such table: users」エラーが発生した。
原因は、SQLite のインメモリ DB がコネクションごとに独立して作られるため、
「テーブルを作ったコネクション」と「テストリクエスト時のコネクション」が
別々のデータベースになってしまうことにある。

【補足：コネクションプールについて】
SQLAlchemy はコネクションプールという仕組みで、一度作ったコネクションを
使い回す（プールする）。

プールの種類（今回関係するもの）：
  QueuePool（デフォルト）
    コネクションをプールして再利用する。
    同一スレッド内で続けて connect() を呼ぶと、
    プールから同じ SQLite コネクションが返ることが多いため、
    テーブルが見える場合もある。
    ただし、テスト時は FastAPI が別スレッドでリクエストを処理するため、
    スレッドごとに新しい SQLite コネクションが作られ、
    別のインメモリ DB になってしまうことがある。

  NullPool
    コネクションをプールせず、使うたびに新しいコネクションを作って即破棄する。
    sqlite:///:memory: では、新しいコネクション = 新しい空の DB になるため、
    問題が確実に再現できる。

  StaticPool
    プール内に常に同一のコネクションを1つだけ保持し、全ての呼び出しで返す。
    sqlite:///:memory: では、全ての操作が同一の DB に対して行われるため、
    「テーブルを作った DB」と「テストリクエスト時の DB」が一致する。

【解決策】
conftest.py の create_engine に poolclass=StaticPool を追加する。
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import NullPool, StaticPool


class Base(DeclarativeBase):
    pass


class SampleTable(Base):
    __tablename__ = "sample"
    id: Mapped[int] = mapped_column(primary_key=True)


# ============================================================
# テスト1：NullPool（問題の再現）
#   NullPool はコネクションを再利用しないため、
#   connect() のたびに新しい SQLite コネクション（＝新しい空の DB）が作られる。
#   テーブルを作った DB と、次に接続した DB が別物になることを確認する。
# ============================================================

print("=" * 60)
print("テスト1：NullPool（問題の再現）")
print("=" * 60)

engine_null = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=NullPool,  # コネクションを再利用しない
)

# コネクション1：conn1 自身のコネクション上でテーブルを作成する
with engine_null.connect() as conn1:
    Base.metadata.create_all(bind=conn1)  # engine ではなく conn1 に直接作成
    result = conn1.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result]
    print(f"コネクション1 から見えるテーブル: {tables}")  # ['sample']

# コネクション2：NullPool なので新しいコネクション＝新しい空の DB
with engine_null.connect() as conn2:
    result = conn2.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result]
    print(f"コネクション2 から見えるテーブル: {tables}")  # [] ← テーブルが見えない！

print()

# ============================================================
# テスト2：StaticPool（解決策）
#   StaticPool は常に同一のコネクションを返すため、
#   全ての操作が同じインメモリ DB に対して行われる。
#   Python オブジェクトの ID は connect() ごとに異なるが、
#   内部の SQLite コネクションは同一のため、テーブルが共有される。
# ============================================================

print("=" * 60)
print("テスト2：StaticPool（解決策）")
print("=" * 60)

engine_static = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 常に同一の SQLite コネクションを再利用する
)

# コネクション1：conn1 自身のコネクション上でテーブルを作成する
with engine_static.connect() as conn1:
    Base.metadata.create_all(bind=conn1)  # engine ではなく conn1 に直接作成
    result = conn1.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result]
    print(f"コネクション1 から見えるテーブル: {tables}")  # ['sample']

# コネクション2：StaticPool なので内部は同じ SQLite コネクション
with engine_static.connect() as conn2:
    result = conn2.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result]
    print(f"コネクション2 から見えるテーブル: {tables}")  # ['sample'] ← 見える！
