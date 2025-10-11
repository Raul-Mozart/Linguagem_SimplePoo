# Gramática Formal da Linguagem SimplePoo

## 1. Primeira Versão da Gramática Formal

### Definição Completa G = (V, T, P, S)

**Conjunto de Variáveis (V)**:
```
V = {Program, TopLevelDecl, VarDecl, FuncDecl, ParamList, Block, Statement,
     ExprStmt, PrintStmt, ReturnStmt, BreakStmt, ContinueStmt, IfStmt,
     ForStmt, ForInit, ForUpdate, Expr, Assignment, AssignOp, OrExpr,
     AndExpr, Equality, RelExpr, AddExpr, MulExpr, UnaryExpr, PostfixExpr,
     Primary, ArgList, ArrayLiteral, Type}
```

**Conjunto de Terminais (T)**:
```
T = {var, let, const, function, if, else, for, return, break, continue,
     print, true, false, null, int, float, string, bool, list,
     =, +=, -=, *=, /=, %=, ==, !=, <, >, <=, >=, &&, ||, ++, --, 
     +, -, *, /, %, !, (, ), {, }, [, ], ;, ",", ., 
     IDENT, NUMBER, STRING}
```

**Símbolo Inicial**: S = Program

### Regras de Produção (P)

**Estrutura do Programa**:
- Program → TopLevelDecl Program | ε
- TopLevelDecl → VarDecl | FuncDecl | Statement

**Declarações de Variáveis**:
- VarDecl → var IDENT = Expr ; | var IDENT ;
- VarDecl → let IDENT = Expr ; | let IDENT ;
- VarDecl → const IDENT = Expr ;
- VarDecl → Type IDENT = Expr ; | Type IDENT ;
- Type → int | float | string | bool | list

**Declarações de Funções**:
- FuncDecl → function IDENT ( ParamList ) Block
- FuncDecl → function IDENT ( ) Block
- ParamList → IDENT , ParamList | IDENT

**Blocos e Comandos**:
- Block → { Statement Block } | { }
- Statement → VarDecl | IfStmt | ForStmt | ExprStmt | ReturnStmt | BreakStmt | ContinueStmt | PrintStmt | Block

**Comandos Específicos**:
- ExprStmt → Expr ;
- PrintStmt → print ( Expr ) ;
- ReturnStmt → return Expr ; | return ;
- BreakStmt → break ;
- ContinueStmt → continue ;

**Estruturas Condicionais**:
- IfStmt → if ( Expr ) Block else Block
- IfStmt → if ( Expr ) Block else IfStmt
- IfStmt → if ( Expr ) Block

**Estruturas de Repetição**:
- ForStmt → for ( ForInit ; Expr ; ForUpdate ) Block
- ForStmt → for ( ForInit ; ; ForUpdate ) Block
- ForInit → VarDecl | ExprStmt | ε
- ForUpdate → Expr , ForUpdate | Expr | ε

**Expressões (Hierarquia de Precedência)**:
- Expr → Assignment
- Assignment → OrExpr AssignOp Assignment | OrExpr
- AssignOp → = | += | -= | *= | /= | %=
- OrExpr → AndExpr || OrExpr | AndExpr
- AndExpr → Equality && AndExpr | Equality
- Equality → RelExpr == Equality | RelExpr != Equality | RelExpr
- RelExpr → AddExpr < RelExpr | AddExpr > RelExpr | AddExpr <= RelExpr | AddExpr >= RelExpr | AddExpr
- AddExpr → MulExpr + AddExpr | MulExpr - AddExpr | MulExpr
- MulExpr → UnaryExpr * MulExpr | UnaryExpr / MulExpr | UnaryExpr % MulExpr | UnaryExpr
- UnaryExpr → - UnaryExpr | ! UnaryExpr | ++ UnaryExpr | -- UnaryExpr | PostfixExpr
- PostfixExpr → Primary [ Expr ] PostfixExpr | Primary ( ArgList ) PostfixExpr | Primary ++ | Primary -- | Primary
- Primary → NUMBER | STRING | true | false | null | IDENT | ArrayLiteral | ( Expr )

**Elementos Auxiliares**:
- ArgList → Expr , ArgList | Expr | ε
- ArrayLiteral → [ ArgList ]

---

## 2. Classificação na Hierarquia de Chomsky

A gramática SimplePoo é classificada como **Tipo 2 (Livre de Contexto)**.

**Justificativa**:
- Todas as produções seguem a forma A → α (lado esquerdo contém apenas um não-terminal)
- Não há dependências contextuais nas regras de produção
- A gramática gera linguagem que não é regular devido a estruturas aninhadas (blocos, parênteses balanceados, arrays)
- É reconhecível por autômato de pilha

