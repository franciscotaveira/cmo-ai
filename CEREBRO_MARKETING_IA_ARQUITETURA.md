# 🧠 CÉREBRO DE GESTÃO DE MARKETING COM IA — Arquitetura Unificada

> **Objetivo**: Unificar MD-OS v4.0 + MDCC como **cérebro de IA** para gestão de marketing
> **Foco**: Automações integradas que nascem dos insights
> **Visão**: Sistema que **pensa → decide → age** automaticamente
> **Data**: 2026-02-25

---

## 🎯 VISÃO DO SISTEMA

### O Que Você Realmente Quer

```
┌─────────────────────────────────────────────────────────────────┐
│                    CÉREBRO DE MARKETING                         │
│                                                                 │
│  1. 🧠 PENSAR: Analisar dados de todas as 60 unidades           │
│  2. 💡 DECIDIR: Gerar insights estratégicos com IA              │
│  3. ⚡ AGIR: Disparar automações integradas automaticamente      │
│                                                                 │
│  Exemplo:                                                       │
│  "IA detectou queda de leads → Criou campanha → Disparou no    │
│   WhatsApp → Acompanhou resultados → Otimizou automático"       │
└─────────────────────────────────────────────────────────────────┘
```

### Por Que MD-OS + MDCC Juntos?

| Função | MD-OS v4.0 | MDCC Spec | **Unificado** |
| :----- | :--------- | :-------- | :------------ |
| **Cérebro (IA)** | ✅ RAG + GPT | ⚠️ Z-score | ✅ **IA + Estatística** |
| **Dados** | ⚠️ Simples | ✅ Canônico | ✅ **Modelo híbrido** |
| **Automações** | ❌ Não tem | ⚠️ Alertas | ✅ **Ações automáticas** |
| **Interface** | ✅ Obsidian | ⚠️ Web | ✅ **Obsidian (estratégia)** |

---

## 🏗 ARQUITETURA DO CÉREBRO

### Diagrama Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRADA DE DADOS                             │
│                                                                 │
│  [Drive] CSV/PDF  [APIs] Meta/Google  [Supabase] CRM           │
│         │                │                    │                 │
│         └────────────────┴────────────────────┘                 │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              CAMADA DE DADOS (Supabase)                         │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  MD-OS v4.0 (Base)                                 │        │
│  │  - tenants (RLS)                                   │        │
│  │  - business_metrics (KPIs)                         │        │
│  │  - knowledge_base (RAG)                            │        │
│  │  - strategic_insights (IA)                         │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  MDCC Add-ons (Camadas extras)                     │        │
│  │  - dim_channel, dim_campaign (dimensões)           │        │
│  │  - fact_ad_performance (específico)                │        │
│  │  - anomaly_alerts (Z-score)                        │        │
│  │  - data_contracts (qualidade)                      │        │
│  └────────────────────────────────────────────────────┘        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              CÉREBRO DE IA (Motor de Decisão)                   │
│                                                                 │
│  ┌─────────────────┐          ┌─────────────────┐              │
│  │  IA Generativa  │          │  IA Estatística │              │
│  │  (RAG + GPT)    │          │  (Z-score)      │              │
│  │                 │          │                 │              │
│  │ - Insights      │          │ - Anomalias     │              │
│  │ - Estratégias   │          │ - Alertas       │              │
│  │ - Recomendações │          │ - Tendências    │              │
│  └────────┬────────┘          └────────┬────────┘              │
│           │                            │                       │
│           └────────────┬───────────────┘                       │
│                        │                                       │
│                        ▼                                       │
│              ┌─────────────────┐                               │
│              │  Decision Engine│                               │
│              │  (Orquestrador) │                               │
│              │                 │                               │
│              │ - Classifica    │                               │
│              │ - Prioriza      │                               │
│              │ - Dispara       │                               │
│              └────────┬────────┘                               │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              AUTOMAÇÕES INTEGRADAS (Ações)                      │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  WhatsApp (Evolution API)                          │        │
│  │  - Enviar insights para franqueados                │        │
│  │  - Disparar campanhas de fidelização               │        │
│  │  - Alertas de anomalias em tempo real              │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Meta Ads / Google Ads (APIs)                      │        │
│  │  - Criar campanhas automaticas                     │        │
│  │  - Otimizar orçamentos por performance             │        │
│  │  - Pausar criativos com fadiga                     │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Email Marketing / SMS                             │        │
│  │  - Segmentar base por comportamento                │        │
│  │  - Disparar campanhas de reativação                │        │
│  │  - A/B testing automático                          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Obsidian (Dashboard Estratégico)                  │        │
│  │  - Atualizar mapas mentais                         │        │
│  │  - Gerar relatórios executivos                     │        │
│  │  - Rastrear linhagem de decisões                   │        │
│  └────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧬 COMPONENTES DO CÉREBRO

