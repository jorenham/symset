"""Symbolic sets."""
import typing

from symset import _core

__all__ = ("EmptySet", "EmptySetType")


def __dir__() -> tuple[str, ...]:
    return __all__


# register `EmptySetType` as a "subclass" of `collections.abc.Set`, so that
# `isinstance(EmptySet, Set) and issubclass(EmptySetType, Set)`.
typing.AbstractSet.register(_core.EmptySetType)  # pyright: ignore[reportAttributeAccessIssue, reportDeprecated, reportUnknownMemberType]


EmptySet: typing.Final = _core.EMPTY_SET
EmptySetType: typing.Final = _core.EmptySetType
del _core
del typing
