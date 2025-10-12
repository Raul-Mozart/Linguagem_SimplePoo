"""Definição de todos os autômatos determinísticos usados pelo lexer SimplePoo.

As construções aqui evitam totalmente expressões regulares. Cada tipo de token
é descrito por um autômato determinístico explícito construído com tabelas de
transição e predicados de caractere reutilizáveis.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from .dfa import (
    DeterministicAutomaton,
    Transition,
    always_true,
    is_digit,
    is_identifier_char,
    is_letter,
    is_whitespace,
    match_exact,
)
from .constantes import COMMENT_MARKERS, DELIMITERS as CONST_DELIMITERS
from .constantes import KEYWORDS as CONST_KEYWORDS
from .constantes import OPERATORS as CONST_OPERATORS


class TokenAutomaton:
    """Container que associa um autômato aos metadados do token."""

    def __init__(self, name: str, automaton: DeterministicAutomaton, priority: int) -> None:
        self.name = name
        self.automaton = automaton
        self.priority = priority

    def match(self, text: str, start: int) -> Tuple[int, str]:
        length, _ = self.automaton.consume_longest(text, start)
        return length, self.name


def _build_trie_transitions(tokens: List[str], base_name: str) -> Tuple[Dict[str, List[Transition]], List[str]]:
    table: Dict[str, Dict[str, str]] = {}
    accept_states: List[str] = []

    def ensure_state(name: str) -> Dict[str, str]:
        return table.setdefault(name, {})

    state_index = 0

    def new_state() -> str:
        nonlocal state_index
        state_index += 1
        return f"{base_name}_{state_index}"

    start_state = f"{base_name}_0"
    ensure_state(start_state)

    for token in tokens:
        state = start_state
        for ch in token:
            branch = ensure_state(state)
            if ch not in branch:
                branch[ch] = new_state()
            state = branch[ch]
            ensure_state(state)
        accept_states.append(state)

    transitions: Dict[str, List[Transition]] = {}
    for state, mapping in table.items():
        transitions[state] = [Transition(match_exact(ch), next_state) for ch, next_state in mapping.items()]

    return transitions, accept_states


def _build_keyword_automaton(keywords: List[str]) -> DeterministicAutomaton:
    transitions, accept_states = _build_trie_transitions(keywords, "kw_state")
    return DeterministicAutomaton("KEYWORD", "kw_state_0", accept_states, transitions)


def _build_identifier_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(is_letter, "id_body"), Transition(match_exact("_"), "id_body")],
        "id_body": [Transition(is_identifier_char, "id_body")],
    }
    accept_states = ["id_body"]
    return DeterministicAutomaton("IDENTIFIER", "s", accept_states, transitions)


def _build_integer_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact("0"), "zero"), Transition(lambda ch: ch in "123456789", "nonzero")],
        "zero": [],
        "nonzero": [Transition(is_digit, "nonzero")],
    }
    accept_states = ["zero", "nonzero"]
    return DeterministicAutomaton("INT_LITERAL", "s", accept_states, transitions)


def _build_float_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact("0"), "zero"), Transition(lambda ch: ch in "123456789", "int_part")],
        "zero": [Transition(match_exact("."), "after_dot_start")],
        "int_part": [
            Transition(is_digit, "int_part"),
            Transition(match_exact("."), "after_dot_start"),
        ],
        "after_dot_start": [Transition(is_digit, "frac_part")],
        "frac_part": [Transition(is_digit, "frac_part")],
    }
    accept_states = ["frac_part"]
    return DeterministicAutomaton("FLOAT_LITERAL", "s", accept_states, transitions)


def _build_scientific_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact("0"), "zero"), Transition(lambda ch: ch in "123456789", "int_part")],
        "zero": [Transition(match_exact("."), "after_dot_start"), Transition(lambda ch: ch in "eE", "exp"), Transition(is_digit, "int_part")],
        "int_part": [
            Transition(is_digit, "int_part"),
            Transition(match_exact("."), "after_dot_start"),
            Transition(lambda ch: ch in "eE", "exp"),
        ],
        "after_dot_start": [Transition(is_digit, "frac_part")],
        "frac_part": [
            Transition(is_digit, "frac_part"),
            Transition(lambda ch: ch in "eE", "exp"),
        ],
        "exp": [Transition(match_exact("+"), "exp_sign"), Transition(match_exact("-"), "exp_sign"), Transition(is_digit, "exp_digits")],
        "exp_sign": [Transition(is_digit, "exp_digits")],
        "exp_digits": [Transition(is_digit, "exp_digits")],
    }
    accept_states = ["exp_digits"]
    return DeterministicAutomaton("SCIENTIFIC_LITERAL", "s", accept_states, transitions)


def _build_string_automaton(delimiter: str) -> DeterministicAutomaton:
    name = "STRING_DOUBLE" if delimiter == '"' else "STRING_SINGLE"
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact(delimiter), "inside")],
        "inside": [
            Transition(match_exact("\\"), "escape"),
            Transition(lambda ch: ch != delimiter and ch not in "\n\r", "inside"),
            Transition(match_exact(delimiter), "end"),
        ],
        "escape": [Transition(always_true, "inside")],
        "end": [],
    }
    accept_states = ["end"]
    return DeterministicAutomaton(name, "s", accept_states, transitions)


def _build_char_literal_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact("'"), "start")],
        "start": [Transition(match_exact("\\"), "escape"), Transition(lambda ch: ch not in "'\n\r", "char")],
        "escape": [Transition(always_true, "char")],
        "char": [Transition(match_exact("'"), "end")],
        "end": [],
    }
    accept_states = ["end"]
    return DeterministicAutomaton("CHAR_LITERAL", "s", accept_states, transitions)


def _build_line_comment_automaton() -> DeterministicAutomaton:
    prefix = COMMENT_MARKERS["linha"]
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact(prefix[0]), "slash")],
        "slash": [Transition(match_exact(prefix[1]), "body")],
        "body": [Transition(lambda ch: ch not in "\n\r", "body"), Transition(lambda ch: ch in "\n\r", "end")],
        "end": [],
    }
    accept_states = ["body", "end"]
    return DeterministicAutomaton("LINE_COMMENT", "s", accept_states, transitions)


def _build_block_comment_automaton() -> DeterministicAutomaton:
    start = COMMENT_MARKERS["bloco_inicio"]
    end = COMMENT_MARKERS["bloco_fim"]
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(match_exact(start[0]), "slash")],
        "slash": [Transition(match_exact(start[1]), "body")],
        "body": [Transition(match_exact(end[0]), "star"), Transition(always_true, "body")],
        "star": [Transition(match_exact(end[1]), "end"), Transition(match_exact(end[0]), "star"), Transition(always_true, "body")],
        "end": [],
    }
    accept_states = ["end"]
    return DeterministicAutomaton("BLOCK_COMMENT", "s", accept_states, transitions)


def _build_whitespace_automaton() -> DeterministicAutomaton:
    transitions: Dict[str, List[Transition]] = {
        "s": [Transition(is_whitespace, "ws")],
        "ws": [Transition(is_whitespace, "ws")],
    }
    accept_states = ["ws"]
    return DeterministicAutomaton("WHITESPACE", "s", accept_states, transitions)


def _build_trie_automaton(tokens: List[str], name: str) -> DeterministicAutomaton:
    transitions, accept_states = _build_trie_transitions(tokens, f"{name.lower()}_state")
    return DeterministicAutomaton(name, f"{name.lower()}_state_0", accept_states, transitions)


KEYWORDS = CONST_KEYWORDS

OPERATORS = CONST_OPERATORS["combinados"] + CONST_OPERATORS["simples"]

DELIMITERS = CONST_DELIMITERS


TOKEN_AUTOMATA: List[TokenAutomaton] = [
    TokenAutomaton("WHITESPACE", _build_whitespace_automaton(), priority=0),
    TokenAutomaton("LINE_COMMENT", _build_line_comment_automaton(), priority=0),
    TokenAutomaton("BLOCK_COMMENT", _build_block_comment_automaton(), priority=0),
    TokenAutomaton("KEYWORD", _build_keyword_automaton(KEYWORDS), priority=10),
    TokenAutomaton("IDENTIFIER", _build_identifier_automaton(), priority=5),
    TokenAutomaton("SCIENTIFIC_LITERAL", _build_scientific_automaton(), priority=9),
    TokenAutomaton("FLOAT_LITERAL", _build_float_automaton(), priority=8),
    TokenAutomaton("INT_LITERAL", _build_integer_automaton(), priority=7),
    TokenAutomaton("STRING_DOUBLE", _build_string_automaton('"'), priority=6),
    TokenAutomaton("STRING_SINGLE", _build_string_automaton("'"), priority=6),
    TokenAutomaton("CHAR_LITERAL", _build_char_literal_automaton(), priority=6),
    TokenAutomaton("OPERATOR", _build_trie_automaton(OPERATORS, "OPERATOR"), priority=4),
    TokenAutomaton("DELIMITER", _build_trie_automaton(DELIMITERS, "DELIMITER"), priority=3),
]


AUTOMATA_BY_NAME: Dict[str, DeterministicAutomaton] = {
    wrapper.name: wrapper.automaton for wrapper in TOKEN_AUTOMATA
}
