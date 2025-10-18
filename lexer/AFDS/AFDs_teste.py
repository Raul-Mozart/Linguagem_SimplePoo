from afd_base import AFD
from afd_ident import AFDIdent
from afd_keyword import AFDKeyword
from afd_number import AFDNumber
from afd_string import AFDString
from afd_char import AFDChar
from afd_comment import AFDComment
from afd_operator import AFDOperator
from afd_delimiters import AFDDelimiters
from afd_whitespace import AFDWhitespace
from afd_error_lex import AFDErrorLex

def run_test(afd_name: str, afd_instance: AFD, test_cases: list):
    """
    Função auxiliar para executar testes em uma instância de AFD.
    """
    print('-' * 40)
    print(f'Iniciando testes para: {afd_name}')
    print('-' * 40)
    
    passed = 0
    failed = 0
    
    for input_string, expected_result in test_cases:
        actual_result = afd_instance.process_string(input_string)
        
        if actual_result == expected_result:
            status = "[PASS]"
            passed += 1
        else:
            status = "[FAIL]"
            failed += 1
            
        print(f'{status} Entrada: "{input_string}" | Resultado: {actual_result} | Esperado: {expected_result}')
    
    print(f'\nResumo ({afd_name}): {passed} passaram, {failed} falharam.\n')

def test_afd_ident():
    """Testa o AFD para Identificadores."""
    afd = AFDIdent()
    test_cases = [
        # Casos Válidos
        ('a', True),
        ('variavel', True),
        ('var123', True),
        ('_underscore', True),
        ('__privateVar', True),
        ('VarCamelCase', True),
        
        # Casos Inválidos
        ('123var', False),
        ('!invalido', False),
        ('var-invalida', False),
        ('var invalida', False),
        ('', False),
        ('+', False)
    ]
    run_test("AFDIdent", afd, test_cases)

def test_afd_keyword():
    """Testa o AFD para Palavras-Chave."""
    afd = AFDKeyword()
    test_cases = [
        # Casos Válidos
        ('if', True),
        ('else', True),
        ('while', True),
        ('for', True),
        ('class', True),
        ('return', True),
        ('int', True),
        ('float', True),
        
        # Casos Inválidos (não são palavras-chave)
        ('iff', False),
        ('IF', False),
        ('forr', False),
        ('whilee', False),
        ('Class', False),
        ('variavel', False),
        ('123', False),
        ('', False)
    ]
    run_test("AFDKeyword", afd, test_cases)

def test_afd_number():
    """Testa o AFD para Números."""
    afd = AFDNumber()
    test_cases = [
        # Casos Válidos
        ('123', True),
        ('0', True),
        ('42.0', True),
        ('3.14159', True),
        ('1e10', True),
        ('1.5e+5', True),
        ('2.0e-10', True),
        
        # Casos Inválidos
        ('1.', False),       # Ponto sem dígito depois
        ('.5', False),       # Ponto sem dígito antes
        ('1e', False),       # 'e' sem expoente
        ('1e+', False),      # 'e' com sinal sem expoente
        ('1.2.3', False),    # Múltiplos pontos
        ('1e-e', False),
        ('abc', False),
        ('', False)
    ]
    run_test("AFDNumber", afd, test_cases)

def test_afd_string():
    """Testa o AFD para Strings."""
    afd = AFDString()
    test_cases = [
        # Casos Válidos
        ('""', True),
        ('"hello"', True),
        ('"com \\"escape\\""', True),
        ('"\\n\\t"', True),
        ("''", True),
        ("'world'", True),
        ("'com \\'escape\\''", True),
        
        # Casos Inválidos
        ('"nao fechada', False),
        ("'nao fechada", False),
        ('"', False),
        ("'", False),
        ('"aspas simples \'', False), # Não são do mesmo tipo
        ('', False)
    ]
    run_test("AFDString", afd, test_cases)

