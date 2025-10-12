"""Coleção de constantes e alfabetos para a linguagem SimplePoo.

Nenhuma expressão regular é utilizada; todas as informações são descritas por
listas e dicionários explícitos para facilitar o estudo dos autômatos.
"""

# Conjunto de caracteres ASCII imprimíveis, além de espaço, tabulações e quebras de linha.
CARACTERES_PERMITIDOS = [chr(c) for c in range(32, 127)] + ["\t", "\n", "\r"]

KEYWORDS = [
    "class",
    "struct",
    "interface",
    "extends",
    "implements",
    "new",
    "this",
    "super",
    "function",
    "void",
    "var",
    "let",
    "const",
    "return",
    "if",
    "else",
    "switch",
    "case",
    "default",
    "break",
    "continue",
    "for",
    "foreach",
    "while",
    "do",
    "true",
    "false",
    "null",
    "public",
    "private",
    "protected",
    "static",
    "int",
    "float",
    "string",
    "bool",
    "list",
    "dict",
]

OPERATORS = {
    "combinados": [
        "==",
        "!=",
        "<=",
        ">=",
        "&&",
        "||",
        "++",
        "--",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "<<=",
        ">>=",
        "&=",
        "|=",
        "^=",
        "=>",
        "->",
        "::",
    ],
    "simples": [
        "+",
        "-",
        "*",
        "/",
        "%",
        "=",
        "<",
        ">",
        "!",
        "&",
        "|",
        "^",
        "~",
        "?",
        ":",
    ],
}

DELIMITERS = ["(", ")", "{", "}", "[", "]", ";", ",", "."]

WHITESPACE = [" ", "\t", "\n", "\r"]

COMMENT_MARKERS = {
    "linha": "//",
    "bloco_inicio": "/*",
    "bloco_fim": "*/",
}
