from afd_base import AFD

class AFDWhitespace(AFD):
    """
    AFD para reconhecer sequências de espaço em branco.
    Regex: [ \t\r\n]+
    """
    def __init__(self):
        whitespace_chars = {' ', '\t', '\r', '\n'}
        
        alphabet = whitespace_chars
        states = {'q0', 'q1'}
        initial_state = 'q0'
        final_states = {'q1'}
        
        transitions = {
            'q0': {char: 'q1' for char in whitespace_chars},
            'q1': {char: 'q1' for char in whitespace_chars},
        }
        
        super().__init__(states, alphabet, transitions, initial_state, final_states)