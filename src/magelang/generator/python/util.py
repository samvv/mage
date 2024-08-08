
from typing import Iterator, Iterable
import marko.inline
from sweetener import is_iterator, warn
from magelang.repr import *
from magelang.lang.python.cst import *
from magelang.util import to_camel_case

type Case = tuple[PyExpr | None, list[PyStmt]]

def namespaced(name: str, prefix: str) -> str:
    return prefix + name if prefix else name

def to_class_name(name: str, prefix: str) -> str:
    return to_camel_case(namespaced(name, prefix))

def build_cond(cases: list[Case]) -> list[PyStmt]:
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

def build_is_none(value: PyExpr) -> PyExpr:
    return PyInfixExpr(
        left=value,
        op=PyIsKeyword(),
        right=PyNamedExpr('None')
    )

def build_infix(it: Iterable[PyExpr] | Iterator[PyExpr], op: PyInfixOp, init: PyExpr) -> PyExpr:
    if not is_iterator(it):
        it = iter(it)
    try:
        out = next(it)
    except StopIteration:
        return init
    for expr in it:
        out = PyInfixExpr(left=out, op=op, right=expr)
    return out

def build_or(iter: Iterable[PyExpr]) -> PyExpr:
    return build_infix(iter, PyOrKeyword(), PyNamedExpr('False'))

def build_and(iter: Iterable[PyExpr]) -> PyExpr:
    return build_infix(iter, PyAndKeyword(), PyNamedExpr('True'))

def build_union(it: list[PyExpr] | Iterator[PyExpr]) -> PyExpr:
    return build_infix(it, PyVerticalBar(), PyNamedExpr('Never'))

def build_isinstance(expr: PyExpr, ty: PyExpr) -> PyExpr:
    return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ expr, ty ])

def gen_py_type(ty: Type, prefix: str) -> PyExpr:
    if isinstance(ty, NodeType) or isinstance(ty, VariantType) or isinstance(ty, TokenType):
        return PyNamedExpr(to_class_name(ty.name, prefix))
    if isinstance(ty, ListType):
        return PySubscriptExpr(expr=PyNamedExpr('list'), slices=[ gen_py_type(ty.element_type, prefix) ])
    if isinstance(ty, PunctType):
        return PySubscriptExpr(expr=PyNamedExpr('Punctuated'), slices=[ gen_py_type(ty.element_type, prefix), gen_py_type(ty.separator_type, prefix) ])
    if isinstance(ty, TupleType):
        return PySubscriptExpr(expr=PyNamedExpr('tuple'), slices=list(gen_py_type(element, prefix) for element in ty.element_types))
    if isinstance(ty, UnionType):
        out = gen_py_type(ty.types[0], prefix)
        for element in ty.types[1:]:
            out = PyInfixExpr(left=out, op=PyVerticalBar(), right=gen_py_type(element, prefix))
        return out
    if isinstance(ty, ExternType):
        return rule_type_to_py_type(ty.name)
    if isinstance(ty, NoneType):
        return PyNamedExpr('None')
    if isinstance(ty, NeverType):
        return PyNamedExpr('Never')
    raise RuntimeError(f'unexpected {ty}')

def rule_type_to_py_type(type_name: str) -> PyExpr:
    if type_name == 'String':
        return PyNamedExpr('str')
    if type_name == 'Integer':
        return PyNamedExpr('int')
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyNamedExpr('float')
    if type_name == 'Float' or type_name == 'Float64':
        return PyNamedExpr('float')
    raise RuntimeError(f"unexpected rule type '{type_name}'")

def gen_rule_type_test(type_name: str, target: PyExpr) -> PyExpr:
    if type_name == 'String':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('str') ])
    if type_name == 'Integer':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('int') ])
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('float') ])
    if type_name == 'Float' or type_name == 'Float64':
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('float') ])
    raise RuntimeError(f"unexpected rule type '{type_name}'")

def gen_shallow_test(ty: Type, target: PyExpr, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_class_name(ty.name, prefix)) ])
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('tuple') ])
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('list') ])
    if isinstance(ty, PunctType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('Punctuated') ])
    if isinstance(ty, UnionType):
        return build_or(gen_shallow_test(element, target, prefix) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr('False')
    raise RuntimeError(f'unexpected {ty}')

def gen_deep_test(ty: Type, target: PyExpr, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_class_name(ty.name, prefix)) ])
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return build_and([
            PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('tuple') ]),
            *(gen_deep_test(element, PySubscriptExpr(target, slices=[ PyConstExpr(i) ]), prefix) for i, element in enumerate(ty.element_types))
        ])
    if isinstance(ty, ListType):
        return PyInfixExpr(
            left=PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('list') ]),
            op=PyAndKeyword(),
            right=PyCallExpr(
                PyNamedExpr('all'),
                args=[
                    PyGeneratorExpr(
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix),
                        generators=[ PyComprehension(PyNamedPattern('element'), target) ]
                    )
                ]
            ),
        )
    if isinstance(ty, PunctType):
        return PyInfixExpr(
            left=PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('Punctuated') ]),
            op=PyAndKeyword(),
            right=PyCallExpr(
                PyNamedExpr('all'),
                args=[
                    PyGeneratorExpr(
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix),
                        generators=[ PyComprehension(PyNamedPattern('element'), target) ]
                    )
                ]
            ),
        )
    if isinstance(ty, UnionType):
        return build_or(gen_deep_test(element, target, prefix) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr('False')
    raise RuntimeError(f'unexpected {ty}')


def get_marko_element_text(el: Any) -> str:
    if isinstance(el, marko.inline.RawText):
        out = ''
        for child in el.children:
            out += child
        return out
    else:
        raise NotImplementedError()

