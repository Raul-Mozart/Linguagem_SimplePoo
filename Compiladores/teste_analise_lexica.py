# Ferramenta de demonstração para o analisador léxico baseado em DFAs.
# Mantém interface simples: analisa arquivo ou exemplo integrado.

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from modulos_lexicos.analisador import LexicalAnalyzer


def format_tokens(tokens: Iterable) -> str:
    lines = ["TOKEN                | TIPO                | [linha:coluna]"]
    lines.append("-" * 60)
    for token in tokens:
        display = token.lexeme if len(token.lexeme) <= 18 else token.lexeme[:15] + "..."
        lines.append(f"{display:<20} | {token.type:<20} | [{token.line}:{token.column}]")
    return "\n".join(lines)


def format_errors(errors: Iterable) -> str:
    if not errors:
        return "Nenhum erro léxico encontrado."
    lines = ["Erros léxicos (contexto exibido entre colchetes):"]
    for error in errors:
        lines.append(
            f"- Linha {error.line}, coluna {error.column}: {error.message} [ {error.context} ]"
        )
    return "\n".join(lines)


def run_analysis(code: str) -> None:
    analyzer = LexicalAnalyzer()
    tokens, errors = analyzer.tokenize(code)
    print(format_tokens(tokens))
    print()
    print(format_errors(errors))


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa análise léxica utilizando DFAs determinísticos.")
    parser.add_argument("arquivo", nargs="?", help="Caminho para o arquivo fonte a ser analisado")
    args = parser.parse_args()

    if args.arquivo:
        caminho = Path(args.arquivo)
        if not caminho.exists():
            raise SystemExit(f"Arquivo não encontrado: {caminho}")
        code = caminho.read_text(encoding="utf-8")
        run_analysis(code)
    else:
        exemplo = (
            "var int idade as 25;\n"
            "function exemplo(valor) {\n"
            "    if (valor >= 10) {\n"
            "        return \"maior\";\n"
            "    }\n"
            "    return \"menor\";\n"
            "}\n"
        )
        print("Analisando exemplo padrão (para analisar arquivo passe o caminho como argumento).\n")
        run_analysis(exemplo)


if __name__ == "__main__":
    main()
