from typing import Iterator, assert_never
import ast
import astor
from magelang.repr import *

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def generate_cst(grammar: Grammar, prefix='') -> str:

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
        if isinstance(ty, NoneType):
            return ast.Name('None', ctx=ast.Load())
        raise RuntimeError(f'unexpected {ty}')

    def yield_coerce_options(ty: Type) -> Generator[Type, None, None]:
        if isinstance(ty, UnionType):
            for element in ty.types:
                yield from yield_coerce_options(element)
            return
        if isinstance(ty, NoneType):
            yield NoneType()
            return
        if isinstance(ty, TokenType):
            if ty.is_singleton:
                yield NoneType()
            yield ty
            return
        if isinstance(ty, NodeType):
            yield ty
            # TODO yield first field if there is only one non-singleton field
            return
        if isinstance(ty, ListType):
            yield ListType(gen_coerce_type(ty.element_type))
            return
        if isinstance(ty, TupleType):
            yield TupleType(list(gen_coerce_type(element_ty) for element_ty in ty.element_types))
            return
        if isinstance(ty, AnyTokenType) or isinstance(ty, AnyNodeType):
            yield ty
            return
        raise RuntimeError(f'unexpected {ty}')

    def gen_coerce_type(ty: Type) -> Type:
        candidates = list(yield_coerce_options(ty))
        elements = []
        has_none = False
        for candidate in candidates:
            for element in flatten_union(candidate):
                if isinstance(element, NoneType):
                    has_none = True
                    continue
                elements.append(element)
        if has_none:
            elements.append(NoneType())
        if len(elements) == 1:
            return elements[0]
        return UnionType(elements)

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

    def gen_shallow_test(ty: Type, target: ast.expr) -> ast.expr:
        if isinstance(ty, NodeType):
            return ast.Call(func=ast.Name('isinstance'), args=[ target, ast.Name(to_class_case(ty.name)) ], keywords=[])
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
        raise RuntimeError(f'unexpected {ty}')

    counter = 0
    def generate_temporary(prefix='temp_') -> str:
        nonlocal counter
        i = counter
        counter += 1
        return prefix + str(i)

    def gen_init_body(ty: Type, field_name: str, in_name: str, out_name: str) -> Generator[ast.stmt, None, None]:
        if isinstance(ty, NodeType) or isinstance(ty, TokenType):
            #assert(ty == orig_ty)
            yield ast.Assign(targets=[ ast.Name(out_name) ], value=ast.Name(in_name, ctx=ast.Load()))
            return
        if isinstance(ty, NoneType):
            yield ast.Assign(targets=[ ast.Name(out_name) ], value=ast.Name('None'))
            # yield ast.Assign(targets=[ ast.Name(out_name) ], value=gen_default_constructor(orig_ty))
            return
        if isinstance(ty, ListType):
            # out_name = list()
            # for element in in_name:
            #     ...
            #     out_name.append(new_element_name)
            yield ast.Assign(targets=[ ast.Name(out_name) ], value=ast.Call(func=ast.Name('list'), args=[], keywords=[]))
            element_name = f'{in_name}_element'
            new_element_name = f'{out_name}_element'
            for_body = list(gen_init_body(ty.element_type, field_name, element_name, new_element_name))
            for_body.append(ast.Expr(ast.Call(func=ast.Attribute(value=ast.Name(out_name), attr='append'), args=[ ast.Name(new_element_name) ], keywords=[])))
            yield ast.For(target=ast.Name(element_name), iter=ast.Name(in_name), body=for_body, orelse=None)
            return
        if isinstance(ty, TupleType):
            # element_0 = field[0]
            # new_element_0 = ...
            # ...
            # out_name = (new_element_0, new_element_1, ...)
            new_elements = []
            for i, element_type in enumerate(ty.element_types):
                element_name = f'{in_name}_{i}'
                new_element_name = f'{out_name}_{i}'
                new_elements.append(ast.Name(new_element_name))
                yield ast.Assign(targets=[ ast.Name(element_name) ], value=ast.Subscript(value=ast.Name(in_name), slice=ast.Constant(i)))
                yield from gen_init_body(element_type, field_name, element_name, new_element_name)
            yield ast.Assign(targets=[ ast.Name(out_name) ], value=ast.Tuple(elts=new_elements))
            return
        if isinstance(ty, UnionType):
            if not ty.types:
                yield ast.Raise(exc=ast.Call(func=ast.Name('ValueError', ctx=ast.Load()), args=[ ast.Constant(value=f"the field '{in_name}' received an unrecognised value'") ], keywords=[]))
                return
            ty0 = ty.types[0]
            if_body = list(gen_init_body(ty0, field_name, in_name, out_name))
            if_orelse = list(gen_init_body(UnionType(ty.types[1:]), field_name, in_name, out_name))
            yield ast.If(test=gen_shallow_test(ty0, ast.Name(in_name)), body=if_body, orelse=if_orelse)
            return
        raise RuntimeError(f'unexpected {ty}')

    spec = grammar_to_nodespec(grammar)
    stmts = []
    for element in spec:
        if isinstance(element, NodeSpec):
            body = []
            params = []
            params_defaults = []
            init_body = []
            for field in element.members:
                param_type = gen_coerce_type(field.ty)
                tmp = f'{field.name}__coerced'
                init_body.extend(gen_init_body(param_type, field.name, field.name, tmp))
                field_ty = astor.to_source(gen_type(param_type)).strip()
                params.append(ast.arg(arg=field.name, annotation=ast.Constant(field_ty)))
                if not is_optional(field.ty) and is_optional(param_type):
                    init_body.append(ast.If(test=ast.Compare(left=ast.Name(tmp), ops=[ ast.IsNot() ], comparators=[ ast.Name('None') ]), body=[
                        ast.Assign(targets=[ ast.Name(tmp) ], value=gen_default_constructor(field.ty))
                    ], orelse=[]))
                    params_defaults.append(ast.Name('None'))
                else:
                    params_defaults.append(None)
                init_body.append(ast.Assign(targets=[ ast.Attribute(value=ast.Name('self', ctx=ast.Store()), attr=field.name) ], value=ast.Name(tmp, ctx=ast.Load())))
            args = ast.arguments(args=[ ast.arg('self') ], kwonlyargs=params, defaults=[], kw_defaults=params_defaults)
            body.append(ast.FunctionDef(name='__init__', args=args, body=init_body, returns=ast.Name('None', ctx=ast.Load()), decorator_list=[]))
            #ctx for field in element.members:
            #     body.append(ast.AnnAssign(target=ast.Name(field.name), annotation=gen_type(field.ty), simple=True))
            stmts.append(ast.ClassDef(name=to_class_case(element.name), body=body, bases=[ ast.Name('Node', ctx=ast.Store()) ], decorator_list=[]))
            continue
        if isinstance(element, TokenSpec):
            body = []
            body.append(ast.Pass())
            stmts.append(ast.ClassDef(name=to_class_case(element.name), bases=[ ast.Name('Token') ], body=body, decorator_list=[]))
            continue
        if isinstance(element, VariantSpec):
            # ty = ast.Name(to_class_case(element.members[0]))
            # for name in element.members[1:]:
            #     ty = ast.BinOp(left=ty, op=ast.BitOr(), right=ast.Name(to_class_case(name)), ctx=ast.Load())
            assert(len(element.members) > 0)
            text = ' | '.join(to_class_case(name) for name in element.members)
            stmts.append(ast.Assign(targets=[ ast.Name(to_class_case(element.name)) ],  value=ast.Constant(text), type_comment='TypeAlias'))
            continue
        assert_never(element)
    return astor.to_source(ast.Module(body=stmts))

def generate_lexer_logic(grammar: Grammar) -> str:
    stmts = []
    for rule in grammar.rules:
        if not rule.is_token:
            continue
    return astor.to_source(ast.Module(body=stmts))

