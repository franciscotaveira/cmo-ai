-- ═══════════════════════════════════════════════════════════════════════════════
-- 03_create_tables.sql — CRIAÇÃO DAS 8 TABELAS PRINCIPAIS
-- ═══════════════════════════════════════════════════════════════════════════════
-- CMO 360° v5.3 — Schema completo
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TENANTS (Empresas/Unidades de Negócio)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('diretoria', 'franquia', 'local_business', 'salao', 'ecommerce', 'saas', 'servicos')),
    settings JSONB DEFAULT '{}'::jsonb,
    business_config JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT tenants_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
    CONSTRAINT tenants_slug_not_empty CHECK (LENGTH(TRIM(slug)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_tenants_slug ON public.tenants(slug);
CREATE INDEX IF NOT EXISTS idx_tenants_type ON public.tenants(type);

COMMENT ON TABLE public.tenants IS 'Empresas/unidades de negócio isoladas no sistema';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. MARKETING ASSETS (Arquivos Processados)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.marketing_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT CHECK (file_type IN ('csv', 'pdf', 'xlsx', 'xls', 'txt', 'json')) NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processing_status TEXT DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'error')),
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT file_name_not_empty CHECK (LENGTH(TRIM(file_name)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_assets_tenant ON public.marketing_assets(tenant_id);
CREATE INDEX IF NOT EXISTS idx_assets_processed ON public.marketing_assets(processed);
CREATE INDEX IF NOT EXISTS idx_assets_status ON public.marketing_assets(processing_status);

COMMENT ON TABLE public.marketing_assets IS 'Arquivos (CSV, PDF, XLSX) ingeridos e processados';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. BUSINESS METRICS (KPIs)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.business_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    asset_id UUID REFERENCES public.marketing_assets(id) ON DELETE SET NULL,
    metric_key TEXT NOT NULL,
    metric_value NUMERIC NOT NULL,
    metric_unit TEXT DEFAULT 'unit',
    date_ref DATE NOT NULL DEFAULT CURRENT_DATE,
    period_type TEXT DEFAULT 'daily' CHECK (period_type IN ('daily', 'weekly', 'monthly', 'yearly')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT metric_key_not_empty CHECK (LENGTH(TRIM(metric_key)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_metrics_tenant ON public.business_metrics(tenant_id);
CREATE INDEX IF NOT EXISTS idx_metrics_date ON public.business_metrics(date_ref DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_key ON public.business_metrics(metric_key);
CREATE INDEX IF NOT EXISTS idx_metrics_tenant_date ON public.business_metrics(tenant_id, date_ref DESC);

COMMENT ON TABLE public.business_metrics IS 'KPIs quantitativos (leads, faturamento, CAC, ROI)';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. KNOWLEDGE BASE (RAG para IA)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    asset_id UUID REFERENCES public.marketing_assets(id) ON DELETE SET NULL,
    content_chunk TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT content_not_empty CHECK (LENGTH(TRIM(content_chunk)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_knowledge_tenant ON public.knowledge_base(tenant_id);

COMMENT ON TABLE public.knowledge_base IS 'Base de conhecimento para RAG - chunks com embeddings';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. STRATEGIC INSIGHTS (Saídas da IA)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.strategic_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    context TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    source_model TEXT,
    confidence_score NUMERIC(3,2),
    status TEXT DEFAULT 'new' CHECK (status IN ('new', 'reviewing', 'applied', 'archived', 'rejected')),
    user_feedback TEXT,
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    applied_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT context_not_empty CHECK (LENGTH(TRIM(context)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_insights_tenant ON public.strategic_insights(tenant_id);
CREATE INDEX IF NOT EXISTS idx_insights_status ON public.strategic_insights(status);
CREATE INDEX IF NOT EXISTS idx_insights_created ON public.strategic_insights(created_at DESC);

COMMENT ON TABLE public.strategic_insights IS 'Estratégias e recomendações geradas pela IA';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. ANOMALY ALERTS (Alertas de Anomalias)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.anomaly_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    metric_key TEXT NOT NULL,
    metric_value NUMERIC NOT NULL,
    expected_value NUMERIC,
    z_score NUMERIC,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    threshold NUMERIC DEFAULT 2.0,
    is_anomaly BOOLEAN GENERATED ALWAYS AS (ABS(z_score) > threshold) STORED,
    status TEXT DEFAULT 'new' CHECK (status IN ('new', 'acknowledged', 'resolved', 'dismissed')),
    action_taken BOOLEAN DEFAULT FALSE,
    action_details JSONB DEFAULT '{}',
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT metric_key_not_empty CHECK (LENGTH(TRIM(metric_key)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_anomaly_tenant ON public.anomaly_alerts(tenant_id);
CREATE INDEX IF NOT EXISTS idx_anomaly_severity ON public.anomaly_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_anomaly_status ON public.anomaly_alerts(status);
CREATE INDEX IF NOT EXISTS idx_anomaly_detected ON public.anomaly_alerts(detected_at DESC);

COMMENT ON TABLE public.anomaly_alerts IS 'Alertas de anomalias (Z-score, gestão por exceção)';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. AUDIT LOGS (Auditoria)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    actor_type TEXT CHECK (actor_type IN ('user', 'system', 'engine', 'ia')) NOT NULL,
    actor_id TEXT,
    details JSONB DEFAULT '{}'::jsonb,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT action_not_empty CHECK (LENGTH(TRIM(action)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_audit_tenant ON public.audit_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON public.audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_date ON public.audit_logs(created_at DESC);

COMMENT ON TABLE public.audit_logs IS 'Log de auditoria de todas as operações';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. AUTOMATION QUEUE (Fila de Ação - HitL)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.automation_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    automation_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')),
    trigger_source TEXT NOT NULL CHECK (trigger_source IN ('manual', 'anomaly', 'insight', 'scheduled')),
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    payload JSONB NOT NULL,
    result JSONB DEFAULT '{}',
    approved_by UUID,
    approved_at TIMESTAMP WITH TIME ZONE,
    scheduled_for TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    CONSTRAINT automation_type_not_empty CHECK (LENGTH(TRIM(automation_type)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_automation_tenant ON public.automation_queue(tenant_id);
CREATE INDEX IF NOT EXISTS idx_automation_status ON public.automation_queue(status);
CREATE INDEX IF NOT EXISTS idx_automation_priority ON public.automation_queue(priority DESC);

COMMENT ON TABLE public.automation_queue IS 'Fila de automações (Human-in-the-Loop)';

-- ═══════════════════════════════════════════════════════════════════════════════
-- CONFIRMAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '✅ 8 tabelas criadas com sucesso!' AS status;

SELECT 
    '📊 TABELAS CRIADAS' AS relatorio,
    COUNT(*) as total
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'tenants', 'marketing_assets', 'business_metrics',
    'knowledge_base', 'strategic_insights', 'anomaly_alerts',
    'audit_logs', 'automation_queue'
  );
