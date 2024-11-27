#
# test_player.py
#

import pytest

from connect_four.player import Player

def test_init(player):
    assert player.token == "O"
    assert player.num_moves == 0
    assert Player("X").token == "X"
    assert Player("X").num_moves == 0

def test_setter_errors(player):
    with pytest.raises(AttributeError):
        player.token = player.token
    with pytest.raises(AttributeError):
        player.num_moves += 1

def test_init_errors():
    with pytest.raises(ValueError):
        Player("F")

def test_repr(player):
    assert repr(player) == "Player O"
    assert repr(Player("X")) == "Player X"

def test_increment_num_moves(player):
    for i in range(1, 11):
        player._increment_num_moves()
        assert player.num_moves == i

def test_get_next_move_errors(player, board):
    with pytest.raises(NotImplementedError):
        player.get_next_move(board)
