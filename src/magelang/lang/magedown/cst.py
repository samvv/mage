from enum import IntEnum


from typing import Any, TypeGuard, TypeIs, TypedDict, Never, Unpack, Sequence, Callable, assert_never, no_type_check


from magelang.runtime import BaseSyntax, Punctuated, ImmutablePunct, Span


class _MagedownBaseSyntax(BaseSyntax):

    pass


class _MagedownBaseNode(_MagedownBaseSyntax):

    pass


class _MagedownBaseToken(_MagedownBaseSyntax):

    def __init__(self, span: Span | None = None):
        self.span = span


class MagedownAcceptKeyword(_MagedownBaseToken):

    pass


class MagedownBacktick(_MagedownBaseToken):

    pass


class MagedownBacktickBacktickBacktick(_MagedownBaseToken):

    pass


class MagedownCloseBrace(_MagedownBaseToken):

    pass


class MagedownCloseBracket(_MagedownBaseToken):

    pass


class MagedownCloseBracketCloseBracket(_MagedownBaseToken):

    pass


class MagedownCloseParen(_MagedownBaseToken):

    pass


class MagedownHashtag(_MagedownBaseToken):

    pass


class MagedownLineFeed(_MagedownBaseToken):

    pass


class MagedownOpenBrace(_MagedownBaseToken):

    pass


class MagedownOpenBraceSlash(_MagedownBaseToken):

    pass


class MagedownOpenBracket(_MagedownBaseToken):

    pass


class MagedownOpenBracketOpenBracket(_MagedownBaseToken):

    pass


class MagedownOpenParen(_MagedownBaseToken):

    pass


class MagedownRejectKeyword(_MagedownBaseToken):

    pass


class MagedownAcceptsDeriveKwargs(TypedDict, total=False):

    open_brace: 'MagedownOpenBrace | None'

    accept_keyword: 'MagedownAcceptKeyword | None'

    close_brace: 'MagedownCloseBrace | None'

    text: 'str'

    open_brace_slash: 'MagedownOpenBraceSlash | None'

    accept_keyword_2: 'MagedownAcceptKeyword | None'

    close_brace_2: 'MagedownCloseBrace | None'


