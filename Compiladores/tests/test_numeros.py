import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.afd_tokens import AUTOMATA_BY_NAME


class NumberAutomataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.int_automaton = AUTOMATA_BY_NAME["INT_LITERAL"]
        self.float_automaton = AUTOMATA_BY_NAME["FLOAT_LITERAL"]
        self.scientific_automaton = AUTOMATA_BY_NAME["SCIENTIFIC_LITERAL"]

    def test_int_accepts_zero(self) -> None:
        self.assertTrue(self.int_automaton.accepts("0"))

    def test_int_rejects_leading_zero(self) -> None:
        self.assertFalse(self.int_automaton.accepts("012"))

    def test_float_accepts(self) -> None:
        self.assertTrue(self.float_automaton.accepts("3.14"))

    def test_float_rejects_missing_fraction(self) -> None:
        self.assertFalse(self.float_automaton.accepts("3."))

    def test_scientific_accepts_uppercase_e(self) -> None:
        self.assertTrue(self.scientific_automaton.accepts("3.0E+10"))

    def test_scientific_rejects_missing_exponent(self) -> None:
        self.assertFalse(self.scientific_automaton.accepts("5.0e"))


if __name__ == "__main__":
    unittest.main()
