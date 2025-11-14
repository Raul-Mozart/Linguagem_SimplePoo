"""
Parser Recursivo Descendente para SimplePOO
Implementa análise sintática com construção de AST

Baseado nos princípios:
- Cada não-terminal da gramática vira uma função
- Parsing descendente preditivo
- Construção simultânea da AST
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))

from lexer_enhanced import EnhancedLexer
from ast_nodes import *

class ParseError(Exception):
    """Exceção para erros de parsing"""
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(message)

class Parser:
    """
    Parser Recursivo Descendente
    
    Características:
    - Parsing top-down (descendente)
    - Preditivo (olha 1 token à frente)
    - Constrói AST durante o parsing
    - Recuperação básica de erros
    """
    
    def __init__(self, lexer):
        """
        Inicializa o parser com um lexer
        
        Args:
            lexer: EnhancedLexer já com tokens carregados
        """
        self.lexer = lexer
        self.errors = []
    
    # ============= MÉTODOS AUXILIARES =============
    
    def current_token(self):
        """Retorna o token atual sem consumir"""
        return self.lexer.peek_token()
    
    def peek(self, offset=0):
        """Olha tokens à frente sem consumir"""
        return self.lexer.peek_token(offset)
    
    def advance(self):
        """Consome e retorna o token atual"""
        return self.lexer.next_token()
    
    def check(self, token_type):
        """Verifica se o token atual é do tipo esperado"""
        token = self.current_token()
        return token and token.tipo == token_type
    
    def check_value(self, token_value):
        """Verifica se o token atual tem o valor esperado"""
        token = self.current_token()
        return token and token.lexema == token_value
    
    def match(self, *token_types):
        """Verifica se o token atual é de algum dos tipos"""
        for token_type in token_types:
            if self.check(token_type):
                return True
        return False
    
    def consume(self, token_type, message=None):
        """Consome token esperado ou lança erro"""
        token = self.current_token()
        if not token:
            raise ParseError(message or f"Esperado {token_type}, encontrado fim do arquivo")
        
        if not self.check(token_type):
            msg = message or f"Esperado {token_type}, encontrado {token.tipo} '{token.lexema}'"
            self.error(msg, token)
            raise ParseError(msg, token)
        
        return self.advance()
    
    def consume_value(self, expected_value, message=None):
        """Consome token com valor específico ou lança erro"""
        token = self.current_token()
        if not token or token.lexema != expected_value:
            msg = message or f"Esperado '{expected_value}'"
            self.error(msg, token)
            raise ParseError(msg, token)
        
        return self.advance()
    
    def error(self, message, token=None):
        """Registra um erro de parsing"""
        if token:
            error_msg = f"Erro na linha {token.linha}, coluna {token.coluna}: {message}"
        else:
            error_msg = f"Erro: {message}"
        
        self.errors.append(error_msg)
        print(f"  ❌ {error_msg}")
    
    def synchronize(self):
        """Recuperação de erro: avança até próximo ponto seguro"""
        self.advance()
        
        while self.current_token():
            # Para em ponto-e-vírgula ou palavra-chave de statement
            if self.check('DELIMITERS') and self.check_value(';'):
                return
            
            if self.check('KEYWORD'):
                lexema = self.current_token().lexema
                if lexema in ['var', 'let', 'const', 'function', 'if', 
                             'for', 'return', 'break', 'continue', 'print']:
                    return
            
            self.advance()
    
    # ============= PARSING DO PROGRAMA =============
    
    def parse(self):
        """
        Ponto de entrada: parseia o programa completo
        
        Program = { TopLevelDecl }
        """
        print("\n[*] Iniciando parsing...")
        declarations = []
        
        while self.current_token():
            try:
                decl = self.parse_top_level_decl()
                if decl:
                    declarations.append(decl)
            except ParseError as e:
                # Recupera do erro e continua
                self.synchronize()
        
        ast = ProgramNode(declarations)
        
        if self.errors:
            print(f"\n[X] Parsing finalizado com {len(self.errors)} erro(s)")
        else:
            print(f"\n[OK] Parsing bem-sucedido! {len(declarations)} declaracoes")
        
        return ast
    
    def parse_top_level_decl(self):
        """
        TopLevelDecl = VarDecl | FuncDecl | Statement
        """
        # Verifica se é declaração de função
        if self.check('KEYWORD') and self.check_value('function'):
            return self.parse_func_decl()
        
        # Verifica se é declaração de variável
        if self.check('KEYWORD'):
            lexema = self.current_token().lexema
            if lexema in ['var', 'let', 'const', 'int', 'float', 'string', 'bool', 'list']:
                return self.parse_var_decl()
        
        # Senão, tenta parsear como statement
        return self.parse_statement()
    
    # ============= DECLARAÇÕES =============
    
    def parse_var_decl(self):
        """
        VarDecl = ("var"|"let"|"const"|Type) IDENT ["=" Expr] ";"
        """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        # Pega tipo ou palavra-chave
        keyword = self.advance()
        var_type = keyword.lexema
        is_const = (var_type == 'const')
        
        # Nome da variável
        name_token = self.consume('IDENT', "Esperado nome da variável")
        name = name_token.lexema
        
        # Inicialização opcional
        initializer = None
        if self.check('OPERATOR') and self.check_value('='):
            self.advance()  # consome '='
            initializer = self.parse_expr()
        
        # Ponto-e-vírgula
        self.consume('DELIMITERS', "Esperado ';' após declaração de variável")
        
        return VarDeclNode(name, var_type, initializer, is_const, linha, coluna)
    
    def parse_func_decl(self):
        """
        FuncDecl = "function" IDENT "(" [ParamList] ")" Block
        """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('function')
        
        # Nome da função
        name_token = self.consume('IDENT', "Esperado nome da função")
        name = name_token.lexema
        
        # Parênteses e parâmetros
        self.consume_value('(', "Esperado '(' após nome da função")
        
        params = []
        if not self.check_value(')'):
            params = self.parse_param_list()
        
        self.consume_value(')', "Esperado ')' após parâmetros")
        
        # Corpo da função
        body = self.parse_block()
        
        return FuncDeclNode(name, params, body, linha, coluna)
    
    def parse_param_list(self):
        """
        ParamList = IDENT { "," IDENT }
        """
        params = []
        
        params.append(self.consume('IDENT').lexema)
        
        while self.check_value(','):
            self.advance()  # consome ','
            params.append(self.consume('IDENT').lexema)
        
        return params
    
    # ============= STATEMENTS =============
    
    def parse_statement(self):
        """
        Statement = VarDecl | IfStmt | ForStmt | Block | 
                   ReturnStmt | BreakStmt | ContinueStmt | 
                   PrintStmt | ExprStmt
        """
        token = self.current_token()
        if not token:
            return None
        
        # Declaração de variável
        if token.tipo == 'KEYWORD':
            if token.lexema in ['var', 'let', 'const', 'int', 'float', 'string', 'bool', 'list']:
                return self.parse_var_decl()
            elif token.lexema == 'if':
                return self.parse_if_stmt()
            elif token.lexema == 'for':
                return self.parse_for_stmt()
            elif token.lexema == 'return':
                return self.parse_return_stmt()
            elif token.lexema == 'break':
                return self.parse_break_stmt()
            elif token.lexema == 'continue':
                return self.parse_continue_stmt()
            elif token.lexema == 'print':
                return self.parse_print_stmt()
        
        # Bloco
        if token.tipo == 'DELIMITERS' and token.lexema == '{':
            return self.parse_block()
        
        # Expression statement
        return self.parse_expr_stmt()
    
    def parse_block(self):
        """
        Block = "{" { Statement } "}"
        """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('{', "Esperado '{'")
        
        statements = []
        while not self.check_value('}') and self.current_token():
            try:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            except ParseError:
                self.synchronize()
        
        self.consume_value('}', "Esperado '}'")
        
        return BlockNode(statements, linha, coluna)
    
    def parse_if_stmt(self):
        """
        IfStmt = "if" "(" Expr ")" Block ["else" (Block | IfStmt)]
        """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('if')
        self.consume_value('(', "Esperado '(' após 'if'")
        
        condition = self.parse_expr()
        
        self.consume_value(')', "Esperado ')' após condição")
        
        then_branch = self.parse_block()
        
        else_branch = None
        if self.check('KEYWORD') and self.check_value('else'):
            self.advance()  # consome 'else'
            
            # else if
            if self.check('KEYWORD') and self.check_value('if'):
                else_branch = self.parse_if_stmt()
            else:
                else_branch = self.parse_block()
        
        return IfNode(condition, then_branch, else_branch, linha, coluna)
    
    def parse_for_stmt(self):
        """
        ForStmt = "for" "(" ForInit ";" [Expr] ";" ForUpdate ")" Block
        """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('for')
        self.consume_value('(', "Esperado '(' após 'for'")
        
        # Inicialização
        init = None
        if not self.check_value(';'):
            if self.check('KEYWORD'):
                init = self.parse_var_decl()
            else:
                init = self.parse_expr()
                self.consume_value(';')
        else:
            self.advance()  # consome ';'
        
        # Condição
        condition = None
        if not self.check_value(';'):
            condition = self.parse_expr()
        self.consume_value(';')
        
        # Update
        update = []
        if not self.check_value(')'):
            update.append(self.parse_expr())
            while self.check_value(','):
                self.advance()
                update.append(self.parse_expr())
        self.consume_value(')')
        
        # Corpo
        body = self.parse_block()
        
        return ForNode(init, condition, update, body, linha, coluna)
    
    def parse_return_stmt(self):
        """ReturnStmt = "return" [Expr] ";" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('return')
        
        value = None
        if not self.check_value(';'):
            value = self.parse_expr()
        
        self.consume_value(';', "Esperado ';' após return")
        
        return ReturnNode(value, linha, coluna)
    
    def parse_break_stmt(self):
        """BreakStmt = "break" ";" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('break')
        self.consume_value(';', "Esperado ';' após break")
        
        return BreakNode(linha, coluna)
    
    def parse_continue_stmt(self):
        """ContinueStmt = "continue" ";" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('continue')
        self.consume_value(';', "Esperado ';' após continue")
        
        return ContinueNode(linha, coluna)
    
    def parse_print_stmt(self):
        """PrintStmt = "print" "(" Expr ")" ";" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('print')
        self.consume_value('(', "Esperado '(' após 'print'")
        
        expr = self.parse_expr()
        
        self.consume_value(')', "Esperado ')' após expressão")
        self.consume_value(';', "Esperado ';' após print")
        
        return PrintNode(expr, linha, coluna)
    
    def parse_expr_stmt(self):
        """ExprStmt = Expr ";" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        expr = self.parse_expr()
        self.consume_value(';', "Esperado ';' após expressão")
        
        return ExprStmtNode(expr, linha, coluna)
    
    # ============= EXPRESSÕES (com precedência) =============
    
    def parse_expr(self):
        """Expr = Assignment"""
        return self.parse_assignment()
    
    def parse_assignment(self):
        """Assignment = OrExpr [AssignOp Assignment]"""
        expr = self.parse_or_expr()
        
        # Verifica operadores de atribuição
        if self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['=', '+=', '-=', '*=', '/=', '%=']:
                token = self.current_token()
                self.advance()
                value = self.parse_assignment()  # Associatividade à direita
                return AssignmentNode(expr, op, value, token.linha, token.coluna)
        
        return expr
    
    def parse_or_expr(self):
        """OrExpr = AndExpr { "||" AndExpr }"""
        left = self.parse_and_expr()
        
        while self.check('OPERATOR') and self.check_value('||'):
            token = self.current_token()
            op = self.advance().lexema
            right = self.parse_and_expr()
            left = BinaryOpNode(left, op, right, token.linha, token.coluna)
        
        return left
    
    def parse_and_expr(self):
        """AndExpr = Equality { "&&" Equality }"""
        left = self.parse_equality()
        
        while self.check('OPERATOR') and self.check_value('&&'):
            token = self.current_token()
            op = self.advance().lexema
            right = self.parse_equality()
            left = BinaryOpNode(left, op, right, token.linha, token.coluna)
        
        return left
    
    def parse_equality(self):
        """Equality = RelExpr { ("==" | "!=") RelExpr }"""
        left = self.parse_rel_expr()
        
        while self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['==', '!=']:
                token = self.current_token()
                self.advance()
                right = self.parse_rel_expr()
                left = BinaryOpNode(left, op, right, token.linha, token.coluna)
            else:
                break
        
        return left
    
    def parse_rel_expr(self):
        """RelExpr = AddExpr { ("<" | ">" | "<=" | ">=") AddExpr }"""
        left = self.parse_add_expr()
        
        while self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['<', '>', '<=', '>=']:
                token = self.current_token()
                self.advance()
                right = self.parse_add_expr()
                left = BinaryOpNode(left, op, right, token.linha, token.coluna)
            else:
                break
        
        return left
    
    def parse_add_expr(self):
        """AddExpr = MulExpr { ("+" | "-") MulExpr }"""
        left = self.parse_mul_expr()
        
        while self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['+', '-']:
                token = self.current_token()
                self.advance()
                right = self.parse_mul_expr()
                left = BinaryOpNode(left, op, right, token.linha, token.coluna)
            else:
                break
        
        return left
    
    def parse_mul_expr(self):
        """MulExpr = UnaryExpr { ("*" | "/" | "%") UnaryExpr }"""
        left = self.parse_unary_expr()
        
        while self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['*', '/', '%']:
                token = self.current_token()
                self.advance()
                right = self.parse_unary_expr()
                left = BinaryOpNode(left, op, right, token.linha, token.coluna)
            else:
                break
        
        return left
    
    def parse_unary_expr(self):
        """UnaryExpr = ("-" | "!" | "++" | "--") UnaryExpr | PostfixExpr"""
        if self.check('OPERATOR'):
            op = self.current_token().lexema
            if op in ['-', '!', '++', '--']:
                token = self.current_token()
                self.advance()
                operand = self.parse_unary_expr()
                return UnaryOpNode(op, operand, token.linha, token.coluna)
        
        return self.parse_postfix_expr()
    
    def parse_postfix_expr(self):
        """PostfixExpr = Primary { "[" Expr "]" | "(" [ArgList] ")" | "++" | "--" }"""
        expr = self.parse_primary()
        
        while True:
            token = self.current_token()
            if not token:
                break
            
            # Array index
            if token.tipo == 'DELIMITERS' and token.lexema == '[':
                self.advance()
                index = self.parse_expr()
                self.consume_value(']', "Esperado ']'")
                expr = IndexNode(expr, index, token.linha, token.coluna)
            
            # Function call
            elif token.tipo == 'DELIMITERS' and token.lexema == '(':
                self.advance()
                args = []
                if not self.check_value(')'):
                    args = self.parse_arg_list()
                self.consume_value(')', "Esperado ')'")
                expr = CallNode(expr, args, token.linha, token.coluna)
            
            # Postfix ++ ou --
            elif token.tipo == 'OPERATOR' and token.lexema in ['++', '--']:
                op = self.advance().lexema
                expr = UnaryOpNode(op + '_post', expr, token.linha, token.coluna)
            
            else:
                break
        
        return expr
    
    def parse_arg_list(self):
        """ArgList = Expr { "," Expr }"""
        args = [self.parse_expr()]
        
        while self.check_value(','):
            self.advance()
            args.append(self.parse_expr())
        
        return args
    
    def parse_primary(self):
        """
        Primary = NUMBER | STRING | "true" | "false" | "null" |
                 IDENT | ArrayLiteral | "(" Expr ")"
        """
        token = self.current_token()
        if not token:
            raise ParseError("Expressão esperada, encontrado fim do arquivo")
        
        linha, coluna = token.linha, token.coluna
        
        # Números
        if token.tipo == 'NUMBER':
            self.advance()
            return LiteralNode(token.valor, 'number', linha, coluna)
        
        # Strings
        if token.tipo == 'STRING':
            self.advance()
            return LiteralNode(token.valor, 'string', linha, coluna)
        
        # Booleanos e null
        if token.tipo == 'KEYWORD':
            if token.lexema == 'true':
                self.advance()
                return LiteralNode(True, 'bool', linha, coluna)
            elif token.lexema == 'false':
                self.advance()
                return LiteralNode(False, 'bool', linha, coluna)
            elif token.lexema == 'null':
                self.advance()
                return LiteralNode(None, 'null', linha, coluna)
        
        # Identificadores
        if token.tipo == 'IDENT':
            name = self.advance().lexema
            return IdentifierNode(name, linha, coluna)
        
        # Array literal
        if token.tipo == 'DELIMITERS' and token.lexema == '[':
            return self.parse_array_literal()
        
        # Expressão entre parênteses
        if token.tipo == 'DELIMITERS' and token.lexema == '(':
            self.advance()
            expr = self.parse_expr()
            self.consume_value(')', "Esperado ')' após expressão")
            return expr
        
        raise ParseError(f"Expressão inesperada: {token.tipo} '{token.lexema}'", token)
    
    def parse_array_literal(self):
        """ArrayLiteral = "[" [Expr {"," Expr}] "]" """
        token = self.current_token()
        linha, coluna = token.linha, token.coluna
        
        self.consume_value('[')
        
        elements = []
        if not self.check_value(']'):
            elements.append(self.parse_expr())
            while self.check_value(','):
                self.advance()
                elements.append(self.parse_expr())
        
        self.consume_value(']', "Esperado ']'")
        
        return ArrayLiteralNode(elements, linha, coluna)

