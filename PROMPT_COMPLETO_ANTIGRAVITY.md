# 🤖 PROMPT COMPLETO — Marketing Director OS v4.0

> **Para**: Antigravity (Sua IA de Desenvolvimento)
> **Objetivo**: Criar toda a ferramenta de Marketing Director OS
> **Contexto**: Docker já instalado

---

## 📋 CONTEXTO DO PROJETO

Estou criando um **Marketing Director OS** — um sistema operacional de marketing que atua como extensão cognitiva para diretores com TDAH.

**O sistema deve**:
- Ingerir arquivos CSV/PDF do Google Drive automaticamente
- Processar dados e armazenar no Supabase
- Gerar dashboards automáticos no Obsidian
- Fornecer IA contextual que já sabe o contexto do negócio (zero prompts manuais)
- Suportar múltiplas empresas (Salão, Franquias, Diretoria) com isolamento total

**Stack Tecnológico**:
- Supabase (PostgreSQL + pgvector)
- Python (Pandas, watchdog, Supabase client)
- Docker Compose (3 serviços: engine, windmill, db)
- Windmill (painel operacional)
- Obsidian (dashboard estratégico)

---

## 🎯 SUA MISSÃO

Criar TODOS os arquivos necessários para implantar o Marketing Director OS v4.0.

Siga a ordem EXATA abaixo. Não pule etapas.

---

## 📁 ORDEM DE CRIAÇÃO

### FASE 1: Estrutura de Pastas (5 min)

Crie a seguinte estrutura:

```
mkt/
├── engine/
│   └── src/
├── docs/
├── drive_data/
│   ├── salao-esposa/
│   ├── franquia-chapeco/
│   └── diretoria/
└── obsidian_data/
```

**Comando sugerido**:
```python
import os
os.makedirs('mkt/engine/src', exist_ok=True)
os.makedirs('mkt/docs', exist_ok=True)
os.makedirs('mkt/drive_data/salao-esposa', exist_ok=True)
os.makedirs('mkt/drive_data/franquia-chapeco', exist_ok=True)
os.makedirs('mkt/drive_data/diretoria', exist_ok=True)
os.makedirs('mkt/obsidian_data', exist_ok=True)
```

---

### FASE 2: Arquivo SQL do Supabase (10 min)

Crie: `mkt/init_supabase.sql`

**Requisitos**:
- 6 tabelas: tenants, marketing_assets, business_metrics, knowledge_base, strategic_insights, audit_logs
- Row Level Security (RLS) ativado em todas
- Extensão pgvector para busca semântica
- Seeds iniciais com 3 tenants (diretoria, salao-esposa, franquia-chapeco)
- Funções utilitárias (set_current_tenant, match_knowledge_chunks)
- Views para dashboard

**Importante**:
- Use UUID como chave primária
- Timestamp com timezone
- JSONB para metadados
- Comentários em português

---

### FASE 3: Docker Compose (5 min)

Crie: `mkt/docker-compose.yml`

**Serviços obrigatórios**:
1. `marketing_engine` — Python engine (build a partir de ./engine)
2. `windmill` — Painel operacional (ghcr.io/windmill-labs/windmill:latest)
3. `windmill_db` — PostgreSQL para Windmill
4. (Opcional) `pgadmin` — Admin do banco

**Volumes obrigatórios**:
- PATH_TO_DRIVE → /app/drive_input
- PATH_TO_OBSIDIAN → /app/obsidian_output

**Health checks** em todos os serviços.

---

### FASE 4: Dockerfile do Engine (3 min)

Crie: `mkt/engine/Dockerfile`

**Requisitos**:
- FROM python:3.11-slim
- Instalar libmagic1 para detecção de arquivos
- WORKDIR /app
- Copiar requirements.txt e instalar dependências
- Copiar código do engine
- CMD ["python", "main.py"]

---

### FASE 5: Requirements.txt (2 min)

