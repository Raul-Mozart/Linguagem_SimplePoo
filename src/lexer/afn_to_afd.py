"""
Algoritmo de Construção de Subconjuntos - Conversão AFN para AFD

Este módulo implementa o algoritmo clássico de construção de subconjuntos
para converter um Autômato Finito Não-Determinístico (AFN/NFA) em um
Autômato Finito Determinístico (AFD/DFA).

Algoritmo:
1. Calcular o fechamento-epsilon do estado inicial
2. Para cada estado do AFD (conjunto de estados do AFN):
   - Para cada símbolo do alfabeto:
     - Calcular o conjunto de estados alcançáveis
     - Aplicar fechamento-epsilon
     - Criar novo estado no AFD se necessário
3. Marcar estados de aceitação (contêm estado final do AFN)

Autor: Sistema de Compiladores
Data: 2025
"""

from collections import deque
from typing import Set, Dict, FrozenSet, List, Optional
from dataclasses import dataclass, field


# ==================== ESTRUTURAS DE DADOS ====================

@dataclass
class EstadoAFN:
    """
    Representa um estado no Autômato Finito Não-Determinístico
    
    Atributos:
        id: identificador único do estado
        transicoes_epsilon: conjunto de estados alcançáveis por ε (epsilon)
        transicoes: dicionário mapeando conjunto de símbolos -> conjunto de estados destino
    """
    id: int
    transicoes_epsilon: Set["EstadoAFN"] = field(default_factory=set)
    transicoes: Dict[FrozenSet[str], Set["EstadoAFN"]] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, EstadoAFN) and self.id == other.id


@dataclass
class AFN:
    """
    Representa um Autômato Finito Não-Determinístico completo
    
    Atributos:
        estado_inicial: estado de onde começa o processamento
        estado_final: estado de aceitação (reconhecimento bem-sucedido)
    """
    estado_inicial: EstadoAFN
    estado_final: EstadoAFN


@dataclass
class AFD:
    """
    Representa um Autômato Finito Determinístico completo
    
    Atributos:
        estado_inicial: índice do estado inicial (geralmente 0)
        estados: lista de conjuntos de IDs dos estados AFN que formam cada estado AFD
        estados_aceitacao: conjunto de índices dos estados de aceitação
        tabela_transicoes: [estado_origem][símbolo] -> estado_destino
    """
    estado_inicial: int
    estados: List[FrozenSet[int]] = field(default_factory=list)
    estados_aceitacao: Set[int] = field(default_factory=set)
    tabela_transicoes: Dict[int, Dict[str, int]] = field(default_factory=dict)
    
    def aceita(self, palavra: str) -> bool:
        """
        Verifica se o AFD aceita uma determinada palavra
        
        Args:
            palavra: string a ser testada
            
        Returns:
            True se a palavra é aceita, False caso contrário
        """
        estado_atual = self.estado_inicial
        
        for simbolo in palavra:
            if estado_atual not in self.tabela_transicoes:
                return False
            if simbolo not in self.tabela_transicoes[estado_atual]:
                return False
            estado_atual = self.tabela_transicoes[estado_atual][simbolo]
        
        return estado_atual in self.estados_aceitacao
    
    def numero_estados(self) -> int:
        """Retorna o número total de estados no AFD"""
        return len(self.estados)


# ==================== FUNÇÕES AUXILIARES ====================

def fechamento_epsilon(estados: Set[EstadoAFN]) -> Set[EstadoAFN]:
    """
    Calcula o fechamento-epsilon de um conjunto de estados.
    
    O fechamento-epsilon é o conjunto de todos os estados alcançáveis
    a partir dos estados dados usando apenas transições epsilon (ε).
    
    Algoritmo:
    1. Inicializar fechamento com os estados originais
    2. Para cada estado, adicionar todos os estados alcançáveis por ε
    3. Repetir até não haver novos estados
    
    Args:
        estados: conjunto inicial de estados
        
    Returns:
        Conjunto expandido com todos os estados alcançáveis por epsilon
        
    Complexidade: O(n) onde n é o número de estados
    """
    pilha = list(estados)
    fechamento = set(estados)
    
    while pilha:
        estado = pilha.pop()
        # Para cada transição epsilon deste estado
        for estado_destino in estado.transicoes_epsilon:
            if estado_destino not in fechamento:
                fechamento.add(estado_destino)
                pilha.append(estado_destino)
    
    return fechamento


def ids_dos_estados(estados_afn: Set[EstadoAFN]) -> FrozenSet[int]:
    """
    Converte conjunto de estados AFN em conjunto imutável de IDs.
    
    Isso é necessário para usar conjuntos de estados como chaves
    em dicionários (para evitar estados duplicados).
    
    Args:
        estados_afn: conjunto de estados do AFN
        
    Returns:
        FrozenSet ordenado de IDs dos estados
    """
    return frozenset(sorted(estado.id for estado in estados_afn))


def mover(estados: Set[EstadoAFN], simbolo: str) -> Set[EstadoAFN]:
    """
    Calcula o conjunto de estados alcançáveis a partir de um conjunto
    de estados lendo um símbolo específico.
    
    Args:
        estados: conjunto de estados origem
        simbolo: símbolo a ser consumido
        
    Returns:
        Conjunto de estados alcançáveis
    """
    resultado = set()
    
    for estado in estados:
        # Para cada transição do estado
        for conjunto_simbolos, estados_destino in estado.transicoes.items():
            # Se o símbolo está no conjunto de símbolos da transição
            if simbolo in conjunto_simbolos:
                resultado.update(estados_destino)
    
    return resultado


# ==================== ALGORITMO PRINCIPAL ====================

def construir_afd(afn: AFN, alfabeto: List[str]) -> AFD:
    """
    Converte um AFN em AFD usando o Algoritmo de Construção de Subconjuntos.
    
    O algoritmo funciona criando estados do AFD que representam
    conjuntos de estados do AFN. Cada estado do AFD corresponde a
    um subconjunto dos estados do AFN que podem estar ativos simultaneamente.
    
    Passos do algoritmo:
    1. Criar estado inicial do AFD = fechamento-ε do estado inicial do AFN
    2. Para cada estado não processado do AFD:
       a. Para cada símbolo do alfabeto:
          - Calcular estados alcançáveis: move(estado, símbolo)
          - Aplicar fechamento-epsilon
          - Se conjunto não vazio, criar/reusar estado do AFD
          - Adicionar transição
    3. Marcar estados de aceitação (contêm estado final do AFN)
    
    Args:
        afn: Autômato Finito Não-Determinístico de entrada
        alfabeto: lista de símbolos possíveis
        
    Returns:
        Autômato Finito Determinístico equivalente
        
    Complexidade: O(2^n * |Σ|) no pior caso, onde n = número de estados do AFN
    """
    
    # PASSO 1: Calcular estado inicial do AFD
    estado_inicial_fechamento = fechamento_epsilon({afn.estado_inicial})
    estado_inicial_ids = ids_dos_estados(estado_inicial_fechamento)
    
    # Estruturas do AFD
    lista_estados: List[FrozenSet[int]] = [estado_inicial_ids]
    mapa_estados: Dict[FrozenSet[int], int] = {estado_inicial_ids: 0}
    estados_aceitacao: Set[int] = set()
    tabela_transicoes: Dict[int, Dict[str, int]] = {}
    
    # Se estado inicial contém estado final do AFN, é estado de aceitação
    if afn.estado_final.id in estado_inicial_ids:
        estados_aceitacao.add(0)
    
    # Fila de estados a processar (BFS - Busca em Largura)
    fila = deque([estado_inicial_fechamento])
    
    # Mapeamento id -> objeto EstadoAFN para busca rápida
    todos_estados_afn = {}
    pilha_descoberta = [afn.estado_inicial]
    while pilha_descoberta:
        estado = pilha_descoberta.pop()
        if estado.id in todos_estados_afn:
            continue
        todos_estados_afn[estado.id] = estado
        # Adicionar estados alcançáveis para descoberta
        for estados_destino in estado.transicoes.values():
            pilha_descoberta.extend(estados_destino)
        pilha_descoberta.extend(estado.transicoes_epsilon)
    
    # PASSO 2: Processar cada estado do AFD
    while fila:
        conjunto_atual = fila.popleft()
        ids_atual = ids_dos_estados(conjunto_atual)
        indice_atual = mapa_estados[ids_atual]
        tabela_transicoes[indice_atual] = {}
        
        # Para cada símbolo do alfabeto
        for simbolo in alfabeto:
            # Calcular move(conjunto_atual, simbolo)
            estados_apos_mover = mover(conjunto_atual, simbolo)
            
            if not estados_apos_mover:
                # Sem transição para este símbolo
                continue
            
            # Aplicar fechamento-epsilon
            novo_conjunto = fechamento_epsilon(estados_apos_mover)
            novos_ids = ids_dos_estados(novo_conjunto)
            
            # Verificar se é um novo estado
            if novos_ids not in mapa_estados:
                # Criar novo estado no AFD
                novo_indice = len(lista_estados)
                mapa_estados[novos_ids] = novo_indice
                lista_estados.append(novos_ids)
                
                # Verificar se é estado de aceitação
                if afn.estado_final.id in novos_ids:
                    estados_aceitacao.add(novo_indice)
                
                # Adicionar à fila para processar
                fila.append(novo_conjunto)
            
            # Adicionar transição ao AFD
            tabela_transicoes[indice_atual][simbolo] = mapa_estados[novos_ids]
    
    # PASSO 3: Retornar AFD construído
    return AFD(
        estado_inicial=0,
        estados=lista_estados,
        estados_aceitacao=estados_aceitacao,
        tabela_transicoes=tabela_transicoes
    )


