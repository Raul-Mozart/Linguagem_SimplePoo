# 🚀 TESTE RÁPIDO - 2 Minutos

> Guia ultra-rápido para testar o compilador SimplePOO

---

## ⚡ Passo a Passo (Windows)

### 1. Abrir PowerShell
- Pressione `Windows + X`
- Escolha "Windows PowerShell"

### 2. Ir para a Pasta do Projeto
```powershell
cd C:\Users\User\Downloads\Linguagem_SimplePoo
```

### 3. Testar Ajuda
```powershell
python compile.py --help
```

**Deve mostrar:** Menu de ajuda do compilador ✅

---

## 🎯 Testes Básicos

### Teste 1: Hello World (30 segundos)
```powershell
python compile.py exemplos/01_hello.txt
```

**Resultado esperado:**
```
✓ Compilação concluída com sucesso!
  Arquivo gerado: exemplos/01_hello.ll
```

### Teste 2: Soma com Detalhes (1 minuto)
```powershell
python compile.py exemplos/02_soma.txt -v
```

**Resultado esperado:**
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

📊 Estatísticas:
  • Tokens reconhecidos: 28
  • Nós da AST: 15
  • Erros semânticos: 0
  • Linhas de IR: 24

✓ Compilação concluída com sucesso!
```

### Teste 3: Ver Código Gerado (30 segundos)
```powershell
type exemplos\02_soma.ll
```

**Resultado esperado:**
```llvm
@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"

; ModuleID = 'SimplePOO'
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define void @main() {
  entry:
    %0 = alloca i64
    store i64 10, i64* %0
    %1 = alloca i64
    store i64 20, i64* %1
    %2 = alloca i64
    %3 = load i64, i64* %0
    %4 = load i64, i64* %1
    %5 = add i64 %3, %4
    store i64 %5, i64* %2
    %6 = load i64, i64* %2
    %7 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %7, i64 %6)
    ret void
}
```

---

## 🔥 Testar Todos os Exemplos (2 minutos)

```powershell
# Hello World
python compile.py exemplos/01_hello.txt

# Soma
python compile.py exemplos/02_soma.txt

# Condicional
python compile.py exemplos/03_condicional.txt

# Loop
python compile.py exemplos/04_loop.txt

# Operações
python compile.py exemplos/05_operacoes.txt
```

**Todos devem compilar com sucesso!** ✅

---

## 🐧 Linux/macOS

Mesmos comandos, mas use `python3`:

```bash
python3 compile.py exemplos/01_hello.txt
python3 compile.py exemplos/02_soma.txt -v
cat exemplos/02_soma.ll
```

---

## ❌ Se Algo Der Errado

### "python não é reconhecido"
**Solução:** Instale Python 3.8+ de https://www.python.org/

### "ModuleNotFoundError"
**Solução:** Certifique-se de estar na pasta raiz do projeto:
```powershell
cd C:\Users\User\Downloads\Linguagem_SimplePoo
```

### Outro problema?
**Consulte:** `INSTALL.md` para instalação completa

---

## ✅ Checklist de Teste

- [ ] `python compile.py --help` funciona
- [ ] `python compile.py exemplos/01_hello.txt` compila
- [ ] Arquivo `.ll` é gerado
- [ ] `python compile.py exemplos/02_soma.txt -v` mostra 4 fases
- [ ] Todos os 5 exemplos compilam

**Tudo ✅? Compilador funcionando perfeitamente!**

---

## 📚 Próximos Passos

1. ✅ Leia `MANUAL_USO.md` para aprender mais
2. ✅ Crie seu próprio programa `.txt`
3. ✅ Compile com `python compile.py seu_programa.txt`
4. ✅ Explore o código LLVM IR gerado

---

## 🎯 Comando Favorito

```powershell
python compile.py exemplos/02_soma.txt -v --show-ir
```

Mostra **tudo**: 4 fases + código IR completo!

---

**Tempo total:** ~2 minutos  
**Dificuldade:** ⭐☆☆☆☆ (Muito fácil)  
**Resultado:** Compilador 100% funcional ✅
