# 📦 Manual de Instalação - Compilador SimplePOO

> Guia completo para instalar e configurar o compilador SimplePOO no seu computador

---

## 📋 Pré-requisitos

O compilador SimplePOO precisa de:
- **Python 3.8 ou superior**
- **LLVM 10.0 ou superior** (para executar o código gerado)

---

## 🪟 Instalação no Windows

### Passo 1: Instalar Python

1. **Baixar Python:**
   - Acesse: https://www.python.org/downloads/
   - Clique em "Download Python 3.x"
   - Baixe o instalador para Windows

2. **Instalar Python:**
   - Execute o arquivo baixado (ex: `python-3.12.0-amd64.exe`)
   - ⚠️ **IMPORTANTE:** Marque a opção **"Add Python to PATH"**
   - Clique em "Install Now"
   - Aguarde a instalação

3. **Verificar instalação:**
   - Abra o PowerShell (tecla Windows + X → PowerShell)
   - Digite:
     ```powershell
     python --version
     ```
   - Deve mostrar algo como: `Python 3.12.0`

### Passo 2: Instalar LLVM (Opcional - para executar código compilado)

1. **Baixar LLVM:**
   - Acesse: https://github.com/llvm/llvm-project/releases
   - Procure por "LLVM-XX.X.X-win64.exe" (versão mais recente)
   - Baixe o instalador

2. **Instalar LLVM:**
   - Execute o arquivo baixado
   - Durante a instalação, escolha **"Add LLVM to system PATH"**
   - Clique em "Install"

3. **Verificar instalação:**
   ```powershell
   lli --version
   ```
   - Deve mostrar a versão do LLVM instalada

**Alternativa sem instalador:** Usar Chocolatey
```powershell
# Instalar Chocolatey primeiro (se não tiver)
# Depois:
choco install llvm
```

### Passo 3: Baixar o Compilador

1. **Clonar o repositório (se tiver Git):**
   ```powershell
   git clone <url-do-repositorio>
   cd Linguagem_SimplePoo
   ```

2. **OU baixar ZIP:**
   - Baixe o projeto como ZIP
   - Extraia em uma pasta (ex: `C:\SimplePOO`)
   - Abra o PowerShell nessa pasta

### Passo 4: Testar Instalação

```powershell
# Testar o compilador
python compile.py --help
```

Se aparecer a ajuda do compilador, está tudo certo! ✅

---

## 🐧 Instalação no Linux (Ubuntu/Debian)

### Passo 1: Instalar Python

```bash
# Atualizar repositórios
sudo apt update

# Instalar Python 3
sudo apt install python3 python3-pip

# Verificar instalação
python3 --version
```

### Passo 2: Instalar LLVM

```bash
# Instalar LLVM e ferramentas
sudo apt install llvm

# Verificar instalação
lli --version
```

### Passo 3: Baixar o Compilador

```bash
# Clonar repositório
git clone <url-do-repositorio>
cd Linguagem_SimplePoo

# Dar permissão de execução
chmod +x compile.py
```

### Passo 4: Testar Instalação

```bash
python3 compile.py --help
```

---

## 🍎 Instalação no macOS

### Passo 1: Instalar Python

```bash
# Usando Homebrew (se não tiver, instale em https://brew.sh)
brew install python3

# Verificar
python3 --version
```

### Passo 2: Instalar LLVM

```bash
# Instalar LLVM via Homebrew
brew install llvm

# Adicionar ao PATH (adicione ao ~/.zshrc ou ~/.bash_profile)
echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verificar
lli --version
```

### Passo 3: Baixar e Testar

```bash
git clone <url-do-repositorio>
cd Linguagem_SimplePoo
python3 compile.py --help
```

---

## ✅ Verificação Completa

Execute este teste para garantir que tudo funciona:

### 1. Criar programa de teste

Crie um arquivo `teste.txt`:
```javascript
function main() {
    int x = 10;
    int y = 20;
    int soma = x + y;
    print(soma);
}
```

### 2. Compilar

```bash
# Windows (PowerShell)
python compile.py teste.txt

# Linux/macOS
python3 compile.py teste.txt
```

**Saída esperada:**
```
[INFO] FASE 1: ANÁLISE LÉXICA
[OK] X tokens reconhecidos
[INFO] FASE 2: ANÁLISE SINTÁTICA
[OK] AST construída com sucesso
[INFO] FASE 3: ANÁLISE SEMÂNTICA
[OK] Verificação semântica concluída
[INFO] FASE 4: GERAÇÃO DE CÓDIGO LLVM IR
[OK] Código LLVM IR gerado
[OK] COMPILAÇÃO CONCLUÍDA COM SUCESSO!
```

### 3. Executar (se LLVM instalado)

```bash
# Windows
lli teste.ll

# Linux/macOS
lli teste.ll
```

**Saída esperada:**
```
30
```

---

## 🔧 Resolução de Problemas

### ❌ "python não é reconhecido como comando"

**Solução:**
- Windows: Reinstale Python marcando "Add to PATH"
- Linux/macOS: Use `python3` ao invés de `python`

### ❌ "lli não é reconhecido como comando"

**Solução Windows:**
1. Adicione LLVM ao PATH manualmente:
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Edite PATH, adicione `C:\Program Files\LLVM\bin`
2. Reinicie o PowerShell

**Solução Linux:**
```bash
sudo apt install llvm
```

### ❌ "Import Error" ao executar compile.py

**Solução:**
Certifique-se de estar na pasta raiz do projeto:
```bash
cd Linguagem_SimplePoo
python compile.py teste.txt
```

### ❌ Erro "ModuleNotFoundError"

**Solução:**
Verifique a estrutura de pastas:
```
Linguagem_SimplePoo/
├── compile.py          ← Você está aqui
├── lexer/
│   └── lexer_enhanced.py
└── parser/
    ├── parser.py
    ├── semantic_analyzer.py
    └── code_generator.py
```

---

## 📱 Verificação Rápida de Dependências

Execute este script Python para verificar tudo:

```python
# verificar.py
import sys
import subprocess

print("🔍 Verificando instalação...\n")

# Python
print(f"✓ Python: {sys.version}")

# LLVM
try:
    result = subprocess.run(['lli', '--version'], capture_output=True, text=True)
    print(f"✓ LLVM: Instalado")
except:
    print("✗ LLVM: Não instalado (opcional)")

# Módulos do compilador
try:
    sys.path.insert(0, 'lexer')
    sys.path.insert(0, 'parser')
    import lexer_enhanced
    import parser
    import semantic_analyzer
    import code_generator
    print("✓ Módulos do compilador: OK")
except Exception as e:
    print(f"✗ Módulos: {e}")

print("\n✅ Verificação completa!")
```

Execute:
```bash
python verificar.py
```

---

## 🎯 Próximos Passos

Agora que instalou tudo:

1. ✅ Leia o **MANUAL_USO.md** para aprender a usar o compilador
2. ✅ Explore os exemplos na pasta `exemplos/`
3. ✅ Compile seu primeiro programa SimplePOO

---

## 📚 Recursos Adicionais

- **Python:** https://www.python.org/
- **LLVM:** https://llvm.org/
- **Documentação SimplePOO:** Veja README.md na raiz do projeto

---

## 💬 Precisa de Ajuda?

Se encontrar problemas:

1. Verifique se seguiu todos os passos
2. Reinicie o terminal/PowerShell
3. Certifique-se de estar na pasta correta
4. Execute o script de verificação acima

---

**Versão:** 1.0  
**Última atualização:** Dezembro 2025  
**Compatibilidade:** Windows 10/11, Linux, macOS
