
import pytest

from magelang.lang.mage.ast import *
from magelang.machine import Jump, JumpNZ, JumpZ, Noop, ParseError, Push, call_machine_method, execute_machine, mage_to_machine, Machine, Inc, Halt, Dec

def test_inc():
    m = Machine([ Inc(), Halt() ]);
    stack = [ 1 ]
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 2)

def test_dec():
    m = Machine([ Dec(), Halt() ]);
    stack = [ 2 ]
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 1)

def test_jump():
    m = Machine([
        Push(1),
        Jump(+2),
        Push(2),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 1)

def test_push():
    m = Machine([ Push(42), Push(33), Halt() ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 33)
    assert(stack[-2] == 42)

def test_jumpz():
    m = Machine([
        Push(0),
        JumpZ(+2),
        Halt(),
        Push(42),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)
    m = Machine([
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
    m = Machine([
        Push(1),
        JumpNZ(+2),
        Halt(),
        Push(42),
        Halt(),
    ])
    stack = []
    execute_machine(m, '', stack=stack)
    assert(stack[-1] == 42)
    m = Machine([
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
        call_machine_method(m, 'one', 'blabla')
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'fooba')
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'oobar')
    # with pytest.raises(ParseError):
    #     execute(m, 'one', 'foobaralaza')
    root = call_machine_method(m, 'one', 'foobar')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    assert(root.fields[0][1] == (0,6))

def test_compile_ref():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageLitExpr('foobar')),
        MageRule('two', MageRefExpr('one')),
    ]))
    with pytest.raises(ParseError):
        call_machine_method(m, 'two', 'blabla')
    with pytest.raises(ParseError):
        call_machine_method(m, 'two', 'fooba')
    with pytest.raises(ParseError):
        call_machine_method(m, 'two', 'oobar')
    root = call_machine_method(m, 'two', 'foobar')
    assert(root.name == 'two')
    assert(len(root.fields) == 1)
    assert(root.fields[0][1] == (0,6))

def test_compile_seq():
    m = mage_to_machine(MageGrammar([
        MageRule(name='one', expr=MageSeqExpr([
            MageLitExpr('a'),
            MageLitExpr('b'),
        ])),
    ]))
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'cc')
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'aa')
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'bb')
    # with pytest.raises(ParseError):
    #     execute(m, 'one', 'abab')
    root = call_machine_method(m, 'one', 'ab')
    assert(root.name == 'one')
    assert(len(root.fields) == 2)
    assert(root.fields[0][1] == (0,1))
    assert(root.fields[1][1] == (1,2))

def test_compile_neg_lookahead():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageSeqExpr([
            MageLookaheadExpr(MageLitExpr('abc'), True),
            MageLitExpr('def')
        ]))
    ]))
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'abcdef')
    root = call_machine_method(m, 'one', 'def')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    assert(root.fields[0][1] == (0,3))

def test_compile_pos_lookahead():
    m = mage_to_machine(MageGrammar([
        MageRule('one', MageSeqExpr([
            MageLookaheadExpr(MageLitExpr('abc'), True),
            MageLitExpr('abcdef')
        ]))
    ]))
    root = call_machine_method(m, 'one', 'abcdef')
    assert(root.name == 'one')
    with pytest.raises(ParseError):
        call_machine_method(m, 'one', 'def')
    assert(root.name == 'one')
    assert(len(root.fields) == 1)
    assert(root.fields[0][1] == (0,6))

