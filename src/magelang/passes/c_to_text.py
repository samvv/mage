from magelang import declare_pass
from magelang.lang import c

@declare_pass()
def c_to_text(tu: c.TranslationUnit) -> str:
    emitter = c.C99Emitter()
    return emitter.emit(tu)