### 1. Camada de Dados Unificada

**MD-OS v4.0 (Base)** + **MDCC (Add-ons)**

```sql
-- ═══════════════════════════════════════════════════════════════
-- BASE: MD-OS v4.0 (MANTER)
-- ═══════════════════════════════════════════════════════════════

-- Tenants (já existe)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('diretoria', 'franquia', 'local_business')),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Business Metrics (já existe)
CREATE TABLE IF NOT EXISTS business_metrics (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    metric_key TEXT NOT NULL,
    metric_value NUMERIC NOT NULL,
    date_ref DATE DEFAULT CURRENT_DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Knowledge Base (RAG - já existe)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    content_chunk TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Strategic Insights (IA - já existe)
CREATE TABLE IF NOT EXISTS strategic_insights (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    context TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════
-- ADD-ONS: MDCC (NOVAS TABELAS PARA AUTOMAÇÕES)
-- ═══════════════════════════════════════════════════════════════

-- Anomaly Alerts (Z-score)
CREATE TABLE IF NOT EXISTS anomaly_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    metric_key TEXT NOT NULL,
    metric_value NUMERIC NOT NULL,
    z_score NUMERIC NOT NULL,
    threshold NUMERIC DEFAULT 2.0,
    is_anomaly BOOLEAN GENERATED ALWAYS AS (ABS(z_score) > threshold) STORED,
    severity TEXT GENERATED ALWAYS AS (
        CASE 
            WHEN ABS(z_score) > 3.0 THEN 'critical'
            WHEN ABS(z_score) > 2.5 THEN 'high'
            WHEN ABS(z_score) > 2.0 THEN 'medium'
            ELSE 'low'
        END
    ) STORED,
    date_ref DATE NOT NULL,
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    action_taken BOOLEAN DEFAULT FALSE,
    action_details JSONB DEFAULT '{}'
);

-- Automation Queue (Fila de Ações)
CREATE TABLE IF NOT EXISTS automation_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    automation_type TEXT NOT NULL CHECK (
        automation_type IN (
            'whatsapp_message',
            'whatsapp_campaign',
            'meta_ads_create',
            'meta_ads_optimize',
            'google_ads_create',
            'google_ads_optimize',
            'email_campaign',
            'sms_campaign',
            'obsidian_report',
            'slack_notification'
        )
    ),
    status TEXT DEFAULT 'pending' CHECK (
        status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')
    ),
    trigger_source TEXT NOT NULL, -- 'manual', 'anomaly', 'insight', 'scheduled'
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    payload JSONB NOT NULL,
    scheduled_for TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    result JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Automation Templates (Modelos de Automação)
CREATE TABLE IF NOT EXISTS automation_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    name TEXT NOT NULL,
    description TEXT,
    automation_type TEXT NOT NULL,
    trigger_conditions JSONB NOT NULL, -- Quando disparar
    payload_template JSONB NOT NULL, -- O que executar
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Automation Logs (Auditoria de Ações)
CREATE TABLE IF NOT EXISTS automation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    automation_queue_id UUID REFERENCES automation_queue(id),
    step_name TEXT NOT NULL,
    step_status TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Decision History (Histórico de Decisões da IA)
CREATE TABLE IF NOT EXISTS decision_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    insight_id UUID REFERENCES strategic_insights(id),
    anomaly_id UUID REFERENCES anomaly_alerts(id),
    decision_type TEXT NOT NULL,
    decision_reasoning TEXT NOT NULL, -- Por que a IA decidiu isso
    alternatives_considered JSONB DEFAULT '[]',
    expected_impact JSONB DEFAULT '{}',
    actual_impact JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_anomaly_tenant_severity ON anomaly_alerts(tenant_id, severity, detected_at DESC);
CREATE INDEX idx_automation_queue_status ON automation_queue(status, priority DESC, scheduled_for);
CREATE INDEX idx_automation_logs_queue ON automation_logs(automation_queue_id);
CREATE INDEX idx_decision_history_tenant ON decision_history(tenant_id, created_at DESC);
```

