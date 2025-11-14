"""
Exemplo Simples de Análise Semântica
Testa casos básicos e principais funcionalidades
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))

from lexer_enhanced import EnhancedLexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

def test_code(title, code):
    """Testa um código e mostra resultados"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)
    print(f"Código:\n{code}\n")
    
    # Léxica
    lexer = EnhancedLexer()
    tokens, lex_errors = lexer.tokenize(code)
    if lex_errors:
        print("[X] Erros lexicos:")
        for e in lex_errors:
            print(f"  {e}")
        return
    
    # Sintática
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        if parser.errors:
            print("[X] Erros sintaticos:")
            for e in parser.errors:
                print(f"  {e}")
            return
    except Exception as e:
        print(f"[X] Erro sintatico: {e}")
        return
    
    # Semântica
    analyzer = SemanticAnalyzer()
    success, errors, warnings = analyzer.analyze(ast)
    
    if errors:
        print(f"[X] {len(errors)} erro(s) semantico(s):")
        for e in errors:
            print(f"  {e}")
    else:
        print("[OK] Nenhum erro semantico!")
    
    if warnings:
        print(f"\n[!] {len(warnings)} aviso(s):")
        for w in warnings:
            print(f"  {w}")

print("\n" + "="*60)
print("EXEMPLOS DE ANÁLISE SEMÂNTICA")
print("="*60)

# 1. Código correto
test_code("1. Código Correto", """
int x = 10;
int y = 20;
int soma = x + y;
""")

# 2. Variável não declarada
test_code("2. Variável Não Declarada", """
int x = 10;
int y = z + 5;
""")

# 3. Redeclaração
test_code("3. Redeclaração", """
int x = 10;
int x = 20;
""")

# 4. Tipo incompatível
test_code("4. Tipo Incompatível", """
int x = "texto";
""")

# 5. Constante
test_code("5. Atribuição a Constante", """
const PI = 3.14;
PI = 3.15;
""")

# 6. Operação inválida
test_code("6. Operação Inválida", """
int x = 10;
string y = "ola";
int z = x + y;
""")

# 7. Condição não booleana
test_code("7. Condição Não Booleana", """
int x = 10;
if (x) {
    print(x);
}
""")

# 8. Função
test_code("8. Função Simples", """
function soma(a, b) {
    return a + b;
}

int resultado = soma(10, 20);
""")

# 9. Shadowing
test_code("9. Shadowing (Correto)", """
int x = 10;

function teste() {
    int x = 20;
    print(x);
}
""")

# 10. Variável não usada
test_code("10. Variável Não Usada", """
function teste() {
    int x = 10;
    int y = 20;
    return x;
}
""")

# 11. Operações aritméticas
test_code("11. Operações Aritméticas", """
int a = 10;
int b = 5;
int soma = a + b;
int diff = a - b;
int prod = a * b;
int div = a / b;
""")

# 12. Operações lógicas
test_code("12. Operações Lógicas", """
bool a = true;
bool b = false;
bool e = a && b;
bool ou = a || b;
bool neg = !a;
""")

# 13. Comparações
test_code("13. Comparações", """
int x = 10;
int y = 20;
bool maior = x > y;
bool igual = x == y;
""")

# 14. Inferência de tipos
test_code("14. Inferência com 'var'", """
var x = 10;
var y = 3.14;
var z = "texto";
""")

# 15. Loop
test_code("15. Loop For", """
function teste() {
    for (int i = 0; i < 10; i++) {
        print(i);
    }
}
""")

print("\n" + "="*60)
print("TESTES COMPLETOS")
print("="*60 + "\n")
