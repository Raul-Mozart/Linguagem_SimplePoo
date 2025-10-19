"""
Lexer integrado usando o AFD combinado criado a partir do AFN.
Este arquivo demonstra como usar o AFD combinado para análise lexical.
"""

from afn import nfa_to_dfa, combine_afds_to_nfa
from afd_ident import AFDIdent
from afd_number import AFDNumber
from afd_keyword import AFDKeyword
from afd_operator import AFDOperator
from afd_string import AFDString
from afd_comment import AFDComment
from afd_delimiters import AFDDelimiters
from afd_whitespace import AFDWhitespace

class LexerIntegrado:
    """
    Lexer que utiliza o AFD combinado para análise lexical.
    """
    
    def __init__(self):
        """Inicializa o lexer criando o AFD combinado."""
        self._create_combined_afd()
    
    def _create_combined_afd(self):
        """Cria o AFD combinado a partir dos AFDs individuais."""
        # AFDs individuais
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

        # Tipos de token correspondentes
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

        # Prioridades (menor valor = maior prioridade)
        self.token_priority = {
            "COMMENT": 1,
            "STRING": 2,
            "KEYWORD": 3,
            "NUMBER": 4,
            "IDENTIFIER": 5,
            "OPERATOR": 6,
            "DELIMITER": 7,
            "WHITESPACE": 8
        }

        # Cria AFN e converte para AFD
        nfa = combine_afds_to_nfa(afds, token_types)
        self.afd, self.afd_rev = nfa_to_dfa(nfa, self.token_priority)
        
        print(f"Lexer inicializado com AFD de {len(self.afd.states)} estados")

    def _get_token_type(self, text):
        """
        Determina o tipo de token para um texto dado.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            str or None: Tipo do token ou None se não reconhecido
        """
        if not self.afd.accepts(text):
            return None
        
        # Percorre o AFD para encontrar o estado final
        current_state = self.afd.initial_state
        for char in text:
            if char in self.afd.transitions.get(current_state, {}):
                current_state = self.afd.transitions[current_state][char]
            else:
                return None
        
        # Retorna o tipo de token associado ao estado final
        if (hasattr(self.afd, 'token_finals') and 
            current_state in self.afd.token_finals):
            return self.afd.token_finals[current_state]
        
        return None

    def tokenize(self, text, skip_whitespace=True):
        """
        Realiza análise lexical de um texto.
        
        Args:
            text (str): Texto a ser analisado
            skip_whitespace (bool): Se True, pula tokens de whitespace
            
        Returns:
            list: Lista de tokens encontrados
        """
        tokens = []
        i = 0
        line = 1
        column = 1
        
        while i < len(text):
            best_match = None
            best_length = 0
            best_token_type = None
            
            # Busca pelo maior match possível a partir da posição atual
            for j in range(i + 1, len(text) + 1):
                substring = text[i:j]
                token_type = self._get_token_type(substring)
                
                if token_type:
                    # Encontrou um match válido
                    if j - i > best_length:
                        best_match = substring
                        best_length = j - i
                        best_token_type = token_type
                    elif j - i == best_length and token_type in self.token_priority:
                        # Mesmo tamanho, usa prioridade
                        if (best_token_type not in self.token_priority or 
                            self.token_priority[token_type] < self.token_priority[best_token_type]):
                            best_match = substring
                            best_token_type = token_type
            
            if best_match:
                # Encontrou um token válido
                if not skip_whitespace or best_token_type != "WHITESPACE":
                    tokens.append({
                        'type': best_token_type,
                        'value': best_match,
                        'line': line,
                        'column': column
                    })
                
                # Atualiza posição
                for char in best_match:
                    if char == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                
                i += best_length
            else:
                # Caractere não reconhecido
                tokens.append({
                    'type': 'ERROR',
                    'value': text[i],
                    'line': line,
                    'column': column,
                    'message': f'Caractere não reconhecido: {text[i]!r}'
                })
                
                if text[i] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                
                i += 1
        
        return tokens

    def analyze_text(self, text):
        """
        Analisa um texto e imprime os tokens encontrados.
        
        Args:
            text (str): Texto a ser analisado
        """
        print(f"=== ANÁLISE LEXICAL ===")
        print(f"Texto: {text!r}")
        print()
        
        tokens = self.tokenize(text)
        
        print(f"{'Tipo':<12} {'Valor':<20} {'Linha':<6} {'Coluna':<6}")
        print("-" * 50)
        
        for token in tokens:
            print(f"{token['type']:<12} {token['value']!r:<20} {token['line']:<6} {token['column']:<6}")
        
        print(f"\nTotal de tokens: {len(tokens)}")

def main():
    """Função principal de demonstração."""
    lexer = LexerIntegrado()
    
    # Exemplos de teste
    test_programs = [
        # Programa simples
        '''class MinhaClasse {
            function teste() {
                var x = 123;
                var nome = "Hello World";
                return x + 42;
            }
        }''',
        
        # Expressões matemáticas
        'x = 10.5 + 2.3e-4 * (y - 1);',
        
        # Comentários
        '''// Comentário de linha
        /* Comentário
           de bloco */ 
        var z = 0;''',
        
        # Operadores diversos
        'if (a == b && c != d) { x++; }',
    ]
    
    for i, program in enumerate(test_programs, 1):
        print(f"\n{'='*60}")
        print(f"EXEMPLO {i}")
        print(f"{'='*60}")
        lexer.analyze_text(program)

if __name__ == "__main__":
    main()