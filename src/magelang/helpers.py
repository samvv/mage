
from typing import Generator, Iterator, Iterable, Sequence

import marko.inline

from magelang.lang.python.emitter import emit
from magelang.lang.treespec import *
from magelang.lang.mage.ast import *
from magelang.lang.python.cst import *
from magelang.lang.mage.constants import integer_rule_type, string_rule_type
from magelang.lang.treespec.helpers import do_types_shallow_overlap, flatten_union, is_optional, is_static_type, make_optional, mangle_type, simplify_type
from magelang.logging import warn
from magelang.util import to_camel_case, is_iterator, NameGenerator, plural


def infer_type(expr: MageExpr, grammar: MageGrammar) -> Type:

    buffer = list()

    def visit(expr: MageExpr) -> Type:
        nonlocal buffer

        if isinstance(expr, MageHideExpr):
            buffer.append(expr.expr)
            # TODO return some internal constant rather than a public type
            return make_unit()

        if isinstance(expr, MageListExpr):
            element_field = visit(expr.element)
            separator_field = visit(expr.separator)
            return PunctType(element_field, separator_field, expr.min_count > 0)

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                return AnyType()
            if rule.is_extern:
                return ExternType(rule.type_name) #TokenType(rule.name) if rule.is_token else NodeType(rule.name)
            if rule.expr is None:
                return AnyType()
            if not rule.is_public:
                return visit(rule.expr)
            if grammar.is_token_rule(rule):
                return TokenType(rule.name)
            if grammar.is_variant_rule(rule):
                return VariantType(rule.name)
            return NodeType(rule.name)

        if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr):
            assert(False) # literals should already have been eliminated

        if isinstance(expr, MageRepeatExpr):
            element_type = visit(expr.expr)
            if expr.max == 0:
                return make_unit()
            elif expr.min == 0 and expr.max == 1:
                ty = make_optional(element_type)
            elif expr.min == 1 and expr.max == 1:
                ty = element_type
            else:
                ty = ListType(element_type, expr.min > 0)
            return ty

        if isinstance(expr, MageSeqExpr):
            types = list()
            for element in expr.elements:
                ty = visit(element)
                if is_unit_type(ty):
                    continue
                buffer = []
                types.append(ty)
            if len(types) == 1:
                return types[0]
            return TupleType(types)

        if isinstance(expr, MageLookaheadExpr):
            return make_unit()

        if isinstance(expr, MageChoiceExpr):
            return UnionType(list(visit(element) for element in expr.elements))

        assert_never(expr)

    return visit(expr)


def get_field_name(expr: MageExpr) -> str | None:
    if expr.label is not None:
        return expr.label
    if isinstance(expr, MageRefExpr):
        return expr.name
    if isinstance(expr, MageRepeatExpr):
        element_label = get_field_name(expr.expr)
        if element_label is not None:
            if expr.max > 1:
                return plural(element_label)
            return element_label
        return None
    if isinstance(expr, MageListExpr):
        element_label = get_field_name(expr.element)
        if element_label is not None:
            return plural(element_label)
        return None
    if isinstance(expr, MageCharSetExpr) or isinstance(expr, MageChoiceExpr):
        return None
    raise RuntimeError(f'unexpected {expr}')

def get_fields(expr: MageExpr, grammar: MageGrammar, include_hidden: bool = False) -> Generator[Field | MageExpr, None, None]:

    generator = NameGenerator()

    def generate_field_name() -> str:
        return generator(prefix='field_')

    def visit(expr: MageExpr, rule_name: str | None) -> Generator[Field | MageExpr, None, None]:

        if isinstance(expr, MageLookaheadExpr):
            return

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is not None and rule.expr is not None and not rule.is_public:
                yield from visit(rule.expr, rule.name)
                return

        if isinstance(expr, MageHideExpr):
            if include_hidden:
                yield from visit(expr.expr, rule_name)
            else:
                yield expr.expr
            return

        if isinstance(expr, MageSeqExpr):
            for element in expr.elements:
                yield from visit(element, rule_name)
            return

        if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr):
            assert(False) # literals should already have been eliminated by previous passes

        field_name = rule_name or get_field_name(expr) or generate_field_name()
        field_type = simplify_type(infer_type(expr, grammar))
        yield Field(field_name, field_type)

    return visit(expr, None)

