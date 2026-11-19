"""Интерфейс командной строки: stdin -> stdout."""

import argparse
import sys

from .errors import ConfigError
from .translator import translate

EXIT_OK = 0
EXIT_ERROR = 1


def build_arg_parser():
    """Создать разборщик аргументов командной строки."""
    return argparse.ArgumentParser(
        prog="confyaml",
        description=(
            "Читает конфигурацию на учебном языке из stdin "
            "и пишет YAML в stdout."
        ),
    )


def main(argv=None, stdin=None, stdout=None, stderr=None):
    """Точка входа. Возвращает код завершения процесса."""
    build_arg_parser().parse_args(argv)
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    try:
        stdout.write(translate(stdin.read()))
    except ConfigError as err:
        stderr.write(f"Ошибка: {err}\n")
        return EXIT_ERROR
    return EXIT_OK
