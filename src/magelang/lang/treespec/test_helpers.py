from sqlite3 import IntegrityError
from magelang.logging import warn
from magelang import make_unit_type, is_optional_type, get_child_types, is_type_assignable, Spec
from magelang.lang.treespec import Specs, TupleType, PunctType, UnionType, ListType, SpecType, Field, EnumSpec, TokenSpec, NodeSpec, NoneType, Variant, Type, is_recursive, spec_to_type, ExternType

def opt(ty: Type) -> Type:
    return UnionType([ ty, NoneType() ])

def string():
    return ExternType('String')

def integer():
    return ExternType('Integer')

def boolean():
    return ExternType('Bool')

def floating():
    return ExternType('Float32')


def test_is_type_assignable_node_recursive():
    node = NodeSpec('node', [
        Field('one', integer()),
        Field('two', opt(SpecType('node'))),
    ])
    specs  = Specs([ node ])
    assert(is_type_assignable(SpecType('node'),  SpecType('node'), specs=specs))
    assert(not is_type_assignable(SpecType('node'), integer(), specs=specs))


def test_is_type_assignable_node_recursive():
    node1 = NodeSpec('node1', [
        Field('one', integer()),
        Field('two', opt(SpecType('node2'))),
    ])
    node2 = NodeSpec('node2', [
        Field('one', integer()),
        Field('two', opt(SpecType('node1'))),
    ])
    specs  = Specs([ node1, node2 ])
    assert(is_type_assignable(SpecType('node1'),  SpecType('node1'), specs=specs))
    assert(is_type_assignable(SpecType('node2'),  SpecType('node2'), specs=specs))
    assert(not is_type_assignable(SpecType('node1'), integer(), specs=specs))
    assert(not is_type_assignable(SpecType('node2'), integer(), specs=specs))


def test_is_type_assignable_type_to_union():
    t1 = UnionType([
        string(),
        integer(),
        boolean(),
    ])
    assert(is_type_assignable(t1, integer(), specs=Specs([])))
    assert(is_type_assignable(t1, string(), specs=Specs([])))
    assert(is_type_assignable(t1, boolean(), specs=Specs([])))
    assert(not is_type_assignable(t1, floating(), specs=Specs([])))


def test_is_type_assignable_union_to_type():
    t1 = UnionType([
        string(),
        integer(),
        boolean(),
    ])
    assert(not is_type_assignable(integer(), t1, specs=Specs([])))
    assert(not is_type_assignable(string(), t1, specs=Specs([])))
    assert(not is_type_assignable(boolean(), t1, specs=Specs([])))
    assert(not is_type_assignable(floating(), t1, specs=Specs([])))


def test_is_type_assignable_union_to_union():
    t1 = UnionType([
        string(),
        integer(),
        boolean(),
    ])
    t2 = UnionType([
        string(),
        integer(),
    ])
    t3 = UnionType([
        string(),
        floating(),
    ])
    assert(is_type_assignable(t1, t2, specs=Specs([])))
    assert(not is_type_assignable(t2, t1, specs=Specs([])))
    assert(not is_type_assignable(t1, t3, specs=Specs([])))
    assert(not is_type_assignable(t3, t1, specs=Specs([])))


def test_is_type_assignable_infinite_variants_doenst_crash():
    s1 = string()
    s2 = string()
    var1 = EnumSpec('var1', [
        Variant('first', SpecType('var2')),
        Variant('second', s1),
    ])
    var2 = EnumSpec('var2', [
        Variant('second', s2),
        Variant('first', SpecType('var1')),
    ])
    specs = Specs([ var1, var2 ])
    assert(not is_type_assignable(spec_to_type(var1), spec_to_type(var2), specs=specs))
    assert(not is_type_assignable(spec_to_type(var2), spec_to_type(var1), specs=specs))

def test_get_child_types_infinite_variant_doesnt_crash():
    s1 = string()
    s2 = string()
    foo = NodeSpec('foo',  [ Field('some_field', s1) ])
    var1 = EnumSpec('var1', [
        Variant('first', SpecType('var2')),
        Variant('second', SpecType('foo')),
    ])
    var2 = EnumSpec('var2', [
        Variant('first', s2),
        Variant('second', SpecType('var1')),
    ])
    specs = Specs([ foo, var1, var2 ])
    l1 = list(get_child_types(spec_to_type(var1), specs=specs))
    print(l1)
    assert(len(l1) == 1)
    assert(s1 in l1)
    l2 = list(get_child_types(spec_to_type(var2), specs=specs))
    assert(len(l2) == 1)
    assert(s1 in l2)

def test_is_self_referential_primitive():
    foo = NodeSpec('foo', [])
    bar = TokenSpec('bar', [], None, False)
    baz = TokenSpec('baz', [], None, True)
    baa = EnumSpec('baa', [])
    specs = Specs([ foo, bar, baz, baa ])
    assert(not is_recursive(spec_to_type(foo), specs=specs))
    assert(not is_recursive(spec_to_type(bar), specs=specs))
    assert(not is_recursive(spec_to_type(baz), specs=specs))
    assert(not is_recursive(spec_to_type(baa), specs=specs))

