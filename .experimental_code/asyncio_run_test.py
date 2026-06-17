"""
動作確認：asyncio.run()

参照元：app/tests/test_generate_token.py の
  _call_generate_token(form_data, db=None)
    return asyncio.run(generate_token(form_data, db))
が「何をやっているのか」を初学者向けに確かめる。

実行方法：
  uv run python .experimental_code/asyncio_run_test.py
"""
import asyncio


# ============================================================
# パート1：async def を「ただ呼ぶだけ」だと何が起きるか
# ============================================================
print("=" * 60)
print("パート1：async def を await/asyncio.run なしで呼ぶとどうなるか")
print("=" * 60)


async def say_hello(name: str) -> str:
    """async def で定義した関数（コルーチン関数）"""
    return f"こんにちは、{name}さん"


# ただ関数として呼んだだけでは、中の処理（return）は実行されない。
# 「コルーチンオブジェクト」という、まだ実行されていない予約票のようなものが返るだけ。
result = say_hello("太郎")

print(f"result の型      : {type(result)}")
print(f"result の値       : {result}")
print("→ 文字列ではなく <coroutine object ...> になっている")
print("→ つまり say_hello(...) を書いた時点では、関数の中身はまだ1行も実行されていない")
print()

# 後始末：実行せずに捨てると "coroutine was never awaited" という警告が出るので、
# ここで明示的に閉じておく（今回の説明用の後処理。本筋ではない）。
result.close()


# ============================================================
# パート2：asyncio.run() を使うと中身が実行される
# ============================================================
print("=" * 60)
print("パート2：asyncio.run() を使うと中身が実行される")
print("=" * 60)

# asyncio.run(コルーチン) は、
#   1. 新しいイベントループを用意する
#   2. そのコルーチンを最後まで実行する（内部の await もすべて解決する）
#   3. 戻り値を返す
#   4. イベントループを終了する
# という一連の処理を1行でやってくれる、
# 「同期コードの中から非同期関数を1回だけ実行したいとき」の標準的な書き方。
result = asyncio.run(say_hello("太郎"))

print(f"result の型      : {type(result)}")
print(f"result の値       : {result}")
print("→ 今度は本物の文字列が返ってきた")
print()

print("これが test_generate_token.py の _call_generate_token がやっていることそのもの：")
print('  return asyncio.run(generate_token(form_data, db))')
print("  generate_token は async def なので、asyncio.run で実行しないと結果が取れない")
