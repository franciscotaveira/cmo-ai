# 🤖 OBSIDIAN COPILIT + MARKETING ENGINE — Configuração e Uso

> **Versão**: v5.2 — EXOCÓRTEX COM IA GENERATIVA  
> **Data**: 2026-03-02  
> **Status**: ✅ Pronto para usar

---

## 📊 RESUMO EXECUTIVO

Com a API key do Copilot configurada no Obsidian, você agora tem:

1. **IA Generativa integrada** ao Marketing Engine
2. **Insights automáticos** baseados em anomalias de métricas
3. **Relatórios semanais** gerados por IA
4. **Ideias de conteúdo** criadas automaticamente
5. **Chat contextual** com seus dados de marketing

---

## 🔧 CONFIGURAÇÃO DO LLM

### Opção 1: **Groq Cloud** (RECOMENDADA — Grátis, Rápido)

**Vantagens**:
- ✅ GRÁTIS (até 30 requisições/minuto)
- ✅ Modelos poderosos (Llama 3.1 70B, Mixtral)
- ✅ Rápido (inferência em milissegundos)
- ✅ Sem necessidade de GPU local

**Setup**:

1. **Obter API Key**:
   - Acesse: https://console.groq.com/
   - Crie conta
   - Vá em "API Keys" → "Create API Key"
   - Copie a key

2. **Configurar no `.env`**:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your-key-here
   ```

3. **Modelos Disponíveis**:
   - `llama-3.1-70b-versatile` (Recomendado)
   - `llama-3.1-8b-instant` (Mais rápido)
   - `mixtral-8x7b-32768` (Alternativo)

---

### Opção 2: **OpenAI API** (Pago, Qualidade)

**Setup**:

1. **Obter API Key**:
   - Acesse: https://platform.openai.com/api-keys
   - Crie uma key

2. **Configurar no `.env`**:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

3. **Custo Estimado**:
   - GPT-3.5-turbo: ~$0.50 por 1000 insights
   - GPT-4: ~$10 por 1000 insights

---

### Opção 3: **Anthropic Claude** (Pago, Qualidade Superior)

**Setup**:

1. **Obter API Key**:
   - Acesse: https://console.anthropic.com/
   - Crie conta e key

2. **Configurar no `.env`**:
   ```env
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Modelos**:
   - `claude-3-haiku-20240307` (Rápido, barato)
   - `claude-3-sonnet-20240229` (Equilibrado)
   - `claude-3-opus-20240229` (Mais inteligente)

---

### Opção 4: **Ollama Local** (Grátis, Privativo, Requer GPU)

**Setup**:

1. **Instalar Ollama**:
   ```bash
   # Windows
   winget install Ollama.Ollama

   # Ou baixe em: https://ollama.ai
   ```

2. **Baixar Modelo**:
   ```bash
   ollama pull llama3.1:8b
   ```

3. **Configurar no `.env`**:
   ```env
   LLM_PROVIDER=ollama
   ```

4. **Modelos Recomendados**:
   - `llama3.1:8b` (Leve, rápido)
   - `llama3.1:70b` (Pesado, requer 40GB+ RAM)
   - `mistral:7b` (Alternativo)

---

## 📂 ESTRUTURA NO OBSIDIAN

Com a IA configurada, uma nova pasta será criada:

```
🧠 EXOCÓRTEX/
└── 08 - AI Insights/
    ├── tenant-1/
    │   └── AI-Insights-Empresa-XYZ-20260302.md
    ├── tenant-2/
    │   └── AI-Insights-Empresa-ABC-20260302.md
    └── tenant-3/
        └── AI-Insights-Empresa-DEF-20260302.md
```

---

## 🎯 FUNCIONALIDADES DE IA

### 1. **Insights Automáticos de Anomalias**

**O que faz**: Quando uma métrica tem anomalia (Z-Score > 2), a IA gera:
- Diagnóstico da causa
- Impacto esperado
- Ações recomendadas
- Nível de confiança

**Exemplo de Insight**:

