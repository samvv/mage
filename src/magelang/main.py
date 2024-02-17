
import argparse
import importlib
from pathlib import Path

from sweetener import visualize, warn

from .scanner import Scanner
from .parser import Parser
from .repr import grammar_to_nodespec
from .prefix import transform as transform_prefix
from .reduce import transform as transform_reduce

here = Path(__file__).parent

generators = dict()
for path in (here / 'codegen').iterdir():
    generators[path.stem] = importlib.import_module(f'magelang.codegen.{path.stem}')

def main():

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    arg_parser.add_argument('--lang', required=True, choices=generators.keys(), help='What target language to generate code for')
 
    args = arg_parser.parse_args()

    with open(args.file[0], 'r') as f:
        text = f.read()
    scanner = Scanner(text)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    #grammar = transform_prefix(grammar)
    #grammar = transform_reduce(grammar)
    #visualize(grammar)
    generator = generators[args.lang]
    files = generator.generate_cst(grammar)

    for path, node in files.items():
        print(path)
        print(node)
        #node.print()

