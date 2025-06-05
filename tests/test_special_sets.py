# pyright: reportUnknownVariableType=false
# ruff: noqa: SIM201, SIM202

from collections.abc import Set as AbstractSet
from typing import Final, Never, TypeAlias

import pytest
from hypothesis import given, strategies as st

from symset import Empty, EmptyType, Universe, UniverseType

_AnyEmpty: TypeAlias = AbstractSet[Never]
_SpecialSet: TypeAlias = EmptyType | UniverseType

_EMPTY_SET: Final[set[Never]] = set()
_EMPTY_FROZENSET: Final[frozenset[Never]] = frozenset(())
_FALSY_NON_SET: Final[tuple[object, ...]] = None, False, 0, 0.0, "", b"", (), [], {}


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_subclass_abc(set_: _SpecialSet) -> None:
    assert isinstance(set_, AbstractSet)
    assert issubclass(type(set_), AbstractSet)


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_cannot_construct(set_: _SpecialSet) -> None:
    with pytest.raises(TypeError):
        _ = type(set_)()  # pyright: ignore[reportGeneralTypeIssues]


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_no_dict(set_: _SpecialSet) -> None:
    assert not hasattr(set_, "__dict__")


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_no_pyo3_internals(set_: _SpecialSet) -> None:
    assert not hasattr(set_, "__richcmp__")
    assert not hasattr(set_, "__concat__")
    assert not hasattr(set_, "__repeat__")
    assert not hasattr(set_, "__traverse__")
    assert not hasattr(set_, "__clear__")


@pytest.mark.parametrize((("set_", "name")), [(Empty, "Empty"), (Universe, "Universe")])
def test_repr(set_: _SpecialSet, name: str) -> None:
    assert repr(set_) == name


@pytest.mark.parametrize((("set_", "name")), [(Empty, "∅"), (Universe, "U")])
def test_str(set_: _SpecialSet, name: str) -> None:
    assert str(set_) == name


def test_bool() -> None:
    assert not Empty
    assert Universe


@given(st.none() | st.booleans() | st.integers() | st.floats() | st.text())
def test_contains_value(value: float | str | None) -> None:
    assert value not in Empty
    assert value in Universe


@pytest.mark.parametrize("value", [Empty, Universe])
def test_contains_other(value: _SpecialSet) -> None:
    assert value not in Empty
    assert value in Universe


def test_len() -> None:
    assert len(Empty) == 0
    with pytest.raises(OverflowError):
        _ = iter(Universe)


def test_iter() -> None:
    assert sum(1 for _ in iter(Empty)) == 0
    with pytest.raises(OverflowError):
        _ = iter(Universe)


def test_hash() -> None:
    assert hash(Empty) == hash(_EMPTY_FROZENSET)
    assert hash(Universe) == ~hash(_EMPTY_FROZENSET)


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_cmp_self(set_: _SpecialSet) -> None:
    assert set_ == set_
    assert set_ <= set_
    assert not (set_ < set_)
    assert not (set_ > set_)
    assert set_ >= set_
    assert not (set_ != set_)


@pytest.mark.parametrize("lhs", [Empty, _EMPTY_FROZENSET, _EMPTY_SET])
@pytest.mark.parametrize("rhs", [Empty, _EMPTY_FROZENSET, _EMPTY_SET])
def test_cmp_empty_empty(lhs: _AnyEmpty, rhs: _AnyEmpty) -> None:
    assert lhs == rhs
    assert lhs <= rhs
    assert not (lhs < rhs)
    assert not (lhs > rhs)
    assert lhs >= rhs
    assert not (lhs != rhs)


@pytest.mark.parametrize("empty", [Empty, _EMPTY_FROZENSET, _EMPTY_SET])
def test_cmp_empty_universe(empty: _AnyEmpty) -> None:
    assert not (empty == Universe)
    assert empty <= Universe
    assert empty < Universe
    assert not (empty > Universe)
    assert not (empty >= Universe)
    assert empty != Universe


@pytest.mark.parametrize("empty", [Empty, _EMPTY_FROZENSET, _EMPTY_SET])
def test_cmp_universe_empty(empty: _AnyEmpty) -> None:
    assert not (Universe == empty)
    assert not (Universe <= empty)
    assert not (Universe < empty)
    assert Universe > empty
    assert Universe >= empty
    assert Universe != empty


@pytest.mark.parametrize("other", [{0}, frozenset({0}), Universe])
def test_cmp_empty_nonempty(other: AbstractSet[object]) -> None:
    assert not (Empty == other)
    assert Empty <= other
    assert Empty < other
    assert not (Empty > other)
    assert not (Empty >= other)
    assert Empty != other


@pytest.mark.parametrize("other", [Empty, _EMPTY_FROZENSET, _EMPTY_SET, {0}, frozenset({0})])
def test_cmp_universe_subset(other: AbstractSet[object]) -> None:
    assert not (Universe == other)
    assert not (Universe <= other)
    assert not (Universe < other)
    assert Universe > other
    assert Universe >= other
    assert Universe != other


@pytest.mark.parametrize("special", [Empty, Universe])
@pytest.mark.parametrize("other", [*_FALSY_NON_SET, {None}, frozenset({None})])
def test_ne(special: _SpecialSet, other: object) -> None:
    assert not (special == other)
    assert not (other == special)
    assert special != other
    assert other != special


@pytest.mark.parametrize("set_", [Empty, Universe])
@pytest.mark.parametrize("not_a_set", [object(), 0, "", (), [], {}])
def test_setop_raise(set_: _SpecialSet, not_a_set: object) -> None:
    with pytest.raises(TypeError):
        _ = set_ <= not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ < not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ > not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ >= not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ & not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = not_a_set & set_  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ | not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = not_a_set | set_  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ ^ not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = not_a_set ^ set_  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = set_ - not_a_set  # pyright: ignore[reportOperatorIssue]
    with pytest.raises(TypeError):
        _ = not_a_set - set_  # pyright: ignore[reportOperatorIssue]


@pytest.mark.parametrize("special", [Empty, Universe])
@pytest.mark.parametrize("empty", [Empty, _EMPTY_FROZENSET, _EMPTY_SET])
def test_setops_empty(special: _SpecialSet, empty: _AnyEmpty) -> None:
    assert special & empty is Empty
    assert special | empty is special
    assert special ^ empty is special
    assert special - empty is special
    assert empty - special is Empty
    assert special.isdisjoint(empty)

    # TODO(jorenham): reflected
    # https://github.com/jorenham/symset/issues/31


@pytest.mark.parametrize("special", [Empty, Universe])
def test_setops_universe(special: _SpecialSet) -> None:
    assert Universe & special is special
    assert Universe | special is Universe
    assert Universe ^ special is special.C
    assert Universe - special is special.C
    assert special - Universe is Empty
    assert special.isdisjoint(Universe) is not special


def test_complement() -> None:
    assert Empty.C is Universe
    assert Universe.C is Empty


@pytest.mark.parametrize("set_", [Empty, Universe])
def test_involution(set_: _SpecialSet) -> None:
    assert set_ is set_
    assert set_.C is not set_
    assert set_.C.C is set_
