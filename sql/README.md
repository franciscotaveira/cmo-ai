# 🗄️ CMO 360° — SQL Migration Scripts

> **Versão**: v5.3  
> **Status**: ✅ Pronto para executar  
> **Tempo estimado**: 5-10 minutos

---

## 📋 ORDEM DE EXECUÇÃO

Execute os scripts **nesta ordem exata**:

| # | Arquivo | Finalidade | Tempo |
| :- | :------ | :--------- | :---- |
| 1 | `01_check_extensions.sql` | Cria extensões (vector, uuid-ossp) | 30s |
| 2 | `02_drop_existing.sql` | Remove tabelas antigas ⚠️ | 30s |
| 3 | `03_create_tables.sql` | Cria 8 tabelas principais | 1min |
| 4 | `04_create_indexes.sql` | Cria índices para performance | 1min |
| 5 | `05_create_functions.sql` | Cria funções e triggers | 1min |
| 6 | `06_enable_rls.sql` | Habilita Row Level Security | 1min |
| 7 | `07_seed_data.sql` | Insere dados de teste | 1min |
| 8 | `08_verify_install.sql` | Verifica instalação | 30s |

---

## 🚀 COMO EXECUTAR

### Passo 1: Acessar Supabase

1. Acesse: **https://supabase.com/dashboard**
2. Selecione seu projeto
3. Vá em: **SQL Editor**

### Passo 2: Executar Scripts

Para cada script (na ordem acima):

1. Abra o arquivo `.sql` no seu computador
2. Copie **TODO** o conteúdo
3. Cole no SQL Editor do Supabase
4. Clique em **RUN** (ou Ctrl+Enter)
5. Aguarde a confirmação ✅
6. Passe para o próximo script

### Passo 3: Verificar

Após executar todos os scripts:

1. Execute: `08_verify_install.sql`
2. Verifique se todas as verificações mostram ✅
3. Se algo falhar, veja a seção de Solução de Problemas

---

## 📊 O QUE SERÁ CRIADO

### 8 Tabelas Principais

```
1. tenants              — Empresas/unidades de negócio
2. marketing_assets     — Arquivos processados (CSV, PDF, XLSX)
3. business_metrics     — KPIs e métricas de negócio
4. knowledge_base       — Base de conhecimento (RAG/IA)
5. strategic_insights   — Insights e estratégias da IA
6. anomaly_alerts       — Alertas de anomalias (Z-Score)
7. audit_logs           — Log de auditoria
8. automation_queue     — Fila de automações (HitL)
```

### 5 Funções Utilitárias

```
1. set_current_tenant()        — Define tenant atual (RLS)
2. match_knowledge_chunks()    — Busca semântica (RAG)
3. update_updated_at_column()  — Atualiza updated_at automaticamente
4. get_tenant_metrics_summary() — Resumo de métricas
5. get_tenant_dashboard()      — Dashboard completo
```

### Índices de Performance

- ~25 índices criados automaticamente
- Otimizados para consultas por tenant, data, métrica
- Índice ivfflat para busca vetorial (knowledge_base)

### Row Level Security (RLS)

- 8 tabelas com RLS habilitado
- Políticas de isolamento por tenant
- Grants para service_role e authenticated

---

## 🔍 VERIFICAÇÃO RÁPIDA

Após instalar, execute no SQL Editor:

```sql
-- Verificar tabelas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_name IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  )
ORDER BY table_name;

-- Verificar tenants
SELECT * FROM tenants;

-- Verificar extensão vector
SELECT * FROM pg_extension WHERE extname = 'vector';
```

**Resultado esperado**: 8 linhas nas tabelas, 6 tenants, extensão vector presente.

---

## ⚠️ SOLUÇÃO DE PROBLEMAS

### "relation already exists"

**Erro**: Tabela já existe.

**Solução**:
```sql
-- Opção 1: Dropar e recriar (perde dados!)
DROP TABLE IF EXISTS public.tenants CASCADE;

-- Opção 2: Pular criação
-- O script 03_create_tables.sql já usa IF NOT EXISTS
```

### "extension vector does not exist"

**Erro**: Extensão pgvector não instalada.

**Solução**:
```sql
-- Instalar extensão
CREATE EXTENSION IF NOT EXISTS vector;

-- Se falhar, ative no dashboard:
-- Supabase Dashboard → Database → Extensions → Enable "pgvector"
```

### "function uuid_generate_v4() does not exist"

**Erro**: Extensão uuid-ossp não instalada.

**Solução**:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### "permission denied"

**Erro**: Sem permissão.

**Solução**:
```sql
-- Grant para service_role
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;
```

### "column is_active does not exist"

**Erro**: Coluna faltando em tabela existente.

**Solução**:
```sql
-- Adicionar coluna faltante
ALTER TABLE public.tenants ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
```

---

## 📚 ESTRUTURA DAS TABELAS

