
from typing import Iterable, Iterator

from magelang.lang.mage.ast import *
from magelang.analysis import can_be_empty
from magelang.manager import Pass, PassBase, pipeline
from magelang.lang.revolv.ast import *
from magelang.ir.constants import *
from magelang.util import NameGenerator, plural, to_snake_case, unreachable
from magelang.passes.mage_simplify import mage_simplify
from magelang.passes.mage_remove_hidden import mage_remove_hidden

# TODO accept list[str] as ident
# TODO decide on parameter order (curry style or imperative)

def mage_type_to_ir_type(name: str) -> Type:
    return PathType(to_snake_case(name))

def make_and(elements: Iterator[Expr]) -> Expr:
    out = LitExpr(True)
    for element in reversed(list(elements)):
        out = CallExpr(PathExpr(name_fn_and), [ element, out ])
    return out

def make_or(elements: Iterator[Expr]) -> Expr:
    out = LitExpr(True)
    for element in reversed(list(elements)):
        out = CallExpr(PathExpr(name_fn_or), [ element, out ])
    return out

def make_optional_type(ty: Type) -> Type:
    return UnionType([ ty, NoneType() ])

def make_none() -> Expr:
    return EnumExpr(name_variant_none, [])

def make_is_none(target: Expr) -> Expr:
    return CallExpr(PathExpr(name_fn_is_none), [ target ])

def make_array_type(element: Type) -> Type:
    return PathType(name_type_array, [ element ])

def is_array_type(ty: Type) -> bool:
    return isinstance(ty, PathType) and ty.name == name_type_array

def is_punct_type(ty: Type) -> bool:
    return isinstance(ty, PathType) and ty.name == name_type_punct

def make_empty_array() -> Expr:
    return NewExpr(name_type_array, [])

def make_empty_punct() -> Expr:
    return NewExpr(name_type_punct, [])

def gen_shallow_instance_check(target: Expr, ty: Type) -> Expr:
    if isinstance(ty, PathType):
        return IsExpr(target, ty.name)
    if isinstance(ty, TupleType):
        return make_and(gen_shallow_instance_check(TupleIndexExpr(target, i), el_ty) for i, el_ty in enumerate(ty.types))
    if isinstance(ty, AnyType):
        return LitExpr(True)
    if isinstance(ty, NeverType):
        return LitExpr(False)
    if isinstance(ty, UnionType):
        return make_or(gen_shallow_instance_check(target, el_ty) for el_ty in ty.types)
    if isinstance(ty, NoneType):
        return CallExpr(PathExpr(name_fn_is_none), [ target ])
    assert_never(ty)

def do_types_shallow_overlap(left: Type, right: Type) -> bool:
    if isinstance(left, NeverType) or isinstance(right, NeverType):
        return False
    if isinstance(left, AnyType) or isinstance(right, AnyType):
        return True
    if isinstance(left, NoneType) and isinstance(right, NoneType):
        return True
    if isinstance(left, TupleType) and isinstance(right, TupleType):
        return True
    if isinstance(left, PathType) and isinstance(right, PathType):
        return left.name == right.name
    if isinstance(left, UnionType):
        return any(do_types_shallow_overlap(ty, right) for ty in left.types)
    if isinstance(right, UnionType):
        return any(do_types_shallow_overlap(left, ty) for ty in right.types)
    return False

@dataclass
class FieldSpec:
    name: str
    ty: Type
    param_ty: Type
    coerced: Expr

def mangle_type(ty: Type) -> str:
    if isinstance(ty, PathType):
        out = 'path_' + ty.name # FIXME escape '_'
        if ty.args is not None:
            out += '_' + str(len(ty.args))
            for arg in ty.args:
                out += '_' + mangle_type(arg)
        return out
    if isinstance(ty, TupleType):
        out = 'tuple_' + str(len(ty.types))
        for el_ty in ty.types:
            out += '_' + mangle_type(el_ty)
        return out
    if isinstance(ty, UnionType):
        out = 'union_' + str(len(ty.types))
        for el_ty in ty.types:
            out += '_' + mangle_type(el_ty)
        return out
    if isinstance(ty, AnyType):
        return 'any'
    if isinstance(ty, NeverType):
        return 'never'
    if isinstance(ty, NoneType):
        return 'none'
    assert_never(ty)

