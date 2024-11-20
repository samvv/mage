
import pytest
from magelang.runtime import Punctuated


def test_punct_elements():
    p0 = Punctuated()
    assert(len(p0.elements) == 0)
    p1 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, None ) ])
    assert(len(p1.elements) == 3)
    assert(p1.elements[0] == 1)
    assert(p1.elements[1] == 2)
    assert(p1.elements[2] == 3)
    p2 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, 'c' ) ])
    assert(len(p2.elements) == 3)
    assert(p2.elements[0] == 1)
    assert(p2.elements[1] == 2)
    assert(p2.elements[2] == 3)

def test_punct_last_delimiter():
    p1 = Punctuated()
    assert(p1.last_delimiter is None)
    p2 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, None ) ])
    assert(p2.last_delimiter is None)
    p3 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, 'c' ) ])
    assert(p3.last_delimiter == 'c')

def test_punct_delimited():
    p1 = Punctuated()
    assert(len(p1.delimited) == 0)
    pytest.raises(IndexError, lambda: p1.delimited[0])
    p2 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, None ) ])
    assert(len(p2.delimited) == 2)
    assert(p2.delimited[0][0] == 1)
    assert(p2.delimited[0][1] == 'a')
    assert(p2.delimited[1][0] == 2)
    assert(p2.delimited[1][1] == 'b')
    pytest.raises(IndexError, lambda: p2.delimited[2])
    p3 = Punctuated([ ( 1, 'a' ), ( 2, 'b' ), ( 3, 'c' ) ])
    assert(len(p3.delimited) == 3)
    assert(p3.delimited[0][0] == 1)
    assert(p3.delimited[0][1] == 'a')
    assert(p3.delimited[1][0] == 2)
    assert(p3.delimited[1][1] == 'b')
    assert(p3.delimited[2][0] == 3)
    assert(p3.delimited[2][1] == 'c')
    pytest.raises(IndexError, lambda: p3.delimited[3])