class MagedownAccepts(_MagedownBaseNode):

    def __init__(self, text: 'str', *, open_brace: 'MagedownOpenBrace | None' = None, accept_keyword: 'MagedownAcceptKeyword | None' = None, close_brace: 'MagedownCloseBrace | None' = None, open_brace_slash: 'MagedownOpenBraceSlash | None' = None, accept_keyword_2: 'MagedownAcceptKeyword | None' = None, close_brace_2: 'MagedownCloseBrace | None' = None) -> None:
        self.open_brace: MagedownOpenBrace = _coerce_union_2_decl_open_brace_none_to_decl_open_brace(open_brace)
        self.accept_keyword: MagedownAcceptKeyword = _coerce_union_2_decl_accept_keyword_none_to_decl_accept_keyword(accept_keyword)
        self.close_brace: MagedownCloseBrace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(close_brace)
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.open_brace_slash: MagedownOpenBraceSlash = _coerce_union_2_decl_open_brace_slash_none_to_decl_open_brace_slash(open_brace_slash)
        self.accept_keyword_2: MagedownAcceptKeyword = _coerce_union_2_decl_accept_keyword_none_to_decl_accept_keyword(accept_keyword_2)
        self.close_brace_2: MagedownCloseBrace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(close_brace_2)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownAcceptsDeriveKwargs]) -> 'MagedownAccepts':
        open_brace = _coerce_union_2_decl_open_brace_none_to_decl_open_brace(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        accept_keyword = _coerce_union_2_decl_accept_keyword_none_to_decl_accept_keyword(kwargs['accept_keyword']) if 'accept_keyword' in kwargs else self.accept_keyword
        close_brace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        open_brace_slash = _coerce_union_2_decl_open_brace_slash_none_to_decl_open_brace_slash(kwargs['open_brace_slash']) if 'open_brace_slash' in kwargs else self.open_brace_slash
        accept_keyword_2 = _coerce_union_2_decl_accept_keyword_none_to_decl_accept_keyword(kwargs['accept_keyword_2']) if 'accept_keyword_2' in kwargs else self.accept_keyword_2
        close_brace_2 = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(kwargs['close_brace_2']) if 'close_brace_2' in kwargs else self.close_brace_2
        return MagedownAccepts(open_brace=open_brace, accept_keyword=accept_keyword, close_brace=close_brace, text=text, open_brace_slash=open_brace_slash, accept_keyword_2=accept_keyword_2, close_brace_2=close_brace_2)

    def parent(self) -> 'MagedownAcceptsParent':
        assert(self._parent is not None)
        return self._parent


class MagedownCodeBlockDeriveKwargs(TypedDict, total=False):

    backtick_backtick_backtick: 'MagedownBacktickBacktickBacktick | None'

    lang: 'MagedownName | None'

    text: 'str'

    backtick_backtick_backtick_2: 'MagedownBacktickBacktickBacktick | None'


class MagedownCodeBlock(_MagedownBaseNode):

    def __init__(self, text: 'str', *, backtick_backtick_backtick: 'MagedownBacktickBacktickBacktick | None' = None, lang: 'MagedownName | None' = None, backtick_backtick_backtick_2: 'MagedownBacktickBacktickBacktick | None' = None) -> None:
        self.backtick_backtick_backtick: MagedownBacktickBacktickBacktick = _coerce_union_2_decl_backtick_backtick_backtick_none_to_decl_backtick_backtick_backtick(backtick_backtick_backtick)
        self.lang: MagedownName | None = _coerce_union_2_decl_name_none_to_union_2_decl_name_none(lang)
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.backtick_backtick_backtick_2: MagedownBacktickBacktickBacktick = _coerce_union_2_decl_backtick_backtick_backtick_none_to_decl_backtick_backtick_backtick(backtick_backtick_backtick_2)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownCodeBlockDeriveKwargs]) -> 'MagedownCodeBlock':
        backtick_backtick_backtick = _coerce_union_2_decl_backtick_backtick_backtick_none_to_decl_backtick_backtick_backtick(kwargs['backtick_backtick_backtick']) if 'backtick_backtick_backtick' in kwargs else self.backtick_backtick_backtick
        lang = _coerce_union_2_decl_name_none_to_union_2_decl_name_none(kwargs['lang']) if 'lang' in kwargs else self.lang
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        backtick_backtick_backtick_2 = _coerce_union_2_decl_backtick_backtick_backtick_none_to_decl_backtick_backtick_backtick(kwargs['backtick_backtick_backtick_2']) if 'backtick_backtick_backtick_2' in kwargs else self.backtick_backtick_backtick_2
        return MagedownCodeBlock(backtick_backtick_backtick=backtick_backtick_backtick, lang=lang, text=text, backtick_backtick_backtick_2=backtick_backtick_backtick_2)

    def parent(self) -> 'MagedownCodeBlockParent':
        assert(self._parent is not None)
        return self._parent


class MagedownDocumentDeriveKwargs(TypedDict, total=False):

    elements: 'Sequence[MagedownSpecial | MagedownText | str] | None'


class MagedownDocument(_MagedownBaseNode):

    def count_elements(self) -> int:
        return len(self.elements)

    def __init__(self, *, elements: 'Sequence[MagedownSpecial | MagedownText | str] | None' = None) -> None:
        self.elements: list[MagedownSpecial | MagedownText] = _coerce_union_2_list_union_3_decl_special_decl_text_extern_string_none_to_list_union_2_decl_special_decl_text(elements)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownDocumentDeriveKwargs]) -> 'MagedownDocument':
        elements = _coerce_union_2_list_union_3_decl_special_decl_text_extern_string_none_to_list_union_2_decl_special_decl_text(kwargs['elements']) if 'elements' in kwargs else self.elements
        return MagedownDocument(elements=elements)

    def parent(self) -> 'MagedownDocumentParent':
        raise AssertionError('trying to access the parent node of a top-level node')


class MagedownHeadingDeriveKwargs(TypedDict, total=False):

    hashtags: 'Sequence[MagedownHashtag] | int'

    text: 'str'


