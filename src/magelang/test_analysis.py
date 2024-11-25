
from magelang.analysis import overlapping_tokens
from magelang.lang.mage.ast import *


def test_overlapping_tokens_str_str():
    r1 = MageRule('foo', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r2 = MageRule('bar', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r3 = MageRule('baz', flags=FORCE_TOKEN, expr=MageLitExpr('foo'))
    r4 = MageRule('bax', flags=FORCE_TOKEN, expr=MageLitExpr('bla'))
    res = overlapping_tokens(MageGrammar([ r1, r2, r3, r4 ]))
    assert(False)
    assert(len(res) == 3)
