-- ═══════════════════════════════════════════════════════════════════════════════
-- 02_drop_existing.sql — LIMPEZA (OPCIONAL)
-- ═══════════════════════════════════════════════════════════════════════════════
-- ⚠️ ATENÇÃO: Este script remove tabelas existentes!
-- Use apenas se quiser começar do zero.
-- ═══════════════════════════════════════════════════════════════════════════════

-- Drop policies (se existirem)
DROP POLICY IF EXISTS "tenant_isolation" ON public.tenants;
DROP POLICY IF EXISTS "tenant_isolation" ON public.marketing_assets;
DROP POLICY IF EXISTS "tenant_isolation" ON public.business_metrics;
DROP POLICY IF EXISTS "tenant_isolation" ON public.knowledge_base;
DROP POLICY IF EXISTS "tenant_isolation" ON public.strategic_insights;
DROP POLICY IF EXISTS "tenant_isolation" ON public.anomaly_alerts;
DROP POLICY IF EXISTS "tenant_isolation" ON public.audit_logs;
DROP POLICY IF EXISTS "tenant_isolation" ON public.automation_queue;

-- Drop functions
DROP FUNCTION IF EXISTS public.set_current_tenant(TEXT) CASCADE;
DROP FUNCTION IF EXISTS public.match_knowledge_chunks(VECTOR, UUID, NUMERIC, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS public.update_updated_at_column() CASCADE;

-- Drop tables (ORDEM IMPORTANTE: dependências primeiro)
DROP TABLE IF EXISTS public.automation_queue CASCADE;
DROP TABLE IF EXISTS public.audit_logs CASCADE;
DROP TABLE IF EXISTS public.anomaly_alerts CASCADE;
DROP TABLE IF EXISTS public.strategic_insights CASCADE;
DROP TABLE IF EXISTS public.knowledge_base CASCADE;
DROP TABLE IF EXISTS public.business_metrics CASCADE;
DROP TABLE IF EXISTS public.marketing_assets CASCADE;
DROP TABLE IF EXISTS public.tenants CASCADE;

SELECT '✅ Tabelas antigas removidas (se existiam)' AS status;
