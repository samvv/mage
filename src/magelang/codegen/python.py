
import ast
from typing import assert_never
import astor

from ..ast import Grammar
from ..repr import *

type Files = dict[str, str]

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def generate_cst(grammar: Grammar) -> Files:

    to_class_case = to_camel_case

    def gen_type(ty: Type) -> ast.expr:
        if isinstance(ty, OptionType):
            return ast.BinOp(left=gen_type(ty.element_type), op=ast.BitOr(), right=ast.Name('None', ctx=ast.Load()))
        if isinstance(ty, NodeType):
            return ast.Name(to_class_case(ty.name), ctx=ast.Load())
        if isinstance(ty, TokenType):
            return ast.Name(to_class_case(ty.name), ctx=ast.Load())
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
        raise RuntimeError(f'unexpected {ty}')

    spec = grammar_to_nodespec(grammar)
    stmts = []
    for element in spec:
        if isinstance(element, NodeSpec):
            body = []
            for field in element.members:
                body.append(ast.AnnAssign(target=ast.Name(field.name), annotation=gen_type(field.ty), simple=True))
            stmts.append(ast.ClassDef(name=to_class_case(element.name), body=body, bases=[ ast.Name('Node', ctx=ast.Store()) ], decorator_list=[]))
            continue
        if isinstance(element, TokenSpec):
            body = []
            body.append(ast.Pass())
            stmts.append(ast.ClassDef(name=to_class_case(element.name), bases=[ ast.Name('Token') ], body=body, decorator_list=[]))
            continue
        if isinstance(element, VariantSpec):
            ty = ast.Name(to_class_case(element.members[0]))
            for name in element.members[1:]:
                ty = ast.BinOp(left=ty, op=ast.BitOr(), right=ast.Name(to_class_case(name)), ctx=ast.Load())
            stmts.append(ast.Assign(targets=[ ast.Name(to_class_case(element.name), ctx=ast.Store()) ], value=ty))
            continue
        assert_never(element)
    mod = ast.Module(body=stmts)
    return {
        'cst.py': astor.to_source(mod),
        }