type PyCondCase = tuple[PyExpr | None, Sequence[PyStmt]]

def namespaced(name: str, prefix: str) -> str:
    return prefix  + '_' + name if prefix else name

def to_py_class_name(name: str, prefix: str) -> str:
    return to_camel_case(namespaced(name, prefix))

def build_cond(cases: Sequence[PyCondCase]) -> list[PyStmt]:
    if len(cases) == 0:
        return []
    test, body = cases[0]
    if len(cases) == 1 and test is None:
        return list(body)
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

def quote_py_type(expr: PyExpr) -> PyExpr:
    return PyConstExpr(emit(expr))

def gen_py_type(ty: Type, prefix: str, immutable=False) -> PyExpr:
    if isinstance(ty, NodeType) or isinstance(ty, VariantType) or isinstance(ty, TokenType):
        return PyNamedExpr(to_py_class_name(ty.name, prefix))
    if isinstance(ty, ListType):
        return PySubscriptExpr(expr=PyNamedExpr('Sequence' if immutable else 'list'), slices=[ gen_py_type(ty.element_type, prefix, immutable) ])
    if isinstance(ty, PunctType):
        return PySubscriptExpr(expr=PyNamedExpr('ImmutablePunct' if immutable else 'Punctuated'), slices=[ gen_py_type(ty.element_type, prefix, immutable), gen_py_type(ty.separator_type, prefix, immutable) ])
    if isinstance(ty, TupleType):
        return PySubscriptExpr(expr=PyNamedExpr('tuple'), slices=list(gen_py_type(element, prefix, immutable) for element in ty.element_types))
    if isinstance(ty, UnionType):
        out = gen_py_type(ty.types[0], prefix, immutable)
        for element in ty.types[1:]:
            out = PyInfixExpr(left=out, op=PyVerticalBar(), right=gen_py_type(element, prefix, immutable))
        return out
    if isinstance(ty, ExternType):
        return rule_type_to_py_type(ty.name)
    if isinstance(ty, NoneType):
        return PyNamedExpr('None')
    if isinstance(ty, NeverType):
        return PyNamedExpr('Never')
    if isinstance(ty, AnyType):
        return PyNamedExpr('Any')
    assert_never(ty)

def rule_type_to_py_type(type_name: str) -> PyExpr:
    if type_name == string_rule_type:
        return PyNamedExpr('str')
    if type_name == integer_rule_type:
        return PyNamedExpr('int')
    if type_name == 'Float32':
        warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
        return PyNamedExpr('float')
    if type_name == 'Float' or type_name == 'Float64':
        return PyNamedExpr('float')
    raise AssertionError(f"unexpected rule type '{type_name}'")

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
    raise AssertionError(f"unexpected rule type '{type_name}'")

def gen_shallow_test(ty: Type, target: PyExpr, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_py_class_name(ty.name, prefix)) ])
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
    if isinstance(ty, AnyType):
        return PyNamedExpr('True')
    assert_never(ty)

def gen_deep_test(ty: Type, target: PyExpr, *, prefix: str) -> PyExpr:
    if isinstance(ty, VariantType):
        return PyCallExpr(operator=PyNamedExpr(f'is_{namespaced(ty.name, prefix)}'), args=[ target ])
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr(to_py_class_name(ty.name, prefix)) ])
    if isinstance(ty, NoneType):
        return build_is_none(target)
    if isinstance(ty, TupleType):
        return build_and([
            PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('tuple') ]),
            *(gen_deep_test(element, PySubscriptExpr(target, slices=[ PyConstExpr(i) ]), prefix=prefix) for i, element in enumerate(ty.element_types))
        ])
    if isinstance(ty, ListType):
        return PyInfixExpr(
            left=PyCallExpr(operator=PyNamedExpr('isinstance'), args=[ target, PyNamedExpr('list') ]),
            op=PyAndKeyword(),
            right=PyCallExpr(
                PyNamedExpr('all'),
                args=[
                    PyGeneratorExpr(
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix=prefix),
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
                        gen_deep_test(ty.element_type, PyNamedExpr('element'), prefix=prefix),
                        generators=[ PyComprehension(PyNamedPattern('element'), target) ]
                    )
                ]
            ),
        )
    if isinstance(ty, UnionType):
        return build_or(gen_deep_test(element, target, prefix=prefix) for element in ty.types)
    if isinstance(ty, ExternType):
        return gen_rule_type_test(ty.name, target)
    if isinstance(ty, NeverType):
        return PyNamedExpr('False')
    if isinstance(ty, AnyType):
        return PyNamedExpr('True')
    assert_never(ty)


