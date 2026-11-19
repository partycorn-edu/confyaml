"""Грамматика учебного конфигурационного языка (формат Lark)."""

GRAMMAR = r"""
start: (declaration | value)*

declaration: NAME "is" value

?value: number | string | array | dict | expr

number: BIN
string: STRING
array: "<<" (value ("," value)* ","?)? ">>"
dict: "table" "(" (entry ("," entry)* ","?)? ")"
entry: NAME "=>" value
expr: "^{" (BIN | DEC | NAME | OP | SQRT)* "}"

BIN.2: /0[bB][01]+/
DEC: /[0-9]+/
STRING: /\[\[.*?\]\]/s
NAME: /[a-zA-Z][a-zA-Z0-9]*/
SQRT: "sqrt"
OP: /[+\-*]/

COMMENT: /#[^\n]*/
%import common.WS
%ignore WS
%ignore COMMENT
"""
