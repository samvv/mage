
from magelang.lang.python import PyModule, emit
from magelang.manager import declare_pass

@declare_pass()
def python_to_text(module: PyModule) -> str:
    return emit(module)

