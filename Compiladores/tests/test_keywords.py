import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modulos_lexicos.analisador import LexicalAnalyzer


class KeywordRecognitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = LexicalAnalyzer()

    def test_keyword_var(self) -> None:
        tokens, errors = self.analyzer.tokenize("var")
        self.assertFalse(errors)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, "KEYWORD")

    def test_keyword_not_identifier(self) -> None:
        tokens, _ = self.analyzer.tokenize("var1")
        self.assertEqual(tokens[0].type, "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
