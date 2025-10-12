# Interface simples para visualizar o funcionamento dos DFAs da linguagem.

from __future__ import annotations

from modulos_lexicos.afd_tokens import KEYWORDS, TOKEN_AUTOMATA
from modulos_lexicos.analisador import LexicalAnalyzer


def listar_automatos() -> None:
    print("AUTÔMATOS CONFIGURADOS")
    print("-" * 60)
    for token in TOKEN_AUTOMATA:
        print(f"{token.name:20} | estados de aceitação: {len(token.automaton.accept_states)}")
    print()


def exemplo_tokenizacao() -> None:
    codigo = (
        "var int idade as 25;\n"
        "var float altura as 1.75;\n"
        "var string nome as \"João\";\n"
        "if (idade >= 18) {\n"
        "    return true;\n"
        "}\n"
    )
    analyzer = LexicalAnalyzer()
    tokens, errors = analyzer.tokenize(codigo)
    print("EXEMPLO DE TOKENIZAÇÃO")
    print("-" * 60)
    for token in tokens:
        print(f"{token.lexeme:<15} | {token.type:<18} | [{token.line}:{token.column}]")
    if errors:
        print("\nErros encontrados:")
        for error in errors:
            print(f"- {error.message} (linha {error.line}, coluna {error.column})")
    print()


def listar_keywords() -> None:
    print("PALAVRAS RESERVADAS")
    print("-" * 60)
    for keyword in sorted(KEYWORDS):
        print(keyword)
    print()


def main() -> None:
    print("COMPILADORES - VISUALIZAÇÃO DOS AFDs")
    print("=" * 60)
    listar_automatos()
    listar_keywords()
    exemplo_tokenizacao()


if __name__ == "__main__":
    main()
