# 🤖 MARKETING BRAIN — Arquitetura Semi-Automática (Human-in-the-Loop)

> **Conceito**: "Iron Man Suit" — Você no comando, IA faz o trabalho pesado
> **Modelo**: HITL (Human-in-the-Loop) — Aprovação humana antes de execução
> **Interface**: Obsidian como Centro de Comando Ativo
> **Data**: 2026-02-25
> **Status**: Arquitetura Conceitual + Implementação Prática

---

## 🎯 VISÃO GERAL

### O Problema das Extremas

```
┌─────────────────────────────────────────────────────────────────┐
│  EXTREMO 1: Dashboard Passivo (Visão 2.0)                       │
│                                                                 │
│  • IA analisa dados                                             │
│  • IA gera relatório                                            │
│  • HUMANO: Lê, interpreta, abre Meta Ads, executa               │
│                                                                 │
│  ❌ Lento, dependente de disciplina humana                      │
│  ❌ Você vira operador de ferramenta                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  EXTREMO 2: Full Agentic (Visão 3.0)                            │
│                                                                 │
│  • IA analisa dados                                             │
│  • IA decide                                                    │
│  • IA executa SOZINHA                                           │
│                                                                 │
│  ❌ "Black Box" — IA queimando orçamento à noite                │
│  ❌ Sem controle humano                                         │
│  ❌ Assustador para maioria dos usuários                        │
└─────────────────────────────────────────────────────────────────┘
```

### Solução: **Semi-Automático (HITL)**

```
┌─────────────────────────────────────────────────────────────────┐
│  CÉREBRO SEMI-AUTOMÁTICO (Human-in-the-Loop)                    │
│                                                                 │
│  1. 🧠 IA DETECTA                                               │
│     • Monitora Supabase 24/7                                    │
│     • Detecta anomalias, oportunidades                          │
│     • Gera diagnóstico + ação sugerida                          │
│                                                                 │
│  2. 📝 IA PROPÕE (Obsidian)                                     │
│     • Cria nota estruturada no Obsidian                         │
│     • Inclui: Contexto + Análise + Ação Sugerida                │
│     • Adiciona: Botão/Comando de aprovação                      │
│                                                                 │
│  3. 👤 HUMANO DECIDE                                            │
│     • Lê nota (30 segundos)                                     │
│     • Avalia: Faz sentido?                                      │
│     • Decide: Aprovar / Rejeitar / Modificar                    │
│                                                                 │
│  4. ⚡ IA EXECUTA                                               │
│     • Se aprovado: Dispara API (Meta, Google, WhatsApp)         │
│     • Se rejeitado: Aprende com feedback                        │
│     • Registra: Decision history para auditoria                 │
│                                                                 │
│  ✅ MELHOR DOS DOIS MUNDOS:                                     │
│  • Velocidade da IA                                             │
│  • Controle humano                                              │
│  • Zero "Black Box"                                             │
│  • Aprendizado contínuo                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗 ARQUITETURA DO SISTEMA

### Diagrama de Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORAMENTO CONTÍNUO                       │
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐                │
│  │  Python Engine   │      │  Supabase        │                │
│  │  (HIVE Brain)    │─────►│  (Real-time)     │                │
│  │                  │      │                  │                │
│  │ - Anomaly detect │      │ - business_      │                │
│  │ - Insight gen    │      │   metrics         │                │
│  │ - Decision eng   │      │ - anomaly_        │                │
│  └──────────────────┘      │   alerts          │                │
│                            └────────┬─────────┘                │
└─────────────────────────────────────┼───────────────────────────┘
                                      │
                                      │ (Postgres Changes)
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN (Centro de Comando)                 │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  🚨 ALERTA: Campanha "Verão 2026" com CAC 30%     │        │
│  │     acima da meta                                  │        │
│  │                                                    │        │
│  │  📊 DIAGNÓSTICO:                                  │        │
│  │  O criativo B fadigou nos últimos 3 dias.         │        │
│  │  - Frequência: 4.2 (ideal: < 3.0)                 │        │
│  │  - CTR: 0.8% → 0.4% (queda de 50%)                │        │
│  │  - CPL: R$ 15 → R$ 28 (aumento de 87%)            │        │
│  │                                                    │        │
│  │  💡 AÇÃO SUGERIDA:                                │        │
│  │  1. Pausar criativo B                             │        │
│  │  2. Aumentar bid do criativo A em 10%             │        │
│  │  3. Testar novo criativo C (público similar)      │        │
│  │                                                    │        │
│  │  📈 IMPACTO ESPERADO:                             │        │
│  │  - Redução de CPL: R$ 28 → R$ 16                  │        │
│  │  - Economia mensal: R$ 3.500                      │        │
│  │                                                    │        │
│  │  ┌──────────────────────────────────────────┐    │        │
│  │  │  ✅ APROVAR AÇÃO  │  ❌ REJEITAR  │  ✏️ EDITAR  │    │        │
│  │  └──────────────────────────────────────────┘    │        │
│  │                                                    │        │
│  │  [Comando: /mdcc approve]                         │        │
│  │  [Comando: /mdcc reject]                          │        │
│  │  [Comando: /mdcc edit]                            │        │
│  └────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      │ (Webhook/API)
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUÇÃO (Backend Python)                    │
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐                │
│  │  Webhook Server  │      │  API Integrations│                │
│  │  (FastAPI)       │─────►│                  │                │
│  │                  │      │ - Meta Ads API   │                │
│  │ - Recebe approve │      │ - Google Ads API │                │
│  │ - Valida auth    │      │ - Evolution API  │                │
│  │ - Executa ação   │      │ - Email/SMS API  │                │
│  └──────────────────┘      └──────────────────┘                │
│                                                                 │
│  ┌──────────────────┐                                          │
│  │  Decision History│                                          │
│  │  (Audit Trail)   │                                          │
│  │                  │                                          │
│  │ - Quem aprovou   │                                          │
│  │ - Quando         │                                          │
│  │ - O que foi feito│                                          │
│  │ - Resultado      │                                          │
│  └──────────────────┘                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENTES TÉCNICOS

### 1. **Backend Python** (FastAPI + Webhooks)

```python
# engine/src/webhook_server.py
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
import hmac
import hashlib

