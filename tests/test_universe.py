# pyright: reportUnknownVariableType=false

from collections.abc import Set as AbstractSet
from typing import Final, Never

import pytest
from hypothesis import given, strategies as st

from symset import Empty, EmptyType, Universe, UniverseType

_EMPTY_BUILTIN_SET: Final[set[Never]] = set()
_EMPTY_FROZENSET: Final[frozenset[Never]] = frozenset(())

_FALSY_NON_SET: Final[tuple[object, ...]] = None, False, 0, 0.0, "", b"", (), [], {}


def test_subclass_abc() -> None:
    assert isinstance(Universe, AbstractSet)
    assert issubclass(type(Universe), AbstractSet)


def test_cannot_construct() -> None:
    with pytest.raises(TypeError):
        _ = type(Universe)()  # pyright: ignore[reportGeneralTypeIssues]


def test_no_dict() -> None:
    assert not hasattr(Universe, "__dict__")


def test_no_pyo3_internals() -> None:
    assert not hasattr(Universe, "__richcmp__")
    assert not hasattr(Universe, "__concat__")
    assert not hasattr(Universe, "__repeat__")
    assert not hasattr(Universe, "__traverse__")
    assert not hasattr(Universe, "__clear__")


def test_repr() -> None:
    assert repr(Universe) == "Universe"


def test_str() -> None:
    assert str(Universe) == "U"


def test_bool() -> None:
    assert Universe


def test_len() -> None:
    with pytest.raises(OverflowError):
        _ = len(Universe)


@given(st.none() | st.booleans() | st.integers() | st.floats() | st.text())
def test_contains_value(value: float | str | None) -> None:
    assert value in Universe


@pytest.mark.parametrize("value", [Empty, Universe])
def test_contains_special_set(value: EmptyType | UniverseType) -> None:
    assert value in Universe


def test_iter() -> None:
    with pytest.raises(OverflowError):
        _ = iter(Universe)


def test_hash() -> None:
    assert hash(Universe) == -hash(_EMPTY_FROZENSET) - 1


def test_eq() -> None:
    assert Universe is Universe


@pytest.mark.parametrize(
    "other", [*_FALSY_NON_SET, _EMPTY_FROZENSET, _EMPTY_BUILTIN_SET, Empty]
)
def test_ne(other: object) -> None:
    assert Universe != other


def test_lt() -> None:
    assert not Universe < Universe
    assert not Universe < Empty
    assert not Universe < _EMPTY_FROZENSET
    assert not Universe < _EMPTY_BUILTIN_SET

    assert not Universe < {object()}
    assert not Universe < frozenset({object()})

    with pytest.raises(TypeError):
        _ = Universe < ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe < []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe < {}  # pyright: ignore[reportOperatorIssue]


def test_le() -> None:
    assert Universe <= Universe
    assert not Universe <= Empty
    assert not Universe <= _EMPTY_FROZENSET
    assert not Universe <= _EMPTY_BUILTIN_SET
    assert not Universe <= {object()}
    assert not Universe <= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Universe <= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe <= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe <= {}  # pyright: ignore[reportOperatorIssue]


def test_ge() -> None:
    assert Universe >= Universe
    assert Universe >= Empty
    assert Universe >= _EMPTY_FROZENSET
    assert Universe >= _EMPTY_BUILTIN_SET
    assert Universe >= {object()}
    assert Universe >= frozenset({object()})

    with pytest.raises(TypeError):
        _ = Universe >= ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe >= []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe >= {}  # pyright: ignore[reportOperatorIssue]


def test_gt() -> None:
    assert not Universe > Universe
    assert Universe > Empty
    assert Universe > _EMPTY_FROZENSET
    assert Universe > _EMPTY_BUILTIN_SET
    assert Universe > {object()}
    assert Universe > frozenset({object()})

    with pytest.raises(TypeError):
        _ = Universe > ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe > []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe > {}  # pyright: ignore[reportOperatorIssue]


def test_and() -> None:
    assert Universe & Universe is Universe
    assert Universe & Empty is Empty
    assert Universe & _EMPTY_FROZENSET is Empty
    assert Universe & _EMPTY_BUILTIN_SET is Empty

    s1 = {object()}
    f1 = frozenset({object()})
    assert Universe & s1 is s1
    assert Universe & f1 is f1

    with pytest.raises(TypeError):
        _ = Universe & ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe & []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe & {}  # pyright: ignore[reportOperatorIssue]


def test_or() -> None:
    assert Universe | Universe is Universe
    assert Universe | Empty is Universe
    assert Universe | _EMPTY_FROZENSET is Universe
    assert Universe | _EMPTY_BUILTIN_SET is Universe

    s1 = {object()}
    f1 = frozenset({object()})
    assert Universe | s1 is Universe
    assert Universe | f1 is Universe

    with pytest.raises(TypeError):
        _ = Universe | ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe | []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe | {}  # pyright: ignore[reportOperatorIssue]


def test_xor() -> None:
    assert Universe ^ Universe is Empty
    assert Universe ^ Empty is Universe
    assert Universe ^ _EMPTY_FROZENSET is Universe
    assert Universe ^ _EMPTY_BUILTIN_SET is Universe

    # TODO: absolute complement
    with pytest.raises(NotImplementedError):
        _ = Universe ^ {object()}

    with pytest.raises(TypeError):
        _ = Universe ^ ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe ^ []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe ^ {}  # pyright: ignore[reportOperatorIssue]


def test_sub() -> None:
    assert Universe - Universe is Empty
    assert Universe - Empty is Universe
    assert Universe - _EMPTY_FROZENSET is Universe
    assert Universe - _EMPTY_BUILTIN_SET is Universe

    # TODO: absolute complement
    with pytest.raises(NotImplementedError):
        _ = Universe - {object()}

    with pytest.raises(TypeError):
        _ = Universe - ()  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe - []  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = Universe - {}  # pyright: ignore[reportOperatorIssue]


def test_rsub() -> None:
    assert _EMPTY_FROZENSET - Universe is Empty
    assert _EMPTY_BUILTIN_SET - Universe is Empty

    s1 = {object()}
    f1 = frozenset({object()})
    assert s1 - Universe is Empty
    assert f1 - Universe is Empty

    with pytest.raises(TypeError):
        _ = () - Universe  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = [] - Universe  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = {} - Universe  # pyright: ignore[reportOperatorIssue]


def test_isdisjoint() -> None:
    assert not Universe.isdisjoint(Universe)
    assert Universe.isdisjoint(Empty)
    assert Universe.isdisjoint(_EMPTY_FROZENSET)
    assert Universe.isdisjoint(_EMPTY_BUILTIN_SET)

    assert not Universe.isdisjoint({object()})
    assert not Universe.isdisjoint(frozenset({object()}))

    with pytest.raises(TypeError):
        _ = Universe.isdisjoint(None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = Universe.isdisjoint(object())  # pyright: ignore[reportArgumentType]


def test_complement() -> None:
    assert Universe.C is Empty, (Universe.C, Empty)
