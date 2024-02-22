from typing import Iterator, assert_never
import ast
import astor
from magelang.repr import *

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def generate_cst(grammar: Grammar, prefix='') -> str:

    specs = grammar_to_specs(grammar)

    def namespace(name: str) -> str:
        return prefix + name if prefix else name

    def to_class_case(name: str) -> str:
        return to_camel_case(namespace(name))

    def gen_type(ty: Type) -> ast.expr:
        if isinstance(ty, NodeType):
            return ast.Name(to_class_case(ty.name))
        if isinstance(ty, TokenType):
            return ast.Name(to_class_case(ty.name))
        if  isinstance(ty, AnyTokenType):
            return ast.Name('Token', ctx=ast.Load())
        if isinstance(ty, ListType):
            return ast.Subscript(value=ast.Name('list', ctx=ast.Load()), slice=gen_type(ty.element_type), ctx=ast.Load())
        if isinstance(ty, TupleType):
            return ast.Subscript(value=ast.Name('tuple', ctx=ast.Load()), slice=ast.Tuple(list(gen_type(element) for element in ty.element_types), ctx=ast.Load()), ctx=ast.Load())
        if isinstance(ty, UnionType):
            out = gen_type(ty.types[0])
            for element in ty.types[1:]:
                out = ast.BinOp(left=out, op=ast.BitOr(), right=gen_type(element), ctx=ast.Load())
            return out
        if isinstance(ty, ExternType):
            return rule_type_to_py_type(ty.name)
        if isinstance(ty, NoneType):
            return ast.Name('None', ctx=ast.Load())
        raise RuntimeError(f'unexpected {ty}')

    def is_optional(ty: Type) -> bool:
        # if isinstance(ty, NoneType):
        #     return True
        if isinstance(ty, UnionType):
            for element in flatten_union(ty):
                if isinstance(element, NoneType):
                    return True
        return False

    def gen_default_constructor(ty: Type) -> ast.expr:
        if isinstance(ty, NodeType) or isinstance(ty, TokenType):
            return ast.Call(func=ast.Name(to_class_case(ty.name)), args=[], keywords=[])
        if isinstance(ty, ListType):
            return ast.Call(func=ast.Name('list'), args=[], keywords=[])
        raise RuntimeError(f'unexpected {ty}')

    def make_or(iter: Iterator[ast.expr]) -> ast.expr:
        try:
            out = next(iter)
        except StopIteration:
            return ast.Name('False')
        for expr in iter:
            out = ast.BoolOp(op=ast.Or(), values=[ out, expr ])
        return out

    def make_and(iter: Iterator[ast.expr]) -> ast.expr:
        try:
            out = next(iter)
        except StopIteration:
            return ast.Name('True')
        for expr in iter:
            out = ast.BoolOp(op=ast.And(), values=[ out, expr ])
        return out

    def make_bitor(it: list[ast.expr] | Iterator[ast.expr]) -> ast.expr:
        if isinstance(it, list):
            it = iter(it)
        out = next(it)
        for element in it:
            out = ast.BinOp(left=out, op=ast.BitOr(), right=element, ctx=ast.Load())
        return out

    def gen_instance_check(name: str, target: ast.expr) -> ast.expr:
        spec = specs.lookup(name)
        if isinstance(spec, VariantSpec):
            return ast.Call(func=ast.Name(f'is_{namespace(name)}'), args=[ target ], keywords=[])
        if isinstance(spec, NodeSpec) or isinstance(spec, TokenSpec):
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name(to_class_case(name)) ], keywords=[])
        raise RuntimeError(f'unexpected {spec}')

    def gen_shallow_test(ty: Type, target: ast.expr) -> ast.expr:
        if isinstance(ty, NodeType):
            return gen_instance_check(ty.name, target)
        if isinstance(ty, TokenType):
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name(to_class_case(ty.name)) ], keywords=[])
        if isinstance(ty, NoneType):
            return ast.Compare(left=target, ops=[ ast.Is() ], comparators=[ ast.Name('None') ])
        if isinstance(ty, TupleType):
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('tuple') ], keywords=[])
            #return ast.BoolOp(left=test, op=ast.And(), values=[ make_and(gen_test(element, ast.Subscript(target, ast.Constant(i))) for i, element in enumerate(ty.element_types)) ])
        if isinstance(ty, ListType):
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('list') ], keywords=[])
        if isinstance(ty, UnionType):
            return make_or(gen_shallow_test(element, target) for element in ty.types)
        if isinstance(ty, ExternType):
            return gen_rule_type_test(ty.name, target)
        raise RuntimeError(f'unexpected {ty}')

    counter = 0
    def generate_temporary(prefix='temp_') -> str:
        nonlocal counter
        i = counter
        counter += 1
        return prefix + str(i)

    def get_list_element(ty: Type) -> Type:
        if isinstance(ty, ListType):
            return ty.element_type
        if isinstance(ty, UnionType):
            list_types = []
            for element in flatten_union(ty):
                if isinstance(element, ListType):
                    list_types.append(element.element_type)
            assert(len(list_types) == 1)
            return list_types[0]
        raise RuntimeError(f'unexpected {ty}')

    def get_tuple_element(ty: Type, i: int) -> Type:
        if isinstance(ty, TupleType):
            return ty.element_types[i]
        if isinstance(ty, UnionType):
            for element in flatten_union(ty):
                if isinstance(element, TupleType):
                    return element.element_types[i]
        raise RuntimeError(f'unexpected {ty}')

    def gen_rule_type_test(type_name: str, target: ast.expr) -> ast.expr:
        if type_name == 'String':
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('str') ], keywords=[])
        if type_name == 'Integer':
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('int') ], keywords=[])
        if type_name == 'Float32':
            warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('float') ], keywords=[])
        if type_name == 'Float' or type_name == 'Float64':
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name('float') ], keywords=[])
        raise RuntimeError(f"unexpected rule type '{type_name}'")

    def rule_type_to_py_type(type_name: str) -> ast.expr:
        if type_name == 'String':
            return ast.Name('str')
        if type_name == 'Integer':
            return ast.Name('int')
        if type_name == 'Float32':
            warn('No exact representation for Float32 was found, so we are falling back to 64-bit Python float type')
            return ast.Name('float')
        if type_name == 'Float' or type_name == 'Float64':
            return ast.Name('float')
        raise RuntimeError(f"unexpected rule type '{type_name}'")

    def make_cond(cases: list[tuple[ast.expr | None, list[ast.stmt]]]) -> list[ast.stmt]:
        if len(cases) == 0:
            return []
        if len(cases) == 1 and cases[0][0] is None:
            return cases[0][1]
        else:
            c_0 = cases[0]
            test = c_0[0]
            assert(test is not None)
            return [ ast.If(test=test, body=c_0[1], orelse=make_cond(cases[1:])) ]

    def gen_init_body(field_name: str, field_type: Type, in_name: str, assign: Callable[[ast.expr], ast.stmt], stmts: list[ast.stmt]) -> Type:

        def visit(ty: Type, in_name: str, assign: Callable[[ast.expr], ast.stmt], stmts: list[ast.stmt], has_none: bool) -> tuple[Type, bool]:
            """
            This function returns a new type and a boolean indicating whether any coercions have been added.
            """

            if isinstance(ty, NodeType):
                #assert(ty == orig_ty)
                coerced_types = []
                coerced_types.append(ty)
                # FIXME this should probably be behind an if-statemnet
                stmts.append(assign(ast.Name(in_name, ctx=ast.Load())))
                spec = specs.lookup(ty.name)
                coercable = False
                # spec can also be a VariantSpec so we need to run isinstance
                if isinstance(spec, NodeSpec) and len(spec.members) == 1:
                    # TODO maybe also coerce spec.members[0].ty?
                    coercable = True
                    first_ty = spec.members[0].ty
                    if_body = []
                    if_body.append(assign(ast.Call(ast.Name(to_class_case(ty.name)), args=[ ast.Name(in_name) ], keywords=[])))
                    stmts.append(ast.If(test=gen_shallow_test(first_ty, ast.Name(in_name)), body=if_body))
                    coerced_types.append(first_ty)
                return UnionType(coerced_types), coercable

            if isinstance(ty, NoneType):
                stmts.append(assign(ast.Name('None')))
                return ty, False

            if isinstance(ty, TokenType):
                coerced_types = []
                coerced_types.append(ty)
                spec = specs.lookup(ty.name)
                assert(isinstance(spec, TokenSpec))
                cases = []
                if spec.is_static:
                    if not has_none:
                        coerced_types.append(NoneType())
                        cases.append((
                            ast.Compare(ast.Name(in_name), [ ast.Is() ], [ ast.Name('None') ]),
                            [ assign(ast.Call(ast.Name(to_class_case(ty.name)), args=[], keywords=[])) ]
                        ))
                else:
                    coerced_types.append(ExternType(spec.field_type))
                    # out_name = Token(in_name)
                    cases.append((
                        gen_rule_type_test(spec.field_type, ast.Name(in_name)),
                        [ assign(ast.Call(ast.Name(to_class_case(ty.name)), args=[ ast.Name(in_name) ], keywords=[])) ]
                    ))
                # out_name = in_name
                cases.append((None, [ assign(ast.Name(in_name)) ]))
                stmts.extend(make_cond(cases))
                return UnionType(coerced_types), True 

            if isinstance(ty, ListType):
                # out_name = list()
                # for element in in_name:
                #     ...
                #     out_name.append(new_element_name)
                coercable_types = []
                cases = []
                orelse = []
                for_body = []

                new_elements_name = f'new_{in_name}'
                element_name = f'{in_name}_element'
                new_element_name = f'new_{in_name}_element'

                if not has_none:
                    coercable_types.append(NoneType())
                    cases.append((
                        ast.Compare(left=ast.Name(in_name), ops=[ ast.Is() ], comparators=[ ast.Name('None') ]),
                        [ assign(ast.Call(func=ast.Name('list'), args=[], keywords=[])) ]
                    ))

                orelse.append(ast.Assign(targets=[ ast.Name(new_elements_name) ], value=ast.Name(ast.Call(func=ast.Name('list'), args=[], keywords=[]))))

                element_assign = lambda value, name=new_element_name: ast.Assign(targets=[ ast.Name(name) ], value=value)
                element_type, element_coercable = visit(ty.element_type, element_name, element_assign, for_body, False)

                coercable_types.append(ListType(element_type))

                for_body.append(ast.Expr(ast.Call(func=ast.Attribute(value=ast.Name(new_elements_name), attr='append'), args=[ ast.Name(new_element_name) ], keywords=[])))
                orelse.append(ast.For(target=ast.Name(element_name), iter=ast.Name(in_name), body=for_body, orelse=None))

                orelse.append(assign(ast.Name(new_elements_name)))

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
                coerced_types = []
                cases = []
                required = []

                for element_type in ty.element_types:
                    # TODO might be posssible to use is_default_constructible
                    if not is_optional(element_type):
                        required.append(element_type)

                if len(required) == 1:

                    case_body = []

                    first_type = required[0]

                    coercable = True
                    def first_assign(value):
                        assert(isinstance(ty, TupleType)) # Needed to keep Pyright happy
                        return assign(ast.Tuple(list(value if ty == first_type else ast.Name('None') for ty in ty.element_types)))
                    new_first_type, _ = visit(first_type, in_name, first_assign, case_body, False)
                    coerced_types.append(new_first_type)
                    cases.append((
                        gen_shallow_test(first_type, ast.Name(in_name)),
                        #ast.Compare(left=ast.Name(in_name), ops=[ ast.Is() ], comparators=[ ast.Name('None') ]),
                        case_body
                    ))

                orelse = []
                new_elements = []
                new_element_types = []

                for i, element_type in enumerate(ty.element_types):

                    element_name = f'{in_name}_{i}'
                    new_element_name = f'new_{in_name}_{i}'
                    element_assign = lambda value, name=new_element_name: ast.Assign(targets=[ ast.Name(name) ], value=value)

                    new_elements.append(ast.Name(new_element_name))

                    orelse.append(ast.Assign(targets=[ ast.Name(element_name) ], value=ast.Subscript(value=ast.Name(in_name), slice=ast.Constant(i))))

                    new_element_type, element_coercable = visit(element_type, element_name, element_assign, orelse, False)

                    if element_coercable:
                        coercable = True

                    new_element_types.append(new_element_type)


                orelse.append(assign(ast.Tuple(elts=new_elements)))
                cases.append((None, orelse))
                coerced_types.append(TupleType(new_element_types))

                stmts.extend(make_cond(cases))

                return UnionType(coerced_types), coercable

            if isinstance(ty, UnionType):

                coercable = False
                coerced_types = []
                cases = []

                for element_type in ty.types:
                    if isinstance(element_type, NoneType):
                        has_none = True
                        break

                for element_type in ty.types:
                    body = [] 
                    new_type, element_coercable = visit(element_type, in_name, assign, body, has_none)
                    if element_coercable:
                        coercable = True
                    coerced_types.append(new_type)
                    cases.append((
                        gen_shallow_test(new_type, ast.Name(in_name)),
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
                    [ ast.Raise(exc=ast.Call(func=ast.Name('ValueError', ctx=ast.Load()), args=[ ast.Constant(value=f"the field '{field_name}' received an unrecognised value'") ], keywords=[])) ]
                ))

                if coercable:
                    stmts.extend(make_cond(cases))
                else:
                    stmts.append(assign(ast.Name(in_name)))

                # ty_0 = ty.types[0]
                # ty_n = ty.types[1:]
                # if_body = []
                # new_ty_0 = visit(ty_0, in_name, out_name, if_body)
                # if_orelse = []
                # new_rest = visit(UnionType(ty_n), in_name, out_name, if_orelse)
                # stmts.append(ast.If(test=gen_shallow_test(ty_0, ast.Name(in_name)), body=if_body, orelse=if_orelse))

                return UnionType(coerced_types), coercable

            raise RuntimeError(f'unexpected {ty}')

        ty, _ = visit(field_type, in_name, assign, stmts, False)
        return ty

    stmts = []

    for spec in specs:

        if isinstance(spec, NodeSpec):

            body = []
            params = []
            params_defaults = []
            init_body = []

            for field in spec.members:

                # param_type = get_coerce_type(field.ty)
                # tmp = f'{field.name}__coerced'

                assign = lambda value, field=field: ast.AnnAssign(ast.Attribute(value=ast.Name('self'), attr=field.name), gen_type(field.ty), value)
                param_type = gen_init_body(field.name, field.ty, field.name, assign, init_body)

                field_ty = astor.to_source(gen_type(param_type)).strip()
                params.append(ast.arg(arg=field.name, annotation=ast.Constant(field_ty)))
                if is_optional(param_type):
                    # init_body.append(ast.If(test=ast.Compare(left=ast.Name(tmp), ops=[ ast.IsNot() ], comparators=[ ast.Name('None') ]), body=[
                    #     ast.Assign(targets=[ ast.Name(tmp) ], value=gen_default_constructor(field.ty))
                    # ], orelse=[]))
                    params_defaults.append(ast.Name('None'))
                else:
                    params_defaults.append(None)

            args = ast.arguments(args=[ ast.arg('self') ], kwonlyargs=params, defaults=[], kw_defaults=params_defaults)
            body.append(ast.FunctionDef(name='__init__', args=args, body=init_body, returns=ast.Name('None', ctx=ast.Load()), decorator_list=[]))

            #for field in element.members:
            #     body.append(ast.AnnAssign(target=ast.Name(field.name), annotation=gen_type(field.ty), simple=True))

            stmts.append(ast.ClassDef(name=to_class_case(spec.name), body=body, bases=[ ast.Name('Node', ctx=ast.Store()) ], decorator_list=[]))

            continue

        if isinstance(spec, TokenSpec):

            body = []

            if spec.is_static:

                body.append(ast.Pass())

            else:

                init_body = []

                init_body.append(ast.Expr(ast.Call(ast.Attribute(ast.Call(ast.Name('super'), args=[], keywords=[]), '__init__'), args=[], keywords=[ ast.keyword('span', ast.Name('span')) ])))

                args = [ ast.arg('self') ]
                defaults: list[ast.expr | None] = [ None ]

                args.append(ast.arg('value', make_bitor([ rule_type_to_py_type(spec.field_type), ast.Name('None') ])))
                defaults.append(ast.Name('None'))

                args.append(ast.arg('span', make_bitor([ ast.Name('Span'), ast.Name('None') ])))
                defaults.append(ast.Name('None'))

                arguments = ast.arguments(args=args, defaults=defaults)

                init_body.append(ast.Assign([ ast.Attribute(ast.Name('self'), 'value') ], ast.Name('value')))

                body.append(ast.FunctionDef(name='__init__', args=arguments, body=init_body, decorator_list=[]))

            stmts.append(ast.ClassDef(name=to_class_case(spec.name), bases=[ ast.Name('Token') ], body=body, decorator_list=[]))

            continue

        if isinstance(spec, VariantSpec):
            # ty = ast.Name(to_class_case(element.members[0]))
            # for name in element.members[1:]:
            #     ty = ast.BinOp(left=ty, op=ast.BitOr(), right=ast.Name(to_class_case(name)), ctx=ast.Load())

            cls_name = to_class_case(spec.name)

            assert(len(spec.members) > 0)
            text = ' | '.join(to_class_case(name) for name in spec.members)
            stmts.append(ast.AnnAssign(target=ast.Name(cls_name),  value=ast.Constant(text), annotation=ast.Name('TypeAlias'), simple=True))

            args = ast.arguments(args=[ ast.arg(arg='value', annotation=ast.Name('Any')) ], defaults=[])
            stmts.append(ast.FunctionDef(
                name=f'is_{namespace(spec.name)}',
                args=args,
                returns=ast.Subscript(ast.Name('TypeGuard'), ast.Name(cls_name)),
                body=[
                    ast.Return(make_or(gen_instance_check(name, ast.Name('value')) for name in spec.members))
                ],
                decorator_list=[]
            ))

            continue

        assert_never(spec)

    return astor.to_source(ast.Module(body=stmts))

def generate_lexer_logic(grammar: Grammar) -> str:
    stmts = []
    for rule in grammar.rules:
        if not rule.is_token:
            continue
    return astor.to_source(ast.Module(body=stmts))

