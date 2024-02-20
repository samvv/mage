
from sweetener import Record

from .ast import *

class Type(Record):
    pass

class AnyTokenType(Type):
    pass

class AnyNodeType(Type):
    pass

class NodeType(Type):
    name: str

class TokenType(Type):
    name: str
    is_singleton: bool

class OptionType(Type):
    element_type: Type

class TupleType(Type):
    element_types: list[Type]

class ListType(Type):
    element_type: Type

class UnionType(Type):
    types: list[Type]

class NoneType(Type):
    pass

class Field(Record):
    name: str
    ty: Type

class SpecBase(Record):
    pass

class TokenSpec(SpecBase):
    name: str

class NodeSpec(SpecBase):
    name: str
    members: list[Field]

class VariantSpec(SpecBase):
    name: str
    members: list[str]

Spec = TokenSpec | NodeSpec | VariantSpec

names = {
    '\x00': 'null',
    '\x01': 'start_of_heading',
    '\x02': 'start_of_text',
    '\x03': 'end_of_text',
    '\x04': 'end_of_transmission',
    '\x05': 'enquiry',
    '\x06': 'acknowledge',
    '\x07': 'bell',
    '\x08': 'backspace',
    '\x09': 'horizontal_tab',
    '\x0A': 'line_feed',
    '\x0B': 'vertical_tabulation',
    '\x0c': 'form_feed',
    '\x0D': 'carriage_return',
    '\x0E': 'shift_out',
    '\x0F': 'shift_in',
    '\x10': 'data_link_escape',
    '\x11': 'device_control_one',
    '\x12': 'device_control_two',
    '\x13': 'device_control_three',
    '\x14': 'device_control_four',
    '\x15': 'negative_acknowledge',
    '\x16': 'synchronous_idle',
    '\x17': 'end_of_transmission_block',
    '\x18': 'cancel',
    '\x19': 'end_of_medium',
    '\x1A': 'substitute',
    '\x1B': 'escape',
    '\x1C': 'file_separator',
    '\x1D': 'group_separator',
    '\x1E': 'record_separator',
    '\x1F': 'unit_separator',
    '!': 'exclamation_mark',
    '"': 'double_quote',
    '#': 'hashtag',
    '$': 'dollar',
    '%': 'percenct',
    '&': 'ampersand',
    '\'': 'single_quote',
    '(': 'open_paren',
    ')': 'close_paren',
    '*': 'asterisk',
    '+': 'plus',
    ',': 'comma',
    '-': 'hyphen',
    '.': 'dot',
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'siz',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '/': 'slash',
    ':': 'colon',
    ';': 'semicolon',
    '<': 'less_than',
    '=': 'equals',
    '>': 'greater_than',
    '?': 'question_mark',
    '@': 'at_sign',
    'A': 'upper_a',
    'B': 'upper_b',
    'C': 'upper_c',
    'D': 'upper_d',
    'E': 'upper_e',
    'F': 'upper_f',
    'G': 'upper_g',
    'H': 'upper_h',
    'I': 'upper_i',
    'J': 'upper_j',
    'K': 'upper_k',
    'L': 'upper_l',
    'M': 'upper_n',
    'N': 'upper_m',
    'O': 'upper_o',
    'P': 'upper_p',
    'Q': 'upper_q',
    'R': 'upper_r',
    'S': 'upper_s',
    'T': 'upper_t',
    'U': 'upper_u',
    'V': 'upper_v',
    'W': 'upper_w',
    'X': 'upper_x',
    'Y': 'upper_y',
    'Z': 'upper_z',
    '[': 'open_bracket',
    '\\': 'backslash',
    ']': 'close_bracket',
    '^': 'caret',
    '`': 'backtick',
    'a': 'lower_a',
    'b': 'lower_b',
    'c': 'lower_c',
    'd': 'lower_d',
    'e': 'lower_e',
    'f': 'lower_f',
    'g': 'lower_g',
    'h': 'lower_h',
    'i': 'lower_i',
    'j': 'lower_j',
    'k': 'lower_k',
    'l': 'lower_l',
    'm': 'lower_n',
    'n': 'lower_m',
    'o': 'lower_o',
    'p': 'lower_p',
    'q': 'lower_q',
    'r': 'lower_r',
    's': 'lower_s',
    't': 'lower_t',
    'u': 'lower_u',
    'v': 'lower_v',
    'w': 'lower_w',
    'x': 'lower_x',
    'y': 'lower_y',
    'z': 'lower_z',
    '{': 'open_brace',
    '|': 'vertical_bar',
    '}': 'close_brace',
    '~': 'tilde',
    '\x7F': 'delete',
    }