Crie: `mkt/engine/requirements.txt`

**Bibliotecas obrigatórias**:
```
watchdog>=3.0.0
pandas>=2.0.0
supabase>=2.0.0
openai>=1.0.0
python-dotenv>=1.0.0
pypdf>=3.17.0
tiktoken>=0.5.0
pydantic>=2.5.0
requests>=2.31.0
```

---

### FASE 6: Engine Python — Database Handler (15 min)

Crie: `mkt/engine/src/database.py`

**Classe**: `DatabaseHandler`

**Métodos obrigatórios**:
- `__init__()` — Conectar ao Supabase
- `get_tenant_by_slug(slug)` — Buscar tenant
- `insert_asset(...)` — Registrar arquivo processado
- `update_asset_status(...)` — Atualizar status
- `insert_metric(...)` — Inserir KPI
- `insert_metrics_batch(...)` — Inserção em lote
- `insert_knowledge_chunk(...)` — Salvar chunk para RAG
- `insert_knowledge_batch(...)` — Lote de chunks
- `insert_insight(...)` — Salvar insight da IA
- `log_audit(...)` — Log de auditoria
- `health_check()` — Verificar conexão

**Tratamento de erros**: Try/except em todos os métodos, logging detalhado.

---

### FASE 7: Engine Python — Processor (20 min)

Crie: `mkt/engine/src/processor.py`

**Classe**: `FileProcessor`

**Métodos obrigatórios**:
- `__init__(db)` — Inicializar com DatabaseHandler
- `process_file(filepath, tenant_slug)` — Método principal
- `_process_csv(filepath, ...)` — Ler CSV com Pandas, detectar encoding
- `_process_excel(filepath, ...)` — Ler múltiplas abas
- `_process_pdf(filepath, ...)` — Extrair texto com pypdf
- `_process_txt(filepath, ...)` — Ler texto simples
- `_extract_metrics_from_dataframe(df, ...)` — Identificar colunas de métricas
- `_identify_metric_type(column_name)` — Mapear palavras-chave (venda, lead, custo)
- `_find_date_column(df)` — Detectar coluna de data
- `_split_text_into_chunks(text, ...)` — Chunking para RAG

**Keywords para identificar métricas**:
- venda, faturamento, receita → vendas
- lead, contato, prospect → leads
- custo, investimento, gasto → custo
- cliques, impressoes, alcance → marketing
- churn, cancelamento, retencao → fidelizacao

---

### FASE 8: Engine Python — Watcher (15 min)

Crie: `mkt/engine/src/watcher.py`

**Classes**:
1. `DriveWatcher(FileSystemEventHandler)` — Herda de watchdog
2. `WatcherManager` — Gerencia observer

**Métodos obrigatórios**:
- `on_created(event)` — Detectar arquivo novo
- `on_modified(event)` — Detectar modificação
- `_detect_tenant(filepath)` — Identificar tenant pela pasta
- `_process_file(filepath)` — Disparar processamento
- `_write_obsidian_update(tenant_slug, result)` — Atualizar Obsidian
- `start(recursive=True)` — Iniciar watcher
- `run_forever()` — Loop infinito

**Mapeamento de pastas**:
- "salao", "salão", "beleza" → salao-esposa
- "franquia", "unidade", "loja" → franquia-chapeco
- "diretoria", "geral", "hq" → diretoria

---

### FASE 9: Engine Python — Obsidian Bridge (10 min)

Crie: `mkt/engine/src/obsidian.py`

**Classe**: `ObsidianBridge`

**Métodos obrigatórios**:
- `write_dashboard_note(tenant_slug, metrics, insights)` — Dashboard automático
- `write_strategy_note(tenant_slug, title, content)` — Nota de estratégia
- `update_summary_note(summary_data)` — Resumo geral
- `_group_metrics_by_type(metrics)` — Agrupar por categoria

