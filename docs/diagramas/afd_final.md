# Diagramas dos Autômatos Determinísticos da Linguagem SimplePoo

Cada autômato descrito abaixo foi construído manualmente utilizando tabelas
explícitas de transição. Os diagramas em Mermaid documentam o comportamento
de cada categoria de token sem depender de expressões regulares.

## KEYWORD (palavras reservadas)

```mermaid
stateDiagram-v2
    [*] --> K0
    K0 --> K_if1: "i"
    K_if1 --> K_if2: "f"
    K_if2 --> [*]
    K0 --> K_var1: "v"
    K_var1 --> K_var2: "a"
    K_var2 --> K_var3: "r"
    K_var3 --> [*]
    K0 --> K_else1: "e"
    K_else1 --> K_else2: "l"
    K_else2 --> K_else3: "s"
    K_else3 --> K_else4: "e"
    K_else4 --> [*]
```

Cada caminho separado representa uma palavra reservada. O autômato real contém
transições para todas as 37 keywords definidas na especificação.

## IDENTIFIER (identificadores)

```mermaid
stateDiagram-v2
    [*] --> I0
    I0 --> I1: letra/_
    I1 --> I1: letra/dígito/_
    I1 --> [*]
```

## INT_LITERAL (literais inteiros)

```mermaid
stateDiagram-v2
    [*] --> N0
    N0 --> N1: "0"
    N0 --> N2: [1-9]
    N1 --> [*]
    N2 --> N2: [0-9]
    N2 --> [*]
```

## FLOAT_LITERAL (literais decimais)

```mermaid
stateDiagram-v2
    [*] --> F0
    F0 --> F1: "0"
    F0 --> F2: [1-9]
    F1 --> F3: "."
    F2 --> F2: [0-9]
    F2 --> F3: "."
    F3 --> F4: [0-9]
    F4 --> F4: [0-9]
    F4 --> [*]
```

## SCIENTIFIC_LITERAL (notação científica)

```mermaid
stateDiagram-v2
    [*] --> S0
    S0 --> S1: "0"
    S0 --> S2: [1-9]
    S1 --> S3: "."
    S1 --> S5: "e/E"
    S1 --> S2: [0-9]
    S2 --> S2: [0-9]
    S2 --> S3: "."
    S2 --> S5: "e/E"
    S3 --> S4: [0-9]
    S4 --> S4: [0-9]
    S4 --> S5: "e/E"
    S5 --> S6: "+/-"
    S5 --> S7: [0-9]
    S6 --> S7: [0-9]
    S7 --> S7: [0-9]
    S7 --> [*]
```

## STRING_DOUBLE / STRING_SINGLE (strings)

```mermaid
stateDiagram-v2
    [*] --> SD0
    SD0 --> SD1: "\""
    SD1 --> SD2: "\\"
    SD1 --> SD1: caractere != "\", quebra de linha
    SD1 --> SD3: "\""
    SD2 --> SD1: qualquer
    SD3 --> [*]
```

O autômato de aspas simples possui a mesma estrutura substituindo o delimitador.

## CHAR_LITERAL (caracteres)

```mermaid
stateDiagram-v2
    [*] --> C0
    C0 --> C1: "'"
    C1 --> C2: "\\"
    C1 --> C3: caractere != '\n', '\r', "'"
    C2 --> C3: qualquer
    C3 --> C4: "'"
    C4 --> [*]
```

## OPERATOR (operadores)

```mermaid
stateDiagram-v2
    [*] --> O0
    O0 --> O1: "="
    O1 --> O2: "="
    O2 --> [*]
    O0 --> O3: "+"
    O3 --> O4: "+"
    O4 --> [*]
    O0 --> O5: "!"
    O5 --> O6: "="
    O6 --> [*]
```

Os ramos representam os operadores compostos e simples. O autômato inclui
transições para os demais símbolos listados na especificação.

## DELIMITER (delimitadores)

```mermaid
stateDiagram-v2
    [*] --> D0
    D0 --> [*]: qualquer de (){}[];,.
```

## WHITESPACE (espaços em branco)

```mermaid
stateDiagram-v2
    [*] --> W0
    W0 --> W1: espaço/tab/\n/\r
    W1 --> W1: espaço/tab/\n/\r
    W1 --> [*]
```

## LINE_COMMENT (comentário de linha)

```mermaid
stateDiagram-v2
    [*] --> L0
    L0 --> L1: "/"
    L1 --> L2: "/"
    L2 --> L2: caractere != quebra de linha
    L2 --> L3: quebra de linha
    L3 --> [*]
```

## BLOCK_COMMENT (comentário de bloco)

```mermaid
stateDiagram-v2
    [*] --> B0
    B0 --> B1: "/"
    B1 --> B2: "*"
    B2 --> B2: qualquer
    B2 --> B3: "*"
    B3 --> B2: qualquer exceto "/"
    B3 --> B4: "/"
    B4 --> [*]
```

Cada um desses autômatos foi implementado na pasta `Compiladores/modulos_lexicos`
utilizando estruturas de dados explícitas, e os testes individuais podem ser
executados com `python -m unittest discover Compiladores/tests`.
