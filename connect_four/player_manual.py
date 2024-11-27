#
# player_manual.py
#

from .board import Board
from .player import Player


class ManualPlayer(Player):
    """ Represents a Connect Four manual player.

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

    def get_next_move(self, board: Board) -> int:
        """ Repeatedly prompts the player to input a valid column index
            and returns the index.

            Parameters
            ----------
            board: :class:`Board`
                The Connect Four game board currently in use.

            Returns
            -------
            :class:`int`
                The index of the column chosen by the player.
        """
        self._increment_num_moves()
        col = input("Enter a column: ")
        while True:
            if col.isdigit() and board.can_add_to(int(col)):
                return int(col)
            col = input("Cannot play token in that column. Try again: ")
