# Analisador Léxico - Implementação com AFD

Esta pasta contém a implementação do **Analisador Léxico** baseado em **Autômatos Finitos Determinísticos (AFD)** para a linguagem proposta.

## 📁 Estrutura de Arquivos

```
src/lexer/
├── afn_to_afd.py      # Algoritmo de Construção de Subconjuntos (AFN→AFD)
├── lexer.py           # Analisador Léxico usando AFD
└── README.md          # Este arquivo
```

## 🎯 Componentes Principais

### 1. `afn_to_afd.py` - Construção de Subconjuntos

Implementa o **Algoritmo de Construção de Subconjuntos** para converter AFN em AFD.

**Principais funções:**
- `fechamento_epsilon()` - Calcula fechamento-ε de estados
- `mover()` - Calcula estados alcançáveis por um símbolo
- `construir_afd()` - **Função principal** que converte AFN em AFD
- `imprimir_afd()` - Visualização textual do AFD
- `afd_para_mermaid()` - Gera diagramas Mermaid

**Estruturas de dados:**
- `EstadoAFN` - Estado do autômato não-determinístico
- `AFN` - Autômato completo (estado inicial + final)
- `AFD` - Autômato determinístico (tabela de transições)

**Exemplo de uso:**
```python
from afn_to_afd import construir_afd, AFN, EstadoAFN

# Criar AFN (exemplo)
q0 = EstadoAFN(id=0)
q1 = EstadoAFN(id=1)
q0.transicoes[frozenset(['a'])] = {q1}

afn = AFN(estado_inicial=q0, estado_final=q1)

# Converter para AFD
alfabeto = ['a', 'b']
afd = construir_afd(afn, alfabeto)

# Testar
print(afd.aceita("a"))  # True
```

### 2. `lexer.py` - Analisador Léxico

Implementa o **Analisador Léxico** completo usando múltiplos AFDs.

**Principais classes:**
- `Token` - Representa um token (tipo, lexema, linha, coluna)
- `ErroLexico` - Representa erro encontrado
- `ResultadoAnalise` - Resultado completo (tokens + erros)
- `AnalisadorLexico` - **Classe principal** do analisador

**Tokens reconhecidos:**
- **Keywords**: `if`, `else`, `for`, `while`, `var`, `function`, `class`, etc.
- **Identificadores**: nomes de variáveis/funções
- **Literais**: inteiros, floats, strings, booleanos
- **Operadores**: aritméticos, relacionais, atribuição
- **Delimitadores**: parênteses, chaves, colchetes
- **Pontuação**: ponto-e-vírgula, vírgula, etc.

**Exemplo de uso:**
```python
from lexer import AnalisadorLexico

# Criar analisador
lexer = AnalisadorLexico()

# Analisar código
codigo = 'var int x as 10;'
resultado = lexer.analisar(codigo)

# Verificar resultado
if resultado.sucesso:
    for token in resultado.tokens:
        print(token)
else:
    for erro in resultado.erros:
        print(erro)
```

## 🚀 Como Executar

### Teste do Algoritmo de Construção de Subconjuntos

```bash
cd /workspaces/compiladores
python src/lexer/afn_to_afd.py
```

**Saída esperada:**
- Imprime AFD construído
- Mostra tabela de transições
- Testa palavras de exemplo
- Gera diagrama Mermaid

### Teste do Analisador Léxico

```bash
cd /workspaces/compiladores
python src/lexer/lexer.py
```

**Saída esperada:**
- Compila 22 tokens para AFDs
- Analisa código de exemplo
- Exibe tokens identificados
- Mostra erros (se houver)

### Analisar Arquivo de Código

```python
from lexer import AnalisadorLexico, imprimir_resultado

lexer = AnalisadorLexico()
resultado = lexer.analisar_arquivo('meu_codigo.txt')
imprimir_resultado(resultado)
```

## 📊 Algoritmo de Matching

O analisador usa a estratégia de **Maximal Munch** (match mais longo):

1. Para cada posição no código fonte
2. Tenta fazer match com **todos os AFDs** simultaneamente
3. Escolhe o **match mais longo** encontrado
4. Aplica **prioridade** (keywords > identificadores)
5. Emite o token correspondente
6. Avança para próxima posição

**Complexidade:** O(n × m) onde:
- n = tamanho do código fonte
- m = número de AFDs (constante)

**Na prática:** O(n) - linear no tamanho do código

## 🎯 Priorização de Tokens