```markdown
### 🔴 🚨 CAC 120% Acima do Benchmark

**Confiança:** 87% | **Métricas:** cac

**Análise:**
O CAC atual de R$ 65,00 está 120% acima do benchmark de R$ 30,00 
para e-commerce. Isso indica ineficiência significativa na aquisição.

Possíveis causas:
1. Canais pagos saturados (CTR caindo)
2. Landing pages com conversão baixa
3. Segmentação de público inadequada

**Ações Recomendadas:**
1. [ ] Auditoria completa de canais pagos
2. [ ] Testes A/B em landing pages
3. [ ] Revisar segmentação de campanhas
4. [ ] Implementar retargeting
```

**Como ativar**:
- Automático (background task a cada 5 minutos)
- Ou manual via webhook

---

### 2. **Relatórios Semanais Automáticos**

**O que faz**: Gera relatório executivo em formato de newsletter

**Exemplo**:

```markdown
# Relatório Semanal - Empresa XYZ

## 📊 Resumo Executivo
A semana teve desempenho misto com receita crescendo 12% mas CAC 
aumentando 18%. Conversão melhorou após otimização das landing pages.

## 🎯 Insights Principais
- Receita cresceu 12% WoW, impulsionada por campanha Black Friday
- CAC subiu 18% devido a maior competição no Google Ads
- Conversão melhorou de 1.8% para 2.3% após testes A/B
- Churn reduziu de 6% para 4.5% com novo onboarding

## ⚠️ Pontos de Atenção
- CAC 120% acima do benchmark requer ação imediata
- ROAS do Facebook Ads caiu para 2.1x (abaixo de 3.5x)

## 📋 Recomendações
1. Otimizar campanhas de paid search (foco em long-tail keywords)
2. Escalar budget de email marketing (ROAS 10x)
3. Implementar programa de referral para reduzir CAC
```

**Uso manual**:

```python
from src.ai_insights import AIInsightsEngine

ai = AIInsightsEngine()

report = ai.generate_weekly_report(
    tenant_name='Empresa XYZ',
    metrics_summary={'revenue': 50000, 'cac': 65, 'ltv': 350},
    wow_comparison={'revenue': 12.5, 'cac': -8.2, 'ltv': 3.1},
    start_date='2026-02-24',
    end_date='2026-03-02'
)

print(report)
```

---

### 3. **Ideias de Conteúdo**

**O que faz**: Gera 10 ideias de conteúdo criativas

**Exemplo**:

```json
{
  "ideas": [
    {
      "title": "Guia Completo: Como Reduzir CAC em 50%",
      "format": "blog",
      "channel": "linkedin",
      "briefing": "Artigo de 2000 palavras com 10 estratégias testadas",
      "cta": "Baixe planilha de cálculo de CAC",
      "estimated_effort": "high",
      "expected_impact": "high"
    },
    {
      "title": "Case: Aumentamos Conversão de 1.8% para 3.5%",
      "format": "video",
      "channel": "youtube",
      "briefing": "Vídeo de 15 min mostrando o processo passo a passo",
      "cta": "Agende consultoria gratuita",
      "estimated_effort": "medium",
      "expected_impact": "high"
    }
  ]
}
```

**Uso manual**:

```python
ideas = ai.generate_content_ideas(
    tenant_name='Empresa XYZ',
    niche='E-commerce de Moda',
    target_audience='Mulheres 25-45 anos, classe AB',
    content_goal='Geração de leads',
    keywords=['moda feminina', 'tendências', 'e-commerce'],
    channels=['instagram', 'linkedin', 'blog']
)
```

---

### 4. **Chat Contextual com Seus Dados**

**O que faz**: Responde perguntas usando contexto do vault + Supabase

**Exemplo de Uso no Obsidian Copilot**:

```
Usuário: "Qual o CAC atual da Empresa XYZ e como está vs benchmark?"

Copilot: [Busca no vault + Supabase]

O CAC atual da Empresa XYZ é R$ 65,00, que está 120% acima do 
benchmark de R$ 30,00 para e-commerce.

**Histórico (últimos 30 dias)**:
- 01/03: R$ 62,00
- 02/03: R$ 68,00
- 03/03: R$ 65,00

**Recomendações**:
1. Auditoria de canais pagos
2. Otimização de landing pages
3. Implementar retargeting

Quer que eu gere um plano de ação detalhado?
```

**API para Chat**:

