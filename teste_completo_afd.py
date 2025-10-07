#!/usr/bin/env python3
"""
Script de Teste Completo - Analisador Léxico com AFD

Este script demonstra o funcionamento completo do sistema:
1. Conversão AFN → AFD (Algoritmo de Construção de Subconjuntos)
2. Analisador Léxico usando AFDs
3. Geração de diagramas Mermaid

Autor: Sistema de Compiladores
Data: 2025
"""

import sys
import os

# Adicionar paths necessários
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src/lexer'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Compiladores'))

from lexer import AnalisadorLexico, imprimir_resultado, Token
from afn_to_afd import *


def linha_separadora(titulo: str = "", char: str = "="):
    """Imprime linha separadora com título opcional"""
    largura = 70
    if titulo:
        padding = (largura - len(titulo) - 2) // 2
        print(f"\n{char * padding} {titulo} {char * padding}")
    else:
        print(char * largura)


def teste_1_construcao_subconjuntos():
    """Teste 1: Demonstra o Algoritmo de Construção de Subconjuntos"""
    linha_separadora("TESTE 1: ALGORITMO DE CONSTRUÇÃO DE SUBCONJUNTOS")
    
    print("\n📚 Teoria:")
    print("O algoritmo converte um AFN em AFD através de:")
    print("  1. Cálculo de fechamento-epsilon")
    print("  2. Construção de estados como subconjuntos")
    print("  3. Determinização das transições")
    
    print("\n🔧 Exemplo: AFN reconhecendo 'ab*' (a seguido de zero ou mais b)")
    
    # Criar AFN
    q0 = EstadoAFN(id=0)
    q1 = EstadoAFN(id=1)
    q2 = EstadoAFN(id=2)
    
    # Transições: q0 --a--> q1 --b--> q2 (loop em q2)
    q0.transicoes[frozenset(['a'])] = {q1}
    q1.transicoes[frozenset(['b'])] = {q2}
    q2.transicoes[frozenset(['b'])] = {q2}  # b* (zero ou mais)
    
    afn = AFN(estado_inicial=q0, estado_final=q2)
    
    print("\nAFN criado:")
    print("  Estados: q0, q1, q2")
    print("  Inicial: q0")
    print("  Final: q2")
    print("  Transições:")
    print("    q0 --[a]--> q1")
    print("    q1 --[b]--> q2")
    print("    q2 --[b]--> q2 (loop)")
    
    # Converter para AFD
    alfabeto = ['a', 'b']
    afd = construir_afd(afn, alfabeto)
    
    print("\n✅ AFD construído com sucesso!")
    print(f"  - Estados: {afd.numero_estados()}")
    print(f"  - Estado inicial: {afd.estado_inicial}")
    print(f"  - Estados de aceitação: {sorted(afd.estados_aceitacao)}")
    
    # Mostrar tabela de transições
    print("\n📊 Tabela de Transições:")
    for estado in sorted(afd.tabela_transicoes.keys()):
        transicoes = afd.tabela_transicoes[estado]
        marcador = " (FINAL)" if estado in afd.estados_aceitacao else ""
        print(f"  q{estado}{marcador}:")
        for simbolo in sorted(transicoes.keys()):
            destino = transicoes[simbolo]
            print(f"    '{simbolo}' → q{destino}")
    
    # Testar palavras
    print("\n🧪 Testes de Aceitação:")
    testes = [
        ("a", True),
        ("ab", True),
        ("abb", True),
        ("abbb", True),
        ("b", False),
        ("ba", False),
        ("", False),
        ("aa", False),
    ]
    
    sucessos = 0
    for palavra, esperado in testes:
        resultado = afd.aceita(palavra)
        status = "✅" if resultado == esperado else "❌"
        esperado_str = "ACEITA" if esperado else "REJEITA"
        resultado_str = "ACEITA" if resultado else "REJEITA"
        print(f"  {status} '{palavra}' → {resultado_str} (esperado: {esperado_str})")
        if resultado == esperado:
            sucessos += 1
    
    print(f"\n📈 Resultado: {sucessos}/{len(testes)} testes corretos")
    
    # Gerar diagrama Mermaid
    print("\n🎨 Diagrama Mermaid do AFD:")
    print(afd_para_mermaid(afd))
    
    return afd


