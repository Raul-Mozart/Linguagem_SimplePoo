"""
Nós da Árvore Sintática Abstrata (AST) para SimplePOO
Representam a estrutura do programa de forma hierárquica
"""

class ASTNode:
    """Classe base para todos os nós da AST"""
    def __init__(self, linha=0, coluna=0):
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"

# ============= NÓS DE PROGRAMA =============

class ProgramNode(ASTNode):
    """Nó raiz: representa o programa completo"""
    def __init__(self, declarations):
        super().__init__()
        self.declarations = declarations  # Lista de declarações de nível superior
    
    def __repr__(self):
        return f"Program({len(self.declarations)} declarations)"

# ============= NÓS DE DECLARAÇÕES =============

class VarDeclNode(ASTNode):
    """Declaração de variável: var/let/const/tipo nome = valor"""
    def __init__(self, name, var_type=None, initializer=None, is_const=False, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.name = name
        self.var_type = var_type
        self.initializer = initializer
        self.is_const = is_const
    
    def __repr__(self):
        return f"VarDecl({self.name}: {self.var_type})"

class FuncDeclNode(ASTNode):
    """Declaração de função: function nome(params) { body }"""
    def __init__(self, name, params, body, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.name = name
        self.params = params  # Lista de nomes de parâmetros
        self.body = body      # BlockNode
    
    def __repr__(self):
        return f"FuncDecl({self.name}, {len(self.params)} params)"

# ============= NÓS DE STATEMENTS =============

class BlockNode(ASTNode):
    """Bloco de código: { statements }"""
    def __init__(self, statements, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.statements = statements
    
    def __repr__(self):
        return f"Block({len(self.statements)} stmts)"

class IfNode(ASTNode):
    """If statement: if (condition) then_branch else else_branch"""
    def __init__(self, condition, then_branch, else_branch=None, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def __repr__(self):
        return f"If(has_else={self.else_branch is not None})"

class ForNode(ASTNode):
    """For loop: for (init; condition; update) body"""
    def __init__(self, init, condition, update, body, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
    
    def __repr__(self):
        return "For()"

class ReturnNode(ASTNode):
    """Return statement: return expr;"""
    def __init__(self, value=None, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.value = value
    
    def __repr__(self):
        return f"Return({self.value is not None})"

class BreakNode(ASTNode):
    """Break statement"""
    def __init__(self, linha=0, coluna=0):
        super().__init__(linha, coluna)
    
    def __repr__(self):
        return "Break"

class ContinueNode(ASTNode):
    """Continue statement"""
    def __init__(self, linha=0, coluna=0):
        super().__init__(linha, coluna)
    
    def __repr__(self):
        return "Continue"

class PrintNode(ASTNode):
    """Print statement: print(expr);"""
    def __init__(self, expression, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.expression = expression
    
    def __repr__(self):
        return "Print"

class ExprStmtNode(ASTNode):
    """Expression statement: expr;"""
    def __init__(self, expression, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.expression = expression
    
    def __repr__(self):
        return "ExprStmt"

# ============= NÓS DE EXPRESSÕES =============

class BinaryOpNode(ASTNode):
    """Operação binária: left op right"""
    def __init__(self, left, operator, right, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.operator})"

class UnaryOpNode(ASTNode):
    """Operação unária: op operand"""
    def __init__(self, operator, operand, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.operator})"

class AssignmentNode(ASTNode):
    """Atribuição: target op value"""
    def __init__(self, target, operator, value, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.target = target  # Identificador ou acesso
        self.operator = operator  # =, +=, -=, etc.
        self.value = value
    
    def __repr__(self):
        return f"Assignment({self.operator})"

class CallNode(ASTNode):
    """Chamada de função: function(args)"""
    def __init__(self, function, arguments, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.function = function
        self.arguments = arguments
    
    def __repr__(self):
        return f"Call({len(self.arguments)} args)"

class IndexNode(ASTNode):
    """Acesso a índice: array[index]"""
    def __init__(self, array, index, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.array = array
        self.index = index
    
    def __repr__(self):
        return "Index"

class ArrayLiteralNode(ASTNode):
    """Literal de array: [elements]"""
    def __init__(self, elements, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.elements = elements
    
    def __repr__(self):
        return f"ArrayLiteral({len(self.elements)} elements)"

# ============= NÓS LITERAIS =============

class LiteralNode(ASTNode):
    """Literal (número, string, bool, null)"""
    def __init__(self, value, value_type, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.value = value
        self.value_type = value_type  # 'number', 'string', 'bool', 'null'
    
    def __repr__(self):
        return f"Literal({self.value!r})"

class IdentifierNode(ASTNode):
    """Identificador (nome de variável)"""
    def __init__(self, name, linha=0, coluna=0):
        super().__init__(linha, coluna)
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"

# ============= UTILITÁRIO: VISUALIZAÇÃO DA AST =============

def print_ast(node, indent=0):
    """Imprime a AST de forma hierárquica para debugging"""
    prefix = "  " * indent
    print(f"{prefix}{node}")
    
    # Percorre os atributos do nó
    if isinstance(node, ProgramNode):
        for decl in node.declarations:
            print_ast(decl, indent + 1)
    
    elif isinstance(node, FuncDeclNode):
        print(f"{prefix}  params: {node.params}")
        print_ast(node.body, indent + 1)
    
    elif isinstance(node, BlockNode):
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, IfNode):
        print(f"{prefix}  condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  then:")
        print_ast(node.then_branch, indent + 2)
        if node.else_branch:
            print(f"{prefix}  else:")
            print_ast(node.else_branch, indent + 2)
    
    elif isinstance(node, ForNode):
        if node.init:
            print(f"{prefix}  init:")
            print_ast(node.init, indent + 2)
        if node.condition:
            print(f"{prefix}  condition:")
            print_ast(node.condition, indent + 2)
        if node.update:
            print(f"{prefix}  update:")
            for expr in node.update if isinstance(node.update, list) else [node.update]:
                print_ast(expr, indent + 2)
        print(f"{prefix}  body:")
        print_ast(node.body, indent + 2)
    
    elif isinstance(node, VarDeclNode):
        if node.initializer:
            print(f"{prefix}  initializer:")
            print_ast(node.initializer, indent + 2)
    
    elif isinstance(node, (ReturnNode, PrintNode, ExprStmtNode)):
        if hasattr(node, 'value') and node.value:
            print_ast(node.value, indent + 1)
        elif hasattr(node, 'expression') and node.expression:
            print_ast(node.expression, indent + 1)
    
    elif isinstance(node, (BinaryOpNode, AssignmentNode)):
        print_ast(node.left if hasattr(node, 'left') else node.target, indent + 1)
        print_ast(node.right if hasattr(node, 'right') else node.value, indent + 1)
    
    elif isinstance(node, UnaryOpNode):
        print_ast(node.operand, indent + 1)
    
    elif isinstance(node, CallNode):
        print_ast(node.function, indent + 1)
        for arg in node.arguments:
            print_ast(arg, indent + 2)
    
    elif isinstance(node, IndexNode):
        print_ast(node.array, indent + 1)
        print_ast(node.index, indent + 1)
    
    elif isinstance(node, ArrayLiteralNode):
        for elem in node.elements:
            print_ast(elem, indent + 1)
