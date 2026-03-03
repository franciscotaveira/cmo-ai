-- ═══════════════════════════════════════════════════════════════════════════════
-- VERIFICAÇÃO DE SCHEMA — CMO 360° (v5.3)
-- ═══════════════════════════════════════════════════════════════════════════════
-- Execute este script no SQL Editor do Supabase para verificar se todas as
-- tabelas necessárias estão criadas
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. VERIFICAR TABELAS EXISTENTES
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📊 TABELAS EXISTENTES' AS relatorio,
    COUNT(*) as total_tabelas
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABELAS ESPERADAS (CMO 360° v5.3)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tabela: tenants (empresas/unidades)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tenants')
        THEN '✅ tenants'
        ELSE '❌ tenants — FALTA CRIAR'
    END AS status_tenants;

-- Tabela: marketing_assets (arquivos processados)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'marketing_assets')
        THEN '✅ marketing_assets'
        ELSE '❌ marketing_assets — FALTA CRIAR'
    END AS status_assets;

-- Tabela: business_metrics (KPIs)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'business_metrics')
        THEN '✅ business_metrics'
        ELSE '❌ business_metrics — FALTA CRIAR'
    END AS status_metrics;

-- Tabela: knowledge_base (RAG)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_base')
        THEN '✅ knowledge_base'
        ELSE '❌ knowledge_base — FALTA CRIAR'
    END AS status_knowledge;

-- Tabela: strategic_insights (IA)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'strategic_insights')
        THEN '✅ strategic_insights'
        ELSE '❌ strategic_insights — FALTA CRIAR'
    END AS status_insights;

-- Tabela: anomaly_alerts (alertas)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'anomaly_alerts')
        THEN '✅ anomaly_alerts'
        ELSE '❌ anomaly_alerts — FALTA CRIAR'
    END AS status_anomaly;

-- Tabela: audit_logs (auditoria)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'audit_logs')
        THEN '✅ audit_logs'
        ELSE '❌ audit_logs — FALTA CRIAR'
    END AS status_audit;

-- Tabela: automation_queue (fila de automação)
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'automation_queue')
        THEN '✅ automation_queue'
        ELSE '❌ automation_queue — FALTA CRIAR'
    END AS status_automation;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. VERIFICAR COLUNAS DAS TABELAS PRINCIPAIS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Colunas da tabela tenants
SELECT 
    '📋 COLUNAS: tenants' AS tabela,
    STRING_AGG(column_name, ', ' ORDER BY ordinal_position) AS colunas
FROM information_schema.columns
WHERE table_name = 'tenants';

-- Colunas da tabela marketing_assets
SELECT 
    '📋 COLUNAS: marketing_assets' AS tabela,
    STRING_AGG(column_name, ', ' ORDER BY ordinal_position) AS colunas
FROM information_schema.columns
WHERE table_name = 'marketing_assets';

-- Colunas da tabela business_metrics
SELECT 
    '📋 COLUNAS: business_metrics' AS tabela,
    STRING_AGG(column_name, ', ' ORDER BY ordinal_position) AS colunas
FROM information_schema.columns
WHERE table_name = 'business_metrics';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. VERIFICAR DADOS EXISTENTES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Quantos tenants existem?
SELECT 
    '🏢 TENANTS CADASTRADOS' AS relatorio,
    COUNT(*) as total
FROM tenants;

-- Listar tenants
SELECT 
    id,
    name,
    slug,
    type,
    is_active,
    created_at
FROM tenants
ORDER BY created_at DESC;

-- Quantos assets processados?
SELECT 
    '📁 ASSETS PROCESSADOS' AS relatorio,
    COUNT(*) as total_processados,
    COUNT(*) FILTER (WHERE processed = true) as processados_sucesso,
    COUNT(*) FILTER (WHERE processed = false) as pendentes
FROM marketing_assets;

-- Quantas métricas existem?
SELECT 
    '📊 MÉTRICAS NO BANCO' AS relatorio,
    COUNT(*) as total_metricas,
    COUNT(DISTINCT tenant_id) as tenants_com_metricas,
    COUNT(DISTINCT metric_key) as tipos_metricas
FROM business_metrics;

-- Métricas por tenant (últimos 7 dias)
SELECT 
    t.name AS tenant,
    COUNT(DISTINCT bm.metric_key) AS tipos_metricas,
    COUNT(*) AS total_registros,
    MIN(bm.date_ref) AS primeira_data,
    MAX(bm.date_ref) AS ultima_data
FROM business_metrics bm
LEFT JOIN tenants t ON bm.tenant_id = t.id
WHERE bm.date_ref >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY t.name
ORDER BY total_registros DESC;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. VERIFICAR EXTENSÕES
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '🔧 EXTENSÕES INSTALADAS' AS relatorio,
    STRING_AGG(extname, ', ') AS extensoes
FROM pg_extension
WHERE extname IN ('vector', 'uuid-ossp', 'pgcrypto');

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. VERIFICAR ÍNDICES
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '📑 ÍNDICES EXISTENTES' AS relatorio,
    COUNT(*) as total_indices
FROM pg_indexes
WHERE schemaname = 'public';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. RESUMO FINAL
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 
    '✅ RESUMO DO SCHEMA' AS relatorio,
    (SELECT COUNT(*) FROM tenants) AS tenants,
    (SELECT COUNT(*) FROM marketing_assets) AS assets,
    (SELECT COUNT(*) FROM business_metrics) AS metricas,
    (SELECT COUNT(*) FROM knowledge_base) AS knowledge_chunks,
    (SELECT COUNT(*) FROM strategic_insights) AS insights,
    (SELECT COUNT(*) FROM anomaly_alerts) AS alertas,
    (SELECT COUNT(*) FROM audit_logs) AS audit_logs,
    (SELECT COUNT(*) FROM automation_queue) AS automacoes_fila;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIM DA VERIFICAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════
