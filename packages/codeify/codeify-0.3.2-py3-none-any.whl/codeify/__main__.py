from .codegen import run_generation, generate_output, replace_text
from .text import insert_text
from .types import CodeGeneration
from argparse import ArgumentParser
from typing import Callable
import sys
import traceback

def _parse_args() -> Callable[[], None]:
    parser = ArgumentParser(description='Codeify (code generator)') 
    subparsers = parser.add_subparsers(dest='command')

    _parse_insert_args(subparsers.add_parser('insert'))
    _parse_generate_args(subparsers.add_parser('generate'))
    _parse_echo_args(subparsers.add_parser('echo'))
    _parse_replace_args(subparsers.add_parser('replace'))
    # TODO: 'remove' and 'replace' and 'echo'

    args = parser.parse_args()
    if args.command == "generate":
        return lambda: run_generation(CodeGeneration(args.input, args.output, args.spec, args.module))
    elif args.command == "insert":
        return lambda: insert_text(args.input, args.text, args.before, args.after)
    elif args.command == "echo":
        return lambda: generate_output(args.template, args.define, args.spec, sys.stdout, args.module)
    elif args.command == "replace":
        return lambda: replace_text(args.input, args.output, args.spec, args.define, args.ignore)
    else:
        parser.print_help()
        sys.exit(1)

def _parse_insert_args(parser: ArgumentParser) -> None:
    parser.add_argument('-i', '--input', help='input file', metavar='<file>', required=True)
    parser.add_argument('-B', '--before', help='text line before boundary', metavar='<str>')
    parser.add_argument('-A', '--after', help='text line after boundary', metavar='<str>')
    parser.add_argument('text', help='text to insert')

def _parse_generate_args(parser: ArgumentParser) -> None:
    parser.add_argument('-i', '--input', help='input directory', metavar='<dir>', required=True)
    parser.add_argument('-o', '--output', help='output directory', metavar='<dir>', required=True)
    parser.add_argument('-s', '--spec', help='specification file (yaml)', metavar='<spec.yaml>', required=True)
    parser.add_argument('-m', '--module', help='import a Python file as a module', metavar='<file.py>', action='append', default=[])

def _parse_echo_args(parser: ArgumentParser) -> None:
    parser.add_argument('template', help='Jinja template file')
    parser.add_argument('-s', '--spec', help='specification file (yaml)', metavar='<spec.yaml>')
    parser.add_argument('-d', '--define', help='define a field (field=[a,b,c]) or (field=fizz)', metavar='<expr>', action='append', default=[])
    parser.add_argument('-m', '--module', help='import a Python file as a module', metavar='<file.py>', action='append', default=[])

def _parse_replace_args(parser: ArgumentParser) -> None:
    parser.add_argument('-i', '--input', help='input directory', metavar='<dir>', required=True)
    parser.add_argument('-o', '--output', help='output directory', metavar='<dir>', required=True)
    parser.add_argument('-s', '--spec', help='specification file of key-value replacements (yaml)', metavar='<spec.yaml>')
    parser.add_argument('-d', '--define', help='define a replacement field (e.g. "red=green")', metavar='<expr>', action='append', default=[])
    parser.add_argument('--ignore', help='ignore a file pattern (e.g. "*.bin")', metavar='<glob>', action='append', default=[])

def main() -> int:
    try:
        _parse_args()()
        return 0
    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1
