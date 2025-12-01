# 📖 Manual de Uso - Compilador SimplePOO

> Guia completo para compilar programas na linguagem SimplePOO

---

## 🚀 Início Rápido

### Compilar um programa

```bash
# Compilar arquivo
python compile.py programa.txt

# Resultado: programa.ll (código LLVM IR)
```

### Executar programa compilado

```bash
# Executar com interpretador LLVM
lli programa.ll
```

---

## 📝 Sintaxe da Linguagem SimplePOO

### Estrutura Básica

```javascript
function main() {
    // Seu código aqui
}
```

### Tipos de Dados

```javascript
int x = 10;          // Inteiro
float pi = 3.14;     // Ponto flutuante
string nome = "João"; // String
bool ativo = true;   // Booleano
```

### Operadores

#### Aritméticos
```javascript
int a = 10 + 5;   // Adição
int b = 10 - 5;   // Subtração
int c = 10 * 5;   // Multiplicação
int d = 10 / 5;   // Divisão
int e = 10 % 3;   // Módulo (resto)
```

#### Comparação
```javascript
bool maior = x > 5;      // Maior que
bool menor = x < 5;      // Menor que
bool maiorIgual = x >= 5; // Maior ou igual
bool menorIgual = x <= 5; // Menor ou igual
bool igual = x == 5;     // Igual a
bool diferente = x != 5; // Diferente de
```

#### Lógicos
```javascript
bool e = true && false;  // E lógico
bool ou = true || false; // OU lógico
bool nao = !true;        // NÃO lógico
```

### Estruturas de Controle

#### If / Else
```javascript
if (x > 10) {
    print(1);
} else {
    print(0);
}
```

#### Loop For
```javascript
for (int i = 0; i < 10; i++) {
    print(i);
}
```

### Funções

```javascript
function soma(int a, int b) {
    return a + b;
}

function main() {
    int resultado = soma(5, 3);
    print(resultado);
}
```

### Saída (Print)

```javascript
print(42);           // Imprime número
print(x + y);        // Imprime expressão
```

---

## 🛠️ Usando o Compilador

### Opções de Linha de Comando

```bash
python compile.py [arquivo] [opções]
```

#### Opções Disponíveis:

| Opção | Descrição |
|-------|-----------|
| `-o, --output` | Especifica arquivo de saída |
| `-v, --verbose` | Modo detalhado (mostra todas as fases) |
| `-r, --run` | Executa código após compilar |
| `--show-ir` | Mostra código LLVM IR gerado |
| `--help` | Mostra ajuda |

### Exemplos de Uso

#### 1. Compilação Básica

```bash
python compile.py programa.txt
```

**Saída:**
- Arquivo `programa.ll` com código LLVM IR

#### 2. Compilar e Executar

```bash
python compile.py programa.txt --run
```

**O que faz:**
1. Compila `programa.txt`
2. Gera `programa.ll`
3. Executa com `lli programa.ll`
4. Mostra resultado

#### 3. Modo Verbose (Detalhado)

```bash
python compile.py programa.txt -v
```

**Mostra:**
- Tokens reconhecidos
- Estrutura da AST
- Tabela de símbolos
- Estatísticas detalhadas

#### 4. Especificar Arquivo de Saída

```bash
python compile.py programa.txt -o meu_codigo.ll
```

#### 5. Ver Código LLVM IR

```bash
python compile.py programa.txt --show-ir
```

#### 6. Compilar, Ver IR e Executar

```bash
python compile.py programa.txt -v --show-ir --run
```

---

## 📚 Exemplos Práticos

### Exemplo 1: Hello World Numérico

**Arquivo:** `hello.txt`
```javascript
function main() {
    print(42);
}
```

**Compilar:**
```bash
python compile.py hello.txt --run
```

**Saída:**
```
42
```

---

### Exemplo 2: Soma de Números

**Arquivo:** `soma.txt`
```javascript
function main() {
    int x = 10;
    int y = 20;
    int soma = x + y;
    print(soma);
}
```

**Compilar:**
```bash
python compile.py soma.txt --run
```

