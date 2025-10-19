# AFN (Autômato Finito Não-determinístico) e AFD Combinado

Este projeto implementa a criação de um **AFN** (Autômato Finito Não-determinístico) a partir dos AFDs existentes no projeto e sua posterior conversão para um **AFD** (Autômato Finito Determinístico) combinado.

## Arquivos Criados

### 1. `afn.py` - Implementação Principal
Arquivo principal que contém:
- **`combine_afds_to_nfa()`**: Função que combina múltiplos AFDs em um único AFN
- **`nfa_to_dfa()`**: Função que converte o AFN em AFD usando o algoritmo de construção de subconjuntos
- **Funções auxiliares**: `epsilon_closure()` e `move()` para operações do AFN

### 2. `test_afn_afd.py` - Testes do AFD Combinado
Arquivo de testes que valida o funcionamento do AFD combinado com diversos casos de teste:
- Identificadores (variavel, _temp, valor123)
- Palavras-chave (class, if, function, return)
- Números (123, 45.67, 1.23e-4, 2E10)
- Strings ("Hello World", 'teste', "")
- Operadores (++, ==, <=, ->, +)
- Delimitadores ((, ), {, ;)
- Comentários (// linha, /* bloco */)
- Whitespace (espaços, tabs, quebras de linha)

### 3. `lexer_integrado.py` - Lexer Completo
Implementação de um lexer completo que utiliza o AFD combinado para análise lexical, incluindo:
- Análise de texto com maior correspondência (longest match)
- Tratamento de prioridades de tokens
- Rastreamento de linha e coluna
- Tratamento de erros lexicais

## Como Funciona

### Criação do AFN
1. **Combinação de AFDs**: Cada AFD individual é renomeado com um prefixo único
2. **Estado inicial único**: Um novo estado inicial se conecta via transições epsilon aos estados iniciais de cada AFD
3. **Mapeamento de tokens**: Estados finais são mapeados para seus respectivos tipos de token

### Conversão AFN → AFD
1. **Algoritmo de construção de subconjuntos**: Converte o AFN em AFD
2. **Epsilon-fecho**: Calcula estados alcançáveis via transições epsilon
3. **Prioridade de tokens**: Quando múltiplos tokens são possíveis, usa prioridade definida

### Estrutura dos AFDs Utilizados
- **AFDComment**: Reconhece comentários de linha (//) e bloco (/* */)
- **AFDString**: Reconhece strings com aspas simples ou duplas
- **AFDNumber**: Reconhece números inteiros, decimais e notação científica
- **AFDKeyword**: Reconhece palavras-chave da linguagem
- **AFDIdent**: Reconhece identificadores
- **AFDOperator**: Reconhece operadores simples e compostos
- **AFDDelimiters**: Reconhece delimitadores ((, ), {, }, [, ], ;, ,, .)
- **AFDWhitespace**: Reconhece espaços em branco

## Prioridades de Tokens
```
1. COMMENT (maior prioridade)
2. STRING
3. KEYWORD
4. NUMBER
5. IDENTIFIER
6. OPERATOR
7. DELIMITER
8. WHITESPACE (menor prioridade)
```

## Resultados
- **AFN criado**: 231 estados
- **AFD final**: 222 estados com 210 estados finais
- **Alfabeto**: 214 símbolos
- **Taxa de sucesso nos testes**: 100% (28/28 casos de teste)

## Como Executar

### Teste básico do AFN/AFD:
```bash
python afn.py
```

### Testes unitários:
```bash
python test_afn_afd.py
```

### Lexer integrado com exemplos:
```bash
python lexer_integrado.py
```

## Exemplo de Uso

```python
from afn import combine_afds_to_nfa, nfa_to_dfa
from afd_ident import AFDIdent
from afd_number import AFDNumber
# ... outros imports

# Criar AFDs
afds = [AFDIdent(), AFDNumber(), ...]
token_types = ["IDENTIFIER", "NUMBER", ...]
token_priority = {"IDENTIFIER": 5, "NUMBER": 4, ...}

# Criar AFN e converter para AFD
nfa = combine_afds_to_nfa(afds, token_types)
afd, afd_rev = nfa_to_dfa(nfa, token_priority)

# Usar o AFD
resultado = afd.accepts("variavel123")  # True
```

## Benefícios da Implementação

1. **Eficiência**: AFD único elimina necessidade de testar múltiplos AFDs
2. **Precisão**: Sistema de prioridades resolve conflitos entre tokens
3. **Completude**: Reconhece todos os tipos de token da linguagem
4. **Manutenibilidade**: Estrutura modular permite fácil adição de novos tipos de token
5. **Conformidade**: Baseado no exemplo de referência fornecido