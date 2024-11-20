
from magelang.lang.python import PyModule, emit

def python_to_text(module: PyModule) -> str:
    return emit(module)

