
from magelang.lang.rust import rust_emit, RustSourceFile

def rust_to_text(source: RustSourceFile) -> str:
    return rust_emit(source)
