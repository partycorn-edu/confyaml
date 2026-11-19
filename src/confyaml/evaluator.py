"""Вычисление дерева разбора: значения и константы времени трансляции."""

import math

from .errors import ConfigError

BASE_BIN = 2
BASE_DEC = 10


def _is_number(value):
    """Проверить, что значение является числом."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _to_int(token):
    """Перевести лексему BIN или DEC в целое число."""
    text = str(token)
    if token.type == "BIN":
        return int(text[2:], BASE_BIN)
    return int(text, BASE_DEC)


def _add(left, right):
    return left + right


def _sub(left, right):
    return left - right


def _mul(left, right):
    return left * right


BINARY_OPS = {"+": _add, "-": _sub, "*": _mul}


class Evaluator:
    """Обходит дерево и строит Python-значения."""

    def __init__(self):
        self.constants = {}

    def run(self, tree):
        """Вернуть список значений верхнего уровня."""
        result = []
        for child in tree.children:
            if child.data == "declaration":
                self._declare(child)
            else:
                result.append(self.visit(child))
        return result

    def visit(self, node):
        """Вычислить узел значения."""
        return getattr(self, "_visit_" + node.data)(node)

    def _declare(self, node):
        name, value_node = node.children
        if str(name) in self.constants:
            raise ConfigError(
                f"константа '{name}' уже объявлена", name.line, name.column
            )
        self.constants[str(name)] = self.visit(value_node)

    def _visit_number(self, node):
        return _to_int(node.children[0])

    def _visit_string(self, node):
        return str(node.children[0])[2:-2]

    def _visit_array(self, node):
        return [self.visit(child) for child in node.children]

    def _visit_dict(self, node):
        result = {}
        for entry in node.children:
            key, value_node = entry.children
            if str(key) in result:
                raise ConfigError(
                    f"повторяющееся имя '{key}' в словаре",
                    key.line,
                    key.column,
                )
            result[str(key)] = self.visit(value_node)
        return result

    def _visit_expr(self, node):
        stack = []
        for token in node.children:
            self._apply(token, stack)
        if not stack:
            raise ConfigError("пустое выражение", node.meta.line)
        if len(stack) > 1:
            raise ConfigError(
                "в выражении остались лишние операнды", node.meta.line
            )
        return stack[0]

    def _apply(self, token, stack):
        """Применить одну лексему выражения к стеку."""
        if token.type in ("BIN", "DEC"):
            stack.append(_to_int(token))
        elif token.type == "NAME":
            stack.append(self._lookup(token))
        elif token.type == "SQRT":
            self._apply_sqrt(token, stack)
        else:
            self._apply_binary(token, stack)

    def _lookup(self, token):
        if str(token) not in self.constants:
            raise ConfigError(
                f"константа '{token}' не объявлена", token.line, token.column
            )
        return self.constants[str(token)]

    def _pop_numbers(self, token, stack, count):
        """Снять со стека count чисел для операции token."""
        if len(stack) < count:
            raise ConfigError(
                f"для '{token}' не хватает операндов", token.line, token.column
            )
        args = [stack.pop() for _ in range(count)][::-1]
        for arg in args:
            if not _is_number(arg):
                raise ConfigError(
                    f"операция '{token}' применима только к числам",
                    token.line,
                    token.column,
                )
        return args

    def _apply_binary(self, token, stack):
        left, right = self._pop_numbers(token, stack, 2)
        stack.append(BINARY_OPS[str(token)](left, right))

    def _apply_sqrt(self, token, stack):
        (value,) = self._pop_numbers(token, stack, 1)
        if value < 0:
            raise ConfigError(
                "sqrt от отрицательного числа", token.line, token.column
            )
        stack.append(math.sqrt(value))