class MagedownHeading(_MagedownBaseNode):

    def count_hashtags(self) -> int:
        return len(self.hashtags)

    def __init__(self, hashtags: 'Sequence[MagedownHashtag] | int', text: 'str') -> None:
        self.hashtags: list[MagedownHashtag] = _coerce_union_2_list_decl_hashtag_required_extern_integer_to_list_decl_hashtag_required(hashtags)
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownHeadingDeriveKwargs]) -> 'MagedownHeading':
        hashtags = _coerce_union_2_list_decl_hashtag_required_extern_integer_to_list_decl_hashtag_required(kwargs['hashtags']) if 'hashtags' in kwargs else self.hashtags
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownHeading(hashtags=hashtags, text=text)

    def parent(self) -> 'MagedownHeadingParent':
        assert(self._parent is not None)
        return self._parent


class MagedownInlineCodeDeriveKwargs(TypedDict, total=False):

    backtick: 'MagedownBacktick | None'

    text: 'str'

    backtick_2: 'MagedownBacktick | None'


class MagedownInlineCode(_MagedownBaseNode):

    def __init__(self, text: 'str', *, backtick: 'MagedownBacktick | None' = None, backtick_2: 'MagedownBacktick | None' = None) -> None:
        self.backtick: MagedownBacktick = _coerce_union_2_decl_backtick_none_to_decl_backtick(backtick)
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.backtick_2: MagedownBacktick = _coerce_union_2_decl_backtick_none_to_decl_backtick(backtick_2)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownInlineCodeDeriveKwargs]) -> 'MagedownInlineCode':
        backtick = _coerce_union_2_decl_backtick_none_to_decl_backtick(kwargs['backtick']) if 'backtick' in kwargs else self.backtick
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        backtick_2 = _coerce_union_2_decl_backtick_none_to_decl_backtick(kwargs['backtick_2']) if 'backtick_2' in kwargs else self.backtick_2
        return MagedownInlineCode(backtick=backtick, text=text, backtick_2=backtick_2)

    def parent(self) -> 'MagedownInlineCodeParent':
        assert(self._parent is not None)
        return self._parent


class MagedownLinkDeriveKwargs(TypedDict, total=False):

    open_bracket: 'MagedownOpenBracket | None'

    text: 'str'

    close_bracket: 'MagedownCloseBracket | None'

    open_paren: 'MagedownOpenParen | None'

    href: 'str'

    close_paren: 'MagedownCloseParen | None'


class MagedownLink(_MagedownBaseNode):

    def __init__(self, text: 'str', href: 'str', *, open_bracket: 'MagedownOpenBracket | None' = None, close_bracket: 'MagedownCloseBracket | None' = None, open_paren: 'MagedownOpenParen | None' = None, close_paren: 'MagedownCloseParen | None' = None) -> None:
        self.open_bracket: MagedownOpenBracket = _coerce_union_2_decl_open_bracket_none_to_decl_open_bracket(open_bracket)
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.close_bracket: MagedownCloseBracket = _coerce_union_2_decl_close_bracket_none_to_decl_close_bracket(close_bracket)
        self.open_paren: MagedownOpenParen = _coerce_union_2_decl_open_paren_none_to_decl_open_paren(open_paren)
        self.href: str = _coerce_extern_string_to_extern_string(href)
        self.close_paren: MagedownCloseParen = _coerce_union_2_decl_close_paren_none_to_decl_close_paren(close_paren)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownLinkDeriveKwargs]) -> 'MagedownLink':
        open_bracket = _coerce_union_2_decl_open_bracket_none_to_decl_open_bracket(kwargs['open_bracket']) if 'open_bracket' in kwargs else self.open_bracket
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        close_bracket = _coerce_union_2_decl_close_bracket_none_to_decl_close_bracket(kwargs['close_bracket']) if 'close_bracket' in kwargs else self.close_bracket
        open_paren = _coerce_union_2_decl_open_paren_none_to_decl_open_paren(kwargs['open_paren']) if 'open_paren' in kwargs else self.open_paren
        href = _coerce_extern_string_to_extern_string(kwargs['href']) if 'href' in kwargs else self.href
        close_paren = _coerce_union_2_decl_close_paren_none_to_decl_close_paren(kwargs['close_paren']) if 'close_paren' in kwargs else self.close_paren
        return MagedownLink(open_bracket=open_bracket, text=text, close_bracket=close_bracket, open_paren=open_paren, href=href, close_paren=close_paren)

    def parent(self) -> 'MagedownLinkParent':
        assert(self._parent is not None)
        return self._parent