**Verificação**:
- ✅ **Não é Tipo 3 (Regular)**: estruturas como `if-else` aninhados e arrays com balanceamento de `[]` não são expressáveis por gramáticas regulares
- ✅ **É Tipo 2 (Livre de Contexto)**: todas as regras seguem o formato A → α
- ❌ **Não precisa ser Tipo 1 (Sensível ao Contexto)**: não há regras do tipo αAβ → αγβ
- ❌ **Não precisa ser Tipo 0 (Irrestrita)**: a gramática é bem estruturada

**Limitações**:

A gramática não captura restrições como:
- Declaração de variável antes de uso
- Compatibilidade de tipos
- Escopo de variáveis

Essas verificações são delegadas à **análise semântica**, usando tabela de símbolos e verificador de tipos.

---

## 3. Exemplos de Derivações

### Exemplo 1: Declaração Tipada

**Código**:
```
float numero = 10.0;
```

**Derivação**:
```
Program
⇒ TopLevelDecl Program
⇒ VarDecl Program
⇒ Type IDENT = Expr ; Program
⇒ float numero = Expr ; Program
⇒ float numero = Assignment ; Program
⇒ float numero = OrExpr ; Program
⇒ float numero = AndExpr ; Program
⇒ float numero = Equality ; Program
⇒ float numero = RelExpr ; Program
⇒ float numero = AddExpr ; Program
⇒ float numero = MulExpr ; Program
⇒ float numero = UnaryExpr ; Program
⇒ float numero = PostfixExpr ; Program
⇒ float numero = Primary ; Program
⇒ float numero = NUMBER ; Program
⇒ float numero = 10.0 ; ε
⇒ float numero = 10.0;
```

**Árvore Sintática**:
```
Program
└── VarDecl
    ├── Type: float
    ├── IDENT: numero
    ├── =
    ├── Expr → NUMBER: 10.0
    └── ;
```

---

### Exemplo 2: Função com Condicional

**Código**:
```
function parImpar(num) {
  if (num % 2 == 0) {
    return "É par";
  } else {
    return "É impar";
  }
}
```

**Derivação (essencial)**:
```
Program
⇒ TopLevelDecl Program
⇒ FuncDecl Program
⇒ function IDENT ( ParamList ) Block Program
⇒ function parImpar ( num ) Block Program
⇒ function parImpar ( num ) { Statement Block } Program
⇒ function parImpar ( num ) { IfStmt Block } Program
⇒ function parImpar ( num ) { if ( Expr ) Block else Block Block } Program
⇒ ... (Expr deriva para: num % 2 == 0)
⇒ ... (primeiro Block: return "É par";)
⇒ ... (segundo Block: return "É impar";)
```

**Árvore Sintática**:
```
FuncDecl
├── function
├── IDENT: parImpar
├── ParamList: num
└── Block
    └── IfStmt
        ├── Condition: (num % 2 == 0)
        ├── Then: Block
        │   └── ReturnStmt: "É par"
        └── Else: Block
            └── ReturnStmt: "É impar"
```

---

### Exemplo 3: Loop For com Array

**Código**:
```
for (var i = 0; i < 5; i = i + 1) {
  numeros[i] = numeros[i] + 1;
}
```

**Derivação (estrutural)**:
```
Program
⇒ TopLevelDecl Program
⇒ Statement Program
⇒ ForStmt Program
⇒ for ( ForInit ; Expr ; ForUpdate ) Block Program
⇒ for ( VarDecl ; Expr ; ForUpdate ) Block Program
⇒ for ( var i = 0 ; i < 5 ; i = i + 1 ) Block Program
⇒ for ( var i = 0 ; i < 5 ; i = i + 1 ) { Statement Block } Program
⇒ for ( var i = 0 ; i < 5 ; i = i + 1 ) { ExprStmt Block } Program
⇒ ... (ExprStmt deriva para: numeros[i] = numeros[i] + 1;)
```

**Árvore Sintática**:
```
ForStmt
├── ForInit: var i = 0
├── Condition: i < 5
├── ForUpdate: i = i + 1
└── Block
    └── ExprStmt
        └── Assignment: numeros[i] = numeros[i] + 1
```

---

### Exemplo 4: Chamada de Função

**Código**:
```
print(parImpar(numero));
```