**Saída:**
```
30
```

---

### Exemplo 3: Condicional

**Arquivo:** `condicional.txt`
```javascript
function main() {
    int idade = 18;
    
    if (idade >= 18) {
        print(1);  // Maior de idade
    } else {
        print(0);  // Menor de idade
    }
}
```

**Compilar:**
```bash
python compile.py condicional.txt --run
```

**Saída:**
```
1
```

---

### Exemplo 4: Loop

**Arquivo:** `loop.txt`
```javascript
function main() {
    for (int i = 0; i < 5; i++) {
        print(i);
    }
}
```

**Compilar:**
```bash
python compile.py loop.txt --run
```

**Saída:**
```
0
1
2
3
4
```

---

### Exemplo 5: Operações Matemáticas

**Arquivo:** `matematica.txt`
```javascript
function main() {
    int a = 10;
    int b = 3;
    
    int soma = a + b;
    int sub = a - b;
    int mult = a * b;
    int div = a / b;
    int mod = a % b;
    
    print(soma);   // 13
    print(sub);    // 7
    print(mult);   // 30
    print(div);    // 3
    print(mod);    // 1
}
```

---

### Exemplo 6: Variáveis e Expressões

**Arquivo:** `expressoes.txt`
```javascript
function main() {
    int x = 5;
    int y = 10;
    int z = (x + y) * 2;
    
    print(z);  // 30
}
```

---

### Exemplo 7: Comparações

**Arquivo:** `comparacoes.txt`
```javascript
function main() {
    int x = 15;
    
    if (x > 10) {
        print(1);
    }
    
    if (x < 20) {
        print(2);
    }
    
    if (x == 15) {
        print(3);
    }
}
```

**Saída:**
```
1
2
3
```

---

## 🔍 Entendendo a Compilação

### Fases do Compilador

#### 1️⃣ Análise Léxica (Lexer)
- **O que faz:** Transforma código em tokens
- **Entrada:** Texto do programa
- **Saída:** Lista de tokens (palavras-chave, identificadores, números, operadores)

**Exemplo:**
```
Código: int x = 10;
Tokens: [INT, IDENT(x), ASSIGN, NUMBER(10), SEMICOLON]
```

#### 2️⃣ Análise Sintática (Parser)
- **O que faz:** Verifica estrutura gramatical
- **Entrada:** Tokens
- **Saída:** AST (Árvore Sintática Abstrata)

**Exemplo:**
```
AST:
  VarDecl
    ├─ type: int
    ├─ name: x
    └─ value: Literal(10)
```

#### 3️⃣ Análise Semântica
- **O que faz:** Verifica significado do código
- **Verifica:**
  - Variáveis declaradas antes de usar
  - Tipos compatíveis em operações
  - Funções existem
  - Sem redeclarações

#### 4️⃣ Geração de Código LLVM IR
- **O que faz:** Gera código intermediário executável
- **Entrada:** AST validada
- **Saída:** Código LLVM IR (.ll)

---

## 📊 Saída do Compilador

### Compilação Normal

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

============================================================
COMPILAÇÃO CONCLUÍDA COM SUCESSO!
============================================================

📊 Estatísticas:
  • Tokens reconhecidos: 28
  • Nós da AST: 15
  • Erros semânticos: 0
  • Linhas de IR: 24

✓ Compilação concluída com sucesso!
  Arquivo gerado: programa.ll
```

### Compilação com Erro

```
============================================================
FASE 3: ANÁLISE SEMÂNTICA
============================================================
✗ 1 erro(s) semântico(s)
  Erro linha 3: Variável 'y' não declarada

✗ Compilação falhou com 1 erro(s)
```

---

## 🎯 Executando Código Compilado

### Método 1: Interpretador LLVM (lli)

```bash
# Compilar
python compile.py programa.txt

# Executar
lli programa.ll
```

**Vantagens:**
- Rápido
- Não gera arquivos extras
- Ideal para testes

### Método 2: Compilar para Executável Nativo

```bash
# 1. Compilar SimplePOO → LLVM IR
python compile.py programa.txt

