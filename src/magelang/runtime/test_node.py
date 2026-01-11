
from .node import BaseNode, BaseToken

def test_construct_kwargs():

    class Foo(BaseNode):
        foo: int
        bar: str

    f = Foo(foo=1, bar='blabla')
    assert(f.foo == 1)
    assert(f.bar == 'blabla')

def test_construct_args():

    class Foo(BaseNode):
        foo: int
        bar: str

    f = Foo(1, 'blabla')
    assert(f.foo == 1)
    assert(f.bar == 'blabla')

def test_construct_kwarg_before_arg():

    class Foo(BaseNode):
        foo: int
        bar: str
        bax: bool

    f = Foo('blabla', True, foo=1)
    assert(f.foo == 1)
    assert(f.bar == 'blabla')

def test_construct_none():

    class Foo(BaseNode):
        blabla: int | None

    f = Foo()
    assert(f.blabla is None)

def test_default_construct_list_from_nothing():

    class Foo(BaseNode):
        blabla: list[int]
        hello: str

    f = Foo(hello='hello')
    assert(isinstance(f.blabla, list))
    assert(len(f.blabla) == 0)
    assert(f.hello == 'hello')

def test_default_construct_list_from_none():

    class Foo(BaseNode):
        blabla: list[int]
        hello: str

    f = Foo(blabla=None, hello='hello')
    assert(isinstance(f.blabla, list))
    assert(len(f.blabla) == 0)
    assert(f.hello == 'hello')

def test_repeat_list():

    class Foo(BaseNode):
        l: list[list[int]]

    f = Foo(5)
    assert(isinstance(f.l, list))
    assert(len(f.l) == 5)

def test_repeat_list_named():

    class Comma(BaseToken):
        pass

    class Foo(BaseNode):
        l: list[Comma]

    f = Foo(l=5)
    assert(isinstance(f.l, list))
    assert(len(f.l) == 5)
    assert(isinstance(f.l[0], Comma))
    assert(isinstance(f.l[1], Comma))
    assert(isinstance(f.l[2], Comma))
    assert(isinstance(f.l[3], Comma))
    assert(isinstance(f.l[4], Comma))

def test_coerce_list_elements():

    class Comma(BaseToken):
        pass

    class Bar(BaseNode):
        pass

    class Foo(BaseNode):
        l: list[tuple[Bar, Comma, Comma]]

    f = Foo([ Bar(), Bar() ])
    assert(isinstance(f.l, list))
    assert(len(f.l) == 2)
    assert(isinstance(f.l[0], tuple))
    assert(isinstance(f.l[1], tuple))
