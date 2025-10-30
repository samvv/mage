
from collections.abc import Sequence
from dataclasses import dataclass


type Doc = ConsDoc | EmptyDoc | TextDoc


@dataclass
class DocBase:
    pass


@dataclass
class ConsDoc(DocBase):
    head: Doc
    tail: Doc


@dataclass
class EmptyDoc(DocBase):
    pass


@dataclass
class TextDoc(DocBase):
    text: str


def empty() -> Doc:
    return EmptyDoc()


def seq(elements: Sequence[Doc]) -> Doc:
    out = EmptyDoc()
    for element in reversed(elements):
        out = ConsDoc(element, out)
    return out


def text(contents: str) -> TextDoc:
    return TextDoc(contents)


def generate(doc: Doc) -> str:
    if isinstance(doc, EmptyDoc):
        return ''
    if isinstance(doc, ConsDoc):
        return generate(doc.head) + generate(doc.tail)
    if isinstance(doc, TextDoc):
        return doc.text
    assert_never(doc)

