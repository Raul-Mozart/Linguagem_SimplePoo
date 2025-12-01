# 🌳 Parser Recursivo Descendente - SimplePOO

## ✅ Implementação Completa

Parser recursivo descendente com construção de AST (Árvore Sintática Abstrata) para a linguagem SimplePOO.

---

## 📁 Arquivos

### 1. **`ast_nodes.py`** - Nós da AST
Define todas as estruturas de dados para representar o programa:
- Nós de programa e declarações
- Nós de statements (if, for, return, etc.)
- Nós de expressões (binário, unário, chamadas, etc.)
- Nós literais (números, strings, identificadores)

### 2. **`parser.py`** - Parser Principal
Implementa o parsing recursivo descendente:
- Uma função para cada não-terminal da gramática
- Constrói AST durante o parsing
- Tratamento e recuperação de erros
- Interface simples com o lexer

---

## 🎯 Características Implementadas

### ✅ 1. **Parsing Recursivo Descendente**
- **Top-down**: Começa do símbolo inicial e desce na árvore
- **Preditivo**: Olha 1 token à frente para decidir
- **Uma função por não-terminal**: Estrutura clara e manutenível

### ✅ 2. **Construção de AST**
- AST construída **durante** o parsing (em tempo real)
- Representa apenas a estrutura semântica essencial
- Remove detalhes sintáticos irrelevantes (parênteses, palavras-chave, etc.)

### ✅ 3. **Precedência de Operadores**
Implementada através da hierarquia de funções:
```
Expr → Assignment      (menor precedência)
Assignment → OrExpr
OrExpr → AndExpr
AndExpr → Equality
Equality → RelExpr
RelExpr → AddExpr
AddExpr → MulExpr
MulExpr → UnaryExpr
UnaryExpr → PostfixExpr
PostfixExpr → Primary   (maior precedência)
```

### ✅ 4. **Tratamento de Erros**
- Mensagens claras com linha e coluna
- **Recuperação de erros**: Continua após encontrar erro
- **Synchronization**: Busca próximo ponto seguro

---

## 🚀 Como Usar

### Uso Básico

```python
from lexer_enhanced import EnhancedLexer
from parser import Parser
from ast_nodes import print_ast

# Código SimplePOO
codigo = '''
    int x = 10;
    function soma(a, b) {
        return a + b;
    }
'''

# 1. Análise Léxica
lexer = EnhancedLexer()
tokens, erros = lexer.tokenize(codigo)

# 2. Análise Sintática
parser = Parser(lexer)
ast = parser.parse()

# 3. Visualizar AST
if not parser.errors:
    print_ast(ast)
```

### Teste Rápido

```bash
cd parser
python parser.py
```

---

## 📖 Estrutura da Gramática

O parser implementa a gramática completa do SimplePOO:

### Declarações
```ebnf
Program       = { TopLevelDecl }
TopLevelDecl  = VarDecl | FuncDecl | Statement
VarDecl       = ("var"|"let"|"const"|Type) IDENT ["=" Expr] ";"
FuncDecl      = "function" IDENT "(" [ParamList] ")" Block
```

### Statements
```ebnf
Statement     = VarDecl | IfStmt | ForStmt | Block |
                ReturnStmt | BreakStmt | ContinueStmt |
                PrintStmt | ExprStmt

IfStmt        = "if" "(" Expr ")" Block ["else" (Block | IfStmt)]
ForStmt       = "for" "(" ForInit ";" [Expr] ";" ForUpdate ")" Block
ReturnStmt    = "return" [Expr] ";"
PrintStmt     = "print" "(" Expr ")" ";"
```

### Expressões (com precedência)
```ebnf
Expr          = Assignment
Assignment    = OrExpr [AssignOp Assignment]
OrExpr        = AndExpr { "||" AndExpr }
AndExpr       = Equality { "&&" Equality }
Equality      = RelExpr { ("==" | "!=") RelExpr }
RelExpr       = AddExpr { ("<" | ">" | "<=" | ">=") AddExpr }
AddExpr       = MulExpr { ("+" | "-") MulExpr }
MulExpr       = UnaryExpr { ("*" | "/" | "%") UnaryExpr }
UnaryExpr     = ("-" | "!" | "++" | "--") UnaryExpr | PostfixExpr
PostfixExpr   = Primary { "[" Expr "]" | "(" [ArgList] ")" | "++" | "--" }
Primary       = NUMBER | STRING | "true" | "false" | "null" |
                IDENT | ArrayLiteral | "(" Expr ")"
```

---

## 🌳 Exemplo de AST

### Código:
```javascript
int x = 10;
function soma(a, b) {
    return a + b;
}
```

