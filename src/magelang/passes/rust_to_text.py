
from magelang.lang.rust import rust_emit, RustSourceFile
from magelang.manager import declare_pass

@declare_pass()
def rust_to_text(source: RustSourceFile) -> str:
    return rust_emit(source)
