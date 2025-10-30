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


class MagedownAcceptsDeriveKwargs(TypedDict, total=False):

    text: 'str'


class MagedownAccepts(_MagedownBaseNode):

    def __init__(self, text: 'str') -> None:
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownAcceptsDeriveKwargs]) -> 'MagedownAccepts':
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownAccepts(text=text)

    @property
    def parent(self) -> 'MagedownAcceptsParent':
        assert(self._parent is not None)
        return self._parent


class MagedownCodeBlockDeriveKwargs(TypedDict, total=False):

    lang: 'MagedownName | None'

    text: 'str'


class MagedownCodeBlock(_MagedownBaseNode):

    def __init__(self, text: 'str', *, lang: 'MagedownName | None' = None) -> None:
        self.lang: MagedownName | None = _coerce_union_2_decl_name_none_to_union_2_decl_name_none(lang)
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownCodeBlockDeriveKwargs]) -> 'MagedownCodeBlock':
        lang = _coerce_union_2_decl_name_none_to_union_2_decl_name_none(kwargs['lang']) if 'lang' in kwargs else self.lang
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownCodeBlock(lang=lang, text=text)

    @property
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

    @property
    def parent(self) -> 'MagedownDocumentParent':
        raise AssertionError('trying to access the parent node of a top-level node')


class MagedownHeadingDeriveKwargs(TypedDict, total=False):

    hashtags: 'int'

    text: 'str'


class MagedownHeading(_MagedownBaseNode):

    def __init__(self, hashtags: 'int', text: 'str') -> None:
        self.hashtags: int = _coerce_extern_integer_to_extern_integer(hashtags)
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownHeadingDeriveKwargs]) -> 'MagedownHeading':
        hashtags = _coerce_extern_integer_to_extern_integer(kwargs['hashtags']) if 'hashtags' in kwargs else self.hashtags
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownHeading(hashtags=hashtags, text=text)

    @property
    def parent(self) -> 'MagedownHeadingParent':
        assert(self._parent is not None)
        return self._parent


class MagedownInlineCodeDeriveKwargs(TypedDict, total=False):

    text: 'str'


class MagedownInlineCode(_MagedownBaseNode):

    def __init__(self, text: 'str') -> None:
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownInlineCodeDeriveKwargs]) -> 'MagedownInlineCode':
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownInlineCode(text=text)

    @property
    def parent(self) -> 'MagedownInlineCodeParent':
        assert(self._parent is not None)
        return self._parent


class MagedownLinkDeriveKwargs(TypedDict, total=False):

    text: 'str'

    href: 'str'


class MagedownLink(_MagedownBaseNode):

    def __init__(self, text: 'str', href: 'str') -> None:
        self.text: str = _coerce_extern_string_to_extern_string(text)
        self.href: str = _coerce_extern_string_to_extern_string(href)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownLinkDeriveKwargs]) -> 'MagedownLink':
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        href = _coerce_extern_string_to_extern_string(kwargs['href']) if 'href' in kwargs else self.href
        return MagedownLink(text=text, href=href)

    @property
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

    @property
    def parent(self) -> 'MagedownNameParent':
        assert(self._parent is not None)
        return self._parent


class MagedownRefDeriveKwargs(TypedDict, total=False):

    name: 'MagedownName'


class MagedownRef(_MagedownBaseNode):

    def __init__(self, name: 'MagedownName') -> None:
        self.name: MagedownName = _coerce_decl_name_to_decl_name(name)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownRefDeriveKwargs]) -> 'MagedownRef':
        name = _coerce_decl_name_to_decl_name(kwargs['name']) if 'name' in kwargs else self.name
        return MagedownRef(name=name)

    @property
    def parent(self) -> 'MagedownRefParent':
        assert(self._parent is not None)
        return self._parent


class MagedownRejectsDeriveKwargs(TypedDict, total=False):

    text: 'str'


class MagedownRejects(_MagedownBaseNode):

    def __init__(self, text: 'str') -> None:
        self.text: str = _coerce_extern_string_to_extern_string(text)

    @no_type_check
    def derive(self, **kwargs: Unpack[MagedownRejectsDeriveKwargs]) -> 'MagedownRejects':
        text = _coerce_extern_string_to_extern_string(kwargs['text']) if 'text' in kwargs else self.text
        return MagedownRejects(text=text)

    @property
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

    @property
    def parent(self) -> 'MagedownTextParent':
        assert(self._parent is not None)
        return self._parent


type MagedownNode = MagedownName | MagedownCodeBlock | MagedownInlineCode | MagedownHeading | MagedownRef | MagedownLink | MagedownAccepts | MagedownRejects | MagedownText | MagedownDocument


def is_magedown_node(value: Any) -> TypeIs[MagedownNode]:
    return isinstance(value, MagedownName) or isinstance(value, MagedownCodeBlock) or isinstance(value, MagedownInlineCode) or isinstance(value, MagedownHeading) or isinstance(value, MagedownRef) or isinstance(value, MagedownLink) or isinstance(value, MagedownAccepts) or isinstance(value, MagedownRejects) or isinstance(value, MagedownText) or isinstance(value, MagedownDocument)


type MagedownSpecial = MagedownCodeBlock | MagedownInlineCode | MagedownHeading | MagedownRef | MagedownLink | MagedownAccepts | MagedownRejects


def is_magedown_special(value: Any) -> TypeIs[MagedownSpecial]:
    return isinstance(value, MagedownCodeBlock) or isinstance(value, MagedownInlineCode) or isinstance(value, MagedownHeading) or isinstance(value, MagedownRef) or isinstance(value, MagedownLink) or isinstance(value, MagedownAccepts) or isinstance(value, MagedownRejects)


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
def _coerce_extern_string_to_extern_string(value: 'str') -> 'str':
    return value


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
def _coerce_extern_integer_to_extern_integer(value: 'int') -> 'int':
    return value


@no_type_check
def _coerce_decl_name_to_decl_name(value: 'MagedownName') -> 'MagedownName':
    return value


