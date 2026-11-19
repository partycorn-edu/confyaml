"""Тесты сообщений об ошибках."""

import unittest

from confyaml.errors import ConfigError
from tests.helpers import values


class ErrorTests(unittest.TestCase):
    """Каждый случай должен давать ConfigError."""

    def fails(self, text, part):
        """Проверить ошибку и фрагмент её сообщения."""
        with self.assertRaises(ConfigError) as ctx:
            values(text)
        self.assertIn(part, str(ctx.exception))
        return ctx.exception

    def test_unexpected_end(self):
        self.fails("x is", "конец входных данных")

    def test_unclosed_string(self):
        self.fails("[[abc", "не закрыта")

    def test_unknown_symbol(self):
        self.fails("^{0b1 ?}", "недопустимый символ")

    def test_decimal_outside_expression(self):
        self.fails("x is 5", "неожиданная лексема")

    def test_bad_binary(self):
        self.fails("0b2", "")

    def test_missing_comma(self):
        self.fails("table(a => 0b1 b => 0b1)", "неожиданная лексема")

    def test_missing_arrow(self):
        self.fails("table(a 0b1)", "неожиданная лексема")

    def test_unclosed_array(self):
        self.fails("<< 0b1", "конец входных данных")

    def test_keyword_as_name(self):
        self.fails("is is 0b1", "неожиданная лексема")

    def test_position_is_reported(self):
        err = self.fails("x is 0b1\ny is", "строка 2")
        self.assertEqual(err.line, 2)

    def test_undefined_constant(self):
        self.fails("^{x}", "не объявлена")

    def test_use_before_declaration(self):
        self.fails("^{x} x is 0b1", "не объявлена")

    def test_redeclaration(self):
        self.fails("x is 0b1 x is 0b10", "уже объявлена")

    def test_duplicate_key(self):
        self.fails("table(a => 0b1, a => 0b10)", "повторяющееся имя")

    def test_empty_expression(self):
        self.fails("^{}", "пустое выражение")

    def test_extra_operands(self):
        self.fails("^{0b1 0b1}", "лишние операнды")

    def test_not_enough_operands(self):
        self.fails("^{0b1 +}", "не хватает операндов")

    def test_sqrt_without_operand(self):
        self.fails("^{sqrt}", "не хватает операндов")

    def test_sqrt_negative(self):
        self.fails("^{0b0 0b1 - sqrt}", "отрицательного")

    def test_operation_on_string(self):
        self.fails("s is [[a]] ^{s 0b1 +}", "только к числам")

    def test_sqrt_of_array(self):
        self.fails("a is << >> ^{a sqrt}", "только к числам")

    def test_table_as_constant_name(self):
        self.fails("table is 0b1", "неожиданная лексема")

    def test_sqrt_as_constant_name(self):
        self.fails("sqrt is 0b1", "неожиданная лексема")

    def test_is_as_dict_key(self):
        self.fails("table(is => 0b1)", "неожиданная лексема")
