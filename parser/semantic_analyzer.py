"""
Analisador Semântico para SimplePOO
Realiza verificações semânticas sobre a AST:
- Declarações de variáveis e funções
- Verificação de tipos
- Verificação de escopo
- Uso de variáveis não declaradas
- Compatibilidade de tipos em operações
"""

from symbol_table import SymbolTable, Symbol
from ast_nodes import *

class SemanticError:
    """Representa um erro semântico encontrado"""
    def __init__(self, message, line=0, column=0):
        self.message = message
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Erro linha {self.line}: {self.message}"


class SemanticAnalyzer:
    """
    Analisador Semântico - Visitor Pattern
    
    Percorre a AST e realiza verificações:
    1. Variáveis declaradas antes de serem usadas
    2. Sem redeclarações no mesmo escopo
    3. Tipos compatíveis em operações
    4. Funções retornam valores corretos
    5. Constantes não são modificadas
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.warnings = []
        self.current_function = None  # Para verificar returns
        self.in_loop = False  # Para verificar break/continue
    
    # ============= ANÁLISE PRINCIPAL =============
    
    def analyze(self, ast):
        """
        Executa análise semântica completa na AST
        
        Returns:
            (success: bool, errors: list, warnings: list)
        """
        try:
            self.visit(ast)
            
            # Sucesso se não houver erros
            success = len(self.errors) == 0
            
            return success, self.errors, self.warnings
        
        except Exception as e:
            # Erro inesperado
            self.errors.append(SemanticError(f"Erro interno: {str(e)}"))
            return False, self.errors, self.warnings
    
    # ============= VISITOR PATTERN =============
    
    def visit(self, node):
        """Despacha para o método correto baseado no tipo do nó"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Método padrão para nós não implementados"""
        return None
    
    # ============= VISITANTES DE NÓS =============
    
    def visit_ProgramNode(self, node):
        """Programa: Lista de declarações de nível superior"""
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_VarDeclNode(self, node):
        """Declaração de variável: var/let/const/tipo nome = valor"""
        
        # Determina o tipo da variável
        var_type = node.var_type if node.var_type else 'var'
        
        # Se há inicializador, infere o tipo
        if node.initializer:
            init_type = self.visit(node.initializer)
            
            # Se tipo foi especificado, verifica compatibilidade
            if node.var_type and init_type:
                if not self.is_compatible(node.var_type, init_type):
                    self.errors.append(SemanticError(
                        f"Tipo incompatível: '{node.name}' declarado como {node.var_type} mas inicializado com {init_type}",
                        node.linha, node.coluna
                    ))
            
            # Se tipo não foi especificado, usa o tipo inferido
            if not node.var_type and init_type:
                var_type = init_type
        
        # Declara símbolo na tabela
        kind = 'const' if node.is_const else 'var'
        initialized = node.initializer is not None
        
        success, message = self.symbol_table.declare(
            node.name, var_type, kind=kind,
            line=node.linha, initialized=initialized, is_const=node.is_const
        )
        
        if not success:
            self.errors.append(SemanticError(message, node.linha, node.coluna))
        
        return var_type
    
    def visit_FuncDeclNode(self, node):
        """Declaração de função"""
        
        # Declara função no escopo atual
        success, message = self.symbol_table.declare(
            node.name, 'function', kind='function', line=node.linha
        )
        
        if not success:
            self.errors.append(SemanticError(message, node.linha, node.coluna))
        
        # Entra em novo escopo para a função
        self.symbol_table.enter_scope()
        self.current_function = node.name
        
        # Declara parâmetros no escopo da função
        for param in node.params:
            self.symbol_table.declare(param, 'any', kind='parameter', initialized=True)
        
        # Visita corpo da função
        if node.body:
            self.visit(node.body)
        
        # Sai do escopo da função
        warnings = self.symbol_table.exit_scope()
        self.warnings.extend(warnings)
        self.current_function = None
    
    def visit_BlockNode(self, node):
        """Bloco de código"""
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_IfNode(self, node):
        """If statement"""
        # Verifica condição
        cond_type = self.visit(node.condition)
        
        if cond_type and cond_type != 'bool':
            self.errors.append(SemanticError(
                f"Condição de if deve ser booleana, encontrado {cond_type}",
                node.linha, node.coluna
            ))
        
        # Visita branches
        self.visit(node.then_branch)
        
        if node.else_branch:
            self.visit(node.else_branch)
    
    def visit_ForNode(self, node):
        """For loop"""
        # Entra em escopo para o loop
        self.symbol_table.enter_scope()
        self.in_loop = True
        
        # Visita componentes
        if node.init:
            self.visit(node.init)
        
        if node.condition:
            cond_type = self.visit(node.condition)
            if cond_type and cond_type != 'bool':
                self.errors.append(SemanticError(
                    f"Condição de for deve ser booleana, encontrado {cond_type}",
                    node.linha, node.coluna
                ))
        
        if node.update:
            self.visit(node.update)
        
        if node.body:
            self.visit(node.body)
        
        # Sai do escopo
        warnings = self.symbol_table.exit_scope()
        self.warnings.extend(warnings)
        self.in_loop = False
    
    def visit_ReturnNode(self, node):
        """Return statement"""
        if not self.current_function:
            self.errors.append(SemanticError(
                "Return fora de função",
                node.linha, node.coluna
            ))
        
        if node.value:
            return self.visit(node.value)
    
    def visit_BreakNode(self, node):
        """Break statement"""
        if not self.in_loop:
            self.errors.append(SemanticError(
                "Break fora de loop",
                node.linha, node.coluna
            ))
    
    def visit_ContinueNode(self, node):
        """Continue statement"""
        if not self.in_loop:
            self.errors.append(SemanticError(
                "Continue fora de loop",
                node.linha, node.coluna
            ))
    
    def visit_PrintNode(self, node):
        """Print statement"""
        if node.expression:
            self.visit(node.expression)
    
    def visit_ExpressionStmtNode(self, node):
        """Expression statement"""
        return self.visit(node.expression)
    
    # ============= EXPRESSÕES =============
    
    def visit_AssignmentNode(self, node):
        """Atribuição: x = valor"""
        # Verifica se variável existe
        if not self.symbol_table.exists(node.target):
            self.errors.append(SemanticError(
                f"Variável '{node.target}' não foi declarada",
                node.linha, node.coluna
            ))
            return None
        
        # Verifica se é constante
        if self.symbol_table.is_const(node.target):
            self.errors.append(SemanticError(
                f"Não é possível atribuir a constante '{node.target}'",
                node.linha, node.coluna
            ))
        
        # Marca como inicializada e usada
        self.symbol_table.mark_initialized(node.target)
        self.symbol_table.mark_used(node.target)
        
        # Verifica tipo do valor
        value_type = self.visit(node.value)
        var_type = self.symbol_table.get_type(node.target)
        
        if var_type and value_type:
            if not self.is_compatible(var_type, value_type):
                self.errors.append(SemanticError(
                    f"Tipo incompatível: '{node.target}' é {var_type} mas valor é {value_type}",
                    node.linha, node.coluna
                ))
        
        return var_type
    
    def visit_BinaryOpNode(self, node):
        """Operação binária: a + b, a < b, etc"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Operadores aritméticos: +, -, *, /, %
        if node.operator in ['+', '-', '*', '/', '%']:
            # String + String é válido (concatenação)
            if node.operator == '+' and left_type == 'string' and right_type == 'string':
                return 'string'
            
            # Números com números
            if self.is_numeric(left_type) and self.is_numeric(right_type):
                # Se um é float, resultado é float
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                return 'int'
            
            self.errors.append(SemanticError(
                f"Operador {node.operator} requer operandos numéricos, encontrado {left_type} e {right_type}",
                node.linha, node.coluna
            ))
            return None
        
        # Operadores de comparação: <, >, <=, >=, ==, !=
        elif node.operator in ['<', '>', '<=', '>=', '==', '!=']:
            # Comparação entre tipos compatíveis
            if left_type and right_type:
                if not self.is_comparable(left_type, right_type):
                    self.errors.append(SemanticError(
                        f"Não é possível comparar {left_type} com {right_type}",
                        node.linha, node.coluna
                    ))
            return 'bool'
        
        # Operadores lógicos: &&, ||
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                self.errors.append(SemanticError(
                    f"Operador {node.operator} requer operandos booleanos",
                    node.linha, node.coluna
                ))
            return 'bool'
        
        return None
    
    def visit_UnaryOpNode(self, node):
        """Operação unária: -x, !x, ++x, --x"""
        operand_type = self.visit(node.operand)
        
        # Negação aritmética: -
        if node.operator == '-':
            if not self.is_numeric(operand_type):
                self.errors.append(SemanticError(
                    f"Operador - requer operando numérico, encontrado {operand_type}",
                    node.linha, node.coluna
                ))
            return operand_type
        
        # Negação lógica: !
        elif node.operator == '!':
            if operand_type != 'bool':
                self.errors.append(SemanticError(
                    f"Operador ! requer operando booleano, encontrado {operand_type}",
                    node.linha, node.coluna
                ))
            return 'bool'
        
        # Incremento/Decremento: ++, --
        elif node.operator in ['++', '--']:
            if not self.is_numeric(operand_type):
                self.errors.append(SemanticError(
                    f"Operador {node.operator} requer operando numérico",
                    node.linha, node.coluna
                ))
            return operand_type
        
        return None
    
    def visit_CallNode(self, node):
        """Chamada de função: f(args)"""
        # Obtém nome da função
        func_name = None
        if isinstance(node.function, IdentifierNode):
            func_name = node.function.name
        elif isinstance(node.function, str):
            func_name = node.function
        
        # Verifica se função existe
        if func_name and not self.symbol_table.exists(func_name):
            self.errors.append(SemanticError(
                f"Função '{func_name}' não foi declarada",
                node.linha, node.coluna
            ))
            return None
        
        # Marca como usada
        if func_name:
            self.symbol_table.mark_used(func_name)
        
        # Visita argumentos
        for arg in node.arguments:
            self.visit(arg)
        
        # Retorna tipo genérico (seria necessário mais info na tabela)
        return 'any'
    
    def visit_IndexNode(self, node):
        """Acesso a array: arr[i]"""
        array_type = self.visit(node.array)
        index_type = self.visit(node.index)
        
        if index_type and not self.is_numeric(index_type):
            self.errors.append(SemanticError(
                f"Índice de array deve ser numérico, encontrado {index_type}",
                node.linha, node.coluna
            ))
        
        return 'any'  # Simplificado
    
    def visit_ArrayLiteralNode(self, node):
        """Array literal: [1, 2, 3]"""
        element_types = []
        for element in node.elements:
            elem_type = self.visit(element)
            if elem_type:
                element_types.append(elem_type)
        
        return 'array'
    
    def visit_IdentifierNode(self, node):
        """Identificador: nome de variável"""
        # Verifica se foi declarado
        if not self.symbol_table.exists(node.name):
            self.errors.append(SemanticError(
                f"Variável '{node.name}' não foi declarada",
                node.linha, node.coluna
            ))
            return None
        
        # Marca como usado
        self.symbol_table.mark_used(node.name)
        
        # Retorna tipo
        return self.symbol_table.get_type(node.name)
    
    def visit_LiteralNode(self, node):
        """Literal: número, string, bool, null"""
        value = node.value
        
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif value is None:
            return 'null'
        
        return 'unknown'
    
    # ============= FUNÇÕES AUXILIARES =============
    
    def is_numeric(self, type_name):
        """Verifica se tipo é numérico"""
        return type_name in ['int', 'float']
    
    def is_compatible(self, type1, type2):
        """Verifica se tipos são compatíveis para atribuição"""
        if type1 == type2:
            return True
        
        # var/any aceita qualquer tipo
        if type1 in ['var', 'any'] or type2 in ['var', 'any']:
            return True
        
        # int pode ser atribuído a float
        if type1 == 'float' and type2 == 'int':
            return True
        
        return False
    
    def is_comparable(self, type1, type2):
        """Verifica se tipos podem ser comparados"""
        # Mesmos tipos são comparáveis
        if type1 == type2:
            return True
        
        # Números entre si
        if self.is_numeric(type1) and self.is_numeric(type2):
            return True
        
        return False
    
    # ============= RELATÓRIOS =============
    
    def print_errors(self):
        """Imprime erros encontrados"""
        if not self.errors:
            print("✅ Nenhum erro semântico encontrado!")
            return
        
        print(f"\n❌ {len(self.errors)} erro(s) semântico(s) encontrado(s):\n")
        for error in self.errors:
            print(f"  {error}")
    
    def print_warnings(self):
        """Imprime avisos"""
        if not self.warnings:
            return
        
        print(f"\n⚠️  {len(self.warnings)} aviso(s):\n")
        for warning in self.warnings:
            print(f"  {warning}")
    
    def print_symbol_table(self):
        """Imprime tabela de símbolos"""
        self.symbol_table.print_table()
