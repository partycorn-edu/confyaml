"""Запуск: python -m confyaml < input.conf > output.yaml"""

import sys

from .cli import main


def _use_utf8():
    """Включить UTF-8 для стандартных потоков."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    _use_utf8()
    sys.exit(main())