---

### 2. Motor de IA (Decision Engine)

**Cérebro que pensa e decide**

```python
# engine/src/decision_engine.py
"""
CÉREBRO DE GESTÃO DE MARKETING

Orquestra IA Generativa + IA Estatística para tomar decisões
e disparar automações integradas.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DecisionPriority(Enum):
    CRITICAL = 1    # Ação imediata (queda > 50%)
    HIGH = 2        # Ação em 1h (queda > 30%)
    MEDIUM = 3      # Ação em 24h (queda > 20%)
    LOW = 4         # Ação em 48h (queda > 10%)
    INFO = 5        # Apenas notificar

class DecisionEngine:
    """
    Cérebro de decisão do Marketing Director OS.
    
    Fluxo:
    1. Recebe insights da IA (RAG + GPT)
    2. Recebe anomalias (Z-score)
    3. Classifica prioridade
    4. Decide ação automática
    5. Dispara automação
    6. Acompanha resultado
    """
    
    def __init__(self, db, ai_engine, anomaly_detector):
        self.db = db
        self.ai = ai_engine
        self.anomaly = anomaly_detector
    
    # ═══════════════════════════════════════════════════════════════
    # 1. RECEBER INSIGHTS E ANOMALIAS
    # ═══════════════════════════════════════════════════════════════
    
    def process_insight(self, insight: Dict[str, Any]) -> Optional[Dict]:
        """
        Processa insight da IA e decide se gera automação.
        
        Exemplo de insight:
        {
            "tenant_id": "uuid",
            "context": "Vendas caíram 30%",
            "ai_response": "Recomendo campanha de reativação...",
            "confidence": 0.85
        }
        """
        # Extrair métricas do insight
        metrics = self._extract_metrics_from_insight(insight)
        
        # Classificar prioridade
        priority = self._classify_priority(metrics)
        
        # Decidir ação
        action = self._decide_action(insight, priority)
        
        if action:
            # Criar registro de decisão
            decision = self._log_decision(insight, action)
            
            # Disparar automação
            automation = self._trigger_automation(action)
            
            return {
                "decision": decision,
                "automation": automation
            }
        
        return None
    
    def process_anomaly(self, anomaly: Dict[str, Any]) -> Optional[Dict]:
        """
        Processa anomalia estatística e decide ação.
        
        Exemplo de anomalia:
        {
            "tenant_id": "uuid",
            "metric_key": "vendas_total",
            "metric_value": 15000,
            "z_score": 3.2,
            "severity": "critical"
        }
        """
        # Mapear severidade para prioridade
        priority_map = {
            "critical": DecisionPriority.CRITICAL,
            "high": DecisionPriority.HIGH,
            "medium": DecisionPriority.MEDIUM,
            "low": DecisionPriority.LOW
        }
        
        priority = priority_map.get(anomaly["severity"], DecisionPriority.INFO)
        
        # Decidir ação baseada na anomalia
        action = self._decide_action_from_anomaly(anomaly, priority)
        
        if action:
            # Log decisão
            decision = self._log_decision(anomaly, action)
            
            # Disparar automação
            automation = self._trigger_automation(action)
            
            return {
                "decision": decision,
                "automation": automation
            }
        
        return None
    
    # ═══════════════════════════════════════════════════════════════
    # 2. CLASSIFICAR PRIORIDADE
    # ═══════════════════════════════════════════════════════════════
    
    def _classify_priority(self, metrics: Dict[str, Any]) -> DecisionPriority:
        """
        Classifica prioridade baseada em impacto nos KPIs.
        """
        # Regras de prioridade
        if metrics.get("revenue_drop", 0) > 0.5:
            return DecisionPriority.CRITICAL
        
        if metrics.get("revenue_drop", 0) > 0.3:
            return DecisionPriority.HIGH
        
        if metrics.get("cac_increase", 0) > 0.5:
            return DecisionPriority.HIGH
        
        if metrics.get("revenue_drop", 0) > 0.2:
            return DecisionPriority.MEDIUM
        
        if metrics.get("leads_drop", 0) > 0.3:
            return DecisionPriority.MEDIUM
        
        return DecisionPriority.LOW
    
    # ═══════════════════════════════════════════════════════════════
    # 3. DECIDIR AÇÃO
    # ═══════════════════════════════════════════════════════════════
    
    def _decide_action(self, insight: Dict, priority: DecisionPriority) -> Optional[Dict]:
        """
        Decide qual automação disparar baseado no insight.
        """
        context = insight.get("context", "").lower()
        ai_response = insight.get("ai_response", "").lower()
        
        # Padrões de decisão
        if any(word in context for word in ["queda", "caiu", "diminuiu"]):
            if "venda" in context:
                return self._create_reactivation_campaign(insight, priority)
            elif "lead" in context:
                return self._create_lead_campaign(insight, priority)
        
        if any(word in ai_response for word in ["campanha", "disparar", "enviar"]):
            return self._create_suggested_campaign(insight, priority)
        
        return None
    
    def _decide_action_from_anomaly(self, anomaly: Dict, priority: DecisionPriority) -> Dict:
        """
        Decide ação baseada em anomalia estatística.
        """
        metric = anomaly["metric_key"]
        severity = anomaly["severity"]
        
        # Ações automáticas por tipo de métrica
        if "venda" in metric or "receita" in metric:
            if priority in [DecisionPriority.CRITICAL, DecisionPriority.HIGH]:
                return {
                    "type": "whatsapp_message",
                    "priority": priority.value,
                    "payload": {
                        "to": "diretoria",
                        "message": f"🚨 ALERTA CRÍTICO: {metric} com queda anômala de {anomaly['z_score']:.1f} desvios padrão. Investigar imediatamente."
                    }
                }
        
        if "lead" in metric:
            if priority == DecisionPriority.CRITICAL:
                return {
                    "type": "whatsapp_campaign",
                    "priority": priority.value,
                    "payload": {
                        "campaign_type": "lead_reactivation",
                        "target": "leads_frios_30d"
                    }
                }
        
        return None
    
    # ═══════════════════════════════════════════════════════════════
    # 4. DISPARAR AUTOMAÇÃO
    # ═══════════════════════════════════════════════════════════════
    
    def _trigger_automation(self, action: Dict) -> Dict:
        """
        Dispara automação e retorna status.
        """
        automation = {
            "automation_type": action["type"],
            "status": "pending",
            "trigger_source": "insight" if "insight" in action else "anomaly",
            "priority": action.get("priority", 5),
            "payload": action.get("payload", {}),
            "scheduled_for": datetime.now()
        }
        
        # Inserir na fila
        queue_id = self.db.insert_automation_queue(automation)
        
        # Processar imediatamente se for crítica
        if automation["priority"] <= 2:
            self._process_automation_now(queue_id)
        
        return {
            "queue_id": queue_id,
            "status": "queued",
            "priority": automation["priority"]
        }
    
    def _process_automation_now(self, queue_id: str):
        """
        Processa automação imediatamente (prioridade crítica).
        """
        # Buscar da fila
        automation = self.db.get_automation_queue(queue_id)
        
        # Executar baseado no tipo
        if automation["automation_type"] == "whatsapp_message":
            self._send_whatsapp_message(automation["payload"])
        elif automation["automation_type"] == "whatsapp_campaign":
            self._send_whatsapp_campaign(automation["payload"])
        elif automation["automation_type"] == "meta_ads_create":
            self._create_meta_ads_campaign(automation["payload"])
        # ... outros tipos
        
        # Atualizar status
        self.db.update_automation_queue(queue_id, "completed")
    
    # ═══════════════════════════════════════════════════════════════
    # 5. LOG DE DECISÕES
    # ═══════════════════════════════════════════════════════════════
    
    def _log_decision(self, source: Dict, action: Dict) -> Dict:
        """
        Registra decisão no histórico para auditoria e aprendizado.
        """
        decision = {
            "tenant_id": source.get("tenant_id"),
            "insight_id": source.get("id") if "insight" in source else None,
            "anomaly_id": source.get("id") if "anomaly" in source else None,
            "decision_type": action["type"],
            "decision_reasoning": self._generate_reasoning(source, action),
            "alternatives_considered": [],
            "expected_impact": self._estimate_impact(action),
            "created_at": datetime.now()
        }
        
        return self.db.insert_decision_history(decision)
    
    def _generate_reasoning(self, source: Dict, action: Dict) -> str:
        """
        Gera explicação do porquê a decisão foi tomada.
        """
        if "anomaly" in source:
            return (
                f"Decisão automática baseada em anomalia estatística: "
                f"{source['metric_key']} com Z-score de {source['z_score']:.2f} "
                f"(severidade: {source['severity']}). "
                f"Ação: {action['type']} para mitigar impacto."
            )
        else:
            return (
                f"Decisão baseada em insight de IA: {source.get('context', 'N/A')}. "
                f"Confiança da IA: {source.get('confidence', 0):.0%}. "
                f"Ação: {action['type']}."
            )
    
    def _estimate_impact(self, action: Dict) -> Dict:
        """
        Estima impacto esperado da ação.
        """
        # Estimativas baseadas em histórico
        if action["type"] == "whatsapp_campaign":
            return {
                "expected_conversion": "5-10%",
                "expected_revenue": "R$ 5.000-10.000",
                "timeframe": "7 dias"
            }
        elif action["type"] == "meta_ads_create":
            return {
                "expected_leads": "50-100",
                "expected_cac": "R$ 20-40",
                "timeframe": "14 dias"
            }
        return {}
```

