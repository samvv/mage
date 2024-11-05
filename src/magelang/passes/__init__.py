
from magelang.manager import Pass
from .check_neg_charset_intervals import *
from .check_overlapping_charset_intervals import *
from .check_token_no_parse import *
from .check_undefined import *
from .extract_literals import *
from .extract_prefixes import *
from .remove_hidden import *
from .inline import *
from .insert_magic_rules import *
from .insert_skip import *
from .axis_to_rust import *
from .axis_to_python import *
from .rust_to_text import *
from .mage_to_python_cst import *
from .mage_to_python_emitter import *
from .mage_to_axis_syntax_tree import *
from .python_to_text import *
from .simplify import *

all_passes = {
    check_neg_charset_intervals,
    check_overlapping_charset_intervals,
    check_token_no_parse,
    check_undefined,
    extract_literals,
    extract_prefixes,
    inline,
    insert_magic_rules,
    insert_skip,
    remove_hidden,
    simplify,
    mage_to_python_cst,
    mage_to_python_emitter,
    mage_to_axis_syntax_tree,
    axis_to_rust,
    axis_to_python,
}

def get_pass_by_name(name: str) -> Pass | None:
    for pass_ in all_passes:
        if pass_.__name__ == name:
            return pass_
