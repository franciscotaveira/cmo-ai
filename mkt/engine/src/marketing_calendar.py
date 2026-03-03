"""
╔═══════════════════════════════════════════════════════════════════════════════
║ MARKETING CALENDAR — Calendário de Marketing (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Gerencia calendário de campanhas, conteúdos e tarefas recorrentes
║ Integra com Obsidian para visualização temporal
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class CampaignType(Enum):
    """Tipos de campanha."""
    ACQUISITION = "acquisition"
    RETENTION = "retention"
    LAUNCH = "launch"
    PROMOTION = "promotion"
    BRANDING = "branding"
    EDUCATION = "education"


class Channel(Enum):
    """Canais de marketing."""
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    PAID_ADS = "paid_ads"
    CONTENT = "content"
    SEO = "seo"
    EVENTS = "events"
    PARTNERSHIPS = "partnerships"


@dataclass
class Campaign:
    """Campanha de marketing."""
    id: str
    title: str
    description: str
    campaign_type: str
    channels: List[str]
    start_date: str
    end_date: str
    budget: float
    target_audience: str
    goals: List[str]
    kpi_metrics: Dict[str, float]
    status: str  # planned, active, paused, completed
    tenant_id: str
    tenant_name: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContentPiece:
    """Peça de conteúdo."""
    id: str
    title: str
    content_type: str  # blog, video, social, email, etc.
    channel: str
    publish_date: str
    status: str  # idea, draft, review, scheduled, published
    author: str
    campaign_id: Optional[str]
    tenant_id: str
    keywords: List[str]
    cta: str


@dataclass
class RecurringTask:
    """Tarefa recorrente de marketing."""
    id: str
    title: str
    description: str
    frequency: str  # daily, weekly, biweekly, monthly, quarterly
    day_of_week: Optional[int] = None  # 0=Monday, 6=Sunday
    day_of_month: Optional[int] = None  # 1-31
    responsible: str = "Marketing Team"
    estimated_hours: float = 1.0
    tenant_id: str = "global"
    related_metrics: List[str] = field(default_factory=list)
    last_completed: Optional[str] = None
    next_due: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))


class MarketingCalendar:
    """
    Calendário de Marketing.

    Gerencia:
    • Campanhas com timeline
    • Conteúdos programados
    • Tarefas recorrentes
    • Visualização no Obsidian
    """

    # Templates de campanhas por objetivo
    CAMPAIGN_TEMPLATES = {
        'black_friday': {
            'title': 'Black Friday',
            'type': CampaignType.PROMOTION,
            'duration_days': 7,
            'channels': [Channel.EMAIL, Channel.PAID_ADS, Channel.SOCIAL_MEDIA],
            'budget_multiplier': 3.0
        },
        'product_launch': {
            'title': 'Lançamento de Produto',
            'type': CampaignType.LAUNCH,
            'duration_days': 21,
            'channels': [Channel.EMAIL, Channel.SOCIAL_MEDIA, Channel.CONTENT, Channel.EVENTS],
            'budget_multiplier': 2.5
        },
        'brand_awareness': {
            'title': 'Brand Awareness',
            'type': CampaignType.BRANDING,
            'duration_days': 30,
            'channels': [Channel.SOCIAL_MEDIA, Channel.CONTENT, Channel.PAID_ADS],
            'budget_multiplier': 1.5
        },
        'customer_retention': {
            'title': 'Retenção de Clientes',
            'type': CampaignType.RETENTION,
            'duration_days': 14,
            'channels': [Channel.EMAIL, Channel.SOCIAL_MEDIA],
            'budget_multiplier': 1.0
        },
        'lead_generation': {
            'title': 'Geração de Leads',
            'type': CampaignType.ACQUISITION,
            'duration_days': 21,
            'channels': [Channel.PAID_ADS, Channel.CONTENT, Channel.EMAIL],
            'budget_multiplier': 2.0
        }
    }

    # Tarefas recorrentes padrão
    RECURRING_TASKS_TEMPLATES = [
        RecurringTask(
            id='weekly-report',
            title='Relatório Semanal de Performance',
            description='Compilar e analisar métricas da semana',
            frequency='weekly',
            day_of_week=0,  # Segunda-feira
            responsible='Marketing Analyst',
            estimated_hours=2.0,
            related_metrics=['revenue', 'cac', 'conversion_rate'],
            last_completed=None,
            next_due=datetime.now().strftime('%Y-%m-%d')
        ),
        RecurringTask(
            id='monthly-review',
            title='Revisão Mensal de Estratégia',
            description='Revisar performance do mês e ajustar estratégia',
            frequency='monthly',
            day_of_month=1,
            responsible='Marketing Director',
            estimated_hours=4.0,
            related_metrics=['revenue', 'ltv', 'churn_rate', 'roi'],
            last_completed=None,
            next_due=datetime.now().strftime('%Y-%m-%d')
        ),
        RecurringTask(
            id='content-planning',
            title='Planejamento de Conteúdo',
            description='Planejar conteúdos das próximas 2 semanas',
            frequency='biweekly',
            day_of_week=3,  # Quarta-feira
            responsible='Content Manager',
            estimated_hours=3.0,
            related_metrics=['organic_traffic', 'engagement'],
            last_completed=None,
            next_due=datetime.now().strftime('%Y-%m-%d')
        ),
        RecurringTask(
            id='campaign-optimization',
            title='Otimização de Campanhas',
            description='Analisar e otimizar campanhas ativas',
            frequency='weekly',
            day_of_week=2,  # Terça-feira
            responsible='Growth Manager',
            estimated_hours=2.5,
            related_metrics=['roas', 'ctr', 'conversion_rate'],
            last_completed=None,
            next_due=datetime.now().strftime('%Y-%m-%d')
        ),
        RecurringTask(
            id='seo-audit',
            title='Auditoria SEO',
            description='Revisar performance SEO e identificar oportunidades',
            frequency='monthly',
            day_of_month=15,
            responsible='SEO Specialist',
            estimated_hours=4.0,
            related_metrics=['organic_traffic', 'rankings', 'backlinks'],
            last_completed=None,
            next_due=datetime.now().strftime('%Y-%m-%d')
        )
    ]

    def __init__(self):
        """Inicializa o Marketing Calendar."""
        self.campaigns: List[Campaign] = []
        self.content_pieces: List[ContentPiece] = []
        self.recurring_tasks: List[RecurringTask] = self.RECURRING_TASKS_TEMPLATES.copy()
        logger.info("📅 MarketingCalendar inicializado")

    def create_campaign(
        self,
        template_key: str,
        tenant_id: str,
        tenant_name: str,
        start_date: Optional[str] = None,
        budget: Optional[float] = None,
        custom_params: Optional[Dict] = None
    ) -> Campaign:
        """
        Cria campanha baseada em template.

        Args:
            template_key: Chave do template (black_friday, product_launch, etc.)
            tenant_id: ID do tenant
            tenant_name: Nome do tenant
            start_date: Data de início (padrão: hoje)
            budget: Budget da campanha (padrão: calculado)
            custom_params: Parâmetros customizados

        Returns:
            Campaign: Campanha criada
        """
        template = self.CAMPAIGN_TEMPLATES.get(
            template_key,
            self.CAMPAIGN_TEMPLATES['lead_generation']
        )

        if start_date is None:
            start_date = datetime.now()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        end_date = start_date + timedelta(days=template['duration_days'])

        # Budget padrão baseado no tipo
        if budget is None:
            budget = self._calculate_default_budget(template, tenant_id)

        # Metas padrão
        goals = self._generate_campaign_goals(template, budget)

        campaign = Campaign(
            id=f"camp-{template_key}-{tenant_id}-{start_date.strftime('%Y%m%d')}",
            title=custom_params.get('title', template['title']) if custom_params else template['title'],
            description=custom_params.get('description', f"Campanha de {template['type'].value}") if custom_params else f"Campanha de {template['type'].value}",
            campaign_type=template['type'].value,
            channels=[c.value for c in template['channels']],
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            budget=budget,
            target_audience=custom_params.get('target_audience', 'Público geral') if custom_params else 'Público geral',
            goals=goals,
            kpi_metrics=self._generate_kpi_metrics(template, budget),
            status='planned',
            tenant_id=tenant_id,
            tenant_name=tenant_name
        )

        self.campaigns.append(campaign)
        logger.info(f"📢 Campanha criada: {campaign.title} para {tenant_name}")
        return campaign

    def schedule_content(
        self,
        title: str,
        content_type: str,
        channel: str,
        publish_date: str,
        tenant_id: str,
        author: str = "Content Team",
        campaign_id: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        cta: str = "Saiba mais"
    ) -> ContentPiece:
        """
        Agenda peça de conteúdo.

        Args:
            title: Título do conteúdo
            content_type: Tipo (blog, video, social, etc.)
            channel: Canal de publicação
            publish_date: Data de publicação
            tenant_id: ID do tenant
            author: Autor/responsável
            campaign_id: ID da campanha relacionada (opcional)
            keywords: Palavras-chave
            cta: Call-to-action

        Returns:
            ContentPiece: Conteúdo agendado
        """
        content = ContentPiece(
            id=f"content-{tenant_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            content_type=content_type,
            channel=channel,
            publish_date=publish_date,
            status='scheduled',
            author=author,
            campaign_id=campaign_id,
            tenant_id=tenant_id,
            keywords=keywords or [],
            cta=cta
        )

        self.content_pieces.append(content)
        logger.info(f"📝 Conteúdo agendado: {title} para {publish_date}")
        return content

    def update_recurring_tasks(
        self,
        task_id: str,
        last_completed: str,
        next_due: str
    ) -> bool:
        """
        Atualiza tarefa recorrente completada.

        Args:
            task_id: ID da tarefa
            last_completed: Data da última conclusão
            next_due: Próxima data de vencimento

        Returns:
            True se atualizado com sucesso
        """
        for task in self.recurring_tasks:
            if task.id == task_id:
                task.last_completed = last_completed
                task.next_due = next_due
                logger.info(f"✅ Tarefa recorrente atualizada: {task.title}")
                return True

        logger.warning(f"⚠️ Tarefa não encontrada: {task_id}")
        return False

    def get_upcoming_tasks(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Obtém tarefas dos próximos dias.

        Args:
            days: Número de dias para frente

        Returns:
            Lista de tarefas próximas
        """
        upcoming = []
        today = datetime.now()
        cutoff = today + timedelta(days=days)

        # Tarefas recorrentes
        for task in self.recurring_tasks:
            try:
                due_date = datetime.strptime(task.next_due, '%Y-%m-%d')
                if today <= due_date <= cutoff:
                    upcoming.append({
                        'type': 'recurring_task',
                        'id': task.id,
                        'title': task.title,
                        'due_date': task.next_due,
                        'responsible': task.responsible,
                        'estimated_hours': task.estimated_hours
                    })
            except:
                pass

        # Conteúdos para publicar
        for content in self.content_pieces:
            if content.status == 'scheduled':
                try:
                    publish_date = datetime.strptime(content.publish_date, '%Y-%m-%d')
                    if today <= publish_date <= cutoff:
                        upcoming.append({
                            'type': 'content',
                            'id': content.id,
                            'title': content.title,
                            'due_date': content.publish_date,
                            'responsible': content.author,
                            'channel': content.channel
                        })
                except:
                    pass

        # Ordenar por data
        upcoming.sort(key=lambda x: x['due_date'])

        return upcoming

    def write_calendar_to_obsidian(
        self,
        tenant_name: str,
        obsidian_path: str,
        months_ahead: int = 3
    ) -> str:
        """
        Escreve calendário no Obsidian.

        Args:
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault
            months_ahead: Meses para mostrar

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        calendar_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "06 - Calendário",
            tenant_name
        )
        os.makedirs(calendar_path, exist_ok=True)

        # Filtrar campanhas do tenant
        tenant_campaigns = [c for c in self.campaigns if c.tenant_name == tenant_name]
        tenant_campaigns.sort(key=lambda x: x.start_date)

        # Filtrar conteúdos do tenant
        tenant_content = [c for c in self.content_pieces if (not tenant_campaigns) or (c.tenant_id == tenant_campaigns[0].tenant_id)]
        tenant_content.sort(key=lambda x: x.publish_date)

        # Gerar conteúdo
        content = f"""---
