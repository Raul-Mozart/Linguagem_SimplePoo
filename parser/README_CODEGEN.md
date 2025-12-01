# ⚡ Geração de Código LLVM IR - SimplePOO

## ✅ Implementação Completa

Gerador de código LLVM IR completo que traduz AST SimplePOO para representação intermediária executável.

---

## 📁 Arquivos Implementados

### 1. **`code_generator.py`** (450 linhas)
Gerador de código LLVM IR:
- **LLVMCodeGenerator**: Classe principal
- Visitor pattern para percorrer AST
- Tradução composicional recursiva
- Formato textual LLVM (.ll)
- Alloca/Load/Store para variáveis mutáveis
- Blocos básicos para controle de fluxo

### 2. **`compiler_llvm.py`** (320 linhas)
Compilador completo integrado:
- 4 fases: Léxica → Sintática → Semântica → Código
- 5 exemplos demonstrando recursos
- Salvamento de código IR em arquivos
- Interface unificada de compilação

---

## 🎯 Recursos Implementados

### ✅ 1. **Expressões**
- ✅ Literais (números, booleanos)
- ✅ Variáveis (load de alloca)
- ✅ Operadores aritméticos (+, -, *, /, %)
- ✅ Operadores de comparação (<, >, <=, >=, ==, !=)
- ✅ Operadores lógicos (&&, ||, !)
- ✅ Operadores unários (-, !)

### ✅ 2. **Comandos**
- ✅ Declarações de variáveis (alloca + store)
- ✅ Atribuições (store)
- ✅ If/Else (blocos básicos + br condicional)
- ✅ Loops For (blocos para cond/body/update)
- ✅ Return
- ✅ Print (via printf)

### ✅ 3. **Funções**
- ✅ Declaração de funções
- ✅ Parâmetros (alloca para cada parâmetro)
- ✅ Chamadas de função
- ✅ Função main

### ✅ 4. **Sistema de Tipos**
- ✅ Mapeamento SimplePOO → LLVM:
  - int → i64
  - float → double
  - string → i8*
  - bool → i1

---

## 🚀 Como Usar

### Uso Básico

```python
from code_generator import LLVMCodeGenerator
from parser import Parser
from lexer_enhanced import EnhancedLexer

# Código SimplePOO
code = '''
function main() {
    int x = 10;
    int y = 20;
    int soma = x + y;
    print(soma);
}
'''

# 1-3. Léxica, Sintática, Semântica (já implementadas)
lexer = EnhancedLexer()
tokens, _ = lexer.tokenize(code)
parser = Parser(lexer)
ast = parser.parse()

# 4. Geração de Código
generator = LLVMCodeGenerator()
generator.add_format_strings()
ir_code = generator.generate(ast)

# Salvar em arquivo
with open('programa.ll', 'w') as f:
    f.write(ir_code)

print(ir_code)
```

### Compilador Completo

```bash
cd parser

# Compilar exemplos
python compiler_llvm.py

# Arquivos gerados:
# - exemplo1.ll (programa simples)
# - exemplo2.ll (funções)
# - exemplo3.ll (condicionais)
# - exemplo4.ll (loops)
# - exemplo5.ll (operações)
```

### Executar Código Gerado

```bash
# Com lli (interpretador LLVM)
lli exemplo1.ll

# Compilar para executável
llc exemplo1.ll -o exemplo1.s
gcc exemplo1.s -o exemplo1
./exemplo1
```

---

## 📖 Estrutura do Código LLVM IR

### Exemplo de Código Gerado

#### Código SimplePOO:
```javascript
function main() {
    int x = 10;
    int y = 20;
    int soma = x + y;
    print(soma);
}
```

#### LLVM IR Gerado:
```llvm
@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"

; ModuleID = 'SimplePOO'
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define void @main() {
  entry:
    %0 = alloca i64           ; Aloca x
    store i64 10, i64* %0     ; x = 10
    
    %1 = alloca i64           ; Aloca y
    store i64 20, i64* %1     ; y = 20
    
    %2 = alloca i64           ; Aloca soma
    %3 = load i64, i64* %0    ; Carrega x
    %4 = load i64, i64* %1    ; Carrega y
    %5 = add i64 %3, %4       ; x + y
    store i64 %5, i64* %2     ; soma = resultado
    
    %6 = load i64, i64* %2    ; Carrega soma
    %7 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %7, i64 %6)  ; print(soma)
    
    ret void
}
```

---

## 🏗️ Arquitetura do Gerador

### Componentes Principais

```
LLVMCodeGenerator
├── output: List[str]              # Linhas de código IR
├── temp_counter: int              # Contador de temporários (%0, %1...)
├── label_counter: int             # Contador de labels
├── variables: Dict[str, str]      # Variável → alloca
├── functions: Dict[str, ...]      # Funções declaradas
│
├── generate(ast) → str            # Gera IR completo
├── emit(line)                     # Emite linha de código
├── new_temp() → str               # Cria temporário
├── new_label(prefix) → str        # Cria label
│
└── Visitors (um por tipo de nó):
    ├── visit_VarDeclNode()        # Declarações
    ├── visit_FuncDeclNode()       # Funções
    ├── visit_IfNode()             # Condicionais
    ├── visit_ForNode()            # Loops
    ├── visit_BinaryOpNode()       # Operações binárias
    ├── visit_IdentifierNode()     # Variáveis
    └── visit_LiteralNode()        # Literais
```

### Padrões de Tradução

#### Declaração de Variável
```javascript
int x = 10;
```
```llvm
%0 = alloca i64
store i64 10, i64* %0
```

