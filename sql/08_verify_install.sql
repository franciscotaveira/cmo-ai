-- ═══════════════════════════════════════════════════════════════════════════════
-- 08_verify_install.sql — VERIFICAÇÃO FINAL DA INSTALAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════
-- Execute este script para confirmar que tudo foi criado corretamente
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TABELAS CRIADAS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📊 TABELAS CRIADAS' AS secao,
    COUNT(*) as total,
    STRING_AGG(table_name, ', ') as tabelas
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );

-- Verificação individual
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenants') THEN '✅ tenants'
        ELSE '❌ tenants — FALTA'
    END AS tenants;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'marketing_assets') THEN '✅ marketing_assets'
        ELSE '❌ marketing_assets — FALTA'
    END AS marketing_assets;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'business_metrics') THEN '✅ business_metrics'
        ELSE '❌ business_metrics — FALTA'
    END AS business_metrics;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_base') THEN '✅ knowledge_base'
        ELSE '❌ knowledge_base — FALTA'
    END AS knowledge_base;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'strategic_insights') THEN '✅ strategic_insights'
        ELSE '❌ strategic_insights — FALTA'
    END AS strategic_insights;

SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'anomaly_alerts') THEN '✅ anomaly_alerts'
        ELSE '❌ anomaly_alerts — FALTA (execute 03_create_tables.sql)'
    END AS anomaly_alerts;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'audit_logs') THEN '✅ audit_logs'
        ELSE '❌ audit_logs — FALTA'
    END AS audit_logs;

SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'automation_queue') THEN '✅ automation_queue'
        ELSE '❌ automation_queue — FALTA'
    END AS automation_queue;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. EXTENSÕES INSTALADAS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '🔧 EXTENSÕES' AS secao,
    COUNT(*) as total,
    STRING_AGG(extname, ', ') as extensoes
FROM pg_extension
WHERE extname IN ('vector', 'uuid-ossp', 'pgcrypto');

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. FUNÇÕES CRIADAS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '🔧 FUNÇÕES CRIADAS' AS secao,
    COUNT(*) as total,
    STRING_AGG(routine_name, ', ') as funcoes
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_type = 'FUNCTION'
  AND routine_name IN (
    'set_current_tenant', 'match_knowledge_chunks',
    'update_updated_at_column', 'get_tenant_metrics_summary',
    'get_tenant_dashboard'
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. RLS HABILITADO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '🔒 RLS HABILITADO' AS secao,
    COUNT(*) as total,
    STRING_AGG(tablename, ', ') as tabelas
FROM pg_tables
WHERE schemaname = 'public'
  AND rowsecurity = true
  AND tablename IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. POLÍTICAS CRIADAS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📜 POLÍTICAS RLS' AS secao,
    COUNT(*) as total
FROM pg_policies
WHERE schemaname = 'public';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. DADOS INSERIDOS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📊 DADOS CADASTRADOS' AS secao,
    (SELECT COUNT(*) FROM tenants) as tenants,
    (SELECT COUNT(*) FROM business_metrics) as metricas,
    (SELECT COUNT(*) FROM strategic_insights) as insights,
    (SELECT COUNT(*) FROM anomaly_alerts) as alertas,
    (SELECT COUNT(*) FROM automation_queue) as automacoes;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. TENANTS CADASTRADOS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '🏢 TENANTS' AS secao,
    id,
    name,
    slug,
    type,
    is_active,
    created_at
FROM tenants
ORDER BY created_at DESC;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. ÍNDICES CRIADOS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📑 ÍNDICES' AS secao,
    COUNT(*) as total
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9. TRIGGERS CRIADOS
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '⚡ TRIGGERS' AS secao,
    COUNT(*) as total,
    STRING_AGG(trigger_name, ', ') as triggers
FROM information_schema.triggers
WHERE trigger_schema = 'public'
  AND trigger_name LIKE 'update_%_updated_at';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 10. RESUMO FINAL
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '✅ INSTALAÇÃO COMPLETA' AS status,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('tenants', 'marketing_assets', 'business_metrics', 'knowledge_base', 'strategic_insights', 'anomaly_alerts', 'audit_logs', 'automation_queue')) as tabelas,
    (SELECT COUNT(*) FROM pg_extension WHERE extname IN ('vector', 'uuid-ossp', 'pgcrypto')) as extensoes,
    (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public' AND routine_type = 'FUNCTION') as funcoes,
    (SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = true) as tabelas_rls,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public') as politicas,
    (SELECT COUNT(*) FROM tenants) as tenants_cadastrados;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIM DA VERIFICAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '🎉 Instalação concluída com sucesso!' AS mensagem;
SELECT '' AS info;
SELECT 'Próximos passos:' AS info;
SELECT '  1. Configurar .env com SUPABASE_URL e SUPABASE_KEY' AS passo;
SELECT '  2. Rodar python -m mkt.engine.main' AS passo;
SELECT '  3. Verificar dashboards no Obsidian' AS passo;
