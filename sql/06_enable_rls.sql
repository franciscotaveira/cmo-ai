-- ═══════════════════════════════════════════════════════════════════════════════
-- 06_enable_rls.sql — ROW LEVEL SECURITY (RLS)
-- ═══════════════════════════════════════════════════════════════════════════════
-- Habilita RLS e cria políticas de isolamento por tenant
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. HABILITAR RLS EM TODAS AS TABELAS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE public.tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.marketing_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.business_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.strategic_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.anomaly_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.automation_queue ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. POLÍTICA DE ISOLAMENTO POR TENANT
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tenants: Permite acesso se o tenant atual for o slug ou se for superuser
CREATE POLICY "tenant_isolation" ON public.tenants FOR ALL
    USING (
        current_setting('app.current_tenant', TRUE) = slug
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Marketing Assets: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.marketing_assets FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Business Metrics: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.business_metrics FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Knowledge Base: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.knowledge_base FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Strategic Insights: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.strategic_insights FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Anomaly Alerts: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.anomaly_alerts FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Audit Logs: Apenas SELECT isolado por tenant_id
CREATE POLICY "tenant_isolation" ON public.audit_logs FOR SELECT
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- Automation Queue: Isola por tenant_id
CREATE POLICY "tenant_isolation" ON public.automation_queue FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. POLÍTICAS ADICIONAIS (STATUS-BASED)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Anomaly Alerts: Permite UPDATE apenas em status (acknowledge, resolve)
CREATE POLICY "anomaly_status_update" ON public.anomaly_alerts FOR UPDATE
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    )
    WITH CHECK (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    );

-- Strategic Insights: Permite UPDATE de status (review, apply, archive)
CREATE POLICY "insight_status_update" ON public.strategic_insights FOR UPDATE
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    )
    WITH CHECK (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    );

-- Automation Queue: Permite UPDATE de status (approve, complete)
CREATE POLICY "automation_status_update" ON public.automation_queue FOR UPDATE
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    )
    WITH CHECK (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
    );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. GRANTS DE PERMISSÃO
-- ═══════════════════════════════════════════════════════════════════════════════

-- Service Role: Acesso total
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- Authenticated: Acesso limitado
GRANT SELECT, INSERT, UPDATE ON public.tenants TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.marketing_assets TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.business_metrics TO authenticated;
GRANT SELECT, INSERT ON public.knowledge_base TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.strategic_insights TO authenticated;
GRANT SELECT, UPDATE ON public.anomaly_alerts TO authenticated;
GRANT SELECT ON public.audit_logs TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.automation_queue TO authenticated;

-- ═══════════════════════════════════════════════════════════════════════════════
-- CONFIRMAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '✅ RLS habilitado e políticas criadas!' AS status;

SELECT 
    '🔒 POLÍTICAS RLS' AS relatorio,
    COUNT(*) as total_politicas
FROM pg_policies
WHERE schemaname = 'public';

SELECT 
    '📋 TABELAS COM RLS' AS relatorio,
    COUNT(*) as total_rls
FROM pg_tables
WHERE schemaname = 'public'
  AND rowsecurity = true;
