
import sys

def debug(message: str) -> None:
    sys.stderr.write(f'{message}\n')

def info(message: str) -> None:
    sys.stderr.write(f'Info: {message}\n')

def warn(message: str) -> None:
    sys.stderr.write(f'Warning: {message}\n')

def error(message: str) -> None:
    sys.stderr.write(f'Error: {message}\n')

def fatal(message: str) -> None:
    sys.stderr.write(f'Fatal: {message}\n')