def get_marko_element_text(el: Any) -> str:
    if isinstance(el, marko.inline.RawText):
        out = ''
        for child in el.children:
            out += child
        return out
    else:
        raise NotImplementedError()

def is_default_constructible(ty: Type, *, specs: Specs, allow_empty_sequences: bool = True) -> bool:
    visited = set()
    def visit(ty: Type, allow_empty_sequences: bool) -> bool:
        if isinstance(ty, ExternType):
            return False
        if isinstance(ty, NeverType):
            return False
        if isinstance(ty, AnyType):
            return False
        if isinstance(ty, ListType):
            return allow_empty_sequences and not ty.required
        if isinstance(ty, PunctType):
            return allow_empty_sequences and not ty.required
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, VariantType):
            return False
        if isinstance(ty, NodeType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, NodeSpec))
            return all(visit(field.ty, allow_empty_sequences) for field in spec.fields)
        if isinstance(ty, TokenType):
            if ty.name in visited:
                return False
            visited.add(ty.name)
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, TokenSpec))
            return spec.is_static
        if isinstance(ty, TupleType):
            return all(visit(element, False) for element in ty.element_types)
        if isinstance(ty, UnionType):
            # We assume the type has been simplified, such that singleton
            # union types do not occur. Otherwise, we did have to recurse
            # on the single union type member.
            return False
        assert_never(ty)
    return visit(ty, allow_empty_sequences)

def gen_default_constructor(ty: Type, *, specs: Specs, prefix: str) -> PyExpr:
    assert(is_default_constructible(ty, specs=specs))
    if isinstance(ty, NoneType):
        return PyNamedExpr('None')
    if isinstance(ty, NodeType) or isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(to_py_class_name(ty.name, prefix)))
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr('list'))
    if isinstance(ty, PunctType):
        # FIXME maybe add the generic arguments?
        return PyCallExpr(operator=PyNamedExpr('Punctuated'))
    if isinstance(ty, TupleType):
        return PyTupleExpr(elements=list(gen_default_constructor(element_type, specs=specs, prefix=prefix) for element_type in ty.element_types))
    if isinstance(ty, UnionType):
        # This assumes we already detected that there is exactly one
        # default-constrcuctible member in the union type
        for ty in flatten_union(ty):
            if is_default_constructible(ty, specs=specs):
                return gen_default_constructor(ty, specs=specs, prefix=prefix)
    raise RuntimeError(f'unexpected {ty}')