def test_afd_char():
    """Testa o AFD para Caracteres."""
    afd = AFDChar()
    test_cases = [
        # Casos Válidos
        ("'a'", True),
        ("'1'", True),
        ("' '", True),
        ("'\\n'", True),
        ("'\\t'", True),
        ("'\\\\'", True),
        
        # Casos Inválidos
        ("''", False),       # Vazio
        ("'ab'", False),     # Múltiplos caracteres
        ("'", False),       # Não fechado
        ("'a", False),      # Não fechado
        ('"a"', False)       # Aspas duplas
    ]
    run_test("AFDChar", afd, test_cases)

def test_afd_comment():
    """Testa o AFD para Comentários."""
    afd = AFDComment()
    test_cases = [
        # Casos Válidos
        ('// comentario de linha', True),
        ('//', True),
        ('/* comentario de bloco */', True),
        ('/**/', True),
        ('/* bloco \n com \n linhas */', True),
        
        # Casos Inválidos
        ('/', False),
        ('/a', False),
        ('/* bloco nao fechado', False),
        ('*/', False),
        ('', False)
    ]
    run_test("AFDComment", afd, test_cases)

def test_afd_operator():
    """Testa o AFD para Operadores."""
    afd = AFDOperator()
    test_cases = [
        # Casos Válidos
        ('+', True),
        ('++', True),
        ('+=', True),
        ('=', True),
        ('==', True),
        ('!', True),
        ('!=', True),
        ('->', True),
        ('::', True),
        
        # Casos Inválidos (incompletos ou não existem)
        ('+!', False),
        ('=>=', False),
        (':', True), 
        ('-', True),
        ('---', False), # Reconhece '--', mas o 3º '-' falha
        ('', False)
    ]
    run_test("AFDOperator", afd, test_cases)

def test_afd_delimiters():
    """Testa o AFD para Delimitadores."""
    afd = AFDDelimiters()
    test_cases = [
        # Casos Válidos
        ('(', True),
        (')', True),
        ('{', True),
        ('}', True),
        ('[', True),
        (']', True),
        (';', True),
        (',', True),
        ('.', True),
        
        # Casos Inválidos
        ('a', False),
        ('()', False), # Reconhece apenas um por vez
        ('+', False),
        ('', False)
    ]
    run_test("AFDDelimiters", afd, test_cases)

def test_afd_whitespace():
    """Testa o AFD para Espaço em Branco."""
    afd = AFDWhitespace()
    test_cases = [
        # Casos Válidos
        (' ', True),
        ('\t', True),
        ('\n', True),
        ('\r', True),
        (' \t \n \r ', True),
        
        # Casos Inválidos
        ('a', False),
        (' a', False), # O AFD só aceita espaço em branco
        ('', False)
    ]
    run_test("AFDWhitespace", afd, test_cases)

def test_afd_error_lex():
    """Testa o AFD para Erro Léxico."""
    afd = AFDErrorLex()
    test_cases = [
        # Casos Válidos (qualquer char do alfabeto)
        ('@', True),
        ('#', True),
        ('$', True),
        ('`', True),
        
        # Casos Inválidos
        ('abc', False), # Reconhece apenas um por vez
        ('', False)
    ]
    run_test("AFDErrorLex", afd, test_cases)

if __name__ == "__main__":
    print("=========================================")
    print("== EXECUTANDO TESTES DOS AFDs DO LEXER ==")
    print("=========================================\n")
    
    test_afd_ident()
    test_afd_keyword()
    test_afd_number()
    test_afd_string()
    test_afd_char()
    test_afd_comment()
    test_afd_operator()
    test_afd_delimiters()
    test_afd_whitespace()
    
    # O AFDErrorLex é conceitual, mas testamos sua implementação.
    # test_afd_error_lex() 
    
    print("\n=========================================")
    print("==        TESTES FINALIZADOS           ==")
    print("=========================================")