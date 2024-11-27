#
# test_board.py
#

import pytest
import re

from connect_four.board import Board

@pytest.fixture
def board():
    return Board(8, 9)

def test_init(board):
    # Test instantiation
    assert board.width == 8
    assert board.height == 9
    assert board.height == len(board._config)
    assert all( board.width == len(row) for row in board._config )

def test_setter_errors(board):
    # Test setter exceptions
    with pytest.raises(AttributeError):
        board.width = 8
    with pytest.raises(AttributeError):
        board.height += 1

def test_init_errors():
    # Test instantiation exceptions
    with pytest.raises(ValueError):
        Board(3, 10)
    with pytest.raises(ValueError):
        Board(12, 1)

def test_repr(board):
    pattern = r"^[01234567|\- \n]+$"
    assert re.match(pattern, repr(board))
    assert "O" not in repr(board)
    assert "X" not in repr(board)

    board.add_token("O", 0)
    pattern = r"^[01234567O|\- \n]+$"
    assert re.match(pattern, repr(board))
    assert "O" in repr(board)
    assert "X" not in repr(board)

    board.add_token("X", 0)
    pattern = r"^[01234567OX|\- \n]+$"
    assert re.match(pattern, repr(board))
    assert "O" in repr(board)
    assert "X" in repr(board)

def test_eq_ne(board):
    other_board = Board(4, 4)
    assert board != other_board

    other_board = Board(board.width, board.height)
    assert board == other_board

    indices = "0323210"
    board._add_tokens(indices)
    assert board != other_board

    other_board._add_tokens(indices)
    assert board == other_board

def test_can_add_to(board):
    for _ in range(board.height):
        assert board.can_add_to(0)
        board.add_token("O", 0)
    assert not board.can_add_to(board.height)

def test_add_token(board):
    board.add_token("O", 0)
    board.add_token("X", 0)
    board.add_token("O", 2)
    assert board._config[-1][0] == "O"
    assert board._config[-2][0] == "X"
    assert board._config[-1][2] == "O"

def test_add_token_errors(board):
    with pytest.raises(ValueError):
        board.add_token("M", 0)
    with pytest.raises(ValueError):
        board.add_token("O", -1)
    
    for _ in range(board.height):
        board.add_token("O", 0)
    with pytest.raises(ValueError):
        board.add_token("O", 0)

def test_is_full(board):
    for _ in range(board.height):
        for col in range(board.width):
            assert not board.is_full()
            board.add_token("O", col)
    assert board.is_full()

def test_remove_tokens(board):
    for _ in range(4):
        board.add_token("O", 0)
    for _ in range(5):
        board.remove_token(0)
    assert all( row[0] == " " for row in board._config )

    for _ in range(4):
        board.add_token("O", 0)
    for _ in range(3):
        board.remove_token(0)
    assert all( row[0] == " " for row in board._config[:-1] )
    assert board._config[-1][0] == "O"

def test_remove_tokens_errors(board):
    with pytest.raises(ValueError):
        board.remove_token(-1)
    with pytest.raises(ValueError):
        board.remove_token(board.width)

def test_connects(board):
    assert not board.connects("O")
    assert not board.connects("X")

def test_connects_horiz(board):
    board._add_tokens("52716443")
    assert not board.connects("O")
    assert board._connects_horiz("X")
    assert board.connects("X")
    board._reset()

    board._add_tokens("33445566")
    assert board._connects_horiz("O")
    assert board.connects("O")
    assert board._connects_horiz("X")
    assert board.connects("X")
    board._reset()

def test_connects_vert(board):
    board._add_tokens("334241424")
    assert board._connects_vert("O")
    assert board.connects("O")
    assert not board.connects("X")
    board._reset()

    board._add_tokens("56565656")
    assert board._connects_vert("O")
    assert board.connects("O")
    assert board._connects_vert("X")
    assert board.connects("X")
    board._reset()

def test_connects_topleft(board):
    board._add_tokens("76654454564")
    assert board._connects_topleft("O")
    assert board.connects("O")
    assert not board.connects("X")
    board._reset()

    board._add_tokens("54432332121121")
    assert board._connects_topleft("O")
    assert board.connects("O")
    assert board._connects_topleft("X")
    assert board.connects("X")
    board._reset()

def test_connects_bottomleft(board):
    board._add_tokens("2324555444563")
    assert board._connects_bottomleft("O")
    assert board.connects("O")
    assert not board.connects("X")
    board._reset()

    board._add_tokens("12234334545545")
    assert board._connects_bottomleft("O")
    assert board.connects("O")
    assert board._connects_bottomleft("X")
    assert board.connects("X")
    board._reset()

def test_reset(board):
    board._add_tokens("0011")
    board._reset()
    assert all( token == " " for row in board._config for token in row )

def test_add_tokens(board):
    board._add_tokens("0123")
    assert "O" == board._config[-1][0] == board._config[-1][2]
    assert "X" == board._config[-1][1] == board._config[-1][3]

    board._add_tokens("3210")
    assert "O" == board._config[-2][1] == board._config[-2][3]
    assert "X" == board._config[-2][0] == board._config[-2][2]

    board._add_tokens("233")
    assert board._connects_bottomleft("O")
    assert not board.connects("X")

    other_board = Board(board.width, board.height)
    other_board.add_token("O", 0)
    other_board.add_token("X", 1)
    other_board.add_token("O", 2)
    other_board.add_token("X", 3)
    other_board.add_token("O", 3)
    other_board.add_token("X", 2)
    other_board.add_token("O", 1)
    other_board.add_token("X", 0)
    other_board.add_token("O", 2)
    other_board.add_token("X", 3)
    other_board.add_token("O", 3)
    assert board == other_board

def test_add_tokens_errors(board):
    with pytest.raises(ValueError):
        board._add_tokens("-1")
    with pytest.raises(ValueError):
        board._add_tokens("9")
