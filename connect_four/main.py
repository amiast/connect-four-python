#
# main.py
#

import sys
import argparse
import time
from typing import Callable, Literal, Sequence

from .board import Board
from .player import Player
from .player_manual import ManualPlayer
from .player_auto import AutoPlayer
from .player_random import RandomPlayer
from .validate import validate_dimension

def _connect_four(
        player_1: Player,
        player_2: Player,
        width: int,
        height: int,
    ) -> None:
    """ Hosts a game of Connect Four between the two :class:`Player`'s
        and prints to the console.

        Parameters
        ----------
        player_1: :class:`Player`
            The player that goes first (`'O'`).
        player_2: :class:`Player`
            The player that goes second (`'X'`).
        width: :class:`int`
            The width of the game board.
        height: :class:`int`
            The height of the game board.
    """
    print("Starting a game of Connect Four...\n")
    board = Board(width, height)
    print(board)
    print()
    while True:
        if _process_move(player_1, board):
            return
        if _process_move(player_2, board):
            return

def _process_move(player: Player, board: Board) -> bool:
    """ Processes the move made by `player` on the `board`
        and checks whether the game is over.

        Parameters
        ----------
        player: :class:`Player`
            The player making the move.
        board: :class:`Board`
            The Connect Four game board currently in use.

        Returns
        -------
        :class:`bool`
            Indicates whether the game is over
            when either player wins or the board is full.
    """
    print(f"{player}'s turn...\n")
    time_start = time.time()
    col = player.get_next_move(board)
    time_end = time.time()
    print(
        f"{ player } placed a token in column {col} "
        f"({ time_end - time_start:.3f} seconds).\n"
    )
    board.add_token(player.token, col)
    print(f"{board}\n")

    if board.connects(player.token, lazy=True):
        print(f"{player} won in {player.num_moves} moves!")
        return True

    if board.is_full():
        print("The board is full. Tie!")
        return True

    return False

def main() -> None:
    """ Parses arguments and hosts a game of Connect Four. """
    args = _parser()(sys.argv[1:])

    match args.p1:
        case "manual":
            player_1 = ManualPlayer("O")
        case "random":
            player_1 = RandomPlayer("O")
        case int() as depth:
            player_1 = AutoPlayer("O", depth)

    match args.p2:
        case "manual":
            player_2 = ManualPlayer("X")
        case "random":
            player_2 = RandomPlayer("X")
        case int() as depth:
            player_2 = AutoPlayer("X", depth)

    try:
        _connect_four(player_1, player_2, args.width, args.height)
    except KeyboardInterrupt:
        print("Game ended by user.")

def _parser() -> Callable[[Sequence[str] | None, argparse.Namespace], argparse.Namespace]:
    """ Returns a helper parser for the `main` function.

        Returns
        -------
        Callable[[Sequence[:class:`str`] | `None`, :class:`argparse.Namespace`], :class:`argparse.Namespace`]
            A parser for the `main` function.
    """
    parser = argparse.ArgumentParser(
        description="Starts a game of Connect Four between two players."
    )
    parser.add_argument(
        "--p1",
        default = "manual",
        type = _parse_player,
        help = "The game mode for player 1, either `manual`, `random` or the depth of an auto-player. (default: manual)",
    )
    parser.add_argument(
        "--p2",
        default = "5",
        type = _parse_player,
        help = "The game mode for player 2, either `manual`, `random` or the depth of an auto-player. (default: 5)",
    )
    parser.add_argument(
        "--width",
        default=7,
        type=_parse_dimension,
        help = "The number of columns. Must be at least 4. (default: 7)",
    )
    parser.add_argument(
        "--height",
        default=6,
        type=_parse_dimension,
        help = "The number of rows. Must be at least 4. (default: 6)",
    )
    return parser.parse_args

def _parse_player(value: str) -> Literal["manual", "random"] | int:
    """ Helper function for validating the player option.

        Parameters
        ----------
        value: :class:`str`
            This is either `"manual"`, `"random"`
            or a digit string representing the non-negative depth of an auto-player.

        Raises
        ------
        ValueError
            `value` does not represent a valid player option.

        Returns
        -------
        Literal[`"manual"`, `"random"`] | :class:`int`
            The corresponding player option.
    """
    if value in ("manual", "random"):
        return value
    if not value.isnumeric():
        raise ValueError("The value must be `manual`, `random` or a number.")
    return int(value)

def _parse_dimension(value: str) -> int:
    """ Helper function for validating the height and width of a board.

        Parameters
        ----------
        value: :class:`str`
            Represents an :class:`int` at least `4`.

        Raises
        ------
        ValueError
            `value` does not represent a number at least `4`.

        Returns
        -------
        :class:`int`
            The corresponding integer value.
    """
    if not value.isnumeric():
        raise ValueError("The value must be a number.")
    value = int(value)
    validate_dimension(value)
    return value
