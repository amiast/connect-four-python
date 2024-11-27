#
# player_random.py
#

import random

from .board import Board
from .player import Player


class RandomPlayer(Player):
    """ Represents a Connect Four player that places tokens randomly.

        Parameters
        ----------
        token: Literal[`'O'`, `'X'`]
            The token used by the player.
            Modifying this attribute after instantiation raises `AttributeError`.

        Attributes
        ----------
        num_moves: :class:`int`
            The number of moves taken by the player so far.
            Modifying this attribute after instantiation raises `AttributeError`.

        Raises
        ------
        `ValueError`
            The supplied `token` is neither `'O'` nor `'X'`.
    """

    def __repr__(self) -> str:
        return f"Player {self.token} (Random)"

    def get_next_move(self, board: Board):
        """ Returns a random index among the available columns.

            Parameters
            ----------
            board: :class:`Board`
                The Connect Four game board currently in use.

            Returns
            -------
            :class:`int`
                The index of the randomly chosen column.
        """
        self._increment_num_moves()
        return random.choice([i for i in range(board.width) if board.can_add_to(i)])
