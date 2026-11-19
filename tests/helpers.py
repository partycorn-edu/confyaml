"""Общие вспомогательные функции тестов."""

from confyaml.evaluator import Evaluator
from confyaml.parser import parse


def values(text):
    """Вернуть значения верхнего уровня для текста конфигурации."""
    return Evaluator().run(parse(text))


def one(text):
    """Вернуть единственное значение верхнего уровня."""
    result = values(text)
    assert len(result) == 1
    return result[0]
