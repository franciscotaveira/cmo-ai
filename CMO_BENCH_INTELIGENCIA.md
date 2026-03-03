# 🧠 CMO-BENCH — INTELIGÊNCIA TIPO SWE-BENCH

> **Versão**: 6.0  
> **Inspiração**: SWE-bench (AI Software Engineering Benchmark)  
> **Status**: ✅ Implementado  
> **Diferencial**: Aprende com casos reais, verifica ações, melhora continuamente

---

## 📊 **O QUE É CMO-BENCH**

**CMO-Bench** aplica os mesmos padrões do **SWE-bench** (o benchmark mais avançado para IA em engenharia de software) ao **marketing**.

### **Analogia Direta**

| SWE-bench | CMO-Bench |
| :-------- | :-------- |
| Issue do GitHub | Problema de marketing (ex: "CAC subiu 40%") |
| Codebase completo | Dados completos do negócio |
| Gold patch | Ação ideal baseada em casos reais |
| Testes unitários | Métricas de verificação |
| Pass/Fail | Resolveu/Não resolveu |
| Aprendizado | Base de casos resolvidos |

---

## 🔥 **COMO FUNCIONA**

### **Fluxo Completo**

```
┌─────────────────────────────────────────────────────────────────┐
│  CMO-BENCH PROCESS                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ISSUE DETECTED                                              │
│     "CAC 120% acima do benchmark"                               │
│                                                                 │
│  2. RETRIEVE FULL CONTEXT                                       │
│     • Métricas atuais e históricas                              │
│     • Ações passadas e resultados                               │
│     • Cases similares de outros tenants                         │
│     • Fatores externos (sazonalidade, mercado)                  │
│                                                                 │
│  3. FIND SIMILAR CASES                                          │
│     Busca na base de casos resolvidos                           │
│     "E-commerce A teve mesmo problema, resolveu assim..."       │
│                                                                 │
│  4. GENERATE ACTION                                             │
│     Combina aprendizado + IA                                    │
│     "Reduzir Meta Ads 40%, aumentar Google Ads 30%"             │
│                                                                 │
│  5. EXECUTE ACTION                                              │
│     Integra com APIs (Google, Meta, etc.)                       │
│                                                                 │
│  6. VERIFY SUCCESS (como testes)                                │
│     Aguarda 14 dias                                             │
│     Compara métricas antes/depois                               │
│     "CAC reduziu 25%? ✅ Resolveu!"                             │
│                                                                 │
│  7. LEARN                                                       │
│     Adiciona caso resolvido à base                              │
│     Próxima vez será mais rápido e preciso                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💡 **DIFERENCIAIS DE INTELIGÊNCIA**

### **1. Contexto Completo (não apenas métricas isoladas)**

**Antes (v5.3)**:
```python
{
    "cac": 65.0,
    "ltv": 350.0,
    "roas": 2.5
}
```

**Agora (v6.0 - CMO-Bench)**:
```python
{
    "issue": {
        "title": "CAC 120% acima do benchmark",
        "description": "CAC subiu de R$ 30 para R$ 65 em 2 semanas",
        "severity": "critical",
        "metrics_involved": ["cac", "roas", "meta_ads_spend"]
    },
    "full_context": {
        "tenant": {"type": "ecommerce", "size": "medium"},
        "historical": {
            "cac_30d": [45, 48, 52, 58, 65],
            "ltv_30d": [340, 345, 350, 355, 350],
            "roas_by_channel": {
                "google_ads": 5.2,
                "meta_ads": 2.1,
                "email": 10.0
            }
        },
        "past_actions": [
            {"date": "2026-02-15", "action": "Aumentou budget Meta Ads", "result": "CAC subiu"},
            {"date": "2026-02-20", "action": "Pausou Google Ads", "result": "Leads caíram"}
        ],
        "external_factors": {
            "seasonality": "Black Friday approaching",
            "market_changes": "iOS privacy changes",
            "competitor_actions": "Concorrente X lançou promoção"
        }
    }
}
```

---

### **2. Verificação Executável (como testes)**

**Antes (v5.3)**:
```python
# Insight gerado, sem validação
{
    "insight": "Otimize Meta Ads",
    "confidence": 0.75
}
```

**Agora (v6.0 - CMO-Bench)**:
```python
# Verificação tipo teste unitário
{
    "action_plan": {
        "actions": [
            {"type": "reduce_budget", "channel": "meta_ads", "change": -0.4},
            {"type": "increase_budget", "channel": "google_ads", "change": 0.3}
        ]
    },
    "success_criteria": {
        "cac": {"type": "decrease", "threshold": 0.2},
        "roas": {"type": "increase", "threshold": 0.15}
    },
    "verification": {
        "resolved": True,  # 80%+ dos testes passaram
        "tests_passed": 4,
        "tests_total": 5,
        "details": {
            "cac_reduced": True,
            "roas_improved": True,
            "leads_stable": True,
            "revenue_maintained": True,
            "churn_not_increased": False  # 1 teste falhou
        }
    }
}
```

---

### **3. Gold Standard Learning**

**Antes (v5.3)**:
```python
# Cada insight é novo, sem aprendizado
IA gera insight → Ninguém valida → Mesmo erro repetido
```

**Agora (v6.0 - CMO-Bench)**:
```python
# Base de casos resolvidos (como gold patches)
knowledge_base = {
    "cases": [
        {
            "issue": "CAC 120% acima no Meta Ads",
            "action": "Reduzir budget 40%, migrar para Google Ads",
            "result": "resolved",
            "metrics_before": {"cac": 65, "roas": 2.1},
            "metrics_after": {"cac": 48, "roas": 3.2},
            "confidence": 0.87,
            "tenant_type": "ecommerce"
        },
        # ... mais casos
    ]
}