A ordem de matching é crucial para evitar ambiguidades:

```python
ORDEM_TOKENS = [
    "COMMENT",          # Prioridade 1: comentários
    "STRING_LITERAL",   # Prioridade 2: strings
    "FLOAT_LITERAL",    # Prioridade 3: floats
    "INT_LITERAL",      # Prioridade 4: inteiros
    "KEYWORD",          # Prioridade 5: palavras-chave
    "IDENTIFIER",       # Prioridade 6: identificadores
    # ... outros tokens
]
```

**Exemplo:**
- Input: `var`
- Keywords reconhece `var` (3 chars)
- Identifier reconhece `var` (3 chars)
- **Resultado:** KEYWORD (tem prioridade)

## 🔍 Tratamento de Erros

Quando nenhum AFD consegue fazer match:

```python
char = codigo[posicao]
erro = ErroLexico(
    mensagem="Caractere inválido",
    linha=linha_atual,
    coluna=coluna_atual,
    caractere=char
)
```

**Estratégia:** Reporta erro e continua análise (modo de recuperação).

## 🧪 Exemplos de Teste

### Código Válido

```python
var int x as 10;
var string nome as "João";
if (x > 5) {
    x = x + 1;
}
```

**Tokens gerados:**
```
KEYWORD       "var"
KEYWORD       "int"
IDENTIFIER    "x"
KEYWORD       "as"
INT_LITERAL   "10"
SEMICOLON     ";"
...
```

### Código com Erro

```python
var int x as 10; @ # $
```

**Erros reportados:**
```
Erro léxico [1:18]: Caractere inválido ('@')
Erro léxico [1:20]: Caractere inválido ('#')
Erro léxico [1:22]: Caractere inválido ('$')
```

## 📈 Estatísticas dos AFDs

| Token | Estados AFD | Complexidade |
|-------|-------------|--------------|
| KEYWORD | 100 | Alta (união de muitas palavras) |
| IDENTIFIER | 3 | Baixa |
| INT_LITERAL | 2 | Baixa |
| FLOAT_LITERAL | 7 | Média |
| STRING_LITERAL | 4 | Baixa |
| RELOP | 9 | Média |
| COMMENT | 4 | Baixa |

**Total:** 22 AFDs compilados

## 🔗 Integração com Sistema Existente

Este analisador é **compatível** com o sistema existente em `Compiladores/`:

```python
# Usa os autômatos já implementados
from modulos_lexicos import compile_regex_to_dfa
from modulos_lexicos.estruturas import DFA

# Compila regex para AFD
afd = compile_regex_to_dfa(r'\d+')
```

## 📚 Referências Teóricas

1. **Construção de Subconjuntos:**
   - Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"
   - Capítulo 3: Análise Léxica

2. **Maximal Munch:**
   - Estratégia padrão em analisadores léxicos
   - Garante reconhecimento do token mais longo

3. **Fechamento-Epsilon:**
   - Calcula estados alcançáveis sem consumir entrada
   - Fundamental para conversão AFN→AFD

## 🎓 Conceitos Implementados

- ✅ **Algoritmo de Construção de Subconjuntos**
- ✅ **Fechamento-Epsilon**
- ✅ **Função Move**
- ✅ **Tabela de Transições Determinística**
- ✅ **Maximal Munch (Longest Match)**
- ✅ **Priorização de Tokens**
- ✅ **Tratamento de Erros Léxicos**
- ✅ **Rastreamento de Posição (linha/coluna)**

## 🛠️ Possíveis Extensões

1. **Otimização do AFD:**
   - Minimização de estados
   - Algoritmo de Hopcroft

2. **Suporte a mais escapes:**
   - `\uXXXX` (Unicode)
   - `\xHH` (hexadecimal)

3. **Comentários de bloco:**
   - `/* ... */`

4. **Strings multi-linha:**
   - `"""..."""`

5. **Cache de AFDs:**
   - Salvar AFDs compilados em arquivo
   - Acelerar inicialização

## ✨ Destaques da Implementação

- 🎯 **100% baseado em teoria de autômatos**
- ⚡ **Eficiente:** Análise em tempo linear
- 🔍 **Preciso:** Reporta linha e coluna dos erros
- 📊 **Completo:** 22 categorias de tokens
- 🧪 **Testado:** Exemplos incluídos
- 📚 **Documentado:** Código bem comentado

---

**Desenvolvido como parte do projeto de Compiladores - 2025**
