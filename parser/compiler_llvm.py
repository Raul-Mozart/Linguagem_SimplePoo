"""
Compilador Completo SimplePOO com Geração de Código LLVM
Integra: Léxica -> Sintática -> Semântica -> Geração de Código
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))

from lexer_enhanced import EnhancedLexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import LLVMCodeGenerator
import subprocess
import tempfile

def compile_to_llvm(code, output_file=None, show_ir=True, run=False):
    """
    Compila código SimplePOO para LLVM IR
    
    Args:
        code: Código fonte SimplePOO
        output_file: Arquivo de saída (.ll)
        show_ir: Mostrar IR gerado
        run: Executar com lli
    
    Returns:
        (success, ir_code) - Tupla com sucesso e código IR
    """
    print("\n" + "="*70)
    print("COMPILADOR SimplePOO -> LLVM IR")
    print("="*70)
    
    # =========== FASE 1: ANÁLISE LÉXICA ===========
    print("\n[1/4] ANALISE LEXICA")
    print("-" * 70)
    
    lexer = EnhancedLexer()
    tokens, lex_errors = lexer.tokenize(code)
    
    if lex_errors:
        print(f"[X] {len(lex_errors)} erro(s) lexico(s):")
        for e in lex_errors:
            print(f"  {e}")
        return False, None
    
    print(f"[OK] {len(tokens)} tokens reconhecidos")
    
    # =========== FASE 2: ANÁLISE SINTÁTICA ===========
    print("\n[2/4] ANALISE SINTATICA")
    print("-" * 70)
    
    parser = Parser(lexer)
    
    try:
        ast = parser.parse()
        if parser.errors:
            print(f"[X] {len(parser.errors)} erro(s) sintatico(s):")
            for e in parser.errors:
                print(f"  {e}")
            return False, None
        
        print("[OK] AST construida")
    
    except Exception as e:
        print(f"[X] Erro sintatico: {e}")
        return False, None
    
    # =========== FASE 3: ANÁLISE SEMÂNTICA ===========
    print("\n[3/4] ANALISE SEMANTICA")
    print("-" * 70)
    
    analyzer = SemanticAnalyzer()
    success, errors, warnings = analyzer.analyze(ast)
    
    if errors:
        print(f"[X] {len(errors)} erro(s) semantico(s):")
        for e in errors:
            print(f"  {e}")
        return False, None
    
    print("[OK] Verificacao semantica concluida")
    
    if warnings:
        print(f"[!] {len(warnings)} aviso(s):")
        for w in warnings:
            print(f"  {w}")
    
    # =========== FASE 4: GERAÇÃO DE CÓDIGO ===========
    print("\n[4/4] GERACAO DE CODIGO LLVM IR")
    print("-" * 70)
    
    generator = LLVMCodeGenerator()
    generator.add_format_strings()
    ir_code = generator.generate(ast)
    
    print(f"[OK] Codigo LLVM IR gerado ({len(ir_code.split(chr(10)))} linhas)")
    
    # Salva em arquivo se especificado
    if output_file:
        with open(output_file, 'w') as f:
            f.write(ir_code)
        print(f"[OK] Salvo em: {output_file}")
    
    # Mostra IR gerado
    if show_ir:
        print("\n" + "="*70)
        print("CODIGO LLVM IR GERADO")
        print("="*70)
        print(ir_code)
    
    # Executa com lli
    if run:
        print("\n" + "="*70)
        print("EXECUTANDO COM LLI")
        print("="*70)
        
        # Salva em arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ll', delete=False) as f:
            f.write(ir_code)
            temp_file = f.name
        
        try:
            result = subprocess.run(['lli', temp_file], 
                                    capture_output=True, 
                                    text=True,
                                    timeout=5)
            
            if result.returncode == 0:
                print("[OK] Execucao bem-sucedida!")
                if result.stdout:
                    print("\nSaida do programa:")
                    print(result.stdout)
            else:
                print(f"[X] Erro na execucao (codigo {result.returncode})")
                if result.stderr:
                    print(result.stderr)
        
        except FileNotFoundError:
            print("[!] lli nao encontrado. Instale LLVM para executar.")
        except subprocess.TimeoutExpired:
            print("[X] Timeout na execucao")
        finally:
            os.unlink(temp_file)
    
    print("\n" + "="*70)
    print("[OK] COMPILACAO COMPLETA!")
    print("="*70)
    
    return True, ir_code


def main():
    """Testa compilador com exemplos"""
    
    print("\n" + "="*70)
    print("COMPILADOR SimplePOO -> LLVM IR - EXEMPLOS")
    print("="*70)
    
    # ========== EXEMPLO 1: Programa Simples ==========
    print("\n" + "="*70)
    print("EXEMPLO 1: Programa Simples")
    print("="*70)
    
    code1 = """