### tenants
```sql
id              UUID PRIMARY KEY
name            TEXT NOT NULL
slug            TEXT UNIQUE NOT NULL
type            TEXT (diretoria, franquia, salao, ecommerce, saas, servicos)
settings        JSONB
business_config JSONB
created_at      TIMESTAMP
updated_at      TIMESTAMP
is_active       BOOLEAN DEFAULT TRUE
```

### marketing_assets
```sql
id                UUID PRIMARY KEY
tenant_id         UUID REFERENCES tenants(id)
file_name         TEXT NOT NULL
file_path         TEXT NOT NULL
file_type         TEXT (csv, pdf, xlsx, xls, txt, json)
processed         BOOLEAN DEFAULT FALSE
processing_status TEXT (pending, processing, completed, error)
error_message     TEXT
metadata          JSONB
ingested_at       TIMESTAMP
processed_at      TIMESTAMP
```

### business_metrics
```sql
id            UUID PRIMARY KEY
tenant_id     UUID REFERENCES tenants(id)
asset_id      UUID REFERENCES marketing_assets(id)
metric_key    TEXT NOT NULL (cac, ltv, roi, revenue, leads, etc.)
metric_value  NUMERIC NOT NULL
metric_unit   TEXT (BRL, percentage, count, ratio)
date_ref      DATE NOT NULL
period_type   TEXT (daily, weekly, monthly, yearly)
metadata      JSONB
created_at    TIMESTAMP
updated_at    TIMESTAMP
```

### knowledge_base
```sql
id            UUID PRIMARY KEY
tenant_id     UUID REFERENCES tenants(id)
asset_id      UUID REFERENCES marketing_assets(id)
content_chunk TEXT NOT NULL
chunk_index   INTEGER DEFAULT 0
embedding     VECTOR(1536)
metadata      JSONB
created_at    TIMESTAMP
```

### strategic_insights
```sql
id               UUID PRIMARY KEY
tenant_id        UUID REFERENCES tenants(id)
context          TEXT NOT NULL
ai_response      TEXT NOT NULL
source_model     TEXT
confidence_score NUMERIC(3,2)
status           TEXT (new, reviewing, applied, archived, rejected)
user_feedback    TEXT
user_rating      INTEGER (1-5)
created_at       TIMESTAMP
reviewed_at      TIMESTAMP
applied_at       TIMESTAMP
```

### anomaly_alerts
```sql
id             UUID PRIMARY KEY
tenant_id      UUID REFERENCES tenants(id)
metric_key     TEXT NOT NULL
metric_value   NUMERIC NOT NULL
expected_value NUMERIC
z_score        NUMERIC
severity       TEXT (low, medium, high, critical)
threshold      NUMERIC DEFAULT 2.0
is_anomaly     BOOLEAN (calculado)
status         TEXT (new, acknowledged, resolved, dismissed)
action_taken   BOOLEAN DEFAULT FALSE
action_details JSONB
detected_at    TIMESTAMP
acknowledged_at TIMESTAMP
resolved_at    TIMESTAMP
```

### audit_logs
```sql
id         UUID PRIMARY KEY
tenant_id  UUID REFERENCES tenants(id)
action     TEXT NOT NULL
actor_type TEXT (user, system, engine, ia)
actor_id   TEXT
details    JSONB
ip_address INET
created_at TIMESTAMP
```

### automation_queue
```sql
id              UUID PRIMARY KEY
tenant_id       UUID REFERENCES tenants(id)
automation_type TEXT NOT NULL
status          TEXT (pending, processing, completed, failed, cancelled)
trigger_source  TEXT (manual, anomaly, insight, scheduled)
priority        INTEGER (1-10)
payload         JSONB NOT NULL
result          JSONB
approved_by     UUID
approved_at     TIMESTAMP
scheduled_for   TIMESTAMP
started_at      TIMESTAMP
completed_at    TIMESTAMP
error_message   TEXT
```

---

## 🎯 PRÓXIMOS PASSOS

Após a migração:

1. **Configurar .env**:
   ```bash
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua-chave-service-role
   ```

2. **Testar conexão**:
   ```bash
   cd c:\Users\Marketing\Documents\Antigravity\antigravity-kit
   .venv_mkt\Scripts\activate
   python -m mkt.engine.main
   ```

3. **Verificar logs**:
   ```
   ✅ Conexão com Supabase estabelecida
   ✅ DatabaseHandler inicializado
   ```

4. **Acessar Obsidian**:
   ```
   🧠 EXOCÓRTEX/00 - Dashboards/
   └── 🌍 CMO-Dashboard-*.md
   ```

---

## 📞 PRECISA DE AJUDA?

Se encontrar erros:

1. **Copie o erro completo**
2. **Verifique qual script falhou**
3. **Consulte a seção de Solução de Problemas**
4. **Me informe** o erro

---

<div align="center">

**🗄️ CMO 360° SQL MIGRATION**

*v5.3 — 8 scripts • 8 tabelas • 5 funções • RLS habilitado*

**Tempo: 5-10 minutos • Status: Pronto para produção**

</div>
