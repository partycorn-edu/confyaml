"""Синтаксический разбор на основе библиотеки Lark (LALR)."""

from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedToken

from .errors import ConfigError
from .grammar import GRAMMAR

_PARSER = Lark(GRAMMAR, parser="lalr", propagate_positions=True)


def _token_message(err):
    """Сообщение об ошибке для неожиданной лексемы."""
    if err.token.type == "$END":
        return "неожиданный конец входных данных"
    return f"неожиданная лексема '{err.token}'"


def _char_message(err):
    """Сообщение об ошибке для недопустимого символа."""
    if err.char == "[":
        return "строка [[...]] не закрыта или записана неверно"
    return f"недопустимый символ '{err.char}'"


def parse(text):
    """Разобрать текст и вернуть дерево Lark.

    Синтаксические ошибки превращаются в ConfigError.
    """
    try:
        return _PARSER.parse(text)
    except UnexpectedToken as err:
        raise ConfigError(_token_message(err), err.line, err.column) from err
    except UnexpectedCharacters as err:
        raise ConfigError(_char_message(err), err.line, err.column) from err
