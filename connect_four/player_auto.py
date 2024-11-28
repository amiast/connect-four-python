#
# player_auto.py
#

import random
from typing import List, Literal

from .board import Board
from .player import Player


class Score:
    """ Represents the score given to playing a token in a column.

        This is a helper data type for :class:`AutoPlayer`'s method `get_next_move`.

        Supported operations
        --------------------
        `x < y`
            Checks if `x` represents a less favorable score than `y`.
        `x > y`
            Checks if `x` represents a more favorable score than `y`.
        `x <= y`
            Checks if `x` represents a score at most as favorable as `y`.
        `x >= y`
            Checks if `x` represents a score at least as favorable as `y`.
        `x == y`
            Checks if two instances represent the same score.
        `x != y`
            Checks if two instances do not represent the same score.

        Parameters
        ----------
        score_type: Literal[`"invalid"`, `"losing"`, `"neutral"`, `"winning"`]
            Indicates whether the column is winning, losing, neither or invalid.
            Modifying this attribute after instantiation raises `AttributeError`.
        score_val: :class:`int` | `None`
            If `score_type` is `"winning"` or `"losing"`,
            this indicates the number of moves before winning or losing AFTER making a move.
            Otherwise, this value should not be provided.
            Modifying this attribute after instantiation raises `AttributeError`.

        Raises
        ------
        `ValueError`
            `score_type` is not a valid option.
        `TypeError`
            `score_val` is not provided when `score_type` is set to `"losing"` or `"winning"`.
    """

    def __init__(
            self,
            score_type: Literal["invalid", "losing", "neutral", "winning"],
            score_val: int | None = None,
        ):
        self.score_type = score_type
        self.score_val = score_val

    @property
    def score_type(self) -> Literal["invalid", "losing", "neutral", "winning"]:
        """ Literal[`"invalid"`, `"losing"`, `"neutral"`, `"winning"`:
            Indicates whether the column is winning or losing.
        """
        return self._score_type

    @score_type.setter
    def score_type(self, value: Literal["invalid", "losing", "neutral", "winning"]) -> None:
        if hasattr(self, "score_type"):
            raise AttributeError("Cannot modify attribute `score_type` after instantiation.")
        if value not in ("invalid", "losing", "neutral", "winning"):
            raise ValueError(
                "Expected `score_type` to be either 'invalid', 'losing', 'neutral' or 'winning', "
                f"instead found '{ value }'"
            )
        self._score_type = value

    @property
    def score_val(self) -> int | None:
        """ :class:`int` | `None`: The number of moves before winning or losing after placing a token.

            This value is negative if the game is already over and the player cannot make another move.
        """
        return self._score_val

    @score_val.setter
    def score_val(self, value: int | None) -> None:
        if hasattr(self, "score_val"):
            raise AttributeError("Cannot modify attribute `score_val` after instantiation.")
        if self.score_type in ("losing", "winning") and not isinstance(value, int):
            raise TypeError(
                "Expected `score_type` to be type `int`, "
                f"instead found { type(value).__name__ }. "
                "Perhaps you forgot to provide it when instantiating a `Score` object?"
            )
        self._score_val = value

    def __repr__(self) -> str:
        match self.score_type:
            case "invalid" | "neutral":
                return f"Score('{ self.score_type }')"
            case _:
                return f"Score('{ self.score_type }', {self.score_val})"

    def __lt__(self, other: "Score") -> bool:
        if not isinstance(other, Score):
            raise TypeError(f"Cannot compare Score object with type { type(other).__name__ }")
        match self.score_type:
            case "invalid":
                return other.score_type != "invalid"
            case "losing":
                return (
                    other.score_type in ("neutral", "winning")
                    or other.score_type == "losing" and self.score_val < other.score_val
                )
            case "neutral":
                return other.score_type == "winning"
            case "winning":
                return other.score_type == "winning" and self.score_val > other.score_val

    def __gt__(self, other: "Score") -> bool:
        if not isinstance(other, Score):
            raise TypeError(f"Cannot compare Score object with type { type(other).__name__ }")
        return other.__lt__(self)

    def __ge__(self, other: "Score") -> bool:
        return not self.__lt__(other)

    def __le__(self, other: "Score") -> bool:
        if not isinstance(other, Score):
            raise TypeError(f"Cannot compare Score object with type { type(other).__name__ }")
        return other.__ge__(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Score)
            and self.__le__(other)
            and self.__ge__(other)
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _reverse(self) -> "Score":
        """ Returns the "reversed" score that would be evaluated
            by the opponent in their previous turn.

            This is a helper function for :class:`AutoPlayer`'s
            look-ahead method `_get_scores_for`.

            Returns
            -------
            :class:`Score`
                The score that the opponent would evaluate in their previous turn.
        """
        match self.score_type:
            case "invalid" | "neutral":
                return Score("neutral", 0)
            case "losing":
                return Score("winning", self.score_val + 1)
            case "winning":
                return Score("losing", self.score_val)


