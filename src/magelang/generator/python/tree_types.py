
from .util import build_union, gen_initializers, gen_py_type, namespaced, rule_type_to_py_type, to_class_name, quote_py_type
from magelang.lang.python.cst import *
from magelang.lang.python.emitter import emit
from magelang.treespec import *

def generate_tree_types(
    specs: Specs,
    prefix = '',
    gen_parent_pointers = False
) -> PyModule:

    base_token_class_name = to_class_name('base_token', prefix)
    base_node_class_name = to_class_name('base_node', prefix)

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
        ]),
        PyTypeAliasStmt(
            to_class_name('syntax', prefix),
            build_union([
                PyNamedExpr(to_class_name('node', prefix)),
                PyNamedExpr(to_class_name('token', prefix))
            ])
        ),
        PyTypeAliasStmt(
            to_class_name('token', prefix),
            build_union(PyNamedExpr(to_class_name(spec.name, prefix)) for spec in specs if isinstance(spec, TokenSpec))
        ),
        PyTypeAliasStmt(
            to_class_name('node', prefix),
            build_union(PyNamedExpr(to_class_name(spec.name, prefix)) for spec in specs if isinstance(spec, NodeSpec))
        ),
        PyClassDef(
            name=base_token_class_name,
            body=PyExprStmt(PyEllipsisExpr()),
        ),
        PyClassDef(
            name=base_node_class_name,
            body=PyExprStmt(PyEllipsisExpr()),
        ),
    ]

    defs = {}

    for spec in specs:

        if isinstance(spec, NodeSpec):

            this_class_name = to_class_name(spec.name, prefix)

            body: list[PyStmt] = []

            derive_params = [
                PyNamedParam(PyNamedPattern('self')),
                PySepParam(),
            ]

            init_required = []
            init_optional = []

            for field in spec.fields:
                param_type, _ = gen_initializers(field.ty, PyNamedExpr('_'), defs=defs, specs=specs, prefix=prefix)
                param_type_str = emit(gen_py_type(param_type, prefix))
                body.append(PyAssignStmt(
                    PyNamedPattern(field.name),
                    annotation=quote_py_type(gen_py_type(field.ty, prefix=prefix)),
                ))
                if is_optional(param_type):
                    derive_params.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=PyConstExpr(literal=param_type_str),
                        default=PyNamedExpr('None')
                    ))
                    init_optional.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=PyConstExpr(literal=param_type_str),
                        default=PyNamedExpr('None')
                    ))
                else:
                    derive_params.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=quote_py_type(gen_py_type(make_optional(param_type), prefix=prefix)),
                        default=PyNamedExpr('None')
                    ))
                    init_required.append(PyNamedParam(
                        pattern=PyNamedPattern(field.name),
                        annotation=PyConstExpr(param_type_str),
                    ))

            init_params = [
                PyNamedParam(PyNamedPattern('self')),
                *init_required,
            ]

            if init_optional:
                init_params.append(PySepParam())
                init_params.extend(init_optional)

            body.append(PyFuncDef(
                name='derive',
                params=derive_params,
                return_type=PyNamedExpr(this_class_name),
                body=PyExprStmt(PyEllipsisExpr()),
            ))

            body.append(
                PyFuncDef(
                    name='__init__',
                    params=init_params,
                    body=PyExprStmt(PyEllipsisExpr()),
                )
            )

            if gen_parent_pointers:
                body.append(PyAssignStmt(
                    PyNamedPattern('parent'),
                    annotation=PyNamedExpr(this_class_name + 'Parent'),
                ))

            stmts.append(PyClassDef(
                name=this_class_name,
                bases=[ base_token_class_name ],
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
                    body=PyExprStmt(PyEllipsisExpr()),
                ),
            ]

            if not spec.is_static:
                body.append(PyAssignStmt(PyNamedPattern('value'), annotation=rule_type_to_py_type(spec.field_type)))

            stmts.append(PyClassDef(
                name=to_class_name(spec.name, prefix),
                bases=[ base_token_class_name ],
                body=body,
            ))

    def build_instance_pred(name: str) -> PyStmt:
        return PyFuncDef(
            name=f'is_{namespaced(name, prefix)}',
            params=[ PyNamedParam(PyNamedPattern('value'), annotation=PyNamedExpr('Any')) ],
            return_type=PySubscriptExpr(PyNamedExpr('TypeGuard'), [ PyNamedExpr(to_class_name(name, prefix)) ]),
            body=PyExprStmt(PyEllipsisExpr()),
        )

    for spec in specs:
        if not isinstance(spec, VariantSpec):
            continue
        this_class_name = to_class_name(spec.name, prefix)
        assert(len(spec.members) > 0)
        stmts.append(PyTypeAliasStmt(this_class_name, build_union(gen_py_type(ty, prefix) for _, ty in spec.members)))
        stmts.append(build_instance_pred(spec.name))
        continue

    stmts.append(build_instance_pred('syntax'))
    stmts.append(build_instance_pred('node'))
    stmts.append(build_instance_pred('token'))

    return PyModule(stmts=stmts)
