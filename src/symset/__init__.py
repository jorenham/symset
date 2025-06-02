"""Symbolic sets."""

from collections.abc import Set as AbstractSet

from ._core import Nothing, NothingType

AbstractSet.register(NothingType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
del AbstractSet


__all__ = "Nothing", "NothingType"


def __dir__() -> tuple[str, ...]:
    return __all__