---

### 3. Automações Integradas

**Ações que o cérebro dispara**

```python
# engine/src/automations/
# ├── whatsapp.py
# ├── meta_ads.py
# ├── google_ads.py
# ├── email.py
# └── obsidian.py

# ═══════════════════════════════════════════════════════════════
# WHATSAPP AUTOMATIONS (Evolution API)
# ═══════════════════════════════════════════════════════════════

class WhatsAppAutomation:
    """
    Automações de WhatsApp via Evolution API.
    """
    
    def __init__(self, evolution_api_url: str, api_key: str):
        self.api_url = evolution_api_url
        self.api_key = api_key
    
    def send_message(self, to: str, message: str):
        """
        Envia mensagem individual.
        """
        payload = {
            "number": to,
            "message": message,
            "instant": True
        }
        
        response = requests.post(
            f"{self.api_url}/message/sendText",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )
        
        return response.json()
    
    def send_campaign(self, campaign_type: str, target: str):
        """
        Dispara campanha em massa.
        
        Tipos:
        - lead_reactivation: Reativar leads frios
        - customer_fidelization: Fidelizar clientes
        - promotion: Campanha promocional
        """
        # Buscar contatos no banco
        contacts = self._get_target_contacts(target)
        
        # Gerar mensagem baseada no tipo
        message = self._generate_campaign_message(campaign_type)
        
        # Disparar em lote (rate limit: 1 msg/seg)
        results = []
        for contact in contacts:
            result = self.send_message(contact["phone"], message)
            results.append(result)
            time.sleep(1)  # Evitar bloqueio
        
        return {
            "campaign_type": campaign_type,
            "sent": len(results),
            "results": results
        }
    
    def _get_target_contacts(self, target: str) -> List[Dict]:
        """
        Busca contatos segmentados no banco.
        """
        if target == "leads_frios_30d":
            # Leads sem compra há 30+ dias
            query = """
            SELECT DISTINCT phone, name
            FROM leads
            WHERE last_contact < NOW() - INTERVAL '30 days'
            AND status = 'lead'
            """
        elif target == "clientes_ativos":
            # Clientes com compra nos últimos 60 dias
            query = """
            SELECT DISTINCT phone, name
            FROM customers
            WHERE last_purchase >= NOW() - INTERVAL '60 days'
            """
        
        return self.db.execute_query(query)
    
    def _generate_campaign_message(self, campaign_type: str) -> str:
        """
        Gera mensagem personalizada baseada no tipo de campanha.
        """
        templates = {
            "lead_reactivation": """
Oi {name}! 👋

Vi que você demonstrou interesse em nossos serviços há algumas semanas.

Que tal retomar nosso contato? Temos uma condição especial para você!

🎁 **{offer}**

Só até {deadline}. Bora agendar?

Responda "SIM" que te explico tudo!
""",
            
            "customer_fidelization": """
Oi {name}! Tudo bem?

Você é um cliente especial pra gente! 💙

Por isso, separamos um presente exclusivo:

🎁 **{offer}**

Válido até {deadline}. Agende agora!
""",
            
            "promotion": """
🔥 **OFERTA RELÂMPAGO!** 🔥

Oi {name}, só hoje:

{offer}

⏰ Só até às {deadline}h!

Bora aproveitar? Responda "QUERO"!
"""
        }
        
        return templates.get(campaign_type, "Olá {name}!")
```

