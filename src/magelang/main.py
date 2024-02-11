
import argparse

from sweetener import visualize

from .scanner import Scanner
from .parser import Parser
from .prefix import transform as transform_prefix
from .reduce import transform as transform_reduce
from .codegen.cxx import generate as generate_cxx

def main():

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('file', nargs=1, help='A path to a grammar file')
 
    args = arg_parser.parse_args()

    with open(args.file[0], 'r') as f:
        text = f.read()
    scanner = Scanner(text)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    grammar = transform_prefix(grammar)
    grammar = transform_reduce(grammar)
    #visualize(grammar)
    files = generate_cxx(grammar)
    for path, node in files.items():
        print(path)
        node.print()

