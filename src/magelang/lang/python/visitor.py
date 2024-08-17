from typing import Callable, no_type_check


from .cst import *


@no_type_check
def for_each_py_pattern(node: PyPattern, proc: Callable[[PyPattern], None]):
    if isinstance(node, PyNamedPattern):
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        for (element, separator) in node.slices.elements:
            if is_py_pattern(element):
                proc(element)
        if node.slices.last is not None:
            if is_py_pattern(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredPattern):
        return
    if isinstance(node, PyListPattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTuplePattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return


@no_type_check
def for_each_py_expr(node: PyExpr, proc: Callable[[PyExpr], None]):
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                if is_py_expr(element.lower):
                    proc(element.lower)
                if is_py_expr(element.upper):
                    proc(element.upper)
                if isinstance(element.step, tuple):
                    proc(element.step[1])
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                if is_py_expr(node.slices.last.lower):
                    proc(node.slices.last.lower)
                if is_py_expr(node.slices.last.upper):
                    proc(node.slices.last.upper)
                if isinstance(node.slices.last.step, tuple):
                    proc(node.slices.last.step[1])
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return


@no_type_check
def for_each_py_arg(node: PyArg, proc: Callable[[PyArg], None]):
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                if is_py_expr(element.lower):
                    proc(element.lower)
                if is_py_expr(element.upper):
                    proc(element.upper)
                if isinstance(element.step, tuple):
                    proc(element.step[1])
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                if is_py_expr(node.slices.last.lower):
                    proc(node.slices.last.lower)
                if is_py_expr(node.slices.last.upper):
                    proc(node.slices.last.upper)
                if isinstance(node.slices.last.step, tuple):
                    proc(node.slices.last.step[1])
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element, separator) in node.args.elements:
            proc(element)
        if node.args.last is not None:
            proc(node.args.last)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return


@no_type_check
def for_each_py_stmt(node: PyStmt, proc: Callable[[PyStmt], None]):
    if isinstance(node, PyImportStmt):
        return
    if isinstance(node, PyImportFromStmt):
        return
    if isinstance(node, PyRetStmt):
        return
    if isinstance(node, PyExprStmt):
        return
    if isinstance(node, PyAssignStmt):
        return
    if isinstance(node, PyPassStmt):
        return
    if isinstance(node, PyGlobalStmt):
        return
    if isinstance(node, PyNonlocalStmt):
        return
    if isinstance(node, PyIfStmt):
        return
    if isinstance(node, PyDeleteStmt):
        return
    if isinstance(node, PyRaiseStmt):
        return
    if isinstance(node, PyForStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyWhileStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyBreakStmt):
        return
    if isinstance(node, PyContinueStmt):
        return
    if isinstance(node, PyTypeAliasStmt):
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_2 in node.finally_clause[2]:
                    proc(element_2)
        return
    if isinstance(node, PyClassDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyFuncDef):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return


