
# FIXME Node and Token should have a common base
# Generate a union type with all nodes/tokens

from typing import Iterator, Sequence, assert_never, TypeVar, cast

import templaty
from sweetener import is_iterator, warn
from magelang.repr import *
from magelang.util import NameGenerator
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit

ctx = templaty.load_context()

grammar = cast(Grammar, ctx['grammar'])
prefix = cast(str, ctx['prefix'])

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def namespace(name: str) -> str:
    return prefix + name if prefix else name

def to_class_name(name: str) -> str:
    return to_camel_case(namespace(name))

type Case = tuple[PyExpr | None, list[PyStmt]]

T = TypeVar('T', covariant=True)
 
is_node_proc_name = f'is_{prefix}node'
is_token_proc_name = f'is_{prefix}token'
is_syntax_name = f'is_{prefix}syntax'
for_each_child_name = f'for_each_{prefix}child'

node_class_name = to_class_name('node')
token_class_name = to_class_name('token')
syntax_class_name = to_class_name('syntax')

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

def make_infix(it: list[PyExpr] | Iterator[PyExpr], op: str, init: PyExpr) -> PyExpr:
    if isinstance(it, list):
        it = iter(it)
    try:
        out = next(it)
    except StopIteration:
        return init
    for expr in it:
        out = PyInfixExpr(left=out, op=op, right=expr)
    return out

def make_or(iter: Iterator[PyExpr]) -> PyExpr:
    return make_infix(iter, 'or', PyNamedExpr(name='False'))

def make_and(iter: Iterator[PyExpr]) -> PyExpr:
    return make_infix(iter, 'and', PyNamedExpr(name='True'))

def make_union(it: list[PyExpr] | Iterator[PyExpr]) -> PyExpr:
    return make_infix(it, '|', PyNamedExpr(name='Never'))

specs = grammar_to_specs(grammar)

def gen_type(ty: Type) -> PyExpr:
    if isinstance(ty, NodeType):
        return PyNamedExpr(name=to_class_name(ty.name))
    if isinstance(ty, TokenType):
        return PyNamedExpr(name=to_class_name(ty.name))
    if  isinstance(ty, AnyTokenType):
        return PyNamedExpr(name='Token')
    if  isinstance(ty, AnyNodeType):
        return PyNamedExpr(name='Node')
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

def is_optional(ty: Type) -> bool:
    # if isinstance(ty, NoneType):
    #     return True
    if isinstance(ty, UnionType):
        for element in flatten_union(ty):
            if isinstance(element, NoneType):
                return True
    return False

def gen_instance_check(name: str, target: PyExpr) -> PyExpr:
    spec = specs.lookup(name)
    if isinstance(spec, VariantSpec):
        return PyCallExpr(operator=PyNamedExpr(name=f'is_{namespace(name)}'), args=[ (target, None) ])
    if isinstance(spec, NodeSpec) or isinstance(spec, TokenSpec):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=[ (target, PyComma()), (PyNamedExpr(name=to_class_name(name)), None) ])
    raise RuntimeError(f'unexpected {spec}')

def gen_shallow_test(ty: Type, target: PyExpr) -> PyExpr:
    if isinstance(ty, NodeType):
        return gen_instance_check(ty.name, target)
    if isinstance(ty, TokenType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ target, PyNamedExpr(name=to_class_name(ty.name)) ]))
    if isinstance(ty, NoneType):
        return PyInfixExpr(left=target, op='is', right=PyNamedExpr(name='None'))
    if isinstance(ty, TupleType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ target, PyNamedExpr(name='tuple') ]))
        #return ast.BoolOp(left=test, op=ast.And(), values=[ make_and(gen_test(element, ast.Subscript(target, ast.Constant(i))) for i, element in enumerate(ty.element_types)) ])
    if isinstance(ty, ListType):
        return PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ target, PyNamedExpr(name='list') ]))
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

