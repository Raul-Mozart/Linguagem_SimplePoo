"""
Gerador de Código LLVM IR para SimplePOO
Traduz AST para representação intermediária LLVM

Baseado no material:
- Tradução sistemática de AST para IR
- Visitor pattern para percorrer nós
- Formato textual LLVM (.ll)
- Alloca/Load/Store para variáveis mutáveis
"""

from ast_nodes import *

class LLVMCodeGenerator:
    """
    Gerador de Código LLVM IR
    
    Estratégia:
    1. Tradução composicional recursiva
    2. Alloca/Load/Store para variáveis
    3. Blocos básicos para controle de fluxo
    4. Formato textual LLVM (.ll)
    """
    
    def __init__(self):
        self.output = []  # Linhas de código IR
        self.temp_counter = 0  # Contador para temporários %0, %1, %2...
        self.label_counter = 0  # Contador para labels
        self.variables = {}  # Mapa de variáveis para seus alloca
        self.functions = {}  # Funções declaradas
        self.current_function = None
        self.indent_level = 0
        
    # ============= GERAÇÃO DE CÓDIGO =============
    
    def generate(self, ast):
        """Gera código LLVM IR completo a partir da AST"""
        self.emit("; ModuleID = 'SimplePOO'")
        self.emit("target triple = \"x86_64-pc-linux-gnu\"")
        self.emit("")
        
        # Declarações de funções externas (printf para print)
        self.emit("declare i32 @printf(i8*, ...)")
        self.emit("")
        
        # Gera código para todas as declarações
        for decl in ast.declarations:
            self.visit(decl)
        
        # Retorna código completo
        return "\n".join(self.output)
    
    def emit(self, line=""):
        """Emite uma linha de código com indentação"""
        if line:
            indent = "  " * self.indent_level
            self.output.append(indent + line)
        else:
            self.output.append("")
    
    def new_temp(self):
        """Cria novo nome de temporário"""
        temp = f"%{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self, prefix="label"):
        """Cria novo label para bloco básico"""
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label
    
    # ============= VISITOR PATTERN =============
    
    def visit(self, node):
        """Despacha para método específico baseado no tipo do nó"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Método padrão para nós não implementados"""
        return None
    
    # ============= DECLARAÇÕES =============
    
    def visit_ProgramNode(self, node):
        """Programa: Lista de declarações"""
        # Se não houver função main, cria uma
        has_main = any(isinstance(d, FuncDeclNode) and d.name == 'main' 
                       for d in node.declarations)
        
        # Processa todas as declarações
        for decl in node.declarations:
            if isinstance(decl, FuncDeclNode):
                self.visit(decl)
            elif isinstance(decl, VarDeclNode):
                # Variáveis globais (simplificado - não implementado ainda)
                pass
            else:
                # Outros comandos no nível global - coloca em main
                pass
    
    def visit_VarDeclNode(self, node):
        """Declaração de variável: tipo nome = valor"""
        # Aloca espaço na pilha
        var_name = node.name
        llvm_type = self.get_llvm_type(node.var_type)
        
        alloca_temp = self.new_temp()
        self.emit(f"{alloca_temp} = alloca {llvm_type}")
        self.variables[var_name] = alloca_temp
        
        # Se há inicializador, armazena valor
        if node.initializer:
            value = self.visit(node.initializer)
            self.emit(f"store {llvm_type} {value}, {llvm_type}* {alloca_temp}")
    
    def visit_FuncDeclNode(self, node):
        """Declaração de função"""
        func_name = node.name
        self.current_function = func_name
        self.temp_counter = 0
        self.label_counter = 0
        self.variables = {}
        
        # Tipo de retorno (simplificado - sempre void por enquanto)
        ret_type = "void"
        
        # Parâmetros (simplificado - todos i64)
        params_str = ", ".join([f"i64 %{p}" for p in node.params])
        
        # Assinatura da função
        self.emit(f"define {ret_type} @{func_name}({params_str}) {{")
        self.indent_level += 1
        
        # Bloco de entrada
        self.emit("entry:")
        self.indent_level += 1
        
        # Aloca espaço para parâmetros (SSA requer isso)
        for param in node.params:
            param_alloca = self.new_temp()
            self.emit(f"{param_alloca} = alloca i64")
            self.emit(f"store i64 %{param}, i64* {param_alloca}")
            self.variables[param] = param_alloca
        
        # Corpo da função
        if node.body:
            self.visit(node.body)
        
        # Se não houver return explícito, adiciona
        if not self.output[-1].strip().startswith("ret"):
            self.emit("ret void")
        
        self.indent_level -= 1
        self.indent_level -= 1
        self.emit("}")
        self.emit("")
        
        self.current_function = None
    
    # ============= STATEMENTS =============
    
    def visit_BlockNode(self, node):
        """Bloco de código"""
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_IfNode(self, node):
        """If statement"""
        # Labels para blocos
        then_label = self.new_label("if.then")
        else_label = self.new_label("if.else") if node.else_branch else None
        end_label = self.new_label("if.end")
        
        # Avalia condição
        cond = self.visit(node.condition)
        
        # Branch condicional
        if else_label:
            self.emit(f"br i1 {cond}, label %{then_label}, label %{else_label}")
        else:
            self.emit(f"br i1 {cond}, label %{then_label}, label %{end_label}")
        
        # Bloco then
        self.indent_level -= 1
        self.emit(f"{then_label}:")
        self.indent_level += 1
        self.visit(node.then_branch)
        self.emit(f"br label %{end_label}")
        
        # Bloco else
        if else_label:
            self.indent_level -= 1
            self.emit(f"{else_label}:")
            self.indent_level += 1
            self.visit(node.else_branch)
            self.emit(f"br label %{end_label}")
        
        # Bloco de merge
        self.indent_level -= 1
        self.emit(f"{end_label}:")
        self.indent_level += 1
    
    def visit_ForNode(self, node):
        """For loop"""
        # Labels
        cond_label = self.new_label("for.cond")
        body_label = self.new_label("for.body")
        update_label = self.new_label("for.update")
        end_label = self.new_label("for.end")
        
        # Inicialização
        if node.init:
            self.visit(node.init)
        
        # Branch para condição
        self.emit(f"br label %{cond_label}")
        
        # Bloco de condição
        self.indent_level -= 1
        self.emit(f"{cond_label}:")
        self.indent_level += 1
        if node.condition:
            cond = self.visit(node.condition)
            self.emit(f"br i1 {cond}, label %{body_label}, label %{end_label}")
        else:
            self.emit(f"br label %{body_label}")
        
        # Bloco de corpo
        self.indent_level -= 1
        self.emit(f"{body_label}:")
        self.indent_level += 1
        if node.body:
            self.visit(node.body)
        self.emit(f"br label %{update_label}")
        
        # Bloco de atualização
        self.indent_level -= 1
        self.emit(f"{update_label}:")
        self.indent_level += 1
        if node.update:
            self.visit(node.update)
        self.emit(f"br label %{cond_label}")
        
        # Bloco de saída
        self.indent_level -= 1
        self.emit(f"{end_label}:")
        self.indent_level += 1
    
    def visit_ReturnNode(self, node):
        """Return statement"""
        if node.value:
            value = self.visit(node.value)
            # Simplificado - sempre retorna void
            self.emit("ret void")
        else:
            self.emit("ret void")
    
    def visit_PrintNode(self, node):
        """Print statement - usa printf"""
        if node.expression:
            value = self.visit(node.expression)
            
            # Format string para printf
            fmt_str = self.new_temp()
            self.emit(f'{fmt_str} = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0')
            
            # Chama printf
            self.emit(f"call i32 (i8*, ...) @printf(i8* {fmt_str}, i64 {value})")
    
    def visit_ExpressionStmtNode(self, node):
        """Expression statement"""
        self.visit(node.expression)
    
    # ============= EXPRESSÕES =============
    
    def visit_AssignmentNode(self, node):
        """Atribuição: x = valor"""
        value = self.visit(node.value)
        var_alloca = self.variables.get(node.target)
        
        if var_alloca:
            self.emit(f"store i64 {value}, i64* {var_alloca}")
        
        return value
    
    def visit_BinaryOpNode(self, node):
        """Operação binária"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp()
        
        # Operadores aritméticos
        if node.operator == '+':
            self.emit(f"{result} = add i64 {left}, {right}")
        elif node.operator == '-':
            self.emit(f"{result} = sub i64 {left}, {right}")
        elif node.operator == '*':
            self.emit(f"{result} = mul i64 {left}, {right}")
        elif node.operator == '/':
            self.emit(f"{result} = sdiv i64 {left}, {right}")
        elif node.operator == '%':
            self.emit(f"{result} = srem i64 {left}, {right}")
        
        # Operadores de comparação
        elif node.operator == '<':
            self.emit(f"{result} = icmp slt i64 {left}, {right}")
        elif node.operator == '>':
            self.emit(f"{result} = icmp sgt i64 {left}, {right}")
        elif node.operator == '<=':
            self.emit(f"{result} = icmp sle i64 {left}, {right}")
        elif node.operator == '>=':
            self.emit(f"{result} = icmp sge i64 {left}, {right}")
        elif node.operator == '==':
            self.emit(f"{result} = icmp eq i64 {left}, {right}")
        elif node.operator == '!=':
            self.emit(f"{result} = icmp ne i64 {left}, {right}")
        
        # Operadores lógicos (assumindo operandos i1)
        elif node.operator == '&&':
            self.emit(f"{result} = and i1 {left}, {right}")
        elif node.operator == '||':
            self.emit(f"{result} = or i1 {left}, {right}")
        
        return result
    
    def visit_UnaryOpNode(self, node):
        """Operação unária"""
        operand = self.visit(node.operand)
        result = self.new_temp()
        
        if node.operator == '-':
            self.emit(f"{result} = sub i64 0, {operand}")
        elif node.operator == '!':
            self.emit(f"{result} = xor i1 {operand}, true")
        elif node.operator in ['++', '--']:
            # Simplificado - não implementado ainda
            return operand
        
        return result
    
    def visit_CallNode(self, node):
        """Chamada de função"""
        # Avalia argumentos
        args = []
        for arg in node.arguments:
            args.append(self.visit(arg))
        
        # Nome da função
        if isinstance(node.function, IdentifierNode):
            func_name = node.function.name
        else:
            func_name = str(node.function)
        
        # Chama função (simplificado - sempre void)
        args_str = ", ".join([f"i64 {a}" for a in args])
        result = self.new_temp()
        self.emit(f"call void @{func_name}({args_str})")
        
        return result
    
    def visit_IdentifierNode(self, node):
        """Referência a variável"""
        var_alloca = self.variables.get(node.name)
        if var_alloca:
            temp = self.new_temp()
            self.emit(f"{temp} = load i64, i64* {var_alloca}")
            return temp
        return node.name
    
    def visit_LiteralNode(self, node):
        """Literal"""
        if isinstance(node.value, bool):
            return "true" if node.value else "false"
        elif isinstance(node.value, (int, float)):
            return str(node.value)
        elif isinstance(node.value, str):
            # String literal (simplificado)
            return f'"{node.value}"'
        elif node.value is None:
            return "null"
        return str(node.value)
    
    # ============= UTILITÁRIOS =============
    
    def get_llvm_type(self, type_name):
        """Mapeia tipo SimplePOO para tipo LLVM"""
        type_map = {
            'int': 'i64',
            'float': 'double',
            'string': 'i8*',
            'bool': 'i1',
            'var': 'i64',  # Default
            'any': 'i64',
            'const': 'i64',
        }
        return type_map.get(type_name, 'i64')
    
    def add_format_strings(self):
        """Adiciona strings de formato para printf (deve ser chamado no início)"""
        self.emit('@.str = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"')
        self.emit("")


# ============= EXEMPLO DE USO =============

if __name__ == "__main__":
    # Teste simples
    print("Gerador de Código LLVM IR para SimplePOO")
    print("Teste básico:")
    
    # Cria AST simples manualmente
    ast = ProgramNode([
        FuncDeclNode(
            name="main",
            params=[],
            body=BlockNode([
                VarDeclNode("x", "int", LiteralNode(10, "number")),
                VarDeclNode("y", "int", LiteralNode(20, "number")),
                VarDeclNode("soma", "int", 
                    BinaryOpNode(
                        IdentifierNode("x"),
                        "+",
                        IdentifierNode("y")
                    )
                ),
                PrintNode(IdentifierNode("soma"))
            ])
        )
    ])
    
    # Gera código
    generator = LLVMCodeGenerator()
    generator.add_format_strings()
    code = generator.generate(ast)
    
    print("\nCódigo LLVM IR gerado:\n")
    print(code)