@no_type_check
def for_each_py_node(node: PyNode, proc: Callable[[PyNode], None]):
    if isinstance(node, PySlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[1])
        return
    if isinstance(node, PyNamedPattern):
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_pattern(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_pattern(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredPattern):
        proc(node.expr)
        return
    if isinstance(node, PyListPattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTuplePattern):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyEllipsisExpr):
        return
    if isinstance(node, PyGuard):
        proc(node.expr)
        return
    if isinstance(node, PyComprehension):
        proc(node.pattern)
        proc(node.target)
        for element in node.guards:
            proc(element)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element in node.generators:
            proc(element)
        return
    if isinstance(node, PyConstExpr):
        return
    if isinstance(node, PyNestExpr):
        proc(node.expr)
        return
    if isinstance(node, PyNamedExpr):
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_expr(element):
                proc(element)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyTupleExpr):
        for (element, separator) in node.elements.elements:
            proc(element)
        if node.elements.last is not None:
            proc(node.elements.last)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        for (element, separator) in node.args.elements:
            proc(element)
        if node.args.last is not None:
            proc(node.args.last)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyQualName):
        return
    if isinstance(node, PyAbsolutePath):
        proc(node.name)
        return
    if isinstance(node, PyRelativePath):
        if isinstance(node.name, PyQualName):
            proc(node.name)
        return
    if isinstance(node, PyAlias):
        proc(node.path)
        return
    if isinstance(node, PyFromAlias):
        return
    if isinstance(node, PyImportStmt):
        for (element, separator) in node.aliases.elements:
            proc(element)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyImportFromStmt):
        proc(node.path)
        for (element, separator) in node.aliases.elements:
            proc(element)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyRetStmt):
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.value, tuple):
            proc(node.value[1])
        return
    if isinstance(node, PyPassStmt):
        return
    if isinstance(node, PyGlobalStmt):
        return
    if isinstance(node, PyNonlocalStmt):
        return
    if isinstance(node, PyIfCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElifCase):
        proc(node.test)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElseCase):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element in node.alternatives:
            proc(element)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyDeleteStmt):
        proc(node.pattern)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[1])
        return
    if isinstance(node, PyForStmt):
        proc(node.pattern)
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyBreakStmt):
        return
    if isinstance(node, PyContinueStmt):
        return
    if isinstance(node, PyTypeAliasStmt):
        if isinstance(node.type_params, tuple):
            for (element, separator) in node.type_params[1].elements:
                proc(element)
            if node.type_params[1].last is not None:
                proc(node.type_params[1].last)
        proc(node.expr)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.expr)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyTryStmt):
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        for element_1 in node.handlers:
            proc(element_1)
        if isinstance(node.else_clause, tuple):
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_2 in node.else_clause[2]:
                    proc(element_2)
        if isinstance(node.finally_clause, tuple):
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_3 in node.finally_clause[2]:
                    proc(element_3)
        return
    if isinstance(node, PyClassDef):
        for element in node.decorators:
            proc(element)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_1 in node.body:
                proc(element_1)
        return
    if isinstance(node, PyNamedParam):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[1])
        return
    if isinstance(node, PyRestPosParam):
        return
    if isinstance(node, PyRestKeywordParam):
        return
    if isinstance(node, PyPosSepParam):
        return
    if isinstance(node, PyKwSepParam):
        return
    if isinstance(node, PyDecorator):
        proc(node.expr)
        return
    if isinstance(node, PyFuncDef):
        for element in node.decorators:
            proc(element)
        for (element_1, separator) in node.params.elements:
            proc(element_1)
        if node.params.last is not None:
            proc(node.params.last)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[1])
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyModule):
        for element in node.stmts:
            proc(element)
        return


