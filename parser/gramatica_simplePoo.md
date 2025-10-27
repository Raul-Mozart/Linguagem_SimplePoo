# 💡 Definição Formal da Gramática SimplePoo

G = (V, Σ, P, S)

onde:

* **V** (variáveis / não-terminais):
  `{Program, TopLevelDecl, VarDecl, FuncDecl, ParamList, Block, Statement, ExprStmt, PrintStmt, ReturnStmt, BreakStmt, ContinueStmt, IfStmt, ForStmt, ForInit, ForUpdate, Expr, Assignment, AssignOp, OrExpr, AndExpr, Equality, RelExpr, AddExpr, MulExpr, UnaryExpr, PostfixExpr, Primary, ArgList, ArrayLiteral, Type}`

* **Σ** (terminais):
  Palavras reservadas, símbolos e identificadores:
  `{var, let, const, function, if, else, for, return, break, continue, print, true, false, null, int, float, string, bool, list, =, +=, -=, *=, /=, %=, ==, !=, <, >, <=, >=, &&, ||, ++, --, +, -, *, /, %, !, (, ), {, }, [, ], ;, ",", ., IDENT, NUMBER, STRING}`

* **S** (símbolo inicial):
  `Program`

* **P** (regras de produção):
  O conjunto de produções segue abaixo, no formato EBNF.

---

## Gramática em EBNF (Extended Backus–Naur Form)

```ebnf
Program       = { TopLevelDecl } .

TopLevelDecl  = VarDecl | FuncDecl | Statement .

VarDecl       = "var" IDENT [ "=" Expr ] ";"
              | "let" IDENT [ "=" Expr ] ";"
              | "const" IDENT "=" Expr ";"
              | Type IDENT [ "=" Expr ] ";" .

Type          = "int" | "float" | "string" | "bool" | "list" .

FuncDecl      = "function" IDENT "(" [ ParamList ] ")" Block .

ParamList     = IDENT { "," IDENT } .

Block         = "{" { Statement } "}" .

Statement     = VarDecl
              | IfStmt
              | ForStmt
              | ExprStmt
              | ReturnStmt
              | BreakStmt
              | ContinueStmt
              | PrintStmt
              | Block .

ExprStmt      = Expr ";" .

PrintStmt     = "print" "(" Expr ")" ";" .

ReturnStmt    = "return" [ Expr ] ";" .

BreakStmt     = "break" ";" .

ContinueStmt  = "continue" ";" .

IfStmt        = "if" "(" Expr ")" Block [ "else" ( Block | IfStmt ) ] .

ForStmt       = "for" "(" ForInit ";" [ Expr ] ";" ForUpdate ")" Block .

ForInit       = VarDecl | ExprStmt | ε .

ForUpdate     = Expr { "," Expr } | ε .

Expr          = Assignment .

Assignment    = OrExpr [ AssignOp Assignment ] .

AssignOp      = "=" | "+=" | "-=" | "*=" | "/=" | "%=" .

OrExpr        = AndExpr { "||" AndExpr } .

AndExpr       = Equality { "&&" Equality } .

Equality      = RelExpr { ( "==" | "!=" ) RelExpr } .

RelExpr       = AddExpr { ( "<" | ">" | "<=" | ">=" ) AddExpr } .

AddExpr       = MulExpr { ( "+" | "-" ) MulExpr } .

MulExpr       = UnaryExpr { ( "*" | "/" | "%" ) UnaryExpr } .

UnaryExpr     = ( "-" | "!" | "++" | "--" ) UnaryExpr
              | PostfixExpr .

PostfixExpr   = Primary { "[" Expr "]" | "(" [ ArgList ] ")" | "++" | "--" } .

Primary       = NUMBER
              | STRING
              | "true"
              | "false"
              | "null"
              | IDENT
              | ArrayLiteral
              | "(" Expr ")" .

ArgList       = Expr { "," Expr } .

ArrayLiteral  = "[" [ ArgList ] "]" .

IDENT         = Letter { Letter | Digit } .
NUMBER        = Digit { Digit } [ "." { Digit } ] .
STRING        = '"' { Character } '"' .
Digit         = "0" | "1" | ... | "9" .
Letter        = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z" | "_" .
Character     = any printable ASCII character except '"' and '\' .
```
