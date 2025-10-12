import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.afd_tokens import AUTOMATA_BY_NAME


class OperatorAutomatonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.operator = AUTOMATA_BY_NAME["OPERATOR"]
        self.delimiter = AUTOMATA_BY_NAME["DELIMITER"]

    def test_operator_accepts_double(self) -> None:
        self.assertTrue(self.operator.accepts("=="))

    def test_operator_accepts_single(self) -> None:
        self.assertTrue(self.operator.accepts("+"))

    def test_operator_rejects_unknown(self) -> None:
        self.assertFalse(self.operator.accepts("<>"))

    def test_delimiter_accepts_parenthesis(self) -> None:
        self.assertTrue(self.delimiter.accepts("("))

    def test_delimiter_rejects_letter(self) -> None:
        self.assertFalse(self.delimiter.accepts("a"))


if __name__ == "__main__":
    unittest.main()
