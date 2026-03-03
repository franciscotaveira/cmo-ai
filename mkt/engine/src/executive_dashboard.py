"""
╔═══════════════════════════════════════════════════════════════════════════════
║ EXECUTIVE DASHBOARD — C-Level Dashboard (v5.3 — CMO 360°)
╠═══════════════════════════════════════════════════════════════════════════════
║ Dashboard unificado para CMOs e Diretores de Marketing
║ Visão 360° de todas as áreas de marketing
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ExecutiveDashboard:
    """
    Executive Dashboard para C-Level.

    Consolida todas as áreas de marketing em um único dashboard executivo:
    • Growth & Performance
    • Brand & Communication
    • Strategy & Planning
    • Budget & Finance
    • AI Insights
    """

    def __init__(self):
        """Inicializa o Executive Dashboard."""
        logger.info("📊 ExecutiveDashboard inicializado")

    def generate_cmo_dashboard(
        self,
        tenant_name: str,
        obsidian_path: str,
        growth_data: Optional[Dict] = None,
        brand_data: Optional[Dict] = None,
        budget_data: Optional[Dict] = None,
        strategy_data: Optional[Dict] = None,
        ai_insights: Optional[List] = None
    ) -> str:
        """
        Gera dashboard executivo para CMO.

        Args:
            tenant_name: Nome do tenant/empresa
            obsidian_path: Caminho para o vault
            growth_data: Dados de growth (opcional)
            brand_data: Dados de brand (opcional)
            budget_data: Dados de budget (opcional)
            strategy_data: Dados de estratégia (opcional)
            ai_insights: Insights de IA (opcional)

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        dashboard_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "00 - Dashboards"
        )
        os.makedirs(dashboard_path, exist_ok=True)

        # Dados simulados (na prática viriam dos engines)
        growth = growth_data or self._get_mock_growth_data()
        brand = brand_data or self._get_mock_brand_data()
        budget = budget_data or self._get_mock_budget_data()
        strategies = strategy_data or self._get_mock_strategy_data()
        insights = ai_insights or self._get_mock_ai_insights()

        # Conteúdo do dashboard
        content = f"""---
tags: [dashboard, executivo, cmo, c-level, {tenant_name.lower().replace(' ', '_')}]
criado: {timestamp}
tipo: cmo_dashboard
---

# 🎯 CMO Executive Dashboard — {tenant_name}

**Atualizado em:** {timestamp}

> [!SUMMARY] Visão Geral
> Dashboard 360° de Marketing para C-Level
> • 10 áreas de marketing integradas
> • Atualização automática (5 em 5 minutos)
> • Insights de IA inclusos

---

## 📊 Scorecard Executivo

### Performance da Semana

| Área | Métrica Chave | Valor | Meta | Status |
| :--- | :------------ | :---- | :--- | :----- |
| **📈 Growth** | ROAS Médio | {growth.get('avg_roas', 0):.1f}x | 4.0x | {self._status_icon(growth.get('avg_roas', 0), 4.0)} |
| **📈 Growth** | CAC | R$ {growth.get('avg_cac', growth.get('cac', 0)):.0f} | R$ 50 | {self._status_icon(growth.get('avg_cac', growth.get('cac', 0)), 50, inverse=True)} |
| **🏛️ Brand** | Brand Equity | {brand.get('equity_score', 0):.0f}/100 | 70 | {self._status_icon(brand.get('equity_score', 0), 70)} |
| **🏛️ Brand** | NPS | {brand.get('nps', 0):.0f} | 60 | {self._status_icon(brand.get('nps', 0), 60)} |
| **🏛️ Brand** | Share of Voice | {brand.get('sov', 0):.1f}% | 25% | {self._status_icon(brand.get('sov', 0), 25)} |
| **💰 Finance** | Budget Utilizado | {budget.get('utilization', 0):.0f}% | 85% | {self._status_icon(budget.get('utilization', 0), 85, tolerance=10)} |
| **💰 Finance** | ROI Geral | {budget.get('roi', 0):.1f}x | 4.0x | {self._status_icon(budget.get('roi', 0), 4.0)} |
| **📋 Strategy** | Estratégias Ativas | {strategies.get('active_count', 0)} | 3 | {self._status_icon(strategies.get('active_count', 0), 3, tolerance=1)} |

---

## 🔴 Alertas Críticos (Ação Imediata)

"""

        # Alertas críticos
        critical_alerts = self._generate_critical_alerts(growth, brand, budget, insights)
        if critical_alerts:
            for i, alert in enumerate(critical_alerts[:5], 1):
                content += f"{i}. **{alert['title']}**\n"
                content += f"   - {alert['description']}\n"
                content += f"   - **Ação:** {alert['action']}\n\n"
        else:
            content += "> ✅ Nenhum alerta crítico no momento.\n\n"

        content += """
---

## 📈 1. Growth & Performance

"""

        # Performance por canal
        content += "### Performance por Canal\n\n"
        content += "| Canal | Spend | Receita | ROAS | CTR | Status |\n"
        content += "| :---- | :---- | :------ | :--- | :-- | :----- |\n"

        for channel in growth.get('channels', []):
            roas = channel.get('roas', 0)
            roas_status = self._status_icon(roas, 3.0)
            content += (
                f"| {channel.get('name', 'N/A')} | R$ {channel.get('spend', 0):,.0f} | "
                f"R$ {channel.get('revenue', 0):,.0f} | {roas:.2f}x | "
                f"{channel.get('ctr', 0):.2%} | {roas_status} |\n"
            )

        content += f"""
### Campanhas Ativas

| Campanha | Canal | Budget | ROAS | Progresso |
| :------- | :---- | :----- | :--- | :-------- |
"""

        for campaign in growth.get('campaigns', [])[:5]:
            progress = campaign.get('progress', 0)
            progress_bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
            content += (
                f"| {campaign.get('name', 'N/A')} | {campaign.get('channel', 'N/A')} | "
                f"R$ {campaign.get('budget', 0):,.0f} | {campaign.get('roas', 0):.2f}x | "
                f"`{progress_bar}` {progress:.0f}% |\n"
            )

        content += """
---

## 🏛️ 2. Brand & Communication

"""

        # Brand health
        content += f"""
### Brand Health

| Métrica | Valor | Tendência | Benchmark |
| :------ | :---- | :-------- | :-------- |
| **Unaided Awareness** | {brand.get('unaided_awareness', 0):.1f}% | ↑ | 30% |
| **Aided Awareness** | {brand.get('aided_awareness', 0):.1f}% | → | 60% |
| **Consideration** | {brand.get('consideration', 0):.1f}% | ↑ | 40% |
| **NPS** | {brand.get('nps', 0):.0f} | → | 60 |
| **Share of Voice** | {brand.get('sov', 0):.1f}% | ↑ | 25% |
| **Positive Sentiment** | {brand.get('positive_sentiment', 0):.1f}% | → | 70% |

### Brand Equity Score: {brand.get('equity_score', 0):.0f}/100

"""

        # Social sentiment
        content += "### Social Sentiment\n\n"
        sentiment = brand.get('sentiment_distribution', {})
        content += f"""
| Positivo 😊 | Neutro 😐 | Negativo 😠 |
| :---------: | :-------: | :---------: |
| {sentiment.get('positive', 0):.1f}% | {sentiment.get('neutral', 0):.1f}% | {sentiment.get('negative', 0):.1f}% |

"""

        content += """
---

## 💰 3. Budget & Finance

"""

        # Budget allocation
        content += f"""
### Budget do Mês

| Métrica | Valor |
| :------ | :---- |
| **Budget Total** | R$ {budget.get('total', 0):,} |
| **Gasto** | R$ {budget.get('spent', 0):,} |
| **Restante** | R$ {budget.get('remaining', 0):,} |
| **Utilização** | {budget.get('utilization', 0):.1f}% |
| **Receita Atribuída** | R$ {budget.get('revenue', 0):,} |
| **ROI Geral** | {budget.get('roi', 0):.2f}x |

### Alocação por Canal

| Canal | Budget | Gasto | ROAS | Eficiência |
| :---- | :----- | :---- | :--- | :--------- |
"""

        for alloc in budget.get('allocations', []):
            roas = alloc.get('roas', 0)
            efficiency = '🟢' if roas >= 4 else '🟡' if roas >= 2.5 else '🔴'
            content += (
                f"| {alloc.get('channel', 'N/A')} | R$ {alloc.get('budget', 0):,.0f} | "
                f"R$ {alloc.get('spent', 0):,.0f} | {roas:.2f}x | {efficiency} |\n"
            )

        content += """
---

## 📋 4. Estratégia & Planning

"""

        # Estratégias ativas
        content += "### Estratégias Ativas\n\n"
        for strat in strategies.get('active', [])[:5]:
            content += f"- **{strat['name']}** ({strat['type']})\n"
            content += f"  - Status: {strat['status']} | Progresso: {strat['progress']:.0f}%\n"

        content += "\n### Metas do Trimestre\n\n"
        for goal in strategies.get('goals', [])[:5]:
            check = "✅" if goal['progress'] >= 100 else "🟡" if goal['progress'] >= 70 else "⏳"
            content += f"- {check} **{goal['name']}**: {goal['progress']:.0f}% (meta: {goal['target']})\n"

        content += """
---

## 🤖 5. AI Insights

"""

        # Insights de IA
        if insights:
            content += "### Últimos Insights\n\n"
            for insight in insights[:5]:
                icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(insight['severity'], '⚪')
                content += f"- {icon} **{insight['title']}**\n"
                content += f"  - {insight['description'][:150]}...\n"
        else:
            content += "> ✅ Sem novos insights de IA.\n"

        content += """
---

## 📅 Próximas Ações (Esta Semana)

- [ ] Revisar performance de canais com ROAS baixo
- [ ] Aprovar budget adicional para campanhas performáticas
- [ ] Analisar insights críticos de IA
- [ ] Reunião com team leads (segunda-feira)
- [ ] Revisar brand health mensal

---

## 📊 Dataview Queries

### Todos os Dashboards

```dataview
TABLE tipo as "Tipo", criado as "Criado"
FROM "🧠 EXOCÓRTEX/00 - Dashboards"
WHERE contains(tags, "dashboard")
SORT criado DESC
LIMIT 10
```

### Alertas Críticos

```dataview
LIST
FROM "🧠 EXOCÓRTEX/02 - Alertas Críticos"
WHERE severity = "critical" AND status != "resolved"
SORT created DESC
```

### Estratégias Ativas

```dataview
TABLE type as "Tipo", status as "Status", progress as "Progresso"
FROM "🧠 EXOCÓRTEX/04 - Estratégias"
WHERE status = "ativa"
SORT priority DESC
```

---

## 🎯 Recomendações do CMO

"""

        # Gerar recomendações
        recommendations = self._generate_cmo_recommendations(growth, brand, budget, insights)
        for i, rec in enumerate(recommendations[:5], 1):
            content += f"{i}. {rec}\n"

        content += f"""
---

*Gerado automaticamente pelo Exocórtex v5.3 — CMO 360° Executive Dashboard*

**Próxima atualização:** Automática (5 minutos)

"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"🌍 CMO-Dashboard-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(dashboard_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📊 CMO Dashboard escrito no Obsidian: {filepath}")
        return filepath

    def _status_icon(
        self,
        value: float,
        target: float,
        inverse: bool = False,
        tolerance: float = 0.1
    ) -> str:
        """Retorna ícone de status baseado na performance vs meta."""
        if inverse:
            # Menor é melhor (ex: CAC)
            if value <= target * (1 - tolerance):
                return "🟢"
            elif value <= target:
                return "🟡"
            else:
                return "🔴"
        else:
            # Maior é melhor (ex: ROAS, NPS)
            if value >= target * (1 + tolerance):
                return "🟢"
            elif value >= target * (1 - tolerance):
                return "🟡"
            else:
                return "🔴"

    def _get_mock_growth_data(self) -> Dict[str, Any]:
        """Retorna dados mock de growth (na prática viria do engine)."""
        return {
            'avg_roas': 3.8,
            'cac': 52,
            'channels': [
                {'name': 'Google Ads', 'spend': 5000, 'revenue': 26000, 'roas': 5.2, 'ctr': 0.045},
                {'name': 'Meta Ads', 'spend': 4000, 'revenue': 10000, 'roas': 2.5, 'ctr': 0.018},
                {'name': 'LinkedIn Ads', 'spend': 3000, 'revenue': 9000, 'roas': 3.0, 'ctr': 0.012},
                {'name': 'Email', 'spend': 500, 'revenue': 5000, 'roas': 10.0, 'ctr': 0.035}
            ],
            'campaigns': [
                {'name': 'Black Friday', 'channel': 'Meta Ads', 'budget': 10000, 'roas': 2.5, 'progress': 65},
                {'name': 'Brand Awareness', 'channel': 'LinkedIn', 'budget': 5000, 'roas': 3.0, 'progress': 40},
                {'name': 'Retargeting', 'channel': 'Google Ads', 'budget': 3000, 'roas': 6.2, 'progress': 80}
            ]
        }

    def _get_mock_brand_data(self) -> Dict[str, Any]:
        """Retorna dados mock de brand (na prática viria do engine)."""
        return {
            'equity_score': 74,
            'nps': 64,
            'sov': 28.5,
            'unaided_awareness': 38.0,
            'aided_awareness': 72.0,
            'consideration': 45.0,
            'positive_sentiment': 72.0,
            'sentiment_distribution': {
                'positive': 72.0,
                'neutral': 20.0,
                'negative': 8.0
            }
        }

    def _get_mock_budget_data(self) -> Dict[str, Any]:
        """Retorna dados mock de budget (na prática viria do engine)."""
        return {
            'total': 50000,
            'spent': 43500,
            'remaining': 6500,
            'utilization': 87.0,
            'revenue': 182000,
            'roi': 4.18,
            'allocations': [
                {'channel': 'Google Ads', 'budget': 15000, 'spent': 14500, 'roas': 5.2},
                {'channel': 'Meta Ads', 'budget': 12000, 'spent': 11000, 'roas': 2.5},
                {'channel': 'LinkedIn', 'budget': 10000, 'spent': 8500, 'roas': 3.0},
                {'channel': 'Email', 'budget': 2000, 'spent': 1800, 'roas': 10.0},
                {'channel': 'Outros', 'budget': 11000, 'spent': 7700, 'roas': 2.8}
            ]
        }

    def _get_mock_strategy_data(self) -> Dict[str, Any]:
        """Retorna dados mock de estratégia (na prática viria do engine)."""
        return {
            'active_count': 4,
            'active': [
                {'name': 'Otimização de CAC', 'type': 'growth', 'status': 'em execução', 'progress': 65},
                {'name': 'Brand Awareness Q1', 'type': 'brand', 'status': 'em execução', 'progress': 45},
                {'name': 'Expansão LinkedIn', 'type': 'channel', 'status': 'em execução', 'progress': 80},
                {'name': 'Programa de Fidelidade', 'type': 'retention', 'status': 'planejada', 'progress': 20}
            ],
            'goals': [
                {'name': 'Reduzir CAC em 20%', 'progress': 65, 'target': 'R$ 40'},
                {'name': 'Aumentar NPS para 70', 'progress': 80, 'target': '70'},
                {'name': 'ROAS médio 4.0x', 'progress': 90, 'target': '4.0x'},
                {'name': 'SOV 30%', 'progress': 75, 'target': '30%'}
            ]
        }

    def _get_mock_ai_insights(self) -> List[Dict[str, Any]]:
        """Retorna insights mock de IA (na prática viria do engine)."""
        return [
            {
                'title': 'CAC 120% acima do benchmark',
                'description': 'O CAC atual está significativamente acima do benchmark do setor. Recomenda-se otimização imediata de canais.',
                'severity': 'critical'
            },
            {
                'title': 'Oportunidade: Escalar Google Ads',
                'description': 'Google Ads com ROAS 5.2x e budget limitado. Oportunidade de escala com ROI positivo.',
                'severity': 'high'
            },
            {
                'title': 'Brand Awareness em crescimento',
                'description': 'Unaided awareness cresceu 5% no mês. Campanha de brand está funcionando.',
                'severity': 'low'
            }
        ]

    def _generate_critical_alerts(
        self,
        growth: Dict,
        brand: Dict,
        budget: Dict,
        insights: List
    ) -> List[Dict[str, Any]]:
        """Gera alertas críticos baseados nos dados."""
        alerts = []

        # Check growth
        avg_roas = growth.get('avg_roas', 0)
        if avg_roas < 2.5:
            alerts.append({
                'title': 'ROAS Médio Crítico',
                'description': f"ROAS médio de {avg_roas:.2f}x está abaixo do mínimo aceitável (2.5x)",
                'action': 'Revisar alocação de budget e otimizar campanhas'
            })

        cac = growth.get('avg_cac', growth.get('cac', 0))
        if cac > 80:
            alerts.append({
                'title': 'CAC Muito Elevado',
                'description': f"CAC de R$ {cac:.0f} está 60%+ acima do benchmark",
                'action': 'Auditoria urgente de canais e funnel de conversão'
            })

        # Check brand
        nps = brand.get('nps', 0)
        if nps < 40:
            alerts.append({
                'title': 'NPS Baixo',
                'description': f"NPS de {nps:.0f} indica insatisfação significativa de clientes",
                'action': 'Implementar programa de melhoria de experiência'
            })

        # Check budget
        utilization = budget.get('utilization', 0)
        if utilization > 95:
            alerts.append({
                'title': 'Budget Quase Esgotado',
                'description': f"{utilization:.0f}% do budget já utilizado",
                'action': 'Revisar performance e solicitar budget adicional se necessário'
            })

        # Check AI insights
        for insight in insights:
            if insight.get('severity') == 'critical':
                alerts.append({
                    'title': f"AI Alert: {insight['title']}",
                    'description': insight['description'],
                    'action': 'Ver insight completo em AI Insights'
                })

        return alerts

    def _generate_cmo_recommendations(
        self,
        growth: Dict,
        brand: Dict,
        budget: Dict,
        insights: List
    ) -> List[str]:
        """Gera recomendações estratégicas para o CMO."""
        recommendations = []

        # Baseado em growth
        channels = growth.get('channels', [])
        if channels:
            best_channel = max(channels, key=lambda x: x.get('roas', 0))
            if best_channel.get('roas', 0) > 4:
                recommendations.append(
                    f"🟢 Escalar {best_channel.get('name', 'Canal')}: ROAS {best_channel.get('roas', 0):.2f}x com budget limitado"
                )

            worst_channel = min(channels, key=lambda x: x.get('roas', 0))
            if worst_channel.get('roas', 0) < 3:
                recommendations.append(
                    f"🔴 Otimizar {worst_channel.get('name', 'Canal')}: ROAS {worst_channel.get('roas', 0):.2f}x abaixo da meta"
                )

        # Baseado em brand
        nps = brand.get('nps', 0)
        if nps >= 60:
            recommendations.append(
                "💚 NPS forte — implementar programa de advocacy e referral"
            )

        # Baseado em budget
        utilization = budget.get('utilization', 0)
        if utilization < 70:
            recommendations.append(
                "💰 Budget sub-utilizado — acelerar campanhas ou revisar alocação"
            )

        # Baseado em insights
        high_severity = [i for i in insights if i.get('severity') in ['critical', 'high']]
        if high_severity:
            recommendations.append(
                f"🤖 {len(high_severity)} insights críticos/altos para revisão imediata"
            )

        if not recommendations:
            recommendations.append("✅ Performance geral dentro do esperado")

        return recommendations