```python
# ═══════════════════════════════════════════════════════════════
# META ADS AUTOMATIONS
# ═══════════════════════════════════════════════════════════════

class MetaAdsAutomation:
    """
    Automações de Meta Ads (Facebook/Instagram Ads).
    """
    
    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def create_campaign(self, objective: str, budget: float, targeting: Dict):
        """
        Cria campanha automaticamente.
        """
        # 1. Criar Campaign
        campaign = self._create_campaign(objective, budget)
        
        # 2. Criar Ad Set
        ad_set = self._create_ad_set(campaign["id"], targeting)
        
        # 3. Criar Ad (criativo)
        ad = self._create_ad(ad_set["id"])
        
        return {
            "campaign_id": campaign["id"],
            "ad_set_id": ad_set["id"],
            "ad_id": ad["id"],
            "status": "active"
        }
    
    def optimize_campaign(self, campaign_id: str, performance: Dict):
        """
        Otimiza campanha baseada em performance.
        """
        # Se ROAS < 2, reduzir orçamento
        if performance.get("roas", 0) < 2.0:
            self._reduce_budget(campaign_id, 0.2)  # -20%
        
        # Se CTR < 1%, pausar criativo
        if performance.get("ctr", 0) < 0.01:
            self._pause_ad(campaign_id)
        
        # Se frequência > 4, renovar criativo
        if performance.get("frequency", 0) > 4:
            self._create_new_ad_variant(campaign_id)
    
    def _create_campaign(self, objective: str, budget: float) -> Dict:
        """
        Cria campanha no Meta Ads.
        """
        params = {
            "name": f"Auto-Generated {objective} {datetime.now().strftime('%Y-%m-%d')}",
            "objective": objective,
            "status": "ACTIVE",
            "daily_budget": budget,
            "access_token": self.access_token
        }
        
        response = requests.post(
            f"{self.base_url}/act_{self.account_id}/campaigns",
            params=params
        )
        
        return response.json()
```

