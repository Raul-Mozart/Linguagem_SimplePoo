from .afd_base import AFD

class AFDComment(AFD):
    """
    AFD para reconhecer comentários de linha e de bloco.
    """
    def __init__(self):
        alphabet = set(map(chr, range(9, 127))) # Tab, NL, CR e imprimíveis

        states = {'q0', 'q1', 'q2_line', 'q3_block_start', 'q4_block_end', 'q5_final'}
        initial_state = 'q0'
        final_states = {'q2_line', 'q5_final'}

        # Transições comuns
        transitions = {
            'q0': {'/': 'q1'},
        }

        # Lógica de comentário de linha (termina com \n, que é tratado pelo lexer)
        transitions['q1'] = {'/': 'q2_line'}
        transitions['q2_line'] = {char: 'q2_line' for char in alphabet if char != '\n'}

        # Lógica de comentário de bloco
        transitions['q1']['*'] = 'q3_block_start'
        transitions['q3_block_start'] = {char: 'q3_block_start' for char in alphabet if char != '*'}
        transitions['q3_block_start']['*'] = 'q4_block_end'
        
        transitions['q4_block_end'] = {char: 'q3_block_start' for char in alphabet if char != '/'}
        transitions['q4_block_end']['*'] = 'q4_block_end' # Suporta múltiplos * como em /***/
        transitions['q4_block_end']['/'] = 'q5_final'

        super().__init__(states, alphabet, transitions, initial_state, final_states)