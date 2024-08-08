
from typing import assert_never
from magelang.ast import Grammar
from magelang.repr import *
from magelang.lang.python.cst import *
from magelang.util import NameGenerator, to_snake_case
from .util import build_cond, Case, gen_shallow_test, namespaced, to_class_name

def generate_visitor(
    grammar: Grammar,
    prefix='',
) -> PyModule:

    specs = grammar_to_specs(grammar)

    generate_temporary = NameGenerator()

    proc_name = 'proc'
    syntax_param_name = 'node'
    token_type_name = to_class_name('token', prefix)
    node_type_name = to_class_name('node', prefix)
    syntax_type_name = to_class_name('syntax', prefix)
    is_token_name = f'is_{namespaced('token', prefix)}'
    for_each_child_name = f'for_each_{namespaced('child', prefix)}'

    def gen_proc_call(ty: Type, target: PyExpr) -> Generator[PyStmt, None, None]:
        if isinstance(ty, NoneType):
            yield PyPassStmt()
            return
        if isinstance(ty, TokenType) or isinstance(ty, NodeType) or isinstance(ty, VariantType):
            yield PyExprStmt(expr=PyCallExpr(operator=PyNamedExpr(proc_name), args=[ target ]))
            return
        if isinstance(ty, TupleType):
            for i, element_type in enumerate(ty.element_types):
                tmp = generate_temporary(prefix='element_')
                yield PyAssignStmt(pattern=PyNamedPattern(tmp), expr=PySubscriptExpr(expr=target, slices=[ PyConstExpr(literal=i) ]))
                yield from gen_proc_call(element_type, PyNamedExpr(tmp))
            return
        if isinstance(ty, ListType):
            element_name = generate_temporary(prefix='element_')
            yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_proc_call(ty.element_type, PyNamedExpr(element_name))))
            return
        if isinstance(ty, PunctType):
            element_name = generate_temporary(prefix='element_')
            separator_name = generate_temporary(prefix='separator_')
            yield PyForStmt(
                pattern=PyTuplePattern(
                    elements=[
                        PyNamedPattern(element_name),
                        PyNamedPattern(separator_name)
                    ],
                ),
                expr=target,
                body=list(gen_proc_call(ty.element_type, PyNamedExpr(element_name)))
            )
            return
        if isinstance(ty, UnionType):
            cases: list[Case] = []
            for element_type in ty.types:
                cases.append((
                    gen_shallow_test(element_type, target, prefix),
                    list(gen_proc_call(element_type, target))
                ))
            cases.append((None, [ PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr('ValueError'))) ]))
            yield from build_cond(cases)
            return
        raise RuntimeError(f'unexpected {ty}')

    body: list[PyStmt] = [
        PyIfStmt(first=PyIfCase(
            test=PyCallExpr(
                operator=PyNamedExpr(is_token_name),
                args=[ PyNamedExpr(syntax_param_name) ]
            ),
            body=PyRetStmt(),
        )),
    ]


    for spec in specs:

        # We're going to start a new scope, so all previous temporary names may be used once again
        generate_temporary.reset()

        if isinstance(spec, TokenSpec):
            continue
        if isinstance(spec, NodeSpec):
            if_body: list[PyStmt] = []
            for field in spec.members:
                if_body.extend(gen_proc_call(field.ty, PyAttrExpr(expr=PyNamedExpr(syntax_param_name), name=field.name)))
            if_body.append(PyRetStmt())
            body.append(PyIfStmt(first=PyIfCase(
                test=PyCallExpr(
                    operator=PyNamedExpr('isinstance'),
                    args=[
                        PyNamedExpr(syntax_param_name),
                        PyNamedExpr(to_class_name(spec.name, prefix))
                    ]
                ),
                body=if_body
            )))
            continue
        if isinstance(spec, VariantSpec):
            continue

        assert_never(spec)

    return PyModule(stmts=[
        PyImportFromStmt(PyAbsolutePath(PyQualName('typing')), aliases=[
            PyAlias(PyAbsolutePath(PyQualName('Callable'))),
        ]),
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('cst')),
            aliases=[ PyAlias(PyAbsolutePath(PyQualName('*'))) ]
        ),
        PyFuncDef(
            name=for_each_child_name,
            params=[
                PyNamedParam(
                    PyNamedPattern(syntax_param_name),
                    annotation=PyNamedExpr(syntax_type_name)
                ),
                PyNamedParam(
                    PyNamedPattern(proc_name),
                    annotation=PySubscriptExpr(expr=PyNamedExpr('Callable'), slices=[ PyListExpr(elements=[ PyNamedExpr(syntax_type_name) ]), PyNamedExpr('None') ])
                )
            ],
            body=body,
        )
    ])
