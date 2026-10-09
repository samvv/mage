
from pathlib import Path

ANONYMOUS_FIELD_NAME = 'field'
"""
The name to use for a Mage expression of which no label can be derived.
"""

SEED_FILENAME_PREFIX = 'seed:'

DEFAULT_FUZZ_DIR = Path("output/fuzz")

DEFAULT_MAX_REPEATS = 1000

DEFAULT_MAX_NAMED_CHARS = 4
"""
How much chars before a literal is named as-is.

The value is configurable when running the program but will default to whatever was set here.
"""
