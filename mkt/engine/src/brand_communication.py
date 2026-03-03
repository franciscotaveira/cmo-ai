"""
╔═══════════════════════════════════════════════════════════════════════════════
║ BRAND & COMMUNICATION ENGINE — v5.3 — CMO 360°
╠═══════════════════════════════════════════════════════════════════════════════
║ Gestão de Brand, Share of Voice, Sentiment e Comunicação
║ Para CMOs e Diretores de Marketing
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class BrandMetricType(Enum):
    """Tipos de métricas de brand."""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    PREFERENCE = "preference"
    LOYALTY = "loyalty"
    ADVOCACY = "advocacy"


class SentimentType(Enum):
    """Tipos de sentimento."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class ChannelType(Enum):
    """Canais de comunicação."""
    SOCIAL_MEDIA = "social_media"
    PR = "public_relations"
    CONTENT = "content"
    EVENTS = "events"
    INFLUENCERS = "influencers"
    PAID_MEDIA = "paid_media"
    OWNED_MEDIA = "owned_media"


@dataclass
class BrandHealth:
    """Saúde da marca."""
    period: str
    
    # Brand Awareness
    unaided_awareness: float = 0.0  # %
    aided_awareness: float = 0.0  # %
    
    # Brand Consideration
    consideration: float = 0.0  # %
    preference: float = 0.0  # %
    
    # Brand Loyalty
    nps: float = 0.0  # 0-100
    retention_rate: float = 0.0  # %
    advocacy_rate: float = 0.0  # %
    
    # Share of Voice
    sov: float = 0.0  # %
    share_of_search: float = 0.0  # %
    
    # Sentiment
    positive_sentiment: float = 0.0  # %
    negative_sentiment: float = 0.0  # %
    
    # Brand Equity (calculado)
    brand_equity_score: float = 0.0  # 0-100
    brand_trend: str = "stable"


@dataclass
class SocialMention:
    """Menção em mídia social."""
    id: str
    platform: str
    author: str
    content: str
    sentiment: str
    reach: int
    engagement: int
    date: str
    topic: str = ""
    influencer: bool = False


@dataclass
class PRActivity:
    """Atividade de Relações Públicas."""
    id: str
    title: str
    type: str  # press_release, media_coverage, interview, event
    outlet: str
    date: str
    reach: int
    sentiment: str
    message: str = ""
    link: str = ""


@dataclass
class ContentPiece:
    """Peça de conteúdo de brand."""
    id: str
    title: str
    format: str  # blog, video, infographic, podcast
    channel: str
    publish_date: str
    status: str  # planned, published, promoted
    
    # Performance
    views: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    
    # Brand alignment
    brand_aligned: bool = True
    key_message: str = ""


