
from .node import BaseNode, BaseSyntax, BaseToken

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
    assert(f.bax is True)

def test_construct_required_before_optional():

    class Foo(BaseNode):
        opt: int | None
        req: str

    foo = Foo('req')
    assert(foo.opt is None)
    assert(foo.req == 'req')

def test_construct_optional_none():

    class Foo(BaseNode):
        blabla: int | None

    f = Foo()
    assert(f.blabla is None)

def test_construct_optional_some():

    class Foo(BaseNode):
        blabla: int | None

    f = Foo(42)
    assert(f.blabla == 42)

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

def test_repeat_list_of_optional():

    class Foo(BaseNode):
        l: list[str | None]

    f = Foo(5)
    assert(isinstance(f.l, list))
    assert(len(f.l) == 5)
    assert(f.l[0] is None)
    assert(f.l[1] is None)
    assert(f.l[2] is None)
    assert(f.l[3] is None)
    assert(f.l[4] is None)

def test_repeat_list_of_token():

    class Comma(BaseToken):
        pass

    class Foo(BaseNode):
        l: list[Comma]

    f = Foo(5)
    assert(isinstance(f.l, list))
    assert(len(f.l) == 5)
    assert(isinstance(f.l[0], Comma))
    assert(isinstance(f.l[1], Comma))
    assert(isinstance(f.l[2], Comma))
    assert(isinstance(f.l[3], Comma))
    assert(isinstance(f.l[4], Comma))

def test_coerce_list_elements_to_tuples():

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
    assert(isinstance(f.l[0][0], Bar))
    assert(isinstance(f.l[0][1], Comma))
    assert(isinstance(f.l[0][2], Comma))
    assert(isinstance(f.l[1], tuple))
    assert(isinstance(f.l[1][0], Bar))
    assert(isinstance(f.l[1][1], Comma))
    assert(isinstance(f.l[1][2], Comma))

def test_coerce_nested():

    class Comma(BaseToken):
        pass

    class Bar(BaseNode):
        comma: Comma

    class Foo(BaseNode):
        bar: Bar

    class Test(BaseNode):
        foo: Foo

    test = Test()
    assert(isinstance(test.foo, Foo))
    assert(isinstance(test.foo.bar, Bar))
    assert(isinstance(test.foo.bar.comma, Comma))


def test_coerce_punctuated_nonempty():

    class Comma(BaseToken):
        pass

    class Foo(BaseNode):
        last: Comma | None

    foo = Foo()
    assert(foo.last is None)

def test_set_parents():

    class Bar1(BaseToken):
        pass

    class Bar2(BaseToken):
        pass

    class Foo(BaseNode):
        left: Bar1
        right: Bar2

    class Bax(BaseNode):
        value: Foo
        tup: tuple[Bar1, Bar2]

    root = Bax(Foo(Bar1(), Bar2()), (Bar1(), Bar2()))
    root.set_parents()
    assert(root.parent is None)
    assert(root.value.parent is root)
    assert(root.value.left.parent is root.value)
    assert(root.value.right.parent is root.value)
    assert(root.tup[0].parent is root)
    assert(root.tup[1].parent is root)
