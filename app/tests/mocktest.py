from unittest.mock import MagicMock

def test_magic_setitem():
    mock_obj = MagicMock()
    mock_obj.__setitem__.side_effect = lambda key, value: print(f"{key} set to {value}")

    # インデックス設定のテスト
    mock_obj['key'] = 'value'
    mock_obj.__setitem__.assert_called_once_with('key', 'value')

def test_magic_call():
    mock_func = MagicMock()
    mock_func.return_value = 'called value'

    # 関数呼び出しのテスト
    assert mock_func(10) == 'called value'
    mock_func.assert_called_once_with(10)