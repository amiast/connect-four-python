#
# player.py
#

from typing import Literal

from .board import Board
from .validate import validate_token


class Player:
    """ Base class detailing common operations by a Connect Four player.

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

    def __init__(self, token: Literal["O", "X"]) -> None:
        self.token = token
        self.num_moves = 0

    @property
    def token(self) -> Literal["O", "X"]:
        """ Literal[`'O'`, `'X'`]: The token used by the player. """
        return self._token

    @token.setter
    def token(self, value: Literal["O", "X"]) -> None:
        if hasattr(self, "token"):
            raise AttributeError("Cannot modify attribute `token` after instantiation.")
        validate_token(value)
        self._token = value

    @property
    def num_moves(self) -> int:
        """ :class:`int`: The number of moves taken by the player. """
        return self._num_moves

    @num_moves.setter
    def num_moves(self, value: int) -> None:
        if hasattr(self, "num_moves"):
            raise AttributeError("`num_moves` can only be incremented via `_increment_move()`.")
        self._num_moves = value

    def __repr__(self) -> str:
        return f'Player {self.token}'

    def _increment_num_moves(self) -> None:
        """ Increments the player's number of moves by `1`. """
        self._num_moves += 1

    def get_next_move(self, board: Board) -> int:
        """ Returns the player's next move on the board.

            Parameters
            ----------
            board: :class:`Board`
                The Connect Four game board currently in use.

            Returns
            -------
            :class:`int`
                The index of the column chosen by the player.
        """
        raise NotImplementedError