tags: [calendario, marketing, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 📅 Calendário de Marketing - {tenant_name}

**Gerado em:** {timestamp}

---

## 🗓️ Visão Geral

"""

        # Timeline visual
        content += self._generate_timeline_visual(tenant_campaigns, months_ahead)

        content += """
---

## 📢 Campanhas

"""

        # Campanhas por status
        campaigns_by_status = {'planned': [], 'active': [], 'paused': [], 'completed': []}
        for campaign in tenant_campaigns:
            campaigns_by_status[campaign.status].append(campaign)

        status_config = {
            'planned': {'icon': '📋', 'label': 'Planejadas'},
            'active': {'icon': '🔴', 'label': 'Ativas'},
            'paused': {'icon': '⏸️', 'label': 'Pausadas'},
            'completed': {'icon': '✅', 'label': 'Completadas'}
        }

        for status, config in status_config.items():
            campaigns = campaigns_by_status[status]
            if campaigns:
                content += f"\n### {config['icon']} {config['label']}\n\n"
                for campaign in campaigns:
                    content += self._format_campaign_card(campaign)

        content += """
---

## 📝 Conteúdos Programados

"""

        if tenant_content:
            content += "| Data | Título | Tipo | Canal | Status |\n"
            content += "| :--- | :---- | :--- | :---- | :----- |\n"
            for c in tenant_content[:20]:  # Limite de 20
                status_icon = {'scheduled': '📅', 'published': '✅', 'draft': '📝', 'review': '👀'}.get(c.status, '❓')
                content += f"| {c.publish_date} | {c.title[:40]} | {c.content_type} | {c.channel} | {status_icon} |\n"
        else:
            content += "> Nenhum conteúdo programado.\n"

        content += """
---

## 🔄 Tarefas Recorrentes

"""

        # Tarefas recorrentes
        content += "| Tarefa | Frequência | Responsável | Próxima |\n"
        content += "| :----- | :--------- | :---------- | :------ |\n"
        for task in self.recurring_tasks:
            content += f"| {task.title} | {self._format_frequency(task.frequency)} | {task.responsible} | {task.next_due} |\n"

        content += """
---

## 📊 Próximos 7 Dias

"""

        upcoming = self.get_upcoming_tasks(days=7)
        if upcoming:
            for item in upcoming:
                content += f"- **{item['due_date']}** | {item['title']} | {item.get('responsible', 'N/A')}\n"
        else:
            content += "> Nenhuma tarefa nos próximos 7 dias.\n"

        content += f"""
---

## 📈 Dataview Queries

### Todas as Campanhas

```dataview
TABLE campaign_type as "Tipo", start_date as "Início", end_date as "Fim", budget as "Budget", status as "Status"
FROM "🧠 EXOCÓRTEX/06 - Calendário/{tenant_name}"
WHERE contains(tags, "campanha")
SORT start_date ASC
```

### Conteúdos Publicados

```dataview
TABLE publish_date as "Data", channel as "Canal", status as "Status"
FROM "🧠 EXOCÓRTEX/06 - Calendário/{tenant_name}"
WHERE contains(tags, "conteudo") AND status = "published"
SORT publish_date DESC
LIMIT 10
```

---

*Gerado automaticamente pelo Exocórtex v5.0 — Marketing Calendar*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Calendario-{safe_name}-{datetime.now().strftime('%Y%m')}.md"
        filepath = os.path.join(calendar_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📅 Calendário escrito no Obsidian: {filepath}")
        return filepath

    def _generate_timeline_visual(
        self,
        campaigns: List[Campaign],
        months_ahead: int
    ) -> str:
        """Gera timeline visual em formato de calendário."""
        content = "```\n"
        content += "=" * 60 + "\n"
        content += "TIMELINE DE CAMPANHAS\n"
        content += "=" * 60 + "\n\n"

        # Gerar meses
        today = datetime.now()
        for i in range(months_ahead):
            month_date = today + timedelta(days=30 * i)
            month_name = month_date.strftime('%B %Y')
            content += f"📍 {month_name}\n"
            content += "-" * 40 + "\n"

            # Campanhas do mês
            month_campaigns = [
                c for c in campaigns
                if self._is_in_month(c.start_date, month_date) or
                   self._is_in_month(c.end_date, month_date)
            ]

            if month_campaigns:
                for campaign in month_campaigns:
                    status_icon = {'active': '🔴', 'planned': '📋', 'completed': '✅'}.get(campaign.status, '⚪')
                    content += f"  {status_icon} {campaign.title}\n"
                    content += f"     {campaign.start_date} → {campaign.end_date}\n"
            else:
                content += "  (sem campanhas)\n"

            content += "\n"

        content += "=" * 60 + "\n"
        content += "```\n"
        return content

    def _format_campaign_card(self, campaign: Campaign) -> str:
        """Formata cartão de campanha."""
        content = f"""
#### {campaign.title}

| Campo | Detalhe |
| :---- | :------ |
| **Período** | {campaign.start_date} → {campaign.end_date} |
| **Tipo** | {campaign.campaign_type.title()} |
| **Budget** | R$ {campaign.budget:,.2f} |
| **Canais** | {', '.join(campaign.channels)} |
| **Status** | {campaign.status.title()} |

**Público-alvo:** {campaign.target_audience}

**Metas:**
"""
        for goal in campaign.goals:
            content += f"- {goal}\n"

        content += "\n---\n"
        return content

    def _format_frequency(self, frequency: str) -> str:
        """Formata frequência em português."""
        freq_map = {
            'daily': 'Diária',
            'weekly': 'Semanal',
            'biweekly': 'Quinzenal',
            'monthly': 'Mensal',
            'quarterly': 'Trimestral'
        }
        return freq_map.get(frequency, frequency.title())

    def _is_in_month(self, date_str: str, month_date: datetime) -> bool:
        """Verifica se data está no mês especificado."""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date.year == month_date.year and date.month == month_date.month
        except:
            return False

    def _calculate_default_budget(
        self,
        template: Dict,
        tenant_id: str
    ) -> float:
        """Calcula budget padrão baseado no template."""
        # Budget base simulado (na prática viria do tenant)
        base_budget = 5000.0

        multiplier = template.get('budget_multiplier', 1.0)
        return base_budget * multiplier

    def _generate_campaign_goals(
        self,
        template: Dict,
        budget: float
    ) -> List[str]:
        """Gera metas para campanha."""
        goals = []

        campaign_type = template['type']

        if campaign_type == CampaignType.ACQUISITION:
            cpa_target = budget / 100  # 100 aquisições
            goals.append(f"Gerar 100 novos leads/clientes")
            goals.append(f"CPA máximo de R$ {cpa_target:.2f}")
            goals.append(f"ROI de 3x no primeiro mês")

        elif campaign_type == CampaignType.RETENTION:
            goals.append(f"Reduzir churn em 15% durante a campanha")
            goals.append(f"Aumentar re-engajamento em 25%")
            goals.append(f"Gerar 20% de receita recorrente adicional")

        elif campaign_type == CampaignType.LAUNCH:
            goals.append(f"Alcançar 10.000 impressões")
            goals.append(f"Gerar 500 leads no lançamento")
            goals.append(f"Converter 10% em clientes pagantes")

        elif campaign_type == CampaignType.BRANDING:
            goals.append(f"Aumentar brand awareness em 20%")
            goals.append(f"Gerar 50.000 reach nas redes sociais")
            goals.append(f"Aumentar seguidores em 15%")

        else:  # PROMOTION
            goals.append(f"Aumentar vendas em 50% durante o período")
            goals.append(f"Gerar R$ {budget * 5:,.2f} em receita")
            goals.append(f"ROAS mínimo de 4x")

        return goals

    def _generate_kpi_metrics(
        self,
        template: Dict,
        budget: float
    ) -> Dict[str, float]:
        """Gera KPIs esperados para campanha."""
        kpis = {
            'budget': budget,
            'impressions': budget * 100,  # CPM estimado
            'clicks': budget * 2,  # CPC estimado
            'conversions': budget / 50,  # CPA estimado
            'revenue': budget * 4  # ROAS estimado de 4x
        }

        return kpis

    def generate_calendar_for_all_tenants(
        self,
        tenants_data: List[Dict[str, Any]],
        obsidian_path: str
    ) -> Dict[str, str]:
        """
        Gera calendário para todos os tenants.

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

            # Só criar campanha se não houver nenhuma planejada
            if not any(c.status == 'planned' for c in self.campaigns if c.tenant_id == tenant_id):
                self.create_campaign(
                    template_key='lead_generation',
                    tenant_id=tenant_id,
                    tenant_name=tenant_name,
                    start_date=datetime.now().strftime('%Y-%m-%d')
                )

            # Escrever calendário
            filepath = self.write_calendar_to_obsidian(
                tenant_name=tenant_name,
                obsidian_path=obsidian_path
            )

            results[tenant_name] = filepath

        return results
