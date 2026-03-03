-- MCT Agent Factory — Supabase Migration
-- Execute no SQL Editor do Supabase
-- Data: 2026-02-24

-- 1. Tabela de contatos (CRM)
CREATE TABLE IF NOT EXISTS public.contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone TEXT NOT NULL UNIQUE,
    name TEXT,
    email TEXT,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    first_contact_at TIMESTAMP WITH TIME ZONE,
    last_contact_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_contacts_phone ON public.contacts (phone);
CREATE INDEX IF NOT EXISTS idx_contacts_tags ON public.contacts USING GIN (tags);

-- 2. Tabela de leads
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone TEXT NOT NULL,
    name TEXT,
    source TEXT DEFAULT 'whatsapp',
    interest TEXT,
    temperature TEXT DEFAULT 'warm',
    status TEXT DEFAULT 'new',
    assigned_to TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_leads_status ON public.leads (status);
CREATE INDEX IF NOT EXISTS idx_leads_temperature ON public.leads (temperature);

-- 3. Tabela de agendamentos (fallback local)
CREATE TABLE IF NOT EXISTS public.appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name TEXT NOT NULL,
    client_phone TEXT NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    service_id TEXT NOT NULL,
    professional_id TEXT NOT NULL,
    status TEXT DEFAULT 'pending_confirmation',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON public.appointments (date, professional_id);
CREATE INDEX IF NOT EXISTS idx_appointments_client ON public.appointments (client_phone);

-- 4. Tabela de cobranças
CREATE TABLE IF NOT EXISTS public.invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_phone TEXT NOT NULL,
    client_name TEXT,
    items JSONB NOT NULL DEFAULT '[]',
    total DECIMAL(10,2) NOT NULL,
    due_date DATE,
    status TEXT DEFAULT 'pending',
    paid_at TIMESTAMP WITH TIME ZONE,
    payment_method TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON public.invoices (status);
CREATE INDEX IF NOT EXISTS idx_invoices_client ON public.invoices (client_phone);

-- 5. Tabela de notificações agendadas
CREATE TABLE IF NOT EXISTS public.scheduled_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'reminder',
    scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notifications_scheduled ON public.scheduled_notifications (scheduled_for, status);

-- 6. Tabela de conversas (já deve existir, mas criando se não existir)
CREATE TABLE IF NOT EXISTS public.conversation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_name TEXT NOT NULL,
    remote_jid TEXT NOT NULL,
    push_name TEXT,
    message_text TEXT,
    message_type TEXT DEFAULT 'text',
    from_me BOOLEAN DEFAULT false,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    intent_detected TEXT,
    campaign_id UUID,
    sentiment_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_logs_instance ON public.conversation_logs (instance_name, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_jid ON public.conversation_logs (remote_jid);

-- 7. Tabela de campanhas de marketing
CREATE TABLE IF NOT EXISTS public.marketing_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id TEXT NOT NULL DEFAULT 'haven-default',
    name TEXT NOT NULL,
    description TEXT,
    keywords TEXT[] NOT NULL DEFAULT '{}',
    prompt_override TEXT,
    is_active BOOLEAN DEFAULT true,
    start_date TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_campaigns_client_active ON public.marketing_campaigns (client_id, is_active);

-- 8. Tabela de configurações de agentes
CREATE TABLE IF NOT EXISTS public.agent_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id TEXT NOT NULL DEFAULT 'haven-default',
    agent_name TEXT NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'receptionist',
    personality TEXT DEFAULT 'professional',
    system_prompt TEXT,
    voice_enabled BOOLEAN DEFAULT false,
    sandbox_mode BOOLEAN DEFAULT true,
    model_routing JSONB DEFAULT '{"default": "haiku", "complex": "sonnet"}',
    tools_enabled TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(client_id, agent_name)
);

-- 9. Tabela de instâncias de clientes
CREATE TABLE IF NOT EXISTS public.client_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id TEXT NOT NULL DEFAULT 'haven-default',
    instance_name TEXT NOT NULL UNIQUE,
    instance_type TEXT NOT NULL DEFAULT 'whatsapp',
    display_name TEXT,
    logo_url TEXT,
    phone_number TEXT,
    status TEXT DEFAULT 'active',
    configuration JSONB DEFAULT '{}',
    last_sync_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_instances_client ON public.client_instances (client_id);

-- 10. Tabela de personas de agentes
CREATE TABLE IF NOT EXISTS public.agent_personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,
    name TEXT NOT NULL,
    tone TEXT DEFAULT 'professional',
    traits TEXT[] DEFAULT '{}',
    forbidden_words TEXT[] DEFAULT '{}',
    system_prompt TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_personas_agent ON public.agent_personas (agent_id);

-- Insert seed data
INSERT INTO public.marketing_campaigns (client_id, name, description, keywords, is_active)
VALUES (
    'haven-default',
    'Campanha Padrao - Haven',
    'Campanha padrao para atendimento e agendamentos',
    ARRAY['agendar', 'horario', 'unha', 'cabelo', 'beleza', 'preco', 'desconto', 'ola', 'oi', 'bom dia', 'boa tarde']::TEXT[],
    true
) ON CONFLICT DO NOTHING;

INSERT INTO public.client_instances (client_id, instance_name, instance_type, display_name, phone_number, status)
VALUES (
    'haven-default',
    'haven',
    'whatsapp',
    'Haven - Esmalteria & Escovaria',
    '554988370054',
    'active'
) ON CONFLICT (instance_name) DO UPDATE SET status = 'active', updated_at = now();

-- Row Level Security (RLS)
ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scheduled_notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.marketing_campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.client_instances ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_personas ENABLE ROW LEVEL SECURITY;

-- Policies (Service Role tem acesso total)
CREATE POLICY "Service Role Full Access" ON public.contacts FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.leads FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.appointments FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.invoices FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.scheduled_notifications FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.conversation_logs FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.marketing_campaigns FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.agent_configurations FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.client_instances FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
CREATE POLICY "Service Role Full Access" ON public.agent_personas FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Anon pode ler dados públicos
CREATE POLICY "Anon Read Campaigns" ON public.marketing_campaigns FOR SELECT USING (is_active = true);
CREATE POLICY "Anon Read Instances" ON public.client_instances FOR SELECT USING (status = 'active');
CREATE POLICY "Anon Read Agent Configs" ON public.agent_configurations FOR SELECT USING (sandbox_mode = false);

-- Função para registrar conversa
CREATE OR REPLACE FUNCTION public.log_conversation(
    p_instance_name TEXT,
    p_remote_jid TEXT,
    p_push_name TEXT,
    p_message_text TEXT,
    p_from_me BOOLEAN DEFAULT false,
    p_intent_detected TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_log_id UUID;
BEGIN
    INSERT INTO public.conversation_logs (
        instance_name, remote_jid, push_name, message_text, from_me, intent_detected
    ) VALUES (
        p_instance_name, p_remote_jid, p_push_name, p_message_text, p_from_me, p_intent_detected
    ) RETURNING id INTO v_log_id;
    
    RETURN v_log_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant para Service Role
GRANT EXECUTE ON FUNCTION public.log_conversation TO service_role;

-- Done!
SELECT '✅ MCT Agent Factory migration completed!' AS status;
