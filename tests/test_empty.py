# pyright: reportUnknownVariableType=false

from collections.abc import Set as AbstractSet
from typing import Final, Never

import pytest
from hypothesis import given, strategies as st

from symset import Empty, EmptyType

_EMPTY_BUILTIN_SET: Final[set[Never]] = set()
_EMPTY_FROZENSET: Final[frozenset[Never]] = frozenset(())

_FALSY_NON_SET: Final[tuple[object, ...]] = None, False, 0, 0.0, "", b"", (), [], {}


def test_subclass_abc() -> None:
    assert isinstance(Empty, AbstractSet)
    assert issubclass(EmptyType, AbstractSet)


def test_cannot_construct() -> None:
    with pytest.raises(TypeError):
        _ = EmptyType()


def test_no_dict() -> None:
    assert not hasattr(Empty, "__dict__")


def test_no_pyo3_internals() -> None:
    assert not hasattr(Empty, "__richcmp__")
    assert not hasattr(Empty, "__concat__")
    assert not hasattr(Empty, "__repeat__")
    assert not hasattr(Empty, "__traverse__")
    assert not hasattr(Empty, "__clear__")


def test_repr() -> None:
    assert repr(Empty) == "Empty"


def test_str() -> None:
    assert str(Empty) == "∅"


def test_bool() -> None:
    assert not Empty


def test_len() -> None:
    assert len(Empty) == 0


@given(st.none() | st.booleans() | st.integers() | st.floats() | st.text())
def test_contains(value: float | str | None) -> None:
    assert value not in Empty


def test_iter() -> None:
    assert sum(1 for _ in iter(Empty)) == 0


def test_hash() -> None:
    assert {Empty} == {_EMPTY_FROZENSET}
    assert hash(Empty) == hash(_EMPTY_FROZENSET)
    assert Empty._hash() == hash(_EMPTY_FROZENSET)  # noqa: SLF001


@pytest.mark.parametrize("other", [Empty, _EMPTY_FROZENSET, _EMPTY_BUILTIN_SET])
def test_eq(other: object) -> None:
    assert Empty == other


@pytest.mark.parametrize("other", [*_FALSY_NON_SET, {None}, frozenset({None})])
def test_ne(other: object) -> None:
    assert Empty != other


def test_lt() -> None:
    assert not Empty < Empty
    assert not Empty < _EMPTY_FROZENSET
    assert not Empty < _EMPTY_BUILTIN_SET

    assert Empty < {object()}
    assert Empty < frozenset({object()})

    with pytest.raises(TypeError):
        _ = Empty < ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty < []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty < {}  # pyright: ignore[reportOperatorIssue]


def test_le() -> None:
    assert Empty <= Empty
    assert Empty <= _EMPTY_FROZENSET
    assert Empty <= _EMPTY_BUILTIN_SET

    assert Empty <= {object()}
    assert Empty <= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Empty <= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty <= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty <= {}  # pyright: ignore[reportOperatorIssue]


def test_ge() -> None:
    assert Empty >= Empty
    assert Empty >= _EMPTY_FROZENSET
    assert Empty >= _EMPTY_BUILTIN_SET

    assert not Empty >= {object()}
    assert not Empty >= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Empty >= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty >= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty >= {}  # pyright: ignore[reportOperatorIssue]


def test_gt() -> None:
    assert not Empty > Empty
    assert not Empty > _EMPTY_FROZENSET
    assert not Empty > _EMPTY_BUILTIN_SET

    assert not Empty > {object()}
    assert not Empty > frozenset({object()})

    with pytest.raises(TypeError):
        _ = Empty > ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty > []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty > {}  # pyright: ignore[reportOperatorIssue]


def test_and() -> None:
    assert Empty & Empty is Empty
    assert Empty & _EMPTY_FROZENSET is Empty
    assert Empty & _EMPTY_BUILTIN_SET is Empty

    assert Empty & {object()} is Empty
    assert Empty & frozenset({object()}) is Empty

    with pytest.raises(TypeError):
        _ = Empty & ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty & []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty & {}  # pyright: ignore[reportOperatorIssue]


def test_or() -> None:
    assert Empty | Empty is Empty
    assert Empty | _EMPTY_FROZENSET is Empty
    assert Empty | _EMPTY_BUILTIN_SET is Empty

    s1 = {object()}
    f1 = frozenset({object()})
    assert Empty | s1 is s1
    assert Empty | f1 is f1

    with pytest.raises(TypeError):
        _ = Empty | ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty | []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty | {}  # pyright: ignore[reportOperatorIssue]


def test_xor() -> None:
    assert Empty ^ Empty is Empty
    assert Empty ^ _EMPTY_FROZENSET is Empty
    assert Empty ^ _EMPTY_BUILTIN_SET is Empty

    s1 = {object()}
    f1 = frozenset({object()})
    assert Empty ^ s1 is s1
    assert Empty ^ f1 is f1

    with pytest.raises(TypeError):
        _ = Empty ^ ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty ^ []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty ^ {}  # pyright: ignore[reportOperatorIssue]


def test_sub() -> None:
    assert Empty - Empty is Empty
    assert Empty - _EMPTY_FROZENSET is Empty
    assert Empty - _EMPTY_BUILTIN_SET is Empty

    assert Empty - {object()} is Empty
    assert Empty - frozenset({object()}) is Empty

    with pytest.raises(TypeError):
        _ = Empty - ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty - []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Empty - {}  # pyright: ignore[reportOperatorIssue]


def test_rsub() -> None:
    assert Empty - Empty is Empty
    assert _EMPTY_FROZENSET - Empty is Empty
    assert _EMPTY_BUILTIN_SET - Empty is Empty

    s1 = {object()}
    f1 = frozenset({object()})
    assert s1 - Empty == s1
    assert f1 - Empty == f1

    with pytest.raises(TypeError):
        _ = () - Empty  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = [] - Empty  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = {} - Empty  # pyright: ignore[reportOperatorIssue]


def test_isdisjoint() -> None:
    assert Empty.isdisjoint(Empty)
    assert Empty.isdisjoint(_EMPTY_FROZENSET)
    assert Empty.isdisjoint(_EMPTY_BUILTIN_SET)

    assert Empty.isdisjoint({object()})
    assert Empty.isdisjoint(frozenset({object()}))

    with pytest.raises(TypeError):
        _ = Empty.isdisjoint(None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = Empty.isdisjoint(object())  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = Empty.isdisjoint(EmptyType)  # pyright: ignore[reportArgumentType]
