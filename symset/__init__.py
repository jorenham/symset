"""Symbolic sets."""

import sys
from typing import Final

from . import _core

__all__ = "Empty", "EmptyType", "Universe", "UniverseType"

if sys.version_info >= (3, 12):
    from typing import TypeAliasType

    EmptyType = TypeAliasType("EmptyType", _core.EmptyType)
    UniverseType = TypeAliasType("UniverseType", _core.UniverseType)
else:
    from typing import TypeAlias

    EmptyType: TypeAlias = _core.EmptyType
    UniverseType: TypeAlias = _core.UniverseType

Empty: Final = _core.Empty
Universe: Final = _core.Universe


def __dir__() -> tuple[str, ...]:
    return __all__
