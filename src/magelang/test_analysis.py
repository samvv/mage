
from magelang.analysis import do_match, overlapping_tokens
from magelang.lang.mage.ast import *

def test_overlapping_tokens_str_str():
    r1 = MageRule('foo', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r2 = MageRule('bar', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r3 = MageRule('baz', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r4 = MageRule('bax', flags=FORCE_TOKEN, expr=MageLitExpr('bla'))
    r5 = MageRule('baa', flags=FORCE_TOKEN, expr=MageLitExpr('hello'))
    res = list(overlapping_tokens(MageGrammar([ r1, r2, r3, r4, r5 ])))
    assert(len(res) == 3)


def test_overlapping_tokens_str_repeat_charset():
    r1 = MageRule('foo', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r2 = MageRule('bax', flags=FORCE_TOKEN, expr=MageRepeatExpr(MageCharSetExpr([ ('a', 'z') ]), 0, POSINF))
    r3 = MageRule('bar', flags=FORCE_TOKEN, expr=MageLitExpr('bar'))
    res = overlapping_tokens(MageGrammar([ r1, r2, r3 ]))
    print(list(list(r.name for r in scc) for scc in res))
    assert(False)
    assert(len(res) == 3)


def test_envelops_lit_lit():
    r1 = MageRule('foo', MageLitExpr('foo'))
    r2 = MageRule('bar', MageLitExpr('foo'))
    r3 = MageRule('bax', MageLitExpr('hello'))
    g = MageGrammar([ r1, r2, r3 ])
    assert(do_match(r1.expr, r2.expr, grammar=g))
    assert(do_match(r2.expr, r1.expr, grammar=g))
    assert(not do_match(r1.expr, r3.expr, grammar=g))
    assert(not do_match(r2.expr, r3.expr, grammar=g))
    assert(not do_match(r3.expr, r1.expr, grammar=g))
    assert(not do_match(r1.expr, r3.expr, grammar=g))


def test_envelops_charset_charset():
    r1 = MageRule('foo', MageCharSetExpr([ ('a', 'a'), ('0', '9') ]))
    r2 = MageRule('bar', MageCharSetExpr([ ('a', 'z'), ('0', '9') ]))
    r3 = MageRule('bax', MageCharSetExpr([ ('$', '$') ]))
    g = MageGrammar([ r1, r2, r3 ])
    assert(not do_match(r1.expr, r2.expr, grammar=g))
    assert(do_match(r2.expr, r1.expr, grammar=g))
    assert(not do_match(r1.expr, r3.expr, grammar=g))
    assert(not do_match(r2.expr, r3.expr, grammar=g))
    assert(not do_match(r3.expr, r1.expr, grammar=g))
    assert(not do_match(r1.expr, r3.expr, grammar=g))


