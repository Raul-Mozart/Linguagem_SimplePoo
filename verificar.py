#!/usr/bin/env python3
"""
Script de Verificação do Compilador SimplePOO
==============================================
Verifica que todos os componentes estão instalados e funcionando
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime cabeçalho colorido"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def print_ok(text):
    """Imprime mensagem de sucesso"""
    print(f"✓ {text}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"✗ {text}")

def print_warning(text):
    """Imprime aviso"""
    print(f"⚠ {text}")

def main():
    """Função principal de verificação"""
    print_header("VERIFICAÇÃO DO COMPILADOR SIMPLEPOO")
    
    errors = []
    warnings = []
    
    # 1. Verificar Python
    print("\n1. Verificando Python...")
    try:
        version = sys.version.split()[0]
        major, minor = map(int, version.split('.')[:2])
        if major >= 3 and minor >= 8:
            print_ok(f"Python {version} instalado")
        else:
            print_warning(f"Python {version} - Recomendado 3.8+")
            warnings.append("Python antigo")
    except:
        print_error("Erro ao verificar Python")
        errors.append("Python")
    
    # 2. Verificar estrutura de arquivos
    print("\n2. Verificando arquivos do projeto...")
    required_files = [
        'compile.py',
        'README.md',
        'INSTALL.md',
        'MANUAL_USO.md',
        'ENTREGA_FINAL.md',
        'lexer/lexer_enhanced.py',
        'parser/parser.py',
        'parser/semantic_analyzer.py',
        'parser/code_generator.py',
        'parser/ast_nodes.py',
        'parser/symbol_table.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print_ok(f"Arquivo encontrado: {file}")
        else:
            print_error(f"Arquivo faltando: {file}")
            errors.append(f"Arquivo {file}")
    
    # 3. Verificar pasta de exemplos
    print("\n3. Verificando exemplos...")
    exemplos = [
        'exemplos/01_hello.txt',
        'exemplos/02_soma.txt',
        'exemplos/03_condicional.txt',
        'exemplos/04_loop.txt',
        'exemplos/05_operacoes.txt'
    ]
    
    for exemplo in exemplos:
        if os.path.exists(exemplo):
            print_ok(f"Exemplo: {exemplo}")
        else:
            print_error(f"Exemplo faltando: {exemplo}")
            errors.append(f"Exemplo {exemplo}")
    
    # 4. Verificar importações
    print("\n4. Verificando módulos Python...")
    try:
        sys.path.insert(0, 'lexer')
        sys.path.insert(0, 'parser')
        
        import lexer_enhanced
        print_ok("lexer_enhanced.py importado")
        
        import parser
        print_ok("parser.py importado")
        
        import semantic_analyzer
        print_ok("semantic_analyzer.py importado")
        
        import code_generator
        print_ok("code_generator.py importado")
        
        import ast_nodes
        print_ok("ast_nodes.py importado")
        
        import symbol_table
        print_ok("symbol_table.py importado")
        
    except ImportError as e:
        print_error(f"Erro ao importar módulo: {e}")
        errors.append(f"Import: {e}")
    
    # 5. Verificar LLVM (opcional)
    print("\n5. Verificando LLVM (opcional)...")
    try:
        result = subprocess.run(['lli', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=2)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_ok(f"LLVM instalado: {version_line}")
        else:
            print_warning("lli encontrado mas retornou erro")
            warnings.append("LLVM")
    except FileNotFoundError:
        print_warning("LLVM não instalado (opcional - para executar código)")
        warnings.append("LLVM não instalado")
    except:
        print_warning("Erro ao verificar LLVM")
        warnings.append("LLVM")
    
    # 6. Testar compilação
    print("\n6. Testando compilação...")
    try:
        if os.path.exists('exemplos/01_hello.txt'):
            # Remover arquivo .ll se existir
            if os.path.exists('exemplos/01_hello.ll'):
                os.remove('exemplos/01_hello.ll')
            
            result = subprocess.run(
                [sys.executable, 'compile.py', 'exemplos/01_hello.txt'],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            
            # Verificar se o arquivo .ll foi gerado (melhor indicador de sucesso)
            if os.path.exists('exemplos/01_hello.ll'):
                print_ok("Teste de compilação passou!")
                print_ok("Arquivo .ll gerado com sucesso")
            else:
                print_error("Arquivo .ll não foi gerado")
                if result.stdout:
                    print(f"  Saída: {result.stdout[:300]}")
                errors.append("Geração de .ll")
        else:
            print_warning("Arquivo de teste não encontrado")
            warnings.append("Arquivo de teste")
    except subprocess.TimeoutExpired:
        print_error("Timeout ao testar compilação")
        errors.append("Timeout compilação")
    except Exception as e:
        print_error(f"Erro ao testar compilação: {e}")
        errors.append(f"Teste: {e}")
    
    # 7. Resultado final
    print_header("RESULTADO DA VERIFICAÇÃO")
    
    if not errors:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n🚀 O compilador está pronto para uso!")
        print("\nPara começar:")
        print("  python compile.py exemplos/02_soma.txt")
        print("  python compile.py --help")
        print("\nConsulte MANUAL_USO.md para mais informações.")
    else:
        print(f"\n❌ {len(errors)} erro(s) encontrado(s):")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print(f"\n⚠ {len(warnings)} aviso(s):")
        for warning in warnings:
            print(f"  • {warning}")
    
    print("\n" + "="*60)
    
    return 0 if not errors else 1

if __name__ == '__main__':
    sys.exit(main())
