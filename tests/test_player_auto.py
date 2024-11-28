#
# test_player_auto.py
#

import pytest

from connect_four.board import Board
from connect_four.player_auto import Score, AutoPlayer

@pytest.mark.parametrize(("score", "type", "val"), (
    (Score("invalid"), "invalid", None),
    (Score("losing", 3), "losing", 3),
    (Score("neutral"), "neutral", None),
    (Score("winning", -1), "winning", -1),
))
def test_score_init(score, type, val):
    assert score.score_type is type
    assert score.score_val is val

def test_score_setter_errors():
    score = Score("neutral")
    with pytest.raises(AttributeError):
        score.score_type = "neutral"
    with pytest.raises(AttributeError):
        score.score_val = 1

    score = Score("losing", 1)
    with pytest.raises(AttributeError):
        score.score_type = "winning"
    with pytest.raises(AttributeError):
        score.score_val -= 1

def test_score_init_errors():
    with pytest.raises(ValueError):
        Score("definitely winning", 3)
    with pytest.raises(TypeError):
        Score("losing")

@pytest.mark.parametrize(("score",), (
    (Score("invalid"),),
    (Score("losing", 3),),
    (Score("neutral"),),
    (Score("winning", -1),),
))
def test_score_repr(score):
    assert eval(repr(score)) == score

@pytest.mark.parametrize(("score", "reversed_score"), (
    (Score("invalid"), Score("neutral")),
    (Score("losing", -1), Score("winning", 0)),
    (Score("neutral"), Score("neutral")),
    (Score("winning", 0), Score("losing", 0)),
))
def test_score_reverse(score, reversed_score):
    assert score._reverse() == reversed_score

@pytest.mark.parametrize(("score", "other", "result"), (
    (Score("invalid"), Score("invalid"), False),
    (Score("invalid"), Score("losing", 3), True),
    (Score("invalid"), Score("neutral"), True),
    (Score("invalid"), Score("winning", 1), True),

    (Score("losing", 5), Score("invalid"), False),
    (Score("losing", 5), Score("losing", 5), False),
    (Score("losing", 5), Score("losing", 10), True),
    (Score("losing", 5), Score("neutral"), True),
    (Score("losing", 5), Score("winning", 5), True),

    (Score("neutral"), Score("invalid"), False),
    (Score("neutral"), Score("losing", 1), False),
    (Score("neutral"), Score("neutral"), False),
    (Score("neutral"), Score("winning", 10), True),

    (Score("winning", 5), Score("invalid"), False),
    (Score("winning", 5), Score("losing", 5), False),
    (Score("winning", 5), Score("neutral"), False),
    (Score("winning", 5), Score("winning", 5), False),
    (Score("winning", 5), Score("winning", 1), True),
))
def test_score_lt(score, other, result):
    assert (score < other) is result

def test_score_comparisons():
    s = Score("invalid", 1)
    t = Score("invalid", -1)
    assert not s < t
    assert not s > t
    assert s <= t
    assert s >= t
    assert s == t
    assert not s != t

def test_score_comparison_errors():
    with pytest.raises(TypeError):
        Score("invalid", 0) < None
    with pytest.raises(TypeError):
        Score("invalid", 0) > None
    with pytest.raises(TypeError):
        Score("invalid", 0) <= None
    with pytest.raises(TypeError):
        Score("invalid", 0) >= None

def test_auto_player_init(auto_player):
    assert auto_player.depth == 3
    assert auto_player.score == Score("neutral")
    assert auto_player._opponent_token == "X"
    assert AutoPlayer("X", 2)._opponent_token == "O"

def test_auto_player_setter_errors(auto_player):
    with pytest.raises(AttributeError):
        auto_player.depth += 1
    with pytest.raises(AttributeError):
        auto_player.score = auto_player.score

def test_auto_player_init_errors():
    with pytest.raises(ValueError):
        AutoPlayer("O", -1)

def test_auto_player_repr(auto_player):
    assert repr(auto_player) == "Player O (Level 3)"

    assert repr(AutoPlayer("X", 0)) == "Player X (Level 0)"

    board = Board(4, 4)
    board._add_tokens("012301230011")
    assert auto_player.get_next_move(board) == 2
    assert repr(auto_player) == "Player O (Level 3 - winning in 1)"

def test_auto_player_get_scores_for():
    board = Board(7, 6)
    board._add_tokens("04122544114")

    assert AutoPlayer("O", 0)._get_scores_for(board) == [Score("neutral")] * 7
    assert AutoPlayer("O", 1)._get_scores_for(board) == [Score("neutral")] * 7
    assert AutoPlayer("O", 2)._get_scores_for(board) == [Score("losing", 0)] * 3 + [Score("neutral")] + [Score("losing", 0)] * 3
    assert AutoPlayer("X", 1)._get_scores_for(board) == [Score("neutral")] * 3 + [Score("winning", 0)] + [Score("neutral")] * 3
    assert AutoPlayer("O", 3)._get_scores_for(board) == [Score("losing", 0)] * 3 + [Score("winning", 1)] + [Score("losing", 0)] * 3
    assert AutoPlayer("X", 3)._get_scores_for(board) == [Score("neutral")] * 3 + [Score("winning", 0)] + [Score("neutral")] * 3
    assert AutoPlayer("X", 4)._get_scores_for(board) == [Score("losing", 1)] * 3 + [Score("winning", 0)] + [Score("losing", 1)] * 3

def test_auto_player_get_next_move(monkeypatch):
    board = Board(7, 6)
    board._add_tokens("04122544114")
    monkeypatch.setattr("random.choice", lambda lst: lst[0])

    assert AutoPlayer("O", 1).get_next_move(board) == 0
    assert AutoPlayer("O", 2).get_next_move(board) == 3
