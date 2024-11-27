#
# test_player_random.py
#

from connect_four.player_random import RandomPlayer

def test_repr(random_player):
    assert repr(random_player) == "Player O (Random)"
    assert repr(RandomPlayer("X")) == "Player X (Random)"

def test_get_next_move(random_player, board):
    assert 0 <= random_player.get_next_move(board) < board.width
    assert random_player.num_moves == 1
    board._reset()

    board._add_tokens("0" * board.height)
    for _ in range(1000):
        col = random_player.get_next_move(board)
        assert 1 <= col < board.width
        board.remove_token(col)
    board._reset()

    board._add_tokens("".join( str(i)*board.height for i in range(board.width-1) ))
    for _ in range(1000):
        assert random_player.get_next_move(board) == board.width - 1
        board.remove_token(board.width - 1)
