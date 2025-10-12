import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.afd_tokens import AUTOMATA_BY_NAME


class StringAutomataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.double = AUTOMATA_BY_NAME["STRING_DOUBLE"]
        self.single = AUTOMATA_BY_NAME["STRING_SINGLE"]
        self.char = AUTOMATA_BY_NAME["CHAR_LITERAL"]

    def test_double_string_accepts(self) -> None:
        self.assertTrue(self.double.accepts("\"texto\""))

    def test_double_string_rejects_unclosed(self) -> None:
        self.assertFalse(self.double.accepts("\"texto"))

    def test_single_string_accepts(self) -> None:
        self.assertTrue(self.single.accepts("'abc'"))

    def test_char_accepts_escape(self) -> None:
        self.assertTrue(self.char.accepts("'\\n'"))

    def test_char_rejects_long(self) -> None:
        self.assertFalse(self.char.accepts("'ab'"))


if __name__ == "__main__":
    unittest.main()
