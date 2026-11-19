"""Тесты командной строки и примеров."""

import io
import unittest
from pathlib import Path

from confyaml.cli import EXIT_ERROR, EXIT_OK, main
from confyaml.translator import translate

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def run_cli(text):
    """Запустить CLI на тексте, вернуть код, stdout и stderr."""
    out, err = io.StringIO(), io.StringIO()
    code = main([], io.StringIO(text), out, err)
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    """Поведение CLI."""

    def test_success(self):
        code, out, err = run_cli("table(a => 0b1)")
        self.assertEqual((code, out, err), (EXIT_OK, "a: 1\n", ""))

    def test_error_goes_to_stderr(self):
        code, out, err = run_cli("x is")
        self.assertEqual(code, EXIT_ERROR)
        self.assertEqual(out, "")
        self.assertTrue(err.startswith("Ошибка: строка 1"))

    def test_empty_input(self):
        self.assertEqual(run_cli("")[:2], (EXIT_OK, ""))

    def test_several_values_become_list(self):
        self.assertEqual(translate("0b1 0b10"), "- 1\n- 2\n")

    def test_unicode_is_kept(self):
        self.assertEqual(translate("[[привет]]"), "привет\n...\n")

    def test_special_string_is_quoted(self):
        self.assertEqual(translate("table(a => [[true]])"), "a: 'true'\n")

    def test_nested_yaml(self):
        text = "table(a => << table(b => 0b1) >>)"
        self.assertEqual(translate(text), "a:\n- b: 1\n")


class ExampleTests(unittest.TestCase):
    """Примеры конфигураций из каталога examples."""

    def check(self, name):
        source = (EXAMPLES / f"{name}.conf").read_text(encoding="utf-8")
        expected = (EXAMPLES / f"{name}.yaml").read_text(encoding="utf-8")
        self.assertEqual(translate(source), expected)

    def test_webservice(self):
        self.check("webservice")

    def test_triangle(self):
        self.check("triangle")
