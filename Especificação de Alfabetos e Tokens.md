# Especificação completa do alfabeto da linguagem

Σ = { A..Z, a..z, 0..9, _, +, -, *, /, %, =, <, >, !, &, |, ^, ~, ?, :, ., ,, ;, (, ), [, ], {, }, ", ', `, /, *, \\, espaço, tab, newline, carriage return }

## Definição formal de todos os tipos de tokens

### IDENT
Identificador → regex: `[A-Za-z_][A-Za-z0-9_]*`

### KEYWORD
Palavras-reservadas → lista: `class`, `struct`, `interface`, `extends`, `implements`, `new`, `this`, `super`, `function`, `void`, `var`, `let`, `const`, `return`, `if`, `else`, `switch`, `case`, `default`, `break`, `continue`, `for`, `foreach`, `while`, `do`, `true`, `false`, `null`, `public`, `private`, `protected`, `static`

### NUMBER
Literais numéricos
- Decimal: `\d+(\.\d+)?([eE][+-]?\d+)?`

### STRING
Literais string
- Aspas duplas: `"(?:\\.|[^"\\])*"`
- Aspas simples: `'(?:\\.|[^'\\])*'`

### CHAR
Literal caractere: `'(?:\\.|[^'\\])'`

### COMMENT
- Comentário de linha: `\/\/[^]*`
- Comentário de bloco: `/\*(?:.|\n|\r)*?\*/`

### OPERATOR
- Operadores compostos (prioridade): `==` `!=` `<=` `>=` `&&` `||` `++` `--` `+=` `-=` `*=` `/=` `%=` `<<=` `>>=` `&=` `|=` `^=` `=>` `->` `::`
- Operadores simples: `+` `-` `*` `/` `%` `=` `<` `>` `!` `&` `|` `^` `~` `?` `:`

### DELIMITERS
`(` `)` `{` `}` `[` `]` `;` `,` `.`

### WHITESPACE
`[ \t\r\n]+` → ignorado (conta linha/coluna)

### ERROR_LEX
Qualquer caractere não reconhecido → erro léxico

## Exemplos concretos de programas válidos na linguagem

### 1)
float numero = 10.0;
function parImpar(num)
{
if (num % 2 == 0)
{
return "É par";
} else
{
return "É impar"
}
}
print(parImpar(numero));

### 2)
list numeros = [1,2,3,4,5];
for (var i = 0; i < 5; i = i + 1)
{
numeros[i] = numeros[i] + 1;
}
print(numeros)
