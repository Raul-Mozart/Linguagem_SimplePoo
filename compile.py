#!/usr/bin/env python3
"""
Compilador SimplePOO - Versão Completa
======================================
Compila código SimplePOO para LLVM IR executável

Uso:
    python compile.py programa.txt
    python compile.py programa.txt -o saida.ll
    python compile.py programa.txt --run
    python compile.py programa.txt --verbose

Fases:
    1. Análise Léxica (Lexer)
    2. Análise Sintática (Parser)
    3. Análise Semântica
    4. Geração de Código LLVM IR
"""

import sys
import os
import argparse
from pathlib import Path

# Adicionar caminhos para módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lexer'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'parser'))

from lexer_enhanced import EnhancedLexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import LLVMCodeGenerator


class SimplePOOCompiler:
    """
    Compilador Completo SimplePOO
    
    Integra todas as 4 fases do compilador:
    - Lexer: Análise léxica (tokens)
    - Parser: Análise sintática (AST)
    - Semantic: Análise semântica (tipos, escopos)
    - CodeGen: Geração de código LLVM IR
    """
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.stats = {
            'tokens': 0,
            'ast_nodes': 0,
            'semantic_errors': 0,
            'ir_lines': 0
        }
    
    def log(self, message, level="INFO"):
        """Log com cores para melhor visualização"""
        colors = {
            "INFO": "\033[94m",     # Azul
            "OK": "\033[92m",       # Verde
            "ERROR": "\033[91m",    # Vermelho
            "WARN": "\033[93m",     # Amarelo
            "RESET": "\033[0m"
        }
        if self.verbose:
            color = colors.get(level, colors["RESET"])
            print(f"{color}[{level}]{colors['RESET']} {message}")
    
    def compile(self, source_code, output_file=None):
        """
        Compila código SimplePOO completo
        
        Args:
            source_code: String com código fonte
            output_file: Caminho para salvar .ll (opcional)
        
        Returns:
            (success: bool, ir_code: str, errors: list)
        """
        try:
            # ============= FASE 1: ANÁLISE LÉXICA =============
            self.log("=" * 60)
            self.log("FASE 1: ANÁLISE LÉXICA", "INFO")
            self.log("=" * 60)
            
            lexer = EnhancedLexer()
            tokens, errors = lexer.tokenize(source_code)
            
            if errors:
                self.log(f"✗ {len(errors)} erro(s) léxico(s) encontrado(s)", "ERROR")
                for error in errors:
                    print(f"  {error}")
                return False, None, errors
            
            self.stats['tokens'] = len(tokens)
            self.log(f"✓ {len(tokens)} tokens reconhecidos", "OK")
            
            if self.verbose:
                print("\nTokens encontrados:")
                for i, token in enumerate(tokens[:10], 1):  # Mostra primeiros 10
                    print(f"  {i:2}. {token}")
                if len(tokens) > 10:
                    print(f"  ... e mais {len(tokens) - 10} tokens")
            
            # ============= FASE 2: ANÁLISE SINTÁTICA =============
            self.log("\n" + "=" * 60)
            self.log("FASE 2: ANÁLISE SINTÁTICA", "INFO")
            self.log("=" * 60)
            
            parser = Parser(lexer)
            ast = parser.parse()
            
            if parser.errors:
                self.log(f"✗ {len(parser.errors)} erro(s) sintático(s)", "ERROR")
                for error in parser.errors:
                    print(f"  {error}")
                return False, None, parser.errors
            
            self.stats['ast_nodes'] = self._count_ast_nodes(ast)
            self.log(f"✓ AST construída com sucesso ({self.stats['ast_nodes']} nós)", "OK")
            
            if self.verbose:
                print(f"\nEstrutura da AST:")
                print(f"  Declarações: {len(ast.declarations)}")
                for decl in ast.declarations:
                    if hasattr(decl, 'name'):
                        print(f"    - {decl.__class__.__name__}: {decl.name}")
            
            # ============= FASE 3: ANÁLISE SEMÂNTICA =============
            self.log("\n" + "=" * 60)
            self.log("FASE 3: ANÁLISE SEMÂNTICA", "INFO")
            self.log("=" * 60)
            
            semantic = SemanticAnalyzer()
            semantic.analyze(ast)
            
            if semantic.errors:
                self.log(f"✗ {len(semantic.errors)} erro(s) semântico(s)", "ERROR")
                for error in semantic.errors:
                    print(f"  {error}")
                self.stats['semantic_errors'] = len(semantic.errors)
                return False, None, semantic.errors
            
            self.log("✓ Verificação semântica concluída", "OK")
            
            if semantic.warnings:
                self.log(f"⚠ {len(semantic.warnings)} aviso(s)", "WARN")
                for warning in semantic.warnings:
                    print(f"  {warning}")
            
            if self.verbose:
                print(f"\nTabela de Símbolos:")
                symbols = semantic.symbol_table.get_all_symbols()
                if isinstance(symbols, dict):
                    for name, symbol in list(symbols.items())[:10]:
                        print(f"  {name}: {symbol.type} (escopo: {symbol.scope})")
                    if len(symbols) > 10:
                        print(f"  ... e mais {len(symbols) - 10} símbolos")
                elif isinstance(symbols, list):
                    for symbol in symbols[:10]:
                        print(f"  {symbol.name}: {symbol.type} (escopo: {symbol.scope})")
                    if len(symbols) > 10:
                        print(f"  ... e mais {len(symbols) - 10} símbolos")
            
            # ============= FASE 4: GERAÇÃO DE CÓDIGO =============
            self.log("\n" + "=" * 60)
            self.log("FASE 4: GERAÇÃO DE CÓDIGO LLVM IR", "INFO")
            self.log("=" * 60)
            
            codegen = LLVMCodeGenerator()
            codegen.add_format_strings()  # Adiciona strings para printf
            ir_code = codegen.generate(ast)
            
            self.stats['ir_lines'] = len(ir_code.split('\n'))
            self.log(f"✓ Código LLVM IR gerado ({self.stats['ir_lines']} linhas)", "OK")
            
            # Salvar arquivo .ll se especificado
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(ir_code)
                self.log(f"✓ Código salvo em: {output_file}", "OK")
            
            # ============= RESUMO =============
            self.log("\n" + "=" * 60)
            self.log("COMPILAÇÃO CONCLUÍDA COM SUCESSO!", "OK")
            self.log("=" * 60)
            print(f"\n📊 Estatísticas:")
            print(f"  • Tokens reconhecidos: {self.stats['tokens']}")
            print(f"  • Nós da AST: {self.stats['ast_nodes']}")
            print(f"  • Erros semânticos: {self.stats['semantic_errors']}")
            print(f"  • Linhas de IR: {self.stats['ir_lines']}")
            
            return True, ir_code, []
        
        except Exception as e:
            self.log(f"✗ Erro durante compilação: {str(e)}", "ERROR")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return False, None, [str(e)]
    
    def _count_ast_nodes(self, node, count=0):
        """Conta número de nós na AST recursivamente"""
        count += 1
        if hasattr(node, 'declarations'):
            for decl in node.declarations:
                count = self._count_ast_nodes(decl, count)
        elif hasattr(node, 'body') and isinstance(node.body, list):
            for stmt in node.body:
                count = self._count_ast_nodes(stmt, count)
        elif hasattr(node, 'left'):
            count = self._count_ast_nodes(node.left, count)
            if hasattr(node, 'right'):
                count = self._count_ast_nodes(node.right, count)
        return count