class MagedownNameDeriveKwargs(TypedDict, total=False):

    field: 'str'

    field_1: 'str'


class MagedownName(_MagedownBaseNode):

    def __init__(self, field: 'str', field_1: 'str') -> None:
        self.field: str = _coerce_extern_string_to_extern_string(field)
        self.field_1: str = _coerce_extern_string_to_extern_string(field_1)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownNameDeriveKwargs]) -> 'MagedownName':
        field = _coerce_extern_string_to_extern_string(kwargs['field']) if 'field' in kwargs else self.field
        field_1 = _coerce_extern_string_to_extern_string(kwargs['field_1']) if 'field_1' in kwargs else self.field_1
        return MagedownName(field=field, field_1=field_1)

    def parent(self) -> 'MagedownNameParent':
        assert(self._parent is not None)
        return self._parent


class MagedownRefDeriveKwargs(TypedDict, total=False):

    open_bracket_open_bracket: 'MagedownOpenBracketOpenBracket | None'

    name: 'MagedownName'

    close_bracket_close_bracket: 'MagedownCloseBracketCloseBracket | None'


class MagedownRef(_MagedownBaseNode):

    def __init__(self, name: 'MagedownName', *, open_bracket_open_bracket: 'MagedownOpenBracketOpenBracket | None' = None, close_bracket_close_bracket: 'MagedownCloseBracketCloseBracket | None' = None) -> None:
        self.open_bracket_open_bracket: MagedownOpenBracketOpenBracket = _coerce_union_2_decl_open_bracket_open_bracket_none_to_decl_open_bracket_open_bracket(open_bracket_open_bracket)
        self.name: MagedownName = _coerce_decl_name_to_decl_name(name)
        self.close_bracket_close_bracket: MagedownCloseBracketCloseBracket = _coerce_union_2_decl_close_bracket_close_bracket_none_to_decl_close_bracket_close_bracket(close_bracket_close_bracket)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownRefDeriveKwargs]) -> 'MagedownRef':
        open_bracket_open_bracket = _coerce_union_2_decl_open_bracket_open_bracket_none_to_decl_open_bracket_open_bracket(kwargs['open_bracket_open_bracket']) if 'open_bracket_open_bracket' in kwargs else self.open_bracket_open_bracket
        name = _coerce_decl_name_to_decl_name(kwargs['name']) if 'name' in kwargs else self.name
        close_bracket_close_bracket = _coerce_union_2_decl_close_bracket_close_bracket_none_to_decl_close_bracket_close_bracket(kwargs['close_bracket_close_bracket']) if 'close_bracket_close_bracket' in kwargs else self.close_bracket_close_bracket
        return MagedownRef(open_bracket_open_bracket=open_bracket_open_bracket, name=name, close_bracket_close_bracket=close_bracket_close_bracket)

    def parent(self) -> 'MagedownRefParent':
        assert(self._parent is not None)
        return self._parent


class MagedownRejectsDeriveKwargs(TypedDict, total=False):

    open_brace: 'MagedownOpenBrace | None'

    reject_keyword: 'MagedownRejectKeyword | None'

    close_brace: 'MagedownCloseBrace | None'

    text: 'str'

    open_brace_slash: 'MagedownOpenBraceSlash | None'

    reject_keyword_2: 'MagedownRejectKeyword | None'

    close_brace_2: 'MagedownCloseBrace | None'


