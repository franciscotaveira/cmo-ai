"""
╔═══════════════════════════════════════════════════════════════════════════════
║ GROWTH MARKETING & PERFORMANCE ENGINE — v5.3 — CMO 360°
╠═══════════════════════════════════════════════════════════════════════════════
║ Gestão completa de Growth, Performance, Aquisição e Canais
║ Para CMOs e Diretores de Marketing
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
    """Tipos de canal de aquisição."""
    GOOGLE_ADS = "google_ads"
    META_ADS = "meta_ads"
    LINKEDIN_ADS = "linkedin_ads"
    TIKTOK_ADS = "tiktok_ads"
    GOOGLE_ORGANIC = "google_organic"
    DIRECT = "direct"
    REFERRAL = "referral"
    EMAIL = "email"
    SOCIAL_ORGANIC = "social_organic"
    AFFILIATE = "affiliate"
    PARTNERSHIPS = "partnerships"
    EVENTS = "events"
    PR = "public_relations"
    CONTENT = "content_marketing"
    OTHER = "other"


class CampaignObjective(Enum):
    """Objetivos de campanha."""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    CONVERSION = "conversion"
    RETENTION = "retention"
    REACTIVATION = "reactivation"


@dataclass
class ChannelPerformance:
    """Performance de um canal."""
    channel: str
    channel_type: str
    period: str
    
    # Métricas de investimento
    spend: float
    impressions: int
    clicks: int
    
    # Métricas de conversão
    leads: int
    customers: int
    revenue: float
    
    # Métricas calculadas
    ctr: float = 0.0
    cpc: float = 0.0
    cpl: float = 0.0
    cac: float = 0.0
    roas: float = 0.0
    roi: float = 0.0
    conversion_rate: float = 0.0
    
    # Qualidade
    quality_score: float = 0.0
    trend: str = "stable"  # increasing, decreasing, stable


@dataclass
class Campaign:
    """Campanha de marketing."""
    id: str
    name: str
    channel: str
    objective: str
    status: str  # planned, active, paused, completed
    start_date: str
    end_date: str
    
    # Budget
    budget_allocated: float
    budget_spent: float
    
    # Performance
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    
    # Metas
    goal_impressions: int = 0
    goal_conversions: int = 0
    goal_roas: float = 0.0
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Experiment:
    """Experimento de growth."""
    id: str
    title: str
    hypothesis: str
    channel: str
    status: str  # idea, planned, running, completed, won, lost
    
    # Métricas
    metric_target: str
    baseline_value: float
    target_lift: float  # em percentual (ex: 0.15 = 15%)
    
    # Resultados
    actual_lift: Optional[float] = None
    confidence: Optional[float] = None
    learnings: str = ""
    
    # Timeline
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    owner: str = ""


class GrowthMarketingEngine:
    """
    Growth Marketing & Performance Engine.

    Para CMOs e Diretores de Marketing gerenciarem:
    • Performance por canal
    • Campanhas e budget
    • Experimentos de growth
    • Otimização de aquisição
    """

    # Benchmarks por canal (médias de mercado)
    CHANNEL_BENCHMARKS = {
        ChannelType.GOOGLE_ADS.value: {
            'ctr': 0.035, 'cpc': 2.5, 'conversion_rate': 0.04, 'roas': 4.0
        },
        ChannelType.META_ADS.value: {
            'ctr': 0.015, 'cpc': 1.2, 'conversion_rate': 0.03, 'roas': 3.5
        },
        ChannelType.LINKEDIN_ADS.value: {
            'ctr': 0.012, 'cpc': 5.0, 'conversion_rate': 0.025, 'roas': 3.0
        },
        ChannelType.EMAIL.value: {
            'ctr': 0.025, 'cpc': 0.1, 'conversion_rate': 0.05, 'roas': 10.0
        },
        ChannelType.GOOGLE_ORGANIC.value: {
            'ctr': 0.02, 'cpc': 0, 'conversion_rate': 0.035, 'roas': 8.0
        },
        ChannelType.OTHER.value: {
            'ctr': 0.01, 'cpc': 1.0, 'conversion_rate': 0.02, 'roas': 3.0
        }
    }

    def __init__(self):
        """Inicializa o Growth Marketing Engine."""
        self.channels: Dict[str, ChannelPerformance] = {}
        self.campaigns: List[Campaign] = []
        self.experiments: List[Experiment] = []
        logger.info("📈 GrowthMarketingEngine inicializado")

    def track_channel_performance(
        self,
        channel: str,
        period: str,
        spend: float,
        impressions: int,
        clicks: int,
        leads: int,
        customers: int,
        revenue: float
    ) -> ChannelPerformance:
        """
        Rastreia performance de um canal.

        Args:
            channel: Nome do canal
            period: Período (ex: 2026-03, 2026-W09)
            spend: Valor gasto
            impressions: Impressões
            clicks: Cliques
            leads: Leads gerados
            customers: Clientes adquiridos
            revenue: Receita atribuída

        Returns:
            ChannelPerformance: Performance calculada
        """
        # Calcular métricas derivadas
        ctr = clicks / impressions if impressions > 0 else 0
        cpc = spend / clicks if clicks > 0 else 0
        cpl = spend / leads if leads > 0 else 0
        cac = spend / customers if customers > 0 else 0
        roas = revenue / spend if spend > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        conversion_rate = customers / clicks if clicks > 0 else 0

        # Obter benchmark
        benchmark = self.CHANNEL_BENCHMARKS.get(
            channel,
            self.CHANNEL_BENCHMARKS[ChannelType.OTHER.value]
        )

        # Calcular quality score (0-100)
        quality_score = self._calculate_quality_score(
            channel=channel,
            ctr=ctr,
            cpc=cpc,
            conversion_rate=conversion_rate,
            roas=roas,
            benchmark=benchmark
        )

        # Determinar tendência (simplificado)
        trend = "stable"  # Será atualizado com histórico

        performance = ChannelPerformance(
            channel=channel,
            channel_type=channel,
            period=period,
            spend=spend,
            impressions=impressions,
            clicks=clicks,
            leads=leads,
            customers=customers,
            revenue=revenue,
            ctr=ctr,
            cpc=cpc,
            cpl=cpl,
            cac=cac,
            roas=roas,
            roi=roi,
            conversion_rate=conversion_rate,
            quality_score=quality_score,
            trend=trend
        )

        self.channels[f"{channel}_{period}"] = performance
        logger.info(f"📊 Performance registrada: {channel} ({period}) - ROAS: {roas:.2f}x")
        return performance

    def create_campaign(
        self,
        name: str,
        channel: str,
        objective: str,
        budget: float,
        start_date: str,
        end_date: str,
        goal_roas: float = 3.0,
        goal_conversions: int = 100
    ) -> Campaign:
        """
        Cria uma campanha.

        Args:
            name: Nome da campanha
            channel: Canal principal
            objective: Objetivo (awareness, conversion, etc.)
            budget: Budget alocado
            start_date: Data de início
            end_date: Data de fim
            goal_roas: Meta de ROAS
            goal_conversions: Meta de conversões

        Returns:
            Campaign: Campanha criada
        """
        campaign = Campaign(
            id=f"camp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            channel=channel,
            objective=objective,
            status='planned',
            start_date=start_date,
            end_date=end_date,
            budget_allocated=budget,
            budget_spent=0,
            goal_impressions=int(budget / 5),  # Estimativa
            goal_conversions=goal_conversions,
            goal_roas=goal_roas
        )

        self.campaigns.append(campaign)
        logger.info(f"📢 Campanha criada: {name} ({channel}) - Budget: R$ {budget:,.0f}")
        return campaign

    def update_campaign_performance(
        self,
        campaign_id: str,
        impressions: int,
        clicks: int,
        conversions: int,
        revenue: float,
        spent: float
    ) -> bool:
        """
        Atualiza performance de campanha.

        Args:
            campaign_id: ID da campanha
            impressions: Impressões acumuladas
            clicks: Cliques acumulados
            conversions: Conversões acumuladas
            revenue: Receita atribuída
            spent: Valor gasto

        Returns:
            True se atualizado com sucesso
        """
        for campaign in self.campaigns:
            if campaign.id == campaign_id:
                campaign.impressions = impressions
                campaign.clicks = clicks
                campaign.conversions = conversions
                campaign.revenue = revenue
                campaign.budget_spent = spent

                # Calcular ROAS atual
                current_roas = revenue / spent if spent > 0 else 0
                progress_roas = current_roas / campaign.goal_roas if campaign.goal_roas > 0 else 0

                # Alertar se ROAS abaixo da meta
                if progress_roas < 0.7 and spent > campaign.budget_allocated * 0.3:
                    logger.warning(
                        f"⚠️ Campanha {campaign.name} com ROAS abaixo da meta: "
                        f"{current_roas:.2f}x (meta: {campaign.goal_roas:.2f}x)"
                    )

                logger.info(f"📊 Campanha atualizada: {campaign.name} - ROAS: {current_roas:.2f}x")
                return True

        logger.warning(f"⚠️ Campanha não encontrada: {campaign_id}")
        return False

    def create_experiment(
        self,
        title: str,
        hypothesis: str,
        channel: str,
        metric_target: str,
        baseline_value: float,
        target_lift: float,
        owner: str = ""
    ) -> Experiment:
        """
        Cria experimento de growth.

        Args:
            title: Título do experimento
            hypothesis: Hipótese sendo testada
            channel: Canal do teste
            metric_target: Métrica alvo
            baseline_value: Valor baseline da métrica
            target_lift: Lift esperado (ex: 0.15 = 15%)
            owner: Responsável

        Returns:
            Experiment: Experimento criado
        """
        experiment = Experiment(
            id=f"exp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            hypothesis=hypothesis,
            channel=channel,
            status='planned',
            metric_target=metric_target,
            baseline_value=baseline_value,
            target_lift=target_lift,
            owner=owner or "Growth Team"
        )

        self.experiments.append(experiment)
        logger.info(f"🧪 Experimento criado: {title} - Lift alvo: {target_lift:.1%}")
        return experiment

    def complete_experiment(
        self,
        experiment_id: str,
        actual_lift: float,
        confidence: float,
        learnings: str = ""
    ) -> bool:
        """
        Completa experimento com resultados.

        Args:
            experiment_id: ID do experimento
            actual_lift: Lift real observado
            confidence: Nível de confiança estatística
            learnings: Aprendizados principais

        Returns:
            True se completado com sucesso
        """
        for exp in self.experiments:
            if exp.id == experiment_id:
                exp.actual_lift = actual_lift
                exp.confidence = confidence
                exp.learnings = learnings
                exp.end_date = datetime.now().strftime('%Y-%m-%d')

                # Determinar se venceu ou perdeu
                if actual_lift >= exp.target_lift * 0.8 and confidence >= 0.8:
                    exp.status = 'won'
                    logger.info(f"✅ Experimento VENCEU: {exp.title} (+{actual_lift:.1%})")
                elif confidence >= 0.8:
                    exp.status = 'lost'
                    logger.info(f"❌ Experimento PERDEU: {exp.title} (+{actual_lift:.1%})")
                else:
                    exp.status = 'completed'
                    logger.info(f"📊 Experimento completado (inconclusivo): {exp.title}")

                return True

        logger.warning(f"⚠️ Experimento não encontrado: {experiment_id}")
        return False

    def get_channel_insights(
        self,
        channel: str,
        periods: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Obtém insights de um canal.

        Args:
            channel: Nome do canal
            periods: Lista de períodos para analisar

        Returns:
            Dicionário com insights do canal
        """
        # Filtrar performances do canal
        performances = [
            perf for key, perf in self.channels.items()
            if perf.channel == channel and (periods is None or perf.period in periods)
        ]

        if not performances:
            return {'error': 'Sem dados para este canal'}

        # Calcular médias
        avg_spend = sum(p.spend for p in performances) / len(performances)
        avg_roas = sum(p.roas for p in performances) / len(performances)
        avg_ctr = sum(p.ctr for p in performances) / len(performances)
        avg_cac = sum(p.cac for p in performances) / len(performances)

        # Obter benchmark
        benchmark = self.CHANNEL_BENCHMARKS.get(
            channel,
            self.CHANNEL_BENCHMARKS[ChannelType.OTHER.value]
        )

        # Gerar insights
        insights = {
            'channel': channel,
            'periods_analyzed': len(performances),
            'total_spend': sum(p.spend for p in performances),
            'total_revenue': sum(p.revenue for p in performances),
            'avg_roas': avg_roas,
            'avg_ctr': avg_ctr,
            'avg_cac': avg_cac,
            'vs_benchmark': {
                'roas': 'above' if avg_roas > benchmark['roas'] else 'below',
                'ctr': 'above' if avg_ctr > benchmark['ctr'] else 'below',
            },
            'recommendation': self._generate_channel_recommendation(
                channel, avg_roas, avg_ctr, benchmark
            )
        }

        return insights

    def get_all_campaigns_summary(self) -> Dict[str, Any]:
        """
        Obtém resumo de todas as campanhas.

        Returns:
            Dicionário com resumo das campanhas
        """
        if not self.campaigns:
            return {'campaigns': [], 'summary': {}}

        active = [c for c in self.campaigns if c.status == 'active']
        planned = [c for c in self.campaigns if c.status == 'planned']
        completed = [c for c in self.campaigns if c.status == 'completed']

        total_budget = sum(c.budget_allocated for c in self.campaigns)
        total_spent = sum(c.budget_spent for c in self.campaigns)
        total_revenue = sum(c.revenue for c in self.campaigns)

        return {
            'campaigns': [
                {
                    'id': c.id,
                    'name': c.name,
                    'channel': c.channel,
                    'status': c.status,
                    'budget': c.budget_allocated,
                    'spent': c.budget_spent,
                    'roas': c.revenue / c.budget_spent if c.budget_spent > 0 else 0,
                    'progress': c.budget_spent / c.budget_allocated if c.budget_allocated > 0 else 0
                }
                for c in self.campaigns
            ],
            'summary': {
                'total_campaigns': len(self.campaigns),
                'active': len(active),
                'planned': len(planned),
                'completed': len(completed),
                'total_budget': total_budget,
                'total_spent': total_spent,
                'total_revenue': total_revenue,
                'overall_roas': total_revenue / total_spent if total_spent > 0 else 0,
                'budget_utilization': total_spent / total_budget if total_budget > 0 else 0
            }
        }

    def get_experiments_pipeline(self) -> Dict[str, Any]:
        """
        Obtém pipeline de experimentos.

        Returns:
            Dicionário com status dos experimentos
        """
        by_status = {
            'idea': [e for e in self.experiments if e.status == 'idea'],
            'planned': [e for e in self.experiments if e.status == 'planned'],
            'running': [e for e in self.experiments if e.status == 'running'],
            'won': [e for e in self.experiments if e.status == 'won'],
            'lost': [e for e in self.experiments if e.status == 'lost']
        }

        # Calcular win rate
        total_completed = len(by_status['won']) + len(by_status['lost'])
        win_rate = len(by_status['won']) / total_completed if total_completed > 0 else 0

        return {
            'pipeline': {
                'idea': len(by_status['idea']),
                'planned': len(by_status['planned']),
                'running': len(by_status['running']),
                'completed': len(by_status['won']) + len(by_status['lost'])
            },
            'results': {
                'won': len(by_status['won']),
                'lost': len(by_status['lost']),
                'win_rate': win_rate
            },
            'experiments': [
                {
                    'id': e.id,
                    'title': e.title,
                    'status': e.status,
                    'channel': e.channel,
                    'metric': e.metric_target,
                    'target_lift': e.target_lift,
                    'actual_lift': e.actual_lift,
                    'confidence': e.confidence
                }
                for e in self.experiments
            ]
        }

    def _calculate_quality_score(
        self,
        channel: str,
        ctr: float,
        cpc: float,
        conversion_rate: float,
        roas: float,
        benchmark: Dict[str, float]
    ) -> float:
        """Calcula quality score (0-100) baseado em métricas vs benchmark."""
        scores = []

        # CTR score (0-25)
        ctr_ratio = ctr / benchmark['ctr'] if benchmark['ctr'] > 0 else 1
        scores.append(min(25, ctr_ratio * 15))

        # CPC score (0-25) - menor é melhor
        if cpc > 0 and benchmark['cpc'] > 0:
            cpc_ratio = benchmark['cpc'] / cpc
            scores.append(min(25, cpc_ratio * 15))
        else:
            scores.append(25)  # CPC zero ou não disponível

        # Conversion rate score (0-25)
        cvr_ratio = conversion_rate / benchmark['conversion_rate'] if benchmark['conversion_rate'] > 0 else 1
        scores.append(min(25, cvr_ratio * 15))

        # ROAS score (0-25)
        roas_ratio = roas / benchmark['roas'] if benchmark['roas'] > 0 else 1
        scores.append(min(25, roas_ratio * 15))

        return sum(scores)

    def _generate_channel_recommendation(
        self,
        channel: str,
        avg_roas: float,
        avg_ctr: float,
        benchmark: Dict[str, float]
    ) -> str:
        """Gera recomendação para o canal."""
        if avg_roas >= benchmark['roas'] * 1.3:
            return "🟢 ESCALAR — Performance excelente, aumentar budget"
        elif avg_roas >= benchmark['roas']:
            return "🟡 MANTER — Performance dentro do esperado, otimizar gradualmente"
        elif avg_roas >= benchmark['roas'] * 0.7:
            return "🟠 OTIMIZAR — Performance abaixo, testar novas abordagens"
        else:
            return "🔴 REAVALIAR — Performance crítica, considerar pausa ou mudança de estratégia"

    def write_growth_report_to_obsidian(
        self,
        tenant_name: str,
        obsidian_path: str,
        include_campaigns: bool = True,
        include_experiments: bool = True
    ) -> str:
        """
        Escreve relatório de Growth no Obsidian.

        Args:
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault
            include_campaigns: Incluir seção de campanhas
            include_experiments: Incluir seção de experimentos

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        growth_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "09 - Growth & Performance",
            tenant_name
        )
        os.makedirs(growth_path, exist_ok=True)

        # Obter dados
        campaigns_summary = self.get_all_campaigns_summary() if include_campaigns else {}
        experiments_pipeline = self.get_experiments_pipeline() if include_experiments else {}

        # Conteúdo
        content = f"""---
