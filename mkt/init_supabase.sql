-- ═══════════════════════════════════════════════════════════════════════════════
-- MARKETING DIRECTOR OS v4.0 — SUPABASE SCHEMA COMPLETO
-- ═══════════════════════════════════════════════════════════════════════════════
-- PROJETO: Marketing Neural Hub para TDAH
-- VERSÃO: 4.0.0
-- FILOSOFIA: Back-end First • Tenant Isolation • Truth in Data • Multi-Business
-- ═══════════════════════════════════════════════════════════════════════════════
-- 
-- INSTRUÇÕES:
-- 1. Acesse: https://supabase.com/dashboard
-- 2. Selecione seu projeto
-- 3. Vá em: SQL Editor
-- 4. Copie TODO este script
-- 5. Clique em: RUN (ou Ctrl+Enter)
-- 6. Verifique se todas as tabelas foram criadas
--
-- TEMPO ESTIMADO: 2-5 minutos
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. EXTENSÕES NECESSÁRIAS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Vetores para busca semântica (IA/RAG)
CREATE EXTENSION IF NOT EXISTS vector;

-- Geração de UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Funções adicionais de timestamp
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABELA DE TENANTS (EMPRESAS/UNIDADES DE NEGÓCIO)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('diretoria', 'franquia', 'local_business', 'salao')),
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
CREATE INDEX IF NOT EXISTS idx_tenants_active ON public.tenants(is_active);

COMMENT ON TABLE public.tenants IS 'Empresas/unidades de negócio isoladas no sistema';
COMMENT ON COLUMN public.tenants.slug IS 'Identificador único para mapear pastas do Drive e Obsidian';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. SEED INICIAL (DADOS DE TESTE)
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO public.tenants (name, slug, type, settings, business_config) VALUES
    ('Diretoria Geral', 'diretoria', 'diretoria', 
     '{"kpi_ouro": ["ltv", "cac", "roi", "retention", "gap"]}'::jsonb,
     '{"unidades": 60, "leads_total": 200000}'::jsonb),
    ('Salão Lux Beauty', 'salao-esposa', 'salao',
     '{"tom_voz": "acolhedor", "objetivo": "fidelizacao"}'::jsonb,
     '{"funcionarios": 5}'::jsonb),
    ('Franquia Chapecó Centro', 'franquia-chapeco-centro', 'franquia',
     '{"unidade_id": "001", "regiao": "centro"}'::jsonb,
     '{"funcionarios": 10}'::jsonb),
    ('Franquia Chapecó Oeste', 'franquia-chapeco-oeste', 'franquia',
     '{"unidade_id": "002", "regiao": "oeste"}'::jsonb,
     '{"funcionarios": 8}'::jsonb)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    type = EXCLUDED.type,
    settings = EXCLUDED.settings,
    updated_at = NOW();

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. MARKETING ASSETS (ARQUIVOS PROCESSADOS)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.marketing_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT CHECK (file_type IN ('csv', 'pdf', 'xlsx', 'xls', 'txt', 'json')) NOT NULL,
    file_size_bytes BIGINT DEFAULT 0,
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
-- 5. BUSINESS METRICS (KPIs)
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
-- 6. KNOWLEDGE BASE (RAG PARA IA)
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

CREATE INDEX IF NOT EXISTS idx_knowledge_embedding 
ON public.knowledge_base USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_knowledge_tenant ON public.knowledge_base(tenant_id);

COMMENT ON TABLE public.knowledge_base IS 'Base de conhecimento para RAG - chunks com embeddings';

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. STRATEGIC INSIGHTS (SAÍDAS DA IA)
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
-- 8. ANOMALY ALERTS (ALERTAS DE ANOMALIAS)
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
-- 9. AUDIT LOGS (AUDITORIA)
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
-- 10. AUTOMATION QUEUE (FILAS DE AÇÃO - HitL)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.automation_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE NOT NULL,
    automation_type TEXT NOT NULL CHECK (
        automation_type IN (
            'whatsapp_message', 'whatsapp_campaign',
            'meta_ads_create', 'meta_ads_optimize', 'meta_ads_pause',
            'google_ads_create', 'google_ads_optimize',
            'email_campaign', 'sms_campaign',
            'obsidian_report', 'slack_notification'
        )
    ),
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
-- 11. SEGURANÇA (ROW LEVEL SECURITY - RLS)
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE public.tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.marketing_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.business_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.strategic_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.anomaly_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.automation_queue ENABLE ROW LEVEL SECURITY;

-- Políticas de isolamento por tenant
CREATE POLICY "tenant_isolation" ON public.tenants FOR ALL
    USING (
        current_setting('app.current_tenant', TRUE) = slug
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.marketing_assets FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.business_metrics FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.knowledge_base FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.strategic_insights FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.anomaly_alerts FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.audit_logs FOR SELECT
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

CREATE POLICY "tenant_isolation" ON public.automation_queue FOR ALL
    USING (
        tenant_id IN (SELECT id FROM public.tenants WHERE slug = current_setting('app.current_tenant', TRUE))
        OR current_setting('app.is_superuser', TRUE) = 'true'
        OR auth.jwt() IS NULL
    );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 12. FUNÇÕES UTILITÁRIAS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Função para definir tenant atual
CREATE OR REPLACE FUNCTION public.set_current_tenant(tenant_slug TEXT)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant', tenant_slug, FALSE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para busca semântica (RAG)
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

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON public.tenants
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_business_metrics_updated_at
    BEFORE UPDATE ON public.business_metrics
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════════
-- 13. GRANTS DE PERMISSÃO
-- ═══════════════════════════════════════════════════════════════════════════════

GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

GRANT SELECT, INSERT, UPDATE ON public.tenants TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.marketing_assets TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.business_metrics TO authenticated;
GRANT SELECT, INSERT ON public.knowledge_base TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.strategic_insights TO authenticated;
GRANT SELECT ON public.anomaly_alerts TO authenticated;
GRANT SELECT ON public.audit_logs TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.automation_queue TO authenticated;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIM DO SCHEMA
-- ═══════════════════════════════════════════════════════════════════════════════

-- VERIFICAÇÃO:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
-- SELECT * FROM public.tenants;