def teste_2_analisador_lexico():
    """Teste 2: Demonstra o Analisador Léxico completo"""
    linha_separadora("TESTE 2: ANALISADOR LÉXICO COM AFD")
    
    print("\n📚 Teoria:")
    print("O analisador léxico usa múltiplos AFDs em paralelo:")
    print("  1. Compila cada regex de token para um AFD")
    print("  2. Tenta match com todos os AFDs")
    print("  3. Escolhe o match mais longo (Maximal Munch)")
    print("  4. Aplica priorização (keywords > identificadores)")
    
    print("\n🔧 Criando Analisador...")
    lexer = AnalisadorLexico()
    
    print(f"\n✅ Analisador criado com {len(lexer.afds)} AFDs compilados")
    
    # Teste com código válido
    linha_separadora("2.1: Código Válido", "-")
    
    codigo_valido = """
var int contador as 0;
var float pi as 3.14159;
var string mensagem as "Olá, Mundo!";

if (contador < 10) {
    contador = contador + 1;
}

for i in 0..5 {
    print(i);
}
"""
    
    print("\n📄 Código de entrada:")
    print("-" * 70)
    print(codigo_valido)
    print("-" * 70)
    
    resultado = lexer.analisar(codigo_valido)
    
    if resultado.sucesso:
        print(f"\n✅ Análise SUCESSO! {len(resultado.tokens)} tokens identificados")
        print("\n📋 Primeiros 20 tokens:")
        for i, token in enumerate(resultado.tokens[:20], 1):
            print(f"  {i:2}. {token.tipo:15} '{token.lexema:15}' @ {token.linha}:{token.coluna}")
        
        if len(resultado.tokens) > 20:
            print(f"  ... e mais {len(resultado.tokens) - 20} tokens")
        
        # Estatísticas
        tipos_tokens = {}
        for token in resultado.tokens:
            tipos_tokens[token.tipo] = tipos_tokens.get(token.tipo, 0) + 1
        
        print("\n📊 Estatísticas de Tokens:")
        for tipo in sorted(tipos_tokens.keys()):
            count = tipos_tokens[tipo]
            barra = "█" * (count // 2 + 1)
            print(f"  {tipo:15}: {count:3} {barra}")
    
    # Teste com código inválido
    linha_separadora("2.2: Código com Erros Léxicos", "-")
    
    codigo_invalido = """
var int x as 10;
var string y as "teste";
x = x @ 5;  // @ é caractere inválido
y = # erro;  // # também
$invalido = 10;
"""
    
    print("\n📄 Código com erros:")
    print("-" * 70)
    print(codigo_invalido)
    print("-" * 70)
    
    resultado_erro = lexer.analisar(codigo_invalido)
    
    print(f"\n❌ Análise encontrou {len(resultado_erro.erros)} erro(s) léxico(s):")
    for erro in resultado_erro.erros:
        print(f"  • Linha {erro.linha}, Coluna {erro.coluna}: {erro.mensagem}")
        print(f"    Caractere: '{erro.caractere}'")
    
    print(f"\n✅ Mesmo com erros, {len(resultado_erro.tokens)} tokens foram identificados")


def teste_3_tokens_especificos():
    """Teste 3: Testa categorias específicas de tokens"""
    linha_separadora("TESTE 3: CATEGORIAS ESPECÍFICAS DE TOKENS")
    
    lexer = AnalisadorLexico()
    
    casos_teste = [
        ("Keywords", "if else for while var function class return"),
        ("Identificadores", "x variavel _temp contador123 _privado"),
        ("Números", "0 42 123 3.14 2.5 1.0e5"),
        ("Strings", '"hello" "mundo" "João" "São Paulo"'),
        ("Operadores", "+ - * / = == != < > <= >="),
        ("Delimitadores", "( ) { } [ ] ; , . :"),
        ("Range", "0..10 1..100"),
    ]
    
    for nome, codigo in casos_teste:
        print(f"\n📦 {nome}:")
        print(f"   Input: {codigo}")
        
        resultado = lexer.analisar(codigo)
        tokens_str = ", ".join([f"{t.tipo}('{t.lexema}')" for t in resultado.tokens])
        print(f"   Tokens: {tokens_str}")
        
        if resultado.erros:
            print(f"   ⚠️  Erros: {len(resultado.erros)}")


def teste_4_prioridade_tokens():
    """Teste 4: Demonstra priorização de tokens"""
    linha_separadora("TESTE 4: PRIORIZAÇÃO DE TOKENS")
    
    print("\n📚 Teoria:")
    print("Quando múltiplos AFDs fazem match, o sistema prioriza:")
    print("  1. Match mais longo (Maximal Munch)")
    print("  2. Tipo de token (keywords > identificadores)")
    
    lexer = AnalisadorLexico()
    
    casos = [
        ("var", "Keyword 'var' tem prioridade sobre identificador"),
        ("variavel", "Identificador (não é keyword)"),
        ("if", "Keyword 'if'"),
        ("ifx", "Identificador (não é keyword exata)"),
        ("123", "Inteiro"),
        ("123.45", "Float (match mais longo que int)"),
    ]
    
    print("\n🧪 Casos de Teste:")
    for input_str, descricao in casos:
        resultado = lexer.analisar(input_str)
        if resultado.tokens:
            token = resultado.tokens[0]
            print(f"  '{input_str:10}' → {token.tipo:15} | {descricao}")


def teste_5_desempenho():
    """Teste 5: Avalia desempenho do analisador"""
    linha_separadora("TESTE 5: ANÁLISE DE DESEMPENHO")
    
    import time
    
    lexer = AnalisadorLexico()
    
    # Código de teste grande
    codigo_grande = """
var int x as 0;
var float y as 0.0;
for i in 0..1000 {
    x = x + 1;
    y = y + 0.5;
    if (x > 100) {
        x = 0;
    }
}
""" * 10  # Repetir 10 vezes
    
    print(f"\n📏 Tamanho do código: {len(codigo_grande)} caracteres")
    print(f"   Linhas: ~{codigo_grande.count(chr(10))}")
    
    print("\n⏱️  Executando análise...")
    inicio = time.time()
    resultado = lexer.analisar(codigo_grande)
    fim = time.time()
    
    tempo = (fim - inicio) * 1000  # em milissegundos
    
    print(f"\n✅ Análise concluída!")
    print(f"   Tempo: {tempo:.2f} ms")
    print(f"   Tokens: {len(resultado.tokens)}")
    print(f"   Velocidade: {len(codigo_grande) / tempo * 1000:.0f} chars/segundo")
    print(f"   Throughput: {len(resultado.tokens) / tempo * 1000:.0f} tokens/segundo")


def menu_principal():
    """Menu interativo para executar testes"""
    linha_separadora("SISTEMA DE TESTES - ANALISADOR LÉXICO")
    
    print("\n🎯 Testes Disponíveis:\n")
    print("  1. Algoritmo de Construção de Subconjuntos (AFN → AFD)")
    print("  2. Analisador Léxico Completo")
    print("  3. Tokens Específicos por Categoria")
    print("  4. Priorização de Tokens")
    print("  5. Análise de Desempenho")
    print("  6. Executar TODOS os testes")
    print("  0. Sair")
    
    while True:
        print("\n" + "="*70)
        escolha = input("Escolha um teste (0-6): ").strip()
        
        if escolha == "0":
            print("\n👋 Encerrando...")
            break
        elif escolha == "1":
            teste_1_construcao_subconjuntos()
        elif escolha == "2":
            teste_2_analisador_lexico()
        elif escolha == "3":
            teste_3_tokens_especificos()
        elif escolha == "4":
            teste_4_prioridade_tokens()
        elif escolha == "5":
            teste_5_desempenho()
        elif escolha == "6":
            teste_1_construcao_subconjuntos()
            teste_2_analisador_lexico()
            teste_3_tokens_especificos()
            teste_4_prioridade_tokens()
            teste_5_desempenho()
            linha_separadora("TODOS OS TESTES CONCLUÍDOS")
            print("\n✅ Bateria completa de testes executada com sucesso!")
        else:
            print("❌ Opção inválida! Escolha entre 0 e 6.")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     ANALISADOR LÉXICO - IMPLEMENTAÇÃO COM AFD                    ║
║     Baseado em Teoria de Autômatos e Linguagens Formais          ║
║                                                                   ║
║     Recursos:                                                     ║
║       • Algoritmo de Construção de Subconjuntos (AFN → AFD)      ║
║       • Analisador Léxico com Maximal Munch                      ║
║       • Suporte a 22 categorias de tokens                        ║
║       • Tratamento de erros léxicos                              ║
║       • Geração de diagramas Mermaid                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
