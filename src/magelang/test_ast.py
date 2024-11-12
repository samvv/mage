
from intervaltree import Interval
from magelang.lang.mage.ast import MageCharSetExpr, MageChoiceExpr, MageGrammar, MageLitExpr, MageRefExpr, MageRule, MageSeqExpr, intersect_interval
from magelang.analysis import intersects

def test_intersects_lit_lit():
    grammar = MageGrammar()
    e1 = MageLitExpr('foo')
    e2 = MageLitExpr('bar')
    e3 = MageLitExpr('oep')
    assert(not intersects(e1, e2, grammar=grammar))
    assert(intersects(e1, e3, grammar=grammar))
    assert(not intersects(e3, e1, grammar=grammar))

def test_intersects_charset_charset():
    grammar = MageGrammar()
    e1 = MageLitExpr('fod')
    e2 = MageLitExpr('aaa')
    e3 = MageCharSetExpr([
        'd',
        ('0', '9')
    ], False, False)
    assert(intersects(e1, e3, grammar=grammar))
    assert(not intersects(e3, e1, grammar=grammar))
    assert(not intersects(e2, e3, grammar=grammar))
    assert(not intersects(e3, e1, grammar=grammar))

def test_intersects_seq_seq():
    grammar = MageGrammar()
    e1 = MageSeqExpr([
        MageLitExpr('aaa'),
        MageLitExpr('fod'),
    ])
    e2 = MageSeqExpr([
        MageLitExpr('doo'),
        MageLitExpr('baz'),
    ])
    assert(intersects(e1, e2, grammar=grammar))
    assert(not intersects(e2, e1, grammar=grammar))

def test_intersects_cycle_true():
    e1 = MageLitExpr('a')
    e2 = MageChoiceExpr([
        MageRefExpr('foo'),
        MageLitExpr('b')
    ])
    grammar = MageGrammar([
        MageRule('foo', MageSeqExpr([
            e1,
            e2
        ]))
    ])
    assert(intersects(e1, e2, grammar=grammar))

def test_intersects_cycle_false():
    e1 = MageLitExpr('a')
    e2 = MageChoiceExpr([
        MageRefExpr('bar'),
        MageLitExpr('b')
    ])
    e3 = MageLitExpr('c')
    e4 = MageChoiceExpr([
        MageRefExpr('foo'),
        MageLitExpr('d'),
    ])
    grammar = MageGrammar([
        MageRule('foo', MageSeqExpr([ e1, e2 ])),
        MageRule('bar', MageSeqExpr([ e3, e4 ]))
    ])
    assert(not intersects(e1, e2, grammar=grammar))
    assert(not intersects(e3, e4, grammar=grammar))
    assert(not intersects(e1, e3, grammar=grammar))

    # Yes, they can overlap:
    # e2 -> cacacacacab
    # e4 -> acacacacacab
    assert(intersects(e4, e2, grammar=grammar))

def test_interval_overlaps():
    assert(intersect_interval(Interval(1, 1), Interval(2, 2)) is None)
    assert(intersect_interval(Interval(1, 1), Interval(1, 1)) is None)
    assert(intersect_interval(Interval(1, 2), Interval(2, 3)) is None)
    assert(intersect_interval(Interval(2, 3), Interval(1, 2)) is None)
    assert(intersect_interval(Interval(1, 2), Interval(1, 2)) == Interval(1, 2))
    assert(intersect_interval(Interval(1, 2), Interval(1, 4)) == Interval(1, 2))
    assert(intersect_interval(Interval(2, 5), Interval(3, 4)) == Interval(3, 4))
    assert(intersect_interval(Interval(3, 4), Interval(2, 5)) == Interval(3, 4))
    assert(intersect_interval(Interval(2, 5), Interval(3, 4)) == Interval(3, 4))
    assert(intersect_interval(Interval(3, 4), Interval(2, 10)) == Interval(3, 4))
    assert(intersect_interval(Interval(1, 3), Interval(2, 4)) == Interval(2, 3))
    assert(intersect_interval(Interval(2, 4), Interval(1, 3)) == Interval(2, 3))
    assert(intersect_interval(Interval(2, 5), Interval(1, 3)) == Interval(2, 3))

def test_charset_overlaps():
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ ])
    ))
    assert(MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ ('a','z') ])
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ ('0', '9') ])
    ))
    assert(MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ], invert=True),
        MageCharSetExpr([ ('0','9') ])
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ], invert=True),
        MageCharSetExpr([ 'a' ])
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ], invert=True),
        MageCharSetExpr([ 'c' ])
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ], invert=True),
        MageCharSetExpr([ 'd' ])
    ))
    assert(MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ], invert=True),
        MageCharSetExpr([ 'e' ])
    ))
    assert(MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ ('0','9') ], invert=True)
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ 'a' ], invert=True)
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ 'c' ], invert=True)
    ))
    assert(not MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ 'd' ], invert=True)
    ))
    assert(MageCharSetExpr.overlaps(
        MageCharSetExpr([ 'a', 'c', 'd' ]),
        MageCharSetExpr([ 'e' ], invert=True)
    ))
