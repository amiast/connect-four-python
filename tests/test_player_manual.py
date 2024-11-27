#
# test_player_manual.py
#

import pytest

@pytest.mark.timeout(1)
def test_get_next_move(board, manual_player, monkeypatch):
    # Input correct index
    monkeypatch.setattr("builtins.input", lambda _: "0")
    assert manual_player.get_next_move(board) == 0
    assert manual_player.num_moves == 1
    board._reset()

    # Input not in range
    inputs = iter(["10000", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert manual_player.get_next_move(board) == 1
    board._reset()

    # Input not digit
    inputs = iter(["one", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert manual_player.get_next_move(board) == 2
    board._reset()

    # Input column is full
    board._add_tokens("000000000")
    inputs = iter(["0", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert manual_player.get_next_move(board) == 3
    board._reset()