# Quando issue similar aparece:
similar_case = knowledge_base.find_similar(current_issue)
# Retorna: "E-commerce A teve mesmo problema, resolveu assim..."
```

---

### **4. Multi-File Reasoning**

**Antes (v5.3)**:
```python
# Dados fragmentados por tabela
tenants → business_metrics → anomaly_alerts
```

**Agora (v6.0 - CMO-Bench)**:
```python
# Conexão entre dados (como código em múltiplos arquivos)
{
    "issue": "CAC alto",
    "connected_data": {
        "tenant": "E-commerce XYZ",
        "metrics": {"cac": 65, "ltv": 350},
        "campaigns": [
            {"name": "Black Friday", "channel": "meta_ads", "performance": "poor"},
            {"name": "Evergreen", "channel": "google_ads", "performance": "excellent"}
        ],
        "past_actions": [
            {"action": "Aumentou budget Meta", "result": "CAC piorou"},
            {"action": "Pausou Google", "result": "Leads caíram 60%"}
        ],
        "seasonality": "Black Friday em 2 semanas",
        "competitors": ["Concorrente A: promoção ativa", "Concorrente B: novo produto"]
    }
}
```

---

### **5. Feedback Loop Automático**

**Antes (v5.3)**:
```
IA gera insight → Humano executa → Sem feedback → IA não aprende
```

**Agora (v6.0 - CMO-Bench)**:
```
Issue → IA + Cases → Ação → Executa → Verifica (14 dias) → Aprende
  ↑                                                        │
  └────────────────────────────────────────────────────────┘
              (base de casos resolvidos cresce)
```

---

## 🚀 **COMO USAR**

### **Exemplo Básico**

```python
from src.cmo_bench import (
    CMOLearningLoop,
    BusinessIssue,
    CMOKnowledgeBase
)

# 1. Inicializar
learning_loop = CMOLearningLoop()

# 2. Criar issue
issue = BusinessIssue(
    id="issue-001",
    title="CAC 120% acima do benchmark",
    description="CAC subiu de R$ 30 para R$ 65 em 2 semanas",
    tenant_id="ecommerce-xyz",
    tenant_type="ecommerce",
    severity="critical",
    detected_at="2026-03-02",
    metrics_involved=["cac", "roas", "meta_ads_spend"],
    external_factors={"seasonality": "black_friday"}
)

# 3. Processar issue (fluxo completo tipo SWE-bench)
result = learning_loop.process_business_issue(issue, "ecommerce-xyz")

# 4. Ver resultado
print(f"Resolveu: {result['verification'].resolved}")
print(f"Testes: {result['verification'].tests_passed}/{result['verification'].tests_total}")
print(f"Aprendeu: {result['learned']}")
```

---

### **Exemplo com Casos Similares**

```python
# 1. Adicionar caso resolvido à base
knowledge_base = CMOKnowledgeBase()

case = GoldCase(
    issue=issue_anterior,
    action_plan=action_bem_sucedida,
    verification=verification_resolved,
    confidence=0.87,
    similarity_vector=vector
)

knowledge_base.cases.append(case)

# 2. Quando issue similar aparecer
similar_cases = knowledge_base.find_similar_cases(
    current_issue,
    current_metrics,
    top_k=5
)

# 3. Usar ação do caso similar
gold_action = knowledge_base.get_gold_action(similar_cases)
# Retorna: "E-commerce A resolveu assim..."
```

---

## 📊 **MÉTRICAS DE INTELIGÊNCIA**

### **Como Medir Evolução**

| Métrica | Como Calcular | Meta |
| :------ | :------------ | :--- |
| **Resolution Rate** | Casos resolvidos / Total | > 80% |
| **Case Base Size** | Casos na base | > 100 em 30 dias |
| **Similarity Match** | Cases similares encontrados | > 3 por issue |
| **Confidence Avg** | Confiança média dos casos | > 0.75 |
| **Learning Rate** | Novos casos / dia | > 3/dia |
| **Verification Pass** | Testes que passam | > 80% |

---

## 🔧 **INTEGRAÇÃO COM SISTEMA EXISTENTE**

### **Adicionar ao Main.py**

```python
from src.cmo_bench import CMOLearningLoop, BusinessIssue