class MagedownRejects(_MagedownBaseNode):

    def __init__(self, text: 'str', *, open_brace: 'MagedownOpenBrace | None' = None, reject_keyword: 'MagedownRejectKeyword | None' = None, close_brace: 'MagedownCloseBrace | None' = None, open_brace_slash: 'MagedownOpenBraceSlash | None' = None, reject_keyword_2: 'MagedownRejectKeyword | None' = None, close_brace_2: 'MagedownCloseBrace | None' = None) -> None:
        self.open_brace: MagedownOpenBrace = _coerce_union_2_decl_open_brace_none_to_decl_open_brace(open_brace)
        self.reject_keyword: MagedownRejectKeyword = _coerce_union_2_decl_reject_keyword_none_to_decl_reject_keyword(reject_keyword)
        self.close_brace: MagedownCloseBrace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(close_brace)
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.open_brace_slash: MagedownOpenBraceSlash = _coerce_union_2_decl_open_brace_slash_none_to_decl_open_brace_slash(open_brace_slash)
        self.reject_keyword_2: MagedownRejectKeyword = _coerce_union_2_decl_reject_keyword_none_to_decl_reject_keyword(reject_keyword_2)
        self.close_brace_2: MagedownCloseBrace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(close_brace_2)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownRejectsDeriveKwargs]) -> 'MagedownRejects':
        open_brace = _coerce_union_2_decl_open_brace_none_to_decl_open_brace(kwargs['open_brace']) if 'open_brace' in kwargs else self.open_brace
        reject_keyword = _coerce_union_2_decl_reject_keyword_none_to_decl_reject_keyword(kwargs['reject_keyword']) if 'reject_keyword' in kwargs else self.reject_keyword
        close_brace = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(kwargs['close_brace']) if 'close_brace' in kwargs else self.close_brace
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        open_brace_slash = _coerce_union_2_decl_open_brace_slash_none_to_decl_open_brace_slash(kwargs['open_brace_slash']) if 'open_brace_slash' in kwargs else self.open_brace_slash
        reject_keyword_2 = _coerce_union_2_decl_reject_keyword_none_to_decl_reject_keyword(kwargs['reject_keyword_2']) if 'reject_keyword_2' in kwargs else self.reject_keyword_2
        close_brace_2 = _coerce_union_2_decl_close_brace_none_to_decl_close_brace(kwargs['close_brace_2']) if 'close_brace_2' in kwargs else self.close_brace_2
        return MagedownRejects(open_brace=open_brace, reject_keyword=reject_keyword, close_brace=close_brace, text=text, open_brace_slash=open_brace_slash, reject_keyword_2=reject_keyword_2, close_brace_2=close_brace_2)

    def parent(self) -> 'MagedownRejectsParent':
        assert(self._parent is not None)
        return self._parent


class MagedownTextDeriveKwargs(TypedDict, total=False):

    contents: 'str'


class MagedownText(_MagedownBaseNode):

    def __init__(self, contents: 'str') -> None:
        self.contents: str = _coerce_extern_string_to_extern_string(contents)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownTextDeriveKwargs]) -> 'MagedownText':
        contents = _coerce_extern_string_to_extern_string(kwargs['contents']) if 'contents' in kwargs else self.contents
        return MagedownText(contents=contents)

    def parent(self) -> 'MagedownTextParent':
        assert(self._parent is not None)
        return self._parent


type MagedownNode = MagedownName | MagedownCodeBlock | MagedownInlineCode | MagedownHeading | MagedownRef | MagedownLink | MagedownAccepts | MagedownRejects | MagedownText | MagedownDocument


def is_magedown_node(value: Any) -> TypeIs[MagedownNode]:
    return isinstance(value, MagedownName) or isinstance(value, MagedownCodeBlock) or isinstance(value, MagedownInlineCode) or isinstance(value, MagedownHeading) or isinstance(value, MagedownRef) or isinstance(value, MagedownLink) or isinstance(value, MagedownAccepts) or isinstance(value, MagedownRejects) or isinstance(value, MagedownText) or isinstance(value, MagedownDocument)


type MagedownSpecial = MagedownCodeBlock | MagedownInlineCode | MagedownHeading | MagedownRef | MagedownLink | MagedownAccepts | MagedownRejects


def is_magedown_special(value: Any) -> TypeIs[MagedownSpecial]:
    return isinstance(value, MagedownCodeBlock) or isinstance(value, MagedownInlineCode) or isinstance(value, MagedownHeading) or isinstance(value, MagedownRef) or isinstance(value, MagedownLink) or isinstance(value, MagedownAccepts) or isinstance(value, MagedownRejects)


type MagedownSyntax = MagedownToken | MagedownNode


def is_magedown_syntax(value: Any) -> TypeIs[MagedownSyntax]:
    return is_magedown_token(value) or is_magedown_node(value)


type MagedownToken = MagedownAcceptKeyword | MagedownRejectKeyword


def is_magedown_token(value: Any) -> TypeIs[MagedownToken]:
    return isinstance(value, MagedownAcceptKeyword) or isinstance(value, MagedownRejectKeyword)


type MagedownAcceptsParent = MagedownDocument


type MagedownCodeBlockParent = MagedownDocument


