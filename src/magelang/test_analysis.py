
from magelang.analysis import INFIX, NONE, POSTFIX, PREFIX, fixity, get_lexer_modes, envelops, get_recursive, get_roots, is_subset
from magelang.lang.mage.ast import *


def test_is_subset_consecutive():
    t1 = IntervalTree()
    t1.addi(1, 2)
    t1.addi(2, 3)
    t1.addi(3, 4)
    t1.addi(6, 7)
    t2 = IntervalTree()
    t2.addi(1, 10)
    t3 = IntervalTree()
    t3.addi(1, 4)
    assert(is_subset(t1, t2))
    assert(not is_subset(t2, t1))
    assert(is_subset(t1, t1))
    assert(is_subset(t2, t2))
    assert(is_subset(t3, t3))
    assert(is_subset(t3, t1))
    assert(is_subset(t3, t2))
    assert(not is_subset(t1, t3))


def test_envelops_str_str():
    e1 = MageLitExpr('foo')
    e2 = MageLitExpr('bar')
    e3 = MageLitExpr('fo')
    e4 = MageLitExpr('fob')
    e5 = MageLitExpr('foo')
    assert(not envelops(e1, e2))
    assert(not envelops(e2, e1))
    assert(envelops(e1, e3))
    assert(not envelops(e3, e1))
    assert(not envelops(e3, e4))
    assert(envelops(e4, e3))
    assert(envelops(e1, e1))
    assert(envelops(e2, e2))
    assert(envelops(e3, e3))
    assert(envelops(e4, e4))
    assert(envelops(e5, e5))
    assert(envelops(e1, e5))


def test_envelops_repeat():
    e0 = MageRepeatExpr(MageLitExpr('a'), 2, 3)
    e2 = MageLitExpr('a')
    e3 = MageLitExpr('aa')
    e4 = MageLitExpr('aaa')
    e5 = MageLitExpr('aaaa')
    assert(not envelops(e0, e2))
    assert(not envelops(e2, e0))
    assert(envelops(e0, e3))
    assert(not envelops(e3, e0))
    assert(envelops(e0, e4))
    assert(envelops(e4, e0))
    assert(not envelops(e0, e5))
    assert(envelops(e5, e0))


def test_envelops_charset_charset():
    e1 = MageCharSetExpr([ ('a', 'a'), ('0', '9') ])
    e2 = MageCharSetExpr([ ('a', 'z'), ('0', '9') ])
    e3 = MageCharSetExpr([ ('$', '$') ])
    assert(not envelops(e1, e2))
    assert(envelops(e2, e1))
    assert(not envelops(e1, e3))
    assert(not envelops(e2, e3))
    assert(not envelops(e3, e1))
    assert(not envelops(e1, e3))


def test_overlapping_tokens_str_str():
    r1 = MageRule('foo', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('foobar'))
    r2 = MageRule('bax', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('foo'))
    r3 = MageRule('bar', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('foobar'))
    r4 = MageRule('baz', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('foobar'))
    r5 = MageRule('baa', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('hello'))
    modes = get_lexer_modes(MageGrammar([ r1, r2, r3, r4, r5 ]))
    assert(modes['bax'] == modes['baa'])
    assert(modes['baz'] == modes['bax'])
    assert(modes['foo'] != modes['bar'])
    assert(modes['foo'] != modes['baz'])
    assert(modes['foo'] != modes['bax'])
    assert(modes['bar'] != modes['baz'])
    assert(modes['bar'] != modes['bax'])


def test_overlapping_tokens_str_repeat_charset():
    r1 = MageRule('foo', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('@@@'))
    r2 = MageRule('bax', flags=PUBLIC | FORCE_TOKEN, expr=MageRepeatExpr(MageCharSetExpr([ ('a', 'z') ]), 0, POSINF))
    r3 = MageRule('bar', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('bar'))
    r4 = MageRule('bla', flags=PUBLIC | FORCE_TOKEN, expr=MageLitExpr('a'))
    modes = get_lexer_modes(MageGrammar([ r1, r2, r3, r4 ]))
    assert(len(modes) == 4)
    assert(modes['bar'] == modes['foo'])
    assert(modes['bar'] == modes['bla'])
    assert(modes['bar'] != modes['bax'])

r1 = MageRule('expr', flags=PUBLIC, expr=MageChoiceExpr([
    MageRefExpr('lit_expr'),
    MageRefExpr('add_expr'),
]))
r2 = MageRule('lit_expr', flags=PUBLIC, expr=MageLitExpr('foobar'))
r3 = MageRule('add_expr', flags=PUBLIC, expr=MageSeqExpr([
    MageRefExpr('expr'),
    MageLitExpr('+'),
    MageRefExpr('expr'),
]))
r4 = MageRule('inc_expr', flags=PUBLIC, expr=MageSeqExpr([
    MageRefExpr('expr'),
    MageLitExpr('++'),
]))
r5 = MageRule('await_expr', flags=PUBLIC, expr=MageSeqExpr([
    MageLitExpr('await'),
    MageRefExpr('expr'),
]))
r6 = MageRule('seq_expr', flags=PUBLIC, expr=MageSeqExpr([
    MageRefExpr('expr'),
    MageRefExpr('expr'),
]))
g1 = MageGrammar([ r1, r2, r3, r4, r5, r6 ])

def test_recursive():
    rec = get_recursive(g1)
    assert(len(rec) == 1)
    roots = list(get_roots(rec[0], g1))
    assert(len(roots) == 1)
    assert(roots[0] == r1)
    assert(fixity(r2, roots, g1) == NONE)
    assert(fixity(r3, roots, g1) == INFIX)
    assert(fixity(r4, roots, g1) == POSTFIX)
    assert(fixity(r5, roots, g1) == PREFIX)
    assert(fixity(r6, roots, g1) == NONE)

