"""Полный цикл трансляции: текст конфигурации в текст YAML."""

import yaml

from .evaluator import Evaluator
from .parser import parse


def to_yaml(values):
    """Сериализовать значения верхнего уровня в YAML.

    Одно значение выводится как есть, несколько как список.
    Пустой вход даёт пустой вывод.
    """
    if not values:
        return ""
    data = values[0] if len(values) == 1 else values
    return yaml.safe_dump(
        data, allow_unicode=True, sort_keys=False, default_flow_style=False
    )


def translate(text):
    """Перевести текст на учебном языке в YAML."""
    tree = parse(text)
    return to_yaml(Evaluator().run(tree))
