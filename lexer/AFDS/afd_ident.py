from afd_base import AFD
import string

class AFDIdent(AFD):
    """
    AFD para reconhecer identificadores.
    Regex: [A-Za-z_][A-Za-z0-9_]*
    """
    def __init__(self):
        # Definição do alfabeto
        letters_ = string.ascii_letters + '_'
        alphanumeric_ = string.ascii_letters + string.digits + '_'
        
        alphabet = set(alphanumeric_)
        
        # Definição dos estados
        states = {'q0', 'q1'}
        initial_state = 'q0'
        final_states = {'q1'}
        
        # Definição das transições
        transitions = {
            'q0': {char: 'q1' for char in letters_},
            'q1': {char: 'q1' for char in alphanumeric_}
        }
        
        super().__init__(states, alphabet, transitions, initial_state, final_states)