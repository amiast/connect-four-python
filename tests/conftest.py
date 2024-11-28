#
# conftest.py
#

import pytest

from connect_four.board import Board
from connect_four.player import Player
from connect_four.player_manual import ManualPlayer
from connect_four.player_auto import AutoPlayer
from connect_four.player_random import RandomPlayer

@pytest.fixture
def board():
    return Board(8, 9)

@pytest.fixture
def player():
    return Player("O")

@pytest.fixture
def manual_player():
    return ManualPlayer("O")

@pytest.fixture
def auto_player():
    return AutoPlayer("O", 3)

@pytest.fixture
def random_player():
    return RandomPlayer("O")
