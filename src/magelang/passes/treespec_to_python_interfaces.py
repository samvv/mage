
from typing import assert_never

from magelang.manager import declare_pass
from magelang.passes.mage_insert_magic_rules import any_node_rule_name, any_token_rule_name, any_syntax_rule_name
from magelang.helpers import make_py_union, get_coercions, treespec_type_to_py_type, namespaced, extern_type_to_py_type, to_py_class_name, quote_py_type, lookup_spec
from magelang.lang.treespec.helpers import is_self_referential, is_optional_type, is_type_assignable, resolve_type_references
from magelang.lang.mage.ast import *
from magelang.lang.treespec.ast import *
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit

def make_py_optional(ty: PyExpr) -> PyExpr:
    return PyInfixExpr(ty, PyVerticalBar(), PyNamedExpr('None'))

def make_py_return(expr: PyExpr) -> PyStmt:
    return PyRetStmt(expr=expr)

@declare_pass()
def treespec_to_python_interfaces(
    specs: Specs,
    prefix: str = '',
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
                body=[ PyExprStmt(PyEllipsisExpr()) ],
            ),
        ]),
    ]

    # Generate token classes

    for spec in specs.elements:

        if not isinstance(spec, TokenSpec):
            continue

        this_class_name = to_py_class_name(spec.name, prefix)

        class_body: list[PyStmt] = []

        if spec.is_static:

            class_body.append(PyPassStmt())

        else:

            init_body: list[PyStmt] = []

            py_type = extern_type_to_py_type(spec.field_type)

            init_params: list[PyParam] = [
                # self
                PyNamedParam(pattern=PyNamedPattern('self')),
                # value: Type
                PyNamedParam(pattern=PyNamedPattern('value'), annotation=py_type),
                # span: Span | None = None
                PyNamedParam(pattern=PyNamedPattern('span'), annotation=make_py_union([ PyNamedExpr('Span'), PyNamedExpr('None') ]), default=PyNamedExpr('None')),
            ]

            init_body.append(PyExprStmt(PyEllipsisExpr()))

            class_body.append(PyAssignStmt(PyNamedPattern('value'), annotation=py_type))

            class_body.append(PyFuncDef(name='__init__', params=init_params, body=init_body))

        stmts.append(PyClassDef(name=this_class_name, bases=[ PyClassBaseArg(base_token_class_name) ], body=class_body))

        stmts.append(PyFuncDef(
            name=f'is_{namespaced(spec.name, prefix)}',
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeIs'), [ PyNamedExpr(this_class_name) ]),
            body=[ PyExprStmt(PyEllipsisExpr()) ]
        ))

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
        derive_args = []

        required_params: list[PyParam] = []
        optional_params: list[PyParam] = []

        for field in spec.fields:
            body.append(PyAssignStmt(PyNamedPattern(field.name), annotation=quote_py_type(treespec_type_to_py_type(field.ty, prefix=prefix))))

        for field in spec.fields:

            type_with_coercions = get_coercions(field.ty, specs=specs)

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
                    body=[ PyExprStmt(PyEllipsisExpr()), ]
                ))

            derive_kwargs_body.append(PyAssignStmt(
                pattern=PyNamedPattern(field.name),
                annotation=quote_py_type(treespec_type_to_py_type(param_type, prefix=prefix, immutable=True)),
            ))
            derive_args.append(PyKeywordArg(field.name, PyNamedExpr(field.name)))

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

        body.append(PyFuncDef(
             name='derive',
             params=[ PyNamedParam(PyNamedPattern('self')), PyRestKeywordParam('kwargs', annotation=PySubscriptExpr(PyNamedExpr('Unpack'), [ PyNamedExpr(derive_kwargs_class_name) ])) ],
             return_type=PyConstExpr(this_class_name),
             body=[ PyExprStmt(PyEllipsisExpr()) ],
         ))

        parent_type_name = f'{to_py_class_name(spec.name, prefix)}Parent'
        parent_type = get_parent_type(spec.name)
        body.append(PyFuncDef(
            decorators=[ PyDecorator(PyNamedExpr('property')) ],
            name='parent',
            params=[ PyNamedParam(PyNamedPattern('self')) ],
            return_type=PyConstExpr(parent_type_name),
            body=[ PyExprStmt(PyEllipsisExpr()) ],
        ))

        stmts.append(PyClassDef(name=this_class_name, bases=[ PyClassBaseArg(base_node_class_name) ], body=body))

        stmts.append(PyFuncDef(
            name=f'is_{namespaced(spec.name, prefix)}',
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeIs'), [ PyNamedExpr(this_class_name) ]),
            body=[ PyExprStmt(PyEllipsisExpr()) ]
        ))

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

        stmts.append(PyFuncDef(
            name=f'is_{namespaced(spec.name, prefix)}',
            params=pred_params,
            return_type=PySubscriptExpr(expr=PyNamedExpr('TypeIs'), slices=[ PyNamedExpr(type_name) ]),
            body=[ PyExprStmt(PyEllipsisExpr()) ],
        ))

    # Generate type aliases for parent fields

    for spec in specs.elements:
        if not isinstance(spec, NodeSpec):
            continue
        parent_type = get_parent_type(spec.name)
        parent_type_name = f'{to_py_class_name(spec.name, prefix)}Parent'
        stmts.append(PyTypeAliasStmt(parent_type_name, treespec_type_to_py_type(parent_type, prefix)))

    # Generate visitors

    proc_param_name = 'proc'
    node_param_name = 'node'

    def gen_visitor(main_spec: Spec) -> PyFuncDef:
        return PyFuncDef(
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
            body=[ PyExprStmt(PyEllipsisExpr()) ],
        )

    stmts.extend(gen_visitor(spec) for spec in specs.elements if isinstance(spec, EnumSpec) and is_self_referential(spec.name, specs=specs))

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
        return PyFuncDef(
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
            body=[ PyExprStmt(PyEllipsisExpr()) ],
        )

    stmts.extend(gen_rewriter(spec) for spec in specs.elements if isinstance(spec, EnumSpec) and is_self_referential(spec.name, specs=specs))

    return PyModule(stmts=stmts)

