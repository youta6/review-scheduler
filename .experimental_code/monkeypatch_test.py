"""
monkeypatch とは何か

【概要】
monkeypatch は pytest が提供するビルトインフィクスチャ（fixture）で、
テスト実行中だけ一時的に環境変数・関数・属性などを書き換えるためのもの。
テストが終わると自動で元の状態に戻してくれる。

【なぜ必要か】
テストコードで os.environ を直接書き換えると、テスト終了後も
環境変数が残り続け、後続のテストに影響が出てしまう。
monkeypatch を使えばそのリスクをなくし、テスト間の独立性を保てる。

【このファイルの構成】
  テスト1：os.environ を直接書き換えた場合（問題の再現）
           → テスト内で手動クリーンアップが必要なことを示す
  テスト2：monkeypatch.setenv を使った場合（解決策）
           → pytest が自動でクリーンアップすることを示す
  テスト3：後続テストで両方がクリーンアップ済みであることを確認する

【実行方法】
  uv run pytest .experimental_code/monkeypatch_test.py -v -s

【実行結果のポイント】
  テスト1 のコード量（手動クリーンアップあり）vs テスト2 のコード量（なし）を見比べる。
  テスト1 で例外が発生した場合、手動クリーンアップが実行されずに環境変数が残るリスクがある。
  monkeypatch はテストが例外で終了した場合でも確実にクリーンアップしてくれる。
"""

import os

# ============================================================
# テスト1：os.environ を直接書き換えた場合（問題の再現）
#
#   os.environ["KEY"] = "value" で直接書き換えると、
#   テストが終わっても環境変数が残り続ける。
#   後続テストへの影響を防ぐために手動クリーンアップが必要になる。
#   さらに、テスト内で例外が発生すると del が実行されず
#   環境変数が残ったままになってしまう（バグの温床）。
# ============================================================
def test_1_directly_set_env_var():
    print("\n--- テスト1 開始（os.environ 直接書き換え）---")
    print(f"  書き換え前: ADMIN_SECRET_KEY_NAME = {os.environ.get('ADMIN_SECRET_KEY_NAME', '（未設定）')}")

    os.environ["ADMIN_SECRET_KEY_NAME"] = "admin"  # 直接書き換え

    print(f"  書き換え後: ADMIN_SECRET_KEY_NAME = {os.environ.get('ADMIN_SECRET_KEY_NAME', '（未設定）')}")

    assert os.environ["ADMIN_SECRET_KEY_NAME"] == "admin"

    # ★ 手動クリーンアップが必要（monkeypatch なら不要）
    #    テスト内で例外が発生するとこの行は実行されず、環境変数が残り続ける
    del os.environ["ADMIN_SECRET_KEY_NAME"]
    print("  手動クリーンアップ実施（本来は monkeypatch に任せるべき）")
    print("--- テスト1 終了 ---")


# ============================================================
# テスト2：monkeypatch.setenv を使った場合（解決策）
#
#   monkeypatch.setenv("KEY", "value") で書き換えると、
#   テスト終了時に pytest が自動で元の状態（未設定）に戻してくれる。
#   テスト内で例外が発生した場合でも確実にクリーンアップされる。
# ============================================================
def test_2_monkeypatch_set_env_var(monkeypatch):
    print("\n--- テスト2 開始（monkeypatch 使用）---")
    print(f"  書き換え前: ADMIN_SECRET_KEY_NAME = {os.environ.get('ADMIN_SECRET_KEY_NAME', '（未設定）')}")

    monkeypatch.setenv("ADMIN_SECRET_KEY_NAME", "admin")  # monkeypatch で書き換え

    print(f"  書き換え後: ADMIN_SECRET_KEY_NAME = {os.environ.get('ADMIN_SECRET_KEY_NAME', '（未設定）')}")

    assert os.environ["ADMIN_SECRET_KEY_NAME"] == "admin"

    # ★ 手動クリーンアップ不要（pytest が自動でクリーンアップする）
    print("  手動クリーンアップ不要（pytest が自動で元の状態に戻す）")
    print("--- テスト2 終了 ---")


# ============================================================
# テスト3：後続テストで両方がクリーンアップ済みであることを確認する
#
#   テスト1：手動で del → 後続テストへの影響なし（手動クリーンアップの結果）
#   テスト2：monkeypatch が自動で復元 → 後続テストへの影響なし（自動クリーンアップの結果）
#   どちらも ADMIN_SECRET_KEY_NAME が残っていないことを確認する。
# ============================================================
def test_3_both_tests_cleaned_up():
    print("\n--- テスト3 開始（後続テストで状態を確認）---")
    value = os.environ.get("ADMIN_SECRET_KEY_NAME", "（未設定）")
    print(f"  ADMIN_SECRET_KEY_NAME = {value}")
    print("  → テスト1（手動クリーンアップ）もテスト2（monkeypatch）も後続テストに影響なし")
    print("--- テスト3 終了 ---")

    assert "ADMIN_SECRET_KEY_NAME" not in os.environ
