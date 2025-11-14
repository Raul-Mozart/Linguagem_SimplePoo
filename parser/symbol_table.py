"""
Tabela de Símbolos para Análise Semântica - SimplePOO
Gerencia escopos e símbolos declarados no programa
"""

class Symbol:
    """
    Representa um símbolo (variável/função) na tabela
    
    Atributos:
    - name: Nome do símbolo
    - symbol_type: Tipo do símbolo (int, float, string, bool, function, etc)
    - kind: Tipo de símbolo (var, const, function, parameter)
    - line: Linha onde foi declarado
    - initialized: Se foi inicializado
    - used: Se foi usado em algum lugar
    - is_const: Se é constante (não pode ser modificada)
    """
    
    def __init__(self, name, symbol_type, kind='var', line=0, initialized=False, is_const=False):
        self.name = name
        self.symbol_type = symbol_type
        self.kind = kind  # 'var', 'const', 'function', 'parameter'
        self.line = line
        self.initialized = initialized
        self.used = False
        self.is_const = is_const
    
    def __repr__(self):
        flags = []
        if self.initialized:
            flags.append('init')
        if self.used:
            flags.append('used')
        if self.is_const:
            flags.append('const')
        
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        return f"{self.name}: {self.symbol_type} ({self.kind}, line {self.line}){flag_str}"


class SymbolTable:
    """
    Tabela de Símbolos com suporte a escopos aninhados
    
    Implementa uma pilha de escopos onde:
    - Escopo global: Nível 0 (variáveis e funções globais)
    - Escopos locais: Níveis 1+ (funções, blocos)
    
    Características:
    - Busca hierárquica (do escopo atual para o global)
    - Shadowing (variável local pode sombrear global)
    - Detecção de redeclarações no mesmo escopo
    - Rastreamento de uso de variáveis
    """
    
    def __init__(self):
        """Inicializa com escopo global"""
        self.scopes = [{}]  # Pilha de escopos (lista de dicionários)
        self.scope_level = 0
    
    # ============= GERENCIAMENTO DE ESCOPOS =============
    
    def enter_scope(self):
        """Entra em um novo escopo (função, bloco, etc)"""
        self.scopes.append({})
        self.scope_level += 1
    
    def exit_scope(self):
        """Sai do escopo atual e retorna símbolos não utilizados"""
        if self.scope_level <= 0:
            raise RuntimeError("Erro interno: Tentativa de sair do escopo global")
        
        # Coletar avisos sobre variáveis não utilizadas
        warnings = []
        current_scope = self.scopes[-1]
        
        for symbol in current_scope.values():
            if not symbol.used and symbol.kind == 'var':
                warnings.append(f"Aviso: Variável '{symbol.name}' declarada na linha {symbol.line} nunca foi utilizada")
        
        self.scopes.pop()
        self.scope_level -= 1
        
        return warnings
    
    # ============= OPERAÇÕES DE SÍMBOLOS =============
    
    def declare(self, name, symbol_type, kind='var', line=0, initialized=False, is_const=False):
        """
        Declara um novo símbolo no escopo atual
        
        Returns:
            (success: bool, message: str) - Tupla com sucesso e mensagem
        """
        current_scope = self.scopes[-1]
        
        # Verifica redeclaração no mesmo escopo
        if name in current_scope:
            existing = current_scope[name]
            return False, f"Erro: '{name}' já foi declarado na linha {existing.line}"
        
        # Adiciona símbolo ao escopo atual
        symbol = Symbol(name, symbol_type, kind, line, initialized, is_const)
        current_scope[name] = symbol
        
        return True, f"Símbolo '{name}' declarado com sucesso"
    
    def lookup(self, name):
        """
        Busca um símbolo, começando do escopo mais interno
        
        Returns:
            Symbol ou None se não encontrado
        """
        # Busca do escopo atual para o global
        for i in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        
        return None  # Não encontrado
    
    def lookup_current_scope(self, name):
        """Busca apenas no escopo atual"""
        return self.scopes[-1].get(name)
    
    def exists(self, name):
        """Verifica se símbolo existe em algum escopo visível"""
        return self.lookup(name) is not None
    
    def get_type(self, name):
        """Obtém o tipo de um símbolo"""
        symbol = self.lookup(name)
        return symbol.symbol_type if symbol else None
    
    # ============= MARCAÇÕES =============
    
    def mark_used(self, name):
        """Marca um símbolo como usado"""
        symbol = self.lookup(name)
        if symbol:
            symbol.used = True
            return True
        return False
    
    def mark_initialized(self, name):
        """Marca um símbolo como inicializado"""
        symbol = self.lookup(name)
        if symbol:
            symbol.initialized = True
            return True
        return False
    
    def is_const(self, name):
        """Verifica se símbolo é constante"""
        symbol = self.lookup(name)
        return symbol.is_const if symbol else False
    
    def is_initialized(self, name):
        """Verifica se símbolo foi inicializado"""
        symbol = self.lookup(name)
        return symbol.initialized if symbol else False
    
    # ============= DEBUG E VISUALIZAÇÃO =============
    
    def print_table(self):
        """Imprime a estrutura completa da tabela (útil para debug)"""
        print("\n" + "="*60)
        print("TABELA DE SÍMBOLOS")
        print("="*60)
        
        for level, scope in enumerate(self.scopes):
            print(f"\nEscopo Nível {level}:" + (" (Global)" if level == 0 else " (Local)"))
            if not scope:
                print("  (vazio)")
            else:
                for symbol in scope.values():
                    print(f"  {symbol}")
        
        print("="*60 + "\n")
    
    def get_all_symbols(self):
        """Retorna todos os símbolos de todos os escopos"""
        all_symbols = []
        for scope in self.scopes:
            all_symbols.extend(scope.values())
        return all_symbols


# ============= EXEMPLO DE USO =============

if __name__ == "__main__":
    print("🔍 Testando Tabela de Símbolos\n")
    
    table = SymbolTable()
    
    # Escopo global
    table.declare('x', 'int', line=1, initialized=True)
    table.declare('PI', 'float', kind='const', line=2, initialized=True, is_const=True)
    
    print(f"Tipo de 'x': {table.get_type('x')}")
    print(f"'x' existe? {table.exists('x')}")
    print(f"'y' existe? {table.exists('y')}")
    
    # Entrar em escopo local (função)
    table.enter_scope()
    table.declare('y', 'string', line=5)
    table.declare('x', 'float', line=6)  # Shadow de x global
    
    print(f"\nTipo de 'x' no escopo interno: {table.get_type('x')}")  # float (shadowing)
    print(f"Tipo de 'PI': {table.get_type('PI')}")  # float (do global)
    
    # Marcar como usados
    table.mark_used('x')
    table.mark_used('PI')
    # 'y' não marcado como usado - vai gerar aviso
    
    table.print_table()
    
    # Sair do escopo
    warnings = table.exit_scope()
    for warning in warnings:
        print(warning)
    
    print(f"\nTipo de 'x' após sair do escopo: {table.get_type('x')}")  # int (global)
    print(f"'y' ainda existe? {table.exists('y')}")  # False
    
    table.print_table()
    
    print("\n✅ Teste da Tabela de Símbolos completo!")
