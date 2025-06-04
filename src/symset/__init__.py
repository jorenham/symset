"""Symbolic sets."""

from collections.abc import Set as AbstractSet
from typing import Final

from ._core import EmptyType, UniverseType

AbstractSet.register(EmptyType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
AbstractSet.register(UniverseType)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
del AbstractSet


Empty: Final = EmptyType.get()
Universe: Final = UniverseType.get()


__all__ = "Empty", "Universe"


def __dir__() -> tuple[str, ...]:
    return __all__