def main():
    """Função principal - interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Compilador SimplePOO - Compila para LLVM IR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python compile.py programa.txt
  python compile.py programa.txt -o saida.ll
  python compile.py programa.txt --run
  python compile.py programa.txt -v --run
  
Executar código gerado:
  lli saida.ll                    # Executar com interpretador LLVM
  llc saida.ll -o saida.s         # Compilar para assembly
  gcc saida.s -o programa         # Compilar para executável
  ./programa                      # Executar
        """
    )
    
    parser.add_argument('input', help='Arquivo de entrada (.txt)')
    parser.add_argument('-o', '--output', help='Arquivo de saída (.ll)', default=None)
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    parser.add_argument('-r', '--run', action='store_true', help='Executar com lli após compilar')
    parser.add_argument('--show-ir', action='store_true', help='Mostrar código IR gerado')
    
    args = parser.parse_args()
    
    # Verificar se arquivo existe
    if not os.path.exists(args.input):
        print(f"\033[91mERRO: Arquivo '{args.input}' nao encontrado\033[0m")
        return 1
    
    # Ler código fonte
    with open(args.input, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # Definir arquivo de saída
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.with_suffix('.ll'))
    
    # Compilar
    compiler = SimplePOOCompiler(verbose=args.verbose)
    success, ir_code, errors = compiler.compile(source_code, args.output)
    
    if not success:
        print(f"\n\033[91mX Compilacao falhou com {len(errors)} erro(s)\033[0m")
        return 1
    
    # Mostrar IR se solicitado
    if args.show_ir and ir_code:
        print(f"\n{'=' * 60}")
        print("CÓDIGO LLVM IR GERADO:")
        print('=' * 60)
        print(ir_code)
    
    # Executar com lli se solicitado
    if args.run:
        print(f"\n{'=' * 60}")
        print("EXECUTANDO COM LLI:")
        print('=' * 60)
        import subprocess
        try:
            result = subprocess.run(['lli', args.output], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=5)
            print(result.stdout)
            if result.stderr:
                print(f"\033[93mErros/Avisos:\033[0m\n{result.stderr}")
            if result.returncode != 0:
                print(f"\033[91mX Execucao terminou com codigo {result.returncode}\033[0m")
        except FileNotFoundError:
            print("\033[93mAVISO: lli nao encontrado. Instale LLVM primeiro.\033[0m")
            print("  Veja INSTALL.md para instrucoes de instalacao.")
        except subprocess.TimeoutExpired:
            print("\033[91mX Timeout: Programa demorou mais de 5 segundos\033[0m")
    
    print(f"\n\033[92mOK - Compilacao concluida com sucesso!\033[0m")
    print(f"  Arquivo gerado: {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
