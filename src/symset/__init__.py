"""Symbolic sets."""

from collections.abc import Set as AbstractSet

from ._core import Empty, EmptyType, Universe, UniverseType

AbstractSet.register(EmptyType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
AbstractSet.register(UniverseType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
del AbstractSet


__all__ = "Empty", "EmptyType", "Universe", "UniverseType"


def __dir__() -> tuple[str, ...]:
    return __all__
