# 🎯 CMO 360° v6.1 — Platform de Inteligência de Marketing

> **Sistema completo de marketing para C-Level com IA que aprende com casos reais**

[![Version](https://img.shields.io/badge/version-6.1-blue.svg)](https://github.com/yourusername/cmo-360-platform)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-production%20ready-green.svg)]()

---

## 📊 O Que É

**CMO 360°** é uma plataforma completa de inteligência de marketing que:

- ✅ **Monitora** métricas em tempo real (24/7)
- ✅ **Detecta** anomalias automaticamente (Z-Score)
- ✅ **Gera** insights acionáveis com IA
- ✅ **Aprende** com casos passados (CMO-Bench™)
- ✅ **Notifica** por e-mail/Slack/Telegram
- ✅ **Custo zero** de infra (free tiers)

---

## 🚀 Funcionalidades Principais

### **1. Detecção de Anomalias** 🔴
```
CAC subiu 120% → Z-Score 3.5 → Alerta Crítico → E-mail enviado
```

### **2. CMO-Bench™ (Aprendizado)** 🧠
```
Problema similar → Busca na base → Aplica solução → Verifica → Aprende
```

### **3. Notificações Sob Demanda** 📧
- Alertas críticos (imediatamente)
- Daily digest (18:00)
- Weekly summary (segunda 09:00)
- Custo: **R$ 0/mês**

### **4. Dashboards Automáticos** 📊
- 10 pastas especializadas no Obsidian
- CMO Executive Dashboard
- Growth & Performance
- Budget & ROI

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│  FONTES → PROCESSAMENTO → BANCO → IA → AÇÕES → OUTPUT  │
├─────────────────────────────────────────────────────────┤
│  CSV/Excel  →  Watcher  →  Supabase  →  CMO-Bench  →   │
│  APIs       →  Processor →  (8 tables) →  AI/Groq  →   │
│                              ↓                          │
│                    NotificationDispatcher               │
│                    (Email/Slack/Telegram)               │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura

```
cmo-360-platform/
├── 📂 mkt/engine/              # Motor principal
│   ├── main.py                 # Entry point
│   ├── src/                    # Módulos Python
│   │   ├── database.py
│   │   ├── processor.py
│   │   ├── watcher.py
│   │   ├── cmo_bench.py        ⭐ CMO-Bench (v6.0)
│   │   ├── notification_dispatcher.py  ⭐ E-mails (v6.1)
│   │   └── ... (15 módulos)
│   └── test_*.py               # Testes
│
├── 📂 sql/                     # Banco de dados
│   └── 01-08_create_*.sql     # Schema completo
│
├── 📂 frontend/                # Web Platform (React)
│   └── src/App.jsx
│
├── 📄 docker-compose.yml       # Docker
├── 📄 .env.example             # Template .env
└── 📚 Documentação/
    ├── CMO_360_FINAL.md
    ├── CMO_BENCH_INTELIGENCIA.md
    └── NOTIFICACOES_EMAIL_CONFIGURADAS.md
```

---

## 🚀 Quick Start

### **Opção A: Docker (Recomendado)** 🐳

```bash
# 1. Clone
git clone https://github.com/yourusername/cmo-360-platform.git
cd cmo-360-platform

# 2. Configure .env
cp .env.example .env
# Edite com suas credenciais

# 3. Deploy automático (Windows)
docker-deploy.bat

# OU deploy manual (Linux/Mac/Windows)
docker-compose up -d --build

# 4. Acesse
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

---

### **Opção B: Manual (Python)** 🐍

```bash
# 1. Clone
git clone https://github.com/yourusername/cmo-360-platform.git
cd cmo-360-platform

# 2. Configure .env
cp mkt/.env.example mkt/.env

# 3. Instale
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

pip install -r mkt/engine/requirements.txt

# 4. Suba o Banco (Supabase)
# Execute: sql/01-08_create_*.sql (na ordem)

# 5. Teste
python mkt/engine/test_notifications.py
python mkt/engine/test_ai_insights.py

# 6. Rode
python -m mkt.engine.main
```

---

## 📊 Módulos Principais

| Módulo | Versão | Função |
| :----- | :----- | :----- |
| `cmo_bench.py` | v6.0 ⭐ | Aprende com casos reais (tipo SWE-bench) |
| `notification_dispatcher.py` | v6.1 ⭐ | E-mails, Slack, Telegram |
| `ai_insights.py` | v5.2 | IA generativa (Groq/Llama-3) |
| `growth_marketing.py` | v5.3 | Growth & Performance |
| `brand_communication.py` | v5.3 | Brand Health |
| `executive_dashboard.py` | v5.3 | Dashboard C-Level |
| `budget_tracker.py` | v5.1 | Budget & ROI |
| `marketing_strategy.py` | v5.1 | Estratégias automáticas |

---

## 🗄️ Banco de Dados (8 Tabelas)

```sql
1. tenants              -- Empresas/unidades
2. marketing_assets     -- Arquivos processados
3. business_metrics     -- KPIs (CAC, LTV, ROAS, etc.)
4. anomaly_alerts       -- Alertas de anomalias
5. strategic_insights   -- Insights da IA
6. audit_logs           -- Log de auditoria
7. automation_queue     -- Fila de ações
8. knowledge_base       -- Casos aprendidos (CMO-Bench)
```

---

## 🔔 Notificações

### **Canais Suportados**

| Canal | Custo | Status |
| :---- | :---- | :----- |
| **E-mail (SMTP)** | Grátis | ✅ Pronto |
| **Slack (Webhook)** | Grátis | ✅ Pronto |
| **Telegram (Bot)** | Grátis | ✅ Pronto |
| **WhatsApp (Twilio)** | $0.005/msg | ✅ Pronto |
| **Push (Firebase)** | Grátis | ✅ Pronto |

### **Tipos de E-mail**

1. **Alerta Crítico** — HTML rico, métricas em destaque
2. **Daily Digest** — Resumo diário (18:00)
3. **Weekly Summary** — Resumo semanal (segunda 09:00)

---

## 💰 Custos de Infra

| Serviço | Plano | Custo |
| :------ | :---- | :---- |
| **Supabase** | Free | R$ 0/mês |
| **Groq** | Free | R$ 0/mês |
| **Gmail** | Free | R$ 0/mês |
| **Redis** | Included | R$ 0/mês |
| **Total** | | **R$ 0/mês** |

---

## 📈 Roadmap

| Versão | Status | Funcionalidades |
| :----- | :----- | :-------------- |
| **v5.0** | ✅ | Core (Watcher, Processor, Obsidian) |
| **v5.1** | ✅ | Planning (Strategy, Goals, Calendar, Budget) |
| **v5.2** | ✅ | AI (Groq, Insights) |
| **v5.3** | ✅ | CMO 360° (Growth, Brand, Dashboard) |
| **v6.0** | ✅ | CMO-Bench (Aprendizado) |
| **v6.1** | ✅ | Notifications (Email, Slack, Telegram) |
| **v7.0** | 🔄 | Web Platform (React + Docker) |
| **v8.0** | 🔄 | APIs (Google Ads, Meta, GA4) |

---

## 🧪 Testes

```bash
# Testar notificações
python mkt/engine/test_notifications.py

# Testar IA
python mkt/engine/test_ai_insights.py

# Testar conexão Supabase
python mkt/engine/test_supabase_connection.py
```

---

## 📚 Documentação

| Arquivo | Descrição |
| :------ | :-------- |
| `CMO_360_FINAL.md` | Visão geral completa |
| `CMO_BENCH_INTELIGENCIA.md` | CMO-Bench (aprendizado) |
| `NOTIFICACOES_EMAIL_CONFIGURADAS.md` | Notificações por e-mail |
| `CONFIG_EMAIL.md` | Configuração de e-mail |
| `README_WEB_PLATFORM.md` | Web Platform (Docker) |

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Pull Request

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/yourprofile)

---

## 🙏 Agradecimentos

- [Supabase](https://supabase.com) - Banco de dados
- [Groq](https://groq.com) - IA rápida e grátis
- [SWE-bench](https://www.swebench.com) - Inspiração para CMO-Bench
- [Obsidian](https://obsidian.md) - Dashboards

---

<div align="center">

**🚀 CMO 360° v6.1**

*Inteligência de Marketing para C-Level*

[Report Bug](https://github.com/yourusername/cmo-360-platform/issues) · [Request Feature](https://github.com/yourusername/cmo-360-platform/issues)

</div>
