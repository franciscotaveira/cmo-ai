-- ═══════════════════════════════════════════════════════════════════════════════
-- 04_create_indexes.sql — ÍNDICES DE PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════
-- Cria índices adicionais para otimizar consultas
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- TENANTS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_tenants_active ON public.tenants(is_active);
CREATE INDEX IF NOT EXISTS idx_tenants_created ON public.tenants(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- MARKETING ASSETS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_assets_tenant_type ON public.marketing_assets(tenant_id, file_type);
CREATE INDEX IF NOT EXISTS idx_assets_ingested ON public.marketing_assets(ingested_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- BUSINESS METRICS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_metrics_tenant_key ON public.business_metrics(tenant_id, metric_key);
CREATE INDEX IF NOT EXISTS idx_metrics_tenant_key_date ON public.business_metrics(tenant_id, metric_key, date_ref DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_period ON public.business_metrics(period_type);

-- ═══════════════════════════════════════════════════════════════════════════════
-- KNOWLEDGE BASE
-- ═══════════════════════════════════════════════════════════════════════════════

-- Índice para busca semântica (vetores)
CREATE INDEX IF NOT EXISTS idx_knowledge_embedding
ON public.knowledge_base USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_knowledge_tenant_asset ON public.knowledge_base(tenant_id, asset_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- STRATEGIC INSIGHTS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_insights_tenant_status ON public.strategic_insights(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_insights_rating ON public.strategic_insights(user_rating DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- ANOMALY ALERTS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_anomaly_tenant_status ON public.anomaly_alerts(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_anomaly_metric ON public.anomaly_alerts(metric_key);
CREATE INDEX IF NOT EXISTS idx_anomaly_zscore ON public.anomaly_alerts(z_score DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- AUDIT LOGS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_audit_tenant_action ON public.audit_logs(tenant_id, action);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON public.audit_logs(actor_type, actor_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- AUTOMATION QUEUE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_automation_tenant_status ON public.automation_queue(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_automation_scheduled ON public.automation_queue(scheduled_for DESC);
CREATE INDEX IF NOT EXISTS idx_automation_trigger ON public.automation_queue(trigger_source);

-- ═══════════════════════════════════════════════════════════════════════════════
-- CONFIRMAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '✅ Índices criados com sucesso!' AS status;

SELECT 
    '📑 ÍNDICES CRIADOS' AS relatorio,
    COUNT(*) as total_indices
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );
