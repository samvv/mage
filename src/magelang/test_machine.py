
import pytest

from magelang.lang.mage.ast import *
from magelang.passes import mage_to_machine
from magelang.machine import Jump, JumpNZ, JumpZ, Noop, ParseError, Push, call_machine_function, execute_machine, Machine, Inc, Halt, Dec, FuncDef

def machine(ops):
    return Machine({ 'main': FuncDef('main', 0, 0, ops) })

def test_inc():
    m = machine([ Inc(), Halt() ]);
    stack = [ 1 ]
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 2)

def test_dec():
    m = machine([ Dec(), Halt() ]);
    stack = [ 2 ]
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 1)

def test_jump():
    m = machine([
        Push(1),
        Jump(+2),
        Push(2),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 1)

def test_push():
    m = machine([ Push(42), Push(33), Halt() ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 33)
    assert(stack[-2] == 42)

def test_jumpz():
    m = machine([
        Push(0),
        JumpZ(+2),
        Halt(),
        Push(42),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)
    m = machine([
        Push(1),
        JumpZ(+3),
        Push(42),
        Halt(),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)

def test_jumpnz():
    m = machine([
        Push(1),
        JumpNZ(+2),
        Halt(),
        Push(42),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)
    m = machine([
        Push(0),
        JumpNZ(+3),
        Push(42),
        Halt(),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)

def test_compile_lit():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageLitExpr('foobar')),
    ]))
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'blabla')
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'fooba')
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'oobar')
    # with pytest.raises(ParseError):
    #     execute(m, 'one', 'foobaralaza')
    root = call_machine_function(m, 'one', 'foobar')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    tok = root.get_field('token_0')
    assert(tok.start == 0)
    assert(tok.end == 6)

def test_compile_ref():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageLitExpr('foobar')),
        MageRule('two', MageRefExpr('one')),
    ]))
    with pytest.raises(ParseError):
        call_machine_function(m, 'two', 'blabla')
    with pytest.raises(ParseError):
        call_machine_function(m, 'two', 'fooba')
    with pytest.raises(ParseError):
        call_machine_function(m, 'two', 'oobar')
    root = call_machine_function(m, 'two', 'foobar')
    assert(root.name == 'two')
    assert(len(root.fields) == 1)
    tok = root.get_field('token_0')
    assert(tok.start == 0)
    assert(tok.end == 6)

def test_compile_seq():
    m = mage_to_machine(MageGrammar([
        MageRule(name='one', expr=MageSeqExpr([
            MageLitExpr('a'),
            MageLitExpr('b'),
        ])),
    ]))
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'cc')
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'aa')
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'bb')
    # with pytest.raises(ParseError):
    #     call_machine_function(m, 'one', 'abab')
    root = call_machine_function(m, 'one', 'ab')
    assert(root.name == 'one')
    assert(len(root.fields) == 2)
    a = root.get_field('lower_a')
    assert(a.start == 0)
    assert(a.end == 1)
    b = root.get_field('lower_b')
    assert(b.start == 1)
    assert(b.end == 2)

def test_compile_neg_lookahead():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageSeqExpr([
            MageLookaheadExpr(MageLitExpr('abc'), True),
            MageLitExpr('defghi')
        ]))
    ]))
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'abcdef')
    root = call_machine_function(m, 'one', 'defghi')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    tok = root.get_field('token_0')
    assert(tok.start == 0)
    assert(tok.end == 6)

def test_compile_pos_lookahead():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageSeqExpr([
            MageLookaheadExpr(MageLitExpr('abc'), True),
            MageLitExpr('abcdef')
        ]))
    ]))
    root = call_machine_function(m, 'one', 'abcdef')
    assert(root.name == 'one')
    with pytest.raises(ParseError):
        call_machine_function(m, 'one', 'def')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    tok = root.get_field('token_0')
    assert(tok.start ==  0)
    assert(tok.end == 6)