### AST Gerada:
```
Program(2 declarations)
  ├─ VarDecl(x: int)
  │  └─ Literal(10)
  └─ FuncDecl(soma, 2 params)
     └─ Block(1 stmts)
        └─ Return
           └─ BinaryOp(+)
              ├─ Identifier(a)
              └─ Identifier(b)
```

---

## 🔧 Arquitetura do Parser

### Métodos Auxiliares
```python
current_token()    # Token atual
peek(offset)       # Olha à frente
advance()          # Consome token
check(tipo)        # Verifica tipo
match(*tipos)      # Verifica múltiplos tipos
consume(tipo)      # Consome ou erro
```

### Funções de Parsing
Cada não-terminal tem sua função:

```python
parse()                  # Program
parse_top_level_decl()   # TopLevelDecl
parse_var_decl()         # VarDecl
parse_func_decl()        # FuncDecl
parse_statement()        # Statement
parse_if_stmt()          # IfStmt
parse_for_stmt()         # ForStmt
parse_block()            # Block
parse_expr()             # Expr
parse_assignment()       # Assignment
parse_or_expr()          # OrExpr
...                      # etc.
```

### Precedência de Operadores
```
Nível 1 (mais baixo): =, +=, -=, *=, /=, %=
Nível 2: ||
Nível 3: &&
Nível 4: ==, !=
Nível 5: <, >, <=, >=
Nível 6: +, -
Nível 7: *, /, %
Nível 8: !, -, ++ (unário)
Nível 9 (mais alto): ++, -- (pós-fixo), chamada, índice
```

---

## 💡 Princípios de Implementação

### 1. **Correspondência Direta Gramática → Código**
```ebnf
# Gramática
IfStmt = "if" "(" Expr ")" Block ["else" (Block | IfStmt)]

# Código Python
def parse_if_stmt(self):
    self.consume_value('if')
    self.consume_value('(')
    condition = self.parse_expr()
    self.consume_value(')')
    then_branch = self.parse_block()
    
    else_branch = None
    if self.check_value('else'):
        self.advance()
        else_branch = self.parse_block() or self.parse_if_stmt()
    
    return IfNode(condition, then_branch, else_branch)
```

### 2. **Recursão para Estruturas Aninhadas**
- Expressões recursivas: `Primary` pode conter `Expr`
- Statements recursivos: `Block` pode conter `Block`
- Função recursiva: Chamada naturalmente

### 3. **Construção Incremental da AST**
- Cada função retorna um nó da AST
- Nós são compostos hierarquicamente
- Resultado final: Árvore completa

---

## 🎓 Conceitos Aplicados

### Do Material Teórico:
✅ **Parsing Recursivo Descendente**
- Técnica top-down
- Previsão com 1 token de lookahead
- Função por não-terminal

✅ **AST (Abstract Syntax Tree)**
- Representação estrutural do programa
- Remove detalhes sintáticos
- Base para análise semântica

✅ **Precedência de Operadores**
- Implementada na hierarquia de funções
- Naturalmente capturada na AST

✅ **Tratamento de Erros**
- Mensagens claras
- Recuperação (synchronization)
- Continue após erro

---

## 📊 Saída do Parser

### Exemplo Completo:
```javascript
int x = 10;

function parImpar(num) {
    if (num % 2 == 0) {
        return "É par";
    } else {
        return "É impar";
    }
}
```

### Resultado:
```
🔍 Iniciando parsing...
✅ Parsing bem-sucedido! 2 declarações

ÁRVORE SINTÁTICA ABSTRATA (AST)
======================================================================
Program(2 declarations)
  VarDecl(x: int)
    initializer:
      Literal(10)
  FuncDecl(parImpar, 1 params)
    params: ['num']
    Block(1 stmts)
      If(has_else=True)
        condition:
          BinaryOp(==)
            BinaryOp(%)
              Identifier(num)
              Literal(2)
            Literal(0)
        then:
          Block(1 stmts)
            Return(True)
              Literal('É par')
        else:
          Block(1 stmts)
            Return(True)
              Literal('É impar')
```

---

## 🚀 Próximos Passos

O parser está pronto para:
1. ✅ **Análise Semântica** - Verificação de tipos, escopo, etc.
2. ✅ **Tabela de Símbolos** - Gerenciamento de identificadores
3. ✅ **Geração de Código** - Compilação para bytecode/assembly
4. ✅ **Interpretação** - Execução direta da AST

---

## 🎯 Status

**✅ IMPLEMENTAÇÃO COMPLETA**

- ✅ Parser recursivo descendente
- ✅ Construção de AST
- ✅ Precedência de operadores
- ✅ Tratamento de erros
- ✅ Recuperação de erros
- ✅ Suporte completo à gramática SimplePOO
- ✅ Testado e funcional

---

**Versão:** 1.0 - Completa  
**Data:** Novembro 2025  
**Base:** Material teórico de Compiladores
