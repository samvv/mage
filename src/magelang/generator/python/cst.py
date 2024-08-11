
from typing import assert_never

from .util import Case, build_cond, build_is_none, build_isinstance, build_or, build_union, gen_deep_test, gen_py_type, gen_shallow_test, namespaced, rule_type_to_py_type, to_class_name
from magelang.repr import *
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit

def generate_cst(
    grammar: Grammar,
    prefix='',
    gen_parent_pointers=False
) -> PyModule:

    is_node_name = f'is_{namespaced('node', prefix)}'
    is_token_name = f'is_{namespaced('token', prefix)}'
    is_syntax_name = f'is_{namespaced('syntax', prefix)}'

    base_syntax_class_name = '_' + to_class_name('base_syntax', prefix)
    base_node_class_name = '_' + to_class_name('base_node', prefix)
    base_token_class_name = '_' + to_class_name('base_token', prefix)
    token_type_name = to_class_name('token', prefix)
    node_type_name = to_class_name('node', prefix)
    syntax_type_name = to_class_name('syntax', prefix)

    specs = grammar_to_specs(grammar)

    parent_nodes = dict[str, set[str]]()

    def get_parent_type(name: str) -> Type:
        if name not in parent_nodes:
            return NeverType()
        # FIXME NodeType does not correctly represent the parent. It could be a VariantType or TokenType.
        return UnionType(list(NodeType(name) for name in parent_nodes[name]))

    def add_to_parent_nodes(name: str, ty: Type) -> None:
        if isinstance(ty, VariantType):
            spec = specs.lookup(ty.name)
            assert(isinstance(spec, VariantSpec))
            for _, member_type in spec.members:
                add_to_parent_nodes(name, member_type)
            return
        if isinstance(ty, NodeType) or isinstance(ty, TokenType):
            spec = specs.lookup(ty.name)
            if spec.name not in parent_nodes:
                parent_nodes[spec.name] = set()
            parent_nodes[spec.name].add(name)
        elif isinstance(ty, TupleType):
            for element in ty.element_types:
                add_to_parent_nodes(name, element)
        elif isinstance(ty, ListType) or isinstance(ty, PunctType):
            add_to_parent_nodes(name, ty.element_type)
        elif isinstance(ty, UnionType):
            for element in ty.types:
                add_to_parent_nodes(name, element)
        elif isinstance(ty, NoneType) or isinstance(ty, ExternType) or isinstance(ty, NeverType):
            pass
        else:
            assert_never(ty)

    if gen_parent_pointers:
        for spec in specs:
            if not isinstance(spec, NodeSpec):
                continue
            for field in spec.members:
                add_to_parent_nodes(spec.name, field.ty)

    def is_default_constructible(ty: Type, allow_empty_sequences: bool = True) -> bool:
        visited = set()
        def visit(ty: Type, allow_empty_sequences: bool) -> bool:
            if isinstance(ty, ExternType):
                return False
            if isinstance(ty, NeverType):
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
                spec = specs.lookup(ty.name)
                assert(isinstance(spec, NodeSpec))
                return all(visit(field.ty, allow_empty_sequences) for field in spec.members)
            if isinstance(ty, TokenType):
                if ty.name in visited:
                    return False
                visited.add(ty.name)
                spec = specs.lookup(ty.name)
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

    def gen_default_constructor(ty: Type) -> PyExpr:
        if isinstance(ty, NoneType):
            return PyNamedExpr('None')
        if isinstance(ty, NodeType) or isinstance(ty, TokenType):
            return PyCallExpr(operator=PyNamedExpr(to_class_name(ty.name, prefix)))
        if isinstance(ty, ListType):
            return PyCallExpr(operator=PyNamedExpr('list'))
        if isinstance(ty, PunctType):
            # FIXME maybe add the generic arguments?
            return PyCallExpr(operator=PyNamedExpr('Punctuated'))
        if isinstance(ty, TupleType):
            return PyTupleExpr(elements=list(gen_default_constructor(element_type) for element_type in ty.element_types))
        if isinstance(ty, UnionType):
            # This assumes we already detected that there is exactly one
            # default-constrcuctible member in the union type
            for ty in ty.types:
                if is_default_constructible(ty):
                    return gen_default_constructor(ty)
        raise RuntimeError(f'unexpected {ty}')

    def gen_initializers(field_name: str, field_type: Type, in_name: str, assign: Callable[[PyExpr], PyStmt]) -> tuple[Type, list[PyStmt]]:

        def collect(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], forbid_none: bool) -> tuple[Type, list[PyStmt]]:

            cases: list[Case] = []
            types: list[Type] = []
            for coerce_ty, coerce_body in coercions(ty, in_name, assign, forbid_none):
                cases.append((gen_shallow_test(coerce_ty, PyNamedExpr(in_name), prefix), coerce_body))
                types.append(coerce_ty)

            res_ty = simplify_type(UnionType(types))

            # For very simple fields, there's no need to do any checks. We
            # assume the type checker catches whatever error the user makes.
            if len(cases) == 1:
                return res_ty, cases[0][1]

            cases.append((
                None,
                [
                    PyRaiseStmt(
                        expr=PyCallExpr(
                            operator=PyNamedExpr('ValueError'),
                            args=[ PyConstExpr(f"the field '{field_name}' received an unrecognised value'") ]
                        )
                    )
                ]
            ))

            return res_ty, build_cond(cases)

        def coercions(ty: Type, in_name: str, assign: Callable[[PyExpr], PyStmt], forbid_none: bool) -> Generator[tuple[Type, list[PyStmt]], None, None]:

            if isinstance(ty, UnionType):

                types = list(flatten_union(ty))

                for element_type in types:
                    if isinstance(element_type, NoneType):
                        forbid_none = True

                rejected = set()
                out = []
                for element_type in types:
                    for coerced_type, coerced_stmts in coercions(element_type, in_name, assign, True):
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
                yield NoneType(), [ assign(gen_default_constructor(ty)) ]
                return

            # Now that we've handled union types and empty types, we can
            # attempt to construct the type from a certain default value.
            # This can only happen if `None` is not already used by the type
            # itself. We continue processing the other types after this
            # operation.
            if not forbid_none and is_default_constructible(ty):
                yield NoneType(), [ assign(gen_default_constructor(ty)) ]

            if isinstance(ty, VariantType):
                yield ty, [ assign(PyNamedExpr(in_name)) ]
                return

            if isinstance(ty, NodeType):

                spec = specs.lookup(ty.name)
                assert(isinstance(spec, NodeSpec))

                optional_fields: list[Field] = []
                required_fields: list[Field] = []

                for field in spec.members:
                    if is_default_constructible(field.ty):
                        optional_fields.append(field)
                    else:
                        required_fields.append(field)

                if len(required_fields) == 0:

                    if not forbid_none:
                        yield NoneType(), [
                            assign(PyCallExpr(PyNamedExpr(to_class_name(ty.name, prefix))))
                        ]

                elif len(required_fields) == 1:

                    required_type = required_fields[0].ty

                    def new_assign(value):
                        return assign(
                            PyCallExpr(
                                operator=PyNamedExpr(to_class_name(ty.name, prefix)),
                                args=[ value ]
                            )
                        )

                    yield from coercions(required_type, in_name, new_assign, forbid_none)

                yield ty, [ assign(PyNamedExpr(in_name)) ]

                return

            if isinstance(ty, TokenType):

                spec = specs.lookup(ty.name)
                assert(isinstance(spec, TokenSpec))

                # If a token is not static, like an identifier or a string,
                # then we might be able to coerce the token based on the data
                # that it wraps.
                if not spec.is_static:

                    yield ExternType(spec.field_type), [
                        assign(
                            PyCallExpr(
                                operator=PyNamedExpr(to_class_name(ty.name, prefix)),
                                args=[ PyNamedExpr(in_name) ]
                            )
                        )
                    ]

                yield ty, [ assign(PyNamedExpr(in_name)) ]

                return

            if isinstance(ty, PunctType):

                assert(is_default_constructible(ty.separator_type))

                new_elements_name = f'new_{in_name}'

                if is_static(ty.element_type, grammar):
                    yield ExternType(integer_rule_type), [
                        PyAssignStmt(PyNamedPattern(new_elements_name), expr=PyCallExpr(PyNamedExpr('Punctuated'))),
                        PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyNamedExpr(in_name) ]), body= [
                            PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(new_elements_name), 'append'), args=[ gen_default_constructor(ty.element_type) ])),
                        ]),
                        assign(PyNamedExpr(new_elements_name)),
                    ]

                first_element_name = f'first_{in_name}_element'
                second_element_name = f'second_{in_name}_element'
                element_name = f'{in_name}_element'
                elements_iter_name = f'{in_name}_iter'
                value_name = f'{in_name}_value'
                new_value_name = f'new_{in_name}_value'
                separator_name = f'{in_name}_separator'
                new_separator_name = f'new_{in_name}_separator'

                value_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_value_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
                value_type, value_stmts = collect(ty.element_type, value_name, value_assign, True)

                separator_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_separator_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
                separator_type, separator_stmts = collect(ty.separator_type, separator_name, separator_assign, True)

                coerced_ty = UnionType([
                    ListType(value_type, ty.required),
                    ListType(TupleType([ value_type, make_optional(separator_type) ]), ty.required),
                    PunctType(value_type, make_optional(separator_type), ty.required),
                ])

                yield coerced_ty, [
                    PyAssignStmt(
                        pattern=PyNamedPattern(new_elements_name),
                        expr=PyCallExpr(operator=PyNamedExpr('Punctuated'))
                    ),
                    PyAssignStmt(
                        pattern=PyNamedPattern(elements_iter_name),
                        expr=PyCallExpr(operator=PyNamedExpr('iter'), args=[ PyNamedExpr(in_name) ]),
                    ),
                    PyTryStmt(
                        body=[
                            PyAssignStmt(
                                pattern=PyNamedPattern(first_element_name),
                                expr=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                            ),
                            PyWhileStmt(
                                expr=PyNamedExpr('True'),
                                body=[
                                    PyTryStmt(
                                        body=[
                                            PyAssignStmt(
                                                pattern=PyNamedPattern(second_element_name),
                                                expr=PyCallExpr(operator=PyNamedExpr('next'), args=[ PyNamedExpr(elements_iter_name) ])
                                            ),
                                            *build_cond([
                                                (
                                                    # FIXME does not handle nested tuples
                                                    build_isinstance(PyNamedExpr(first_element_name), PyNamedExpr('tuple')),
                                                    [
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(value_name),
                                                            expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=0) ]),
                                                        ),
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(separator_name),
                                                            expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(literal=1) ]),
                                                        ),
                                                    ]
                                                ),
                                                (
                                                    None,
                                                    [
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(value_name),
                                                            expr=PyNamedExpr(first_element_name),
                                                        ),
                                                        PyAssignStmt(
                                                            pattern=PyNamedPattern(separator_name),
                                                            expr=gen_default_constructor(ty.separator_type),
                                                        ),
                                                    ]
                                                )
                                            ]),
                                            *value_stmts,
                                            *separator_stmts,
                                            PyExprStmt(
                                                expr=PyCallExpr(
                                                    operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'append'),
                                                    args=[
                                                        PyNamedExpr(new_value_name),
                                                        PyNamedExpr(new_separator_name)
                                                    ]
                                                )
                                            ),
                                            PyAssignStmt(
                                                pattern=PyNamedPattern(first_element_name),
                                                expr=PyNamedExpr(second_element_name),
                                            ),
                                        ],
                                        handlers=[
                                            PyExceptHandler(
                                                expr=PyNamedExpr('StopIteration'),
                                                body=[
                                                    *build_cond([
                                                        (
                                                            # FIXME does not handle nested tuples
                                                            build_isinstance(PyNamedExpr(first_element_name), PyNamedExpr('tuple')),
                                                            [
                                                                PyAssignStmt(
                                                                    pattern=PyNamedPattern(value_name),
                                                                    expr=PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(0) ]),
                                                                ),
                                                                PyExprStmt(
                                                                    expr=PyCallExpr(
                                                                        operator=PyNamedExpr('assert'),
                                                                        args=[ build_is_none(PySubscriptExpr(expr=PyNamedExpr(first_element_name), slices=[ PyConstExpr(1) ])) ]
                                                                    )
                                                                )
                                                            ]
                                                        ),
                                                        (
                                                            None,
                                                            [
                                                                PyAssignStmt(
                                                                    pattern=PyNamedPattern(value_name),
                                                                    expr=PyNamedExpr(first_element_name),
                                                                )
                                                            ]
                                                        )
                                                    ]),
                                                    *value_stmts,
                                                    PyExprStmt(
                                                        expr=PyCallExpr(
                                                            operator=PyAttrExpr(PyNamedExpr(new_elements_name), 'append'),
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
                    assign(PyNamedExpr(new_elements_name))
                ]

                return

            if isinstance(ty, ListType):

                # Generates:
                #
                # out_name = list()
                # for element in in_name:
                #     ...
                #     out_name.append(new_element_name)

                new_elements_name = f'new_{in_name}'

                if is_static(ty.element_type, grammar):
                    yield ExternType(integer_rule_type), [
                        PyAssignStmt(PyNamedPattern(new_elements_name), expr=PyCallExpr(PyNamedExpr('list'))),
                        PyForStmt(PyNamedPattern('_'), PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyNamedExpr(in_name) ]), body= [
                            PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(new_elements_name), 'append'), args=[ gen_default_constructor(ty.element_type) ])),
                        ]),
                        assign(PyNamedExpr(new_elements_name)),
                    ]

                element_name = f'{in_name}_element'
                new_element_name = f'new_{in_name}_element'

                element_assign: Callable[[PyExpr], PyStmt] = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)
                element_type, element_stmts = collect(ty.element_type, element_name, element_assign, True)

                yield ListType(element_type, ty.required), [
                    PyAssignStmt(
                        pattern=PyNamedPattern(new_elements_name),
                        expr=PyCallExpr(operator=PyNamedExpr('list'))
                    ),
                    PyForStmt(
                        pattern=PyNamedPattern(element_name),
                        expr=PyNamedExpr(in_name),
                        body=[
                            *element_stmts,
                            PyExprStmt(
                                expr=PyCallExpr(
                                    operator=PyAttrExpr(
                                        expr=PyNamedExpr(new_elements_name),
                                        name='append'
                                    ),
                                    args=[ PyNamedExpr(new_element_name) ]
                                )
                            )
                        ]
                    ),
                    assign(PyNamedExpr(new_elements_name))
                ]

                return

            if isinstance(ty, TupleType):

                # Generates:
                #
                # element_0 = field[0]
                # new_element_0 = ...
                # ...
                # out_name = (new_element_0, new_element_1, ...)

                required: list[Type] = []

                for element_type in ty.element_types:
                    if not is_default_constructible(element_type, allow_empty_sequences=False):
                        required.append(element_type)

                if len(required) == 1:

                    main_type = required[0]

                    def first_assign(value: PyExpr):
                        assert(isinstance(ty, TupleType)) # Needed to keep Pyright happy
                        # Generates for example: self.field = (Dot(), $value, Dot())
                        return assign(
                            PyTupleExpr(
                                elements=list(value if el_ty == main_type else gen_default_constructor(el_ty) for el_ty in ty.element_types)
                            )
                        )

                    yield from coercions(main_type, in_name, first_assign, True)

                new_elements: list[PyExpr] = []
                new_element_types: list[Type] = []

                # Generates for example: assert(isinstance(in_name, ty))
                orelse: list[PyStmt] = [
                    PyExprStmt(
                        expr=PyCallExpr(
                            operator=PyNamedExpr('assert'),
                            args=[ gen_shallow_test(ty, PyNamedExpr(in_name), prefix) ]
                        )
                    )
                ]

                for i, element_type in enumerate(ty.element_types):

                    element_name = f'{in_name}_{i}'
                    new_element_name = f'new_{in_name}_{i}'
                    element_assign = lambda value, name=new_element_name: PyAssignStmt(pattern=PyNamedPattern(name), expr=value)

                    new_elements.append(PyNamedExpr(new_element_name))

                    orelse.append(
                        PyAssignStmt(
                            pattern=PyNamedPattern(element_name),
                            expr=PySubscriptExpr(
                                expr=PyNamedExpr(in_name),
                                slices=[ PyConstExpr(literal=i) ]
                            )
                        )
                    )

                    new_element_type, new_element_stmts = collect(element_type, element_name, element_assign, False)

                    orelse.extend(new_element_stmts)

                    new_element_types.append(new_element_type)

                orelse.append(assign(PyTupleExpr(elements=new_elements)))

                yield TupleType(new_element_types), orelse

                return

        return collect(field_type, in_name, assign, False)

    stmts: list[PyStmt] = [
        PyImportFromStmt(PyAbsolutePath(PyQualName('typing')), aliases=[
            PyFromAlias('Any'),
            PyFromAlias('TypeGuard'),
            PyFromAlias('Never'),
        ]),
        PyImportFromStmt(PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')), aliases=[
            PyFromAlias('BaseNode'),
            PyFromAlias('BaseToken'),
            PyFromAlias('Punctuated'),
            PyFromAlias('Span'),
        ]),
        PyClassDef(base_node_class_name, bases=[ 'BaseNode' ], body=[
            PyPassStmt(),
        ]),
        PyClassDef(base_token_class_name, bases=[ 'BaseToken' ], body=[
            PyPassStmt(),
        ]),
        # def is_foo_token(value: Any) -> TypeGuard[FooToken]:
        #     return isinstance(value, BaseFooToken)
        PyFuncDef(
            is_token_name,
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeGuard'), slices=[ PyConstExpr(token_type_name) ]),
            body=[
                PyRetStmt(expr=build_isinstance(PyNamedExpr('value'), PyNamedExpr(base_token_class_name))),
            ]
        ),
        # def is_foo_node(value: Any) -> TypeGuard[FooNode]:
        #     return isinstance(value, BaseFooNode)
        PyFuncDef(
            is_node_name,
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeGuard'), slices=[ PyConstExpr(node_type_name) ]),
            body=[
                PyRetStmt(expr=build_isinstance(PyNamedExpr('value'), PyNamedExpr(base_node_class_name))),
            ]
        ),
        # def is_foo_syntax(value: Any) -> TypeGuard[FooSyntax]:
        #     return isinstance(value, BaseFooSyntax)
        PyFuncDef(
            is_syntax_name,
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeGuard'), slices=[ PyConstExpr(syntax_type_name) ]),
            body=[
                PyRetStmt(expr=PyInfixExpr(
                    PyCallExpr(PyNamedExpr(is_node_name), args=[ PyNamedExpr('value') ]),
                    PyOrKeyword(),
                    PyCallExpr(PyNamedExpr(is_token_name), args=[ PyNamedExpr('value') ]),
                )),
            ]
        ),
    ]

    for spec in specs:

        if isinstance(spec, NodeSpec):

            body: list[PyStmt] = []
            params: list[PyParam] = []
            init_body: list[PyStmt] = []

            required = []
            optional = []

            for field in spec.members:

                out_name = f'{field.name}_out'
                assign: Callable[[PyExpr], PyStmt] = lambda value, name=out_name: PyAssignStmt(PyNamedPattern(name), value)
                param_type, param_stmts = gen_initializers(field.name, field.ty, field.name, assign)
                param_stmts.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern('self'), name=field.name), annotation=gen_py_type(field.ty, prefix), expr=PyNamedExpr(out_name)))

                init_body.extend(param_stmts)

                param_type_str = emit(gen_py_type(param_type, prefix))

                if is_optional(param_type):
                    optional.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=PyConstExpr(literal=param_type_str),
                        default=PyNamedExpr('None')
                    ))
                else:
                    required.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=PyConstExpr(param_type_str),
                    ))

                if isinstance(field.ty, PunctType) or isinstance(field.ty, ListType):
                    body.append(PyFuncDef(
                        name=f'count_{field.name}',
                        params=[ PyNamedParam(PyNamedPattern('self')) ],
                        return_type=PyNamedExpr('int'),
                        body=[
                            PyRetStmt(expr=PyCallExpr(PyNamedExpr('len'), args=[ PyAttrExpr(PyNamedExpr('self'), field.name) ])),
                        ]
                    ))

            params.extend(required)
            if optional:
                params.append(PySepParam())
                params.extend(optional)

            body.append(PyFuncDef(
                name='__init__',
                params=[ PyNamedParam(pattern=PyNamedPattern('self')), *params ],
                return_type=PyNamedExpr('None'),
                body=init_body
            ))

            if gen_parent_pointers:
                parent_type = get_parent_type(spec.name)
                parent_type_name = f'{to_class_name(spec.name, prefix)}Parent'
                stmts.append(PyTypeAliasStmt(parent_type_name, gen_py_type(parent_type, prefix)))
                get_parent_body = []
                if isinstance(parent_type, NeverType):
                    get_parent_body.append(PyRaiseStmt(PyCallExpr(PyNamedExpr('AssertionError'), args=[ PyConstExpr('trying to access the parent node of a top-level node') ])))
                else:
                    get_parent_body.append(PyCallExpr(PyNamedExpr('assert'), args=[ PyInfixExpr(PyAttrExpr(PyNamedExpr('self'), '_parent'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')) ]))
                    get_parent_body.append(PyRetStmt(expr=PyAttrExpr(PyNamedExpr('self'), '_parent')))
                body.append(PyFuncDef(
                    decorators=[ PyDecorator(PyNamedExpr('property')) ],
                    name='parent',
                    params=[ PyNamedParam(PyNamedPattern('self')) ],
                    return_type=PyNamedExpr(parent_type_name),
                    body=get_parent_body,
                ))

            stmts.append(PyClassDef(name=to_class_name(spec.name, prefix), bases=[ base_node_class_name ], body=body))

            continue

        if isinstance(spec, TokenSpec):

            body: list[PyStmt] = []

            if spec.is_static:

                body.append(PyPassStmt())

            else:

                init_body: list[PyStmt] = []

                init_body.append(PyExprStmt(expr=PyCallExpr(operator=PyAttrExpr(expr=PyCallExpr(operator=PyNamedExpr('super')), name='__init__'), args=[ (PyKeywordArg(name='span', expr=PyNamedExpr('span')), None) ])))

                params: list[PyParam] = []

                # self
                params.append(PyNamedParam(pattern=PyNamedPattern('self')))

                # value: Type
                params.append(PyNamedParam(pattern=PyNamedPattern('value'), annotation=rule_type_to_py_type(spec.field_type)))

                # span: Span | None = None
                params.append(PyNamedParam(pattern=PyNamedPattern('span'), annotation=build_union([ PyNamedExpr('Span'), PyNamedExpr('None') ]), default=PyNamedExpr('None')))

                # self.value = value
                init_body.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern('self'), name='value'), expr=PyNamedExpr('value')))

                body.append(PyFuncDef(name='__init__', params=params, body=init_body))

            stmts.append(PyClassDef(name=to_class_name(spec.name, prefix), bases=[ base_token_class_name ], body=body))

            continue

        if isinstance(spec, VariantSpec):
            # ty = PyNamedExpr(to_class_case(element.members[0]))
            # for name in element.members[1:]:
            #     ty = ast.BinOp(left=ty, op=ast.BitOr(), right=PyNamedExpr(to_class_case(name)))

            cls_name = to_class_name(spec.name, prefix)

            assert(len(spec.members) > 0)
            stmts.append(PyTypeAliasStmt(cls_name, build_union(gen_py_type(ty, prefix) for _, ty in spec.members)))

            params: list[PyParam] = []
            params.append(PyNamedParam(pattern=PyNamedPattern('value'), annotation=PyNamedExpr('Any')))
            stmts.append(PyFuncDef(
                name=f'is_{namespaced(spec.name, prefix)}',
                params=params,
                return_type=PySubscriptExpr(expr=PyNamedExpr('TypeGuard'), slices=[ PyNamedExpr(cls_name) ]),
                body=[
                    PyRetStmt(expr=build_or(gen_deep_test(ty, PyNamedExpr('value'), prefix=prefix) for _, ty in spec.members))
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

    # Generates:
    #
    # Token = Comma | Dot | Ident | ...
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(token_type_name),
            expr=build_union(PyNamedExpr(to_class_name(name, prefix)) for name in token_names)
        )
    )

    # Generates:
    #
    # Node = Foo | Bar | ...
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(node_type_name),
            expr=build_union(PyNamedExpr(to_class_name(name, prefix)) for name in node_names)
        )
    )

    # Generates:
    #
    # Syntax = Token | Node
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(syntax_type_name),
            expr=build_union([ PyNamedExpr(token_type_name), PyNamedExpr(node_type_name) ])
        )
    )

    return PyModule(stmts=stmts)

