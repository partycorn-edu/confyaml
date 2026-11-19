"""Тесты чисел, строк, массивов, словарей и комментариев."""

import unittest

from tests.helpers import one, values


class NumberTests(unittest.TestCase):
    """Числа 0[bB][01]+."""

    def test_binary_lower(self):
        self.assertEqual(one("0b101"), 5)

    def test_binary_upper(self):
        self.assertEqual(one("0B11"), 3)

    def test_leading_zeros(self):
        self.assertEqual(one("0b0001"), 1)


class StringTests(unittest.TestCase):
    """Строки [[...]]."""

    def test_simple(self):
        self.assertEqual(one("[[Это строка]]"), "Это строка")

    def test_empty(self):
        self.assertEqual(one("[[]]"), "")

    def test_hash_inside_is_not_comment(self):
        self.assertEqual(one("[[a # b]]"), "a # b")

    def test_multiline(self):
        self.assertEqual(one("[[a\nb]]"), "a\nb")

    def test_brackets_and_keywords_inside(self):
        self.assertEqual(one("[[ << table( is ]]"), " << table( is ")


class ArrayTests(unittest.TestCase):
    """Массивы << ... >>."""

    def test_empty(self):
        self.assertEqual(one("<< >>"), [])

    def test_mixed(self):
        self.assertEqual(one("<< 0b1, [[x]] >>"), [1, "x"])

    def test_trailing_comma(self):
        self.assertEqual(one("<<0b1, 0b10,>>"), [1, 2])

    def test_nested(self):
        self.assertEqual(one("<< <<0b1>>, << >> >>"), [[1], []])

    def test_array_of_tables(self):
        text = "<< table(a => 0b1), table() >>"
        self.assertEqual(one(text), [{"a": 1}, {}])


class DictTests(unittest.TestCase):
    """Словари table(...)."""

    def test_empty(self):
        self.assertEqual(one("table()"), {})

    def test_simple(self):
        self.assertEqual(one("table(a => 0b1, b => [[x]])"), {"a": 1, "b": "x"})

    def test_trailing_comma(self):
        self.assertEqual(one("table(a => 0b1,)"), {"a": 1})

    def test_nested(self):
        text = "table(a => table(b => << 0b1 >>))"
        self.assertEqual(one(text), {"a": {"b": [1]}})

    def test_keys_keep_order(self):
        self.assertEqual(list(one("table(z => 0b1, a => 0b1)")), ["z", "a"])

    def test_names_with_digits_and_keyword_prefixes(self):
        text = "table(isx => 0b1, tablet => 0b1, sqrt2 => 0b1, A1 => 0b1)"
        self.assertEqual(len(one(text)), 4)


class CommentTests(unittest.TestCase):
    """Однострочные комментарии."""

    def test_only_comment(self):
        self.assertEqual(values("# просто комментарий"), [])

    def test_comment_between_items(self):
        text = "table(# к словарю\n a => 0b1, # после\n b => 0b10\n)"
        self.assertEqual(one(text), {"a": 1, "b": 2})

    def test_comment_inside_expression(self):
        self.assertEqual(one("^{0b1 # один\n 0b1 +}"), 2)


class TopLevelTests(unittest.TestCase):
    """Значения верхнего уровня."""

    def test_empty_text(self):
        self.assertEqual(values(""), [])

    def test_several_values(self):
        self.assertEqual(values("0b1 [[a]] << >>"), [1, "a", []])
