import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.afd_tokens import AUTOMATA_BY_NAME


class IdentifierAutomatonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.automaton = AUTOMATA_BY_NAME["IDENTIFIER"]

    def test_accepts_basic_identifier(self) -> None:
        self.assertTrue(self.automaton.accepts("variavel"))

    def test_accepts_identifier_with_digits_and_underscore(self) -> None:
        self.assertTrue(self.automaton.accepts("dados_123"))

    def test_rejects_identifier_starting_with_digit(self) -> None:
        self.assertFalse(self.automaton.accepts("1invalido"))

    def test_rejects_symbol(self) -> None:
        self.assertFalse(self.automaton.accepts("nome-errado"))


if __name__ == "__main__":
    unittest.main()