**Template Markdown gerado**:
```markdown
---
tags: [dashboard, salao-esposa, auto-generated]
updated: 2024-01-15 10:30:00
---

# 📊 Dashboard: Salão Lux Beauty

## 📈 Métricas Principais
| Métrica | Valor | Data |
| :------ | :---- | :--- |
| Vendas | R$ 870,00 | 2024-01-15 |

## 🧠 Insights da IA
> Estratégia recomendada...
```

---

### FASE 10: Engine Python — AI Engine (15 min)

Crie: `mkt/engine/src/ai_engine.py`

**Classe**: `AIEngine`

**Suporte a providers**: OpenAI E/OU Gemini

**Métodos obrigatórios**:
- `__init__(db, provider)` — Inicializar cliente
- `_init_openai()` — Configurar OpenAI
- `_init_gemini()` — Configurar Gemini
- `generate_strategic_insight(tenant_id, question, metrics)` — Insight estratégico
- `analyze_metrics_anomaly(tenant_id, current, historical)` — Detectar anomalias
- `generate_marketing_campaign(tenant_id, type, audience, budget)` — Campanha completa
- `_retrieve_context(tenant_id)` — RAG: buscar chunks relevantes
- `_generate_response(prompt)` — Chamar API da IA
- `health_check()` — Verificar se IA está configurada

**Prompt template para insights**:
```
Você é um consultor estratégico de marketing sênior.

EMPRESA: {tenant_name}

CONTEXTO (documentos e histórico):
{context_chunks}

MÉTRICAS ATUAIS:
{metrics}

PERGUNTA: {question}

Seja direto, prático e baseado em dados. Use Markdown.
```

---

### FASE 11: Engine Python — Main (10 min)

Crie: `mkt/engine/main.py`

**Função principal**: `main()`

**Fluxo**:
1. Imprimir banner
2. Validar variáveis de ambiente
3. Inicializar componentes (DatabaseHandler, AIEngine, ObsidianBridge)
4. Health check inicial
5. Sincronização inicial (processar arquivos existentes)
6. Iniciar watcher (loop infinito)

**Logging**:
- Console handler (stdout)
- File handler (logs/engine_YYYYMMDD.log)
- Formato: %(asctime)s | %(levelname)-8s | %(message)s

**Variáveis de ambiente**:
- SUPABASE_URL, SUPABASE_KEY
- OPENAI_API_KEY (ou GEMINI_API_KEY)
- PATH_TO_DRIVE, PATH_TO_OBSIDIAN
- LOG_LEVEL, WATCHER_RECURSIVE

---

### FASE 12: Pacote Python (2 min)

Crie: `mkt/engine/src/__init__.py`

```python
from .database import DatabaseHandler
from .processor import FileProcessor
from .watcher import DriveWatcher
from .obsidian import ObsidianBridge
from .ai_engine import AIEngine

__version__ = "4.0.0"
```

---

### FASE 13: Arquivo .env.example (5 min)

Crie: `mkt/.env.example`

**Variáveis obrigatórias**:
```ini
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...

# IA
OPENAI_API_KEY=sk-proj-...
# GEMINI_API_KEY=...

# Caminhos (usar barras normais /)
PATH_TO_DRIVE=C:/Users/.../drive_data
PATH_TO_OBSIDIAN=C:/Users/.../obsidian_data

# Configurações
WINDMILL_PORT=8000
DB_PASSWORD=changeme123
LOG_LEVEL=INFO
WATCHER_RECURSIVE=true
```

**Comentários explicativos** em cada seção.

---

### FASE 14: .gitignore (3 min)

Crie: `mkt/.gitignore`

**Ignorar obrigatoriamente**:
```
.env
.env.local
*.key
*.pem
__pycache__/
*.pyc
.docker/
logs/
*.log
drive_data/*.csv
drive_data/*.pdf
obsidian_data/*.md
.DS_Store
Thumbs.db
```

---

### FASE 15: README.md (15 min)

Crie: `mkt/README.md`

