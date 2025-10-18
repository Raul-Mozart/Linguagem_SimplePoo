# Analisador Léxico - Linguagem SimplePoo

Este diretório contém o analisador léxico (lexer) para a linguagem SimplePoo, implementado usando múltiplos Autômatos Finitos Determinísticos (AFDs).

## Estrutura do Projeto

```
lexer/
├── README.md                  # Este arquivo
├── lexer.py                   # Analisador léxico principal
├── test_string.py            # Arquivo de teste para strings
└── AFDS/                     # Diretório com os AFDs
    ├── afd_base.py           # Classe base para AFDs
    ├── afd_ident.py          # AFD para identificadores
    ├── afd_keyword.py        # AFD para palavras-chave
    ├── afd_number.py         # AFD para números
    ├── afd_operator.py       # AFD para operadores
    ├── afd_string.py         # AFD para strings
    ├── afd_char.py           # AFD para caracteres
    ├── afd_comment.py        # AFD para comentários
    ├── afd_delimiters.py     # AFD para delimitadores
    ├── afd_whitespace.py     # AFD para espaços em branco
    └── AFDs_teste.py         # Testes dos AFDs
```

## Como Executar

### Pré-requisitos
- Python 3.6 ou superior instalado
- Todos os arquivos AFD devem estar no diretório `AFDS/`

### Execução Principal

1. **Navegue até o diretório do lexer:**
   ```bash
   cd lexer
   ```

2. **Execute o analisador léxico:**
   ```bash
   python lexer.py
   ```

   O comando acima executará o lexer com o código de exemplo padrão:
   ```javascript
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
   ```

### Usando o Lexer Programaticamente

Você pode usar o lexer em seus próprios scripts Python:

```python
from lexer import Lexer

# Criar uma instância do lexer
lexer = Lexer()

# Seu código fonte
codigo = '''
    var x = 42;
    if (x > 0) {
        print("Positivo");
    }
'''

# Analisar o código
tokens, erros = lexer.analisar(codigo)

# Os tokens são uma lista de objetos Token
for token in tokens:
    print(f"{token.tipo}: {token.lexema}")

# Os erros são uma lista de objetos LexicalError
for erro in erros:
    print(erro)
```

### Modificando o Código de Teste

Para testar com seu próprio código, edite a variável `codigo_teste` na função `main()` do arquivo `lexer.py`:

```python
def main():
    # Substitua este código pelo seu código de teste
    codigo_teste = '''
        // Seu código aqui
        var nome = "João";
        print(nome);
    '''
    
    lexer = Lexer()
    tokens, erros = lexer.analisar(codigo_teste)
```

## Saída do Analisador

O analisador léxico produz duas saídas principais:

### 1. Tabela de Tokens
```
TOKENS RECONHECIDOS:
==================================================
TIPO            LEXEMA
--------------------------------------------------
KEYWORD         'float'
IDENT           'numero'
OPERATOR        '='
NUMBER          '10.0'
DELIMITERS      ';'
...
```

### 2. Erros Léxicos (se houver)
```
ERROS LÉXICOS ENCONTRADOS:
==================================================
Erro léxico na linha 11, coluna 8: Token não reconhecido '"É'
Erro léxico na linha 11, coluna 14: Token não reconhecido '";'
...
```

## Tipos de Tokens Reconhecidos

| Tipo        | Descrição                           | Exemplos                    |
|-------------|-------------------------------------|-----------------------------|
| `KEYWORD`   | Palavras reservadas da linguagem    | `float`, `function`, `if`   |
| `IDENT`     | Identificadores                     | `numero`, `parImpar`        |
| `NUMBER`    | Literais numéricos                  | `10.0`, `42`, `1.5e-10`     |
| `STRING`    | Literais de string                  | `"Hello"`, `'World'`        |
| `CHAR`      | Literais de caractere               | `'a'`, `'\n'`               |
| `OPERATOR`  | Operadores                          | `=`, `+`, `==`, `&&`        |
| `DELIMITERS`| Delimitadores                       | `(`, `)`, `{`, `}`, `;`     |
| `COMMENT`   | Comentários                         | `// linha`, `/* bloco */`   |

## Testando AFDs Individuais

Para testar um AFD específico:

```bash
cd AFDS
python AFDs_teste.py
```

## Tratamento de Erros

O lexer detecta e reporta os seguintes tipos de erros léxicos:

- **Caracteres não reconhecidos**: Caracteres que não fazem parte do alfabeto da linguagem
- **Tokens malformados**: Strings não fechadas, números inválidos, etc.
- **Posicionamento preciso**: Cada erro inclui linha e coluna exatas

## Funcionalidades

- ✅ **Reconhecimento de tokens** com base em AFDs
- ✅ **Princípio do maior match** (longest match)
- ✅ **Detecção de erros léxicos** com posição precisa
- ✅ **Suporte a múltiplos tipos de tokens**
- ✅ **Pulo automático de espaços em branco**
- ✅ **Tratamento de comentários**

## Palavras-Chave Suportadas

```
class, struct, interface, extends, implements, new, this, super, 
function, void, var, let, const, return, if, else, switch, case, 
default, break, continue, for, foreach, while, do, true, false, 
null, public, private, protected, static, int, float, string, 
bool, list, dict, print
```

## Limitações Conhecidas

- Caracteres Unicode especiais podem não ser reconhecidos corretamente em strings
- Comentários de bloco aninhados não são suportados
- Números em notação hexadecimal/octal não são suportados

## Solução de Problemas

### Erro: "Import could not be resolved"
Certifique-se de que todos os arquivos AFD estão no diretório `AFDS/` e que você está executando o lexer do diretório correto.

### Tokens não reconhecidos
Verifique se o caractere/token está definido em algum dos AFDs. Consulte a especificação da linguagem em `../Entregas 2,3,4/`.

### Erro de execução
Verifique se o Python 3.6+ está instalado e se todos os arquivos estão presentes.