# 🎯 PROMPT RESUMIDO — Marketing Director OS v4.0

> **Versão**: Curta e Direta
> **Para**: Antigravity
> **Tempo de Leitura**: 2 min

---

## 📋 CONTEXTO

Criar **Marketing Director OS v4.0** — sistema que:
- Lê CSV/PDF do Google Drive automaticamente
- Armazena dados no Supabase
- Gera dashboards no Obsidian
- IA contextual com RAG (zero prompts manuais)
- Multi-tenant (Salão, Franquias, Diretoria)

**Stack**: Supabase + Python + Docker + Windmill + Obsidian

---

## 🎯 SUA MISSÃO

Criar TODOS os 23 arquivos listados abaixo, na ordem exata.

---

## 📁 ARQUIVOS PARA CRIAR

### 1-5: Infraestrutura Básica
```
1. mkt/init_supabase.sql          (6 tabelas + RLS + pgvector + seeds)
2. mkt/docker-compose.yml          (3 serviços: engine, windmill, db)
3. mkt/engine/Dockerfile           (Python 3.11-slim)
4. mkt/engine/requirements.txt     (watchdog, pandas, supabase, openai)
5. mkt/.env.example                (Supabase, IA, caminhos)
```

### 6-11: Engine Python
```
6. mkt/engine/main.py              (watcher + processamento)
7. mkt/engine/src/__init__.py      (pacote)
8. mkt/engine/src/database.py      (DatabaseHandler, ~400 linhas)
9. mkt/engine/src/processor.py     (FileProcessor, ~500 linhas)
10. mkt/engine/src/watcher.py      (DriveWatcher, ~350 linhas)
11. mkt/engine/src/obsidian.py     (ObsidianBridge, ~300 linhas)
12. mkt/engine/src/ai_engine.py    (AIEngine com RAG, ~350 linhas)
```

### 13-17: Documentação Técnica
```
13. mkt/README.md                  (visão geral, quick start)
14. mkt/CODEBASE.md                (doc técnica completa)
15. mkt/AGENT_FLOW.md              (workflow HIVE OS)
16. mkt/CHANGELOG.md               (histórico versões)
17. mkt/.gitignore                 (segurança)
```

### 18-21: Documentação do Usuário
```
18. mkt/docs/MANUAL_USUARIO.md     (guia usuário final)
19. mkt/docs/DEPLOYMENT_CHECKLIST.md (passo-a-passo 30 min)
20. mkt/docs/SUMMARY.md            (índice mestre)
21. mkt/docs/PRODUCT_VISION.md     (visão estratégica)
```

### 22-23: Testes e Setup
```
22. mkt/test_system.py             (7 testes automatizados)
23. mkt/setup.ps1                  (setup automático PowerShell)
```

### 24-26: Arquivos Finais
```
24. mkt/DOCS_SUMMARY.md            (resumo documentação)
25. mkt/QUICK_START.txt            (referência rápida ASCII)
26. mkt/PROMPT_COMPLETO.md         (este arquivo)
```

---

## 🎯 REGRAS DE QUALIDADE

### Python
- Type hints em tudo
- Docstrings em classes e métodos
- Logging (não print)
- Try/except em I/O
- Comentários em português

### SQL
- RLS em todas tabelas
- UUID chaves primárias
- Indexes para performance
- Comentários explicativos

### Docker
- Health checks
- Restart policies
- Logs com rotação

### Documentação
- Markdown formatado
- Tabelas alinhadas
- Emojis para navegação
- Tom profissional

---

## ✅ CHECKLIST DE VALIDAÇÃO

Após criar, verifique:

**Estrutura**:
- [ ] `mkt/engine/src/` com 6 arquivos .py
- [ ] `mkt/docs/` com 4 arquivos .md
- [ ] `mkt/drive_data/` com 3 subpastas
- [ ] `mkt/obsidian_data/` existe

**Funcional**:
- [ ] `docker-compose up --build` funciona
- [ ] SQL cria 6 tabelas no Supabase
- [ ] Python importa sem erros
- [ ] Testes rodam (`python test_system.py`)

**Documentação**:
- [ ] README.md tem quick start
- [ ] CODEBASE.md tem arquitetura completa
- [ ] MANUAL_USUARIO.md é compreensível por leigos

---

## 🚀 ORDEM DE EXECUÇÃO

**Siga esta ordem**:

1. **Fase 1**: Estrutura de pastas (5 min)
2. **Fase 2**: `init_supabase.sql` (10 min)
3. **Fase 3**: `docker-compose.yml` (5 min)
4. **Fase 4**: `Dockerfile` (3 min)
5. **Fase 5**: `requirements.txt` (2 min)
6. **Fase 6-11**: Engine Python (60 min)
7. **Fase 12-17**: Documentação Técnica (60 min)
8. **Fase 18-21**: Documentação Usuário (40 min)
9. **Fase 22-26**: Testes e Setup (20 min)

**Total**: ~3-4 horas

---

## 📞 PRINCÍPIOS

1. **Back-end First**: SQL → Python → Docker → Frontend
2. **Truth in Data**: Zero mocks, zero placeholders
3. **Tenant Isolation**: RLS em todas tabelas
4. **Zero Prompt Manual**: IA já sabe contexto via RAG
5. **Gestão por Exceção**: Só mostra problemas

---

## 🎯 COMECE AGORA

```bash
# Passo 1: Criar estrutura
mkdir -p mkt/engine/src mkt/docs mkt/drive_data/{salao-esposa,franquia-chapeco,diretoria} mkt/obsidian_data

# Passo 2: Começar pelo SQL
# Criar: mkt/init_supabase.sql
```

**Boa criação!**

---

<div align="center">

**Prompt Completo**: `PROMPT_COMPLETO_ANTIGRAVITY.md`  
**Este Arquivo**: Versão resumida para referência rápida

</div>