def test_is_self_referential_single_node_recursive():
    node = NodeSpec('foo', [
        Field('one', string()),
        Field('two', opt(SpecType('foo'))),
    ])
    specs = Specs([ node ])
    assert(is_recursive(spec_to_type(node), specs=specs))

def test_is_self_referential_mutual_recursion():
    a = NodeSpec('a', [
        Field('one', opt(SpecType('b'))),
        Field('two', string()),
    ])
    b = NodeSpec('b', [
        Field('three', ExternType('Integer')),
        Field('four', opt(SpecType('a'))),
    ])
    specs = Specs([ a, b ])
    assert(is_recursive(spec_to_type(a), specs=specs))
    assert(is_recursive(spec_to_type(b), specs=specs))

def test_is_self_referential_nested_enum():
    var = EnumSpec('var', [
        Variant('a', SpecType('b')),
    ])
    a = NodeSpec('a', [
        Field('one', string()),
    ])
    b = NodeSpec('b', [
        Field('two', opt(SpecType('var'))),
    ])
    c = NodeSpec('c', [
        Field('three', SpecType('b')),
    ])
    specs = Specs([ var, a, b, c ])
    assert(not is_recursive(spec_to_type(a), specs=specs))
    assert(is_recursive(spec_to_type(b), specs=specs))
    assert(not is_recursive(spec_to_type(c), specs=specs))
    assert(is_recursive(spec_to_type(var), specs=specs))

def test_is_self_referential_long_chain():
    n1 = NodeSpec('n1', [ Field('foo', SpecType('n2')) ])
    n2 = NodeSpec('n2', [ Field('foo', SpecType('n3')) ])
    n3 = NodeSpec('n3', [ Field('foo', SpecType('n4')) ])
    n4 = NodeSpec('n4', [ Field('foo', SpecType('n5')) ])
    n5 = NodeSpec('n5', [ Field('foo', SpecType('n6')) ])
    n6 = NodeSpec('n6', [ Field('foo', SpecType('n7')) ])
    n7 = NodeSpec('n7', [ Field('foo', SpecType('n8')) ])
    n8 = NodeSpec('n8', [ Field('foo', SpecType('n9')) ])
    n9 = NodeSpec('n9', [ Field('foo', SpecType('n1')) ])
    specs = Specs([ n1, n2, n3, n4, n5, n6, n7, n8, n9 ])
    assert(is_recursive(SpecType('n1'), specs=specs))
    assert(is_recursive(SpecType('n2'), specs=specs))
    assert(is_recursive(SpecType('n3'), specs=specs))
    assert(is_recursive(SpecType('n4'), specs=specs))
    assert(is_recursive(SpecType('n5'), specs=specs))
    assert(is_recursive(SpecType('n6'), specs=specs))
    assert(is_recursive(SpecType('n7'), specs=specs))
    assert(is_recursive(SpecType('n8'), specs=specs))
    assert(is_recursive(SpecType('n9'), specs=specs))

def test_is_self_referential_real_world():
    comma = TokenSpec('comma', [], None, True)
    open_paren = TokenSpec('open_paren',  [],None, True)
    close_paren = TokenSpec('close_paren', [], None, True)
    expr = EnumSpec('expr', [
        Variant('ref', SpecType('ref_expr')),
        Variant('call', SpecType('call_expr')),
    ])
    ref_expr = NodeSpec('ref_expr', [
        Field('name', string()),
    ])
    call_expr = NodeSpec('call_expr', [
        Field('operator', SpecType('expr')),
        Field('args', TupleType([
            SpecType('open_paren'),
            PunctType(SpecType('expr'), SpecType('comma'), False),
            SpecType('close_paren'),
        ])),
    ])
    specs = Specs([ expr, ref_expr, call_expr, comma, open_paren, close_paren ])
    assert(not is_recursive(SpecType('comma'), specs=specs))
    assert(not is_recursive(SpecType('open_paren'), specs=specs))
    assert(not is_recursive(SpecType('close_paren'), specs=specs))
    assert(is_recursive(SpecType('expr'), specs=specs))
    assert(not is_recursive(SpecType('ref_expr'), specs=specs))
    assert(is_recursive(SpecType('call_expr'), specs=specs))

def test_is_self_referential_infinite_variants_doesnt_crash():
    var1 = EnumSpec('var1', [
        Variant('first', SpecType('var2')),
        Variant('second', string()),
    ])
    var2 = EnumSpec('var2', [
        Variant('second', string()),
        Variant('first', SpecType('var1')),
    ])
    specs = Specs([ var1, var2 ])
    assert(not is_recursive(spec_to_type(var1), specs=specs))
    assert(not is_recursive(spec_to_type(var2), specs=specs))

