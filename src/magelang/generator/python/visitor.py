
from magelang.ast import Grammar
from magelang.treespec import *
from magelang.lang.python.cst import *
from magelang.util import NameGenerator
from .util import build_cond, Case, build_isinstance, gen_shallow_test, namespaced, to_class_name

def generate_visitor(
    grammar: Grammar,
    prefix='',
    debug = False,
) -> PyModule:

    specs = grammar_to_specs(grammar)

    generate_temporary = NameGenerator()

    proc_param_name = 'proc'
    value_param_name = 'node'
    token_type_name = to_class_name('token', prefix)
    node_type_name = to_class_name('node', prefix)
    syntax_type_name = to_class_name('syntax', prefix)
    is_token_name = f'is_{namespaced('token', prefix)}'
    for_each_syntax_name = f'for_each_{namespaced('syntax', prefix)}'

    def gen_visitor(name: str) -> PyFuncDef:

        main_spec = specs.lookup(name)
        main_type = spec_to_type(main_spec)

        body: list[PyStmt] = []

        def gen_each_field(spec: NodeSpec, target: PyExpr) -> Generator[PyStmt, None, None]:
            for field in spec.fields:
                if contains_type(field.ty, main_type, specs=specs):
                    yield from gen_proc_call(field.ty, PyAttrExpr(expr=target, name=field.name))

        def gen_proc_call(ty: Type, target: PyExpr) -> Generator[PyStmt, None, None]:
            if is_type_assignable(ty, main_type, specs=specs):
                yield PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ target ]))
                return
            if isinstance(ty, NoneType):
                return
            if isinstance(ty, VariantType):
                spec = specs.lookup(ty.name)
                assert(isinstance(spec, VariantSpec))
                cases = []
                for _, ty_2 in spec.members:
                    body = list(gen_proc_call(ty_2, target))
                    if body:
                        cases.append((
                            gen_shallow_test(ty_2, target, prefix),
                            body
                        ))
                yield from build_cond(cases)
                return
            if isinstance(ty, NodeType):
                spec = specs.lookup(ty.name)
                assert(isinstance(spec, NodeSpec))
                yield from gen_each_field(spec, target)
                return
            if isinstance(ty, TokenType):
                return
            if isinstance(ty, TupleType):
                for i, element_type in enumerate(ty.element_types):
                    yield from gen_proc_call(element_type, PySubscriptExpr(expr=target, slices=[ PyConstExpr(literal=i) ]))
                return
            if isinstance(ty, ListType):
                element_name = generate_temporary(prefix='element')
                yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_proc_call(ty.element_type, PyNamedExpr(element_name))))
                return
            if isinstance(ty, PunctType):
                element_name = generate_temporary(prefix='element')
                separator_name = generate_temporary(prefix='separator')
                yield PyForStmt(
                    pattern=PyTuplePattern(
                        elements=[
                            PyNamedPattern(element_name),
                            PyNamedPattern(separator_name)
                        ],
                    ),
                    expr=PyAttrExpr(target, 'elements'),
                    body=[
                        *gen_proc_call(ty.element_type, PyNamedExpr(element_name)),
                        *gen_proc_call(ty.separator_type, PyNamedExpr(separator_name)),
                    ]
                )
                yield PyIfStmt(first=PyIfCase(
                    test=PyInfixExpr(PyAttrExpr(target, 'last'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                    body=list(gen_proc_call(ty.element_type, PyAttrExpr(target, 'last')))
                ))
                return
            if isinstance(ty, UnionType):
                cases: list[Case] = []
                for element_type in ty.types:
                    body = list(gen_proc_call(element_type, target))
                    if body:
                        cases.append((
                            gen_shallow_test(element_type, target, prefix),
                            body
                        ))
                yield from build_cond(cases)
                return
            raise RuntimeError(f'unexpected {ty}')

        for spec in specs:

            if not is_type_assignable(spec_to_type(spec), main_type, specs=specs):
                continue

            if isinstance(spec, NodeSpec):

                # We're going to start a new scope, so all previous temporary names may be used once again
                generate_temporary.reset()

                if_body = list(gen_each_field(spec, PyNamedExpr(value_param_name)))
                if_body.append(PyRetStmt())
                body.append(PyIfStmt(first=PyIfCase(
                    test=PyCallExpr(
                        operator=PyNamedExpr('isinstance'),
                        args=[
                            PyNamedExpr(value_param_name),
                            PyNamedExpr(to_class_name(spec.name, prefix))
                        ]
                    ),
                    body=if_body
                )))

            elif isinstance(spec, TokenSpec):

                # body.append(PyExprStmt(PyCallExpr(operator=PyNamedExpr(proc_param_name), args=[ PyNamedExpr(value_param_name) ])))
                body.append(PyIfStmt(first=PyIfCase(
                    test=build_isinstance(
                        PyNamedExpr(value_param_name),
                        PyNamedExpr(to_class_name(spec.name, prefix))
                    ),
                    body=[
                        PyRetStmt(),
                    ],
                )))

        decorators = []
        if not debug:
            # We add `@typing.no_type_check` to drastically improve the performance of the type checker.
            decorators.append(PyDecorator(PyNamedExpr('no_type_check')))

        return PyFuncDef(
            decorators=decorators,
            name=f'for_each_{namespaced(name, prefix)}',
            params=[
                PyNamedParam(
                    PyNamedPattern(value_param_name),
                    annotation=PyNamedExpr(to_class_name(name, prefix))
                ),
                PyNamedParam(
                    PyNamedPattern(proc_param_name),
                    annotation=PySubscriptExpr(expr=PyNamedExpr('Callable'), slices=[ PyListExpr(elements=[ PyNamedExpr(to_class_name(name, prefix)) ]), PyNamedExpr('None') ])
                ),
            ],
            body=body,
        )

    variant_visitors = list(gen_visitor(spec.name) for spec in specs if isinstance(spec, VariantSpec) and is_cyclic(spec.name, specs=specs))

    return PyModule(stmts=[
        PyImportFromStmt(
            PyAbsolutePath('typing'),
            aliases=[
                PyFromAlias('Callable'),
                PyFromAlias('no_type_check'),
            ]
        ),
        PyImportFromStmt(
            PyRelativePath(dots=1, name=PyQualName('cst')),
            aliases=[ PyFromAlias(PyAsterisk()) ]
        ),
        *variant_visitors,
    ])

