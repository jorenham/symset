# pyright: reportUnknownVariableType=false

from collections.abc import Set as AbstractSet
from typing import Final, Never

import pytest
from hypothesis import given, strategies as st

from symset import Nothing, NothingType

_EMPTY_BUILTIN_SET: Final[set[Never]] = set()
_EMPTY_FROZENSET: Final[frozenset[Never]] = frozenset(())

_FALSY_NON_SET: Final[tuple[object, ...]] = None, False, 0, 0.0, "", b"", (), [], {}


def test_subclass_abc() -> None:
    assert isinstance(Nothing, AbstractSet)
    assert issubclass(NothingType, AbstractSet)


def test_cannot_construct() -> None:
    with pytest.raises(TypeError):
        _ = NothingType()


def test_no_dict() -> None:
    assert not hasattr(Nothing, "__dict__")


def test_no_pyo3_internals() -> None:
    assert not hasattr(Nothing, "__richcmp__")
    assert not hasattr(Nothing, "__concat__")
    assert not hasattr(Nothing, "__repeat__")
    assert not hasattr(Nothing, "__traverse__")
    assert not hasattr(Nothing, "__clear__")


def test_repr() -> None:
    assert repr(Nothing) == "Nothing"


def test_str() -> None:
    assert str(Nothing) == "∅"


def test_bool() -> None:
    assert not Nothing


def test_len() -> None:
    assert len(Nothing) == 0


@given(st.none() | st.booleans() | st.integers() | st.floats() | st.text())
def test_contains(value: float | str | None) -> None:
    assert value not in Nothing


def test_iter() -> None:
    assert sum(1 for _ in iter(Nothing)) == 0


def test_hash() -> None:
    assert {Nothing} == {_EMPTY_FROZENSET}
    assert hash(Nothing) == hash(_EMPTY_FROZENSET)
    assert Nothing._hash() == hash(_EMPTY_FROZENSET)  # noqa: SLF001


@pytest.mark.parametrize("other", [Nothing, _EMPTY_FROZENSET, _EMPTY_BUILTIN_SET])
def test_eq(other: object) -> None:
    assert Nothing == other


@pytest.mark.parametrize("other", [*_FALSY_NON_SET, {None}, frozenset({None})])
def test_ne(other: object) -> None:
    assert Nothing != other


def test_lt() -> None:
    assert not Nothing < Nothing
    assert not Nothing < _EMPTY_FROZENSET
    assert not Nothing < _EMPTY_BUILTIN_SET

    assert Nothing < {object()}
    assert Nothing < frozenset({object()})

    with pytest.raises(TypeError):
        _ = Nothing < ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing < []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing < {}  # pyright: ignore[reportOperatorIssue]


def test_le() -> None:
    assert Nothing <= Nothing
    assert Nothing <= _EMPTY_FROZENSET
    assert Nothing <= _EMPTY_BUILTIN_SET

    assert Nothing <= {object()}
    assert Nothing <= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Nothing <= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing <= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing <= {}  # pyright: ignore[reportOperatorIssue]


def test_ge() -> None:
    assert Nothing >= Nothing
    assert Nothing >= _EMPTY_FROZENSET
    assert Nothing >= _EMPTY_BUILTIN_SET

    assert not Nothing >= {object()}
    assert not Nothing >= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Nothing >= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing >= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing >= {}  # pyright: ignore[reportOperatorIssue]


def test_gt() -> None:
    assert not Nothing > Nothing
    assert not Nothing > _EMPTY_FROZENSET
    assert not Nothing > _EMPTY_BUILTIN_SET

    assert not Nothing > {object()}
    assert not Nothing > frozenset({object()})

    with pytest.raises(TypeError):
        _ = Nothing > ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing > []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing > {}  # pyright: ignore[reportOperatorIssue]


def test_and() -> None:
    assert Nothing & Nothing is Nothing
    assert Nothing & _EMPTY_FROZENSET is Nothing
    assert Nothing & _EMPTY_BUILTIN_SET is Nothing

    assert Nothing & {object()} is Nothing
    assert Nothing & frozenset({object()}) is Nothing

    with pytest.raises(TypeError):
        _ = Nothing & ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing & []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing & {}  # pyright: ignore[reportOperatorIssue]


def test_or() -> None:
    assert Nothing | Nothing is Nothing
    assert Nothing | _EMPTY_FROZENSET is Nothing
    assert Nothing | _EMPTY_BUILTIN_SET is Nothing

    s1 = {object()}
    f1 = frozenset({object()})
    assert Nothing | s1 is s1
    assert Nothing | f1 is f1

    with pytest.raises(TypeError):
        _ = Nothing | ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing | []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing | {}  # pyright: ignore[reportOperatorIssue]


def test_xor() -> None:
    assert Nothing ^ Nothing is Nothing
    assert Nothing ^ _EMPTY_FROZENSET is Nothing
    assert Nothing ^ _EMPTY_BUILTIN_SET is Nothing

    s1 = {object()}
    f1 = frozenset({object()})
    assert Nothing ^ s1 is s1
    assert Nothing ^ f1 is f1

    with pytest.raises(TypeError):
        _ = Nothing ^ ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing ^ []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing ^ {}  # pyright: ignore[reportOperatorIssue]


def test_sub() -> None:
    assert Nothing - Nothing is Nothing
    assert Nothing - _EMPTY_FROZENSET is Nothing
    assert Nothing - _EMPTY_BUILTIN_SET is Nothing

    assert Nothing - {object()} is Nothing
    assert Nothing - frozenset({object()}) is Nothing

    with pytest.raises(TypeError):
        _ = Nothing - ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing - []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Nothing - {}  # pyright: ignore[reportOperatorIssue]


def test_rsub() -> None:
    assert Nothing - Nothing is Nothing
    assert _EMPTY_FROZENSET - Nothing is Nothing
    assert _EMPTY_BUILTIN_SET - Nothing is Nothing

    s1 = {object()}
    f1 = frozenset({object()})
    assert s1 - Nothing == s1
    assert f1 - Nothing == f1

    with pytest.raises(TypeError):
        _ = () - Nothing  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = [] - Nothing  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = {} - Nothing  # pyright: ignore[reportOperatorIssue]


def test_isdisjoint() -> None:
    assert Nothing.isdisjoint(Nothing)
    assert Nothing.isdisjoint(_EMPTY_FROZENSET)
    assert Nothing.isdisjoint(_EMPTY_BUILTIN_SET)

    assert Nothing.isdisjoint({object()})
    assert Nothing.isdisjoint(frozenset({object()}))

    with pytest.raises(TypeError):
        _ = Nothing.isdisjoint(None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = Nothing.isdisjoint(object())  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = Nothing.isdisjoint(NothingType)  # pyright: ignore[reportArgumentType]
