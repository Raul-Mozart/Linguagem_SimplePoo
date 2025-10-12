"""Analisador léxico que consome os autômatos determinísticos definidos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .afd_tokens import TOKEN_AUTOMATA, KEYWORDS
from .dfa import DeterministicAutomaton


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int


@dataclass
class LexicalError:
    message: str
    line: int
    column: int
    context: str


class LexicalAnalyzer:
    """Tokeniza o código-fonte utilizando os DFAs previamente construídos."""

    def __init__(self) -> None:
        self.automata = TOKEN_AUTOMATA
        self.keyword_set = set(KEYWORDS)

    def _select_match(
        self,
        source: str,
        index: int,
    ) -> Tuple[Optional[str], int]:
        best_type: Optional[str] = None
        best_len = 0
        best_priority = -1

        for wrapper in self.automata:
            length, token_type = wrapper.match(source, index)
            if length == 0:
                continue
            if length > best_len or (length == best_len and wrapper.priority > best_priority):
                best_len = length
                best_type = token_type
                best_priority = wrapper.priority

        return best_type, best_len

    def tokenize(self, code: str) -> Tuple[List[Token], List[LexicalError]]:
        tokens: List[Token] = []
        errors: List[LexicalError] = []
        line = 1
        column = 1
        index = 0
        length = len(code)

        while index < length:
            token_type, match_len = self._select_match(code, index)

            if token_type is None or match_len == 0:
                errors.append(
                    LexicalError(
                        message="Caractere inválido conforme especificação de tokens.",
                        line=line,
                        column=column,
                        context=code[index],
                    )
                )
                index += 1
                if code[index - 1] == "\n":
                    line += 1
                    column = 1
                else:
                    column += 1
                continue

            lexeme = code[index : index + match_len]

            if token_type in {"WHITESPACE", "LINE_COMMENT", "BLOCK_COMMENT"}:
                for ch in lexeme:
                    if ch == "\n":
                        line += 1
                        column = 1
                    else:
                        column += 1
                index += match_len
                continue

            if token_type == "IDENTIFIER" and lexeme in self.keyword_set:
                token_type = "KEYWORD"

            tokens.append(Token(token_type, lexeme, line, column))

            for ch in lexeme:
                if ch == "\n":
                    line += 1
                    column = 1
                else:
                    column += 1

            index += match_len

        return tokens, errors