class BrandCommunicationEngine:
    """
    Brand & Communication Engine.

    Para CMOs e Diretores de Marketing gerenciarem:
    • Brand Health e Equity
    • Share of Voice
    • Sentiment Analysis
    • PR e Communications
    • Content de Brand
    """

    def __init__(self):
        """Inicializa o Brand & Communication Engine."""
        self.brand_health: Dict[str, BrandHealth] = {}
        self.social_mentions: List[SocialMention] = []
        self.pr_activities: List[PRActivity] = []
        self.content_pieces: List[ContentPiece] = []
        logger.info("🏛️ BrandCommunicationEngine inicializado")

    def track_brand_health(
        self,
        period: str,
        unaided_awareness: float,
        aided_awareness: float,
        consideration: float,
        nps: float,
        sov: float,
        positive_sentiment: float,
        negative_sentiment: float,
        retention_rate: float = 0.0,
        share_of_search: float = 0.0
    ) -> BrandHealth:
        """
        Rastreia saúde da marca.

        Args:
            period: Período (ex: 2026-Q1, 2026-03)
            unaided_awareness: Brand awareness não auxiliado (%)
            aided_awareness: Brand awareness auxiliado (%)
            consideration: Consideração da marca (%)
            nps: Net Promoter Score (0-100)
            sov: Share of Voice (%)
            positive_sentiment: Sentimento positivo (%)
            negative_sentiment: Sentimento negativo (%)
            retention_rate: Taxa de retenção (%)
            share_of_search: Share of Search (%)

        Returns:
            BrandHealth: Saúde da marca registrada
        """
        # Calcular advocacy rate (proxy)
        advocacy_rate = nps / 100 * retention_rate if nps > 0 else 0

        # Calcular brand equity score (0-100)
        brand_equity_score = self._calculate_brand_equity(
            unaided_awareness=unaided_awareness,
            aided_awareness=aided_awareness,
            consideration=consideration,
            nps=nps,
            sov=sov,
            positive_sentiment=positive_sentiment,
            negative_sentiment=negative_sentiment
        )

        # Determinar tendência (comparar com período anterior)
        brand_trend = self._determine_brand_trend(period, brand_equity_score)

        brand_health = BrandHealth(
            period=period,
            unaided_awareness=unaided_awareness,
            aided_awareness=aided_awareness,
            consideration=consideration,
            nps=nps,
            retention_rate=retention_rate,
            advocacy_rate=advocacy_rate,
            sov=sov,
            share_of_search=share_of_search,
            positive_sentiment=positive_sentiment,
            negative_sentiment=negative_sentiment,
            brand_equity_score=brand_equity_score,
            brand_trend=brand_trend
        )

        self.brand_health[period] = brand_health
        logger.info(f"🏛️ Brand Health registrada: {period} - Equity Score: {brand_equity_score:.1f}")
        return brand_health

    def add_social_mention(
        self,
        platform: str,
        author: str,
        content: str,
        sentiment: str,
        reach: int,
        engagement: int,
        date: str,
        topic: str = "",
        influencer: bool = False
    ) -> SocialMention:
        """
        Adiciona menção social.

        Args:
            platform: Plataforma (instagram, twitter, linkedin, etc.)
            author: Autor da menção
            content: Conteúdo da menção
            sentiment: Sentimento (positive, neutral, negative)
            reach: Alcance estimado
            engagement: Engajamento (likes + comments + shares)
            date: Data da menção
            topic: Tópico/tag
            influencer: Se é influenciador

        Returns:
            SocialMention: Menção registrada
        """
        mention = SocialMention(
            id=f"mention-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            platform=platform,
            author=author,
            content=content,
            sentiment=sentiment,
            reach=reach,
            engagement=engagement,
            date=date,
            topic=topic,
            influencer=influencer
        )

        self.social_mentions.append(mention)
        logger.info(f"📱 Menção social registrada: {platform} - {sentiment}")
        return mention

    def add_pr_activity(
        self,
        title: str,
        activity_type: str,
        outlet: str,
        date: str,
        reach: int,
        sentiment: str,
        message: str = "",
        link: str = ""
    ) -> PRActivity:
        """
        Adiciona atividade de PR.

        Args:
            title: Título da atividade
            activity_type: Tipo (press_release, media_coverage, etc.)
            outlet: Veículo/mídia
            date: Data
            reach: Alcance estimado
            sentiment: Sentimento da cobertura
            message: Mensagem chave
            link: Link da matéria

        Returns:
            PRActivity: Atividade registrada
        """
        activity = PRActivity(
            id=f"pr-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            type=activity_type,
            outlet=outlet,
            date=date,
            reach=reach,
            sentiment=sentiment,
            message=message,
            link=link
        )

        self.pr_activities.append(activity)
        logger.info(f"📰 Atividade PR registrada: {title} ({outlet})")
        return activity

    def add_content_piece(
        self,
        title: str,
        format: str,
        channel: str,
        publish_date: str,
        status: str = "planned",
        key_message: str = "",
        brand_aligned: bool = True
    ) -> ContentPiece:
        """
        Adiciona peça de conteúdo de brand.

        Args:
            title: Título do conteúdo
            format: Formato (blog, video, etc.)
            channel: Canal de distribuição
            publish_date: Data de publicação
            status: Status (planned, published, promoted)
            key_message: Mensagem chave de brand
            brand_aligned: Alinhado com brand guidelines

        Returns:
            ContentPiece: Conteúdo registrado
        """
        content = ContentPiece(
            id=f"content-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            format=format,
            channel=channel,
            publish_date=publish_date,
            status=status,
            key_message=key_message,
            brand_aligned=brand_aligned
        )

        self.content_pieces.append(content)
        logger.info(f"📝 Conteúdo de brand registrado: {title}")
        return content

    def update_content_performance(
        self,
        content_id: str,
        views: int,
        shares: int,
        engagement_rate: float
    ) -> bool:
        """
        Atualiza performance de conteúdo.

        Args:
            content_id: ID do conteúdo
            views: Visualizações
            shares: Compartilhamentos
            engagement_rate: Taxa de engajamento

        Returns:
            True se atualizado com sucesso
        """
        for content in self.content_pieces:
            if content.id == content_id:
                content.views = views
                content.shares = shares
                content.engagement_rate = engagement_rate
                content.status = 'published'
                logger.info(f"📊 Performance de conteúdo atualizada: {content.title}")
                return True

        logger.warning(f"⚠️ Conteúdo não encontrado: {content_id}")
        return False

    def get_brand_health_summary(self) -> Dict[str, Any]:
        """
        Obtém resumo da saúde da marca.

        Returns:
            Dicionário com resumo da brand health
        """
        if not self.brand_health:
            return {'error': 'Sem dados de brand health'}

        # Ordenar períodos
        sorted_periods = sorted(self.brand_health.keys())
        latest = self.brand_health[sorted_periods[-1]]

        # Calcular tendências
        if len(sorted_periods) > 1:
            previous = self.brand_health[sorted_periods[-2]]
            awareness_change = latest.unaided_awareness - previous.unaided_awareness
            nps_change = latest.nps - previous.nps
            sov_change = latest.sov - previous.sov
            equity_change = latest.brand_equity_score - previous.brand_equity_score
        else:
            awareness_change = 0
            nps_change = 0
            sov_change = 0
            equity_change = 0

        return {
            'latest': {
                'period': latest.period,
                'unaided_awareness': latest.unaided_awareness,
                'aided_awareness': latest.aided_awareness,
                'consideration': latest.consideration,
                'nps': latest.nps,
                'sov': latest.sov,
                'share_of_search': latest.share_of_search,
                'positive_sentiment': latest.positive_sentiment,
                'negative_sentiment': latest.negative_sentiment,
                'brand_equity_score': latest.brand_equity_score,
                'brand_trend': latest.brand_trend
            },
            'trends': {
                'awareness_change': awareness_change,
                'nps_change': nps_change,
                'sov_change': sov_change,
                'equity_change': equity_change
            },
            'history': [
                {
                    'period': period,
                    'equity_score': health.brand_equity_score,
                    'nps': health.nps,
                    'sov': health.sov
                }
                for period, health in self.brand_health.items()
            ]
        }

    def get_social_sentiment_analysis(
        self,
        period: Optional[str] = None,
        platform: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analisa sentimento de menções sociais.

        Args:
            period: Filtrar por período (ex: 2026-03)
            platform: Filtrar por plataforma

        Returns:
            Dicionário com análise de sentimento
        """
        # Filtrar menções
        mentions = self.social_mentions
        if period:
            mentions = [m for m in mentions if m.date.startswith(period)]
        if platform:
            mentions = [m for m in mentions if m.platform == platform]

        if not mentions:
            return {'error': 'Sem menções para analisar'}

        # Calcular distribuição de sentimento
        total = len(mentions)
        positive = sum(1 for m in mentions if m.sentiment == 'positive')
        neutral = sum(1 for m in mentions if m.sentiment == 'neutral')
        negative = sum(1 for m in mentions if m.sentiment == 'negative')

        # Calcular engajamento por sentimento
        engagement_by_sentiment = {
            'positive': sum(m.engagement for m in mentions if m.sentiment == 'positive'),
            'neutral': sum(m.engagement for m in mentions if m.sentiment == 'neutral'),
            'negative': sum(m.engagement for m in mentions if m.sentiment == 'negative')
        }

        # Identificar tópicos mais mencionados
        topics = {}
        for m in mentions:
            if m.topic:
                topics[m.topic] = topics.get(m.topic, 0) + 1

        # Influenciadores
        influencer_mentions = [m for m in mentions if m.influencer]

        return {
            'total_mentions': total,
            'sentiment_distribution': {
                'positive': {'count': positive, 'percentage': positive / total * 100 if total > 0 else 0},
                'neutral': {'count': neutral, 'percentage': neutral / total * 100 if total > 0 else 0},
                'negative': {'count': negative, 'percentage': negative / total * 100 if total > 0 else 0}
            },
            'engagement_by_sentiment': engagement_by_sentiment,
            'top_topics': sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5],
            'influencer_mentions': len(influencer_mentions),
            'avg_engagement': sum(m.engagement for m in mentions) / total if total > 0 else 0
        }

    def get_pr_impact_summary(self) -> Dict[str, Any]:
        """
        Obtém resumo de impacto de PR.

        Returns:
            Dicionário com resumo de PR
        """
        if not self.pr_activities:
            return {'error': 'Sem atividades de PR'}

        total_reach = sum(a.reach for a in self.pr_activities)
        positive = sum(1 for a in a.pr_activities if a.sentiment == 'positive')
        
        # Agrupar por tipo
        by_type = {}
        for activity in self.pr_activities:
            if activity.type not in by_type:
                by_type[activity.type] = []
            by_type[activity.type].append(activity)

        # Agrupar por outlet
        by_outlet = {}
        for activity in self.pr_activities:
            if activity.outlet not in by_outlet:
                by_outlet[activity.outlet] = []
            by_outlet[activity.outlet].append(activity)

        return {
            'total_activities': len(self.pr_activities),
            'total_reach': total_reach,
            'positive_coverage': positive / len(self.pr_activities) * 100,
            'by_type': {t: len(activities) for t, activities in by_type.items()},
            'top_outlets': sorted(
                [(outlet, sum(a.reach for a in activities)) for outlet, activities in by_outlet.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

    def _calculate_brand_equity(
        self,
        unaided_awareness: float,
        aided_awareness: float,
        consideration: float,
        nps: float,
        sov: float,
        positive_sentiment: float,
        negative_sentiment: float
    ) -> float:
        """Calcula brand equity score (0-100)."""
        # Ponderação de componentes
        awareness_score = (unaided_awareness * 0.6 + aided_awareness * 0.4) * 0.25
        consideration_score = consideration * 0.25
        loyalty_score = (nps / 100) * 0.25
        visibility_score = (sov / 100) * 0.15
        sentiment_score = ((positive_sentiment - negative_sentiment) / 100 + 1) / 2 * 0.10

        return min(100, max(0, awareness_score + consideration_score + loyalty_score + visibility_score + sentiment_score))

    def _determine_brand_trend(self, period: str, current_equity: float) -> str:
        """Determina tendência da marca."""
        # Obter período anterior
        if len(self.brand_health) < 1:
            return "stable"

        # Simplificado: comparar com média dos últimos períodos
        avg_equity = sum(h.brand_equity_score for h in self.brand_health.values()) / len(self.brand_health)

        if current_equity > avg_equity * 1.05:
            return "improving"
        elif current_equity < avg_equity * 0.95:
            return "declining"
        else:
            return "stable"

    def write_brand_report_to_obsidian(
        self,
        tenant_name: str,
        obsidian_path: str
    ) -> str:
        """
        Escreve relatório de Brand no Obsidian.

        Args:
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        brand_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "10 - Brand & Communication",
            tenant_name
        )
        os.makedirs(brand_path, exist_ok=True)

        # Obter dados
        brand_summary = self.get_brand_health_summary()
        sentiment_analysis = self.get_social_sentiment_analysis()
        pr_summary = self.get_pr_impact_summary()

        # Conteúdo
        content = f"""---
tags: [brand, communication, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 🏛️ Brand & Communication - {tenant_name}

**Gerado em:** {timestamp}

---

## 📊 Brand Health

"""

        if 'error' not in brand_summary:
            latest = brand_summary.get('latest', {})
            trends = brand_summary.get('trends', {})

            # Ícones de tendência
            def trend_icon(change):
                if change > 2: return "🟢 ↑"
                elif change < -2: return "🔴 ↓"
                else: return "🟡 →"

            content += f"""
### Métricas Principais

| Métrica | Valor | Tendência |
| :------ | :---- | :-------- |
| **Brand Awareness (Unaided)** | {latest.get('unaided_awareness', 0):.1f}% | {trend_icon(trends.get('awareness_change', 0))} {trends.get('awareness_change', 0):+.1f}% |
| **NPS** | {latest.get('nps', 0):.0f} | {trend_icon(trends.get('nps_change', 0))} {trends.get('nps_change', 0):+.0f} |
| **Share of Voice** | {latest.get('sov', 0):.1f}% | {trend_icon(trends.get('sov_change', 0))} {trends.get('sov_change', 0):+.1f}% |
| **Share of Search** | {latest.get('share_of_search', 0):.1f}% | - |

### Brand Equity

**Score:** {latest.get('brand_equity_score', 0):.1f}/100

**Tendência:** {latest.get('brand_trend', 'stable').title()}

### Sentimento

| Positivo | Neutro | Negativo |
| :------: | :----: | :------: |
| {latest.get('positive_sentiment', 0):.1f}% | {100 - latest.get('positive_sentiment', 0) - latest.get('negative_sentiment', 0):.1f}% | {latest.get('negative_sentiment', 0):.1f}% |

"""

            # Histórico de equity
            history = brand_summary.get('history', [])
            if history:
                content += "### Histórico de Brand Equity\n\n"
                content += "| Período | Equity Score | NPS | SOV |\n"
                content += "| :------ | :----------: | :-- | :-- |\n"
                for h in history[-6:]:  # Últimos 6 períodos
                    content += f"| {h['period']} | {h['equity_score']:.1f} | {h['nps']:.0f} | {h['sov']:.1f}% |\n"
        else:
            content += f"> {brand_summary.get('error', 'Sem dados')}\n"

        # Seção de Social Sentiment
        content += """
---

## 📱 Social Sentiment

"""

        if 'error' not in sentiment_analysis:
            dist = sentiment_analysis.get('sentiment_distribution', {})
            content += f"""
### Distribuição de Sentimento

| Sentimento | Menções | % | Engajamento |
| :--------- | :-----: | :- | :---------- |
| 😊 Positivo | {dist.get('positive', {}).get('count', 0)} | {dist.get('positive', {}).get('percentage', 0):.1f}% | {sentiment_analysis.get('engagement_by_sentiment', {}).get('positive', 0)} |
| 😐 Neutro | {dist.get('neutral', {}).get('count', 0)} | {dist.get('neutral', {}).get('percentage', 0):.1f}% | {sentiment_analysis.get('engagement_by_sentiment', {}).get('neutral', 0)} |
| 😠 Negativo | {dist.get('negative', {}).get('count', 0)} | {dist.get('negative', {}).get('percentage', 0):.1f}% | {sentiment_analysis.get('engagement_by_sentiment', {}).get('negative', 0)} |

**Total de Menções:** {sentiment_analysis.get('total_mentions', 0)}
**Menções de Influenciadores:** {sentiment_analysis.get('influencer_mentions', 0)}
**Engajamento Médio:** {sentiment_analysis.get('avg_engagement', 0):.0f}

### Tópicos Mais Mencionados

"""
            for topic, count in sentiment_analysis.get('top_topics', [])[:5]:
                content += f"- **{topic}**: {count} menções\n"
        else:
            content += f"> {sentiment_analysis.get('error', 'Sem dados')}\n"

        # Seção de PR
        content += """
---

## 📰 Public Relations

"""

        if 'error' not in pr_summary:
            content += f"""
### Resumo de Impacto

| Métrica | Valor |
| :------ | :---- |
| **Total Atividades** | {pr_summary.get('total_activities', 0)} |
| **Alcance Total** | {pr_summary.get('total_reach', 0):,} |
| **Cobertura Positiva** | {pr_summary.get('positive_coverage', 0):.1f}% |

### Top Veículos

"""
            for outlet, reach in pr_summary.get('top_outlets', [])[:5]:
                content += f"- **{outlet}**: {reach:,} alcance\n"
        else:
            content += f"> {pr_summary.get('error', 'Sem dados')}\n"

        # Conteúdos de Brand
        content += """
---

## 📝 Conteúdos de Brand

"""

        if self.content_pieces:
            content += "| Título | Formato | Canal | Status | Views | Shares |\n"
            content += "| :----- | :------ | :---- | :----- | :---- | :----- |\n"
            for c in self.content_pieces[-10:]:  # Últimos 10
                status_icon = {'published': '✅', 'planned': '📋', 'promoted': '📢'}.get(c.status, '⚪')
                content += (
                    f"| {c.title[:40]} | {c.format} | {c.channel} | "
                    f"{status_icon} {c.status.title()} | {c.views:,} | {c.shares:,} |\n"
                )
        else:
            content += "> Nenhum conteúdo registrado.\n"

        # Recomendações
        content += """
---

## 💡 Recomendações

"""

        recommendations = self._generate_brand_recommendations()
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"

        content += f"""
---

## 📅 Próximas Ações

- [ ] Monitorar brand health mensalmente
- [ ] Analisar sentimento de menções sociais (semanal)
- [ ] Planejar próximos conteúdos de brand
- [ ] Acompanhar share of voice vs concorrentes
- [ ] Revisar estratégia de comunicação

---

*Gerado automaticamente pelo Exocórtex v5.3 — Brand & Communication Engine*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Brand-Communication-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(brand_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"🏛️ Relatório de Brand escrito no Obsidian: {filepath}")
        return filepath

    def _generate_brand_recommendations(self) -> List[str]:
        """Gera recomendações baseadas em dados de brand."""
        recommendations = []

        # Analisar brand health
        if self.brand_health:
            latest = list(self.brand_health.values())[-1]

            if latest.unaided_awareness < 30:
                recommendations.append("📢 Aumentar investimento em brand awareness (atual < 30%)")

            if latest.nps < 50:
                recommendations.append("💚 Implementar programa de melhoria de NPS")

            if latest.sov < 20:
                recommendations.append("📈 Aumentar share of voice (atual < 20%)")

            if latest.negative_sentiment > 30:
                recommendations.append("⚠️ Atenção: Sentimento negativo alto — revisar comunicação")

        # Analisar sentiment
        if self.social_mentions:
            recent_mentions = self.social_mentions[-50:]
            negative_count = sum(1 for m in recent_mentions if m.sentiment == 'negative')
            if negative_count > len(recent_mentions) * 0.2:
                recommendations.append("🚨 Monitorar crise: +20% de menções negativas recentes")

        if not recommendations:
            recommendations.append("✅ Brand health dentro do esperado")

        return recommendations[:5]
