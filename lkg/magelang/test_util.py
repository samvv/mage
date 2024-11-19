
import pytest
from magelang.util import DropProxy


def test_drop_none():
    d1 = DropProxy([], 0)
    assert(len(d1) == 0)
    pytest.raises(IndexError, lambda: d1[0])
    pytest.raises(IndexError, lambda: d1[1])
    pytest.raises(IndexError, lambda: d1[2])
    pytest.raises(IndexError, lambda: d1[3])
    assert(len(d1[0:0]) == 0)
    assert(len(d1[0:1]) == 0)
    assert(len(d1[0:2]) == 0)
    assert(len(d1[1:0]) == 0)
    assert(len(d1[1:1]) == 0)
    assert(len(d1[1:2]) == 0)
    d2 = DropProxy([1,2,3], 0)
    assert(len(d2) == 3)
    assert(d2[0] == 1)
    assert(d2[1] == 2)
    assert(d2[2] == 3)

def test_drop_one():
    d1 = DropProxy([ 1, 2, 3 ], 1)
    assert(len(d1) == 2)
    assert(d1[0] == 1)
    assert(d1[1] == 2)
    pytest.raises(IndexError, lambda: d1[2])
    pytest.raises(IndexError, lambda: d1[3])
    pytest.raises(IndexError, lambda: d1[4])

def test_drop_many():
    d1 = DropProxy([ 5, 4, 3, 2, 1 ], 3)
    assert(len(d1) == 2)
    assert(d1[0] == 5)
    assert(d1[1] == 4)
    pytest.raises(IndexError, lambda: d1[2])
    pytest.raises(IndexError, lambda: d1[3])
    pytest.raises(IndexError, lambda: d1[4])
    rev = list(reversed(d1))
    assert(len(rev) == 2)
    assert(d1[1] == 4)
    assert(d1[0] == 5)