**Seções obrigatórias**:
1. Visão Geral (o que é, diferenciais)
2. Arquitetura (diagrama ASCII)
3. Stack Tecnológico (tabela)
4. Quick Start (passo-a-passo)
5. Estrutura de Pastas (tree)
6. Modelagem de Dados (tabelas)
7. Casos de Uso (Diretor, Esposa, Franqueados)
8. Roadmap (v0.1 a v10.0)
9. Troubleshooting
10. Links de Documentação

**Tom**: Profissional mas acessível.

---

### FASE 16: CODEBASE.md (20 min)

Crie: `mkt/CODEBASE.md`

**Seções obrigatórias**:
1. Visão Executiva (o que é, para quem)
2. Arquitetura de Sistemas (fluxo de dados)
3. Stack Tecnológico (tabela detalhada)
4. Estrutura de Pastas (tree completo)
5. Modelagem de Dados (todas as colunas)
6. Módulos do Backend (descrição de cada arquivo Python)
7. Frontend (Windmill + Obsidian)
8. Protocolo de Deploy
9. Métricas de Ouro (KPIs do Diretor)
10. Riscos e Mitigações
11. Roadmap
12. Glossário

---

### FASE 17: AGENT_FLOW.md (15 min)

Crie: `mkt/AGENT_FLOW.md`

**Baseado no HIVE OS v4.0**.

**Seções obrigatórias**:
1. Visual Core (ASCII + Mermaid)
2. Step-by-Step Visual Guide (tabela)
3. Detailed Workflow (Boot Sequence, Socratic Gate, Satellites)
4. Native Workflows (tabela de comandos)
5. Checklist de Implementação
6. Validation Pipeline
7. Métricas de Qualidade

---

### FASE 18: Documentação do Usuário (20 min)

Crie em `mkt/docs/`:

**MANUAL_USUARIO.md**:
- Para quem é este manual
- 3 interfaces (Drive, Obsidian, Windmill)
- Estrutura de pastas do Drive
- Tipos de arquivos suportados
- Fluxo de trabalho diário
- Exemplos de uso
- FAQ
- Erros comuns

**DEPLOYMENT_CHECKLIST.md**:
- Fase 0: Pré-requisitos
- Fase 1: Setup do Projeto
- Fase 2: Configurar Supabase
- Fase 3: Iniciar Docker
- Fase 4: Testar Sistema
- Fase 5: Configuração Final
- Troubleshooting

**SUMMARY.md**:
- Índice mestre de toda documentação
- Mapa mental da documentação
- Links para todos os arquivos

**PRODUCT_VISION.md**:
- Declaração de Visão
- Problema que resolvemos
- Solução proposta
- Personas (Diretor, Esposa, Franqueado)
- Princípios de Design
- Roadmap estratégico

---

### FASE 19: Scripts de Teste (10 min)

Crie: `mkt/test_system.py`

**7 testes obrigatórios**:
1. `test_environment()` — Variáveis de ambiente
2. `test_supabase_connection()` — Conexão Supabase
3. `test_docker_services()` — Serviços Docker
4. `test_drive_folder()` — Pasta do Drive
5. `test_obsidian_folder()` — Pasta do Obsidian
6. `test_create_test_file()` — Criar CSV de teste
7. `test_windmill_access()` — Acesso ao Windmill

**Relatório final**: Mostrar quantos testes passaram.

---

### FASE 20: Scripts de Setup (10 min)

Crie: `mkt/setup.ps1` (PowerShell)

**Funcionalidades**:
1. Verificar Docker instalado
2. Criar estrutura de pastas
3. Copiar .env.example para .env
4. Criar arquivos de teste
5. Verificar Docker Desktop rodando
6. Mostrar instruções finais
7. Perguntar se quer iniciar agora

**Interativo**: Usar `Read-Host` para perguntas.

---

### FASE 21: Arquivos Finais (5 min)

Crie:

