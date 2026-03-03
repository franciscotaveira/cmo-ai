"""
╔═══════════════════════════════════════════════════════════════════════════════
║ BUDGET & ROI TRACKER — Gestão de Orçamento (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Gerencia budget por canal, calcula ROI e otimiza alocação
║ Integra com Obsidian para relatórios financeiros
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ChannelType(Enum):
    """Tipos de canal de marketing."""
    PAID_SEARCH = "paid_search"  # Google Ads
    PAID_SOCIAL = "paid_social"  # Facebook, Instagram, LinkedIn Ads
    DISPLAY = "display"  # Display/Programmatic
    VIDEO = "video"  # YouTube, TikTok Ads
    NATIVE = "native"  # Taboola, Outbrain
    AFFILIATE = "affiliate"  # Afiliados
    EMAIL = "email"  # Email Marketing
    CONTENT = "content"  # Produção de conteúdo
    SEO = "seo"  # SEO (investimento em produção/link building)
    EVENTS = "events"  # Eventos e patrocínios
    INFLUENCER = "influencer"  # Influenciadores
    OTHER = "other"


@dataclass
class ChannelBudget:
    """Orçamento por canal."""
    channel: str
    channel_type: str
    allocated_budget: float
    spent_budget: float
    remaining_budget: float
    roas: float
    cpa: float
    conversions: int
    revenue: float
    efficiency_score: float  # 0-100
    recommendation: str


@dataclass
class CampaignROI:
    """ROI de campanha."""
    campaign_id: str
    campaign_name: str
    total_investment: float
    total_revenue: float
    gross_profit: float
    roi_percentage: float
    roi_multiple: float
    payback_days: int
    npv: float  # Valor presente líquido
    irr: float  # Taxa interna de retorno


@dataclass
class BudgetAllocation:
    """Alocação de budget recomendada."""
    channel: str
    current_budget: float
    recommended_budget: float
    change_percentage: float
    change_direction: str  # increase, decrease, maintain
    rationale: str
    expected_impact: str


class BudgetTracker:
    """
    Budget & ROI Tracker.

    Gerencia:
    • Alocação de budget por canal
    • Cálculo de ROI/ROAS
    • Otimização de budget
    • Previsão de receita
    """

    # Benchmarks de ROAS por canal
    ROAS_BENCHMARKS = {
        ChannelType.PAID_SEARCH.value: {'roas': 4.0, 'cpa': 50},
        ChannelType.PAID_SOCIAL.value: {'roas': 3.5, 'cpa': 40},
        ChannelType.DISPLAY.value: {'roas': 2.0, 'cpa': 80},
        ChannelType.VIDEO.value: {'roas': 3.0, 'cpa': 60},
        ChannelType.NATIVE.value: {'roas': 2.5, 'cpa': 70},
        ChannelType.AFFILIATE.value: {'roas': 5.0, 'cpa': 30},
        ChannelType.EMAIL.value: {'roas': 10.0, 'cpa': 5},
        ChannelType.CONTENT.value: {'roas': 4.0, 'cpa': 100},
        ChannelType.SEO.value: {'roas': 6.0, 'cpa': 80},
        ChannelType.EVENTS.value: {'roas': 3.0, 'cpa': 200},
        ChannelType.INFLUENCER.value: {'roas': 3.5, 'cpa': 90},
        ChannelType.OTHER.value: {'roas': 2.5, 'cpa': 100}
    }

    # Pesos para score de eficiência
    EFFICIENCY_WEIGHTS = {
        'roas': 0.4,
        'volume': 0.3,
        'consistency': 0.2,
        'trend': 0.1
    }

    def __init__(self):
        """Inicializa o Budget Tracker."""
        self.channel_budgets: Dict[str, ChannelBudget] = {}
        self.campaign_rois: Dict[str, CampaignROI] = {}
        logger.info("💰 BudgetTracker inicializado")

    def allocate_budget(
        self,
        total_budget: float,
        historical_performance: Dict[str, Dict[str, float]],
        strategy: str = 'performance'
    ) -> List[BudgetAllocation]:
        """
        Aloca budget por canal baseado em performance.

        Args:
            total_budget: Budget total disponível
            historical_performance: Performance histórica por canal
                {channel: {'roas': x, 'spend': y, 'revenue': z}}
            strategy: Estratégia de alocação (performance, balanced, aggressive)

        Returns:
            Lista de alocações recomendadas
        """
        allocations = []

        # Calcular scores por canal
        channel_scores = self._calculate_channel_scores(historical_performance)

        # Estratégia de alocação
        if strategy == 'balanced':
            # Distribuição mais igualitária
            allocations = self._balanced_allocation(
                total_budget, channel_scores, historical_performance
            )
        elif strategy == 'aggressive':
            # Foco máximo nos melhores canais
            allocations = self._aggressive_allocation(
                total_budget, channel_scores, historical_performance
            )
        else:  # performance
            # Balanceado com viés de performance
            allocations = self._performance_allocation(
                total_budget, channel_scores, historical_performance
            )

        logger.info(f"💰 Alocação de budget calculada: {len(allocations)} canais")
        return allocations

    def calculate_channel_roi(
        self,
        channel: str,
        spend: float,
        revenue: float,
        period_days: int = 30
    ) -> ChannelBudget:
        """
        Calcula ROI e métricas de um canal.

        Args:
            channel: Nome do canal
            spend: Valor gasto
            revenue: Receita gerada
            period_days: Período em dias

        Returns:
            ChannelBudget: Métricas do canal
        """
        # Calcular métricas básicas
        roas = revenue / spend if spend > 0 else 0
        profit = revenue - spend
        roi_percentage = (profit / spend * 100) if spend > 0 else 0

        # Obter benchmark
        benchmark = self.ROAS_BENCHMARKS.get(
            channel,
            self.ROAS_BENCHMARKS[ChannelType.OTHER.value]
        )

        # Calcular CPA estimado (assumindo ticket médio)
        avg_order_value = revenue / max(1, spend / benchmark['cpa'])
        cpa = spend / max(1, revenue / avg_order_value) if revenue > 0 else 0

        # Calcular conversões estimadas
        conversions = int(revenue / avg_order_value) if avg_order_value > 0 else 0

        # Calcular score de eficiência
        efficiency_score = self._calculate_efficiency_score(
            roas=roas,
            benchmark_roas=benchmark['roas'],
            spend=spend,
            trend='stable'  # Simplificado
        )

        # Gerar recomendação
        recommendation = self._generate_channel_recommendation(
            channel=channel,
            roas=roas,
            benchmark_roas=benchmark['roas'],
            efficiency_score=efficiency_score
        )

        remaining_budget = 0  # Será definido na alocação

        channel_budget = ChannelBudget(
            channel=channel,
            channel_type=channel,
            allocated_budget=spend,
            spent_budget=spend,
            remaining_budget=remaining_budget,
            roas=roas,
            cpa=cpa,
            conversions=conversions,
            revenue=revenue,
            efficiency_score=efficiency_score,
            recommendation=recommendation
        )

        self.channel_budgets[channel] = channel_budget
        return channel_budget

    def calculate_campaign_roi(
        self,
        campaign_id: str,
        campaign_name: str,
        investment: float,
        revenue: float,
        campaign_duration_days: int,
        discount_rate: float = 0.1
    ) -> CampaignROI:
        """
        Calcula ROI completo de campanha.

        Args:
            campaign_id: ID da campanha
            campaign_name: Nome da campanha
            investment: Investimento total
            revenue: Receita total
            campaign_duration_days: Duração da campanha
            discount_rate: Taxa de desconto para NPV

        Returns:
            CampaignROI: ROI da campanha
        """
        # Métricas básicas
        gross_profit = revenue - investment
        roi_percentage = (gross_profit / investment * 100) if investment > 0 else 0
        roi_multiple = revenue / investment if investment > 0 else 0

        # Payback period (simplificado)
        daily_revenue = revenue / campaign_duration_days if campaign_duration_days > 0 else 0
        payback_days = int(investment / daily_revenue) if daily_revenue > 0 else campaign_duration_days

        # NPV (simplificado - assumindo fluxo uniforme)
        daily_cash_flow = gross_profit / campaign_duration_days if campaign_duration_days > 0 else 0
        daily_discount_rate = discount_rate / 365
        npv = 0
        for day in range(1, campaign_duration_days + 1):
            npv += daily_cash_flow / ((1 + daily_discount_rate) ** day)
        npv -= investment

        # IRR (simplificado)
        irr = (revenue / investment) ** (365 / campaign_duration_days) - 1 if investment > 0 and campaign_duration_days > 0 else 0

        campaign_roi = CampaignROI(
            campaign_id=campaign_id,
            campaign_name=campaign_name,
            total_investment=investment,
            total_revenue=revenue,
            gross_profit=gross_profit,
            roi_percentage=roi_percentage,
            roi_multiple=roi_multiple,
            payback_days=payback_days,
            npv=npv,
            irr=irr
        )

        self.campaign_rois[campaign_id] = campaign_roi
        return campaign_roi

    def optimize_budget_allocation(
        self,
        current_allocations: List[ChannelBudget],
        total_budget: float,
        min_budget_per_channel: float = 500
    ) -> List[BudgetAllocation]:
        """
        Otimiza alocação de budget.

        Args:
            current_allocations: Alocações atuais
            total_budget: Budget total disponível
            min_budget_per_channel: Budget mínimo por canal

        Returns:
            Lista de alocações otimizadas
        """
        optimizations = []

        # Ordenar por eficiência
        sorted_channels = sorted(
            current_allocations,
            key=lambda x: x.efficiency_score,
            reverse=True
        )

        # Calcular budget total atual
        current_total = sum(c.allocated_budget for c in current_allocations)

        # Distribuir budget baseado em eficiência
        total_efficiency = sum(c.efficiency_score for c in current_allocations)

        for channel in sorted_channels:
            # Proporção baseada em eficiência
            efficiency_ratio = channel.efficiency_score / total_efficiency if total_efficiency > 0 else 0

            # Budget recomendado
            recommended = max(
                min_budget_per_channel,
                total_budget * efficiency_ratio
            )

            # Calcular mudança
            current = channel.allocated_budget
            change = recommended - current
            change_pct = (change / current * 100) if current > 0 else 0

            if change_pct > 10:
                direction = 'increase'
            elif change_pct < -10:
                direction = 'decrease'
            else:
                direction = 'maintain'

            # Rationale
            rationale = self._generate_allocation_rationale(
                channel=channel.channel,
                efficiency_score=channel.efficiency_score,
                roas=channel.roas,
                direction=direction
            )

            # Impacto esperado
            expected_impact = self._estimate_budget_impact(
                channel=channel.channel,
                current_budget=current,
                new_budget=recommended,
                roas=channel.roas
            )

            optimizations.append(BudgetAllocation(
                channel=channel.channel,
                current_budget=current,
                recommended_budget=recommended,
                change_percentage=abs(change_pct),
                change_direction=direction,
                rationale=rationale,
                expected_impact=expected_impact
            ))

        logger.info(f"📊 Otimização de budget calculada: {len(optimizations)} canais")
        return optimizations

    def write_budget_report_to_obsidian(
        self,
        tenant_name: str,
        obsidian_path: str,
        allocations: Optional[List[BudgetAllocation]] = None,
        channel_metrics: Optional[List[ChannelBudget]] = None,
        campaign_rois: Optional[List[CampaignROI]] = None
    ) -> str:
        """
        Escreve relatório de budget no Obsidian.

        Args:
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault
            allocations: Alocações de budget
            channel_metrics: Métricas por canal
            campaign_rois: ROIs de campanhas

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        budget_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "07 - Budget & ROI",
            tenant_name
        )
        os.makedirs(budget_path, exist_ok=True)

        content = f"""---
tags: [budget, roi, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 💰 Budget & ROI - {tenant_name}

**Gerado em:** {timestamp}

---

## 📊 Visão Geral

"""

        # Resumo executivo
        if channel_metrics:
            total_spend = sum(c.spent_budget for c in channel_metrics)
            total_revenue = sum(c.revenue for c in channel_metrics)
            avg_roas = total_revenue / total_spend if total_spend > 0 else 0
            total_conversions = sum(c.conversions for c in channel_metrics)

            content += f"""
| Métrica | Valor |
| :------ | :---- |
| **Total Investido** | R$ {total_spend:,.2f} |
| **Total Receita** | R$ {total_revenue:,.2f} |
| **ROAS Médio** | {avg_roas:.2f}x |
| **Total Conversões** | {total_conversions:,} |
| **Lucro Bruto** | R$ {total_revenue - total_spend:,.2f} |

---

## 📈 Performance por Canal

"""

            # Tabela de canais
            content += "| Canal | Budget | Gasto | Receita | ROAS | CPA | Conversões | Eficiência |\n"
            content += "| :---- | :----- | :---- | :------ | :--- | :-- | :--------- | :--------- |\n"

            sorted_channels = sorted(channel_metrics, key=lambda x: x.efficiency_score, reverse=True)
            for ch in sorted_channels:
                efficiency_icon = '🟢' if ch.efficiency_score > 70 else '🟡' if ch.efficiency_score > 40 else '🔴'
                content += f"| {ch.channel.title()} | R$ {ch.allocated_budget:,.0f} | R$ {ch.spent_budget:,.0f} | R$ {ch.revenue:,.0f} | {ch.roas:.2f}x | R$ {ch.cpa:.0f} | {ch.conversions:,} | {efficiency_icon} {ch.efficiency_score:.0f}% |\n"

        # Alocações recomendadas
        if allocations:
            content += """
---

## 💡 Alocação Recomendada

"""
            for alloc in allocations:
                direction_icon = {'increase': '📈', 'decrease': '📉', 'maintain': '➡️'}.get(alloc.change_direction, '❓')
                content += f"""
### {direction_icon} {alloc.channel.title()}

| Campo | Valor |
| :---- | :---- |
| **Atual** | R$ {alloc.current_budget:,.2f} |
| **Recomendado** | R$ {alloc.recommended_budget:,.2f} |
| **Mudança** | {alloc.change_direction.title()} {alloc.change_percentage:.1f}% |

**Rationale:** {alloc.rationale}

**Impacto Esperado:** {alloc.expected_impact}

---
"""

        # ROI de campanhas
        if campaign_rois:
            content += """
---

## 🎯 ROI por Campanha

"""
            for roi in campaign_rois:
                roi_icon = '🟢' if roi.roi_percentage > 100 else '🟡' if roi.roi_percentage > 50 else '🔴'
                content += f"""
### {roi_icon} {roi.campaign_name}

| Métrica | Valor |
| :------ | :---- |
| **Investimento** | R$ {roi.total_investment:,.2f} |
| **Receita** | R$ {roi.total_revenue:,.2f} |
| **Lucro** | R$ {roi.gross_profit:,.2f} |
| **ROI** | {roi.roi_percentage:.1f}% |
| **ROI Múltiplo** | {roi.roi_multiple:.2f}x |
| **Payback** | {roi.payback_days} dias |
| **NPV** | R$ {roi.npv:,.2f} |
| **IRR** | {roi.irr:.1%} |

---
"""

        # Benchmark comparison
        content += """
---

## 📊 Benchmarks do Setor

| Canal | ROAS Benchmark | Seu ROAS | Status |
| :---- | :------------- | :------- | :----- |
"""

        for channel_type, benchmark in self.ROAS_BENCHMARKS.items():
            if channel_metrics:
                channel_metric = next((c for c in channel_metrics if c.channel == channel_type), None)
                if channel_metric:
                    status = '🟢' if channel_metric.roas >= benchmark['roas'] else '🔴'
                    content += f"| {channel_type.replace('_', ' ').title()} | {benchmark['roas']:.1f}x | {channel_metric.roas:.2f}x | {status} |\n"

        content += f"""
---

## 📅 Próximas Ações

- [ ] Revisar alocação de budget com base nas recomendações
- [ ] Otimizar canais com ROAS abaixo do benchmark
- [ ] Escalar canais com alta eficiência
- [ ] Revisar performance de campanhas
- [ ] Atualizar forecast de receita

---

## 📈 Dataview Queries

### Todas as Campanhas

```dataview
TABLE total_investment as "Investimento", total_revenue as "Receita", roi_percentage as "ROI", payback_days as "Payback"
FROM "🧠 EXOCÓRTEX/07 - Budget & ROI/{tenant_name}"
WHERE contains(tags, "campanha")
SORT roi_percentage DESC
```

### Performance Mensal

```dataview
TABLE sum(spent_budget) as "Gasto", sum(revenue) as "Receita", sum(revenue)/sum(spent_budget) as "ROAS"
FROM "🧠 EXOCÓRTEX/07 - Budget & ROI/{tenant_name}"
WHERE contains(tags, "mensal")
GROUP BY month
```

---

*Gerado automaticamente pelo Exocórtex v5.0 — Budget & ROI Tracker*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Budget-ROI-{safe_name}-{datetime.now().strftime('%Y%m')}.md"
        filepath = os.path.join(budget_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"💰 Relatório de budget escrito no Obsidian: {filepath}")
        return filepath

    def _calculate_channel_scores(
        self,
        historical_performance: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """Calcula scores para cada canal."""
        scores = {}

        for channel, metrics in historical_performance.items():
            roas = metrics.get('roas', 2.0)
            spend = metrics.get('spend', 0)
            revenue = metrics.get('revenue', 0)

            # Score baseado em ROAS normalizado
            benchmark = self.ROAS_BENCHMARKS.get(
                channel,
                self.ROAS_BENCHMARKS[ChannelType.OTHER.value]
            )
            roas_score = (roas / benchmark['roas']) * 50

            # Score de volume
            volume_score = min(30, (spend / 10000) * 30) if spend > 0 else 0

            # Score de consistência (simplificado)
            consistency_score = 20  # Assumido como médio

            scores[channel] = min(100, roas_score + volume_score + consistency_score)

        return scores

    def _performance_allocation(
        self,
        total_budget: float,
        channel_scores: Dict[str, float],
        historical_performance: Dict[str, Dict[str, float]]
    ) -> List[BudgetAllocation]:
        """Alocação com viés de performance."""
        allocations = []
        total_score = sum(channel_scores.values())

        for channel, score in channel_scores.items():
            # Peso maior para canais com maior score
            weight = score / total_score if total_score > 0 else 0

            # Ajustar para dar mínimo para todos
            base_weight = 0.1  # 10% mínimo para cada canal
            performance_weight = 0.9 * weight  # 90% baseado em performance

            recommended = total_budget * (base_weight / len(channel_scores) + performance_weight)

            current = historical_performance.get(channel, {}).get('spend', recommended)
            change_pct = ((recommended - current) / current * 100) if current > 0 else 0

            direction = 'increase' if change_pct > 10 else 'decrease' if change_pct < -10 else 'maintain'

            allocations.append(BudgetAllocation(
                channel=channel,
                current_budget=current,
                recommended_budget=recommended,
                change_percentage=abs(change_pct),
                change_direction=direction,
                rationale=f"Canal com score de {score:.0f}/100",
                expected_impact=f"ROAS esperado: {self.ROAS_BENCHMARKS.get(channel, self.ROAS_BENCHMARKS[ChannelType.OTHER.value])['roas']:.1f}x"
            ))

        return allocations

    def _balanced_allocation(
        self,
        total_budget: float,
        channel_scores: Dict[str, float],
        historical_performance: Dict[str, Dict[str, float]]
    ) -> List[BudgetAllocation]:
        """Alocação balanceada."""
        allocations = []
        num_channels = len(channel_scores)
        base_per_channel = total_budget / num_channels

        for channel, score in channel_scores.items():
            # Variação de ±30% baseado em score
            adjustment = (score - 50) / 50 * 0.3  # -0.3 a +0.3
            recommended = base_per_channel * (1 + adjustment)

            current = historical_performance.get(channel, {}).get('spend', recommended)
            change_pct = ((recommended - current) / current * 100) if current > 0 else 0

            direction = 'increase' if change_pct > 10 else 'decrease' if change_pct < -10 else 'maintain'

            allocations.append(BudgetAllocation(
                channel=channel,
                current_budget=current,
                recommended_budget=recommended,
                change_percentage=abs(change_pct),
                change_direction=direction,
                rationale=f"Distribuição balanceada com ajuste de performance",
                expected_impact="Diversificação de risco com otimização moderada"
            ))

        return allocations

    def _aggressive_allocation(
        self,
        total_budget: float,
        channel_scores: Dict[str, float],
        historical_performance: Dict[str, Dict[str, float]]
    ) -> List[BudgetAllocation]:
        """Alocação agressiva nos melhores canais."""
        allocations = []

        # Ordenar por score
        sorted_channels = sorted(channel_scores.items(), key=lambda x: x[1], reverse=True)

        # Top 3 canais recebem 80% do budget
        top_3_budget = total_budget * 0.8
        remaining_budget = total_budget * 0.2

        for i, (channel, score) in enumerate(sorted_channels):
            if i < 3:
                # Top 3: distribuição proporcional ao score
                top_3_total_score = sum(s for _, s in sorted_channels[:3])
                recommended = (score / top_3_total_score) * top_3_budget
            else:
                # Restante: divisão igualitária
                remaining_channels = len(sorted_channels) - 3
                recommended = remaining_budget / remaining_channels if remaining_channels > 0 else 0

            current = historical_performance.get(channel, {}).get('spend', recommended)
            change_pct = ((recommended - current) / current * 100) if current > 0 else 0

            direction = 'increase' if change_pct > 10 else 'decrease' if change_pct < -10 else 'maintain'

            allocations.append(BudgetAllocation(
                channel=channel,
                current_budget=current,
                recommended_budget=recommended,
                change_percentage=abs(change_pct),
                change_direction=direction,
                rationale=f"Foco agressivo em canais top performers" if i < 3 else "Canal secundário com budget reduzido",
                expected_impact="Maximização de ROI através de concentração nos melhores canais"
            ))

        return allocations

    def _calculate_efficiency_score(
        self,
        roas: float,
        benchmark_roas: float,
        spend: float,
        trend: str
    ) -> float:
        """Calcula score de eficiência do canal."""
        # ROAS component (0-50)
        roas_component = min(50, (roas / benchmark_roas) * 40)

        # Volume component (0-30)
        volume_component = min(30, (spend / 10000) * 30)

        # Trend component (0-20)
        trend_component = {'increasing': 20, 'stable': 15, 'decreasing': 5}.get(trend, 10)

        return min(100, roas_component + volume_component + trend_component)

    def _generate_channel_recommendation(
        self,
        channel: str,
        roas: float,
        benchmark_roas: float,
        efficiency_score: float
    ) -> str:
        """Gera recomendação para o canal."""
        if roas >= benchmark_roas * 1.2:
            return "🟢 Escalar budget — performance acima do benchmark"
        elif roas >= benchmark_roas:
            return "🟡 Manter budget — performance dentro do esperado"
        elif roas >= benchmark_roas * 0.7:
            return "🟠 Otimizar antes de escalar — performance abaixo do ideal"
        else:
            return "🔴 Reavaliar canal — performance crítica, considerar pausa"

    def _generate_allocation_rationale(
        self,
        channel: str,
        efficiency_score: float,
        roas: float,
        direction: str
    ) -> str:
        """Gera rationale para alocação."""
        if direction == 'increase':
            return f"Canal eficiente ({efficiency_score:.0f}%, ROAS {roas:.2f}x) — oportunidade de escala"
        elif direction == 'decrease':
            return f"Canal abaixo do esperado ({efficiency_score:.0f}%, ROAS {roas:.2f}x) — reduzir exposição"
        else:
            return f"Canal em equilíbrio ({efficiency_score:.0f}%, ROAS {roas:.2f}x) — manter investimento"

    def _estimate_budget_impact(
        self,
        channel: str,
        current_budget: float,
        new_budget: float,
        roas: float
    ) -> str:
        """Estima impacto da mudança de budget."""
        budget_change = new_budget - current_budget
        revenue_impact = budget_change * roas

        if revenue_impact > 0:
            return f"+R$ {revenue_impact:,.0f} em receita esperada"
        elif revenue_impact < 0:
            return f"-R$ {abs(revenue_impact):,.0f} em receita (redução de risco)"
        else:
            return "Impacto neutro esperado"

    def generate_budget_report_for_all_tenants(
        self,
        tenants_data: List[Dict[str, Any]],
        obsidian_path: str
    ) -> Dict[str, str]:
        """
        Gera relatório de budget para todos os tenants.

        Args:
            tenants_data: Lista de tenants
            obsidian_path: Caminho para o vault

        Returns:
            Dicionário {tenant_name: filepath}
        """
        results = {}

        for tenant in tenants_data:
            tenant_name = tenant.get('name', 'Unknown')
            tenant_id = tenant.get('id', 'unknown')

            # Simular métricas por canal
            channel_metrics = []
            for channel_type in ChannelType:
                # Dados simulados
                spend = 5000 + (hash(f"{tenant_id}_{channel_type.value}") % 10000)
                roas = 2.0 + (hash(f"{tenant_id}_{channel_type.value}") % 50) / 10
                revenue = spend * roas

                channel_budget = self.calculate_channel_roi(
                    channel=channel_type.value,
                    spend=spend,
                    revenue=revenue
                )
                channel_metrics.append(channel_budget)

            # Otimizar alocação
            total_budget = sum(c.allocated_budget for c in channel_metrics)
            allocations = self.optimize_budget_allocation(channel_metrics, total_budget)

            # Escrever relatório
            filepath = self.write_budget_report_to_obsidian(
                tenant_name=tenant_name,
                obsidian_path=obsidian_path,
                allocations=allocations,
                channel_metrics=channel_metrics
            )

            results[tenant_name] = filepath

        return results