def gen_coercions(field_type: Type, *, specs: Specs, prefix: str, defs: dict[str, PyFuncDef]) -> tuple[Type, PyExpr]:

    param_name = 'value'

    def gen_coerce_fn(ty: Type, forbid_none: bool) -> tuple[Type, PyExpr]:

        cases: list[PyCondCase] = []
        types = list[Type]()
        for coerce_ty, coerce_body in gen_coerce_body(ty, forbid_none):
            cases.append((gen_shallow_test(coerce_ty, PyNamedExpr(param_name), prefix), coerce_body))
            types.append(coerce_ty)

        coerced_type = simplify_type(UnionType(types))

        id = f'{mangle_type(coerced_type)}_to_{mangle_type(ty)}'
        coerce_fn_name = f'_coerce_{id}'

        if id not in defs:
            py_param_type = gen_py_type(coerced_type, prefix=prefix, immutable=True)
            py_return_type = gen_py_type(ty, prefix=prefix)
            defs[id] = PyFuncDef(
                decorators=[ PyNamedExpr('no_type_check') ],
                name=coerce_fn_name,
                params=[ PyNamedParam(PyNamedPattern(param_name), annotation=quote_py_type(py_param_type)) ],
                return_type=quote_py_type(py_return_type),
                # For very simple fields, there's no need to do any checks. We
                # assume the type checker catches whatever error the user makes.
                body=cases[0][1] if len(cases) == 1 else build_cond([
                    *cases,
                    (
                        None,
                        [
                            PyRaiseStmt(
                                expr=PyCallExpr(
                                    operator=PyNamedExpr('ValueError'),
                                    # TODO inerpolate with `in_name`
                                    args=[ PyConstExpr(f"the coercion from {emit(py_param_type)} to {emit(py_return_type)} failed") ]
                                )
                            )
                        ]
                    )
                ])
            )

        return coerced_type, PyNamedExpr(coerce_fn_name)

    def gen_coerce_call(ty: Type, value: PyExpr, forbid_none: bool) -> tuple[Type, PyExpr]:
        coerce_ty, coerce_fn = gen_coerce_fn(ty, forbid_none)
        return coerce_ty, PyCallExpr(coerce_fn, args=[ value ])

    def gen_coerce_body(ty: Type, forbid_none: bool) -> Generator[tuple[Type, list[PyStmt]]]:

        if isinstance(ty, AnyType):
            yield ty, [ PyRetStmt(expr=PyNamedExpr(param_name)) ]
            return

        if isinstance(ty, NeverType):
            return

        if isinstance(ty, ExternType):
            yield ty, [ PyRetStmt(expr=PyNamedExpr(param_name)) ]
            return

        if isinstance(ty, UnionType):

            types = list(flatten_union(ty))

            for element_type in types:
                if isinstance(element_type, NoneType):
                    forbid_none = True

            rejected = set()
            out = []
            for element_type in types:
                for coerced_type, coerced_stmts in gen_coerce_body(element_type, True):
                    for i, (ty, _) in enumerate(out):
                        if do_types_shallow_overlap(ty, coerced_type):
                            rejected.add(i)
                            continue
                    out.append((coerced_type, coerced_stmts))

            for i, (ty, stmts) in enumerate(out):
                if i in rejected:
                    continue
                yield ty, stmts

            return

        if isinstance(ty, NoneType):
            yield NoneType(), [ PyRetStmt(expr=gen_default_constructor(ty, specs=specs, prefix=prefix)) ]
            return

        # Now that we've handled union types and empty types, we can
        # attempt to construct the type from a certain default value.
        # This can only happen if `None` is not already used by the type
        # itself. We continue processing the other types after this
        # operation.
        if not forbid_none and is_default_constructible(ty, specs=specs):
            yield NoneType(), [ PyRetStmt(expr=gen_default_constructor(ty, specs=specs, prefix=prefix)) ]

        if isinstance(ty, VariantType):
            yield ty, [ PyRetStmt(expr=PyNamedExpr(param_name)) ]
            return

        if isinstance(ty, NodeType):

            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, NodeSpec))

            this_class_name = to_py_class_name(ty.name, prefix)

            optional_fields: list[Field] = []
            required_fields: list[Field] = []

            for field in spec.fields:
                if is_optional(field.ty) or is_default_constructible(field.ty, specs=specs):
                    optional_fields.append(field)
                else:
                    required_fields.append(field)

            if len(required_fields) == 0:

                if not forbid_none:
                    yield NoneType(), [
                        PyRetStmt(expr=PyCallExpr(PyNamedExpr(this_class_name)))
                    ]

            elif len(required_fields) == 1:

                required_type = required_fields[0].ty

                coerce_type, coerce_expr = gen_coerce_call(required_type, PyNamedExpr(param_name), forbid_none)

                yield coerce_type, [
                    PyRetStmt(expr=PyCallExpr(
                        operator=PyNamedExpr(this_class_name),
                        args=[ coerce_expr ]
                    )),
                ]

            yield ty, [ PyRetStmt(expr=PyNamedExpr(param_name)) ]

            return

        if isinstance(ty, TokenType):

            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, TokenSpec))

            # If a token is not static, like an identifier or a string,
            # then we might be able to coerce the token based on the data
            # that it wraps.
            if not spec.is_static:

                yield ExternType(spec.field_type), [
                    PyRetStmt(
                        expr=PyCallExpr(
                            operator=PyNamedExpr(to_py_class_name(ty.name, prefix)),
                            args=[ PyNamedExpr(param_name) ]
                        )
                    )
                ]

            yield ty, [ PyRetStmt(expr=PyNamedExpr(param_name)) ]

            return

        if isinstance(ty, PunctType):

            assert(is_default_constructible(ty.separator_type, specs=specs))

            new_elements_name = f'new_{param_name}'

            if is_static_type(ty.element_type, specs=specs):
                yield ExternType(integer_rule_type), [
                    PyAssignStmt(PyNamedPattern(new_elements_name), value=PyCallExpr(PyNamedExpr('Punctuated'))),
                    PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyInfixExpr(PyNamedExpr(param_name), PyHyphen(), PyConstExpr(1)) ]), body=[
                        PyExprStmt(PyCallExpr(
                            PyAttrExpr(PyNamedExpr(new_elements_name), 'push'),
                            args=[
                                gen_default_constructor(ty.element_type, specs=specs, prefix=prefix),
                                gen_default_constructor(ty.separator_type, specs=specs, prefix=prefix),
                            ])
                       ),
                    ]),
                    PyExprStmt(PyCallExpr(
                        PyAttrExpr(PyNamedExpr(new_elements_name), 'push_final'),
                        args=[
                            gen_default_constructor(ty.element_type, specs=specs, prefix=prefix),
                        ])
                   ),
                    PyRetStmt(expr=PyNamedExpr(new_elements_name)),
                ]

            first_element_name = f'first_element'
            second_element_name = f'second_element'
            element_name = f'element'
            elements_iter_name = f'iterator'
            value_name = f'element_value'
            new_value_name = f'new_element_value'
            separator_name = f'element_separator'
            new_separator_name = f'new_element_separator'

            value_type, value_expr = gen_coerce_call(ty.element_type, PyNamedExpr(value_name), True)

            separator_type, separator_expr = gen_coerce_call(ty.separator_type, PyNamedExpr(separator_name), True)

            coerced_ty = UnionType([
                ListType(value_type, ty.required),
                ListType(TupleType(list([ value_type, make_optional(separator_type) ])), ty.required),
                PunctType(value_type, separator_type, ty.required),
            ])

            def gen_unwrap(last = False) -> list[PyStmt]:
                tuple_then: list[PyStmt] = [
                    PyAssignStmt(
                        pattern=PyNamedPattern(value_name),
                        value=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=0) ]),
                    ),
                ]
                plain_then: list[PyStmt] = [
                    PyAssignStmt(
                        pattern=PyNamedPattern(value_name),
                        value=PyNamedExpr(first_element_name),
                    ),
                ]
                if last:
                    tuple_then.append(
                        PyExprStmt(
                            PyCallExpr(
                                operator=PyNamedExpr('assert'),
                                args=[ build_is_none(PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(1) ])) ]
                            )
                        )
                    )
                else:
                    tuple_then.append(
                        PyAssignStmt(
                            pattern=PyNamedPattern(separator_name),
                            value=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=1) ])
                        )
                    )
                    tuple_then.append(
                        PyExprStmt(PyCallExpr(
                            operator=PyNamedExpr('assert'),
                            args=[ PyInfixExpr(PyNamedExpr(separator_name), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')) ]
                        ))
                    )
                    plain_then.append(
                        PyAssignStmt(
                            pattern=PyNamedPattern(separator_name),
                            value=gen_default_constructor(ty.separator_type, specs=specs, prefix=prefix),
                        )
                    )
                return build_cond([
                    (
                        # FIXME does not handle nested tuples
                        build_isinstance(PyNamedExpr(first_element_name), PyNamedExpr('tuple')),
                        tuple_then
                    ),
                    (
                        None,
                        plain_then
                    )
                ])

            yield coerced_ty, [
                PyAssignStmt(
                    pattern=PyNamedPattern(new_elements_name),
                    value=PyCallExpr(operator=PyNamedExpr('Punctuated'))
                ),
                PyAssignStmt(
                    pattern=PyNamedPattern(elements_iter_name),
                    value=PyCallExpr(operator=PyNamedExpr('iter'), args=[ PyNamedExpr(param_name) ]),
                ),
                PyTryStmt(
                    body=[
                        PyAssignStmt(
                            pattern=PyNamedPattern(first_element_name),
                            value=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                        ),
                        PyWhileStmt(
                            expr=PyNamedExpr('True'),
                            body=[
                                PyTryStmt(
                                    body=[
                                        PyAssignStmt(
                                            pattern=PyNamedPattern(second_element_name),
                                            value=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                                        ),
                                        *gen_unwrap(),
                                        PyAssignStmt(PyNamedPattern(new_value_name), value=value_expr),
                                        PyAssignStmt(PyNamedPattern(new_separator_name), value=separator_expr),
                                        PyExprStmt(
                                            expr=PyCallExpr(
                                                operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'push'),
                                                args=[
                                                    PyNamedExpr(new_value_name),
                                                    PyNamedExpr(new_separator_name)
                                                ]
                                            )
                                        ),
                                        PyAssignStmt(
                                            pattern=PyNamedPattern(first_element_name),
                                            value=PyNamedExpr(second_element_name),
                                        ),
                                    ],
                                    handlers=[
                                        PyExceptHandler(
                                            expr=PyNamedExpr('StopIteration'),
                                            body=[
                                                *gen_unwrap(last=True),
                                                PyAssignStmt(PyNamedPattern(new_value_name), value=value_expr),
                                                PyExprStmt(
                                                    expr=PyCallExpr(
                                                        operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'push_final'),
                                                        args=[ PyNamedExpr(new_value_name) ]
                                                    )
                                                ),
                                                PyBreakStmt(),
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    handlers=[
                        PyExceptHandler(
                            expr=PyNamedExpr('StopIteration'),
                            body=[ PyPassStmt() ]
                        )
                    ]
                ),
                PyRetStmt(expr=PyNamedExpr(new_elements_name))
            ]

            return

        if isinstance(ty, ListType):

            # Generates:
            #
            # out_name = list()
            # for element in in_name:
            #     ...
            #     out_name.append(new_element_name)

            new_elements_name = f'new_elements'

            if is_static_type(ty.element_type, specs=specs):
                yield ExternType(integer_rule_type), [
                    PyAssignStmt(PyNamedPattern(new_elements_name), value=PyCallExpr(PyNamedExpr('list'))),
                    PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyNamedExpr(param_name) ]), body= [
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(new_elements_name), 'append'), args=[ gen_default_constructor(ty.element_type, specs=specs, prefix=prefix) ])),
                    ]),
                    PyRetStmt(expr=PyNamedExpr(new_elements_name)),
                ]

            element_name = f'{param_name}_element'

            element_type, element_expr = gen_coerce_call(ty.element_type, PyNamedExpr(element_name), True)

            yield ListType(element_type, ty.required), [
                PyAssignStmt(
                    pattern=PyNamedPattern(new_elements_name),
                    value=PyCallExpr(operator=PyNamedExpr('list'))
                ),
                PyForStmt(
                    pattern=PyNamedPattern(element_name),
                    expr=PyNamedExpr(param_name),
                    body=[
                        PyExprStmt(
                            expr=PyCallExpr(
                                operator=PyAttrExpr(
                                    expr=PyNamedExpr(new_elements_name),
                                    name='append'
                                ),
                                args=[ element_expr ]
                            )
                        )
                    ]
                ),
                PyRetStmt(expr=PyNamedExpr(new_elements_name))
            ]

            return

        if isinstance(ty, TupleType):

            required: list[Type] = []

            for element_type in ty.element_types:
                if not is_optional(element_type) and not is_default_constructible(element_type, specs=specs, allow_empty_sequences=False):
                    required.append(element_type)

            if len(required) == 1:
                main_type = required[0]
                coerced_type, coerce_expr = gen_coerce_call(main_type, PyNamedExpr(param_name), True)
                elements = []
                for el_ty in ty.element_types:
                    if el_ty == main_type:
                        element = coerce_expr
                    elif is_optional(el_ty):
                        element = PyNamedExpr('None')
                    else:
                        element = gen_default_constructor(el_ty, specs=specs, prefix=prefix)
                    elements.append(element)
                yield coerced_type, [
                    PyRetStmt(expr=PyTupleExpr(
                        elements=elements,
                    )),
                ]

            new_elements: list[PyExpr] = []
            new_element_types = list[Type]()

            # Generates:
            #
            # return (_coerce_foo(value[0]), _coerce_bar(value[1]), ...)

            for i, element_type in enumerate(ty.element_types):

                element_name = f'{param_name}_{i}'

                new_element_type, new_element_expr = gen_coerce_call(
                    element_type,
                    PySubscriptExpr(
                        expr=PyNamedExpr(param_name),
                        slices=[ PyConstExpr(literal=i) ]
                    ),
                    False
                )

                new_elements.append(new_element_expr)
                new_element_types.append(new_element_type)

            yield TupleType(new_element_types), [
                PyRetStmt(expr=PyTupleExpr(elements=new_elements)),
            ]

            return

        assert_never(ty)

    return gen_coerce_fn(field_type, False)