**CHANGELOG.md**:
- Versão 4.0.0 (atual)
- Adicionado, Mudado, Corrigido, Segurança
- Roadmap futuro

**DOCS_SUMMARY.md**:
- Resumo de toda documentação gerada
- Estatísticas (arquivos, linhas de código)
- Próximos passos

**QUICK_START.txt**:
- Guia ASCII de referência rápida
- 5 passos principais
- Comandos copy/paste
- Troubleshooting rápido

---

## ✅ CHECKLIST DE VALIDAÇÃO

Após criar todos os arquivos, verifique:

### Estrutura
- [ ] `mkt/engine/src/` existe com 6 arquivos Python
- [ ] `mkt/docs/` existe com 4 arquivos Markdown
- [ ] `mkt/drive_data/` existe com 3 subpastas
- [ ] `mkt/obsidian_data/` existe

### Arquivos Principais
- [ ] `init_supabase.sql` — Schema completo
- [ ] `docker-compose.yml` — 3 serviços
- [ ] `engine/Dockerfile` — Build do engine
- [ ] `engine/requirements.txt` — Dependências
- [ ] `.env.example` — Modelo configurável
- [ ] `.gitignore` — Segurança

### Engine Python
- [ ] `main.py` — Ponto de entrada
- [ ] `src/database.py` — Supabase client
- [ ] `src/processor.py` — CSV/PDF parser
- [ ] `src/watcher.py` — File watcher
- [ ] `src/obsidian.py` — Markdown writer
- [ ] `src/ai_engine.py` — IA com RAG
- [ ] `src/__init__.py` — Pacote

### Documentação
- [ ] `README.md` — Visão geral
- [ ] `CODEBASE.md` — Técnico completo
- [ ] `AGENT_FLOW.md` — Workflow
- [ ] `CHANGELOG.md` — Versões
- [ ] `docs/MANUAL_USUARIO.md` — Usuário final
- [ ] `docs/DEPLOYMENT_CHECKLIST.md` — Deploy
- [ ] `docs/SUMMARY.md` — Índice
- [ ] `docs/PRODUCT_VISION.md` — Visão

### Testes e Setup
- [ ] `test_system.py` — 7 testes
- [ ] `setup.ps1` — Setup automático
- [ ] `QUICK_START.txt` — Referência rápida
- [ ] `DOCS_SUMMARY.md` — Resumo

---

## 🎯 REGRAS DE QUALIDADE

### Código Python
- Type hints em todas as funções
- Docstrings em todas as classes e métodos
- Logging em vez de print
- Try/except em operações I/O
- Comentários em português

### SQL
- Comentários explicativos
- Chaves UUID
- RLS em todas as tabelas
- Indexes para performance

### Docker
- Health checks em todos os serviços
- Logs com rotação
- Restart policies

### Documentação
- Markdown formatado corretamente
- Tabelas alinhadas
- Código em blocks com syntax highlighting
- Emojis para navegação visual
- Tom profissional mas acessível

---

## 🚀 INSTRUÇÕES FINAIS

1. **Siga a ordem EXATA** das 21 fases
2. **Não pule nenhuma fase**
3. **Valide cada arquivo** após criar
4. **Use o checklist** para verificar completude
5. **Teste mentalmente** o fluxo de cada componente

**Tempo estimado total**: 4-5 horas de desenvolvimento

**Entregável**: Pasta `mkt/` completa com todos os 23+ arquivos

---

## 📞 SUPORTE DURANTE DESENVOLVIMENTO

Se tiver dúvidas durante a criação:

1. **Consulte** `AGENT_FLOW.md` para workflow
2. **Valide** com Socratic Gate (4 questões)
3. **Mantenha** Truth in Data (zero mocks)
4. **Priorize** Back-end First (SQL → Python → Docker → Frontend)

---

<div align="center">

**🚀 Comece agora pela FASE 1: Estrutura de Pastas**

*Boa criação!*

</div>