def cst() -> str:

    def is_default_constructible(ty: Type, allow_empty_lists: bool = True) -> bool:
        if isinstance(ty, ListType):
            return allow_empty_lists
        if isinstance(ty, NoneType):
            return True
        if isinstance(ty, NodeType):
            spec = specs.lookup(ty.name)
            if not isinstance(spec, NodeSpec): # if it's a VariantSpec
                return False
            return all(is_default_constructible(field.ty, allow_empty_lists) for field in spec.members)
        if isinstance(ty, TokenType):
            spec = specs.lookup(ty.name)
            assert(isinstance(spec, TokenSpec))
            return spec.is_static
        if isinstance(ty, TupleType):
            return all(is_default_constructible(element, False) for element in ty.element_types)
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
            return PyCallExpr(operator=PyNamedExpr(name=to_class_name(ty.name)))
        if isinstance(ty, ListType):
            return PyCallExpr(operator=PyNamedExpr(name='list'))
        if isinstance(ty, TupleType):
            return PyTupleExpr(elements=list_comma(gen_default_constructor(element_type) for element_type in ty.element_types))
        if isinstance(ty, UnionType):
            # This assumes we already detected that there is exactly one
            # default-constrcuctible member in the union type
            for ty in ty.types:
                if is_default_constructible(ty):
                    return gen_default_constructor(ty)
        raise RuntimeError(f'unexpected {ty}')

    def gen_init_body(field_name: str, field_type: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], stmts: list[PyStmt]) -> Type:

        def visit(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], stmts: list[PyStmt], has_none: bool) -> tuple[Type, bool]:
            """
            This function returns a new type and a boolean indicating whether any coercions have been added.
            """

            if isinstance(ty, NodeType):
                #assert(ty == orig_ty)
                coerced_types: list[Type] = []
                coerced_types.append(ty)
                # FIXME this should probably be behind an if-statemnet
                stmts.append(assign(PyNamedExpr(name=in_name)))
                spec = specs.lookup(ty.name)
                coercable = False
                # spec can also be a VariantSpec so we need to run isinstance
                if isinstance(spec, NodeSpec) and len(spec.members) == 1:
                    # TODO maybe also coerce spec.members[0].ty?
                    coercable = True
                    first_ty = spec.members[0].ty
                    if_body: list[PyStmt] = []
                    if_body.append(assign(PyCallExpr(operator=PyNamedExpr(name=to_class_name(ty.name)), args=list([ (PyNamedExpr(name=in_name), None) ]))))
                    stmts.append(PyIfStmt(first=PyIfCase(test=gen_shallow_test(first_ty, PyNamedExpr(name=in_name)), body=if_body)))
                    coerced_types.append(first_ty)
                return UnionType(coerced_types), coercable

            if isinstance(ty, NoneType):
                stmts.append(assign(PyNamedExpr(name='None')))
                return ty, False

            if isinstance(ty, TokenType):
                coerced_types: list[Type] = []
                coerced_types.append(ty)
                spec = specs.lookup(ty.name)
                assert(isinstance(spec, TokenSpec))
                cases: list[Case] = []
                if spec.is_static:
                    if not has_none:
                        coerced_types.append(NoneType())
                        cases.append((
                            PyInfixExpr(left=PyNamedExpr(name=in_name), op='is', right=PyNamedExpr(name='None')),
                            [ assign(PyCallExpr(operator=PyNamedExpr(name=to_class_name(ty.name)), args=[])) ]
                        ))
                else:
                    coerced_types.append(ExternType(spec.field_type))
                    # out_name = Token(in_name)
                    cases.append((
                        gen_rule_type_test(spec.field_type, PyNamedExpr(name=in_name)),
                        [ assign(PyCallExpr(operator=PyNamedExpr(name=to_class_name(ty.name)), args=[ (PyNamedExpr(name=in_name), None) ])) ]
                    ))
                # out_name = in_name
                cases.append((None, [ assign(PyNamedExpr(name=in_name)) ]))
                stmts.extend(make_cond(cases))
                return UnionType(coerced_types), True 

            if isinstance(ty, ListType):
                # out_name = list()
                # for element in in_name:
                #     ...
                #     out_name.append(new_element_name)
                coercable_types: list[Type] = []
                cases: list[Case] = []
                orelse: list[PyStmt] = []
                for_body: list[PyStmt] = []

                new_elements_name = f'new_{in_name}'
                element_name = f'{in_name}_element'
                new_element_name = f'new_{in_name}_element'

                if not has_none:
                    coercable_types.append(NoneType())
                    cases.append((
                        PyInfixExpr(left=PyNamedExpr(name=in_name), op='is', right=PyNamedExpr(name='None')),
                        [ assign(PyCallExpr(operator=PyNamedExpr(name='list'))) ]
                    ))

                orelse.append(PyAssignStmt(pattern=PyNamedPattern(name=new_elements_name), expr=PyCallExpr(operator=PyNamedExpr(name='list'))))

                element_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)
                element_type, element_coercable = visit(ty.element_type, element_name, element_assign, for_body, False)

                coercable_types.append(ListType(element_type))

                for_body.append(PyExprStmt(expr=PyCallExpr(operator=PyAttrExpr(expr=PyNamedExpr(name=new_elements_name), name='append'), args=[ (PyNamedExpr(name=new_element_name), None) ])))
                orelse.append(PyForStmt(pattern=PyNamedPattern(name=element_name), expr=PyNamedExpr(name=in_name), body=for_body))

                orelse.append(assign(PyNamedExpr(name=new_elements_name)))

                cases.append((
                    None,
                    orelse
                ))

                stmts.extend(make_cond(cases))

                return UnionType(coercable_types), True

            if isinstance(ty, TupleType):

                # element_0 = field[0]
                # new_element_0 = ...
                # ...
                # out_name = (new_element_0, new_element_1, ...)

                coercable = False
                coerced_types: list[Type] = []
                cases: list[Case] = []
                required: list[Type] = []

                for element_type in ty.element_types:
                    if not is_default_constructible(element_type, allow_empty_lists=False):
                        required.append(element_type)

                if len(required) == 1:

                    case_body: list[PyStmt] = []

                    first_type = required[0]

                    coercable = True

                    def first_assign(value: PyExpr):
                        assert(isinstance(ty, TupleType)) # Needed to keep Pyright happy
                        return assign(PyTupleExpr(elements=list_comma(value if el_ty == first_type else gen_default_constructor(el_ty) for el_ty in ty.element_types)))

                    new_first_type, _ = visit(first_type, in_name, first_assign, case_body, has_none)
                    coerced_types.append(new_first_type)
                    cases.append((
                        gen_shallow_test(new_first_type, PyNamedExpr(name=in_name)),
                        #ast.Compare(left=PyNamedExpr(name=in_name), ops=[ ast.Is() ], comparators=[ PyNamedExpr(name='None') ]),
                        case_body
                    ))

                orelse: list[PyStmt] = []
                new_elements: list[PyExpr] = []
                new_element_types: list[Type] = []

                orelse.append(PyExprStmt(expr=PyCallExpr(operator=PyNamedExpr(name='assert'), args=[ (gen_shallow_test(ty, PyNamedExpr(name=in_name)), None) ])))

                for i, element_type in enumerate(ty.element_types):

                    element_name = f'{in_name}_{i}'
                    new_element_name = f'new_{in_name}_{i}'
                    element_assign = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name=name), expr=value)

                    new_elements.append(PyNamedExpr(name=new_element_name))

                    orelse.append(PyAssignStmt(pattern=PyNamedPattern(name=element_name), expr=PySubscriptExpr(expr=PyNamedExpr(name=in_name), slices=list([ (PyConstExpr(literal=i), None) ]))))

                    new_element_type, element_coercable = visit(element_type, element_name, element_assign, orelse, False)

                    if element_coercable:
                        coercable = True

                    new_element_types.append(new_element_type)


                orelse.append(assign(PyTupleExpr(elements=list_comma(new_elements))))
                cases.append((None, orelse))
                coerced_types.append(TupleType(new_element_types))

                stmts.extend(make_cond(cases))

                return UnionType(coerced_types), coercable

            if isinstance(ty, UnionType):

                coercable = False
                coerced_types: list[Type] = []
                cases: list[Case] = []

                for element_type in ty.types:
                    if isinstance(element_type, NoneType):
                        has_none = True
                        break

                for element_type in ty.types:
                    body: list[PyStmt] = [] 
                    new_type, element_coercable = visit(element_type, in_name, assign, body, has_none)
                    if element_coercable:
                        coercable = True
                    coerced_types.append(new_type)
                    cases.append((
                        gen_shallow_test(new_type, PyNamedExpr(name=in_name)),
                        body
                    ))

                # TODO ensure duplicate types are eliminated
                # if len(not_none) == 1 and is_default_constructible(not_none[0]):
                #     cases.append((
                #         None,
                #         [ assign(gen_default_constructor(ty.types[0])) ]
                #     ))
                # else:
                cases.append((
                    None,
                    list([ PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ValueError'), args=[ (PyConstExpr(literal=f"the field '{field_name}' received an unrecognised value'"), None) ])) ])
                ))

                if coercable:
                    stmts.extend(make_cond(cases))
                else:
                    stmts.append(assign(PyNamedExpr(name=in_name)))

                # ty_0 = ty.types[0]
                # ty_n = ty.types[1:]
                # if_body = []
                # new_ty_0 = visit(ty_0, in_name, out_name, if_body)
                # if_orelse = []
                # new_rest = visit(UnionType(ty_n), in_name, out_name, if_orelse)
                # stmts.append(ast.If(test=gen_shallow_test(ty_0, PyNamedExpr(name=in_name)), body=if_body, orelse=if_orelse))

                return UnionType(coerced_types), coercable

            raise RuntimeError(f'unexpected {ty}')

        ty, _ = visit(field_type, in_name, assign, stmts, False)
        return ty

    stmts: list[PyStmt] = []

    for spec in specs:

        if isinstance(spec, NodeSpec):

            body: list[PyStmt] = []
            params: list[PyParam] = []
            init_body: list[PyStmt] = []

            for field in spec.members:

                # param_type = get_coerce_type(field.ty)
                # tmp = f'{field.name}__coerced'

                assign: Callable[[PyExpr], PyStmt] = lambda value, field=field: PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern(name='self'), name=field.name), annotation=gen_type(field.ty), expr=value)
                param_type = gen_init_body(field.name, field.ty, field.name, assign, init_body)

                param_type_str = emit(gen_type(param_type))
                params.append(PyNamedParam(
                    pattern=PyNamedPattern(name=field.name),
                    annotation=PyConstExpr(literal=param_type_str),
                    default=PyNamedExpr(name='None') if is_optional(param_type) else None
                ))

            # args = ast.arguments(args=[ ast.arg('self') ], kwonlyargs=params, defaults=[], kw_defaults=params_defaults)
            body.append(PyFuncDef(
                name='__init__',
                params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='self')), PySepParam(), *params ]),
                return_type=PyNamedExpr(name='None'),
                body=init_body
            ))

            #for field in element.members:
            #     body.append(ast.AnnAssign(target=PyNamedExpr(name=field.name), annotation=gen_type(field.ty), simple=True))

            stmts.append(PyClassDef(name=to_class_name(spec.name), bases=list_comma([ '_BaseNode' ]), body=body))

            continue

        if isinstance(spec, TokenSpec):

            body: list[PyStmt] = []

            if spec.is_static:

                body.append(PyPassStmt())

            else:

                init_body: list[PyStmt] = []

                init_body.append(PyExprStmt(expr=PyCallExpr(operator=PyAttrExpr(expr=PyCallExpr(operator=PyNamedExpr(name='super')), name='__init__'), args=[ (PyKeywordArg(name='span', expr=PyNamedExpr(name='span')), None) ])))

                params: list[PyParam] = []
                params.append(PyNamedParam(pattern=PyNamedPattern(name='self')))

                # value: Field | None = None
                params.append(PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=make_union([ rule_type_to_py_type(spec.field_type), PyNamedExpr(name='None') ]), default=PyNamedExpr(name='None')))

                # span: Span | None = None
                params.append(PyNamedParam(pattern=PyNamedPattern(name='span'), annotation=make_union([ PyNamedExpr(name='Span'), PyNamedExpr(name='None') ]), default=PyNamedExpr(name='None')))

                init_body.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern(name='self'), name='value'), expr=PyNamedExpr(name='value')))

                body.append(PyFuncDef(name='__init__', params=list_comma(params), body=init_body))

            stmts.append(PyClassDef(name=to_class_name(spec.name), bases=list_comma([ '_BaseToken' ]), body=body))

            continue

        if isinstance(spec, VariantSpec):
            # ty = PyNamedExpr(name=to_class_case(element.members[0]))
            # for name in element.members[1:]:
            #     ty = ast.BinOp(left=ty, op=ast.BitOr(), right=PyNamedExpr(name=to_class_case(name)))

            cls_name = to_class_name(spec.name)

            assert(len(spec.members) > 0)
            py_type = PyConstExpr(literal=emit(make_union(PyNamedExpr(name=to_class_name(name)) for name in spec.members)))
            stmts.append(PyAssignStmt(pattern=PyNamedPattern(name=cls_name), annotation=PyNamedExpr(name='TypeAlias'), expr=py_type))

            params: list[PyParam] = []
            params.append(PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')))
            stmts.append(PyFuncDef(
                name=f'is_{namespace(spec.name)}',
                params=list_comma(params),
                return_type=PySubscriptExpr(expr=PyNamedExpr(name='TypeGuard'), slices=[ (PyNamedExpr(name=cls_name), None) ]),
                body=[
                    PyRetStmt(expr=make_or(gen_instance_check(name, PyNamedExpr(name='value')) for name in spec.members))
                ],
            ))

            continue

        assert_never(spec)

    node_names: list[str] = []
    token_names: list[str] = []
    for spec in specs:
        if isinstance(spec, TokenSpec):
            token_names.append(spec.name)
        elif isinstance(spec, NodeSpec):
            node_names.append(spec.name)

    stmts.append(PyAssignStmt(pattern=PyNamedPattern(name=token_class_name), expr=make_union(PyNamedExpr(name=to_class_name(name)) for name in token_names)))
    stmts.append(PyAssignStmt(pattern=PyNamedPattern(name=node_class_name), expr=make_union(PyNamedExpr(name=to_class_name(name)) for name in node_names)))
    stmts.append(PyAssignStmt(pattern=PyNamedPattern(name=syntax_class_name), expr=make_union([ PyNamedExpr(name=token_class_name), PyNamedExpr(name=node_class_name) ])))

    stmts.append(PyFuncDef(
        name=is_token_proc_name,
        params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')) ]),
        return_type=PySubscriptExpr(expr=PyNamedExpr(name='TypeGuard'), slices=list_comma([ PyNamedExpr(name=token_class_name) ])),
        body=PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name='_BaseToken') ])))
        # body=PyRetStmt(expr=make_or(PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name=to_class_name(name)) ])) for name in token_names))
    ))

    stmts.append(PyFuncDef(
        name=is_node_proc_name,
        params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')) ]),
        return_type=PySubscriptExpr(expr=PyNamedExpr(name='TypeGuard'), slices=list_comma([ PyNamedExpr(name=node_class_name) ])),
        body=PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name='_BaseNode') ])))
        # body=PyRetStmt(expr=make_or(PyCallExpr(operator=PyNamedExpr(name='isinstance'), args=list_comma([ PyNamedExpr(name='value'), PyNamedExpr(name=to_class_name(name)) ])) for name in node_names))
    ))

    stmts.append(PyFuncDef(
        name=is_syntax_name,
        params=list_comma([ PyNamedParam(pattern=PyNamedPattern(name='value'), annotation=PyNamedExpr(name='Any')) ]),
        body=PyRetStmt(expr=PyInfixExpr(
                 left=PyCallExpr(operator=PyNamedExpr(name=is_node_proc_name), args=list_comma([ PyNamedExpr(name='value') ])),
                 op='or',
                 right=PyCallExpr(operator=PyNamedExpr(name=is_token_proc_name), args=list_comma([ PyNamedExpr(name='value') ]))
        ))
    ))

    return emit(PyModule(stmts=stmts))

