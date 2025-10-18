from afd_base import AFD

class AFDDelimiters(AFD):
    """
    AFD para reconhecer delimitadores de caractere único.
    """
    def __init__(self):
        delimiters = {'(', ')', '{', '}', '[', ']', ';', ',', '.'}
        
        alphabet = delimiters
        states = {'q0', 'q1'}
        initial_state = 'q0'
        final_states = {'q1'}
        
        transitions = {
            'q0': {char: 'q1' for char in delimiters}
        }
        
        super().__init__(states, alphabet, transitions, initial_state, final_states)