class mage_to_revolv_syntax_tree(PassBase):

    def get_depends(self) -> Pass:
        return pipeline(mage_remove_hidden, mage_simplify)

    def apply(self, grammar: MageGrammar, prefix: str) -> Program:

        toplevel = list[ProgramElement]()

        defs = dict[str, FuncDecl]()

        def rename(name: str) -> str:
            return prefix + '_' + name if prefix else name

        def get_variant_name(expr: MageExpr) -> str:
            if expr.label is not None:
                return expr.label
            if isinstance(expr, MageRefExpr):
                rule = grammar.lookup(expr.name)
                if rule is None:
                    return expr.name
                if not rule.is_public and rule.expr is not None:
                    return get_variant_name(rule.expr)
                return rule.name
            if isinstance(expr, MageSeqExpr):
                return '_'.join(get_variant_name(element) for element in expr.elements)
            raise NotImplementedError()

        def make_unit_type() -> Type:
            return TupleType([])

        def make_punct_type(element: Type, separator: Type) -> Type:
            return PathType(name_type_punct, [ element, separator ])

        def infer_type(expr: MageExpr) -> Type:
            if isinstance(expr, MageRefExpr):
                rule = grammar.lookup(expr.name)
                if rule is None:
                    return AnyType()
                if not rule.is_public:
                    assert(rule.expr is not None)
                    return infer_type(rule.expr)
                return PathType(rename(rule.name))
            if isinstance(expr, MageSeqExpr):
                return TupleType(list(infer_type(element) for element in expr.elements))
            if isinstance(expr, MageChoiceExpr):
                return UnionType(list(infer_type(element) for element in expr.elements))
            if isinstance(expr, MageListExpr):
                return PathType(name_type_punct, [ infer_type(expr.element), infer_type(expr.separator) ])
            if isinstance(expr, MageRepeatExpr):
                if expr.min == 0 and expr.max == 1:
                    return PathType(name_type_optional, [ infer_type(expr.expr) ])
                return PathType(name_type_array, [ infer_type(expr.expr) ])
            if isinstance(expr, MageLitExpr):
                return make_unit_type()
            if isinstance(expr, MageHideExpr):
                return make_unit_type()
            if isinstance(expr, MageLookaheadExpr):
                return make_unit_type()
            if isinstance(expr, MageCharSetExpr):
                return PathType(name_type_string)
            assert_never(expr)

        def get_field_name(expr: MageExpr) -> str | None:
            if expr.label is not None:
                return expr.label
            if isinstance(expr, MageRefExpr):
                return expr.name
            if isinstance(expr, MageRepeatExpr):
                element_label = get_field_name(expr.expr)
                if element_label is not None:
                    if expr.max > 1:
                        return plural(element_label)
                    return element_label
                return None
            if isinstance(expr, MageListExpr):
                element_label = get_field_name(expr.element)
                if element_label is not None:
                    return plural(element_label)
                return None
            if isinstance(expr, MageCharSetExpr) or isinstance(expr, MageChoiceExpr):
                return None
            raise RuntimeError(f'unexpected {expr}')

        def is_default_constructible(expr: MageExpr) -> bool:
            if isinstance(expr, MageSeqExpr):
                return all(is_default_constructible(element) for element in expr.elements)
            if isinstance(expr, MageChoiceExpr):
                return False
            if isinstance(expr, MageHideExpr):
                unreachable()
            if isinstance(expr, MageLitExpr):
                return True
            if isinstance(expr, MageCharSetExpr):
                return len(expr) == 1
            if isinstance(expr, MageRepeatExpr):
                # We allow the default creation of the empty array
                return expr.min == 0
            if isinstance(expr, MageListExpr):
                # We allow the default creation of the empty punctuated type
                return expr.min_count == 0
            if isinstance(expr, MageRefExpr):
                rule = grammar.lookup(expr.name)
                if rule is None or rule.is_extern:
                    return False
                assert(rule.is_public)
                assert(rule.expr is not None)
                if grammar.is_token_rule(rule):
                    return grammar.is_static_token_rule(rule)
                return is_default_constructible(rule.expr)
            if isinstance(expr, MageLookaheadExpr):
                return True
            assert_never(expr)

        def gen_default_constructor(expr: MageExpr) -> Expr:
            if isinstance(expr, MageSeqExpr):
                return TupleExpr(list(gen_default_constructor(element) for element in expr.elements))
            if isinstance(expr, MageListExpr):
                assert(expr.min_count == 0)
                return make_empty_array()
            if isinstance(expr, MageRefExpr):
                return CallExpr(PathExpr(rename(expr.name)), [])
            unreachable()

        def gen_coerce_expr(expr: MageExpr, value: Expr) -> tuple[Type, Expr]:

            value_param_name = 'value'

            def gen_coerce_call(expr: MageExpr, value: Expr, allow_none: bool) -> tuple[Type, Expr]:

                ty = infer_type(expr)
                cases = list[CondCase]()
                types = list[Type]()
                for coerce_ty, coerce_body in gen_coerce_fn_body(expr, allow_none):
                    cases.append(CondCase(gen_shallow_instance_check(PathExpr(value_param_name), coerce_ty), BlockExpr(coerce_body)))
                    types.append(coerce_ty)

                coerced_ty = UnionType(types)

                fn_name = f'coerce_{mangle_type(coerced_ty)}_to_{mangle_type(ty)}'

                if fn_name not in defs:
                    defs[fn_name] = FuncDecl(
                        name=fn_name,
                        params=[ Param(value_param_name, coerced_ty) ],
                        returns=ty,
                        body=[ CondExpr(cases) ]
                    )

                return coerced_ty, CallExpr(PathExpr(fn_name), [ value ])

            def gen_coerce_fn_body(expr: MageExpr, allow_coerce_from_none: bool) -> Generator[tuple[Type, Body]]:

                if isinstance(expr, MageChoiceExpr):

                    elements = list(flatten_choice(expr))

                    has_none = False
                    for element in elements:
                        if can_be_empty(element, grammar=grammar):
                            has_none = True

                    # Gather all possible coercions, recording or skipping those that overlap
                    rejected = set()
                    results = []
                    for element in elements:
                        for coerced_type, coerced_stmts in gen_coerce_fn_body(element, False):
                            reject = False
                            for i, (ty, _) in enumerate(results):
                                if do_types_shallow_overlap(ty, coerced_type):
                                    rejected.add(i) # Type at index i will be removed
                                    reject = True
                                    continue
                            if not reject:
                                results.append((coerced_type, coerced_stmts))

                    # Omit those coercions that conflict with another type
                    yield from ((ty, stmts) for i, (ty, stmts) in enumerate(results) if i not in rejected)

                    if has_none:
                        yield NoneType(), [ RetExpr(make_none()) ]

                    return

                if allow_coerce_from_none and is_default_constructible(expr):
                    yield NoneType(), [ RetExpr(make_none()) ]

                if isinstance(expr, MageRefExpr):

                    rule = grammar.lookup(expr.name)

                    if rule is None or rule.expr is None:
                        return

                    # Rules have already been inlined at this point
                    assert(rule.is_public)

                    yield PathType(rename(rule.name)), [ RetExpr(PathExpr(value_param_name)) ]

                    if grammar.is_token_rule(rule):
                        if not grammar.is_static_token_rule(rule):
                            yield mage_type_to_ir_type(rule.type_name), [
                                RetExpr(NewExpr(rename(rule.name), [ PathExpr(value_param_name) ]))
                            ]
                        return

                    if grammar.is_variant_rule(rule):
                        return

                    optional, required = split_fields(rule.expr)

                    if not required:

                        if allow_coerce_from_none:
                            yield NoneType(), [ RetExpr(NewExpr(rename(rule.name), [])) ]

                    elif len(required) == 1:

                        main = required[0]
                        coerce_ty, coerce_expr = gen_coerce_call(main, PathExpr(value_param_name), allow_coerce_from_none)
                        yield coerce_ty, [ RetExpr(NewExpr(rename(rule.name), [ coerce_expr ])) ]

                    return

                if isinstance(expr, MageListExpr):

                    assert(is_default_constructible(expr.separator))

                    new_elements_name = 'new_elements'
                    elements_iter_name = 'iterator'
                    first_element_name = 'first_element'
                    second_element_name = 'second_element'
                    separator_name = 'separator'
                    value_name = 'value'
                    new_value_name = 'new_value'
                    new_separator_name = 'new_separator'

                    if grammar.is_static(expr.element):
                        yield PathType(name_type_integer), [
                            AssignExpr(NamedPatt(new_elements_name), make_empty_punct()),
                            ForExpr(NamedPatt('_'), CallExpr(PathExpr(name_fn_range), [ LitExpr(0), PathExpr(value_param_name) ]), [
                                # FIXME does not append the separator
                                CallExpr(PathExpr(name_fn_punct_append), [ PathExpr(new_elements_name), gen_default_constructor(expr.element) ])
                            ]),
                            RetExpr(PathExpr(new_elements_name))
                        ]

                    value_type, value_expr = gen_coerce_call(expr.element, PathExpr(value_name), False)
                    separator_type, separator_expr = gen_coerce_call(expr.separator, PathExpr(separator_name), False)

                    coerced_type = UnionType([
                        make_array_type(value_type),
                        make_array_type(TupleType([ value_type, make_optional_type(separator_type) ])),
                        make_punct_type(value_type, separator_type),
                    ])

                    def gen_unwrap(last = False) -> Generator[BodyElement]:
                        tuple_then: list[BodyElement] = [ AssignExpr(NamedPatt(value_name), TupleIndexExpr(PathExpr(first_element_name), 0)) ]
                        plain_then: list[BodyElement] = [ AssignExpr(NamedPatt(value_name), PathExpr(first_element_name)) ]
                        if last:
                            tuple_then.append(CallExpr(PathExpr(name_fn_assert), [ make_is_none(TupleIndexExpr(PathExpr(first_element_name), 1)) ]))
                        else:
                            tuple_then.append(AssignExpr(NamedPatt(separator_name), TupleIndexExpr(PathExpr(first_element_name), 1)))
                            tuple_then.append(CallExpr(PathExpr(name_fn_assert), [ make_is_none(PathExpr(separator_name)) ]))
                            plain_then.append(AssignExpr(NamedPatt(separator_name), gen_default_constructor(expr.separator)))
                        yield CondExpr([
                            CondCase(
                                # FIXME does not handle nested tuples
                                IsExpr(PathExpr(first_element_name), name_type_tuple),
                                BlockExpr(tuple_then),
                            ),
                            CondCase(LitExpr(True), BlockExpr(plain_then)),
                        ])

                    yield coerced_type, [
                        AssignExpr(NamedPatt(new_elements_name), NewExpr(name_type_punct, [])),
                        AssignExpr(NamedPatt(elements_iter_name), CallExpr(PathExpr(name_fn_iter), [ PathExpr(value_param_name) ])),
                        MatchExpr(CallExpr(PathExpr(name_fn_next), [ PathExpr(elements_iter_name) ]), [
                            MatchArm(VariantPatt(name_variant_some, [ NamedPatt(first_element_name) ]), LoopExpr([
                                MatchExpr(CallExpr(PathExpr(name_fn_next), [ PathExpr(elements_iter_name) ]), [
                                    MatchArm(
                                        VariantPatt(name_variant_some, [ NamedPatt(second_element_name) ]),
                                        BlockExpr([
                                            *gen_unwrap(),
                                            AssignExpr(NamedPatt(new_value_name), value_expr),
                                            AssignExpr(NamedPatt(new_separator_name), separator_expr),
                                            CallExpr(PathExpr(name_fn_punct_append), [ PathExpr(new_elements_name), PathExpr(new_value_name), PathExpr(new_separator_name) ]),
                                            AssignExpr(NamedPatt(first_element_name), PathExpr(second_element_name)),
                                        ])
                                    ),
                                    MatchArm(
                                        VariantPatt(name_variant_none, []),
                                        BlockExpr([
                                            *gen_unwrap(last=True),
                                            AssignExpr(NamedPatt(new_value_name), value_expr),
                                            CallExpr(PathExpr(name_fn_punct_append_final), [ PathExpr(new_value_name) ]),
                                            BreakExpr(),
                                        ])
                                    )
                                ]),
                            ]))
                        ])
                    ]

                    return

                if isinstance(expr, MageRepeatExpr):

                    if expr.min == 0 and expr.max == 1:
                        yield from gen_coerce_fn_body(expr.expr, False)
                        return

                    new_elements_name = 'new_elements'
                    element_name = 'element'

                    if grammar.is_static(expr.expr):
                        yield PathType(name_type_integer), [
                            AssignExpr(NamedPatt(new_elements_name), make_empty_array()),
                            ForExpr(NamedPatt('_'), CallExpr(PathExpr(name_fn_range), [ LitExpr(0), PathExpr(value_param_name) ]), [
                                CallExpr(PathExpr(name_fn_append), [ PathExpr(new_elements_name), gen_default_constructor(expr.expr) ])
                            ]),
                            RetExpr(PathExpr(new_elements_name))
                        ]

                    element_type, element_expr = gen_coerce_call(expr.expr, PathExpr(element_name), False)

                    yield make_array_type(element_type), [
                        AssignExpr(NamedPatt(new_elements_name), make_empty_array()),
                        ForExpr(NamedPatt(element_name), PathExpr(value_param_name), [
                            CallExpr(PathExpr(name_fn_append), [ element_expr ]),
                        ]),
                        RetExpr(PathExpr(new_elements_name)),
                    ]

                    return

                if isinstance(expr, MageSeqExpr):

                    required = []
                    for element in expr.elements:
                        ty = infer_type(element)
                        if is_array_type(ty) or is_punct_type(ty) or (not can_be_empty(element, grammar=grammar) and not is_default_constructible(element)):
                            required.append(element)

                    if len(required) == 1:
                        main = required[0]
                        coerced_type, coerce_expr = gen_coerce_call(main, PathExpr(value_param_name), False)
                        out = []
                        for element in expr.elements:
                            if element is main:
                                out_expr = coerce_expr
                            elif can_be_empty(element, grammar=grammar):
                                out_expr = NoneExpr()
                            else:
                                out_expr = gen_default_constructor(element)
                            out.append(out_expr)
                        yield coerced_type, [ RetExpr(TupleExpr(out)) ]

                    new_exprs = []
                    new_types = []

                    for i, element in enumerate(expr.elements):
                        coerced_type, coerced_expr = gen_coerce_call(element, TupleIndexExpr(PathExpr(value_param_name), i), False)
                        new_types.append(coerced_type)
                        new_exprs.append(coerced_expr)

                    yield TupleType(new_types), [ RetExpr(TupleExpr(new_exprs)) ]

                    return

                assert(not isinstance(expr, MageLitExpr))
                assert(not isinstance(expr, MageHideExpr))
                assert_never(expr)

            return gen_coerce_call(expr, value, True)

        def split_fields(expr: MageExpr) -> tuple[list[MageExpr], list[MageExpr]]:

            required = []
            optional = []

            def visit(expr: MageExpr) -> None:

                if isinstance(expr, MageLookaheadExpr):
                    return

                if isinstance(expr, MageHideExpr):
                    return

                if isinstance(expr, MageRefExpr):
                    rule = grammar.lookup(expr.name)
                    if rule is not None and rule.expr is not None and not rule.is_public:
                        visit(rule.expr)
                        return

                if isinstance(expr, MageSeqExpr):
                    for element in expr.elements:
                        visit(element)
                    return

                if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr):
                    unreachable() # literals should already have been eliminated by previous passes

                if can_be_empty(expr, grammar=grammar):
                    optional.append(expr)
                else:
                    required.append(expr)

            visit(expr)

            return optional, required

        def get_fields(expr: MageExpr) -> Iterable[FieldSpec]:

            generator = NameGenerator()

            def generate_field_name() -> str:
                return generator(prefix='field_')

            def visit(expr: MageExpr, rule_name: str | None) -> Generator[FieldSpec]:

                if isinstance(expr, MageLookaheadExpr):
                    return

                if isinstance(expr, MageHideExpr):
                    return

                if isinstance(expr, MageRefExpr):
                    rule = grammar.lookup(expr.name)
                    if rule is not None and rule.expr is not None and not rule.is_public:
                        yield from visit(rule.expr, rule.name)
                        return

                if isinstance(expr, MageSeqExpr):
                    for element in expr.elements:
                        yield from visit(element, rule_name)
                    return

                if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr):
                    unreachable() # literals should already have been eliminated by previous passes

                field_name = rule_name or get_field_name(expr) or generate_field_name()
                field_type = infer_type(expr)
                param_type, init = gen_coerce_expr(expr, PathExpr(field_name))
                # expr.field_name = field_name
                # expr.field_type = field_type
                yield FieldSpec(field_name, field_type, param_type, init)

            return visit(expr, None)

        for rule in grammar.rules:
            if grammar.is_token_rule(rule):
                name_param_value = 'value'
                name_field_value = 'value'
                name_param_span = 'span'
                name_field_span = 'span'
                fields = list[Field]()
                new_params = [
                    Param(name_param_span, make_optional_type(PathType(name_type_span)), make_none())
                ]
                new_body: Body = []
                fields.append(Field(name_field_span, PathType(name_type_span)))
                new_body.append(FieldAssignExpr(name_field_span, PathExpr(name_param_span)))
                if rule.expr is not None and not grammar.is_static_token_rule(rule):
                    fields.append(Field(name_param_value, mage_type_to_ir_type(rule.type_name)))
                    new_params.append(Param(name_param_value, mage_type_to_ir_type(rule.type_name)))
                    new_body.append(FieldAssignExpr(name_field_value, PathExpr(name_param_value)))
                toplevel.append(StructDecl(
                    name=rename(rule.name),
                    fields=fields
                ))
                toplevel.append(FuncDecl(
                    name=name_fn_constructor,
                    self=rename(rule.name),
                    params=new_params,
                    returns=make_unit_type(),
                    body=new_body
                ))
            elif grammar.is_variant_rule(rule):
                assert(isinstance(rule.expr, MageChoiceExpr))
                toplevel.append(EnumDecl(
                    name=rename(rule.name),
                    variants=list(Variant(get_variant_name(element), infer_type(element)) for element in rule.expr.elements)
                ))
            elif grammar.is_parse_rule(rule):
                if rule.expr is None:
                    continue
                specs = list(get_fields(rule.expr))
                toplevel.append(StructDecl(
                    name=rename(rule.name),
                    fields=list(Field(spec.name, spec.ty) for spec in specs),
                ))
                new_params = list(Param(spec.name, spec.param_ty) for spec in specs)
                new_body: Body = list(FieldAssignExpr(spec.name, spec.coerced) for spec in specs)
                toplevel.append(FuncDecl(
                    name=name_fn_constructor,
                    self=rename(rule.name),
                    params=new_params,
                    returns=make_unit_type(),
                    body=new_body,
                ))
            elif rule == grammar.skip_rule:
                pass
            else:
                unreachable()

        toplevel.extend(defs.values())

        return Program(toplevel)
