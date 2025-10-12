import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.afd_tokens import AUTOMATA_BY_NAME


class TriviaAutomataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ws = AUTOMATA_BY_NAME["WHITESPACE"]
        self.line = AUTOMATA_BY_NAME["LINE_COMMENT"]
        self.block = AUTOMATA_BY_NAME["BLOCK_COMMENT"]

    def test_whitespace_accepts_spaces_and_newlines(self) -> None:
        self.assertTrue(self.ws.accepts(" \t\n"))

    def test_whitespace_rejects_letter(self) -> None:
        self.assertFalse(self.ws.accepts(" a"))

    def test_line_comment_accepts_until_newline(self) -> None:
        self.assertTrue(self.line.consume_longest("// comentario\nresto")[0] >= 2)

    def test_block_comment_accepts_balanced(self) -> None:
        self.assertTrue(self.block.accepts("/* bloco */"))

    def test_block_comment_rejects_unclosed(self) -> None:
        self.assertFalse(self.block.accepts("/* aberto"))


if __name__ == "__main__":
    unittest.main()
