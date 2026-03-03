# 🚀 GUIA RÁPIDO — Instalação do Banco de Dados

> **Tempo**: 5-10 minutos  
> **Dificuldade**: Fácil  
> **Status**: ✅ Pronto

---

## ⚡ RESUMO EM 3 PASSOS

### 1️⃣ ABRIR SUPABASE
```
https://supabase.com/dashboard → Seu Projeto → SQL Editor
```

### 2️⃣ EXECUTAR SCRIPTS (na ordem)
```
1. 01_check_extensions.sql
2. 03_create_tables.sql
3. 04_create_indexes.sql
4. 05_create_functions.sql
5. 06_enable_rls.sql
6. 07_seed_data.sql
7. 08_verify_install.sql
```

### 3️⃣ VERIFICAR
```sql
SELECT * FROM tenants;
-- Deve mostrar 6 tenants
```

---

## 📋 CHECKLIST

### Antes de Começar
- [ ] Acessar https://supabase.com/dashboard
- [ ] Selecionar projeto
- [ ] Ir em SQL Editor

### Durante Instalação
- [ ] Executar 01_check_extensions.sql ✅
- [ ] Executar 03_create_tables.sql ✅
- [ ] Executar 04_create_indexes.sql ✅
- [ ] Executar 05_create_functions.sql ✅
- [ ] Executar 06_enable_rls.sql ✅
- [ ] Executar 07_seed_data.sql ✅
- [ ] Executar 08_verify_install.sql ✅

### Após Instalação
- [ ] Verificar 8 tabelas criadas
- [ ] Verificar 6 tenants cadastrados
- [ ] Verificar extensão vector instalada
- [ ] Configurar .env (SUPABASE_URL, SUPABASE_KEY)
- [ ] Testar Python (`python -m mkt.engine.main`)

---

## 🎯 ORDEM COMPLETA (8 SCRIPTS)

| # | Script | O que faz | Obrigatório? |
| :- | :----- | :-------- | :----------- |
| 1 | `01_check_extensions.sql` | Cria vector, uuid-ossp | ✅ Sim |
| 2 | `02_drop_existing.sql` | Remove tabelas antigas | ⚠️ Opcional |
| 3 | `03_create_tables.sql` | Cria 8 tabelas | ✅ Sim |
| 4 | `04_create_indexes.sql` | Cria índices | ✅ Sim |
| 5 | `05_create_functions.sql` | Cria funções | ✅ Sim |
| 6 | `06_enable_rls.sql` | Habilita RLS | ✅ Sim |
| 7 | `07_seed_data.sql` | Insere dados | ✅ Sim |
| 8 | `08_verify_install.sql` | Verifica tudo | ✅ Sim |

---

## 🔍 VERIFICAÇÃO RÁPIDA

Após instalar, execute no SQL Editor:

```sql
-- 1. Verificar tabelas (deve mostrar 8)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_name IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );

-- 2. Verificar tenants (deve mostrar 6)
SELECT * FROM tenants;

-- 3. Verificar extensão vector
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## ⚠️ PROBLEMAS COMUNS

### "relation already exists"
```sql
-- Solução: Executar 02_drop_existing.sql primeiro
-- OU usar IF NOT EXISTS (já incluso nos scripts)
```

### "extension vector does not exist"
```sql
-- Solução:
CREATE EXTENSION IF NOT EXISTS vector;

-- Ou ativar no dashboard:
-- Database → Extensions → Enable "pgvector"
```

### "column is_active does not exist"
```sql
-- Solução: Adicionar coluna
ALTER TABLE public.tenants 
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
```

---

## 📞 PRÓXIMOS PASSOS

Após instalação concluída:

1. **Configurar .env**:
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua-chave
   ```

2. **Testar Python**:
   ```bash
   .venv_mkt\Scripts\activate
   python -m mkt.engine.main
   ```

3. **Verificar Obsidian**:
   ```
   🧠 EXOCÓRTEX/00 - Dashboards/
   └── 🌍 CMO-Dashboard-*.md
   ```

---

<div align="center">

**🗄️ INSTALAÇÃO DO BANCO**

*8 scripts • 8 tabelas • 5-10 minutos*

**Comece por: sql/01_check_extensions.sql**

</div>