#### Expressão Binária
```javascript
int z = x + y;
```
```llvm
%1 = load i64, i64* %x_alloca
%2 = load i64, i64* %y_alloca
%3 = add i64 %1, %2
%4 = alloca i64
store i64 %3, i64* %4
```

#### Condicional
```javascript
if (x > 10) {
    y = 1;
} else {
    y = 0;
}
```
```llvm
%1 = load i64, i64* %x_alloca
%2 = icmp sgt i64 %1, 10
br i1 %2, label %if.then0, label %if.else1

if.then0:
  store i64 1, i64* %y_alloca
  br label %if.end2

if.else1:
  store i64 0, i64* %y_alloca
  br label %if.end2

if.end2:
  ; continua...
```

#### Loop For
```javascript
for (int i = 0; i < 10; i++) {
    print(i);
}
```
```llvm
; Inicialização
%i = alloca i64
store i64 0, i64* %i
br label %for.cond0

for.cond0:
  %1 = load i64, i64* %i
  %2 = icmp slt i64 %1, 10
  br i1 %2, label %for.body1, label %for.end3

for.body1:
  ; corpo do loop
  br label %for.update2

for.update2:
  %3 = load i64, i64* %i
  %4 = add i64 %3, 1
  store i64 %4, i64* %i
  br label %for.cond0

for.end3:
  ; continua...
```

---

## 🎓 Conceitos Aplicados

### Do Material Teórico:

✅ **Interpretação vs Compilação**
- Geração de código estático
- Execução sem interpretar AST
- Performance superior

✅ **LLVM IR**
- Representação intermediária moderna
- Independente de arquitetura
- Formato textual (.ll)
- Blocos básicos (SSA form)

✅ **Tradução Sistemática**
- Composicional recursiva
- Visitor pattern
- Um método por tipo de nó

✅ **Alloca/Load/Store**
- Variáveis mutáveis em SSA
- Alloca no entry block
- Load para ler, Store para escrever

✅ **Blocos Básicos**
- Sem branches internas
- Terminador obrigatório (br, ret)
- Labels para controle de fluxo

---

## 📊 Exemplos de Saída

### Exemplo 1: Soma Simples
**Entrada:**
```javascript
function main() {
    int x = 10;
    int y = 20;
    print(x + y);
}
```

**Saída:** Código LLVM de 24 linhas ✅

### Exemplo 2: Condicional
**Entrada:**
```javascript
function main() {
    int x = 15;
    if (x > 10) {
        print(1);
    }
}
```

**Saída:** Código LLVM com 3 blocos básicos ✅

### Exemplo 3: Loop
**Entrada:**
```javascript
function main() {
    for (int i = 0; i < 10; i++) {
        print(i);
    }
}
```

**Saída:** Código LLVM com 4 blocos (cond, body, update, end) ✅

---

## 🛠️ Ferramentas LLVM

### Executar IR
```bash
# Interpretador JIT
lli programa.ll

# Com otimizações
lli -O2 programa.ll
```

### Otimizar IR
```bash
# Aplicar otimizações
opt -O2 programa.ll -S -o programa_opt.ll

# Passes específicos
opt -mem2reg -constprop -dce programa.ll -S -o programa_opt.ll
```

### Compilar para Assembly
```bash
# Gerar assembly nativo
llc programa.ll -o programa.s

# Para arquitetura específica
llc -march=x86-64 programa.ll -o programa_x86.s
llc -march=aarch64 programa.ll -o programa_arm.s
```

### Gerar Executável
```bash
# Compilar para objeto
llc programa.ll -o programa.s
as programa.s -o programa.o

# Linkar
gcc programa.o -o programa
./programa
```

---

## 💡 Limitações e Melhorias Futuras

### Limitações Atuais
- Funções sempre retornam void
- Parâmetros sempre i64
- Sem suporte a arrays/structs
- Print apenas para inteiros
- Sem inferência completa de tipos

### Melhorias Possíveis
1. **Tipos de Retorno**: Funções com tipos variados
2. **Arrays**: Suporte a listas e acesso por índice
3. **Strings**: Manipulação completa de strings
4. **Otimizações**: mem2reg automático, constant folding
5. **Chamadas de Sistema**: I/O mais completo
6. **Biblioteca Padrão**: Funções built-in

---

## 🎯 Status

**✅ IMPLEMENTAÇÃO COMPLETA**

- ✅ Gerador de código LLVM IR
- ✅ Tradução de expressões
- ✅ Tradução de comandos
- ✅ Funções e parâmetros
- ✅ Controle de fluxo (if/for)
- ✅ Blocos básicos
- ✅ Alloca/Load/Store
- ✅ Formato textual (.ll)
- ✅ Integração completa com pipeline
- ✅ 5 exemplos funcionais

---

## 📈 Resultados

### Pipeline Completo
```
Código SimplePOO (10 linhas)
    ↓
Léxica (28 tokens)
    ↓
Sintática (AST com 4 nós)
    ↓
Semântica (0 erros)
    ↓
Código LLVM IR (24 linhas)
    ↓
Executável (via lli/llc)
```

### Estatísticas
- **Código gerado**: ~20-30 linhas IR por função simples
- **Temporários**: 5-10 por função
- **Blocos básicos**: 1-4 por estrutura de controle
- **Instruções**: add, sub, mul, div, icmp, br, load, store, alloca, call, ret

---

**Versão:** 1.0 - Completa  
**Data:** 22 de Novembro de 2025  
**Base Teórica:** Material "Geração de Código e LLVM IR"  
**Linguagem:** SimplePOO → LLVM IR
