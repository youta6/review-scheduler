"""
lambda x: x[0] の挙動テスト

groupby_test.py での使われ方：
    sorted_results = sorted(results, key=lambda x: x[0].review_id)
    for review_id, group in groupby(sorted_results, key=lambda x: x[0].review_id):

x はタプル (Review, ReviewManagement) の1行。
x[0] は Review オブジェクト、x[1] は ReviewManagement オブジェクト。
"""

from itertools import groupby

# --- シンプルなタプルのリストで挙動を確認 ---

# SQLAlchemyのjoin結果は (Review, ReviewManagement) のタプルが並ぶ。
# ここでは単純な (review_id, review_time) のタプルで代用する。
results = [
    ("Python基礎", 1),   # x[0]="Python基礎", x[1]=1
    ("Python基礎", 2),
    ("Python基礎", 3),
    ("FastAPI入門", 1),
    ("FastAPI入門", 2),
]

print("=== results の中身 ===")
for x in results:
    print(f"  x={x},  x[0]={x[0]},  x[1]={x[1]}")

print()

# lambda x: x[0] は「タプルの0番目の要素を取り出す」という意味
# sorted の key= に渡すと、0番目の要素を基準にソートする
sorted_results = sorted(results, key=lambda x: x[0])

print("=== sorted後（x[0] = review_item 基準） ===")
for x in sorted_results:
    print(f"  {x}")

print()

# groupby の key= に渡すと、0番目の要素が同じものをグループにまとめる
print("=== groupby後（x[0] が同じものをまとめる） ===")
for review_item, group in groupby(sorted_results, key=lambda x: x[0]):
    group_list = list(group)
    print(f"  review_item={review_item}  → {group_list}")

print()
print("=" * 50)
print("比較：lambda を使わずに def で書くパターン")
print("=" * 50)
print()

# lambda x: x[0] と全く同じ動作を def で書く
def get_first(x):
    return x[0]

sorted_def = sorted(results, key=get_first)

print("=== sorted後（def get_first 使用） ===")
for x in sorted_def:
    print(f"  {x}")

print()

print("=== groupby後（def get_first 使用） ===")
for key, group in groupby(sorted_def, key=get_first):
    group_list = list(group)
    print(f"  key={key}  -> {group_list}")


print()
print("=" * 50)
print("補足：sorted() が get_first を自動で呼んでいる確認")
print("=" * 50)
print()

# print を追加して、sorted() がいつ・何を渡して get_first を呼ぶか確認する
def get_first_with_log(x):
    print(f"  get_first_with_log が呼ばれた: x={x}")
    return x[0]

print("sorted() を実行すると get_first_with_log が各要素に対して自動で呼ばれる:")
sorted(results, key=get_first_with_log)