function main() {
    int x = 10;
    int y = 20;
    int soma = x + y;
    print(soma);
}
"""
    
    print(f"\nCodigo SimplePOO:\n{code1}")
    compile_to_llvm(code1, output_file="exemplo1.ll", show_ir=True, run=False)
    
    # ========== EXEMPLO 2: Função com Parâmetros ==========
    print("\n" + "="*70)
    print("EXEMPLO 2: Funcao com Parametros")
    print("="*70)
    
    code2 = """
function soma(a, b) {
    int resultado = a + b;
    return resultado;
}

function main() {
    int x = soma(10, 20);
    print(x);
}
"""
    
    print(f"\nCodigo SimplePOO:\n{code2}")
    compile_to_llvm(code2, output_file="exemplo2.ll", show_ir=False, run=False)
    
    # ========== EXEMPLO 3: Condicionais ==========
    print("\n" + "="*70)
    print("EXEMPLO 3: Condicionais")
    print("="*70)
    
    code3 = """
function main() {
    int x = 15;
    
    if (x > 10) {
        print(1);
    } else {
        print(0);
    }
}
"""
    
    print(f"\nCodigo SimplePOO:\n{code3}")
    compile_to_llvm(code3, output_file="exemplo3.ll", show_ir=False, run=False)
    
    # ========== EXEMPLO 4: Loop ==========
    print("\n" + "="*70)
    print("EXEMPLO 4: Loop For")
    print("="*70)
    
    code4 = """
function main() {
    int soma = 0;
    
    for (int i = 1; i <= 10; i++) {
        soma = soma + i;
    }
    
    print(soma);
}
"""
    
    print(f"\nCodigo SimplePOO:\n{code4}")
    compile_to_llvm(code4, output_file="exemplo4.ll", show_ir=False, run=False)
    
    # ========== EXEMPLO 5: Operações ==========
    print("\n" + "="*70)
    print("EXEMPLO 5: Operacoes Aritmeticas")
    print("="*70)
    
    code5 = """
function main() {
    int a = 100;
    int b = 50;
    
    int soma = a + b;
    int diff = a - b;
    int prod = a * b;
    int div = a / b;
    
    print(soma);
    print(diff);
    print(prod);
    print(div);
}
"""
    
    print(f"\nCodigo SimplePOO:\n{code5}")
    compile_to_llvm(code5, output_file="exemplo5.ll", show_ir=False, run=False)
    
    # ========== RESUMO FINAL ==========
    print("\n" + "="*70)
    print("RESUMO")
    print("="*70)
    print("""
FASES IMPLEMENTADAS:
[OK] 1. Analise Lexica - Tokenizacao
[OK] 2. Analise Sintatica - Construcao de AST
[OK] 3. Analise Semantica - Tipos e Escopos
[OK] 4. Geracao de Codigo - LLVM IR

RECURSOS DO GERADOR:
- Traducao de expressoes (aritmeticas, logicas, comparacoes)
- Traducao de comandos (declaracoes, atribuicoes, if/else, loops)
- Funcoes com parametros
- Variaveis locais (alloca/load/store)
- Blocos basicos e controle de fluxo
- Formato textual LLVM (.ll)

PROXIMOS PASSOS:
[ ] Otimizacao com opt
[ ] Compilacao para assembly com llc
[ ] Geracao de executavel
[ ] Suporte a tipos complexos (arrays, structs)
[ ] Chamadas de sistema
    """)
    print("="*70 + "\n")
    
    # Instruções de uso
    print("\nPara executar o codigo gerado:")
    print("  lli exemplo1.ll")
    print("\nPara compilar para executavel:")
    print("  llc exemplo1.ll -o exemplo1.s")
    print("  gcc exemplo1.s -o exemplo1")
    print("  ./exemplo1")


if __name__ == "__main__":
    main()