tags: [growth, performance, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 📈 Growth & Performance - {tenant_name}

**Gerado em:** {timestamp}

---

## 📊 Visão Geral de Canais

"""

        # Performance por canal
        if self.channels:
            content += "| Canal | Spend | Receita | ROAS | CTR | Conv. | Quality |\n"
            content += "| :---- | :---- | :------ | :--- | :-- | :---- | :------ |\n"

            # Agrupar por canal
            channels_grouped = {}
            for key, perf in self.channels.items():
                if perf.channel not in channels_grouped:
                    channels_grouped[perf.channel] = []
                channels_grouped[perf.channel].append(perf)

            for channel, performances in channels_grouped.items():
                # Usar performance mais recente
                latest = performances[-1]
                quality_icon = '🟢' if latest.quality_score > 70 else '🟡' if latest.quality_score > 40 else '🔴'

                content += (
                    f"| {channel.title()} | "
                    f"R$ {latest.spend:,.0f} | "
                    f"R$ {latest.revenue:,.0f} | "
                    f"{latest.roas:.2f}x | "
                    f"{latest.ctr:.2%} | "
                    f"{latest.conversion_rate:.2%} | "
                    f"{quality_icon} {latest.quality_score:.0f} |\n"
                )
        else:
            content += "> Sem dados de canais registrados.\n"

        # Seção de Campanhas
        if include_campaigns and campaigns_summary:
            content += """
---

## 📢 Campanhas

"""

            summary = campaigns_summary.get('summary', {})
            content += f"""
### Resumo

| Métrica | Valor |
| :------ | :---- |
| **Total Campanhas** | {summary.get('total_campaigns', 0)} |
| **Ativas** | {summary.get('active', 0)} |
| **Budget Total** | R$ {summary.get('total_budget', 0):,.0f} |
| **Gasto** | R$ {summary.get('total_spent', 0):,.0f} |
| **Receita** | R$ {summary.get('total_revenue', 0):,.0f} |
| **ROAS Geral** | {summary.get('overall_roas', 0):.2f}x |
| **Utilização Budget** | {summary.get('budget_utilization', 0):.1%} |

"""

            # Listar campanhas ativas
            active_campaigns = [c for c in campaigns_summary.get('campaigns', []) if c['status'] == 'active']
            if active_campaigns:
                content += "### Campanhas Ativas\n\n"
                content += "| Campanha | Canal | Budget | Gasto | ROAS | Progresso |\n"
                content += "| :------- | :---- | :----- | :---- | :--- | :-------- |\n"

                for camp in active_campaigns:
                    roas_status = '🟢' if camp['roas'] >= 3 else '🟡' if camp['roas'] >= 2 else '🔴'
                    content += (
                        f"| {camp['name']} | {camp['channel']} | "
                        f"R$ {camp['budget']:,.0f} | R$ {camp['spent']:,.0f} | "
                        f"{roas_status} {camp['roas']:.2f}x | {camp['progress']:.1%} |\n"
                    )

        # Seção de Experimentos
        if include_experiments and experiments_pipeline:
            content += """
---

## 🧪 Experimentos

"""

            pipeline = experiments_pipeline.get('pipeline', {})
            results = experiments_pipeline.get('results', {})

            content += f"""
### Pipeline

| Estágio | Quantidade |
| :------ | :--------: |
| 💡 Ideias | {pipeline.get('idea', 0)} |
| 📋 Planejados | {pipeline.get('planned', 0)} |
| 🔬 Rodando | {pipeline.get('running', 0)} |
| ✅ Completos | {pipeline.get('completed', 0)} |

**Win Rate:** {results.get('win_rate', 0):.1%}
**Venceu:** {results.get('won', 0)} | **Perdeu:** {results.get('lost', 0)}

"""

            # Listar experimentos rodando
            running = [e for e in experiments_pipeline.get('experiments', []) if e['status'] == 'running']
            if running:
                content += "### Em Andamento\n\n"
                content += "| Experimento | Canal | Métrica | Lift Alvo | Status |\n"
                content += "| :---------- | :---- | :------ | :-------- | :----- |\n"

                for exp in running:
                    content += (
                        f"| {exp['title']} | {exp['channel']} | "
                        f"{exp['metric']} | {exp['target_lift']:.1%} | "
                        f"🔬 Rodando |\n"
                    )

        # Recomendações
        content += """
---

## 💡 Recomendações

"""

        # Gerar recomendações baseadas em performance
        recommendations = self._generate_strategic_recommendations()
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"

        content += f"""
---

## 📅 Próximas Ações

- [ ] Revisar performance de canais (semanal)
- [ ] Otimizar campanhas com ROAS baixo
- [ ] Escalar campanhas com ROAS alto
- [ ] Lançar novos experimentos
- [ ] Analisar resultados de experimentos completos

---

## 📈 Dataview Queries

### Todas as Campanhas

```dataview
TABLE channel as "Canal", status as "Status", budget_allocated as "Budget", revenue as "Receita"
FROM "🧠 EXOCÓRTEX/09 - Growth & Performance/{tenant_name}"
WHERE contains(tags, "campanha")
SORT start_date DESC
```

### Experimentos

```dataview
TABLE status as "Status", channel as "Canal", actual_lift as "Lift"
FROM "🧠 EXOCÓRTEX/09 - Growth & Performance/{tenant_name}"
WHERE contains(tags, "experimento")
SORT end_date DESC
```

---

*Gerado automaticamente pelo Exocórtex v5.3 — Growth Marketing Engine*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Growth-Performance-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(growth_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📈 Relatório de Growth escrito no Obsidian: {filepath}")
        return filepath

    def _generate_strategic_recommendations(self) -> List[str]:
        """Gera recomendações estratégicas baseadas em dados."""
        recommendations = []

        # Analisar canais
        for key, perf in self.channels.items():
            if perf.roas < 2 and perf.spend > 1000:
                recommendations.append(
                    f"⚠️ Otimizar {perf.channel}: ROAS {perf.roas:.2f}x abaixo do ideal"
                )
            elif perf.roas > 5 and perf.spend < 5000:
                recommendations.append(
                    f"🟢 Escalar {perf.channel}: ROAS {perf.roas:.2f}x, budget pode aumentar"
                )

        # Analisar campanhas
        for camp in self.campaigns:
            if camp.status == 'active' and camp.budget_spent > camp.budget_allocated * 0.9:
                recommendations.append(
                    f"⚠️ Campanha {camp.name}: Budget quase esgotado ({camp.budget_spent/camp.budget_allocated:.1%})"
                )

        # Analisar experimentos
        won_experiments = [e for e in self.experiments if e.status == 'won']
        if won_experiments:
            recommendations.append(
                f"✅ {len(won_experiments)} experimentos venceram — implementar aprendizados"
            )

        if not recommendations:
            recommendations.append("✅ Performance geral dentro do esperado")

        return recommendations[:10]  # Máximo 10 recomendações
