"""Исключения транслятора."""


class ConfigError(Exception):
    """Ошибка во входном тексте с позицией (если она известна)."""

    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        if self.line is None:
            return self.message
        place = f"строка {self.line}"
        if self.column is not None:
            place += f", столбец {self.column}"
        return f"{place}: {self.message}"
