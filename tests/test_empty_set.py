# pyright: reportUnknownVariableType=false

from collections.abc import Set as AbstractSet
from typing import Final, Never

import pytest
from hypothesis import given, strategies as st

from symset import EmptySet, EmptySetType

_EMPTY_BUILTIN_SET: Final[set[Never]] = set()
_EMPTY_FROZENSET: Final[frozenset[Never]] = frozenset(())

_FALSY_NON_SET: Final[tuple[object, ...]] = None, False, 0, 0.0, "", b"", (), [], {}


def test_subclass_abc() -> None:
    assert isinstance(EmptySet, AbstractSet)
    assert issubclass(EmptySetType, AbstractSet)


def test_cannot_construct() -> None:
    with pytest.raises(TypeError):
        _ = EmptySetType()


def test_no_dict() -> None:
    assert not hasattr(EmptySet, "__dict__")


def test_no_pyo3_internals() -> None:
    assert not hasattr(EmptySet, "__richcmp__")
    assert not hasattr(EmptySet, "__concat__")
    assert not hasattr(EmptySet, "__repeat__")
    assert not hasattr(EmptySet, "__traverse__")
    assert not hasattr(EmptySet, "__clear__")


def test_repr() -> None:
    assert repr(EmptySet) == "EmptySet"


def test_str() -> None:
    assert str(EmptySet) == "∅"


def test_bool() -> None:
    assert not EmptySet


def test_len() -> None:
    assert len(EmptySet) == 0


@given(st.none() | st.booleans() | st.integers() | st.floats() | st.text())
def test_contains(value: float | str | None) -> None:
    assert value not in EmptySet


def test_iter() -> None:
    assert sum(1 for _ in iter(EmptySet)) == 0


def test_hash() -> None:
    assert {EmptySet} == {_EMPTY_FROZENSET}
    assert hash(EmptySet) == hash(_EMPTY_FROZENSET)
    assert EmptySet._hash() == hash(_EMPTY_FROZENSET)  # noqa: SLF001


@pytest.mark.parametrize("other", [EmptySet, _EMPTY_FROZENSET, _EMPTY_BUILTIN_SET])
def test_eq(other: object) -> None:
    assert EmptySet == other


@pytest.mark.parametrize("other", [*_FALSY_NON_SET, {None}, frozenset({None})])
def test_ne(other: object) -> None:
    assert EmptySet != other


def test_lt() -> None:
    assert not EmptySet < EmptySet
    assert not EmptySet < _EMPTY_FROZENSET
    assert not EmptySet < _EMPTY_BUILTIN_SET

    assert EmptySet < {object()}
    assert EmptySet < frozenset({object()})

    with pytest.raises(TypeError):
        _ = EmptySet < ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet < []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet < {}  # pyright: ignore[reportOperatorIssue]


def test_le() -> None:
    assert EmptySet <= EmptySet
    assert EmptySet <= _EMPTY_FROZENSET
    assert EmptySet <= _EMPTY_BUILTIN_SET

    assert EmptySet <= {object()}
    assert EmptySet <= frozenset({object()})

    with pytest.raises(TypeError):
        _ = EmptySet <= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet <= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet <= {}  # pyright: ignore[reportOperatorIssue]


def test_ge() -> None:
    assert EmptySet >= EmptySet
    assert EmptySet >= _EMPTY_FROZENSET
    assert EmptySet >= _EMPTY_BUILTIN_SET

    assert not EmptySet >= {object()}
    assert not EmptySet >= frozenset({object()})

    with pytest.raises(TypeError):
        _ = EmptySet >= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet >= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet >= {}  # pyright: ignore[reportOperatorIssue]


def test_gt() -> None:
    assert not EmptySet > EmptySet
    assert not EmptySet > _EMPTY_FROZENSET
    assert not EmptySet > _EMPTY_BUILTIN_SET

    assert not EmptySet > {object()}
    assert not EmptySet > frozenset({object()})

    with pytest.raises(TypeError):
        _ = EmptySet > ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet > []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet > {}  # pyright: ignore[reportOperatorIssue]


def test_and() -> None:
    assert EmptySet & EmptySet is EmptySet
    assert EmptySet & _EMPTY_FROZENSET is EmptySet
    assert EmptySet & _EMPTY_BUILTIN_SET is EmptySet

    assert EmptySet & {object()} is EmptySet
    assert EmptySet & frozenset({object()}) is EmptySet

    with pytest.raises(TypeError):
        _ = EmptySet > ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet > []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = EmptySet > {}  # pyright: ignore[reportOperatorIssue]