**Derivação**:
```
Program
⇒ TopLevelDecl Program
⇒ Statement Program
⇒ PrintStmt Program
⇒ print ( Expr ) ; Program
⇒ print ( Assignment ) ; Program
⇒ print ( OrExpr ) ; Program
⇒ print ( AndExpr ) ; Program
⇒ print ( Equality ) ; Program
⇒ print ( RelExpr ) ; Program
⇒ print ( AddExpr ) ; Program
⇒ print ( MulExpr ) ; Program
⇒ print ( UnaryExpr ) ; Program
⇒ print ( PostfixExpr ) ; Program
⇒ print ( Primary ( ArgList ) PostfixExpr ) ; Program
⇒ print ( IDENT ( Expr ) PostfixExpr ) ; Program
⇒ print ( parImpar ( Primary ) Primary ) ; Program
⇒ print ( parImpar ( numero ) ) ; ε
⇒ print(parImpar(numero));
```

**Árvore Sintática**:
```
PrintStmt
└── Expr
    └── PostfixExpr (chamada)
        ├── IDENT: parImpar
        └── ArgList
            └── IDENT: numero
```

---

## 4. Análise de Ambiguidades e Estratégias de Resolução

### Ambiguidade 1: Dangling-Else

**Problema**:
```
if (a > 0)
  if (b > 0)
    print("Positivos");
else  // Pertence ao if interno ou externo?
  print("Negativo");
```

**Estratégias de Resolução**:

1. **Regra de associação** (implementada): `else` sempre se associa ao `if` mais próximo não pareado
   - Ordem das regras na gramática força associação correta:
   ```
   IfStmt → if ( Expr ) Block else IfStmt
   IfStmt → if ( Expr ) Block else Block
   IfStmt → if ( Expr ) Block
   ```

2. **Reescrita da gramática** (alternativa): separar statements com e sem else
   ```
   StatementWithElse → if ( Expr ) StatementWithElse else StatementWithElse
   StatementNoElse → if ( Expr ) Statement
   StatementNoElse → if ( Expr ) StatementWithElse else StatementNoElse
   ```

3. **Resolução no parser**: usar diretivas de precedência em geradores como YACC

---

### Ambiguidade 2: Precedência de Operadores

**Problema**: expressões como `2 + 3 * 4` podem ser interpretadas como `(2 + 3) * 4 = 20` ou `2 + (3 * 4) = 14`.

**Solução**: hierarquia de não-terminais reflete precedência:

1. Atribuição: `=, +=, -=, *=, /=, %=` (mais baixa)
2. OR lógico: `||`
3. AND lógico: `&&`
4. Igualdade: `==, !=`
5. Relacional: `<, >, <=, >=`
6. Adição/Subtração: `+, -`
7. Multiplicação/Divisão/Módulo: `*, /, %`
8. Unários: `-, !, ++, --`
9. Pós-fixos: `++, --`, `[]`, `()`
10. Primários: literais, identificadores, `()` (mais alta)

**Resultado**: `2 + 3 * 4` sempre deriva como `2 + (3 * 4) = 14`

---

### Ambiguidade 3: Associatividade

**Problema**: como interpretar `a + b + c` ou `a = b = 5`?

**Solução**:
- **Operadores aritméticos e lógicos**: associativos à **esquerda**
  - `a + b + c` = `(a + b) + c`
  - Regra: `AddExpr → MulExpr + AddExpr` (recursão à direita força associatividade esquerda)

- **Atribuição**: associativa à **direita**
  - `a = b = 5` = `a = (b = 5)`
  - Regra: `Assignment → OrExpr AssignOp Assignment`

- **Comparações**: não-encadeáveis
  - `a < b < c` gera erro (requer `(a < b) && (b < c)`)

---

### Ambiguidade 4: Declaração vs Expressão

**Problema**: distinguir `int x` (declaração) de expressão iniciada por identificador.

**Solução**:
- Tokens `int`, `float`, `string`, `bool`, `list` são **keywords distintas**
- Lexer classifica como `TYPE`, não como `IDENT`
- Regras separadas eliminam conflito:
  ```
  VarDecl → Type IDENT ...
  ExprStmt → Expr ;
  ```
- `Type` nunca pode iniciar uma expressão

---

### Ambiguidade 5: Chamadas de Função vs Acesso a Array

**Problema**: distinguir `foo()` (chamada) de `foo[0]` (indexação).

**Solução**:
- Ambos tratados como `PostfixExpr`
- Regra: `PostfixExpr → Primary ( ArgList ) PostfixExpr | Primary [ Expr ] PostfixExpr | Primary`
- Parser decide pelo próximo token:
  - `(` → chamada de função
  - `[` → acesso a array
- Encadeamento permitido: `foo()[0]` ou `arr[0]()`