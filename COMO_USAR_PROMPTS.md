# 🤖 COMO USAR OS PROMPTS COM ANTIGRAVITY

> **Status**: Pronto para usar
> **Tempo**: 5 min para configurar + 3-4 horas de criação

---

## 📋 RESUMO

Criei **2 prompts** para você usar com o Antigravity:

| Arquivo | Tamanho | Quando Usar |
| :------ | :------ | :---------- |
| **PROMPT_COMPLETO_ANTIGRAVITY.md** | 21 fases, ~600 linhas | Primeira criação, detalhado |
| **PROMPT_RESUMIDO.md** | 26 arquivos, ~200 linhas | Referência rápida, segunda criação |

---

## 🚀 PASSO A PASSO

### 1. Escolha o Prompt

**Primeira vez?** → Use `PROMPT_COMPLETO_ANTIGRAVITY.md`

**Já conhece o projeto?** → Use `PROMPT_RESUMIDO.md`

---

### 2. Abrir Antigravity

No seu ambiente Antigravity, inicie uma nova conversa.

---

### 3. Copiar e Colar o Prompt

**Opção A: Prompt Completo**

```
1. Abra: PROMPT_COMPLETO_ANTIGRAVITY.md
2. Selecione TODO o conteúdo (Ctrl+A)
3. Copie (Ctrl+C)
4. Cole no Antigravity
5. Envie
```

**Opção B: Prompt Resumido**

```
1. Abra: PROMPT_RESUMIDO.md
2. Selecione TODO o conteúdo
3. Copie
4. Cole no Antigravity
5. Envie
```

---

### 4. Aguardar Criação

O Antigravity vai criar **23-26 arquivos** na pasta `mkt/`.

**Tempo estimado**: 3-4 horas de processamento (dependendo da velocidade da IA)

---

### 5. Validar Arquivos Criados

Após criação, execute:

```powershell
cd c:\Users\Marketing\Documents\Antigravity\antigravity-kit

# Verificar estrutura
tree mkt /F

# Ou liste todos os arquivos
dir mkt /s /b
```

**Esperado**: 23+ arquivos criados

---

## 📊 O QUE SERÁ CRIADO

### Estrutura Final

```
mkt/
├── 📘 PRINCIPAIS (10 arquivos)
│   ├── README.md
│   ├── CODEBASE.md
│   ├── AGENT_FLOW.md
│   ├── CHANGELOG.md
│   ├── DOCS_SUMMARY.md
│   ├── init_supabase.sql
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── .gitignore
│   └── test_system.py
│
├── 🐍 ENGINE (7 arquivos)
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── src/
│       ├── __init__.py
│       ├── database.py
│       ├── processor.py
│       ├── watcher.py
│       ├── obsidian.py
│       └── ai_engine.py
│
└── 📚 DOCUMENTAÇÃO (docs/ - 4 arquivos)
    ├── SUMMARY.md
    ├── MANUAL_USUARIO.md
    ├── DEPLOYMENT_CHECKLIST.md
    └── PRODUCT_VISION.md
```

---

## ✅ CHECKLIST PÓS-CRIAÇÃO

Após o Antigravity criar tudo, valide:

### Estrutura de Pastas
- [ ] `mkt/` existe
- [ ] `mkt/engine/` existe
- [ ] `mkt/engine/src/` existe
- [ ] `mkt/docs/` existe
- [ ] `mkt/drive_data/` existe (ou crie manualmente)
- [ ] `mkt/obsidian_data/` existe (ou crie manualmente)

### Arquivos Python
- [ ] `mkt/engine/main.py` existe
- [ ] `mkt/engine/src/database.py` existe
- [ ] `mkt/engine/src/processor.py` existe
- [ ] `mkt/engine/src/watcher.py` existe
- [ ] `mkt/engine/src/obsidian.py` existe
- [ ] `mkt/engine/src/ai_engine.py` existe

### Arquivos de Configuração
- [ ] `mkt/docker-compose.yml` existe
- [ ] `mkt/engine/Dockerfile` existe
- [ ] `mkt/engine/requirements.txt` existe
- [ ] `mkt/.env.example` existe
- [ ] `mkt/.gitignore` existe

### Documentação
- [ ] `mkt/README.md` existe
- [ ] `mkt/CODEBASE.md` existe
- [ ] `mkt/AGENT_FLOW.md` existe
- [ ] `mkt/docs/MANUAL_USUARIO.md` existe
- [ ] `mkt/docs/DEPLOYMENT_CHECKLIST.md` existe

### Testes e Setup
- [ ] `mkt/test_system.py` existe
- [ ] `mkt/setup.ps1` existe

---

## 🚨 PROBLEMAS COMUNS

### Arquivo não criado

**Solução**:
```
Peça para o Antigravity:
"Crie apenas o arquivo X que faltou"
```

### Código incompleto

**Solução**:
```
Peça para o Antigravity:
"Complete o arquivo X, faltam as funções Y e Z"
```

### Erro de sintaxe Python

**Solução**:
```
Peça para o Antigravity:
"Corrija erro de sintaxe no arquivo X"
```

---

## 🎯 PRÓXIMOS PASSOS (Após Criação)

### Dia 1: Validação
1. Revisar arquivos criados
2. Rodar `python -m py_compile mkt/engine/*.py`
3. Verificar se imports funcionam

### Dia 2: Configuração
1. Copiar `.env.example` para `.env`
2. Preencher credenciais do Supabase
3. Executar SQL no Supabase

### Dia 3: Implantação
1. `docker-compose up --build`
2. Rodar testes
3. Testar com arquivo real

---

## 📞 DICAS DE USO

### Para Melhor Resultado

1. **Divida em sessões**:
   - Sessão 1: Fases 1-11 (Infra + Python)
   - Sessão 2: Fases 12-21 (Documentação)
   - Sessão 3: Fases 22-26 (Testes + Setup)

2. **Valide após cada fase**:
   ```
   "Mostre os arquivos criados até agora"
   ```

3. **Peça explicações**:
   ```
   "Explique como funciona o arquivo X"
   ```

4. **Solicite melhorias**:
   ```
   "Melhore a documentação do arquivo Y"
   ```

---

## 🎁 BÔNUS: Comandos Úteis

### Após Criação

```powershell
# Verificar estrutura
tree mkt /F

# Contar linhas de código
(Get-ChildItem mkt -Recurse -Include *.py,*.sql,*.yml,*.md | Get-Content | Measure-Object -Line).Lines

# Testar imports Python
cd mkt/engine
python -c "from src.database import DatabaseHandler; print('OK')"
```

---

## 📚 ARQUIVOS DE REFERÊNCIA

| Arquivo | Finalidade |
| :------ | :--------- |
| `PROMPT_COMPLETO_ANTIGRAVITY.md` | Prompt detalhado (21 fases) |
| `PROMPT_RESUMIDO.md` | Prompt rápido (26 arquivos) |
| `COMO_USAR_PROMPTS.md` | Este arquivo |
| `mkt/DEPLOYMENT_GUIDE.md` | Guia de implantação (pós-criação) |
| `mkt/QUICK_START.txt` | Referência rápida |

---

## 🚀 COMECE AGORA

```bash
# 1. Escolha o prompt (Completo ou Resumido)
# 2. Abra o Antigravity
# 3. Copie e cole o prompt escolhido
# 4. Aguarde criação dos arquivos
# 5. Valide com checklist acima
```

**Boa criação!**

---

<div align="center">

**📦 Prompts prontos para usar!**

`PROMPT_COMPLETO_ANTIGRAVITY.md` — Detalhado  
`PROMPT_RESUMIDO.md` — Rápido

</div>