@no_type_check
def for_each_py_syntax(node: PySyntax, proc: Callable[[PySyntax], None]):
    if isinstance(node, PyIdent):
        return
    if isinstance(node, PyFloat):
        return
    if isinstance(node, PyInteger):
        return
    if isinstance(node, PyString):
        return
    if isinstance(node, PySlice):
        if is_py_expr(node.lower):
            proc(node.lower)
        proc(node.colon)
        if is_py_expr(node.upper):
            proc(node.upper)
        if isinstance(node.step, tuple):
            proc(node.step[0])
            proc(node.step[1])
        return
    if isinstance(node, PyNamedPattern):
        proc(node.name)
        return
    if isinstance(node, PyAttrPattern):
        proc(node.pattern)
        proc(node.dot)
        proc(node.name)
        return
    if isinstance(node, PySubscriptPattern):
        proc(node.pattern)
        proc(node.open_bracket)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_pattern(element):
                proc(element)
            proc(separator)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_pattern(node.slices.last):
                proc(node.slices.last)
        proc(node.close_bracket)
        return
    if isinstance(node, PyStarredPattern):
        proc(node.asterisk)
        proc(node.expr)
        return
    if isinstance(node, PyListPattern):
        proc(node.open_bracket)
        for (element, separator) in node.elements.elements:
            proc(element)
            proc(separator)
        if node.elements.last is not None:
            proc(node.elements.last)
        proc(node.close_bracket)
        return
    if isinstance(node, PyTuplePattern):
        proc(node.open_paren)
        for (element, separator) in node.elements.elements:
            proc(element)
            proc(separator)
        if node.elements.last is not None:
            proc(node.elements.last)
        proc(node.close_paren)
        return
    if isinstance(node, PyEllipsisExpr):
        proc(node.dot_dot_dot)
        return
    if isinstance(node, PyGuard):
        proc(node.if_keyword)
        proc(node.expr)
        return
    if isinstance(node, PyComprehension):
        if isinstance(node.async_keyword, PyAsyncKeyword):
            proc(node.async_keyword)
        proc(node.for_keyword)
        proc(node.pattern)
        proc(node.in_keyword)
        proc(node.target)
        for element in node.guards:
            proc(element)
        return
    if isinstance(node, PyGeneratorExpr):
        proc(node.element)
        for element in node.generators:
            proc(element)
        return
    if isinstance(node, PyConstExpr):
        if isinstance(node.literal, PyFloat):
            proc(node.literal)
        elif isinstance(node.literal, PyInteger):
            proc(node.literal)
        elif isinstance(node.literal, PyString):
            proc(node.literal)
        return
    if isinstance(node, PyNestExpr):
        proc(node.open_paren)
        proc(node.expr)
        proc(node.close_paren)
        return
    if isinstance(node, PyNamedExpr):
        proc(node.name)
        return
    if isinstance(node, PyAttrExpr):
        proc(node.expr)
        proc(node.dot)
        proc(node.name)
        return
    if isinstance(node, PySubscriptExpr):
        proc(node.expr)
        proc(node.open_bracket)
        for (element, separator) in node.slices.elements:
            if isinstance(element, PySlice):
                proc(element)
            elif is_py_expr(element):
                proc(element)
            proc(separator)
        if node.slices.last is not None:
            if isinstance(node.slices.last, PySlice):
                proc(node.slices.last)
            elif is_py_expr(node.slices.last):
                proc(node.slices.last)
        proc(node.close_bracket)
        return
    if isinstance(node, PyStarredExpr):
        proc(node.asterisk)
        proc(node.expr)
        return
    if isinstance(node, PyListExpr):
        proc(node.open_bracket)
        for (element, separator) in node.elements.elements:
            proc(element)
            proc(separator)
        if node.elements.last is not None:
            proc(node.elements.last)
        proc(node.close_bracket)
        return
    if isinstance(node, PyTupleExpr):
        proc(node.open_paren)
        for (element, separator) in node.elements.elements:
            proc(element)
            proc(separator)
        if node.elements.last is not None:
            proc(node.elements.last)
        proc(node.close_paren)
        return
    if isinstance(node, PyKeywordArg):
        proc(node.name)
        proc(node.equals)
        proc(node.expr)
        return
    if isinstance(node, PyCallExpr):
        proc(node.operator)
        proc(node.open_paren)
        for (element, separator) in node.args.elements:
            proc(element)
            proc(separator)
        if node.args.last is not None:
            proc(node.args.last)
        proc(node.close_paren)
        return
    if isinstance(node, PyPrefixExpr):
        proc(node.prefix_op)
        proc(node.expr)
        return
    if isinstance(node, PyInfixExpr):
        proc(node.left)
        proc(node.right)
        return
    if isinstance(node, PyQualName):
        for element in node.modules:
            proc(element[0])
            proc(element[1])
        proc(node.name)
        return
    if isinstance(node, PyAbsolutePath):
        proc(node.name)
        return
    if isinstance(node, PyRelativePath):
        for element in node.dots:
            proc(element)
        if isinstance(node.name, PyQualName):
            proc(node.name)
        return
    if isinstance(node, PyAlias):
        proc(node.path)
        if isinstance(node.asname, tuple):
            proc(node.asname[0])
            proc(node.asname[1])
        return
    if isinstance(node, PyFromAlias):
        if isinstance(node.name, PyAsterisk):
            proc(node.name)
        elif isinstance(node.name, PyIdent):
            proc(node.name)
        if isinstance(node.asname, tuple):
            proc(node.asname[0])
            proc(node.asname[1])
        return
    if isinstance(node, PyImportStmt):
        proc(node.import_keyword)
        for (element, separator) in node.aliases.elements:
            proc(element)
            proc(separator)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyImportFromStmt):
        proc(node.from_keyword)
        proc(node.path)
        proc(node.import_keyword)
        for (element, separator) in node.aliases.elements:
            proc(element)
            proc(separator)
        if node.aliases.last is not None:
            proc(node.aliases.last)
        return
    if isinstance(node, PyRetStmt):
        proc(node.return_keyword)
        if is_py_expr(node.expr):
            proc(node.expr)
        return
    if isinstance(node, PyExprStmt):
        proc(node.expr)
        return
    if isinstance(node, PyAssignStmt):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[0])
            proc(node.annotation[1])
        if isinstance(node.value, tuple):
            proc(node.value[0])
            proc(node.value[1])
        return
    if isinstance(node, PyPassStmt):
        proc(node.pass_keyword)
        return
    if isinstance(node, PyGlobalStmt):
        proc(node.global_keyword)
        for (element, separator) in node.names.elements:
            proc(element)
            proc(separator)
        if node.names.last is not None:
            proc(node.names.last)
        return
    if isinstance(node, PyNonlocalStmt):
        proc(node.nonlocal_keyword)
        for (element, separator) in node.names.elements:
            proc(element)
            proc(separator)
        if node.names.last is not None:
            proc(node.names.last)
        return
    if isinstance(node, PyIfCase):
        proc(node.if_keyword)
        proc(node.test)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElifCase):
        proc(node.elif_keyword)
        proc(node.test)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyElseCase):
        proc(node.else_keyword)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyIfStmt):
        proc(node.first)
        for element in node.alternatives:
            proc(element)
        if isinstance(node.last, PyElseCase):
            proc(node.last)
        return
    if isinstance(node, PyDeleteStmt):
        proc(node.del_keyword)
        proc(node.pattern)
        return
    if isinstance(node, PyRaiseStmt):
        proc(node.raise_keyword)
        proc(node.expr)
        if isinstance(node.cause, tuple):
            proc(node.cause[0])
            proc(node.cause[1])
        return
    if isinstance(node, PyForStmt):
        proc(node.for_keyword)
        proc(node.pattern)
        proc(node.in_keyword)
        proc(node.expr)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            proc(node.else_clause[0])
            proc(node.else_clause[1])
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyWhileStmt):
        proc(node.while_keyword)
        proc(node.expr)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        if isinstance(node.else_clause, tuple):
            proc(node.else_clause[0])
            proc(node.else_clause[1])
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_1 in node.else_clause[2]:
                    proc(element_1)
        return
    if isinstance(node, PyBreakStmt):
        proc(node.break_keyword)
        return
    if isinstance(node, PyContinueStmt):
        proc(node.continue_keyword)
        return
    if isinstance(node, PyTypeAliasStmt):
        proc(node.type_keyword)
        proc(node.name)
        if isinstance(node.type_params, tuple):
            proc(node.type_params[0])
            for (element, separator) in node.type_params[1].elements:
                proc(element)
                proc(separator)
            if node.type_params[1].last is not None:
                proc(node.type_params[1].last)
            proc(node.type_params[2])
        proc(node.equals)
        proc(node.expr)
        return
    if isinstance(node, PyExceptHandler):
        proc(node.except_keyword)
        proc(node.expr)
        if isinstance(node.binder, tuple):
            proc(node.binder[0])
            proc(node.binder[1])
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        return
    if isinstance(node, PyTryStmt):
        proc(node.try_keyword)
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element in node.body:
                proc(element)
        for element_1 in node.handlers:
            proc(element_1)
        if isinstance(node.else_clause, tuple):
            proc(node.else_clause[0])
            proc(node.else_clause[1])
            if is_py_stmt(node.else_clause[2]):
                proc(node.else_clause[2])
            elif isinstance(node.else_clause[2], list):
                for element_2 in node.else_clause[2]:
                    proc(element_2)
        if isinstance(node.finally_clause, tuple):
            proc(node.finally_clause[0])
            proc(node.finally_clause[1])
            if is_py_stmt(node.finally_clause[2]):
                proc(node.finally_clause[2])
            elif isinstance(node.finally_clause[2], list):
                for element_3 in node.finally_clause[2]:
                    proc(element_3)
        return
    if isinstance(node, PyClassDef):
        for element in node.decorators:
            proc(element)
        proc(node.class_keyword)
        proc(node.name)
        if isinstance(node.bases, tuple):
            proc(node.bases[0])
            for (element_1, separator) in node.bases[1].elements:
                proc(element_1)
                proc(separator)
            if node.bases[1].last is not None:
                proc(node.bases[1].last)
            proc(node.bases[2])
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyNamedParam):
        proc(node.pattern)
        if isinstance(node.annotation, tuple):
            proc(node.annotation[0])
            proc(node.annotation[1])
        if isinstance(node.default, tuple):
            proc(node.default[0])
            proc(node.default[1])
        return
    if isinstance(node, PyRestPosParam):
        proc(node.asterisk)
        proc(node.name)
        return
    if isinstance(node, PyRestKeywordParam):
        proc(node.asterisk_asterisk)
        proc(node.name)
        return
    if isinstance(node, PyPosSepParam):
        proc(node.slash)
        return
    if isinstance(node, PyKwSepParam):
        proc(node.asterisk)
        return
    if isinstance(node, PyDecorator):
        proc(node.at_sign)
        proc(node.expr)
        return
    if isinstance(node, PyFuncDef):
        for element in node.decorators:
            proc(element)
        if isinstance(node.async_keyword, PyAsyncKeyword):
            proc(node.async_keyword)
        proc(node.def_keyword)
        proc(node.name)
        proc(node.open_paren)
        for (element_1, separator) in node.params.elements:
            proc(element_1)
            proc(separator)
        if node.params.last is not None:
            proc(node.params.last)
        proc(node.close_paren)
        if isinstance(node.return_type, tuple):
            proc(node.return_type[0])
            proc(node.return_type[1])
        proc(node.colon)
        if is_py_stmt(node.body):
            proc(node.body)
        elif isinstance(node.body, list):
            for element_2 in node.body:
                proc(element_2)
        return
    if isinstance(node, PyModule):
        for element in node.stmts:
            proc(element)
        return
    if isinstance(node, PyTilde):
        return
    if isinstance(node, PyVerticalBar):
        return
    if isinstance(node, PyWhileKeyword):
        return
    if isinstance(node, PyTypeKeyword):
        return
    if isinstance(node, PyTryKeyword):
        return
    if isinstance(node, PyReturnKeyword):
        return
    if isinstance(node, PyRaiseKeyword):
        return
    if isinstance(node, PyPassKeyword):
        return
    if isinstance(node, PyOrKeyword):
        return
    if isinstance(node, PyNotKeyword):
        return
    if isinstance(node, PyNonlocalKeyword):
        return
    if isinstance(node, PyIsKeyword):
        return
    if isinstance(node, PyInKeyword):
        return
    if isinstance(node, PyImportKeyword):
        return
    if isinstance(node, PyIfKeyword):
        return
    if isinstance(node, PyGlobalKeyword):
        return
    if isinstance(node, PyFromKeyword):
        return
    if isinstance(node, PyForKeyword):
        return
    if isinstance(node, PyFinallyKeyword):
        return
    if isinstance(node, PyExceptKeyword):
        return
    if isinstance(node, PyElseKeyword):
        return
    if isinstance(node, PyElifKeyword):
        return
    if isinstance(node, PyDelKeyword):
        return
    if isinstance(node, PyDefKeyword):
        return
    if isinstance(node, PyContinueKeyword):
        return
    if isinstance(node, PyClassKeyword):
        return
    if isinstance(node, PyBreakKeyword):
        return
    if isinstance(node, PyAsyncKeyword):
        return
    if isinstance(node, PyAsKeyword):
        return
    if isinstance(node, PyAndKeyword):
        return
    if isinstance(node, PyCaret):
        return
    if isinstance(node, PyCloseBracket):
        return
    if isinstance(node, PyOpenBracket):
        return
    if isinstance(node, PyAtSign):
        return
    if isinstance(node, PyGreaterThanGreaterThan):
        return
    if isinstance(node, PyGreaterThanEquals):
        return
    if isinstance(node, PyGreaterThan):
        return
    if isinstance(node, PyEqualsEquals):
        return
    if isinstance(node, PyEquals):
        return
    if isinstance(node, PyLessThanEquals):
        return
    if isinstance(node, PyLessThanLessThan):
        return
    if isinstance(node, PyLessThan):
        return
    if isinstance(node, PySemicolon):
        return
    if isinstance(node, PyColon):
        return
    if isinstance(node, PySlashSlash):
        return
    if isinstance(node, PySlash):
        return
    if isinstance(node, PyDotDotDot):
        return
    if isinstance(node, PyDot):
        return
    if isinstance(node, PyRArrow):
        return
    if isinstance(node, PyHyphen):
        return
    if isinstance(node, PyComma):
        return
    if isinstance(node, PyPlus):
        return
    if isinstance(node, PyAsteriskAsterisk):
        return
    if isinstance(node, PyAsterisk):
        return
    if isinstance(node, PyCloseParen):
        return
    if isinstance(node, PyOpenParen):
        return
    if isinstance(node, PyAmpersand):
        return
    if isinstance(node, PyPercent):
        return
    if isinstance(node, PyHashtag):
        return
    if isinstance(node, PyExclamationMarkEquals):
        return
    if isinstance(node, PyCarriageReturnLineFeed):
        return
    if isinstance(node, PyLineFeed):
        return


