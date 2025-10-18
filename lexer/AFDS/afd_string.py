from afd_base import AFD

class AFDString(AFD):
    """
    AFD para reconhecer literais de string (aspas simples ou duplas).
    Regex: "(?:\\.|[^"\\])*" | '(?:\\.|[^'\\])*'
    """
    def __init__(self):
        # Alfabeto: qualquer caractere imprimível incluindo acentos + aspas e barra invertida
        alphabet = set(map(chr, range(32, 127)))  # ASCII imprimível
        # Adiciona caracteres acentuados comuns
        alphabet.update(map(chr, range(160, 256))) # Adiciona Bloco "Latin-1 Supplement" (inclui É, á, ç, ñ, ö, etc.)

        states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
        initial_state = 'q0'
        final_states = {'q3', 'q6'}

        # Transições para strings com aspas duplas
        t_double = {
            'q0': {'"': 'q1'},
            'q1': {char: 'q1' for char in alphabet if char not in ['"', '\\']},
            'q2': {char: 'q1' for char in alphabet},
        }
        t_double['q1']['\\'] = 'q2'
        t_double['q1']['"'] = 'q3'
        
        # Transições para strings com aspas simples
        t_single = {
            'q0': {"'": 'q4'},
            'q4': {char: 'q4' for char in alphabet if char not in ["'", '\\']},
            'q5': {char: 'q4' for char in alphabet},
        }
        t_single['q4']['\\'] = 'q5'
        t_single['q4']["'"] = 'q6'

        # Combina as transições
        transitions = {
            'q0': {**t_double['q0'], **t_single['q0']},
            'q1': t_double['q1'], 'q2': t_double['q2'],
            'q4': t_single['q4'], 'q5': t_single['q5'],
        }

        super().__init__(states, alphabet, transitions, initial_state, final_states)