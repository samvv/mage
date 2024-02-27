
# FIXME Node and Token should have a common base
# Generate a union type with all nodes/tokens

from typing import Iterator, Sequence, TypeVar, assert_never

from sweetener import is_iterator
from magelang.repr import *
from magelang.lang.python.cst import *

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

type Case = tuple[PyExpr | None, list[PyStmt]]

T = TypeVar('T', covariant=True)

def list_comma(it: Iterator[T] | Sequence[T]) -> list[tuple[T, PyComma | None]]:
    if not is_iterator(it):
        it = iter(it)
    out: list[tuple[T, PyComma | None]] = []
    prev: T | None = None
    while True:
        try:
            curr = next(it)
        except StopIteration:
            if prev is not None:
                out.append((prev, None))
            break
        if prev is not None:
            out.append((prev, PyComma()))
        prev = curr
    return out

specs = grammar_to_specs(grammar)

def namespace(name: str) -> str:
    return prefix + name if prefix else name

def to_class_case(name: str) -> str:
    return to_camel_case(namespace(name))

def gen_type(ty: Type) -> PyExpr:
    if isinstance(ty, NodeType):
        return PyNamedExpr(name=to_class_case(ty.name))
    if isinstance(ty, TokenType):
        return PyNamedExpr(name=to_class_case(ty.name))
    if  isinstance(ty, AnyTokenType):
        return PyNamedExpr(name='Token')
    if isinstance(ty, ListType):
        return PySubscriptExpr(expr=PyNamedExpr(name='list'), slices=[ (gen_type(ty.element_type), None) ])
    if isinstance(ty, TupleType):
        return PySubscriptExpr(expr=PyNamedExpr(name='tuple'), slices=[
            (PyTupleExpr(elements=list_comma(gen_type(element) for element in ty.element_types)), None)
        ])
    if isinstance(ty, UnionType):
        out = gen_type(ty.types[0])
        for element in ty.types[1:]:
            out = PyInfixExpr(left=out, op='|', right=gen_type(element))
        return out
    if isinstance(ty, ExternType):
        return rule_type_to_py_type(ty.name)
    if isinstance(ty, NoneType):
        return PyNamedExpr(name='None')
    raise RuntimeError(f'unexpected {ty}')

def is_optional(ty: Type) -> bool:
    # if isinstance(ty, NoneType):
    #     return True
    if isinstance(ty, UnionType):
        for element in flatten_union(ty):
            if isinstance(element, NoneType):
                return True
    return False

def is_default_constructible(ty: Type, allow_empty_lists: bool = True) -> bool:
    if isinstance(ty, ListType):
        return allow_empty_lists
    if isinstance(ty, NoneType):
        return True
    if isinstance(ty, NodeType):
        spec = specs.lookup(ty.name)
        if not isinstance(spec, NodeSpec):
            return False
        return all(is_default_constructible(field.ty, allow_empty_lists) for field in spec.members)
    if isinstance(ty, TokenType):
        spec = specs.lookup(ty.name)
        assert(isinstance(spec, TokenSpec))
        return spec.is_static
    if isinstance(ty, UnionType):
        counter = 0
        for element_type in ty.types:
            if is_default_constructible(element_type, allow_empty_lists):
                counter += 1
        return counter == 1
    raise RuntimeError(f'unexpected {ty}')

def gen_default_constructor(ty: Type) -> PyExpr:
    if isinstance(ty, NoneType):
        return PyNamedExpr(name='None')
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(name=to_class_case(ty.name)))
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr(name='list'))
    if isinstance(ty, UnionType):
        # This assumes we already detected that there is exactly one
        # default-constrcuctible member in the union type
        for ty in ty.types:
            if is_default_constructible(ty):
                return gen_default_constructor(ty)
    raise RuntimeError(f'unexpected {ty}')

def make_or(iter: Iterator[PyExpr]) -> PyExpr:
    try:
        out = next(iter)
    except StopIteration:
        return PyNamedExpr(name='False')
    for expr in iter:
        out = PyInfixExpr(left=out, op='or', right=expr)
    return out

def make_and(iter: Iterator[PyExpr]) -> PyExpr:
    try:
        out = next(iter)
    except StopIteration:
        return PyNamedExpr(name='True')
    for expr in iter:
        out = PyInfixExpr(left=out, op='and', right=expr)
    return out

def make_bitor(it: list[PyExpr] | Iterator[PyExpr]) -> PyExpr:
    if isinstance(it, list):
        it = iter(it)
    out = next(it)
    for element in it:
        out = PyInfixExpr(left=out, op='|', right=element)
    return out

def gen_instance_check(name: str, target: PyExpr) -> PyExpr:
    spec = specs.lookup(name)
    if isinstance(spec, VariantSpec):
        return PyCallExpr(operator=PyNamedExpr(name=f'is_{namespace(name)}'), args=[ (target, None) ])
    if isinstance(spec, NodeSpec) or isinstance(spec, TokenSpec):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name=to_class_case(name)), None) ])
    assert_never(spec)

def gen_shallow_test(ty: Type, target: PyExpr) -> PyExpr:
    if isinstance(ty, NodeType):
        return gen_instance_check(ty.name, target)
    if isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name=to_class_case(ty.name)), None) ])
    if isinstance(ty, NoneType):
        return PyInfixExpr(left=target, op='is', right=PyNamedExpr(name='None'))
    if isinstance(ty, TupleType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='tuple'), None) ])
        #return ast.BoolOp(left=test, op=ast.And(), values=[ make_and(gen_test(element, ast.Subscript(target, ast.Constant(i))) for i, element in enumerate(ty.element_types)) ])
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='list'), None) ])
    if isinstance(ty, UnionType):
        return make_or(gen_shallow_test(element, target) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    raise RuntimeError(f'unexpected {ty}')

def gen_rule_type_test(type_name: str, target: PyExpr) -> PyExpr:
    if type_name == 'String':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='str'), None) ])
    if type_name == 'Integer':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='int'), None) ])
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='float'), None) ])
    if type_name == 'Float' or type_name == 'Float64':
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name='float'), None) ])
    raise RuntimeError(f"unexpected rule type '{type_name}'")

def rule_type_to_py_type(type_name: str) -> PyExpr:
    if type_name == 'String':
        return PyNamedExpr(name='str')
    if type_name == 'Integer':
        return PyNamedExpr(name='int')
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyNamedExpr(name='float')
    if type_name == 'Float' or type_name == 'Float64':
        return PyNamedExpr(name='float')
    raise RuntimeError(f"unexpected rule type '{type_name}'")

def make_cond(cases: list[Case]) -> list[PyStmt]:
    if len(cases) == 0:
        return []
    test, body = cases[0]
    if len(cases) == 1 and test is None:
        return body
    assert(test is not None)
    first = PyIfCase(test=test, body=body)
    alternatives: list[PyElifCase] = []
    last = None
    for test, body in cases[1:]:
        if test is None:
            last = PyElseCase(body=body)
            break
        alternatives.append(PyElifCase(test=test, body=body))
    return [ PyIfStmt(first=first, alternatives=alternatives, last=last) ]

