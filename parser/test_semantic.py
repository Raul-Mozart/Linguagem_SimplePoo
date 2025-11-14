"""
Teste Completo da Análise Semântica - SimplePOO
Demonstra todas as verificações implementadas
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))

from lexer_enhanced import EnhancedLexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

def test_semantic_analysis(code, description):
    """Testa análise semântica em um código"""
    print("=" * 70)
    print(f"TESTE: {description}")
    print("=" * 70)
    print(f"Código:\n{code}\n")
    
    # 1. Análise Léxica
    lexer = EnhancedLexer()
    tokens, lex_errors = lexer.tokenize(code)
    
    if lex_errors:
        print("❌ Erros léxicos encontrados:")
        for error in lex_errors:
            print(f"  {error}")
        return
    
    # 2. Análise Sintática
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        
        if parser.errors:
            print("❌ Erros sintáticos encontrados:")
            for error in parser.errors:
                print(f"  {error}")
            return
    except Exception as e:
        print(f"❌ Erro sintático: {e}")
        return
    
    # 3. Análise Semântica
    analyzer = SemanticAnalyzer()
    success, errors, warnings = analyzer.analyze(ast)
    
    # Resultados
    analyzer.print_errors()
    analyzer.print_warnings()
    
    if success:
        print("\n✅ Análise semântica bem-sucedida!")
        # analyzer.print_symbol_table()
    
    print("\n")


def main():
    print("\n" + "=" * 70)
    print("TESTES DE ANÁLISE SEMÂNTICA - SimplePOO")
    print("=" * 70 + "\n")
    
    # ============= TESTE 1: Código Correto =============
    test_semantic_analysis("""
        int x = 10;
        float y = 3.14;
        string nome = "João";
        bool ativo = true;
        
        function soma(a, b) {
            return a + b;
        }
        
        function teste() {
            int resultado = soma(x, 5);
            if (resultado > 10) {
                print(resultado);
            }
        }
    """, "Código Correto - Sem Erros")
    
    # ============= TESTE 2: Variável Não Declarada =============
    test_semantic_analysis("""
        int x = 10;
        int y = z + 5;
    """, "Erro: Variável Não Declarada")
    
    # ============= TESTE 3: Redeclaração =============
    test_semantic_analysis("""
        int x = 10;
        int x = 20;
    """, "Erro: Redeclaração de Variável")
    
    # ============= TESTE 4: Tipo Incompatível =============
    test_semantic_analysis("""
        int x = "texto";
    """, "Erro: Tipo Incompatível na Inicialização")
    
    # ============= TESTE 5: Atribuição a Constante =============
    test_semantic_analysis("""
        const PI = 3.14;
        PI = 3.15;
    """, "Erro: Atribuição a Constante")
    
    # ============= TESTE 6: Operação com Tipos Incompatíveis =============
    test_semantic_analysis("""
        int x = 10;
        string y = "texto";
        int z = x + y;
    """, "Erro: Operação com Tipos Incompatíveis")
    
    # ============= TESTE 7: Condição Não Booleana =============
    test_semantic_analysis("""
        int x = 10;
        if (x) {
            print(x);
        }
    """, "Erro: Condição Não Booleana no If")
    
    # ============= TESTE 8: Return Fora de Função =============
    test_semantic_analysis("""
        int x = 10;
        return x;
    """, "Erro: Return Fora de Função")
    
    # ============= TESTE 9: Break Fora de Loop =============
    test_semantic_analysis("""
        function teste() {
            break;
        }
    """, "Erro: Break Fora de Loop")
    
    # ============= TESTE 10: Variável Não Utilizada =============
    test_semantic_analysis("""
        function teste() {
            int x = 10;
            int y = 20;
            return x;
        }
    """, "Aviso: Variável Não Utilizada")
    
    # ============= TESTE 11: Shadowing (Correto) =============
    test_semantic_analysis("""
        int x = 10;
        
        function teste() {
            int x = 20;
            return x;
        }
    """, "Shadowing - Variável Local Sobrescreve Global")
    
    # ============= TESTE 12: Operações Aritméticas =============
    test_semantic_analysis("""
        int a = 10;
        int b = 5;
        int soma = a + b;
        int subtracao = a - b;
        int multiplicacao = a * b;
        int divisao = a / b;
        float resultado = a / 2.0;
    """, "Operações Aritméticas Corretas")
    
    # ============= TESTE 13: Operações Lógicas =============
    test_semantic_analysis("""
        bool a = true;
        bool b = false;
        bool e = a && b;
        bool ou = a || b;
        bool negacao = !a;
    """, "Operações Lógicas Corretas")
    
    # ============= TESTE 14: Comparações =============
    test_semantic_analysis("""
        int x = 10;
        int y = 20;
        bool maior = x > y;
        bool menor = x < y;
        bool igual = x == y;
        bool diferente = x != y;
    """, "Comparações Corretas")
    
    # ============= TESTE 15: Loop For =============
    test_semantic_analysis("""
        function teste() {
            for (int i = 0; i < 10; i++) {
                if (i == 5) {
                    break;
                }
                if (i == 3) {
                    continue;
                }
                print(i);
            }
        }
    """, "Loop For com Break e Continue")
    
    # ============= TESTE 16: Função Não Declarada =============
    test_semantic_analysis("""
        int x = funcaoInexistente(10);
    """, "Erro: Função Não Declarada")
    
    # ============= TESTE 17: Índice de Array Não Numérico =============
    test_semantic_analysis("""
        var arr = [1, 2, 3];
        string indice = "texto";
        var valor = arr[indice];
    """, "Erro: Índice de Array Não Numérico")
    
    # ============= TESTE 18: Inferência de Tipos =============
    test_semantic_analysis("""
        var x = 10;
        var y = 3.14;
        var z = "texto";
        var w = true;
    """, "Inferência de Tipos com 'var'")
    
    # ============= TESTE 19: Concatenação de Strings =============
    test_semantic_analysis("""
        string nome = "João";
        string sobrenome = "Silva";
        string completo = nome + sobrenome;
    """, "Concatenação de Strings Correta")
    
    # ============= TESTE 20: Código Complexo =============
    test_semantic_analysis("""
        int x = 10;
        
        function fatorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * fatorial(n - 1);
        }
        
        function parImpar(num) {
            if (num % 2 == 0) {
                return "par";
            } else {
                return "impar";
            }
        }
        
        function principal() {
            int resultado = fatorial(5);
            string tipo = parImpar(resultado);
            print(resultado);
            print(tipo);
            
            for (int i = 0; i < resultado; i++) {
                if (i % 2 == 0) {
                    print(i);
                }
            }
        }
    """, "Código Complexo - Múltiplas Funções")
    
    print("\n" + "=" * 70)
    print("TESTES COMPLETOS")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