app = FastAPI()

class ActionApproval(BaseModel):
    action_id: str
    decision: str  # "approve", "reject", "edit"
    user_id: str
    edits: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None

class WebhookServer:
    def __init__(self, supabase, meta_api, google_api):
        self.supabase = supabase
        self.meta_api = meta_api
        self.google_api = google_api
    
    @app.post("/webhook/mdcc/action")
    async def receive_action_decision(
        approval: ActionApproval,
        x_obsidian_signature: str = Header(None)
    ):
        """
        Recebe decisão do Obsidian (aprovar/rejeitar ação).
        """
        # 1. Validar assinatura (segurança)
        if not verify_signature(approval, x_obsidian_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # 2. Buscar ação original
        action = supabase.from_("automation_queue").select("*").eq("id", approval.action_id).execute()
        
        if not action.data:
            raise HTTPException(status_code=404, detail="Action not found")
        
        action = action.data[0]
        
        # 3. Processar decisão
        if approval.decision == "approve":
            # Executar ação aprovada
            result = await execute_action(action)
            
            # Atualizar status
            supabase.table("automation_queue").update({
                "status": "completed",
                "completed_at": datetime.now(),
                "result": result,
                "approved_by": approval.user_id
            }).eq("id", approval.action_id).execute()
            
            # Log de auditoria
            log_decision(approval, action, result)
            
            return {"status": "success", "message": "Action executed"}
        
        elif approval.decision == "reject":
            # Rejeitar ação
            supabase.table("automation_queue").update({
                "status": "rejected",
                "rejected_by": approval.user_id,
                "rejection_reason": approval.reason
            }).eq("id", approval.action_id).execute()
            
            # IA aprende com rejeição
            await ai_learn_from_rejection(action, approval.reason)
            
            return {"status": "rejected", "message": "Action rejected"}
        
        elif approval.decision == "edit":
            # Editar e depois executar
            edited_action = {**action, **approval.edits}
            result = await execute_action(edited_action)
            
            supabase.table("automation_queue").update({
                "status": "completed",
                "completed_at": datetime.now(),
                "result": result,
                "edited_by": approval.user_id,
                "edits": approval.edits
            }).eq("id", approval.action_id).execute()
            
            return {"status": "success", "message": "Action edited and executed"}

async def execute_action(action: Dict) -> Dict:
    """
    Executa ação baseada no tipo.
    """
    if action["automation_type"] == "meta_ads_pause":
        return await meta_api.pause_ad(action["payload"]["ad_id"])
    
    elif action["automation_type"] == "meta_ads_increase_bid":
        return await meta_api.increase_bid(
            action["payload"]["ad_id"],
            action["payload"]["increase_percent"]
        )
    
    elif action["automation_type"] == "whatsapp_campaign":
        return await evolution_api.send_campaign(action["payload"])
    
    # ... outros tipos

async def ai_learn_from_rejection(action: Dict, reason: str):
    """
    IA aprende com rejeições para melhorar próximas sugestões.
    """
    # Inserir no banco para análise futura
    supabase.table("ai_feedback").insert({
        "action_id": action["id"],
        "feedback_type": "rejection",
        "reason": reason,
        "created_at": datetime.now()
    }).execute()
    
    # Fine-tune do modelo (opcional)
    # await retrain_model_based_on_feedback()
```

---

### 2. **Plugin Obsidian** (Comandos + Webhooks)

```typescript
// src/commands/action_commands.ts
import { App, Notice, MarkdownView } from 'obsidian';
import { MarketingBrainPlugin } from '../main';

export class ActionCommands {
    constructor(private app: App, private plugin: MarketingBrainPlugin) {}
    
    /**
     * Comando: /mdcc approve
     * Aprovar ação sugerida
     */
    async approveAction() {
        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!view) {
            new Notice("❌ Nenhuma nota ativa");
            return;
        }
        
        // Extrair action_id da nota (frontmatter)
        const file = view.file;
        const cache = this.app.metadataCache.getCache(file.path);
        const actionId = cache.frontmatter?.action_id;
        
        if (!actionId) {
            new Notice("❌ Nota não é uma ação válida");
            return;
        }
        
        // Disparar webhook de aprovação
        try {
            const response = await fetch(`${this.plugin.settings.webhookUrl}/webhook/mdcc/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Obsidian-Signature': await this.generateSignature(actionId, 'approve')
                },
                body: JSON.stringify({
                    action_id: actionId,
                    decision: 'approve',
                    user_id: this.plugin.settings.userId
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Atualizar nota com status
                const content = view.getData();
                const updatedContent = content.replace(
                    '⏳ Pendente de aprovação',
                    '✅ Aprovado e executado'
                );
                await view.setData(updatedContent);
                
                new Notice("✅ Ação aprovada e executada!");
            } else {
                new Notice(`❌ Erro: ${result.message}`);
            }
        } catch (error) {
            new Notice(`❌ Erro ao aprovar: ${error.message}`);
        }
    }
    
    /**
     * Comando: /mdcc reject
     * Rejeitar ação sugerida
     */
    async rejectAction() {
        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!view) return;
        
        const file = view.file;
        const cache = this.app.metadataCache.getCache(file.path);
        const actionId = cache.frontmatter?.action_id;
        
        if (!actionId) return;
        
        // Pedir motivo da rejeição
        const reason = await this.promptForReason();
        
        // Disparar webhook de rejeição
        try {
            const response = await fetch(`${this.plugin.settings.webhookUrl}/webhook/mdcc/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Obsidian-Signature': await this.generateSignature(actionId, 'reject')
                },
                body: JSON.stringify({
                    action_id: actionId,
                    decision: 'reject',
                    user_id: this.plugin.settings.userId,
                    reason: reason
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'rejected') {
                // Atualizar nota
                const content = view.getData();
                const updatedContent = content.replace(
                    '⏳ Pendente de aprovação',
                    '❌ Rejeitado'
                );
                await view.setData(updatedContent);
                
                new Notice("❌ Ação rejeitada. IA vai aprender com isso.");
            }
        } catch (error) {
            new Notice(`❌ Erro ao rejeitar: ${error.message}`);
        }
    }
    
    /**
     * Comando: /mdcc edit
     * Editar ação antes de aprovar
     */
    async editAction() {
        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!view) return;
        
        const file = view.file;
        const cache = this.app.metadataCache.getCache(file.path);
        const actionId = cache.frontmatter?.action_id;
        
        if (!actionId) return;
        
        // Abrir modal de edição
        const edits = await this.openEditModal();
        
        // Disparar webhook com edições
        try {
            const response = await fetch(`${this.plugin.settings.webhookUrl}/webhook/mdcc/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Obsidian-Signature': await this.generateSignature(actionId, 'edit')
                },
                body: JSON.stringify({
                    action_id: actionId,
                    decision: 'edit',
                    user_id: this.plugin.settings.userId,
                    edits: edits
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                new Notice("✅ Ação editada e executada!");
            }
        } catch (error) {
            new Notice(`❌ Erro ao editar: ${error.message}`);
        }
    }
    
    private async promptForReason(): Promise<string> {
        // Modal simples para pedir motivo
        return new Promise((resolve) => {
            const reason = prompt("Por que você está rejeitando esta ação?");
            resolve(reason || "Sem motivo específico");
        });
    }
    
    private async openEditModal(): Promise<Dict<any>> {
        // Modal mais complexo para editar parâmetros
        // Retorna objeto com edições
        return {
            "increase_percent": 15  // Ex: mudar de 10% para 15%
        };
    }
    
    private async generateSignature(actionId: string, decision: string): Promise<string> {
        // Gerar assinatura HMAC para segurança
        const secret = this.plugin.settings.webhookSecret;
        const data = `${actionId}:${decision}:${this.plugin.settings.userId}`;
        
        const encoder = new TextEncoder();
        const keyData = encoder.encode(secret);
        const dataData = encoder.encode(data);
        
        const key = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );
        
        const signature = await crypto.subtle.sign('HMAC', key, dataData);
        return Array.from(new Uint8Array(signature))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }
}
```

---

### 3. **Templates de Ações** (Markdown Estruturado)

```markdown
---
action_id: "act_123456789"
action_type: "meta_ads_optimize"
status: "pending_approval"
created_at: 2026-02-25 10:30:00
priority: "high"
expected_impact: "R$ 3.500/mês"
---

# 🚨 ALERTA DE OTIMIZAÇÃO

**Campanha**: Verão 2026  
**Problema**: CAC 30% acima da meta  
**Detectado em**: 2026-02-25 10:30:00

---

## 📊 DIAGNÓSTICO

### Métricas Atuais vs Meta

| Métrica | Atual | Meta | Variação |
| :------ | :---- | :--- | :------- |
| **CAC** | R$ 45 | R$ 35 | ▲ +29% |
| **CTR** | 0.4% | 0.8% | ▼ -50% |
| **Frequência** | 4.2 | < 3.0 | ▲ +40% |
| **CPL** | R$ 28 | R$ 15 | ▲ +87% |

### Causa Raiz

**Criativo B fadigou** nos últimos 3 dias:

- Impressões: 50.000 (público saturado)
- Frequência: 4.2 (usuários vendo muitas vezes)
- CTR: 0.8% → 0.4% (queda de 50%)
- CPL: R$ 15 → R$ 28 (aumento de 87%)

---

## 💡 AÇÃO SUGERIDA

### 1. Pausar Criativo B
```
Ad ID: ad_987654321
Ação: Pause
Motivo: Fadiga de criativo (frequência > 4.0)
```

### 2. Aumentar Bid do Criativo A
```
Ad ID: ad_123456789
Ação: Increase bid by 10%
Motivo: Melhor performance (CTR 1.2%, CPL R$ 12)
```

### 3. Testar Novo Criativo C
```
Público: Lookalike 1% (clientes últimos 90 dias)
Budget: R$ 50/dia
Duração: 7 dias
```

---

## 📈 IMPACTO ESPERADO

### Projeção (Baseado em dados históricos)

| Métrica | Antes | Depois | Melhoria |
| :------ | :---- | :----- | :------- |
| **CAC** | R$ 45 | R$ 32 | ▼ -29% |
| **CTR** | 0.4% | 0.9% | ▲ +125% |
| **CPL** | R$ 28 | R$ 16 | ▼ -43% |

### Economia Mensal

- **Atual**: R$ 12.000/mês (CAC R$ 45 × 267 clientes)
- **Projetado**: R$ 8.500/mês (CAC R$ 32 × 267 clientes)
- **Economia**: **R$ 3.500/mês**

---

## ⚡ DECISÃO

**Tempo estimado de execução**: 2 minutos  
**Risco**: Baixo (ações reversíveis)  
**Reversibilidade**: Sim (pode desfazer em 5 minutos)

---

### Aprovar Ação

**Comandos disponíveis**:

- `/mdcc approve` — Aprovar e executar
- `/mdcc reject` — Rejeitar (pede motivo)
- `/mdcc edit` — Editar parâmetros antes de aprovar

---

**Status**: ⏳ Pendente de aprovação  
**Aguardando**: Decisão do usuário  
**Expira em**: 24 horas (após isso, ação é arquivada)

---

*Gerado automaticamente pelo MDCC v4.0*  
*Action ID: act_123456789*
```

---

## 📋 CASOS DE USO IMEDIATOS

### 1. **Otimização de Campanhas (Meta Ads)**

**Fluxo**:
```
1. IA detecta: Criativo com frequência > 4.0
2. IA gera: Nota no Obsidian com diagnóstico
3. Humano: Lê, aprova com /mdcc approve
4. IA: Executa pause no Meta Ads via API
5. IA: Registra resultado no Supabase
```

**Tempo economizado**: 15 minutos por campanha × 10 campanhas/semana = **2.5 horas/semana**

---

### 2. **Reativação de Leads Frios**

**Fluxo**:
```
1. IA detecta: Leads sem compra há 30+ dias
2. IA gera: Campanha de WhatsApp (copy + lista)
3. Humano: Revisa copy, aprova com /mdcc approve
4. IA: Dispara campanha via Evolution API
5. IA: Acompanha respostas e converte vendas
```

**Resultado típico**: 5-10% de conversão, R$ 5.000-10.000 em vendas recuperadas

---

### 3. **Draft de E-mails Frios**

**Fluxo**:
```
1. IA analisa: Leads qualificados sem resposta
2. IA gera: 3 versões de e-mail frio (A/B/C)
3. Humano: Escolhe melhor versão, aprova
4. IA: Dispara via API de e-mail (SendGrid, etc.)
5. IA: Track de opens/clicks/respostas
```

**Tempo economizado**: 30 minutos por campanha × 4 campanhas/semana = **2 horas/semana**

---

### 4. **Chat com Dados (Text-to-SQL)**

**Fluxo**:
```
1. Humano: Abre nota em branco no Obsidian
2. Humano: Digita: "Quanto faturamos ontem?"
3. Plugin: Envia query para MDCC
4. MDCC: Converte texto → SQL (via RAG + LLM)
5. MDCC: Executa SQL no Supabase
6. MDCC: Retorna resposta em Markdown
7. Plugin: Imprime resposta na nota
```

**Exemplo de resposta**:
```markdown
# 📊 Faturamento Ontem (2026-02-24)

**Total**: R$ 45.230,00  
**Pedidos**: 127  
**Ticket Médio**: R$ 356,00

### Por Canal

| Canal | Faturamento | % |
| :---- | :---------- | :- |
| Meta Ads | R$ 18.500 | 41% |
| Google Ads | R$ 15.200 | 34% |
| Orgânico | R$ 8.530 | 19% |
| Email | R$ 3.000 | 6% |

---
*Query: SELECT SUM(value) FROM business_metrics WHERE...*
```

---

## ⚖️ COMPARAÇÃO DE MODELOS

| Característica | Dashboard (2.0) | **Semi-Auto (HITL)** | Full Agentic (3.0) |
| :------------- | :-------------: | :------------------: | :----------------: |
| **Descoberta** | Humano | IA | IA |
| **Diagnóstico** | Humano | IA | IA |
| **Ação Sugerida** | Humano | IA | IA |
| **Decisão** | Humano | **Humano** | IA |
| **Execução** | Humano | **IA** | IA |
| **Velocidade** | 🐢 Lenta | ⚡⚡ Rápida | ⚡⚡⚡ Instantânea |
| **Controle** | ✅ Total | ✅ Alto | ❌ Nenhum |
| **Risco** | ✅ Baixo | ✅ Baixo | ⚠️ Alto |
| **Aprendizado** | ❌ Nenhum | ✅ Feedback | ✅ Automático |
| **Complexidade** | 🟢 Baixa | 🟡 Média | 🔴 Alta |

---

## 🚀 IMPLEMENTAÇÃO PRÁTICA

### Fase 1: Webhook Server (10 horas)

```bash
# 1. Criar FastAPI server
cd engine
mkdir src/webhook_server
touch src/webhook_server/main.py

# 2. Implementar endpoints
# - POST /webhook/mdcc/action
# - GET /health
# - POST /webhook/test

# 3. Configurar CORS para Obsidian
# 4. Implementar assinatura HMAC
# 5. Testar com Postman
```

### Fase 2: Plugin Obsidian (20 horas)

```bash
# 1. Clonar template de plugin
git clone https://github.com/obsidianmd/obsidian-sample-plugin.git marketing-brain

# 2. Adicionar comandos
# - /mdcc approve
# - /mdcc reject
# - /mdcc edit

# 3. Implementar webhooks
# 4. Gerar assinaturas HMAC
# 5. Atualizar notas com status

# 6. Build e testar
npm run build
```

### Fase 3: Templates de Ações (5 horas)

```bash
# 1. Criar templates em docs/templates/
# - action_alert.md
# - action_optimization.md
# - action_campaign.md

# 2. Integrar com Decision Engine
# 3. Testar geração automática
```

### Fase 4: Integrações de API (30 horas)

```bash
# 1. Meta Ads API
# - pause_ad()
# - increase_bid()
# - create_campaign()

# 2. Google Ads API
# - pause_ad()
# - adjust_budget()

# 3. Evolution API (WhatsApp)
# - send_message()
# - send_campaign()

# 4. Email API (SendGrid)
# - send_email()
# - send_bulk()
```

**Total**: 65 horas (~2 semanas)

---

## 🔒 SEGURANÇA

### Assinatura HMAC

```python
# Backend valida assinatura de cada request
def verify_signature(payload: Dict, signature: str) -> bool:
    secret = os.getenv("WEBHOOK_SECRET")
    expected = hmac.new(
        secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)
```

### Rate Limiting

```python
# Evitar abuso
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/webhook/mdcc/action", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def receive_action_decision(...):
    ...
```

### Audit Trail

```python
# Toda ação é registrada
def log_decision(approval: ActionApproval, action: Dict, result: Dict):
    supabase.table("decision_history").insert({
        "action_id": action["id"],
        "decision": approval.decision,
        "user_id": approval.user_id,
        "executed_at": datetime.now(),
        "result": result,
        "ip_address": get_client_ip()
    }).execute()
```

---

## 🏆 VEREDITO FINAL

### Por Que Semi-Automático é o Sweet Spot?

```
┌─────────────────────────────────────────────────────────────────┐
│  VANTAGENS DO MODELO SEMI-AUTOMÁTICO                            │
│                                                                 │
│  ✅ CONTROLE: Você decide o que é importante                    │
│  ✅ VELOCIDADE: IA executa em segundos, não minutos             │
│  ✅ APRENDIZADO: IA melhora com seu feedback                    │
│  ✅ AUDITORIA: Tudo registrado (quem, quando, o quê)            │
│  ✅ BAIXO RISCO: Sem "Black Box" queimando orçamento            │
│  ✅ ESCALABILIDADE: Uma pessoa gerencia 10x mais campanhas      │
│                                                                 │
│  🎯 RESULTADO:                                                  │
│  • Diretor foca em estratégia (não em clicar botões)            │
│  • IA faz trabalho operacional (chato, repetitivo)              │
│  • Equipe confia no sistema (não é caixa preta)                 │
│  • Orçamento seguro (nada sem aprovação)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 ARQUIVOS PARA CRIAR

| Arquivo | Descrição | Horas |
| :------ | :-------- | :---: |
| `engine/src/webhook_server.py` | FastAPI + Webhooks | 10h |
| `plugin/src/commands/action_commands.ts` | Comandos Obsidian | 10h |
| `plugin/src/webhook_client.ts` | Cliente de webhooks | 5h |
| `docs/templates/action_alert.md` | Template de alertas | 2h |
| `docs/templates/action_optimization.md` | Template de otimização | 2h |
| `engine/src/integrations/meta_ads.py` | Meta Ads API | 10h |
| `engine/src/integrations/google_ads.py` | Google Ads API | 10h |
| `engine/src/integrations/evolution_api.py` | WhatsApp | 5h |
| `engine/src/integrations/sendgrid.py` | Email API | 3h |

**Total**: 57 horas

---

## 📋 PRÓXIMOS PASSOS

### Hoje (2 horas)
- [ ] Ler este documento completo
- [ ] Decidir: Quer implementar?
- [ ] Se sim, começar por Fase 1 (Webhook Server)

### Esta Semana (10 horas)
- [ ] Setup FastAPI server
- [ ] Implementar endpoint `/webhook/mdcc/action`
- [ ] Testar com Postman

### Próxima Semana (15 horas)
- [ ] Começar plugin Obsidian
- [ ] Implementar comando `/mdcc approve`
- [ ] Testar end-to-end

---

<div align="center">

**🤖 MARKETING BRAIN — SEMI-AUTOMÁTICO (HITL)**

*Iron Man Suit: Você no comando, IA faz o trabalho pesado*

**57 horas • Controle total • Zero "Black Box"**

</div>
