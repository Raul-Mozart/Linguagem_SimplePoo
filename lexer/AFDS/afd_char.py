from afd_base import AFD

class AFDChar(AFD):
    """
    AFD para reconhecer literais de caractere.
    Regex: '(?:\\.|[^'\\])'
    """
    def __init__(self):
        alphabet = set(map(chr, range(32, 127)))
        
        states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
        initial_state = 'q0'
        final_states = {'q5'}

        transitions = {
            'q0': {"'": 'q1'},
            'q1': {char: 'q2' for char in alphabet if char not in ["'", '\\']},
            'q2': {"'": 'q5'},
            'q3': {char: 'q4' for char in alphabet},
            'q4': {"'": 'q5'},
        }
        transitions['q1']['\\'] = 'q3'

        super().__init__(states, alphabet, transitions, initial_state, final_states)