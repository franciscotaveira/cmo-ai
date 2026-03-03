-- ═══════════════════════════════════════════════════════════════════════════════
-- 05_create_functions.sql — FUNÇÕES UTILITÁRIAS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Cria funções para RAG, triggers e utilitários
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. SET CURRENT TENANT (RLS)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.set_current_tenant(tenant_slug TEXT)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant', tenant_slug, FALSE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION public.set_current_tenant IS 'Define o tenant atual para Row Level Security';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. MATCH KNOWLEDGE CHUNKS (RAG - Busca Semântica)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.match_knowledge_chunks(
    query_embedding VECTOR(1536),
    match_tenant_id UUID,
    match_threshold NUMERIC DEFAULT 0.7,
    match_count INTEGER DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    content_chunk TEXT,
    metadata JSONB,
    similarity NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT k.id, k.content_chunk, k.metadata, 1 - (k.embedding <=> query_embedding)
    FROM public.knowledge_base k
    WHERE k.tenant_id = match_tenant_id
      AND 1 - (k.embedding <=> query_embedding) > match_threshold
    ORDER BY k.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

COMMENT ON FUNCTION public.match_knowledge_chunks IS 'Busca semântica na knowledge base (RAG)';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. UPDATE UPDATED_AT (Trigger)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION public.update_updated_at_column IS 'Atualiza automaticamente o campo updated_at';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. GET TENANT METRICS (Resumo de Métricas)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.get_tenant_metrics_summary(
    p_tenant_id UUID,
    p_days INTEGER DEFAULT 30
)
RETURNS TABLE (
    metric_key TEXT,
    metric_value NUMERIC,
    metric_unit TEXT,
    date_ref DATE,
    avg_value NUMERIC,
    min_value NUMERIC,
    max_value NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        bm.metric_key,
        bm.metric_value,
        bm.metric_unit,
        bm.date_ref,
        AVG(bm.metric_value) OVER (PARTITION BY bm.metric_key) as avg_value,
        MIN(bm.metric_value) OVER (PARTITION BY bm.metric_key) as min_value,
        MAX(bm.metric_value) OVER (PARTITION BY bm.metric_key) as max_value
    FROM public.business_metrics bm
    WHERE bm.tenant_id = p_tenant_id
      AND bm.date_ref >= CURRENT_DATE - p_days
    ORDER BY bm.date_ref DESC, bm.metric_key;
END;
$$;

COMMENT ON FUNCTION public.get_tenant_metrics_summary IS 'Retorna resumo de métricas do tenant';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. GET TENANT DASHBOARD (Dashboard Completo)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.get_tenant_dashboard(
    p_tenant_id UUID
)
RETURNS TABLE (
    total_assets BIGINT,
    total_metrics BIGINT,
    total_insights BIGINT,
    active_alerts BIGINT,
    critical_alerts BIGINT,
    pending_automations BIGINT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM public.marketing_assets WHERE tenant_id = p_tenant_id) as total_assets,
        (SELECT COUNT(*) FROM public.business_metrics WHERE tenant_id = p_tenant_id) as total_metrics,
        (SELECT COUNT(*) FROM public.strategic_insights WHERE tenant_id = p_tenant_id AND status = 'new') as total_insights,
        (SELECT COUNT(*) FROM public.anomaly_alerts WHERE tenant_id = p_tenant_id AND status = 'new') as active_alerts,
        (SELECT COUNT(*) FROM public.anomaly_alerts WHERE tenant_id = p_tenant_id AND severity = 'critical' AND status = 'new') as critical_alerts,
        (SELECT COUNT(*) FROM public.automation_queue WHERE tenant_id = p_tenant_id AND status = 'pending') as pending_automations;
END;
$$;

COMMENT ON FUNCTION public.get_tenant_dashboard IS 'Retorna dashboard completo do tenant';

-- ═══════════════════════════════════════════════════════════════════════════════
-- APLICAR TRIGGERS DE UPDATED_AT
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON public.tenants
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_business_metrics_updated_at
    BEFORE UPDATE ON public.business_metrics
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_marketing_assets_updated_at
    BEFORE UPDATE ON public.marketing_assets
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════════
-- CONFIRMAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '✅ Funções criadas com sucesso!' AS status;

SELECT 
    '🔧 FUNÇÕES CRIADAS' AS relatorio,
    COUNT(*) as total_funcoes,
    STRING_AGG(routine_name, ', ') as funcoes
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_type = 'FUNCTION';