# ============= FUNÇÃO PRINCIPAL DE TESTE =============

def main():
    """Testa o parser com código SimplePOO"""
    
    codigo = '''
    int x = 10;
    float y = 3.14;
    
    function soma(a, b) {
        return a + b;
    }
    
    function teste() {
        var resultado = soma(x, y);
        
        if (resultado > 10) {
            print("Grande!");
        } else {
            print("Pequeno");
        }
        
        for (var i = 0; i < 5; i++) {
            print(i);
        }
        
        return resultado;
    }
    '''
    
    print("="*70)
    print("PARSER RECURSIVO DESCENDENTE - SIMPLEPOO")
    print("="*70)
    print("\nCódigo a parsear:")
    print("-"*70)
    print(codigo)
    print("-"*70)
    
    # Lexer
    lexer = EnhancedLexer()
    tokens, erros_lex = lexer.tokenize(codigo)
    
    if erros_lex:
        print(f"\n❌ {len(erros_lex)} erro(s) léxico(s) encontrado(s)")
        return
    
    print(f"\n✅ Análise léxica: {len(tokens)} tokens")
    
    # Parser
    parser = Parser(lexer)
    ast = parser.parse()
    
    if not parser.errors:
        print("\n" + "="*70)
        print("ÁRVORE SINTÁTICA ABSTRATA (AST)")
        print("="*70)
        print_ast(ast)
        print("="*70)
    
    return ast

if __name__ == "__main__":
    main()
