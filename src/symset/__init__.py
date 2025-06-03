"""Symbolic sets."""

from collections.abc import Set as AbstractSet

from ._core import Empty, EmptyType

AbstractSet.register(EmptyType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
del AbstractSet


__all__ = "Empty", "EmptyType"


def __dir__() -> tuple[str, ...]:
    return __all__