def visitor() -> str:

    generate_temporary = NameGenerator()

    proc_name = 'proc'
    syntax_param_name = 'node'

    def gen_proc_call(ty: Type, target: PyExpr) -> Generator[PyStmt, None, None]:
        if isinstance(ty, NoneType):
            yield PyPassStmt()
            return
        if isinstance(ty, TokenType) or isinstance(ty, NodeType):
            yield PyExprStmt(expr=PyCallExpr(operator=PyNamedExpr(name=proc_name), args=list_comma([ target ])))
            return
        if isinstance(ty, TupleType):
            for i, element_type in enumerate(ty.element_types):
                tmp = generate_temporary(prefix='element_')
                yield PyAssignStmt(pattern=PyNamedPattern(name=tmp), expr=PySubscriptExpr(expr=target, slices=list_comma([ PyConstExpr(literal=i) ])))
                yield from gen_proc_call(element_type, PyNamedExpr(name=tmp))
            return
        if isinstance(ty, ListType):
            element_name = generate_temporary(prefix='element_')
            yield PyForStmt(pattern=PyNamedPattern(name=element_name), expr=target, body=list(gen_proc_call(ty.element_type, PyNamedExpr(name=element_name))))
            return
        if isinstance(ty, UnionType):
            cases: list[Case] = []
            for element_type in ty.types:
                cases.append((
                    gen_shallow_test(element_type, target),
                    list(gen_proc_call(element_type, target))
                ))
            cases.append((None, [ PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ValueError'))) ]))
            yield from make_cond(cases)
            return
        raise RuntimeError(f'unexpected {ty}')

    body: list[PyStmt] = []

    body.append(PyIfStmt(first=PyIfCase(
        test=PyCallExpr(operator=PyNamedExpr(name=is_token_proc_name), args=list_comma([ PyNamedExpr(name=syntax_param_name) ])),
        body=PyRetStmt(),
    )))

    for spec in specs:

        # We're going to start a new scope, so all previous temporary names may be used once again
        generate_temporary.reset()

        if isinstance(spec, TokenSpec):
            continue
        if isinstance(spec, NodeSpec):
            if_body: list[PyStmt] = []
            for field in spec.members:
                if_body.extend(gen_proc_call(field.ty, PyAttrExpr(expr=PyNamedExpr(name=syntax_param_name), name=field.name)))
            if_body.append(PyRetStmt())
            body.append(PyIfStmt(first=PyIfCase(
                test=PyCallExpr(
                    operator=PyNamedExpr(name='isinstance'),
                    args=list_comma([
                        PyNamedExpr(name=syntax_param_name),
                        PyNamedExpr(name=to_class_name(spec.name))
                    ])
                ),
                body=if_body
            )))
            continue
        if isinstance(spec, VariantSpec):
            continue

        assert_never(spec)

    return emit(PyFuncDef(
        name=for_each_child_name,
        params=list_comma([
            PyNamedParam(
                pattern=PyNamedPattern(name=syntax_param_name),
                annotation=PyNamedExpr(name=syntax_class_name)
            ),
            PyNamedParam(
                pattern=PyNamedPattern(name=proc_name),
                annotation=PySubscriptExpr(expr=PyNamedExpr(name='Callable'), slices=list_comma([ PyListExpr(elements=list_comma([ PyNamedExpr(name=syntax_class_name) ])), PyNamedExpr(name='None') ]))
            )
        ]),
        body=body,
    ))

def lexer_logic() -> str:

    def make_set_predicate(element: CharSetElement, target: PyExpr) -> PyExpr:
        if isinstance(element, str):
            return PyInfixExpr(left=target, op='==', right=PyConstExpr(literal=element))
        if isinstance(element, tuple):
            low, high = element
            return PyInfixExpr(
                left=PyInfixExpr(left=PyCallExpr(operator=PyNamedExpr(name='ord'), args=list_comma([ target ])), op='>=', right=PyConstExpr(literal=ord(low))),
                op='and',
                right=PyInfixExpr(left=PyCallExpr(operator=PyNamedExpr(name='ord'), args=list_comma([ target ])), op='<=', right=PyConstExpr(literal=ord(high)))
            )
        assert_never(element)

    stmts: list[PyStmt] = []
    i = 0

    def visit(expr: Expr, rule_name: str) -> list[PyStmt]:
        nonlocal i
        out: list[PyStmt] = []
        if isinstance(expr, LitExpr):
            for ch in expr.text:
                ch_name = f'c_{i}'
                i += 1
                out.append(PyAssignStmt(pattern=PyNamedPattern(name=ch_name), expr=PyCallExpr(operator=PyAttrExpr(expr=PyNamedExpr(name='self'), name='_get_char'))))
                out.extend(make_cond([(
                    PyInfixExpr(left=PyNamedExpr(name=ch_name), op='!=', right=PyConstExpr(literal=ch)),
                    [
                        PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ScanError'), args=[]))
                    ]
                )]))
            return out
        if isinstance(expr, SeqExpr):
            out: list[PyStmt] = []
            for element in expr.elements:
                out.extend(visit(element, rule_name))
            return out
        if isinstance(expr, CharSetExpr):
            out: list[PyStmt] = []
            ch_name = f'c_{i}'
            i += 1
            out.append(PyAssignStmt(pattern=PyNamedPattern(name=ch_name), expr=PyCallExpr(operator=PyAttrExpr(expr=PyNamedExpr(name='self'), name='_get_char'))))
            out.extend(make_cond([(
                make_or(make_set_predicate(element, PyNamedExpr(name=ch_name)) for element in expr.elements),
                [
                    PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr(name='ScanError'), args=[]))
                ]
            )]))
            return out
        if isinstance(expr, RepeatExpr):
            if expr.max == POSINF:
                out: list[PyStmt] = []
                min_body = visit(expr.expr, rule_name)
                out.append(PyForStmt(
                    pattern=PyNamedPattern(name='_'),
                    expr=PyCallExpr(operator=PyNamedExpr(name='range'), args=list_comma([ PyConstExpr(literal=0), PyConstExpr(literal=expr.min) ])),
                    body=min_body
                ))
                out.append(PyWhileStmt(expr=PyNamedExpr(name='True'), body=[
                    #PyTryStmt(body=min_body, handlers=[ PyExceptHandler(expr=PyNamedExpr(name='ScanError'), body=[]) ]),
                ]))
                return out 
            else:
                out: list[PyStmt] = []
                min_body = visit(expr.expr, rule_name)
                out.append(PyForStmt(
                    pattern=PyNamedPattern(name='_'),
                    expr=PyCallExpr(operator=PyNamedExpr(name='range'), args=list_comma([ PyConstExpr(literal=0), PyConstExpr(literal=expr.min) ])),
                    body=min_body
                ))
                out.append(PyForStmt(
                    pattern=PyNamedPattern(name='_'),
                    expr=PyCallExpr(operator=PyNamedExpr(name='range'), args=list_comma([ PyConstExpr(literal=0), PyConstExpr(literal=expr.max - expr.min) ])),
                    body=[
                        #PyTryStmt(body=min_body, handlers=[ PyExceptHandler(expr=PyNamedExpr(name='ScanError')) ]),
                    ]
                ))
        if isinstance(expr, ChoiceExpr):
            out: list[PyStmt] = []
            # TODO
            return out
        raise RuntimeError(f'unexpected {expr}')

    for rule in grammar.rules:
        if not rule.is_token:
            continue
        if rule.expr is not None:
            stmts.extend(visit(rule.expr, rule.name))

    return emit(PyModule(stmts=stmts))