```python
# ═══════════════════════════════════════════════════════════════
# OBSIDIAN AUTOMATIONS
# ═══════════════════════════════════════════════════════════════

class ObsidianAutomation:
    """
    Automações de escrita no Obsidian.
    """
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = obsidian_path
    
    def write_executive_report(self, tenant_id: str, period: str):
        """
        Gera relatório executivo automático.
        """
        # Buscar dados do período
        metrics = self.db.get_metrics_summary(tenant_id, period)
        insights = self.db.get_insights(tenant_id, period)
        anomalies = self.db.get_anomalies(tenant_id, period)
        
        # Gerar Markdown
        content = f"""
# 📊 Relatório Executivo — {period}

**Gerado em**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 Resumo Executivo

{self._generate_executive_summary(metrics)}

---

## 📈 KPIs Principais

{self._generate_kpi_table(metrics)}

---

## 🧠 Insights da IA

{self._generate_insights_section(insights)}

---

## 🚨 Anomalias Detectadas

{self._generate_anomalies_section(anomalies)}

---

## ✅ Ações Automáticas Disparadas

{self._generate_actions_section(tenant_id, period)}

---

## 📋 Próximos Passos

{self._generate_next_steps(tenant_id)}

---

*Relatório gerado automaticamente pelo Cérebro de Marketing*
"""
        
        # Escrever arquivo
        filename = f"RELATORIO_{tenant_id}_{period}.md"
        filepath = os.path.join(self.obsidian_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
```

