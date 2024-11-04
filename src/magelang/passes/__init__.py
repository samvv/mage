
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
from .ir_to_rust import *
from .ir_to_python import *
from .simplify import *

mage_passes = {
    'check_neg_charset_intervals': check_neg_charset_intervals,
    'check_overlapping_charset_intervals': check_overlapping_charset_intervals,
    'check_token_no_parse': check_token_no_parse,
    'check_undefined': check_undefined,
    'extract_literals': extract_literals,
    'extract_prefixes': extract_prefixes,
    'inline': inline,
    'insert_magic_rules': insert_magic_rules,
    'insert_skip': insert_skip,
    'remove_hidden': remove_hidden,
    'simplify': simplify,
}

ir_passes = {
    ir_to_rust,
    ir_to_python,
}