# 2. LLVM IR → Assembly
llc programa.ll -o programa.s

# 3. Assembly → Executável
gcc programa.s -o programa.exe

# 4. Executar
./programa.exe
```

**Vantagens:**
- Executável nativo otimizado
- Mais rápido que lli
- Pode distribuir o .exe

### Método 3: Otimizar Código

```bash
# Compilar
python compile.py programa.txt

# Otimizar IR
opt -O2 programa.ll -S -o programa_opt.ll

# Executar otimizado
lli programa_opt.ll
```

---

## ❌ Tratamento de Erros

### Erros Léxicos

```javascript
int x = 10@;  // Erro: caractere inválido '@'
```

**Mensagem:**
```
Erro léxico na linha 1, coluna 11: Token não reconhecido '@'
```

### Erros Sintáticos

```javascript
int x = ;  // Erro: esperava expressão após '='
```

**Mensagem:**
```
Erro sintático: Esperado expressão após '='
```

### Erros Semânticos

```javascript
function main() {
    print(x);  // Erro: 'x' não declarado
}
```

**Mensagem:**
```
Erro linha 2: Variável 'x' não declarada
```

---

## 💡 Dicas e Boas Práticas

### ✅ Fazer

1. **Declare variáveis antes de usar**
   ```javascript
   int x = 10;
   print(x);  // ✓ OK
   ```

2. **Use nomes descritivos**
   ```javascript
   int idade = 25;        // ✓ Bom
   int x = 25;            // ✗ Ruim
   ```

3. **Sempre tenha função main**
   ```javascript
   function main() {
       // Ponto de entrada
   }
   ```

4. **Use parênteses para clareza**
   ```javascript
   int x = (a + b) * c;   // ✓ Claro
   int x = a + b * c;     // ✓ OK, mas menos claro
   ```

### ❌ Evitar

1. **Redeclarar variáveis**
   ```javascript
   int x = 10;
   int x = 20;  // ✗ Erro
   ```

2. **Usar variáveis não declaradas**
   ```javascript
   print(y);    // ✗ Erro se 'y' não foi declarado
   ```

3. **Esquecer ponto e vírgula**
   ```javascript
   int x = 10   // ✗ Erro: falta ';'
   ```

---

## 🔧 Ferramentas Úteis

### Visualizar Código LLVM IR

```bash
python compile.py programa.txt --show-ir
```

### Debug Detalhado

```bash
python compile.py programa.txt -v --show-ir
```

### Verificar Otimizações

```bash
# Gerar IR
python compile.py programa.txt

# Ver diferença com otimizações
opt -O2 -S programa.ll -o programa_opt.ll
diff programa.ll programa_opt.ll
```

---

## 📖 Referência Rápida

### Comandos Essenciais

```bash
# Compilar
python compile.py arquivo.txt

# Compilar e executar
python compile.py arquivo.txt --run

# Modo verbose
python compile.py arquivo.txt -v

# Ver código gerado
python compile.py arquivo.txt --show-ir

# Ajuda
python compile.py --help
```

### Sintaxe Essencial

```javascript
// Declaração de variável
int x = 10;

// Condicional
if (x > 5) { /* ... */ }

// Loop
for (int i = 0; i < 10; i++) { /* ... */ }

// Função
function nome(int param) { /* ... */ }

// Print
print(x);
```

---

## 🎓 Próximos Passos

1. ✅ Experimente os exemplos acima
2. ✅ Crie seus próprios programas
3. ✅ Explore o código LLVM IR gerado (--show-ir)
4. ✅ Teste diferentes otimizações
5. ✅ Compile para executável nativo

---

## 💬 Precisa de Ajuda?

- **Erros de compilação:** Use modo `-v` para mais detalhes
- **Dúvidas sobre sintaxe:** Veja exemplos acima
- **Instalação:** Consulte `INSTALL.md`
- **Visão geral:** Leia `README.md`

---

**Versão:** 1.0  
**Última atualização:** Dezembro 2025  
**Linguagem:** SimplePOO