---

## 🚀 FLUXO COMPLETO DE AUTOMAÇÃO

### Exemplo Real: Queda de Vendas

```
1. 📊 DADO ENTRA
   └─> CSV de vendas cai em drive_data/franquia-chapeco/

2. ⚙️ PROCESSAMENTO
   └─> Engine processa CSV
   └─> Salva em business_metrics

3. 🧠 IA ANALISA
   └─> RAG detecta: "Vendas caíram 45% vs média 30d"
   └─> Z-score: 3.2 (crítico)

4. 💡 INSIGHT GERADO
   └─> IA: "Recomendo campanha de reativação imediata"
   └─> Confiança: 87%

5. ⚡ DECISÃO AUTOMÁTICA
   └─> Decision Engine classifica: CRITICAL
   └─> Decide: WhatsApp Campaign + Alerta Diretoria

6. 🚀 AÇÕES DISPARADAS
   ├─> WhatsApp para franqueado: "🚨 ALERTA: Queda de 45%"
   ├─> WhatsApp Campaign: "Oferta Relâmpago" para 500 leads
   └─> Obsidian: Relatório atualizado

7. 📊 ACOMPANHAMENTO
   └─> Monitora conversão da campanha
   └─> Se ROAS > 3, aumenta orçamento
   └─> Se ROAS < 2, pausa e notifica

8. 📈 APRENDIZADO
   └─> Registra no decision_history
   └─> Atualiza modelo para próxima decisão
```

---

## 📋 ROADMAP DE IMPLEMENTAÇÃO

### Fase 0: Base (MD-OS v4.0) — ✅ JÁ FEITO
- [x] Supabase schema
- [x] Engine Python
- [x] Obsidian Bridge
- [x] IA RAG

### Fase 1: Anomalias + Fila (20 horas)
- [ ] Tabela anomaly_alerts
- [ ] Tabela automation_queue
- [ ] Z-score detector
- [ ] Decision Engine básico

### Fase 2: WhatsApp (30 horas)
- [ ] Integration com Evolution API
- [ ] Send message
- [ ] Send campaign
- [ ] Templates de mensagens

### Fase 3: Meta Ads (40 horas)
- [ ] Integration com Meta Ads API
- [ ] Create campaign
- [ ] Optimize campaign
- [ ] Pause/Resume ads

### Fase 4: Obsidian Reports (15 horas)
- [ ] Executive reports automáticos
- [ ] Anomaly reports
- [ ] Decision history

### Fase 5: Aprendizado (25 horas)
- [ ] Decision history analysis
- [ ] Impact measurement
- [ ] Model improvement

**Total**: 130 horas (~3-4 semanas)

---

## 🏆 CONCLUSÃO

### O Que Você Terá

```
┌─────────────────────────────────────────────────────────────────┐
│           CÉREBRO DE GESTÃO DE MARKETING                        │
│                                                                 │
│  ✅ Analisa dados de 60 unidades automaticamente                │
│  ✅ Detecta anomalias antes de você perceber                    │
│  ✅ Gera insights estratégicos com IA                           │
│  ✅ Dispara automações (WhatsApp, Ads) sozinho                  │
│  ✅ Acompanha resultados e otimiza                              │
│  ✅ Gera relatórios no Obsidian                                 │
│                                                                 │
│  VOCÊ: Foca em estratégia, não em operação                      │
└─────────────────────────────────────────────────────────────────┘
```

### Próximo Passo Imediato

```bash
# 1. Validar MD-OS v4.0 atual
cd mkt
docker-compose ps

# 2. Começar Fase 1 (Anomalias)
# Criar tabela anomaly_alerts no Supabase
# Implementar Z-score detector
```

---

<div align="center">

**🧠 CÉREBRO DE MARKETING COM IA — ARQUITETURA COMPLETA**

*Pensar → Decidir → Agir Automaticamente*

</div>