```python
response = ai.chat_with_context(
    question="Qual o LTV atual e como melhorar?",
    context={
        'tenant_name': 'Empresa XYZ',
        'current_ltv': 350,
        'benchmark_ltv': 600
    },
    vault_context=[
        "LTV melhorou 15% após programa de fidelidade",
        "Ticket médio: R$ 175, Compra recorrente: 2x/mês"
    ]
)

print(response.message)
print(response.follow_up_questions)
```

---

## 🔌 INTEGRAÇÃO COM OBSIDIAN COPILIT

### Plugin Obsidian Copilot

O plugin Copilot do Obsidian pode ser configurado para:

1. **Usar a mesma API key** que o Marketing Engine
2. **Acessar insights gerados** automaticamente
3. **Chat com RAG** no seu vault

**Configuração no Obsidian**:

1. Instalar plugin "Copilot"
2. Settings → Copilot → API Key
3. Colocar a MESMA key do `.env`
4. Habilitar "Local LLM" se usar Ollama

**Comandos Úteis no Copilot**:

```
Ctrl+P → "Copilot: Chat"

Prompt: "Mostre insights críticos de todos os tenants"
Prompt: "Gere relatório semanal para Empresa XYZ"
Prompt: "Quais anomalias foram detectadas hoje?"
Prompt: "Crie plano de ação para reduzir CAC"
```

---

## 📋 PROMPTS PRONTOS

### Prompt: Análise de Anomalia

```
Você é um especialista em marketing analytics. Analise esta anomalia:

**Métrica**: [nome da métrica]
**Valor Atual**: [valor]
**Benchmark**: [valor]
**Desvio**: [X]%

Contexto: [tipo de negócio, tamanho, etc.]

Gere um insight acionável com:
1. Causa raiz provável
2. Impacto no negócio
3. 3-5 ações imediatas
4. Como prevenir no futuro
```

### Prompt: Estratégia de Marketing

```
Você é um estrategista de marketing sênior. Crie estratégia para:

**Empresa**: [nome]
**Nicho**: [nicho]
**Métricas Atuais**: [lista de métricas]
**Problemas**: [lista de problemas]

Desenvolva:
1. Diagnóstico situacional (SWOT)
2. Objetivo SMART
3. 3-5 iniciativas estratégicas
4. KPIs de sucesso
5. Timeline e budget
```

### Prompt: Relatório Executivo

```
Você é um analista de marketing. Gere relatório semanal:

**Período**: [datas]
**Empresa**: [nome]
**Métricas**: [tabela com valores]
**WoW**: [comparação semana anterior]

Formato: Newsletter executiva com:
- Resumo em 1 parágrafo
- 3-5 insights principais
- Recomendações para próxima semana
```

---

## 🚀 EXEMPLOS DE USO

### Exemplo 1: Insight Automático de Anomalia

```python
from src.ai_insights import AIInsightsEngine, LLMProvider

# Inicializar
ai = AIInsightsEngine(
    llm_provider=LLMProvider.GROQ,
    api_key='gsk-your-key'
)

# Gerar insight
insight = ai.generate_insight_from_anomaly(
    metric_key='cac',
    current_value=65.0,
    expected_value=30.0,
    z_score=3.5,
    tenant_name='Empresa XYZ',
    tenant_type='ecommerce',
    historical_data=[
        {'date': '2026-02-24', 'value': 58},
        {'date': '2026-02-25', 'value': 62},
        {'date': '2026-02-26', 'value': 68},
        {'date': '2026-02-27', 'value': 65}
    ]
)

print(f"Título: {insight.title}")
print(f"Severidade: {insight.severity}")
print(f"Ações: {insight.action_items}")
```

---

### Exemplo 2: Relatório Semanal

```python
report = ai.generate_weekly_report(
    tenant_name='Empresa XYZ',
    metrics_summary={
        'revenue': 52000,
        'cac': 58,
        'ltv': 380,
        'conversion_rate': 2.4,
        'churn_rate': 4.2
    },
    wow_comparison={
        'revenue': 8.5,
        'cac': -5.2,
        'ltv': 4.1,
        'conversion_rate': 12.5,
        'churn_rate': -15.3
    },
    start_date='2026-02-24',
    end_date='2026-03-02'
)

# Salvar ou enviar por email
with open('relatorio-semanal.md', 'w') as f:
    f.write(report)
```

