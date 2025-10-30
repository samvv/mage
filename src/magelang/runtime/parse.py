
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from magelang.runtime.node import BaseToken, BaseNode
from magelang.runtime.stream import Stream


__all__ = [
    'ParseFn',
    'ParseError',
    'AbstractParser',
    'ParseStream',
    'Operator',
    'OperatorTable',
    'Prefix',
    'Infix',
    'Postfix',
    'parse_climbing',
    'NOASSOC',
    'LASSOC',
    'RASSOC',
]

type Parsed = Any


ParseStream = Stream[BaseToken]


type ParseFn = Callable[[Stream[Any]], Parsed | None]


class ParseError(RuntimeError):
    pass


class AbstractParser:
    pass


@dataclass(frozen=True)
class Prefix:
    parse: ParseFn
    build: Callable[[Parsed, Parsed], BaseNode]


@dataclass(frozen=True)
class Postfix:
    parse: ParseFn
    build: Callable[[Parsed, Parsed], BaseNode]


@dataclass(frozen=True)
class Infix:
    parse: ParseFn
    build: Callable[[Parsed, Parsed, Parsed], BaseNode]
    assoc: int


NOASSOC = 0
RASSOC  = 1
LASSOC  = 2


type Operator = Prefix | Postfix | Infix


type OperatorTable = list[list[Operator]]


def _get_infix_operators(table: OperatorTable) -> Iterable[tuple[int, Infix]]:
    for prec, ops in enumerate(table):
        for op in ops:
            if isinstance(op, Infix):
                yield prec, op


def _get_prefix_operators(table: OperatorTable) -> Iterable[Prefix]:
    for ops in table:
        for op in ops:
            if isinstance(op, Prefix):
                yield op


def _get_suffix_operators(table: OperatorTable) -> Iterable[Postfix]:
    for ops in table:
        for op in ops:
            if isinstance(op, Postfix):
                yield op


def parse_climbing(stream: Stream[Any], lhs: Parsed, min_prec: int, table: OperatorTable, parse_prim: ParseFn) -> Parsed | None:

    def parse_infix_operator(stream: Stream[Any]) -> tuple[Parsed, int, Infix] | None:
        for prec, op in _get_infix_operators(table):
            stream_2 = stream.fork()
            res = op.parse(stream_2)
            if res is not None:
                stream.join_to(stream_2)
                return res, prec, op

    def peek_infix_operator(stream: Stream[Any]) -> tuple[Parsed, int, Infix] | None:
        for prec, op in _get_infix_operators(table):
            stream_2 = stream.fork()
            res = op.parse(stream_2)
            if res is not None:
                return res, prec, op

    def parse_prefix_operator(stream: Stream[Any]) -> tuple[Parsed, Prefix] | None:
        for op in _get_prefix_operators(table):
            stream_2 = stream.fork()
            node = op.parse(stream_2)
            if node is not None:
                stream.join_to(stream_2)
                return node, op

    def parse_suffix_operator(stream: Stream[Any]) -> tuple[Parsed, Postfix] | None:
        for op in _get_suffix_operators(table):
            stream_2 = stream.fork()
            node = op.parse(stream_2)
            if node is not None:
                stream.join_to(stream_2)
                return node, op

    def parse_term(stream: Stream[Any]) -> Parsed | None:
        prefixes = list[tuple[Parsed, Prefix]]()
        while True:
            result = parse_prefix_operator(stream)
            if result is None:
                break
            prefixes.append(result)
        out = parse_prim(stream)
        suffixes = list[tuple[Parsed, Postfix]]()
        while True:
            result = parse_suffix_operator(stream)
            if result is None:
                break
            suffixes.append(result)
        for node, op in prefixes:
            out = op.build(node, out)
        for node, op in reversed(suffixes):
            out = op.build(node, out)
        return out

    while True:
        res = parse_infix_operator(stream)
        if res is None:
            break
        node, prec, op = res
        if prec < min_prec:
            break
        rhs = parse_term(stream)
        if rhs is None:
            return
        while True:
            res_2 = peek_infix_operator(stream)
            if res_2 is None:
                break
            _, prec_2, op_2 = res_2
            if prec_2 > prec or (prec_2 == prec and op_2.assoc == RASSOC):
                break
            rhs = parse_climbing(stream, rhs, prec_2, table, parse_term)
            if rhs is None:
                return
        lhs = op.build(node, lhs, rhs)

    return lhs



