from afn import nfa_to_dfa, combine_afds_to_nfa
from afd_ident import AFDIdent
from afd_number import AFDNumber
from afd_keyword import AFDKeyword
from afd_operator import AFDOperator
from afd_string import AFDString
from afd_comment import AFDComment
from afd_delimiters import AFDDelimiters
from afd_whitespace import AFDWhitespace

def test_combined_afd():
    """
    Testa o AFD combinado com várias cadeias de entrada.
    """
    # Cria os AFDs individuais
    afds = [
        AFDComment(),
        AFDString(),
        AFDNumber(),
        AFDKeyword(),
        AFDIdent(),
        AFDOperator(),
        AFDDelimiters(),
        AFDWhitespace()
    ]

    token_types = [
        "COMMENT",
        "STRING", 
        "NUMBER",
        "KEYWORD",
        "IDENTIFIER",
        "OPERATOR",
        "DELIMITER",
        "WHITESPACE"
    ]

    token_priority = {
        "COMMENT": 1,
        "STRING": 2,
        "KEYWORD": 3,
        "NUMBER": 4,
        "IDENTIFIER": 5,
        "OPERATOR": 6,
        "DELIMITER": 7,
        "WHITESPACE": 8
    }

    # Cria o AFN e converte para AFD
    print("Criando AFN e convertendo para AFD...")
    nfa = combine_afds_to_nfa(afds, token_types)
    dfa, dfa_rev = nfa_to_dfa(nfa, token_priority)
    print(f"AFD criado com {len(dfa.states)} estados\n")

    # Casos de teste
    test_cases = [
        # Identificadores
        ("variavel", "IDENTIFIER"),
        ("_temp", "IDENTIFIER"),
        ("valor123", "IDENTIFIER"),
        
        # Palavras-chave
        ("class", "KEYWORD"),
        ("if", "KEYWORD"),
        ("function", "KEYWORD"),
        ("return", "KEYWORD"),
        
        # Números
        ("123", "NUMBER"),
        ("45.67", "NUMBER"),
        ("1.23e-4", "NUMBER"),
        ("2E10", "NUMBER"),
        
        # Strings
        ('"Hello World"', "STRING"),
        ("'teste'", "STRING"),
        ('""', "STRING"),
        
        # Operadores
        ("++", "OPERATOR"),
        ("==", "OPERATOR"),
        ("<=", "OPERATOR"),
        ("->", "OPERATOR"),
        ("+", "OPERATOR"),
        
        # Delimitadores
        ("(", "DELIMITER"),
        (")", "DELIMITER"),
        ("{", "DELIMITER"),
        (";", "DELIMITER"),
        
        # Comentários
        ("// comentario de linha", "COMMENT"),
        ("/* comentario de bloco */", "COMMENT"),
        
        # Whitespace
        (" ", "WHITESPACE"),
        ("\t", "WHITESPACE"),
        ("\n", "WHITESPACE"),
    ]

    print("=== TESTES DO AFD COMBINADO ===\n")
    
    passed = 0
    total = len(test_cases)
    
    for test_string, expected_token in test_cases:
        # Testa se a string é aceita pelo AFD
        is_accepted = dfa.accepts(test_string)
        
        if is_accepted:
            # Descobre qual token foi reconhecido
            current_state = dfa.initial_state
            for char in test_string:
                if char in dfa.transitions.get(current_state, {}):
                    current_state = dfa.transitions[current_state][char]
                else:
                    current_state = None
                    break
            
            recognized_token = None
            if current_state and hasattr(dfa, 'token_finals') and current_state in dfa.token_finals:
                recognized_token = dfa.token_finals[current_state]
            
            if recognized_token == expected_token:
                status = "✅ PASS"
                passed += 1
            else:
                status = f"❌ FAIL (esperado: {expected_token}, obtido: {recognized_token})"
        else:
            status = f"❌ FAIL (string rejeitada, esperado: {expected_token})"
        
        print(f"{test_string:<25} → {status}")
    
    print(f"\n=== RESULTADO ===")
    print(f"Testes passaram: {passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")

    return dfa, dfa_rev

if __name__ == "__main__":
    dfa, dfa_rev = test_combined_afd()