# 🐍 INSTALAÇÃO DO PYTHON NO WINDOWS

> **Status**: ⚠️ Python não encontrado  
> **Ação Necessária**: Instalar Python para rodar o Marketing Engine

---

## 📋 RESUMO DO PROBLEMA

O Marketing Engine v5.3 é um sistema Python que requer:
- ✅ Python 3.9+ instalado
- ✅ Ambiente virtual (.venv) configurado
- ✅ Dependências instaladas

**Situação atual**: Python não encontrado no Windows.

---

## 🚀 OPÇÃO 1: INSTALAÇÃO RECOMENDADA (Python.org)

### Passo 1: Baixar Python

1. Acesse: **https://www.python.org/downloads/**
2. Clique em **"Download Python 3.12.x"** (ou versão mais recente)
3. Salve o instalador (`python-3.12.x-amd64.exe`)

### Passo 2: Instalar

1. **Execute o instalador**
2. ⚠️ **IMPORTANTE**: Marque a caixa ✅ **"Add Python to PATH"**
3. Clique em **"Install Now"**
4. Aguarde a instalação concluir

### Passo 3: Verificar

Abra o **Prompt de Comando (cmd)** e digite:

```bash
python --version
```

Deve aparecer: `Python 3.12.x`

---

## 🚀 OPÇÃO 2: MICROSOFT STORE (Mais Simples)

### Passo 1: Abrir Microsoft Store

1. Pressione `Windows + S`
2. Digite **"Microsoft Store"**
3. Abra a loja

### Passo 2: Instalar Python

1. Busque por **"Python 3.12"** ou **"Python 3.11"**
2. Clique em **"Obter"** ou **"Instalar"**
3. Aguarde a instalação

### Passo 3: Verificar

```bash
python --version
```

---

## 🔧 CONFIGURAR AMBIENTE VIRTUAL

Após instalar o Python, configure o ambiente:

### Passo 1: Navegar até o projeto

```bash
cd C:\Users\Marketing\Documents\Antigravity\antigravity-kit
```

### Passo 2: Remover .venv antiga (Mac)

```bash
# No Prompt de Comando:
rmdir /s /q .venv

# Ou no PowerShell:
Remove-Item -Recurse -Force .venv
```

### Passo 3: Criar nova .venv (Windows)

```bash
python -m venv .venv
```

### Passo 4: Ativar ambiente virtual

```bash
# No Prompt de Comando:
.venv\Scripts\activate

# No PowerShell:
.venv\Scripts\Activate.ps1
```

Você verá `(.venv)` no início do prompt.

### Passo 5: Instalar dependências

```bash
pip install --upgrade pip
pip install -r mkt/engine/requirements.txt
```

---

## ✅ VERIFICAR INSTALAÇÃO

### Testar Python

```bash
python --version
# Deve mostrar: Python 3.x.x
```

### Testar pip

```bash
pip --version
# Deve mostrar: pip X.X.X from ...
```

### Testar dependências

```bash
python -c "import pandas; import numpy; import fastapi; print('✅ Dependências OK')"
```

---

## 🧪 RODAR TESTES

### Teste 1: Script de IA

```bash
cd mkt/engine
python test_ai_insights.py
```

### Teste 2: Main Engine

```bash
cd mkt/engine
python -m main
```

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### Problema: "python não é reconhecido"

**Solução 1**: Reinicie o terminal após instalar

**Solução 2**: Verifique se Python está no PATH
```bash
where python
```

**Solução 3**: Use `py` ao invés de `python`
```bash
py --version
py -m venv .venv
```

### Problema: Erro ao criar .venv

**Solução**:
```bash
# Tente com py (Python Launcher)
py -m venv .venv

# Ou com python3
python3 -m venv .venv
```

### Problema: Permissão negada no PowerShell

**Solução**: Execute como Administrador ou:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: pip não encontrado

**Solução**:
```bash
python -m ensurepip --upgrade
```

---

## 📦 INSTALAÇÃO DAS DEPENDÊNCIAS

Após criar e ativar o ambiente virtual:

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar tudo
pip install -r mkt/engine/requirements.txt

# Ou instalar manualmente:
pip install watchdog pandas openpyxl numpy
pip install fastapi uvicorn
pip install supabase psycopg2-binary
pip install openai tiktoken anthropic groq ollama
pip install python-dotenv pydantic requests python-dateutil
pip install plotly jinja2
```

---

## 🎯 CHECKLIST DE INSTALAÇÃO

- [ ] Python 3.9+ instalado
- [ ] `python --version` funciona
- [ ] `pip --version` funciona
- [ ] .venv antiga removida
- [ ] Nova .venv criada (`python -m venv .venv`)
- [ ] Ambiente ativado (`.venv\Scripts\activate`)
- [ ] Dependências instaladas (`pip install -r mkt/engine/requirements.txt`)
- [ ] Teste básico funcionou (`python -c "import pandas; print('OK')"`)

---

## 🚀 PRÓXIMOS PASSOS

Após instalar Python e dependências:

1. **Configurar .env**:
   ```bash
   copy mkt\.env.example mkt\.env
   ```

2. **Editar .env** com:
   - SUPABASE_URL, SUPABASE_KEY
   - GROQ_API_KEY (https://console.groq.com/keys)
   - PATH_TO_DRIVE
   - PATH_TO_OBSIDIAN

3. **Rodar testes**:
   ```bash
   cd mkt/engine
   python test_ai_insights.py
   ```

4. **Rodar sistema**:
   ```bash
   python -m main
   ```

5. **Abrir Obsidian** e ver dashboards

---

## 📞 PRECISO DE AJUDA?

Me informe:

1. **Qual opção você escolheu?** (Python.org ou Microsoft Store)
2. **Em qual passo encontrou problemas?**
3. **Qual erro apareceu?** (copie e cole o erro)

Posso então fornecer instruções específicas para seu caso!

---

## 🎯 COMANDO RÁPIDO (Se Python já estiver instalado)

Se Python já estiver instalado, execute em sequência:

```bash
# 1. Navegar até projeto
cd C:\Users\Marketing\Documents\Antigravity\antigravity-kit

# 2. Remover .venv antiga
rmdir /s /q .venv

# 3. Criar nova .venv
python -m venv .venv

# 4. Ativar
.venv\Scripts\activate

# 5. Instalar dependências
pip install -r mkt/engine/requirements.txt

# 6. Testar
python -c "import pandas; print('✅ Python configurado!')"
```

---

<div align="center">

**🐍 INSTALE O PYTHON PARA CONTINUAR**

*Escolha: Python.org (recomendado) ou Microsoft Store*

**Tempo estimado: 5-10 minutos**

</div>
