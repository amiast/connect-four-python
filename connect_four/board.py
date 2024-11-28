#
# board.py
#

from typing import Literal

from .validate import validate_dimension, validate_token


class Board:
    """ A game board that manages the states of a Connect Four game.

        Supported operations
        --------------------
        `x == y`
            Checks if two boards are equivalent.
            The boards must have the same `width` and `height`,
            and they must represent identical token configurations.
        `x != y`
            Checks if two boards are not equivalent.

        Parameters
        ----------
        width: :class:`int`
            The number of columns in the Connect Four board.
            Modifying this attribute after instantiation raises `AttributeError`.
        height: :class:`int`
            The number of rows in the Connect Four board.
            Modifying this attribute after instantiation raises `AttributeError`.

        Raises
        ------
        `ValueError`
            Attribute `width` or `height` is set to less than 4.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._reset_private_attr()

    @property
    def width(self) -> int:
        """ :class:`int`: The number of columns in the board. """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if hasattr(self, "width"):
            raise AttributeError("Cannot modify attribute `width` after instantiation.")
        validate_dimension(value)
        self._width = value

    @property
    def height(self) -> int:
        """ :class:`int`: The number of rows in the board. """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        if hasattr(self, "height"):
            raise AttributeError("Cannot modify attribute `height` after instantiation.")
        validate_dimension(value)
        self._height = value

    def _reset_private_attr(self) -> None:
        """ Resets the board configuration in `_config`,
            the list of available rows in `_available_rows`,
            and their `_available_min` and `_filled_max`.
        """
        # Token configuration
        self._config = [[" "] * self.width for _ in range(self.height)]
        # List of available rows for adding tokens
        self._available_rows = [self.height - 1] * self.width
        # Minimum available row (near the top)
        self._available_min = self.height - 1
        # Maximum filled (unavailable) row (near the bottom)
        self._filled_max = self.height

    def __repr__(self) -> str:
        result = ""

        # Add tokens
        for row in range(self.height):
            result += "|" + "|".join(self._config[row]) + "|\n"

        # Draw a line at the bottom of the board
        result += "-" * (self.width * 2 + 1) + "\n"

        # Add indices
        result += " " + " ".join(str(col % 10) for col in range(self.width))

        return result

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Board)
            and self.width == other.width
            and self.height == other.height
            and all(
                self._config[i][j] == other._config[i][j]
                for i in range(self.height)
                for j in range(self.width)
            )
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def can_add_to(self, col: int) -> bool:
        """ Checks whether the board has a valid empty space in the specified `col`.

            Parameters
            ----------
            col: :class:`int`
                The index of the column where the token is added.

            Returns
            -------
            :class:`bool`
                Indicates whether the token can be added.
        """
        return (
            0 <= col < self.width
            and self._available_rows[col] >= 0
        )

    def add_token(self, token: Literal["O", "X"], col: int) -> None:
        """ Adds the specified `token` to the specified `col` to the board.

            Parameters
            ----------
            token: Literal[`'O'`, `'X'`]
                The token to be added.
            col: :class:`int`
                The index of the column where the token is added.
                This column cannot be full.

            Raises
            ------
            ValueError
                The `token` is incorrect, or the specified `col` cannot accept any token.
        """
        validate_token(token)
        if not self.can_add_to(col):
            raise ValueError("Cannot add token to the specified `col`.")

        self._config[self._available_rows[col]][col] = token
        self._available_rows[col] -= 1

        # Update min max
        if self._available_rows[col] < self._available_min:
            self._available_min = self._available_rows[col]
        self._filled_max = max(self._available_rows) + 1

    def is_full(self) -> bool:
        """ Checks whether the board is full of tokens.

            Returns
            -------
            :class:`bool`
                Indicates whether the board is full.
        """
        return all( row == -1 for row in self._available_rows )

    def remove_token(self, col) -> None:
        """ Removes the top token from the specified `col` in the board.

            Parameters
            ----------
            col: :class:`int`
                The index of the column containing the token to be removed.

            Raises
            ------
            ValueError
                `col` is an invalid index or is empty.
        """
        if col < 0 or col >= self.width:
            raise ValueError("The specified `col` is not a valid index.")

        if self._available_rows[col] == self.height - 1:
            raise ValueError("The specified `col` is empty.")

        self._config[self._available_rows[col] + 1][col] = " "
        self._available_rows[col] += 1

        # Update min max
        self._available_min = min(self._available_rows)
        if self._available_rows[col] + 1 > self._filled_max:
            self._filled_max = self._available_rows[col] + 1

    def connects(self, token: Literal["O", "X"], *, lazy: bool = False) -> bool:
        """ Checks whether the board contains four connected `token`'s.

            Parameters
            ----------
            token: Literal[`'O'`, `'X'`]
                The token for verification.
            lazy: :class:`bool`
                If `True`, only search regions near the top of the board,
                assuming the remaining parts have already been searched by an earlier call.
                Otherwise, search the entire board.

            Raises
            ------
            `TypeError`
                The `token` is invalid.

            Returns
            -------
            :class:`bool`
                Indicates whether the board contains four connected `token`'s.
        """
        validate_token(token)
        return (
            self._connects_horiz(token, lazy=lazy)
            or self._connects_vert(token, lazy=lazy)
            or self._connects_topleft(token, lazy=lazy)
            or self._connects_bottomleft(token, lazy=lazy)
        )

    def _connects_horiz(self, token: Literal["O", "X"], *, lazy: bool = False) -> bool:
        """ Returns whether the board has four connected HORIZONTAL `token`'s. """
        if lazy:
            start = self._available_min + 1
            stop = min(self._filled_max + 1, self.height)
        else:
            start = 0
            stop = self.height

        for row in range(start, stop):
            for col in range(self.width - 3):
                if (
                    token
                    == self._config[row][col]
                    == self._config[row][col + 1]
                    == self._config[row][col + 2]
                    == self._config[row][col + 3]
                ):
                    return True

        return False

    def _connects_vert(self, token: Literal["O", "X"], *, lazy: bool = False) -> bool:
        """ Returns whether the board has four connected VERTICAL `token`'s. """
        if lazy:
            start = self._available_min + 1
            stop = min(self._filled_max + 1, self.height - 3)
        else:
            start = 0
            stop = self.height - 3

        for row in range(start, stop):
            for col in range(self.width):
                if (
                    token
                    == self._config[row][col]
                    == self._config[row + 1][col]
                    == self._config[row + 2][col]
                    == self._config[row + 3][col]
                ):
                    return True

        return False

    def _connects_topleft(self, token: Literal["O", "X"], *, lazy: bool = False) -> bool:
        """ Returns whether the board has four connected TOP-LEFT-DIAGONAL `token`'s. """
        if lazy:
            start = self._available_min + 1
            stop = min(self._filled_max + 1, self.height - 3)
        else:
            start = 0
            stop = self.height - 3

        for row in range(start, stop):
            for col in range(self.width - 3):
                if (
                    token
                    == self._config[row][col]
                    == self._config[row + 1][col + 1]
                    == self._config[row + 2][col + 2]
                    == self._config[row + 3][col + 3]
                ):
                    return True

        return False

    def _connects_bottomleft(self, token: Literal["O", "X"], *, lazy: bool = False) -> bool:
        """ Returns whether the board has four connected BOTTOM-LEFT-DIAGONAL `token`'s. """
        if lazy:
            start = self._available_min + 1
            stop = min(self._filled_max + 1, self.height - 3)
        else:
            start = 0
            stop = self.height - 3

        for row in range(start, stop):
            for col in range(self.width - 3):
                if (
                    token
                    == self._config[row][col + 3]
                    == self._config[row + 1][col + 2]
                    == self._config[row + 2][col + 1]
                    == self._config[row + 3][col]
                ):
                    return True

        return False

    #
    # Debugging functions
    #

    def _add_tokens(self, indices: str) -> None:
        """ This function is for debugging purposes only.

            Adds `'O'` and `'X'` tokens repeatedly to the board,
            specified by the columns in digit string `indices`.

            Parameters
            ----------
            indices: :class:`str`
                A digit string of column indices.

            Raises
            ------
            `ValueError`
                `tokens` is not a digit string or contains invalid column indices.
        """
        if not indices.isdigit():
            raise ValueError(
                "Expected `tokens` to be a digit string, "
                f"instead found {indices}"
                )

        token = "O"
        for col in indices:
            self.add_token(token, int(col))
            token = "O" if token == "X" else "X"
