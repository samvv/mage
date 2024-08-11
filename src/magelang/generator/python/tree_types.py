
from magelang.generator.python.util import build_union, gen_initializers, gen_py_type, namespaced, rule_type_to_py_type, to_class_name
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit
from magelang.repr import NodeSpec, Specs, TokenSpec, VariantSpec, is_optional

def quote_py_type(expr: PyExpr) -> PyExpr:
    return PyConstExpr(emit(expr))

def generate_tree_types(
    specs: Specs,
    prefix = '',
    gen_parent_pointers = False
) -> PyModule:

    stmts: list[PyStmt] = [
        PyImportFromStmt(PyAbsolutePath(PyQualName('typing')), aliases=[
            PyFromAlias('Any'),
            PyFromAlias('TypeGuard'),
            PyFromAlias('Never'),
            PyFromAlias('Sequence'),
        ]),
        PyImportFromStmt(PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')), aliases=[
            PyFromAlias('Span'),
            PyFromAlias('Punctuated'),
            PyFromAlias('BaseNode', asname='Node'),
            PyFromAlias('BaseToken', asname='Token'),
        ]),
    ]

    def build_instance_pred(name: str) -> PyStmt:
        return PyFuncDef(
            name=f'is_{namespaced(name, prefix)}',
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeGuard'), [ PyNamedExpr(to_class_name(name, prefix)) ]),
            body=PyExprStmt(PyNamedExpr('...')), # FIXME
        )

    for spec in specs:

        if isinstance(spec, NodeSpec):

            body: list[PyStmt] = [
            ]

            required = []
            optional = []

            for field in spec.members:
                param_type, _ = gen_initializers(field.name, field.ty, 'unknown', lambda _: PyPassStmt(), specs=specs, prefix=prefix)
                param_type_str = emit(gen_py_type(param_type, prefix))
                body.append(PyAssignStmt(
                    PyNamedPattern(field.name),
                    annotation=quote_py_type(gen_py_type(field.ty, prefix=prefix)),
                    expr=PyConstExpr('delme')
                ))
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

            body.append(
                PyFuncDef(
                    name='__init__',
                    params=[
                        PyNamedParam(PyNamedPattern('self')),
                        *required,
                        *optional,
                    ],
                    body=PyExprStmt(PyNamedExpr('...')), # FIXME
                )
            )

            if gen_parent_pointers:
                pass

            stmts.append(PyClassDef(
                name=to_class_name(spec.name, prefix),
                bases=[ 'Node' ],
                body=body,
            ))

        if isinstance(spec, TokenSpec):

            init_params: list[PyParam] = [ PyNamedParam(PyNamedPattern('self')) ]

            if not spec.is_static:
                init_params.append(PyNamedParam(PyNamedPattern('value'), annotation=rule_type_to_py_type(spec.field_type)))

            init_params.append(
                PyNamedParam(PyNamedPattern('span'), annotation=build_union([ PyNamedExpr('Span'), PyNamedExpr('None') ]), default=PyNamedExpr('None')),
            )

            body = [
                PyFuncDef(
                    name='__init__',
                    params=init_params,
                    body=PyExprStmt(PyNamedExpr('...')), # FIXME
                ),
            ]

            if not spec.is_static:
                body.append(PyAssignStmt(PyNamedPattern('value'), annotation=rule_type_to_py_type(spec.field_type), expr=PyConstExpr('delme')))

            stmts.append(PyClassDef(
                name=to_class_name(spec.name, prefix),
                bases=[ 'Token' ],
                body=body,
            ))

        if isinstance(spec, VariantSpec):
            cls_name = to_class_name(spec.name, prefix)
            assert(len(spec.members) > 0)
            stmts.append(PyTypeAliasStmt(cls_name, build_union(gen_py_type(ty, prefix) for _, ty in spec.members)))
            stmts.append(build_instance_pred(spec.name))
            continue

    stmts.append(build_instance_pred('syntax'))
    stmts.append(build_instance_pred('node'))
    stmts.append(build_instance_pred('token'))

    stmts.append(PyTypeAliasStmt(
        to_class_name('syntax', prefix),
        build_union([
            PyNamedExpr(to_class_name('node', prefix)),
            PyNamedExpr(to_class_name('token', prefix))
        ])
    ))

    stmts.append(PyTypeAliasStmt(
        to_class_name('token', prefix),
        build_union(PyNamedExpr(to_class_name(spec.name, prefix)) for spec in specs if isinstance(spec, TokenSpec))
    ))

    stmts.append(PyTypeAliasStmt(
        to_class_name('node', prefix),
        build_union(PyNamedExpr(to_class_name(spec.name, prefix)) for spec in specs if isinstance(spec, NodeSpec))
    ))

    return PyModule(stmts=stmts)
