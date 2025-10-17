from .afd_base import AFD

class AFDKeyword(AFD):
    """
    AFD para reconhecer palavras-chave da linguagem.
    A estrutura é gerada dinamicamente a partir da lista de palavras-chave.
    """
    def __init__(self):
        keywords = {
            'class', 'struct', 'interface', 'extends', 'implements', 'new', 
            'this', 'super', 'function', 'void', 'var', 'let', 'const', 'return', 
            'if', 'else', 'switch', 'case', 'default', 'break', 'continue', 'for', 
            'foreach', 'while', 'do', 'true', 'false', 'null', 'public', 'private', 
            'protected', 'static', 'int', 'float', 'string', 'bool', 'list', 'dict'
        }

        states = {'q0'}
        initial_state = 'q0'
        final_states = set()
        transitions = {'q0': {}}
        alphabet = set()

        # Constrói a árvore de transições (Trie)
        for keyword in keywords:
            current_state = 'q0'
            for i, char in enumerate(keyword):
                alphabet.add(char)
                next_state_name = f'{current_state}_{char}'
                
                if char not in transitions.get(current_state, {}):
                    states.add(next_state_name)
                    if current_state not in transitions:
                        transitions[current_state] = {}
                    transitions[current_state][char] = next_state_name
                
                current_state = next_state_name
            
            # O último estado de uma palavra-chave é um estado final
            final_states.add(current_state)

        super().__init__(states, alphabet, transitions, initial_state, final_states)