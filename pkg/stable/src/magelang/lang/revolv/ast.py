
from dataclasses import dataclass
from typing import Any, NewType, Sequence, TypeGuard

type BodyElement = Expr | FuncDecl | VarDecl

type Body = Sequence[BodyElement]

@dataclass
class ExprBase:
    pass

type Expr = BreakExpr | CondExpr | LitExpr | CallExpr | PathExpr | TupleExpr | TupleIndexExpr | RetExpr | NewExpr | ForExpr | AssignExpr | LoopExpr | MatchExpr | BlockExpr | SpecialExpr | EnumExpr

type SpecialExpr = IsExpr | FieldAssignExpr

def is_expr(value: Any) -> TypeGuard[Expr]:
    return isinstance(value, ExprBase)

type Type = AnyType | NeverType | PathType | TupleType | UnionType | NoneType

@dataclass
class TypeBase:
    pass

@dataclass
class NoneType(TypeBase):
    pass

@dataclass
class PathType(TypeBase):
    name: str
    args: Sequence[Type] | None = None

@dataclass
class TupleType(TypeBase):
    types: Sequence[Type]

@dataclass
class AnyType(TypeBase):
    pass

@dataclass
class NeverType(TypeBase):
    pass

@dataclass
class UnionType(TypeBase):
    types: Sequence[Type]

@dataclass
class PattBase:
    pass

type Patt = NamedPatt | VariantPatt | TuplePatt

@dataclass
class NamedPatt(PattBase):
    name: str

@dataclass
class TuplePatt(PattBase):
    elements: Sequence[Patt]

@dataclass
class VariantPatt(PattBase):
    name: str
    members: Sequence[Patt]

@dataclass
class RetExpr(ExprBase):
    value: Expr | None

@dataclass
class MatchArm:
    patt: Patt
    expr: Expr

@dataclass
class BlockExpr(ExprBase):
    body: Body
    last: Expr | None = None

    def derive(self, **kwargs) -> 'BlockExpr':
        body = self.body if 'body' not in kwargs else kwargs['body']
        last = self.last if 'last' not in kwargs else kwargs['last']
        return BlockExpr(body=body, last=last)

@dataclass
class MatchExpr(ExprBase):
    value: Expr
    arms: Sequence[MatchArm]

@dataclass
class PathExpr(ExprBase):
    name: str

@dataclass
class BreakExpr(ExprBase):
    value: Expr | None = None

@dataclass
class CallExpr(ExprBase):
    func: Expr
    args: Sequence[Expr]

@dataclass
class NewExpr(ExprBase):
    name: str
    args: Sequence[Expr]

@dataclass
class EnumExpr(ExprBase):
    name: str
    args: Sequence[Expr]

@dataclass
class IsExpr(ExprBase):
    expr: Expr
    name: str

@dataclass
class LitExpr(ExprBase):
    value: str | int | bool

@dataclass
class TupleExpr(ExprBase):
    elements: Sequence[Expr]

@dataclass
class TupleIndexExpr(ExprBase):
    expr: Expr
    index: int

@dataclass
class FieldAssignExpr(ExprBase):
    name: str
    expr: Expr

@dataclass
class NoneExpr(ExprBase):
    pass

@dataclass
class IsNoneExpr(ExprBase):
    value: Expr

@dataclass
class AssignExpr(ExprBase):
    patt: Patt
    expr: Expr

@dataclass
class ForExpr(ExprBase):
    patt: Patt
    iter: Expr
    body: Body

@dataclass
class ListExpr(ExprBase):
    elements: Sequence[Expr]

@dataclass
class Param:
    name: str
    ty: Type
    default: Expr | None = None

@dataclass
class CondCase:
    test: Expr
    body: Expr

@dataclass
class CondExpr(ExprBase):
    cases: Sequence[CondCase]

@dataclass
class LoopExpr(ExprBase):
    body: Body

VisFlags = NewType('VisFlags', int)

PRIVATE = VisFlags(0)
PUBLIC = VisFlags(1)

@dataclass
class FuncDecl:
    name: str
    params: Sequence[Param]
    returns: Type
    body: Body
    self: str | None = None
    flags: VisFlags = PRIVATE

class VarDecl:
    name: str
    is_mut: bool = False
    expr: Expr | None = None
    ty: Type | None = None
    flags: VisFlags = PRIVATE

@dataclass
class Field:
    name: str
    ty: Type

@dataclass
class StructDecl:
    name: str
    fields: Sequence[Field]
    flags: VisFlags = PRIVATE

@dataclass
class Variant:
    name: str
    ty: Type

@dataclass
class EnumDecl:
    name: str
    variants: Sequence[Variant]

type ProgramElement = StructDecl | EnumDecl | FuncDecl | VarDecl | Expr

@dataclass
class Program:
    elements: Sequence[ProgramElement]

    def derive(self, **kwargs) -> 'Program':
        elements = self.elements if 'elements' not in kwargs else kwargs['elements']
        return Program(elements=elements)

type Node = Program | EnumDecl | StructDecl | FuncDecl | VarDecl | Expr | Type | Field | Variant | Param
