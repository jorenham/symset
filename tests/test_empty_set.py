import pytest

from symset import EmptySet, EmptySetType


def test_equiv_frozenset() -> None:
    empty_frozen = frozenset(())
    assert hash(EmptySet) == hash(empty_frozen)
    assert EmptySet == empty_frozen


def test_equal_set() -> None:
    assert EmptySet == set()


def test_cannot_construct() -> None:
    with pytest.raises(TypeError):
        _ = EmptySetType()
