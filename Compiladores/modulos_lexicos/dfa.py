"""Primitivas mínimas de autômato determinístico utilizadas na
ferramenta da linguagem SimplePoo.

A implementação é propositalmente leve e evita expressões regulares,
confiando somente em transições explícitas de estado.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

Condition = Callable[[str], bool]


@dataclass(frozen=True)
class Transition:
    """Representa uma transição condicionada por um predicado de caractere."""

    condition: Condition
    next_state: str


class DeterministicAutomaton:
    """DFA simples com suporte à leitura do maior prefixo aceito."""

    def __init__(
        self,
        name: str,
        start_state: str,
        accept_states: List[str],
        transitions: Dict[str, List[Transition]],
    ) -> None:
        self.name = name
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = transitions

    def _step(self, state: str, ch: str) -> Optional[str]:
        for transition in self.transitions.get(state, []):
            if transition.condition(ch):
                return transition.next_state
        return None

    def accepts(self, text: str) -> bool:
        state = self.start_state
        if not text:
            return state in self.accept_states
        for ch in text:
            state = self._step(state, ch)
            if state is None:
                return False
        return state in self.accept_states

    def consume_longest(self, text: str, start: int = 0) -> Tuple[int, Optional[str]]:
        """Retorna o tamanho do maior prefixo aceito a partir de *start*.

        O segundo valor indica o estado que gerou a aceitação, útil quando
        autômatos compartilham lógica (por exemplo, palavras-chave vs
        identificadores).
        """

        state = self.start_state
        longest_accept = -1
        accept_state: Optional[str] = None
        i = start
        while i < len(text):
            next_state = self._step(state, text[i])
            if next_state is None:
                break
            state = next_state
            i += 1
            if state in self.accept_states:
                longest_accept = i
                accept_state = state
        if longest_accept == -1:
            return 0, None
        return longest_accept - start, accept_state


# Funções auxiliares centralizadas para evitar duplicação.
def is_upper(ch: str) -> bool:
    return "A" <= ch <= "Z"


def is_lower(ch: str) -> bool:
    return "a" <= ch <= "z"


def is_letter(ch: str) -> bool:
    return is_lower(ch) or is_upper(ch)


def is_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def is_alnum(ch: str) -> bool:
    return is_letter(ch) or is_digit(ch)


def is_identifier_char(ch: str) -> bool:
    return is_alnum(ch) or ch == "_"


def is_whitespace(ch: str) -> bool:
    return ch in " \t\r\n"


def always_true(_: str) -> bool:
    return True


def match_exact(expected: str) -> Condition:
    def _match(ch: str) -> bool:
        return ch == expected

    return _match
