
from typing import Iterable, assert_never

from magelang.passes.mage_insert_magic_rules import any_node_rule_name, any_token_rule_name, any_syntax_rule_name
from magelang.helpers import make_py_cond, make_py_or, make_py_union, treespec_type_to_deep_py_test, make_py_coercions, treespec_type_to_py_type, treespec_type_to_shallow_py_test, namespaced, extern_type_to_py_type, to_py_class_name, quote_py_type, make_py_isinstance, PyCondCase, lookup_spec
from magelang.lang.treespec.helpers import contains_type, expand_variant_types, is_self_referential, is_optional_type, is_type_assignable, resolve_type_references, spec_to_type
from magelang.lang.mage.ast import *
from magelang.lang.treespec.ast import *
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit
from magelang.util import NameGenerator

def make_py_optional(ty: PyExpr) -> PyExpr:
    return PyInfixExpr(ty, PyVerticalBar(), PyNamedExpr('None'))

def make_py_return(expr: PyExpr) -> PyStmt:
    return PyRetStmt(expr=expr)

def treespec_to_python(
    specs: Specs,
    prefix: str = '',
    gen_parent_pointers: bool = True,
    enable_asserts: bool = False,
) -> PyModule:

    def get_base_class_name(name: str) -> str:
        return '_' + to_py_class_name('base_' + name, prefix=prefix)

    base_syntax_class_name = get_base_class_name(any_syntax_rule_name)
    base_node_class_name =  get_base_class_name(any_node_rule_name)
    base_token_class_name = get_base_class_name(any_token_rule_name)

    parent_nodes = dict[str, set[str]]()

    def get_parent_type(name: str) -> Type:
        if name not in parent_nodes:
            return NeverType()
        return UnionType(list(SpecType(name) for name in sorted(parent_nodes[name])))

    def add_to_parent_nodes(name: str, ty: Type) -> None:
        ty = resolve_type_references(ty, specs=specs)
        if isinstance(ty, SpecType):
            spec = lookup_spec(specs, ty.name)
            assert(not isinstance(spec, TypeSpec))
            if spec is None or isinstance(spec, ConstEnumSpec):
                return
            if isinstance(spec, EnumSpec):
                for member in spec.members:
                    add_to_parent_nodes(name, member.ty)
                return
            if isinstance(spec, NodeSpec) or isinstance(spec, TokenSpec):
                if spec.name not in parent_nodes:
                    parent_nodes[ty.name] = set()
                parent_nodes[spec.name].add(name)
                return
            assert_never(spec)
        elif isinstance(ty, TupleType):
            for element in ty.element_types:
                add_to_parent_nodes(name, element)
        elif isinstance(ty, ListType) or isinstance(ty, PunctType):
            add_to_parent_nodes(name, ty.element_type)
        elif isinstance(ty, UnionType):
            for element in ty.types:
                add_to_parent_nodes(name, element)
        elif isinstance(ty, NoneType) or isinstance(ty, ExternType) or isinstance(ty, NeverType) or isinstance(ty, AnyType):
            pass
        else:
            assert_never(ty)

    if gen_parent_pointers:
        for spec in specs.elements:
            if not isinstance(spec, NodeSpec):
                continue
            for field in spec.fields:
                add_to_parent_nodes(spec.name, field.ty)

    stmts: list[PyStmt] = [
        PyImportFromStmt(PyAbsolutePath('enum'), aliases=[
            'IntEnum',
        ]),
        PyImportFromStmt(PyAbsolutePath('typing'), aliases=[
            'Any',
            'TypeGuard',
            'TypeIs',
            'TypedDict',
            'Never',
            'Unpack',
            'Sequence',
            'Callable',
            'assert_never',
            'no_type_check',
        ]),
        PyImportFromStmt(PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')), aliases=[
            'BaseSyntax',
            'Punctuated',
            'ImmutablePunct',
            'Span',
        ]),
        PyClassDef(base_syntax_class_name, bases=[ PyClassBaseArg('BaseSyntax') ], body=[
            PyPassStmt(),
        ]),
        PyClassDef(base_node_class_name, bases=[ PyClassBaseArg(base_syntax_class_name) ], body=[
            PyPassStmt(),
        ]),
        PyClassDef(base_token_class_name, bases=[ PyClassBaseArg(base_syntax_class_name) ], body=[
            PyFuncDef(
                name='__init__',
                params=[ PyNamedParam(PyNamedPattern('self')), PyNamedParam(PyNamedPattern('span'), annotation=make_py_optional(PyNamedExpr('Span')), default=PyNamedExpr('None')) ],
                body=[ PyAssignStmt(PyAttrPattern(PyNamedPattern('self'), 'span'), value=PyNamedExpr('span')) ]
            ),
        ]),
    ]

    defs = {}

    # Generate token classes

    for spec in specs.elements:

        if not isinstance(spec, TokenSpec):
            continue

        body: list[PyStmt] = []

        if spec.is_static:

            body.append(PyPassStmt())

        else:

            init_body: list[PyStmt] = []

            init_body.append(PyExprStmt(expr=PyCallExpr(operator=PyAttrExpr(expr=PyCallExpr(operator=PyNamedExpr('super')), name='__init__'), args=[ (PyKeywordArg(name='span', expr=PyNamedExpr('span')), None) ])))

            init_params: list[PyParam] = []

            # self
            init_params.append(PyNamedParam(pattern=PyNamedPattern('self')))

            # value: Type
            init_params.append(PyNamedParam(pattern=PyNamedPattern('value'), annotation=extern_type_to_py_type(spec.field_type)))

            # span: Span | None = None
            init_params.append(PyNamedParam(pattern=PyNamedPattern('span'), annotation=make_py_union([ PyNamedExpr('Span'), PyNamedExpr('None') ]), default=PyNamedExpr('None')))

            # self.value = value
            init_body.append(PyAssignStmt(pattern=PyAttrPattern(pattern=PyNamedPattern('self'), name='value'), value=PyNamedExpr('value')))

            body.append(PyFuncDef(name='__init__', params=init_params, body=init_body))

        stmts.append(PyClassDef(name=to_py_class_name(spec.name, prefix), bases=[ PyClassBaseArg(base_token_class_name) ], body=body))

    # Generate node classes

    for spec in specs.elements:

        if not isinstance(spec, NodeSpec):
            continue

        this_class_name = to_py_class_name(spec.name, prefix)
        derive_kwargs_class_name = to_py_class_name(spec.name + '_derive_kwargs', prefix)

        body: list[PyStmt] = []

        init_params: list[PyParam] = []
        init_body: list[PyStmt] = []

        derive_kwargs_body = []
        derive_body = []
        derive_args = []

        # derive_overload_params: list[PyParam] = [
        #     PyNamedParam(PyNamedPattern('self')),
        #     PyKwSepParam(),
        # ]

        required_params: list[PyParam] = []
        optional_params: list[PyParam] = []

        for field in spec.fields:

            type_with_coercions, coerce_fn = make_py_coercions(field.ty, defs=defs, specs=specs, prefix=prefix)
            init_body.append(PyAssignStmt(
                pattern=PyAttrPattern(
                    pattern=PyNamedPattern('self'),
                    name=field.name
                ),
                annotation=treespec_type_to_py_type(field.ty, prefix),
                value=PyCallExpr(coerce_fn, args=[ PyNamedExpr(field.name) ]),
            ))

            param_type = type_with_coercions

            param_type_str = emit(treespec_type_to_py_type(param_type, prefix=prefix, immutable=True))

            if is_optional_type(param_type):
                optional_params.append(PyNamedParam(
                    pattern=PyNamedPattern(field.name),
                    annotation=PyConstExpr(literal=param_type_str),
                    default=PyNamedExpr('None')
                ))
            else:
                required_params.append(PyNamedParam(
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

            derive_kwargs_body.append(PyAssignStmt(
                pattern=PyNamedPattern(field.name),
                annotation=quote_py_type(treespec_type_to_py_type(param_type, prefix=prefix, immutable=True)),
            ))
            derive_args.append(PyKeywordArg(field.name, PyNamedExpr(field.name)))
            derive_body.append(PyAssignStmt(
                PyNamedPattern(field.name),
                value=PyIfExpr(
                    PyCallExpr(coerce_fn, args=[ PySubscriptExpr(PyNamedExpr('kwargs'), [ PyConstExpr(field.name) ]) ]),
                    PyInfixExpr(PyConstExpr(field.name), PyInKeyword(), PyNamedExpr('kwargs')),
                    PyAttrExpr(PyNamedExpr('self'), field.name)
                )
            ))

        if not spec.fields:
            init_body.append(PyPassStmt())
            derive_kwargs_body.append(PyPassStmt())

        init_params.extend(required_params)
        if optional_params:
            init_params.append(PyKwSepParam())
            init_params.extend(optional_params)

        body.append(PyFuncDef(
            name='__init__',
            params=[ PyNamedParam(pattern=PyNamedPattern('self')), *init_params ],
            return_type=PyNamedExpr('None'),
            body=init_body
        ))

        stmts.append(PyClassDef(
            name=derive_kwargs_class_name,
            bases=[ PyClassBaseArg('TypedDict'), PyKeywordBaseArg('total', PyNamedExpr('False')) ],
            body=derive_kwargs_body
        ))

        derive_body.append(PyRetStmt(expr=PyCallExpr(PyNamedExpr(this_class_name), args=derive_args)))

        derive_decorators = []
        if not enable_asserts:
            derive_decorators.append(PyDecorator(PyNamedExpr('no_type_check')))
        body.append(PyFuncDef(
             decorators=derive_decorators,
             name='derive',
             params=[ PyNamedParam(PyNamedPattern('self')), PyRestKeywordParam('kwargs', annotation=PySubscriptExpr(PyNamedExpr('Unpack'), [ PyNamedExpr(derive_kwargs_class_name) ])) ],
             return_type=PyConstExpr(this_class_name),
             body=derive_body,
         ))

        if gen_parent_pointers:
            parent_type_name = f'{to_py_class_name(spec.name, prefix)}Parent'
            # body.append(PyAssignStmt(PyNamedPattern('parent'), annotation=PyConstExpr(parent_type_name)))
            parent_type = get_parent_type(spec.name)
            parent_type_name = f'{to_py_class_name(spec.name, prefix)}Parent'
            # stmts.append(PyTypeAliasStmt(parent_type_name, gen_py_type(parent_type, prefix)))
            get_parent_body = []
            if isinstance(parent_type, NeverType):
                get_parent_body.append(PyRaiseStmt(PyCallExpr(PyNamedExpr('AssertionError'), args=[ PyConstExpr('trying to access the parent node of a top-level node') ])))
            else:
                get_parent_body.append(PyCallExpr(PyNamedExpr('assert'), args=[ PyInfixExpr(PyAttrExpr(PyNamedExpr('self'), '_parent'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')) ]))
                get_parent_body.append(PyRetStmt(expr=PyAttrExpr(PyNamedExpr('self'), '_parent')))
            body.append(PyFuncDef(
                #decorators=[ PyDecorator(PyNamedExpr('property')) ],
                name='parent',
                params=[ PyNamedParam(PyNamedPattern('self')) ],
                return_type=PyConstExpr(parent_type_name),
                body=get_parent_body,
            ))

        stmts.append(PyClassDef(name=this_class_name, bases=[ PyClassBaseArg(base_node_class_name) ], body=body))

    # Generate constant enumerations

    for spec in specs.elements:

        if not isinstance(spec, ConstEnumSpec):
            continue

        stmts.append(PyClassDef(
            name=to_py_class_name(spec.name, prefix=prefix),
            bases=[ PyClassBaseArg('IntEnum') ],
            body=list(PyAssignStmt(PyNamedPattern(name), value=PyConstExpr(i)) for name, i in spec.members)
        ))

    # Generate type aliases

    for spec in specs.elements:

        if not isinstance(spec, TypeSpec):
            continue

        stmts.append(PyTypeAliasStmt(
            name=to_py_class_name(spec.name, prefix=prefix),
            expr=treespec_type_to_py_type(spec.ty, prefix=prefix),
        ))

    # Generate variant classes and base classes

    for spec in specs.elements:

        if not isinstance(spec, EnumSpec):
            continue

        type_name = to_py_class_name(spec.name, prefix)

        stmts.append(PyTypeAliasStmt(type_name, make_py_union(treespec_type_to_py_type(member.ty, prefix) for member in spec.members)))

        pred_params: Sequence[PyParam] = [
            PyNamedParam(pattern=PyNamedPattern('value'), annotation=PyNamedExpr('Any'))
        ]

        # if is_cyclic(spec.name, specs=specs):
        #     base_class_name = get_base_class_name(spec.name)
        #     if spec.name not in [ any_node_rule_name, any_token_rule_name, any_syntax_rule_name ]:
        #         stmts.append(PyClassDef(
        #             name=base_class_name,
        #             bases=[ PyClassBaseArg(base_node_class_name) ],
        #             body=[ PyPassStmt() ]
        #         ))
        #     pred_expr = build_isinstance(PyNamedExpr('value'), PyNamedExpr(base_class_name))
        # else:
        pred_expr = make_py_or(treespec_type_to_deep_py_test(member.ty, PyNamedExpr('value'), prefix=prefix, specs=specs) for member in spec.members)

        stmts.append(PyFuncDef(
            name=f'is_{namespaced(spec.name, prefix)}',
            params=pred_params,
            return_type=PySubscriptExpr(expr=PyNamedExpr('TypeIs'), slices=[ PyNamedExpr(type_name) ]),
            body=[ PyRetStmt(expr=pred_expr) ],
        ))

    # Generate type aliases for parent fields

    if gen_parent_pointers:
        for spec in specs.elements:
            if not isinstance(spec, NodeSpec):
                continue
            parent_type = get_parent_type(spec.name)
            parent_type_name = f'{to_py_class_name(spec.name, prefix)}Parent'
            stmts.append(PyTypeAliasStmt(parent_type_name, treespec_type_to_py_type(parent_type, prefix)))

    # Add coercers and other generated helpers

    stmts.extend(defs.values())

    # Generate visitors

    proc_param_name = 'proc'
    node_param_name = 'node'

    def is_type_reachable(source: Type, dest: Type) -> bool:
        visited = set()
        def visit(source: Type) -> bool:
            source = resolve_type_references(source, specs=specs)
            if is_type_assignable(dest, source, specs=specs):
                return True
            if source in visited:
                return False
            visited.add(source)
            if isinstance(source, SpecType):
                spec = lookup_spec(specs, source.name)
                assert(not isinstance(spec, TypeSpec))
                if spec is None or isinstance(spec, ConstEnumSpec) or isinstance(spec, TokenSpec):
                    return False
                if isinstance(spec, NodeSpec):
                    for field in spec.fields:
                        if visit(field.ty):
                            return True
                    return False
                if isinstance(spec, EnumSpec):
                    for member in spec.members:
                        if visit(member.ty):
                            return True
                    return False
                assert_never(spec)
            if isinstance(source, NeverType) or isinstance(source, ExternType) or isinstance(source, NoneType):
                return False
            if isinstance(source, AnyType):
                return True
            if isinstance(source, TupleType):
                return any(visit(ty_2) for ty_2 in source.element_types)
            if isinstance(source, PunctType):
                return visit(source.element_type) or visit(source.element_type)
            if isinstance(source, ListType):
                return visit(source.element_type)
            if isinstance(source, UnionType):
                return any(visit(ty_2) for ty_2 in source.types)
            assert_never(source)
        return visit(source)

    def gen_visitor(main_spec: Spec) -> PyFuncDef:

        generate_temporary = NameGenerator()

        main_type = expand_variant_types(spec_to_type(main_spec), specs=specs)

        body: list[PyStmt] = []

        def gen_visit_fields(spec: NodeSpec, input: PyExpr) -> Generator[PyStmt]:
            for field in spec.fields:
                if is_type_reachable(field.ty, main_type):
                    yield from gen_visit_type(field.ty, PyAttrExpr(expr=input, name=field.name))

        def gen_visit_union(input: PyExpr, types: Iterable[Type]) -> Generator[PyStmt]:
            cases = []
            for ty in types:
                body = list(gen_visit_type(ty, input))
                if body:
                    cases.append((
                        treespec_type_to_shallow_py_test(ty, input, prefix=prefix, specs=specs),
                        body
                    ))
            yield from make_py_cond(cases)

        def gen_visit_type(ty: Type, input: PyExpr) -> Generator[PyStmt]:
            ty = resolve_type_references(ty, specs=specs)
            if is_type_assignable(main_type, expand_variant_types(ty, specs=specs), specs=specs):
                yield PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ input ]))
                return
            if isinstance(ty, NoneType):
                return
            if isinstance(ty, ExternType):
                return
            if isinstance(ty, SpecType):
                spec = lookup_spec(specs, ty.name)
                assert(not isinstance(spec, TypeSpec))
                if spec is None or isinstance(spec, TokenSpec) or isinstance(spec, ConstEnumSpec):
                    return
                if isinstance(spec, EnumSpec):
                    yield from gen_visit_union(input, (member.ty for member in spec.members))
                    return
                if isinstance(spec, NodeSpec):
                    yield from gen_visit_fields(spec, input)
                    return
                assert_never(spec)
            if isinstance(ty, TupleType):
                for i, element_type in enumerate(ty.element_types):
                    yield from gen_visit_type(element_type, PySubscriptExpr(expr=input, slices=[ PyConstExpr(literal=i) ]))
                return
            if isinstance(ty, ListType):
                element_name = generate_temporary(prefix='element')
                yield PyForStmt(pattern=PyNamedPattern(element_name), expr=input, body=list(gen_visit_type(ty.element_type, PyNamedExpr(element_name))))
                return
            if isinstance(ty, PunctType):
                element_name = generate_temporary(prefix='element')
                separator_name = generate_temporary(prefix='separator')
                for_body = list(gen_visit_type(ty.element_type, PyNamedExpr(element_name)))
                sep_body = list(gen_visit_type(ty.separator_type, PyNamedExpr(separator_name)))
                if sep_body:
                    for_body.append(PyIfStmt(first=PyIfCase(
                        test=PyInfixExpr(PyNamedExpr(separator_name), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                        body=sep_body,
                    )))
                yield PyForStmt(
                    pattern=PyTuplePattern(
                        elements=[
                            PyNamedPattern(element_name),
                            PyNamedPattern(separator_name)
                        ],
                    ),
                    expr=input,
                    body=for_body
                )
                return
            if isinstance(ty, UnionType):
                yield from gen_visit_union(input, ty.types)
                return
            raise RuntimeError(f'unexpected {ty}')

        for spec in specs.elements:

            if not is_type_assignable(main_type, expand_variant_types(spec_to_type(spec), specs=specs), specs=specs):
                continue

            if isinstance(spec, NodeSpec):

                if_body = list(gen_visit_fields(spec, PyNamedExpr(node_param_name)))
                if_body.append(PyRetStmt())
                body.append(PyIfStmt(first=PyIfCase(
                    test=PyCallExpr(
                        operator=PyNamedExpr('isinstance'),
                        args=[
                            PyNamedExpr(node_param_name),
                            PyNamedExpr(to_py_class_name(spec.name, prefix))
                        ]
                    ),
                    body=if_body
                )))

            elif isinstance(spec, TokenSpec):

                if_body = []
                if_body.append(PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ PyNamedExpr(node_param_name) ])))
                if_body.append(PyRetStmt())
                body.append(PyIfStmt(first=PyIfCase(
                    test=make_py_isinstance(
                        PyNamedExpr(node_param_name),
                        PyNamedExpr(to_py_class_name(spec.name, prefix))
                    ),
                    body=if_body,
                )))

        decorators = []
        if not enable_asserts:
            # We add `@typing.no_type_check` to drastically improve the performance of the type checker.
            decorators.append(PyDecorator(PyNamedExpr('no_type_check')))

        return PyFuncDef(
            decorators=decorators,
            name=f'for_each_{namespaced(main_spec.name, prefix)}',
            params=[
                PyNamedParam(
                    PyNamedPattern(node_param_name),
                    annotation=PyNamedExpr(to_py_class_name(main_spec.name, prefix))
                ),
                PyNamedParam(
                    PyNamedPattern(proc_param_name),
                    annotation=PySubscriptExpr(expr=PyNamedExpr('Callable'), slices=[ PyListExpr(elements=[ PyNamedExpr(to_py_class_name(main_spec.name, prefix)) ]), PyNamedExpr('None') ])
                ),
            ],
            body=body,
        )

    stmts.extend(gen_visitor(spec) for spec in specs.elements if isinstance(spec, EnumSpec) and is_self_referential(spec.name, specs=specs))

    def gen_member_visitor(main_spec: Spec, visit_spec: Spec) -> PyFuncDef:

        generate_temporary = NameGenerator()

        main_type = expand_variant_types(spec_to_type(main_spec), specs=specs)
        visit_type = expand_variant_types(spec_to_type(visit_spec), specs=specs)

        fn_name = f'for_each_{namespaced(visit_spec.name, prefix)}'

        body: list[PyStmt] = []

        def gen_visit_fields(spec: NodeSpec, input: PyExpr) -> Generator[PyStmt]:
            for field in spec.fields:
                if contains_type(expand_variant_types(field.ty, specs=specs), main_type, specs=specs):
                    yield from gen_visit_type(field.ty, PyAttrExpr(expr=input, name=field.name))

        def gen_visit_union(input: PyExpr, types: Iterable[Type]) -> Generator[PyStmt]:
            cases = []
            for ty in types:
                body = list(gen_visit_type(ty, input))
                if body:
                    cases.append((
                        treespec_type_to_shallow_py_test(ty, input, prefix=prefix, specs=specs),
                        body
                    ))
            yield from make_py_cond(cases)

        def gen_visit_type(ty: Type, input: PyExpr) -> Generator[PyStmt]:
            ty = resolve_type_references(ty, specs=specs)
            if is_type_assignable(visit_type, expand_variant_types(ty, specs=specs), specs=specs):
                yield PyExprStmt(PyCallExpr(PyNamedExpr(proc_param_name), args=[ input ]))
                return
            if is_type_assignable(main_type, expand_variant_types(ty, specs=specs), specs=specs):
                yield PyExprStmt(PyCallExpr(PyNamedExpr(fn_name), args=[ input, PyNamedExpr(proc_param_name) ]))
                return
            if isinstance(ty, NoneType):
                return
            if isinstance(ty, ExternType):
                return
            if isinstance(ty, SpecType):
                spec = lookup_spec(specs, ty.name)
                assert(not isinstance(spec, TypeSpec))
                if spec is None or isinstance(spec, TokenSpec) or isinstance(spec, ConstEnumSpec):
                    return
                if isinstance(spec, EnumSpec):
                    yield from gen_visit_union(input, (member.ty for member in spec.members))
                    return
                if isinstance(spec, NodeSpec):
                    yield from gen_visit_fields(spec, input)
                    return
                assert_never(spec)
            if isinstance(ty, TupleType):
                for i, element_type in enumerate(ty.element_types):
                    yield from gen_visit_type(element_type, PySubscriptExpr(expr=input, slices=[ PyConstExpr(literal=i) ]))
                return
            if isinstance(ty, ListType):
                element_name = generate_temporary(prefix='element')
                yield PyForStmt(pattern=PyNamedPattern(element_name), expr=input, body=list(gen_visit_type(ty.element_type, PyNamedExpr(element_name))))
                return
            if isinstance(ty, PunctType):
                element_name = generate_temporary(prefix='element')
                separator_name = generate_temporary(prefix='separator')
                each_sep = list(gen_visit_type(ty.separator_type, PyNamedExpr(separator_name)))
                for_body = list(gen_visit_type(ty.element_type, PyNamedExpr(element_name)))
                if each_sep:
                    for_body.append(PyIfStmt(first=PyIfCase(
                        test=PyInfixExpr(PyNamedExpr(separator_name), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                        body=each_sep,
                    )))
                yield PyForStmt(
                    pattern=PyTuplePattern(
                        elements=[
                            PyNamedPattern(element_name),
                            PyNamedPattern(separator_name)
                        ],
                    ),
                    expr=input,
                    body=for_body
                )
                # yield PyIfStmt(first=PyIfCase(
                #     test=PyInfixExpr(PyAttrExpr(target, 'last'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                #     body=list(gen_proc_calls(ty.element_type, PyAttrExpr(target, 'last')))
                # ))
                return
            if isinstance(ty, UnionType):
                yield from gen_visit_union(input, ty.types)
                return
            raise RuntimeError(f'unexpected {ty}')

        for spec in specs.elements:

            if isinstance(spec, NodeSpec):

                if_body = []
                for field in spec.fields:
                    if_body.extend(gen_visit_type(field.ty, PyAttrExpr(expr=PyNamedExpr(node_param_name), name=field.name)))
                if_body.append(PyRetStmt())
                body.append(PyIfStmt(first=PyIfCase(
                    test=PyCallExpr(
                        operator=PyNamedExpr('isinstance'),
                        args=[
                            PyNamedExpr(node_param_name),
                            PyNamedExpr(to_py_class_name(spec.name, prefix))
                        ]
                    ),
                    body=if_body
                )))

            elif isinstance(spec, TokenSpec):

                if_body = []
                if_body.append(PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ PyNamedExpr(node_param_name) ])))
                if_body.append(PyRetStmt())
                body.append(PyIfStmt(first=PyIfCase(
                    test=make_py_isinstance(
                        PyNamedExpr(node_param_name),
                        PyNamedExpr(to_py_class_name(spec.name, prefix))
                    ),
                    body=if_body,
                )))

        decorators = []
        if not enable_asserts:
            # We add `@typing.no_type_check` to drastically improve the performance of the type checker.
            decorators.append(PyDecorator(PyNamedExpr('no_type_check')))

        return PyFuncDef(
            decorators=decorators,
            name=fn_name,
            params=[
                PyNamedParam(
                    PyNamedPattern(node_param_name),
                    annotation=PyNamedExpr(to_py_class_name(main_spec.name, prefix))
                ),
                PyNamedParam(
                    PyNamedPattern(proc_param_name),
                    annotation=PySubscriptExpr(expr=PyNamedExpr('Callable'), slices=[ PyListExpr(elements=[ PyNamedExpr(to_py_class_name(visit_spec.name, prefix)) ]), PyNamedExpr('None') ])
                ),
            ],
            body=body,
        )

    # NOTE This is disabled right now because we don't actually need it
    # TODO dynamically specify which types of which node to visit
    # tokens_spec = lookup_spec(specs, any_token_rule_name)
    # syntax_spec = lookup_spec(specs, any_syntax_rule_name)
    # if tokens_spec is not None and syntax_spec is not None:
    #     stmts.append(gen_member_visitor(syntax_spec, tokens_spec))

    # Generate rewriters

    proc_param_name = 'proc'
    node_param_name = 'node'

    def gen_rewriter(main_spec: Spec) -> PyFuncDef:

        generate_temporary = NameGenerator()

        main_type = expand_variant_types(spec_to_type(main_spec), specs=specs)

        changed_var_name = f'changed'

        body: list[PyStmt] = []

        def gen_rewrite_fields(spec: NodeSpec, input: PyExpr, assign: Callable[[PyExpr], PyStmt], total: bool) -> Iterable[PyStmt]:

            body = []
            new_args = []

            can_be_rewritten = False

            body.append(PyAssignStmt(PyNamedPattern(changed_var_name), value=PyNamedExpr('False')))

            for field in spec.fields:
                if contains_type(expand_variant_types(field.ty, specs=specs), main_type, specs=specs):
                    can_be_rewritten = True
                    new_field_name = generate_temporary(f'new_{field.name}')
                    new_args.append(PyKeywordArg(field.name, PyNamedExpr(new_field_name)))
                    body.extend(gen_rewrite_type(field.ty, PyAttrExpr(input, name=field.name), new_field_name, total)) # FIXME
                else:
                    new_args.append(PyKeywordArg(field.name, PyAttrExpr(input, field.name)))

            if not can_be_rewritten:
                return [ assign(input) ]

            body.extend(make_py_cond([
                (PyNamedExpr(changed_var_name), [ assign(PyCallExpr(PyNamedExpr(to_py_class_name(spec.name, prefix=prefix)), args=new_args)) ]),
                (None, [ assign(input) ])
            ]))

            return body

        def gen_rewrite_union(types: Iterable[Type], input: PyExpr, output: str, total: bool) -> Generator[PyStmt]:
            cases: list[PyCondCase] = []
            for element_type in types:
                body = list(gen_rewrite_type(element_type, input, output, total))
                if not body:
                    body.append(PyPassStmt())
                cases.append((
                    treespec_type_to_shallow_py_test(element_type, input, prefix=prefix, specs=specs),
                    body
                ))
            if cases:
                cases.append((None, [ PyExprStmt(PyCallExpr(PyNamedExpr('assert_never'), args=[ input ])) ]))
            yield from make_py_cond(cases)

        def gen_rewrite_type(ty: Type, input: PyExpr, output: str, total: bool) -> Generator[PyStmt]:

            ty = resolve_type_references(ty, specs=specs)

            if is_type_assignable(main_type, expand_variant_types(ty, specs=specs),  specs=specs):
                yield PyAssignStmt(PyNamedPattern(output), value=PyCallExpr(PyNamedExpr(proc_param_name), args=[ input ]))
                yield PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ treespec_type_to_shallow_py_test(ty, PyNamedExpr(output), prefix=prefix, specs=specs) ] ))
                yield PyIfStmt(first=PyIfCase(
                    PyInfixExpr(PyNamedExpr(output), (PyIsKeyword(), PyNotKeyword()), input),
                    [ PyAssignStmt(PyNamedPattern(changed_var_name), value=PyNamedExpr('True')) ]
                ))
                return

            if isinstance(ty, NoneType) or isinstance(ty, ExternType):
                if total:
                    yield PyAssignStmt(PyNamedPattern(output), value=input)
                return

            if isinstance(ty, SpecType):

                spec = lookup_spec(specs, ty.name)

                assert(not isinstance(spec, TypeSpec))

                if spec is None or isinstance(spec, TokenSpec) or isinstance(spec, ConstEnumSpec):
                    if total:
                        yield PyAssignStmt(PyNamedPattern(output), value=input)
                    return

                if isinstance(spec, EnumSpec):
                    yield from gen_rewrite_union((member.ty for member in spec.members), input, output, total)
                    return

                if isinstance(spec, NodeSpec):
                    def assign(expr: PyExpr) -> PyStmt:
                        return PyAssignStmt(PyNamedPattern(output), value=expr)
                    yield from gen_rewrite_fields(spec, input, assign, total)
                    return

                assert_never(spec)

            if isinstance(ty, TupleType):

                new_elements_var_name = generate_temporary('new_elements')

                yield PyAssignStmt(PyNamedPattern(new_elements_var_name), value=PyListExpr())

                for i, element_type in enumerate(ty.element_types):

                    old_element_var_name = generate_temporary(f'element_{i}')
                    new_element_var_name = generate_temporary(f'new_element_{i}')

                    yield PyAssignStmt(
                        PyNamedPattern(old_element_var_name),
                        value=PySubscriptExpr(expr=input, slices=[ PyConstExpr(literal=i) ])
                    )

                    yield from gen_rewrite_type(element_type, PyNamedExpr(old_element_var_name), new_element_var_name, total=True)

                    yield PyExprStmt(PyCallExpr(
                        PyAttrExpr(PyNamedExpr(new_elements_var_name), 'append'),
                        args=[ PyNamedExpr(new_element_var_name) ]
                    ))

                yield PyAssignStmt(PyNamedPattern(output), value=PyIfExpr(PyCallExpr(PyNamedExpr('tuple'), args=[ PyNamedExpr(new_elements_var_name) ]), PyNamedExpr(changed_var_name), input))

                return

            if isinstance(ty, ListType):

                element_name = generate_temporary('element')
                new_element_var_name = generate_temporary('new_element')

                yield PyAssignStmt(PyNamedPattern(output), value=PyListExpr())

                yield PyForStmt(
                    pattern=PyNamedPattern(element_name),
                    expr=input,
                    body=list(gen_rewrite_type(ty.element_type, PyNamedExpr(element_name), new_element_var_name, total=True))
                )

                return

            if isinstance(ty, PunctType):

                element_name = generate_temporary('element')
                separator_name = generate_temporary('separator')
                new_last_var_name = generate_temporary('new_last')
                new_element_var_name = generate_temporary('new_element')
                new_separator_var_name = generate_temporary('new_separator')

                yield PyAssignStmt(
                    PyNamedPattern(output),
                    value=PyCallExpr(PyNamedExpr('Punctuated'))
                )

                yield PyForStmt(
                    pattern=PyTuplePattern(
                        elements=[
                            PyNamedPattern(element_name),
                            PyNamedPattern(separator_name)
                        ],
                    ),
                    expr=PyAttrExpr(input, 'delimited'),
                    body=[
                        *gen_rewrite_type(ty.element_type, PyNamedExpr(element_name), new_element_var_name, total=True),
                        *gen_rewrite_type(ty.separator_type, PyNamedExpr(separator_name), new_separator_var_name, total=True),
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(output), 'append'), args=[
                            PyNamedExpr(new_element_var_name),
                            PyNamedExpr(new_separator_var_name),
                        ]))
                    ]
                )

                yield from gen_rewrite_type(ty.element_type, PyAttrExpr(input, 'last'), new_last_var_name, total=True)
                yield PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(output), 'append_final'), args=[ PyNamedExpr(new_last_var_name) ]))

                return

            if isinstance(ty, UnionType):
                yield from gen_rewrite_union(ty.types, input, output, total)
                return

            raise RuntimeError(f'unexpected {ty}')

        for spec in specs.elements:

            if not is_type_assignable(main_type, expand_variant_types(spec_to_type(spec), specs=specs), specs=specs):
                continue

            if isinstance(spec, NodeSpec):

                body.append(PyIfStmt(first=PyIfCase(
                    test=PyCallExpr(
                        operator=PyNamedExpr('isinstance'),
                        args=[
                            PyNamedExpr(node_param_name),
                            PyNamedExpr(to_py_class_name(spec.name, prefix))
                        ]
                    ),
                    body=list(gen_rewrite_fields(spec, PyNamedExpr(node_param_name), make_py_return, True))
                )))

            elif isinstance(spec, TokenSpec):

                # body.append(PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ PyNamedExpr(node_param_name) ])))
                body.append(PyIfStmt(first=PyIfCase(
                    test=make_py_isinstance(
                        PyNamedExpr(node_param_name),
                        PyNamedExpr(to_py_class_name(spec.name, prefix))
                    ),
                    body=[
                        PyRetStmt(),
                    ],
                )))

        decorators = []
        if not enable_asserts:
            # We add `@typing.no_type_check` to drastically improve the performance of the type checker.
            decorators.append(PyDecorator(PyNamedExpr('no_type_check')))

        return PyFuncDef(
            decorators=decorators,
            name=f'rewrite_each_{namespaced(main_spec.name, prefix)}',
            params=[
                PyNamedParam(
                    PyNamedPattern(node_param_name),
                    annotation=PyNamedExpr(to_py_class_name(main_spec.name, prefix))
                ),
                PyNamedParam(
                    PyNamedPattern(proc_param_name),
                    annotation=PySubscriptExpr(expr=PyNamedExpr('Callable'), slices=[ PyListExpr(elements=[ PyNamedExpr(to_py_class_name(main_spec.name, prefix)) ]), PyNamedExpr(to_py_class_name(main_spec.name, prefix)) ])
                ),
            ],
            return_type=PyNamedExpr(to_py_class_name(main_spec.name, prefix)),
            body=body,
        )

    stmts.extend(gen_rewriter(spec) for spec in specs.elements if isinstance(spec, EnumSpec) and is_self_referential(spec.name, specs=specs))

    return PyModule(stmts=stmts)

