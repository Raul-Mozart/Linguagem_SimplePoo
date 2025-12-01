# 🚀 Compilador SimplePOO

> Compilador completo da linguagem SimplePOO para LLVM IR

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![LLVM](https://img.shields.io/badge/LLVM-10.0%2B-orange.svg)](https://llvm.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Sobre o Projeto

O **Compilador SimplePOO** é um compilador completo que transforma código na linguagem SimplePOO em código LLVM IR executável. Implementado em Python, o compilador passa por todas as 4 fases clássicas de compilação:

1. **Análise Léxica** - Tokenização do código fonte
2. **Análise Sintática** - Construção da AST (Árvore Sintática Abstrata)
3. **Análise Semântica** - Verificação de tipos, escopos e símbolos
4. **Geração de Código** - Tradução para LLVM IR

---

## ✨ Características

- ✅ **4 Fases Completas**: Léxica → Sintática → Semântica → Geração de Código
- ✅ **LLVM IR**: Gera código intermediário executável
- ✅ **Análise de Erros**: Mensagens detalhadas em todas as fases
- ✅ **Otimizável**: Código gerado pode ser otimizado com LLVM
- ✅ **Executável**: Compila para binário nativo via LLVM
- ✅ **Bem Documentado**: Manuais completos de instalação e uso

---

## 🚀 Início Rápido

### Instalação

```bash
# 1. Clonar repositório
git clone https://github.com/Raul-Mozart/Linguagem_SimplePoo/tree/Automatos_raul
cd Linguagem_SimplePoo

# 2. Verificar Python
python --version  # Necessário 3.8+

# 3. (Opcional) Instalar LLVM para executar código
# Veja INSTALL.md para instruções detalhadas
```

### Primeiro Programa

Crie um arquivo `hello.txt`:
```javascript
function main() {
    int x = 10;
    int y = 20;
    print(x + y);
}
```

Compile:
```bash
python compile.py hello.txt
```

Resultado:
```
✓ Compilação concluída com sucesso!
  Arquivo gerado: hello.ll
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| **[INSTALL.md](INSTALL.md)** | 📦 Manual de instalação completo (Windows/Linux/macOS) |
| **[MANUAL_USO.md](MANUAL_USO.md)** | 📖 Manual de uso com exemplos práticos |
| **[lexer/README.md](lexer/README.md)** | 🔤 Documentação do analisador léxico |
| **[parser/README_PARSER.md](parser/README_PARSER.md)** | 🌳 Documentação do analisador sintático |
| **[parser/README_SEMANTIC.md](parser/README_SEMANTIC.md)** | ✔️ Documentação do analisador semântico |
| **[parser/README_CODEGEN.md](parser/README_CODEGEN.md)** | ⚡ Documentação da geração de código |

---

## 🎯 Estrutura do Projeto

```
Linguagem_SimplePoo/
├── compile.py                      # 🚀 Compilador principal (USE ESTE!)
├── INSTALL.md                      # 📦 Manual de instalação
├── MANUAL_USO.md                   # 📖 Manual de uso
├── README.md                       # 📄 Este arquivo
│
├── exemplos/                       # 💡 Programas de exemplo
│   ├── 01_hello.txt               # Hello World
│   ├── 02_soma.txt                # Operações aritméticas
│   ├── 03_condicional.txt         # If/Else
│   ├── 04_loop.txt                # Loop For
│   └── 05_operacoes.txt           # Operações completas
│
├── lexer/                          # 🔤 FASE 1: Análise Léxica
│   ├── lexer_enhanced.py          # Lexer principal
│   ├── README.md                  # Documentação
│   └── AFDS/                      # Autômatos finitos
│       ├── afd_ident.py           # Identificadores
│       ├── afd_keyword.py         # Palavras-chave
│       ├── afd_number.py          # Números
│       ├── afd_operator.py        # Operadores
│       └── ...                    # Outros AFDs
│
└── parser/                         # 🌳 FASES 2-4
    ├── parser.py                  # FASE 2: Análise Sintática
    ├── ast_nodes.py               # Nós da AST
    ├── semantic_analyzer.py       # FASE 3: Análise Semântica
    ├── symbol_table.py            # Tabela de símbolos
    ├── code_generator.py          # FASE 4: Geração de Código
    ├── README_PARSER.md           # Documentação Parser
    ├── README_SEMANTIC.md         # Documentação Semântica
    └── README_CODEGEN.md          # Documentação Geração de Código
```

---

## 💻 Uso do Compilador

### Comandos Básicos

```bash
# Compilar programa
python compile.py programa.txt

# Compilar e executar (requer LLVM)
python compile.py programa.txt --run

# Modo detalhado (mostra todas as fases)
python compile.py programa.txt -v

# Ver código LLVM IR gerado
python compile.py programa.txt --show-ir

# Especificar arquivo de saída
python compile.py programa.txt -o saida.ll

# Ajuda completa
python compile.py --help
```

### Exemplo de Saída

```
============================================================
FASE 1: ANÁLISE LÉXICA
============================================================
✓ 28 tokens reconhecidos

============================================================
FASE 2: ANÁLISE SINTÁTICA
============================================================
✓ AST construída com sucesso (15 nós)

============================================================
FASE 3: ANÁLISE SEMÂNTICA
============================================================
✓ Verificação semântica concluída

============================================================
FASE 4: GERAÇÃO DE CÓDIGO LLVM IR
============================================================
✓ Código LLVM IR gerado (24 linhas)
✓ Código salvo em: programa.ll

📊 Estatísticas:
  • Tokens reconhecidos: 28
  • Nós da AST: 15
  • Erros semânticos: 0
  • Linhas de IR: 24

✓ Compilação concluída com sucesso!
```

---

## 🔤 Linguagem SimplePOO

### Sintaxe Básica

```javascript
// Declaração de variáveis
int x = 10;
float pi = 3.14;
bool ativo = true;

// Operações aritméticas
int soma = x + y;
int sub = x - y;
int mult = x * y;
int div = x / y;
int mod = x % y;

// Condicionais
if (x > 10) {
    print(1);
} else {
    print(0);
}

// Loops
for (int i = 0; i < 10; i++) {
    print(i);
}

// Funções
function main() {
    // Código aqui
}
```

### Exemplos Prontos

Explore a pasta `exemplos/` para ver programas funcionais:

```bash
# Hello World
python compile.py exemplos/01_hello.txt --run

# Soma de números
python compile.py exemplos/02_soma.txt --run

# Condicional
python compile.py exemplos/03_condicional.txt --run

# Loop
python compile.py exemplos/04_loop.txt --run

# Operações matemáticas
python compile.py exemplos/05_operacoes.txt --run
```

---

## 🏗️ Arquitetura do Compilador

### Pipeline de Compilação

```
Código SimplePOO (.txt)
        ↓
┌───────────────────────────────────────┐
│  FASE 1: ANÁLISE LÉXICA              │
│  • Tokenização                        │
│  • Match mais longo                   │
│  • Bufferização                       │
└───────────────────────────────────────┘
        ↓ [Tokens]
┌───────────────────────────────────────┐
│  FASE 2: ANÁLISE SINTÁTICA           │
│  • Parser recursivo descendente       │
│  • Construção da AST                  │
│  • Verificação gramatical             │
└───────────────────────────────────────┘
        ↓ [AST]
┌───────────────────────────────────────┐
│  FASE 3: ANÁLISE SEMÂNTICA           │
│  • Tabela de símbolos                 │
│  • Verificação de tipos               │
│  • Verificação de escopos             │
└───────────────────────────────────────┘
        ↓ [AST Validada]
┌───────────────────────────────────────┐
│  FASE 4: GERAÇÃO DE CÓDIGO           │
│  • Tradução para LLVM IR              │
│  • Alloca/Load/Store                  │
│  • Blocos básicos (SSA)               │
└───────────────────────────────────────┘
        ↓
Código LLVM IR (.ll)
        ↓
[lli] Executar diretamente
[llc] Compilar para Assembly
[gcc] Gerar executável nativo
```

### Componentes Principais

#### 1. Analisador Léxico (Lexer)
- **Arquivo:** `lexer/lexer_enhanced.py`
- **Função:** Transforma texto em tokens
- **Técnicas:** AFDs, match mais longo, bufferização
- **Saída:** Lista de tokens com posição

#### 2. Analisador Sintático (Parser)
- **Arquivo:** `parser/parser.py`
- **Função:** Constrói árvore sintática (AST)
- **Técnica:** Recursivo descendente preditivo
- **Saída:** AST com nós tipados

#### 3. Analisador Semântico
- **Arquivo:** `parser/semantic_analyzer.py`
- **Função:** Valida significado do código
- **Verifica:** Tipos, escopos, declarações
- **Saída:** AST validada + erros semânticos

#### 4. Gerador de Código
- **Arquivo:** `parser/code_generator.py`
- **Função:** Traduz AST para LLVM IR
- **Técnica:** Visitor pattern, SSA form
- **Saída:** Código LLVM IR executável

---

## 🛠️ Executando Código Compilado

### Método 1: Interpretador LLVM (lli)

```bash
# Compilar
python compile.py programa.txt

# Executar
lli programa.ll
```

### Método 2: Compilar para Executável Nativo

```bash
# SimplePOO → LLVM IR
python compile.py programa.txt

# LLVM IR → Assembly
llc programa.ll -o programa.s

# Assembly → Executável
gcc programa.s -o programa.exe

# Executar
./programa.exe
```

### Método 3: Com Otimizações LLVM

```bash
# Compilar
python compile.py programa.txt

# Otimizar IR
opt -O2 programa.ll -S -o programa_opt.ll

# Executar otimizado
lli programa_opt.ll
```

---

## 📊 Estatísticas do Projeto

- **Linhas de Código:** ~3000+ linhas Python
- **Módulos:** 15+ arquivos principais
- **Fases:** 4 completas
- **AFDs:** 11 autômatos finitos
- **Nós AST:** 15+ tipos diferentes
- **Testes:** 5+ exemplos funcionais

---

## 🎓 Conceitos Implementados

### Teoria de Compiladores
- ✅ Análise léxica com AFDs
- ✅ Parsing recursivo descendente
- ✅ Construção de AST
- ✅ Tabelas de símbolos com escopos
- ✅ Verificação de tipos
- ✅ Geração de código intermediário

### LLVM
- ✅ Formato IR textual (.ll)
- ✅ SSA form (Static Single Assignment)
- ✅ Alloca/Load/Store para variáveis
- ✅ Blocos básicos
- ✅ Instruções aritméticas e lógicas
- ✅ Controle de fluxo (br, ret)
- ✅ Chamadas de função (printf)

### Padrões de Projeto
- ✅ Visitor pattern (AST traversal)
- ✅ Strategy pattern (AFDs)
- ✅ Composição (nós da AST)

---

## 🐛 Tratamento de Erros

O compilador detecta e reporta erros em todas as fases:

### Erros Léxicos
```
Erro léxico na linha 3, coluna 10: Token não reconhecido '@'
```

### Erros Sintáticos
```
Erro sintático na linha 5: Esperado ';' após declaração
```

### Erros Semânticos
```
Erro linha 7: Variável 'x' não declarada
Erro linha 10: Tipos incompatíveis: int + string
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin feature/nova-feature`
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja arquivo LICENSE para mais detalhes.

---

## 👥 Autores

Desenvolvido como projeto acadêmico de Compiladores.

---

## 📚 Referências

- **LLVM Documentation:** https://llvm.org/docs/
- **Compilers: Principles, Techniques, and Tools** (Dragon Book)
- **Modern Compiler Implementation in ML** (Tiger Book)

---

## 💬 Suporte

Problemas ou dúvidas?

1. Consulte a [Documentação](#-documentação)
2. Veja os [Exemplos](exemplos/)
3. Leia o [Manual de Uso](MANUAL_USO.md)
4. Verifique o [Manual de Instalação](INSTALL.md)

---

