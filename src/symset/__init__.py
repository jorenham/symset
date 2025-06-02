"""Symbolic sets."""

from typing import Final

from symset import _core

__all__ = ("EmptySet", "EmptySetType")


def __dir__() -> tuple[str, ...]:
    return __all__


EmptySet: Final = _core.EMPTY_SET
EmptySetType: Final = _core.EmptySetType
