#
# validate.py
#

from typing import Any

def validate_token(token: Any):
    """ Checks whether the `token` is either `'O'` or `'X'`.

        Parameters
        ----------
        token: Any
            This should be a :class:`str` representing the token, either `'O'` or `'X'`.

        Raises
        ------
        ValueError
            The `token` is neither `'O'` nor `'X'`.
    """
    if token not in ("O", "X"):
        raise ValueError(
            "Expected `token` to be either 'O' or 'X', "
            f"instead found '{token}'"
        )

def validate_dimension(value: Any) -> None:
    """ Checks whether the `value` is a valid dimension (an :class:`int` at least `4`).

        Parameters
        ----------
        value: Any
            This should be an :class:`int` no less than `4`.

        Raises
        ------
        TypeError
            The `value` is not an :class:`int`.
        ValueError
            The `value` is less than `4`.
    """
    if not isinstance(value, int):
        raise TypeError(
            "Expected dimension to have type `int`, "
            f"instead found type {type(value).__name__}"
        )
    if value < 4:
        raise ValueError(
            "Epected dimension to be at least 4, "
            f"instead found {value}"
        )
