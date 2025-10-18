from afd_base import AFD
import string

class AFDErrorLex(AFD):
    """
    AFD conceitual para representar um erro léxico.
    Na prática, o analisador léxico principal identifica um erro quando
    nenhum outro AFD consegue consumir a entrada. Este AFD aceita
    qualquer caractere único do alfabeto da linguagem.
    """
    def __init__(self):
        # Constrói o alfabeto completo da linguagem Σ
        alphabet = set(string.ascii_letters + string.digits + 
                       '_+-*/%=<>!&|^~?:.,;()[]{} "\'`\\ \t\n\r')
        
        states = {'q0', 'q1'}
        initial_state = 'q0'
        final_states = {'q1'}
        
        # Aceita qualquer caractere único e para
        transitions = {
            'q0': {char: 'q1' for char in alphabet}
        }
        
        super().__init__(states, alphabet, transitions, initial_state, final_states)