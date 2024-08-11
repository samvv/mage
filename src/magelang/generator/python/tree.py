
from typing import assert_never

from .util import build_isinstance, build_or, build_union, gen_deep_test, gen_initializers, gen_py_type, namespaced, rule_type_to_py_type, to_class_name
from magelang.repr import *
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit

def generate_tree(
    specs: Specs,
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

    parent_nodes = dict[str, set[str]]()

    def name_to_type(name: str) -> Type:
        spec = specs.lookup(name)
        if isinstance(spec, VariantSpec):
            return VariantType(name)
        if isinstance(spec, NodeSpec):
            return NodeType(name)
        if isinstance(spec, TokenSpec):
            return TokenType(name)
        raise AssertionError()

    def get_parent_type(name: str) -> Type:
        if name not in parent_nodes:
            return NeverType()
        return UnionType(list(name_to_type(name) for name in parent_nodes[name]))

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

    stmts: list[PyStmt] = [
        PyImportFromStmt(PyAbsolutePath(PyQualName('typing')), aliases=[
            PyFromAlias('Any'),
            PyFromAlias('TypeGuard'),
            PyFromAlias('Never'),
            PyFromAlias('Sequence'),
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

            required: list[PyParam] = []
            optional: list[PyParam] = []

            for field in spec.members:

                out_name = f'{field.name}_out'
                assign: Callable[[PyExpr], PyStmt] = lambda value, name=out_name: PyAssignStmt(PyNamedPattern(name), value=value)
                param_type, param_stmts = gen_initializers(field.name, field.ty, field.name, assign, specs=specs, prefix=prefix)
                param_stmts.append(PyAssignStmt(
                    pattern=PyAttrPattern(
                        pattern=PyNamedPattern('self'),
                        name=field.name
                    ),
                    annotation=gen_py_type(field.ty, prefix),
                    value=PyNamedExpr(out_name)
                ))

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
                init_body.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern('self'), name='value'), value=PyNamedExpr('value')))

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
            value=build_union(PyNamedExpr(to_class_name(name, prefix)) for name in token_names)
        )
    )

    # Generates:
    #
    # Node = Foo | Bar | ...
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(node_type_name),
            value=build_union(PyNamedExpr(to_class_name(name, prefix)) for name in node_names)
        )
    )

    # Generates:
    #
    # Syntax = Token | Node
    stmts.append(
        PyAssignStmt(
            pattern=PyNamedPattern(syntax_type_name),
            value=build_union([ PyNamedExpr(token_type_name), PyNamedExpr(node_type_name) ])
        )
    )

    return PyModule(stmts=stmts)