type MagedownDocumentParent = Never


type MagedownHeadingParent = MagedownDocument


type MagedownInlineCodeParent = MagedownDocument


type MagedownLinkParent = MagedownDocument


type MagedownNameParent = MagedownCodeBlock | MagedownRef


type MagedownRefParent = MagedownDocument


type MagedownRejectsParent = MagedownDocument


type MagedownTextParent = MagedownDocument


@no_type_check
def _coerce_union_2_decl_open_brace_none_to_decl_open_brace(value: 'MagedownOpenBrace | None') -> 'MagedownOpenBrace':
    if value is None:
        return MagedownOpenBrace()
    elif isinstance(value, MagedownOpenBrace):
        return value
    else:
        raise ValueError('the coercion from MagedownOpenBrace | None to MagedownOpenBrace failed')


@no_type_check
def _coerce_union_2_decl_accept_keyword_none_to_decl_accept_keyword(value: 'MagedownAcceptKeyword | None') -> 'MagedownAcceptKeyword':
    if value is None:
        return MagedownAcceptKeyword()
    elif isinstance(value, MagedownAcceptKeyword):
        return value
    else:
        raise ValueError('the coercion from MagedownAcceptKeyword | None to MagedownAcceptKeyword failed')


@no_type_check
def _coerce_union_2_decl_close_brace_none_to_decl_close_brace(value: 'MagedownCloseBrace | None') -> 'MagedownCloseBrace':
    if value is None:
        return MagedownCloseBrace()
    elif isinstance(value, MagedownCloseBrace):
        return value
    else:
        raise ValueError('the coercion from MagedownCloseBrace | None to MagedownCloseBrace failed')


@no_type_check
def _coerce_extern_string_to_extern_string(value: 'str') -> 'str':
    return value


@no_type_check
def _coerce_union_2_decl_open_brace_slash_none_to_decl_open_brace_slash(value: 'MagedownOpenBraceSlash | None') -> 'MagedownOpenBraceSlash':
    if value is None:
        return MagedownOpenBraceSlash()
    elif isinstance(value, MagedownOpenBraceSlash):
        return value
    else:
        raise ValueError('the coercion from MagedownOpenBraceSlash | None to MagedownOpenBraceSlash failed')


@no_type_check
def _coerce_union_2_decl_backtick_backtick_backtick_none_to_decl_backtick_backtick_backtick(value: 'MagedownBacktickBacktickBacktick | None') -> 'MagedownBacktickBacktickBacktick':
    if value is None:
        return MagedownBacktickBacktickBacktick()
    elif isinstance(value, MagedownBacktickBacktickBacktick):
        return value
    else:
        raise ValueError('the coercion from MagedownBacktickBacktickBacktick | None to MagedownBacktickBacktickBacktick failed')


@no_type_check
def _coerce_union_2_decl_name_none_to_union_2_decl_name_none(value: 'MagedownName | None') -> 'MagedownName | None':
    if isinstance(value, MagedownName):
        return value
    elif value is None:
        return None
    else:
        raise ValueError('the coercion from MagedownName | None to MagedownName | None failed')


@no_type_check
def _coerce_union_3_decl_special_decl_text_extern_string_to_union_2_decl_special_decl_text(value: 'MagedownSpecial | MagedownText | str') -> 'MagedownSpecial | MagedownText':
    if is_magedown_special(value):
        return value
    elif isinstance(value, str):
        return MagedownText(_coerce_extern_string_to_extern_string(value))
    elif isinstance(value, MagedownText):
        return value
    else:
        raise ValueError('the coercion from MagedownSpecial | MagedownText | str to MagedownSpecial | MagedownText failed')


