
from .node import BaseNode

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

def test_default_construct_list():

    class Node(BaseNode):
        pass

    class Foo(Node):
        blabla: list[int]
        hello: str

    f = Foo(hello='hello')
    assert(isinstance(f.blabla, list))
    assert(len(f.blabla) == 0)
    assert(f.hello == 'hello')