---

### Exemplo 3: Ideias de Conteúdo

```python
ideas = ai.generate_content_ideas(
    tenant_name='Empresa XYZ',
    niche='E-commerce de Moda Sustentável',
    target_audience='Mulheres 25-40, classe AB, conscientes',
    content_goal='Brand awareness + geração de leads',
    keywords=['moda sustentável', 'eco-friendly', 'slow fashion'],
    channels=['instagram', 'pinterest', 'blog', 'email']
)

for idea in ideas:
    print(f"📝 {idea['title']}")
    print(f"   Formato: {idea['format']}")
    print(f"   Canal: {idea['channel']}")
    print(f"   CTA: {idea['cta']}")
    print()
```

---

## 💡 WORKFLOW RECOMENDADO

### Daily (Todo Dia)

1. **Checkar AI Insights** no Obsidian
2. **Resolver críticos** (🔴) primeiro
3. **Mover tarefas** para "Hoje" no Kanban

### Weekly (Segunda-feira)

1. **Gerar relatório semanal** automático
2. **Revisar com time** em reunião
3. **Ajustar estratégia** baseado em insights

### Monthly (Dia 1)

1. **Gerar ideias de conteúdo** para o mês
2. **Planejar campanhas** no calendário
3. **Revisar budget** e otimizar alocação

---

## 📊 CUSTOS ESTIMADOS

### Groq (Grátis)

- **Limite**: 30 requisições/minuto, 1440/dia
- **Custo**: R$ 0
- **Ideal para**: Uso diário, insights automáticos

### OpenAI

- **GPT-3.5-turbo**: ~$0.50 por 1000 insights
- **GPT-4**: ~$10 por 1000 insights
- **Ideal para**: Relatórios executivos, estratégias complexas

### Anthropic

- **Claude Haiku**: ~$0.25 por 1000 insights
- **Claude Sonnet**: ~$3 por 1000 insights
- **Ideal para**: Análise qualitativa, conteúdo criativo

### Ollama Local

- **Custo**: R$ 0 (já tem hardware)
- **Ideal para**: Privacidade total, uso intensivo

---

## 🔒 SEGURANÇA E PRIVACIDADE

### Melhores Práticas

1. **Nunca commitar `.env`** no Git
2. **Usar variáveis de ambiente** para API keys
3. **Groq/Ollama** para dados sensíveis (não envia para OpenAI)
4. **Revisar insights** antes de compartilhar

### Dados que São Enviados

- **Métricas agregadas** (não PII)
- **Nomes de tenants** (empresas, não pessoas)
- **Contexto de negócio**

**NÃO enviar**:
- Dados pessoais de clientes
- Informações financeiras sensíveis
- Segredos comerciais críticos

---

## 🎯 PRÓXIMOS PASSOS

### Setup Inicial (30 minutos)

1. [ ] Escolher provedor de LLM (recomendo Groq)
2. [ ] Obter API key
3. [ ] Adicionar ao `.env`
4. [ ] Testar com script simples
5. [ ] Configurar Obsidian Copilot com mesma key

### Primeiro Uso (1 hora)

1. [ ] Rodar `python -m mkt.engine.main`
2. [ ] Aguardar background tasks (5 min)
3. [ ] Abrir Obsidian → 🧠 EXOCÓRTEX → 08 - AI Insights
4. [ ] Revisar insights gerados
5. [ ] Mover ações para Kanban

### Workflow Semanal (30 min/semana)

1. [ ] Segunda: Gerar relatório semanal
2. [ ] Revisar com time
3. [ ] Ajustar prioridades no Kanban
4. [ ] Executar ações

---

## 📚 RECURSOS ADICIONAIS

### Documentação

- [Groq API Docs](https://console.groq.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Ollama Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

### Prompts Avançados

Ver arquivo: `PROMPTS_AI_ADVANCED.md` (em criação)

### Exemplos de Código

Ver pasta: `examples/ai_insights/` (em criação)

---

<div align="center">

**🤖 OBSIDIAN COPILIT + MARKETING ENGINE**

*v5.2 — EXOCÓRTEX COM IA GENERATIVA*

**4 provedores • 8 templates de prompt • Insights automáticos**

</div>
