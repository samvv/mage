from .cst import *


from magelang.runtime import AbstractLexer, ScanError


class PyLexer(AbstractLexer):

    def lex(self) -> PyToken:
        i = self._curr_offset
        while True:
            keep = i
            ch = self._char_at(i)
            if (ch == '\n') or (ch == '\r') or (ch == '\t') or (ch == ' '):
                i += 1
                continue
            i = keep
            keep_1 = i
            ch_1 = self._char_at(i)
            if ch_1 == '#':
                i += 1
                while True:
                    keep_2 = i
                    matches_2 = True
                    keep_3 = i
                    keep_4 = i
                    ch_2 = self._char_at(i)
                    if ch_2 == '\r':
                        i += 1
                        ch_3 = self._char_at(i)
                        if ch_3 == '\n':
                            i += 1
                            i = keep_2
                            matches_2 = False
                    i = keep_4
                    keep_5 = i
                    ch_4 = self._char_at(i)
                    if ch_4 == '\n':
                        i += 1
                        i = keep_2
                        matches_2 = False
                    i = keep_5
                    i = keep_3
                    keep_6 = i
                    keep_7 = i
                    matches_3 = True
                    i = keep_7
                    matches_3 = False
                    i = keep_7
                    if matches_3:
                        i = keep_2
                        matches_2 = False
                    i = keep_6
                    i = keep_2
                    if matches_2:
                        continue
                    break
                continue
            i = keep_1
            break
        start = i
        keep_8 = i
        ch_7 = self._char_at(i)
        if ch_7 == '~':
            i += 1
            self._curr_offset = i
            return PyTilde()
        i = keep_8
        keep_9 = i
        ch_8 = self._char_at(i)
        if ch_8 == '|':
            i += 1
            self._curr_offset = i
            return PyVerticalBar()
        i = keep_9
        keep_10 = i
        ch_9 = self._char_at(i)
        if ch_9 == '^':
            i += 1
            self._curr_offset = i
            return PyCaret()
        i = keep_10
        keep_11 = i
        ch_10 = self._char_at(i)
        if ch_10 == ']':
            i += 1
            self._curr_offset = i
            return PyCloseBracket()
        i = keep_11
        keep_12 = i
        ch_11 = self._char_at(i)
        if ch_11 == '[':
            i += 1
            self._curr_offset = i
            return PyOpenBracket()
        i = keep_12
        keep_13 = i
        ch_12 = self._char_at(i)
        if ch_12 == '@':
            i += 1
            self._curr_offset = i
            return PyAtSign()
        i = keep_13
        keep_14 = i
        ch_13 = self._char_at(i)
        if ch_13 == '>':
            i += 1
            ch_14 = self._char_at(i)
            if ch_14 == '>':
                i += 1
                self._curr_offset = i
                return PyGreaterThanGreaterThan()
        i = keep_14
        keep_15 = i
        ch_15 = self._char_at(i)
        if ch_15 == '>':
            i += 1
            ch_16 = self._char_at(i)
            if ch_16 == '=':
                i += 1
                self._curr_offset = i
                return PyGreaterThanEquals()
        i = keep_15
        keep_16 = i
        ch_17 = self._char_at(i)
        if ch_17 == '>':
            i += 1
            self._curr_offset = i
            return PyGreaterThan()
        i = keep_16
        keep_17 = i
        ch_18 = self._char_at(i)
        if ch_18 == '=':
            i += 1
            ch_19 = self._char_at(i)
            if ch_19 == '=':
                i += 1
                self._curr_offset = i
                return PyEqualsEquals()
        i = keep_17
        keep_18 = i
        ch_20 = self._char_at(i)
        if ch_20 == '=':
            i += 1
            self._curr_offset = i
            return PyEquals()
        i = keep_18
        keep_19 = i
        ch_21 = self._char_at(i)
        if ch_21 == '<':
            i += 1
            ch_22 = self._char_at(i)
            if ch_22 == '=':
                i += 1
                self._curr_offset = i
                return PyLessThanEquals()
        i = keep_19
        keep_20 = i
        ch_23 = self._char_at(i)
        if ch_23 == '<':
            i += 1
            ch_24 = self._char_at(i)
            if ch_24 == '<':
                i += 1
                self._curr_offset = i
                return PyLessThanLessThan()
        i = keep_20
        keep_21 = i
        ch_25 = self._char_at(i)
        if ch_25 == '<':
            i += 1
            self._curr_offset = i
            return PyLessThan()
        i = keep_21
        keep_22 = i
        ch_26 = self._char_at(i)
        if ch_26 == ';':
            i += 1
            self._curr_offset = i
            return PySemicolon()
        i = keep_22
        keep_23 = i
        ch_27 = self._char_at(i)
        if ch_27 == ':':
            i += 1
            self._curr_offset = i
            return PyColon()
        i = keep_23
        keep_24 = i
        ch_28 = self._char_at(i)
        if ch_28 == '/':
            i += 1
            ch_29 = self._char_at(i)
            if ch_29 == '/':
                i += 1
                self._curr_offset = i
                return PySlashSlash()
        i = keep_24
        keep_25 = i
        ch_30 = self._char_at(i)
        if ch_30 == '/':
            i += 1
            self._curr_offset = i
            return PySlash()
        i = keep_25
        keep_26 = i
        ch_31 = self._char_at(i)
        if ch_31 == '.':
            i += 1
            ch_32 = self._char_at(i)
            if ch_32 == '.':
                i += 1
                ch_33 = self._char_at(i)
                if ch_33 == '.':
                    i += 1
                    self._curr_offset = i
                    return PyDotDotDot()
        i = keep_26
        keep_27 = i
        ch_34 = self._char_at(i)
        if ch_34 == '.':
            i += 1
            self._curr_offset = i
            return PyDot()
        i = keep_27
        keep_28 = i
        ch_35 = self._char_at(i)
        if ch_35 == '-':
            i += 1
            ch_36 = self._char_at(i)
            if ch_36 == '>':
                i += 1
                self._curr_offset = i
                return PyRArrow()
        i = keep_28
        keep_29 = i
        ch_37 = self._char_at(i)
        if ch_37 == '-':
            i += 1
            self._curr_offset = i
            return PyHyphen()
        i = keep_29
        keep_30 = i
        ch_38 = self._char_at(i)
        if ch_38 == ',':
            i += 1
            self._curr_offset = i
            return PyComma()
        i = keep_30
        keep_31 = i
        ch_39 = self._char_at(i)
        if ch_39 == '+':
            i += 1
            self._curr_offset = i
            return PyPlus()
        i = keep_31
        keep_32 = i
        ch_40 = self._char_at(i)
        if ch_40 == '*':
            i += 1
            ch_41 = self._char_at(i)
            if ch_41 == '*':
                i += 1
                self._curr_offset = i
                return PyAsteriskAsterisk()
        i = keep_32
        keep_33 = i
        ch_42 = self._char_at(i)
        if ch_42 == '*':
            i += 1
            self._curr_offset = i
            return PyAsterisk()
        i = keep_33
        keep_34 = i
        ch_43 = self._char_at(i)
        if ch_43 == ')':
            i += 1
            self._curr_offset = i
            return PyCloseParen()
        i = keep_34
        keep_35 = i
        ch_44 = self._char_at(i)
        if ch_44 == '(':
            i += 1
            self._curr_offset = i
            return PyOpenParen()
        i = keep_35
        keep_36 = i
        ch_45 = self._char_at(i)
        if ch_45 == '&':
            i += 1
            self._curr_offset = i
            return PyAmpersand()
        i = keep_36
        keep_37 = i
        ch_46 = self._char_at(i)
        if ch_46 == '%':
            i += 1
            self._curr_offset = i
            return PyPercent()
        i = keep_37
        keep_38 = i
        ch_47 = self._char_at(i)
        if ch_47 == '#':
            i += 1
            self._curr_offset = i
            return PyHashtag()
        i = keep_38
        keep_39 = i
        ch_48 = self._char_at(i)
        if ch_48 == '!':
            i += 1
            ch_49 = self._char_at(i)
            if ch_49 == '=':
                i += 1
                self._curr_offset = i
                return PyExclamationMarkEquals()
        i = keep_39
        keep_40 = i
        ch_50 = self._char_at(i)
        if ch_50 == '\r':
            i += 1
            ch_51 = self._char_at(i)
            if ch_51 == '\n':
                i += 1
                self._curr_offset = i
                return PyCarriageReturnLineFeed()
        i = keep_40
        keep_41 = i
        ch_52 = self._char_at(i)
        if ch_52 == '\n':
            i += 1
            self._curr_offset = i
            return PyLineFeed()
        i = keep_41
        keep_42 = i
        ch_53 = self._char_at(i)
        if ((ord(ch_53) >= 97) and (ord(ch_53) <= 122)) or ((ord(ch_53) >= 65) and (ord(ch_53) <= 90)) or (ch_53 == '_'):
            i += 1
            while True:
                ch_54 = self._char_at(i)
                if ((ord(ch_54) >= 97) and (ord(ch_54) <= 122)) or ((ord(ch_54) >= 65) and (ord(ch_54) <= 90)) or (ch_54 == '_') or ((ord(ch_54) >= 48) and (ord(ch_54) <= 57)):
                    i += 1
                    continue
                break
            self._curr_offset = i
            text = self._text[start:i]
            if text == 'while':
                return PyWhileKeyword()
            elif text == 'type':
                return PyTypeKeyword()
            elif text == 'try':
                return PyTryKeyword()
            elif text == 'return':
                return PyReturnKeyword()
            elif text == 'raise':
                return PyRaiseKeyword()
            elif text == 'pass':
                return PyPassKeyword()
            elif text == 'or':
                return PyOrKeyword()
            elif text == 'not':
                return PyNotKeyword()
            elif text == 'nonlocal':
                return PyNonlocalKeyword()
            elif text == 'is':
                return PyIsKeyword()
            elif text == 'in':
                return PyInKeyword()
            elif text == 'import':
                return PyImportKeyword()
            elif text == 'if':
                return PyIfKeyword()
            elif text == 'global':
                return PyGlobalKeyword()
            elif text == 'from':
                return PyFromKeyword()
            elif text == 'for':
                return PyForKeyword()
            elif text == 'finally':
                return PyFinallyKeyword()
            elif text == 'except':
                return PyExceptKeyword()
            elif text == 'else':
                return PyElseKeyword()
            elif text == 'elif':
                return PyElifKeyword()
            elif text == 'del':
                return PyDelKeyword()
            elif text == 'def':
                return PyDefKeyword()
            elif text == 'continue':
                return PyContinueKeyword()
            elif text == 'class':
                return PyClassKeyword()
            elif text == 'break':
                return PyBreakKeyword()
            elif text == 'async':
                return PyAsyncKeyword()
            elif text == 'as':
                return PyAsKeyword()
            elif text == 'and':
                return PyAndKeyword()
            return PyIdent(str(self._text[start:i]))
        i = keep_42
        keep_43 = i
        while True:
            ch_55 = self._char_at(i)
            if ((ord(ch_55) >= 48) and (ord(ch_55) <= 57)):
                i += 1
                continue
            break
        ch_56 = self._char_at(i)
        if ch_56 == '.':
            i += 1
            matches_6 = True
            for _ in range(0, 1):
                ch_57 = self._char_at(i)
                if ((ord(ch_57) >= 48) and (ord(ch_57) <= 57)):
                    i += 1
                    continue
                matches_6 = False
                break
            if matches_6:
                while True:
                    ch_58 = self._char_at(i)
                    if ((ord(ch_58) >= 48) and (ord(ch_58) <= 57)):
                        i += 1
                        continue
                    break
                self._curr_offset = i
                return PyFloat(float(self._text[start:i]))
        i = keep_43
        keep_44 = i
        keep_45 = i
        ch_59 = self._char_at(i)
        if ((ord(ch_59) >= 49) and (ord(ch_59) <= 57)):
            i += 1
            while True:
                ch_60 = self._char_at(i)
                if ((ord(ch_60) >= 48) and (ord(ch_60) <= 57)):
                    i += 1
                    continue
                break
            self._curr_offset = i
            return PyInteger(int(self._text[start:i]))
        i = keep_45
        keep_46 = i
        matches_8 = True
        for _ in range(0, 1):
            ch_61 = self._char_at(i)
            if ch_61 == '0':
                i += 1
                continue
            matches_8 = False
            break
        if matches_8:
            while True:
                ch_62 = self._char_at(i)
                if ch_62 == '0':
                    i += 1
                    continue
                break
            self._curr_offset = i
            return PyInteger(int(self._text[start:i]))
        i = keep_46
        i = keep_44
        keep_47 = i
        keep_48 = i
        ch_63 = self._char_at(i)
        if ch_63 == '"':
            i += 1
            while True:
                keep_49 = i
                matches_10 = True
                ch_64 = self._char_at(i)
                if ch_64 == '"':
                    i += 1
                    i = keep_49
                    matches_10 = False
                i = keep_49
                if matches_10:
                    continue
                break
            ch_66 = self._char_at(i)
            if ch_66 == '"':
                i += 1
                self._curr_offset = i
                return PyString(str(self._text[start:i]))
        i = keep_48
        keep_50 = i
        ch_67 = self._char_at(i)
        if ch_67 == "'":
            i += 1
            while True:
                keep_51 = i
                matches_12 = True
                ch_68 = self._char_at(i)
                if ch_68 == "'":
                    i += 1
                    i = keep_51
                    matches_12 = False
                i = keep_51
                if matches_12:
                    continue
                break
            ch_70 = self._char_at(i)
            if ch_70 == "'":
                i += 1
                self._curr_offset = i
                return PyString(str(self._text[start:i]))
        i = keep_50
        i = keep_47
        raise ScanError()


