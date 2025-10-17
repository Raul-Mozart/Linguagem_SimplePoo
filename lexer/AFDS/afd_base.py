class AFD:
    """
    Classe base para um Autômato Finito Determinístico (AFD).
    """
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        """
        Inicializa o AFD.

        Args:
            states (set): O conjunto de estados.
            alphabet (set): O conjunto de símbolos do alfabeto.
            transitions (dict): A função de transição, representada como um
                                dicionário de dicionários. Ex: {'q0': {'a': 'q1'}}.
            initial_state (str): O estado inicial.
            final_states (set): O conjunto de estados de aceitação.
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.current_state = self.initial_state

    def process_string(self, input_string: str) -> bool:
        """
        Processa uma cadeia de entrada e verifica se ela é aceita pelo autômato.

        Args:
            input_string (str): A cadeia a ser processada.

        Returns:
            bool: True se a cadeia é aceita, False caso contrário.
        """
        self.current_state = self.initial_state
        for char in input_string:
            if char not in self.alphabet:
                self.current_state = None  # Caractere inválido
                break
            
            # Obtém o próximo estado da tabela de transições
            self.current_state = self.transitions.get(self.current_state, {}).get(char)

            if self.current_state is None:
                # Nenhuma transição definida para o estado/caractere atual
                break
        
        return self.current_state in self.final_states

    def accepts(self, input_string: str) -> bool:
        """
        Método alias para process_string.
        """
        return self.process_string(input_string)