def grammar_to_nodespec(grammar: Grammar) -> list[Spec]:

    field_counter = 0
    def generate_field_name() -> str:
        nonlocal field_counter
        name = f'field_{field_counter}'
        field_counter += 1
        return name

    token_counter = 0
    def generate_token_name() -> str:
        nonlocal token_counter
        name = f'token_{token_counter}'
        token_counter += 1
        return name

    literal_to_name = dict()

    def str_to_name(text: str) -> str | None:
        if text[0].isalpha() and all(ch.isalnum() for ch in text[1:]):
            return f'{text}_keyword'
        elif len(text) <= 4:
            return '_'.join(names[ch] for ch in text)

    def is_variant(rule: Rule) -> bool:
        def visit(expr: Expr) -> bool:
            if isinstance(expr, RefExpr):
                rule = grammar.lookup(expr.name)
                if grammar.is_parse_rule(rule):
                    return True
                # FIXME What to do with Rule(is_extern=True, is_public=False) ?
                assert(rule.expr is not None)
                return visit(rule.expr)
            if isinstance(expr, ChoiceExpr):
                for element in expr.elements:
                    if not visit(element):
                        return False
                return True
            return False
        if rule.is_extern:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(rule.expr is not None)
        return visit(rule.expr)

    def get_variant_members(expr: Expr) -> Generator[str, None, None]:
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule.is_public:
                yield rule.name
                return
            # FIXME What to do with Rule(is_extern=True, is_public=False) ?
            if rule.expr is not None:
                yield from get_variant_members(rule.expr)
            return
        if isinstance(expr, ChoiceExpr):
            for element in expr.elements:
                yield from get_variant_members(element)
            return
        assert(False)

    def get_node_members(expr: Expr, toplevel: bool) -> Generator[Field, None, None]:
        if isinstance(expr, HideExpr):
            return
        if isinstance(expr, ListExpr):
            element_fields = list(get_node_members(expr.element, False))
            separator_fields = list(get_node_members(expr.separator, False))
            if not element_fields and not separator_fields:
                return
            assert(len(element_fields) == 1)
            assert(len(separator_fields) == 1)
            label = expr.label
            if label is None:
                label = generate_field_name()
            yield Field(label, ListType(TupleType([ element_fields[0].ty, OptionType(separator_fields[0].ty) ])))
            return
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            label = rule.name if expr.label is None else expr.label
            if rule.is_extern:
                yield Field(label, TokenType(rule.name, False) if rule.is_token else NodeType(rule.name))
                return
            if not rule.is_public:
                assert(rule.expr is not None)
                yield from get_node_members(rule.expr, toplevel)
                return
            # TODO yield TokenType if rule is a token rule
            yield Field(label, NodeType(expr.name))
            return
        if isinstance(expr, LitExpr):
            label = expr.label
            if label is None:
                label = str_to_name(expr.text)
                if label is None:
                    label = generate_field_name()
            yield Field(label, TokenType(literal_to_name[expr.text], True))
            return
        if isinstance(expr, RepeatExpr):
            fields = list(get_node_members(expr.expr, False))
            assert(len(fields) == 1)
            field = fields[0]
            label = expr.label
            if label is None:
                label = field.name
                if label is None:
                    label = generate_field_name()
            if expr.max == 0:
                return
            elif expr.min == 0 and expr.max == 1:
                ty = OptionType(field.ty)
            elif expr.min == 1 and expr.max == 1:
                ty = field.ty
            else:
                ty = ListType(field.ty)
            yield Field(label, ty)
            return
        if isinstance(expr, CharSetExpr):
            label = expr.label if expr.label is not None else generate_field_name()
            yield Field(label, AnyTokenType())
            return
        if isinstance(expr, SeqExpr):
            if toplevel:
                for element in expr.elements:
                    yield from get_node_members(element, True)
            else:
                label = expr.label if expr.label is not None else generate_field_name()
                types = []
                for element in expr.elements:
                    for field in get_node_members(element, False):
                        types.append(field.ty)
                if not types:
                    return
                yield Field(label, TupleType(types) if len(types) > 1 else types[0])
            return
        if isinstance(expr, LookaheadExpr):
            return
        if isinstance(expr, ChoiceExpr):
            label = expr.label if expr.label is not None else generate_field_name()
            fields = list(field for element in expr.elements for field in get_node_members(element, False))
            if len(fields) == 1:
                yield fields[0]
                return
            yield Field(label, UnionType(list(field.ty for field in fields)))
            return
        raise RuntimeError(f'unexpected {expr}')

    specs = []

    def collect_literals(expr: Expr):
        if isinstance(expr, LitExpr):
            name = str_to_name(expr.text)
            if name is None:
                name = generate_token_name()
            if expr.text not in literal_to_name:
                specs.append(TokenSpec(name))
                literal_to_name[expr.text] = name
            return
        for_each_expr(expr, collect_literals)

    for rule in grammar.rules:
        if rule.expr is not None:
            collect_literals(rule.expr)

    for rule in grammar.rules:
        if rule.is_extern or grammar.is_fragment(rule) or rule.has_decorator('skip'):
            continue
        # only Rule(is_extern=True) can have an empty expression
        assert(rule.expr is not None)
        if grammar.is_token_rule(rule):
            specs.append(TokenSpec(rule.name))
            continue
        if is_variant(rule):
            specs.append(VariantSpec(rule.name, list(get_variant_members(rule.expr))))
            continue
        field_counter = 0
        assert(rule.expr is not None)
        members = list(get_node_members(rule.expr, True))
        specs.append(NodeSpec(rule.name, members))

    return specs

