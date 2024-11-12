
from magelang.manager import Pass

from .mage_check_neg_charset_intervals import *
from .mage_check_overlapping_charset_intervals import *
from .mage_check_token_no_parse import *
from .mage_check_undefined import *
from .mage_extract_literals import *
from .mage_extract_prefixes import *
from .mage_inline import *
from .mage_insert_magic_rules import *
from .mage_insert_skip import *
from .mage_remove_hidden import *
from .mage_simplify import *
from .mage_to_python_emitter import *
from .mage_to_revolv_syntax_tree import *
from .mage_to_treespec import *
from .python_to_text import *
from .revolv_lift_assign_expr import *
from .revolv_to_python import *
from .revolv_to_rust import *
from .rust_to_text import *
from .treespec_cst_to_ast import *
from .treespec_to_python import *

all_passes = {
    mage_extract_literals,
    mage_extract_prefixes,
    mage_check_neg_charset_intervals,
    mage_check_overlapping_charset_intervals,
    mage_check_token_no_parse,
    mage_check_undefined,
    mage_inline,
    mage_insert_magic_rules,
    mage_insert_skip,
    mage_remove_hidden,
    mage_simplify,
    mage_to_python_emitter,
    mage_to_revolv_syntax_tree,
    mage_to_treespec,
    python_to_text,
    revolv_lift_assign_expr,
    revolv_to_python,
    revolv_to_rust,
    rust_to_text,
    treespec_cst_to_ast,
    treespec_to_python,
}

def get_pass_by_name(name: str) -> Pass[Any, Any]:
    for pass_ in all_passes:
        if pass_.__name__ == name:
            return pass_
    raise RuntimeError(f"A pass named '{name}' was not found")
