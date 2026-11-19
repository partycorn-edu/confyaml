"""Тесты констант и постфиксных выражений ^{...}."""

import unittest

from tests.helpers import one, values


class DeclarationTests(unittest.TestCase):
    """Объявления «имя is значение»."""

    def test_declaration_gives_no_output(self):
        self.assertEqual(values("x is 0b1"), [])

    def test_constant_of_each_kind(self):
        text = (
            "n is 0b11 s is [[a]] a is << 0b1 >> d is table(k => 0b1)\n"
            "<< ^{n}, ^{s}, ^{a}, ^{d} >>"
        )
        self.assertEqual(one(text), [3, "a", [1], {"k": 1}])

    def test_constant_from_expression(self):
        self.assertEqual(one("x is 0b10 y is ^{x x *} ^{y}"), 4)

    def test_constant_in_nested_structure(self):
        text = "x is 0b1 table(a => << table(b => ^{x}) >>)"
        self.assertEqual(one(text), {"a": [{"b": 1}]})


class ExpressionTests(unittest.TestCase):
    """Операции +, -, * и sqrt."""

    def test_add(self):
        self.assertEqual(one("^{0b1 0b10 +}"), 3)

    def test_sub(self):
        self.assertEqual(one("^{0b101 0b10 -}"), 3)

    def test_mul(self):
        self.assertEqual(one("^{0b11 0b100 *}"), 12)

    def test_sqrt(self):
        self.assertEqual(one("^{0b10000 sqrt}"), 4.0)

    def test_sqrt_inexact(self):
        self.assertAlmostEqual(one("^{0b10 sqrt}"), 2 ** 0.5)

    def test_decimal_literal(self):
        self.assertEqual(one("x is 0b1 ^{x 10 +}"), 11)

    def test_sub_order(self):
        self.assertEqual(one("^{0b1 0b11 -}"), -2)

    def test_long_expression(self):
        self.assertEqual(one("^{0b1 0b10 + 0b11 * 0b1 -}"), 8)

    def test_name_only(self):
        self.assertEqual(one("x is [[hi]] ^{x}"), "hi")

    def test_sqrt_of_constant_expression(self):
        text = "a is 0b11 b is 0b100 ^{a a * b b * + sqrt}"
        self.assertEqual(one(text), 5.0)
