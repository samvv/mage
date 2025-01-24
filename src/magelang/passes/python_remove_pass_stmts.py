
from magelang.lang.python.cst import *

def python_remove_pass_stmts(module: PyModule) -> PyModule:

    def rewrite_stmt(stmt: PyStmt) -> PyStmt:
        if isinstance(stmt, PyIfStmt):
            new_first = stmt.first.derive(body=rewrite_body(stmt.first.body))
            new_alternatives = list(case.derive(body=rewrite_body(case.body)) for case in stmt.alternatives)
            new_last = stmt.last.derive(body=rewrite_body(stmt.last.body)) if stmt.last is not None else None
            return stmt.derive(first=new_first, alternatives=new_alternatives, last=new_last)
        if isinstance(stmt, PyForStmt):
            return stmt.derive(body=rewrite_body(stmt.body))
        if isinstance(stmt, PyWhileStmt):
            return stmt.derive(body=rewrite_body(stmt.body))
        if isinstance(stmt, PyTryStmt):
            new_handlers = list(handler.derive(body=rewrite_body(handler.body)) for handler in stmt.handlers)
            new_else_clause = None
            if stmt.else_clause is not None:
                else_keyword, colon, body = stmt.else_clause
                new_else_clause = else_keyword, colon, rewrite_body(body)
            new_finally_clause = None
            if stmt.finally_clause is not None:
                finally_keyword, colon, body = stmt.finally_clause
                new_finally_clause = finally_keyword, colon, rewrite_body(body)
            return stmt.derive(
                body=rewrite_body(stmt.body),
                handlers=new_handlers,
                else_clause=new_else_clause,
                finally_clause=new_finally_clause
            )
        if isinstance(stmt, PyFuncDef):
            return stmt.derive(body=rewrite_body(stmt.body))
        if isinstance(stmt, PyClassDef):
            return stmt.derive(body=rewrite_body(stmt.body))
        return stmt

    def rewrite_body(body: PyStmt | list[PyStmt]) -> PyStmt | list[PyStmt]:
        if not isinstance(body, list):
            return body
        new_stmts = list(rewrite_stmt(stmt) for stmt in body if not isinstance(stmt, PyPassStmt))
        return [ PyPassStmt() ] if not new_stmts else new_stmts

    return module.derive(stmts=list(rewrite_stmt(stmt) for stmt in module.stmts if not isinstance(stmt, PyPassStmt)))