# ==================== FUNÇÕES DE UTILIDADE ====================

def imprimir_afd(afd: AFD):
    """
    Imprime representação textual do AFD para debug
    
    Args:
        afd: Autômato Finito Determinístico
    """
    print("\n" + "="*60)
    print("AUTÔMATO FINITO DETERMINÍSTICO (AFD)")
    print("="*60)
    print(f"Estado Inicial: {afd.estado_inicial}")
    print(f"Total de Estados: {afd.numero_estados()}")
    print(f"Estados de Aceitação: {sorted(afd.estados_aceitacao)}")
    print("\nTabela de Transições:")
    print("-"*60)
    
    for estado in sorted(afd.tabela_transicoes.keys()):
        transicoes = afd.tabela_transicoes[estado]
        marcador = " (FINAL)" if estado in afd.estados_aceitacao else ""
        print(f"Estado {estado}{marcador}:")
        
        for simbolo in sorted(transicoes.keys()):
            destino = transicoes[simbolo]
            print(f"  '{simbolo}' -> Estado {destino}")
    
    print("="*60 + "\n")


def afd_para_mermaid(afd: AFD, nome: str = "AFD") -> str:
    """
    Gera diagrama Mermaid do AFD para visualização
    
    Args:
        afd: Autômato Finito Determinístico
        nome: nome do diagrama
        
    Returns:
        String contendo código Mermaid
    """
    linhas = [
        "```mermaid",
        "stateDiagram-v2",
        f"    direction LR",
        ""
    ]
    
    # Estado inicial
    linhas.append(f"    [*] --> q{afd.estado_inicial}")
    linhas.append("")
    
    # Estados de aceitação
    for estado in sorted(afd.estados_aceitacao):
        linhas.append(f"    q{estado} --> [*]")
    
    if afd.estados_aceitacao:
        linhas.append("")
    
    # Transições
    for estado in sorted(afd.tabela_transicoes.keys()):
        transicoes = afd.tabela_transicoes[estado]
        # Agrupar transições por destino
        destino_simbolos = {}
        for simbolo, destino in transicoes.items():
            if destino not in destino_simbolos:
                destino_simbolos[destino] = []
            destino_simbolos[destino].append(simbolo)
        
        # Gerar linhas de transição
        for destino, simbolos in sorted(destino_simbolos.items()):
            rotulo = ",".join(sorted(simbolos))
            linhas.append(f"    q{estado} --> q{destino}: {rotulo}")
    
    linhas.append("```")
    return "\n".join(linhas)


# ==================== EXEMPLO DE USO ====================

if __name__ == "__main__":
    """Exemplo de conversão AFN -> AFD"""
    
    # Criar um AFN simples: reconhece "ab*"
    # Estados: q0 -> a -> q1 -> b* -> q2 (final)
    q0 = EstadoAFN(id=0)
    q1 = EstadoAFN(id=1)
    q2 = EstadoAFN(id=2)
    
    # Transições
    q0.transicoes[frozenset(['a'])] = {q1}
    q1.transicoes[frozenset(['b'])] = {q2}
    q2.transicoes[frozenset(['b'])] = {q2}  # b*
    
    afn_exemplo = AFN(estado_inicial=q0, estado_final=q2)
    
    # Converter para AFD
    alfabeto = ['a', 'b']
    afd_resultado = construir_afd(afn_exemplo, alfabeto)
    
    # Mostrar resultado
    imprimir_afd(afd_resultado)
    
    # Testar palavras
    testes = ["a", "ab", "abb", "abbb", "ba", "aab", ""]
    print("Testes de aceitação:")
    print("-"*40)
    for palavra in testes:
        aceita = afd_resultado.aceita(palavra)
        status = "✅ ACEITA" if aceita else "❌ REJEITA"
        print(f"  '{palavra}' -> {status}")
    
    # Gerar diagrama Mermaid
    print("\nDiagrama Mermaid:")
    print(afd_para_mermaid(afd_resultado))
