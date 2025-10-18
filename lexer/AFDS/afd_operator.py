from afd_base import AFD

class AFDOperator(AFD):
    """
    AFD para reconhecer operadores da linguagem.
    A estrutura é gerada dinamicamente para lidar com operadores
    compostos e o princípio do "maior match".
    """
    def __init__(self):
        operators = {
            '==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '*=', '/=', 
            '%=', '<<=', '>>=', '&=', '|=', '^=', '=>', '->', '::',
            '+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~', '?', ':'
        }
        
        # Ordenar por tamanho decrescente para garantir o "maior match" na construção
        sorted_operators = sorted(list(operators), key=len, reverse=True)
        
        states = {'q0'}
        initial_state = 'q0'
        final_states = set()
        transitions = {'q0': {}}
        alphabet = set()

        # Constrói a árvore de transições
        for op in sorted_operators:
            current_state = 'q0'
            for i, char in enumerate(op):
                alphabet.add(char)
                # O nome do estado é o prefixo do operador
                next_state_name = op[:i+1]
                
                if char not in transitions.get(current_state, {}):
                    states.add(next_state_name)
                    if current_state not in transitions:
                        transitions[current_state] = {}
                    transitions[current_state][char] = next_state_name
                
                current_state = next_state_name
            
            # Todos os estados que representam um operador válido são finais
            final_states.add(current_state)
            
        super().__init__(states, alphabet, transitions, initial_state, final_states)