from afd_base import AFD
import string

class AFDNumber(AFD):
    """
    AFD para reconhecer literais numéricos (inteiros, decimais, científicos).
    Regex: \d+(\.\d+)?([eE][+-]?\d+)?
    """
    def __init__(self):
        digits = set(string.digits)
        signs = {'+', '-'}
        exponents = {'e', 'E'}
        dot = {'.'}

        alphabet = digits | signs | exponents | dot

        states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
        initial_state = 'q0'
        final_states = {'q1', 'q3', 'q6'}

        transitions = {
            'q0': {d: 'q1' for d in digits},
            'q1': {d: 'q1' for d in digits},
            'q2': {d: 'q3' for d in digits},
            'q3': {d: 'q3' for d in digits},
            'q4': {s: 'q5' for s in signs},
            'q5': {d: 'q6' for d in digits},
            'q6': {d: 'q6' for d in digits},
        }

        transitions['q1']['.'] = 'q2'
        transitions['q1'].update({e: 'q4' for e in exponents})
        transitions['q3'].update({e: 'q4' for e in exponents})
        transitions['q4'].update({d: 'q6' for d in digits})

        super().__init__(states, alphabet, transitions, initial_state, final_states)