# Inicializar
cmo_bench = CMOLearningLoop(db, llm_client)

# No loop de background (a cada 5 min):
def background_tasks():
    # ... código existente ...
    
    # Processar alertas como issues do CMO-bench
    for alert in critical_alerts:
        issue = BusinessIssue(
            id=alert['id'],
            title=f"{alert['metric_key']} {alert['severity']}",
            description=f"{alert['metric_key']} está {alert['z_score']:.2f} desvios acima",
            tenant_id=alert['tenant_id'],
            tenant_type=tenant_type,
            severity=alert['severity'],
            detected_at=alert['detected_at'],
            metrics_involved=[alert['metric_key']]
        )
        
        result = cmo_bench.process_business_issue(issue, alert['tenant_id'])
        
        # Armazenar resultado
        if result['learned']:
            logger.info(f"✅ Caso aprendido: {issue.title}")
```

---

## 🎯 **COMPARAÇÃO: ANTES VS DEPOIS**

| Aspecto | v5.3 (Sem CMO-Bench) | v6.0 (Com CMO-Bench) |
| :------ | :------------------- | :------------------- |
| **Contexto** | Métricas isoladas | Contexto completo |
| **Verificação** | Sem validação | Testes executáveis |
| **Aprendizado** | Zero | Base de casos resolvidos |
| **Similaridade** | Zero | Encontra casos similares |
| **Confiança** | Fixa (0.75) | Dinâmica (baseada em resultados) |
| **Feedback** | Zero | Loop automático |
| **Evolução** | Estática | Melhora com uso |

---

## 📈 **ROADMAP DE INTELIGÊNCIA**

### **Fase 1: Implementação (Semana 1-2)** ✅
- [x] CMOKnowledgeBase
- [x] CMOVerification
- [x] CMOLearningLoop
- [ ] Integração com Supabase

### **Fase 2: Casos Reais (Semana 3-4)**
- [ ] Popular com 10-20 casos iniciais
- [ ] Definir critérios de sucesso por tipo de issue
- [ ] Configurar verificação automática (14 dias)

### **Fase 3: Aprendizado (Semana 5-6)**
- [ ] Feedback loop com métricas reais
- [ ] Similaridade mais precisa
- [ ] Ponderação automática (IA vs aprendizado)

### **Fase 4: Produção (Semana 7-8)**
- [ ] Monitoramento de resolução
- [ ] Dashboard de evolução
- [ ] Export de casos resolvidos

---

## 💡 **BENEFÍCIOS ESPERADOS**

### **Após 30 Dias de Uso**

| Benefício | Impacto |
| :-------- | :------ |
| **Resolution Rate** | 60% → 85% |
| **Tempo para Resolução** | 14 dias → 7 dias |
| **Confiança dos Insights** | 0.65 → 0.85 |
| **Cases na Base** | 0 → 50-100 |
| **Ações Bem-Sucedidas** | 40% → 75% |

---

## 🔥 **POR QUE ISSO É DIFERENTE**

### **Outras Soluções de IA para Marketing**

```
IA Genérica → Insight Genérico → Sem Validação → Mesmo Erro Repetido
```

### **CMO-Bench (Tipo SWE-bench)**

```
Issue Específica → Contexto Completo → Ação Baseada em Cases → Verificação → Aprendizado
                                              ↑
                                              │
                              Cases Similares de Outros Tenants
```

---

## 🏆 **VEREDITO**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  CMO-BENCH v6.0 — INTELIGÊNCIA TIPO SWE-BENCH                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ✅ Contexto completo (não apenas métricas)                                  ║
║  ✅ Verificação executável (como testes)                                     ║
║  ✅ Gold standard learning (cases resolvidos)                                ║
║  ✅ Multi-file reasoning (dados conectados)                                  ║
║  ✅ Feedback loop automático                                                 ║
║                                                                              ║
║  DIFERENCIAL COMPETITIVO:                                                    ║
║  • Aprende com cada caso resolvido                                           ║
║  • Encontra soluções de tenants similares                                    ║
║  • Verifica se funcionou (não apenas gera insight)                           ║
║  • Melhora continuamente com uso                                             ║
║                                                                              ║
║  STATUS: ✅ Implementado, pronto para teste com dados reais                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

<div align="center">

**🧠 CMO-BENCH v6.0**

*Aplicando SWE-bench ao Marketing*

**Implementado • Pronto para teste • Aprendizado contínuo**

</div>