class AutoPlayer(Player):
    """ Represents a Connect Four manual player.

        Parameters
        ----------
        token: Literal[`'O'`, `'X'`]
            The token used by the auto-player.
            Modifying this attribute after instantiation raises `AttributeError`.
        depth: :class:`int`
            The non-negative number of steps to be computed by the auto-player.
            Modifying this attribute after instantiation raises `AttributeError`.

        Attributes
        ----------
        num_moves: :class:`int`
            The number of moves taken by the auto-player so far.
            Modifying this attribute after instantiation raises `AttributeError`.
        score: :class:`Score`
            Represents the score of the last move made by the auto-player.
            Modifying this attribute after instantiation raises `AttributeError`.

        Raises
        ------
        `ValueError`
            The supplied `token` is neither `'O'` nor `'X'`,
            or `depth` is non-positive.
    """

    def __init__(self, token: Literal["O", "X"], depth: int) -> None:
        if depth < 0:
            raise ValueError(
                "Expected `depth` to be non-negative, "
                f"instead found { depth }"
            )

        super().__init__(token)
        self.depth = depth
        self.score = Score("neutral")
        self._opponent_token = "O" if self.token == "X" else "X"

    @property
    def depth(self) -> int:
        """ :class:`int`: The number of steps to be computed by the auto-player. """
        return self._depth

    @depth.setter
    def depth(self, value: int) -> None:
        if hasattr(self, "depth"):
            raise AttributeError("Cannot modify attribute `depth` after instantiation.")
        self._depth = value

    @property
    def score(self) -> Score:
        """ :class:`Score`: Represents whether the auto-player is winning, losing or neither. """
        return self._score

    @score.setter
    def score(self, value: Score) -> None:
        if hasattr(self, "score"):
            raise AttributeError("`score` can only be modified via `_set_score()`.")
        self._score = value

    def __repr__(self) -> str:
        if (
            self.score.score_type in ("invalid", "neutral")
            or self.score.score_val <= 0
        ):
            return f"Player { self.token } (Level { self.depth })"
        return f"Player { self.token } (Level { self.depth } - { self.score.score_type } in { self.score.score_val })"

    def _set_score(self, score: Score) -> None:
        """ Modifies the auto-player's `score` attribute.

            Parameters
            ----------
            score: :class:`Score`
                The updated score instance.
        """
        self._score = score

    def _get_scores_for(self, board: Board) -> List[Score]:
        """ Evaluates the `board` and returns a list of :class:`Score`
            representing scores for each column.

            Parameters
            ----------
            board: :class:`Board`
                The Connect Four game board currently in use.

            Returns
            -------
            List[`Score`]
                A list of scores for every column.
        """
        scores = [Score("invalid")] * board.width

        for col in range(board.width):
            if not board.can_add_to(col):
                continue

            if board.connects(self._opponent_token, lazy=True):
                scores[col] = Score("losing", -1)
                continue

            if self.depth == 0:
                scores[col] = Score("neutral")
                continue

            # Look ahead
            board.add_token(self.token, col)
            opponent = AutoPlayer(self._opponent_token, self.depth - 1)
            opponent_score = max(opponent._get_scores_for(board))
            scores[col] = opponent_score._reverse()
            board.remove_token(col)

        return scores

    def get_next_move(self, board: Board) -> int:
        """ Evaluates the `board` and returns the best column to be played.

            Parameters
            ----------
            board: :class:`Board`
                The Connect Four game board currently in use.

            Returns
            -------
            :class:`int`
                The index of the column played by the auto-player.
        """
        self._increment_num_moves()
        scores = self._get_scores_for(board)
        max_score = max(scores)
        self._set_score(max_score)
        candidate_cols = [
            i for i in range(board.width)
            if scores[i] == max_score
        ]
        return random.choice(candidate_cols)
