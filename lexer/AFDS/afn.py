EPS = None  # símbolo para epsilon nas transições do NFA

from afd_base import AFD
from afd_ident import AFDIdent
from afd_number import AFDNumber
from afd_keyword import AFDKeyword
from afd_operator import AFDOperator
from afd_string import AFDString
from afd_comment import AFDComment
from afd_delimiters import AFDDelimiters
from afd_whitespace import AFDWhitespace

# --- Combinação AFDs -> AFN com mapeamento de token ---
def combine_afds_to_nfa(afds, token_types):
    """
    Combina múltiplos AFDs em um único AFN (Autômato Finito Não-determinístico)
    usando transições epsilon do estado inicial para cada AFD individual.
    
    Args:
        afds: Lista de instâncias de AFD
        token_types: Lista de strings com os tipos de token correspondentes
    
    Returns:
        dict: Representação do AFN com estados, alfabeto, transições, etc.
    """
    estados = set()
    alfabeto = set()
    transicoes = {}
    finais = set()
    token_map = {}  # estado final -> tipo de token

    start = "S_COMBINED"
    estados.add(start)
    transicoes[start] = {}

    for i, (afd, ttype) in enumerate(zip(afds, token_types)):
        prefix = f"A{i}_"  # prefixo para renomear estados e evitar conflitos
        
        # Renomeia todos os estados do AFD
        for s in afd.states:
            ns = prefix + s
            estados.add(ns)
            transicoes.setdefault(ns, {})

        # Coleta todos os símbolos do alfabeto
        for sym in afd.alphabet:
            alfabeto.add(sym)

        # Converte transições do AFD para o formato AFN
        for s, row in afd.transitions.items():
            ns = prefix + s
            for sym, dest in row.items():
                nd = prefix + dest
                transicoes[ns].setdefault(sym, set()).add(nd)

        # ligação por epsilon do estado inicial global para o inicial do afd
        transicoes[start].setdefault(EPS, set()).add(prefix + afd.initial_state)

        # marca estado final e mapeia tipo de token
        for f in afd.final_states:
            final_state = prefix + f
            finais.add(final_state)
            token_map[final_state] = ttype

    # Garante que todos os estados tenham entrada no dicionário de transições
    for s in list(estados):
        transicoes.setdefault(s, {})

    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "transicoes": transicoes,
        "inicial": start,
        "finais": finais,
        "token_map": token_map
    }

# --- Operações auxiliares para conversão AFN -> AFD ---
def epsilon_closure(states, trans):
    """
    Calcula o epsilon-fecho de um conjunto de estados.
    
    Args:
        states: Conjunto de estados
        trans: Dicionário de transições do AFN
    
    Returns:
        set: Estados alcançáveis através de transições epsilon
    """
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        eps_dests = trans.get(s, {}).get(EPS)
        if eps_dests:
            for d in eps_dests:
                if d not in closure:
                    closure.add(d)
                    stack.append(d)
    return closure

def move(states, symbol, trans):
    """
    Calcula o conjunto de estados alcançados a partir de um conjunto
    de estados através de um símbolo específico.
    
    Args:
        states: Conjunto de estados de origem
        symbol: Símbolo da transição
        trans: Dicionário de transições do AFN
    
    Returns:
        set: Estados de destino
    """
    resultados = set()
    for s in states:
        dests = trans.get(s, {}).get(symbol)
        if dests:
            resultados.update(dests)
    return resultados

# --- AFN -> AFD com prioridade de token ---
def nfa_to_dfa(nfa, token_priority):
    """
    Converte um AFN em AFD usando o algoritmo de construção de subconjuntos.
    
    Args:
        nfa: Dicionário representando o AFN
        token_priority: Dicionário com prioridades dos tokens (menor valor = maior prioridade)
    
    Returns:
        tuple: (AFD, mapeamento_reverso) onde AFD é uma instância da classe AFD
    """
    trans = nfa["transicoes"]
    alphabet = set(nfa["alfabeto"])
    start = nfa["inicial"]
    finals_nfa = nfa["finais"]
    token_map = nfa["token_map"]

    start_closure = frozenset(epsilon_closure({start}, trans))

    dfa_states_map = {start_closure: "D0"}
    dfa_rev = {"D0": start_closure}
    dfa_trans = {}
    dfa_finals = {}  # estado -> token_type
    queue = [start_closure]
    counter = 1

    while queue:
        T = queue.pop(0)
        T_name = dfa_states_map[T]
        dfa_trans[T_name] = {}

        # Se algum estado é final no NFA, define token com maior prioridade
        final_tokens = [token_map[s] for s in T if s in finals_nfa]
        if final_tokens:
            # escolher token com menor valor (maior prioridade)
            dfa_finals[T_name] = min(final_tokens, key=lambda t: token_priority[t])

        for a in sorted(alphabet):
            moved = move(T, a, trans)
            if not moved:
                continue
            closure = frozenset(epsilon_closure(moved, trans))
            if closure not in dfa_states_map:
                dfa_states_map[closure] = f"D{counter}"
                dfa_rev[f"D{counter}"] = closure
                counter += 1
                queue.append(closure)
            dfa_trans[T_name][a] = dfa_states_map[closure]

    # Constrói o AFD final
    dfa_estados = set(dfa_trans.keys())
    dfa_inicial = dfa_states_map[start_closure]
    dfa_alfabeto = alphabet
    dfa_finais_list = set(dfa_finals.keys())

    # Cria uma instância da classe AFD
    dfa = AFD(dfa_estados, dfa_alfabeto, dfa_trans, dfa_inicial, dfa_finais_list)
    dfa.token_finals = dfa_finals  # guarda o tipo de token em cada estado final

    return dfa, dfa_rev

# --- Execução principal ---
if __name__ == "__main__":
    # Instancia todos os AFDs disponíveis
    afds = [
        AFDComment(),
        AFDString(),
        AFDNumber(),
        AFDKeyword(),
        AFDIdent(),
        AFDOperator(),
        AFDDelimiters(),
        AFDWhitespace()
    ]

    # Define os tipos de token correspondentes
    token_types = [
        "COMMENT",
        "STRING",
        "NUMBER",
        "KEYWORD",
        "IDENTIFIER",
        "OPERATOR",
        "DELIMITER",
        "WHITESPACE"
    ]

    # Define prioridades dos tokens (menor valor = maior prioridade)
    token_priority = {
        "COMMENT": 1,
        "STRING": 2,
        "KEYWORD": 3,
        "NUMBER": 4,
        "IDENTIFIER": 5,
        "OPERATOR": 6,
        "DELIMITER": 7,
        "WHITESPACE": 8
    }

    print("Criando AFN a partir dos AFDs...")
    nfa = combine_afds_to_nfa(afds, token_types)
    print(f"AFN criado com {len(nfa['estados'])} estados")

    print("Convertendo AFN para AFD...")
    dfa, dfa_rev = nfa_to_dfa(nfa, token_priority)
    print(f"AFD gerado com {len(dfa.states)} estados e {len(dfa.final_states)} estados finais")

    print("\nEstados finais do AFD e seus tipos de token:")
    for estado in sorted(dfa.final_states):
        if hasattr(dfa, 'token_finals') and estado in dfa.token_finals:
            print(f"  {estado}: {dfa.token_finals[estado]}")
    
    print(f"\nAlfabeto do AFD: {len(dfa.alphabet)} símbolos")
    print(f"Estado inicial: {dfa.initial_state}")