@no_type_check
def _coerce_union_2_list_union_3_decl_special_decl_text_extern_string_none_to_list_union_2_decl_special_decl_text(value: 'Sequence[MagedownSpecial | MagedownText | str] | None') -> 'list[MagedownSpecial | MagedownText]':
    if value is None:
        return list()
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_union_3_decl_special_decl_text_extern_string_to_union_2_decl_special_decl_text(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[MagedownSpecial | MagedownText | str] | None to list[MagedownSpecial | MagedownText] failed')


@no_type_check
def _coerce_decl_hashtag_to_decl_hashtag(value: 'MagedownHashtag') -> 'MagedownHashtag':
    return value


@no_type_check
def _coerce_union_2_list_decl_hashtag_required_extern_integer_to_list_decl_hashtag_required(value: 'Sequence[MagedownHashtag] | int') -> 'list[MagedownHashtag]':
    if isinstance(value, int):
        new_elements = list()
        for _ in range(0, value):
            new_elements.append(MagedownHashtag())
        return new_elements
    elif isinstance(value, list):
        new_elements = list()
        for value_element in value:
            new_elements.append(_coerce_decl_hashtag_to_decl_hashtag(value_element))
        return new_elements
    else:
        raise ValueError('the coercion from Sequence[MagedownHashtag] | int to list[MagedownHashtag] failed')


@no_type_check
def _coerce_union_2_decl_backtick_none_to_decl_backtick(value: 'MagedownBacktick | None') -> 'MagedownBacktick':
    if value is None:
        return MagedownBacktick()
    elif isinstance(value, MagedownBacktick):
        return value
    else:
        raise ValueError('the coercion from MagedownBacktick | None to MagedownBacktick failed')


@no_type_check
def _coerce_union_2_decl_open_bracket_none_to_decl_open_bracket(value: 'MagedownOpenBracket | None') -> 'MagedownOpenBracket':
    if value is None:
        return MagedownOpenBracket()
    elif isinstance(value, MagedownOpenBracket):
        return value
    else:
        raise ValueError('the coercion from MagedownOpenBracket | None to MagedownOpenBracket failed')


@no_type_check
def _coerce_union_2_decl_close_bracket_none_to_decl_close_bracket(value: 'MagedownCloseBracket | None') -> 'MagedownCloseBracket':
    if value is None:
        return MagedownCloseBracket()
    elif isinstance(value, MagedownCloseBracket):
        return value
    else:
        raise ValueError('the coercion from MagedownCloseBracket | None to MagedownCloseBracket failed')


@no_type_check
def _coerce_union_2_decl_open_paren_none_to_decl_open_paren(value: 'MagedownOpenParen | None') -> 'MagedownOpenParen':
    if value is None:
        return MagedownOpenParen()
    elif isinstance(value, MagedownOpenParen):
        return value
    else:
        raise ValueError('the coercion from MagedownOpenParen | None to MagedownOpenParen failed')


@no_type_check
def _coerce_union_2_decl_close_paren_none_to_decl_close_paren(value: 'MagedownCloseParen | None') -> 'MagedownCloseParen':
    if value is None:
        return MagedownCloseParen()
    elif isinstance(value, MagedownCloseParen):
        return value
    else:
        raise ValueError('the coercion from MagedownCloseParen | None to MagedownCloseParen failed')


@no_type_check
def _coerce_union_2_decl_open_bracket_open_bracket_none_to_decl_open_bracket_open_bracket(value: 'MagedownOpenBracketOpenBracket | None') -> 'MagedownOpenBracketOpenBracket':
    if value is None:
        return MagedownOpenBracketOpenBracket()
    elif isinstance(value, MagedownOpenBracketOpenBracket):
        return value
    else:
        raise ValueError('the coercion from MagedownOpenBracketOpenBracket | None to MagedownOpenBracketOpenBracket failed')


@no_type_check
def _coerce_decl_name_to_decl_name(value: 'MagedownName') -> 'MagedownName':
    return value


@no_type_check
def _coerce_union_2_decl_close_bracket_close_bracket_none_to_decl_close_bracket_close_bracket(value: 'MagedownCloseBracketCloseBracket | None') -> 'MagedownCloseBracketCloseBracket':
    if value is None:
        return MagedownCloseBracketCloseBracket()
    elif isinstance(value, MagedownCloseBracketCloseBracket):
        return value
    else:
        raise ValueError('the coercion from MagedownCloseBracketCloseBracket | None to MagedownCloseBracketCloseBracket failed')


@no_type_check
def _coerce_union_2_decl_reject_keyword_none_to_decl_reject_keyword(value: 'MagedownRejectKeyword | None') -> 'MagedownRejectKeyword':
    if value is None:
        return MagedownRejectKeyword()
    elif isinstance(value, MagedownRejectKeyword):
        return value
    else:
        raise ValueError('the coercion from MagedownRejectKeyword | None to MagedownRejectKeyword failed')


