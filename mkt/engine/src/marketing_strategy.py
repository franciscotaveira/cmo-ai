"""
╔═══════════════════════════════════════════════════════════════════════════════
║ MARKETING STRATEGY ENGINE — Estratégias Automáticas (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Gera estratégias e planos de ação baseados em métricas e anomalias
║ Integra com Obsidian para escrever estratégias automaticamente
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """Tipos de estratégia de marketing."""
    GROWTH = "growth"
    RETENTION = "retention"
    ACQUISITION = "acquisition"
    OPTIMIZATION = "optimization"
    BRANDING = "branding"
    CONVERSION = "conversion"


class Priority(Enum):
    """Níveis de prioridade."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ActionItem:
    """Item de ação dentro de um plano."""
    title: str
    description: str
    responsible: str
    deadline_days: int
    effort: str  # low, medium, high
    kpi: str
    expected_impact: str


@dataclass
class Strategy:
    """Estratégia de marketing gerada."""
    title: str
    strategy_type: str
    priority: str
    tenant_id: str
    tenant_name: str
    context: str
    diagnosis: str
    objective: str
    key_results: List[str]
    action_plan: List[ActionItem]
    budget_estimate: float
    expected_roi: float
    timeline_weeks: int
    created_at: str


class MarketingStrategyEngine:
    """
    Motor de Estratégias de Marketing.

    Gera estratégias automaticamente baseadas em:
    • Métricas de desempenho (CAC, LTV, Conversão, etc.)
    • Anomalias detectadas (Z-Score)
    • Tipo de negócio
    • Benchmarks do setor
    """

    # Benchmarks por tipo de negócio
    BENCHMARKS = {
        'ecommerce': {
            'cac_ideal': 30.0,
            'ltv_ideal': 150.0,
            'conversion_rate_ideal': 2.5,
            'roi_ideal': 4.0,
            'churn_ideal': 5.0
        },
        'saas': {
            'cac_ideal': 100.0,
            'ltv_ideal': 600.0,
            'conversion_rate_ideal': 5.0,
            'roi_ideal': 3.0,
            'churn_ideal': 3.0
        },
        'servicos': {
            'cac_ideal': 50.0,
            'ltv_ideal': 300.0,
            'conversion_rate_ideal': 10.0,
            'roi_ideal': 5.0,
            'churn_ideal': 8.0
        },
        'imobiliario': {
            'cac_ideal': 200.0,
            'ltv_ideal': 2000.0,
            'conversion_rate_ideal': 3.0,
            'roi_ideal': 6.0,
            'churn_ideal': 15.0
        },
        'default': {
            'cac_ideal': 50.0,
            'ltv_ideal': 300.0,
            'conversion_rate_ideal': 3.0,
            'roi_ideal': 4.0,
            'churn_ideal': 5.0
        }
    }

    # Templates de estratégias por problema
    STRATEGY_TEMPLATES = {
        'cac_alto': {
            'title': 'Otimização de Aquisição - Redução de CAC',
            'type': StrategyType.OPTIMIZATION,
            'diagnosis': 'CAC acima do benchmark indica ineficiência na aquisição',
            'objective': 'Reduzir CAC em 30% mantendo volume de aquisições',
            'actions': [
                ActionItem(
                    title='Auditoria de Canais Pagos',
                    description='Analisar ROI por canal e identificar canais ineficientes',
                    responsible='Growth Manager',
                    deadline_days=7,
                    effort='medium',
                    kpi='ROI por canal',
                    expected_impact='Identificar 20-30% de economia potencial'
                ),
                ActionItem(
                    title='Otimização de Landing Pages',
                    description='Melhorar conversão de LPs para reduzir CPA',
                    responsible='CRO Specialist',
                    deadline_days=14,
                    effort='high',
                    kpi='Conversion Rate',
                    expected_impact='Aumento de 15-25% na conversão'
                ),
                ActionItem(
                    title='Implementar Retargeting',
                    description='Criar campanhas de retargeting para recuperar abandonos',
                    responsible='Media Buyer',
                    deadline_days=10,
                    effort='medium',
                    kpi='Retargeting Conversion Rate',
                    expected_impact='Recuperar 10-15% de visitantes perdidos'
                ),
                ActionItem(
                    title='Estratégia de Conteúdo Orgânico',
                    description='Desenvolver conteúdo SEO para reduzir dependência de paid',
                    responsible='Content Manager',
                    deadline_days=30,
                    effort='high',
                    kpi='Organic Traffic',
                    expected_impact='30-40% de tráfego orgânico em 3 meses'
                )
            ]
        },
        'ltv_baixo': {
            'title': 'Estratégia de Retenção e Lifetime Value',
            'type': StrategyType.RETENTION,
            'diagnosis': 'LTV baixo indica problemas de retenção ou monetização',
            'objective': 'Aumentar LTV em 50% através de retenção e upsell',
            'actions': [
                ActionItem(
                    title='Programa de Fidelidade',
                    description='Criar programa de recompensas para clientes recorrentes',
                    responsible='CRM Manager',
                    deadline_days=21,
                    effort='high',
                    kpi='Repeat Purchase Rate',
                    expected_impact='Aumento de 20-30% em compras repetidas'
                ),
                ActionItem(
                    title='Email Marketing de Nutrição',
                    description='Sequências de email pós-compra para engajamento',
                    responsible='Email Marketing',
                    deadline_days=14,
                    effort='medium',
                    kpi='Email Engagement Rate',
                    expected_impact='15-20% aumento em re-engajamento'
                ),
                ActionItem(
                    title='Estratégia de Upsell/Cross-sell',
                    description='Identificar oportunidades de venda adicional',
                    responsible='Sales Manager',
                    deadline_days=14,
                    effort='medium',
                    kpi='Average Order Value',
                    expected_impact='Aumento de 10-20% no ticket médio'
                ),
                ActionItem(
                    title='Onboarding Otimizado',
                    description='Melhorar experiência inicial do cliente',
                    responsible='Customer Success',
                    deadline_days=21,
                    effort='high',
                    kpi='Day-30 Retention',
                    expected_impact='Redução de 25% em churn inicial'
                )
            ]
        },
        'conversao_baixa': {
            'title': 'Estratégia de Otimização de Conversão',
            'type': StrategyType.CONVERSION,
            'diagnosis': 'Taxa de conversão abaixo do benchmark do setor',
            'objective': 'Aumentar conversão em 50% através de CRO',
            'actions': [
                ActionItem(
                    title='Análise de Funil',
                    description='Mapear funil completo e identificar pontos de abandono',
                    responsible='Analytics Lead',
                    deadline_days=7,
                    effort='low',
                    kpi='Funnel Drop-off Points',
                    expected_impact='Identificar 3-5 oportunidades de melhoria'
                ),
                ActionItem(
                    title='Testes A/B em Elementos-Chave',
                    description='Testar headlines, CTAs, formulários',
                    responsible='CRO Specialist',
                    deadline_days=21,
                    effort='high',
                    kpi='Conversion Rate Lift',
                    expected_impact='10-30% de melhoria por teste'
                ),
                ActionItem(
                    title='Melhoria de Velocidade',
                    description='Otimizar tempo de carregamento do site',
                    responsible='Tech Lead',
                    deadline_days=14,
                    effort='medium',
                    kpi='Page Load Time',
                    expected_impact='Redução de 40% em bounce rate'
                ),
                ActionItem(
                    title='Prova Social',
                    description='Adicionar depoimentos, cases, avaliações',
                    responsible='Content Manager',
                    deadline_days=10,
                    effort='low',
                    kpi='Social Proof Engagement',
                    expected_impact='Aumento de 15-20% em confiança'
                )
            ]
        },
        'churn_alto': {
            'title': 'Estratégia Anti-Churn',
            'type': StrategyType.RETENTION,
            'diagnosis': 'Churn alto indica insatisfação ou falta de valor percebido',
            'objective': 'Reduzir churn em 40% através de ações proativas',
            'actions': [
                ActionItem(
                    title='Análise de Churn',
                    description='Entender motivos de cancelamento (survey, entrevistas)',
                    responsible='Customer Success',
                    deadline_days=14,
                    effort='medium',
                    kpi='Churn Reasons',
                    expected_impact='Identificar top 3 causas de churn'
                ),
                ActionItem(
                    title='Programa de Win-back',
                    description='Campanhas para recuperar clientes cancelados',
                    responsible='CRM Manager',
                    deadline_days=21,
                    effort='medium',
                    kpi='Win-back Rate',
                    expected_impact='Recuperar 10-15% de churned customers'
                ),
                ActionItem(
                    title='Check-ins Proativos',
                    description='Contato regular com clientes em risco',
                    responsible='Customer Success',
                    deadline_days=7,
                    effort='high',
                    kpi='At-risk Retention Rate',
                    expected_impact='Redução de 30% em churn evitável'
                ),
                ActionItem(
                    title='Melhoria de Onboarding',
                    description='Garantir time-to-value rápido para novos clientes',
                    responsible='Product + CS',
                    deadline_days=28,
                    effort='high',
                    kpi='Time to First Value',
                    expected_impact='Redução de 50% no churn inicial'
                )
            ]
        },
        'crescimento_lento': {
            'title': 'Estratégia de Aceleração de Crescimento',
            'type': StrategyType.GROWTH,
            'diagnosis': 'Crescimento abaixo do potencial ou metas',
            'objective': 'Acelerar crescimento em 2x através de expansão',
            'actions': [
                ActionItem(
                    title='Expansão de Canais',
                    description='Identificar e testar novos canais de aquisição',
                    responsible='Growth Manager',
                    deadline_days=30,
                    effort='high',
                    kpi='New Channel ROI',
                    expected_impact='20-30% de receita de novos canais'
                ),
                ActionItem(
                    title='Parcerias Estratégicas',
                    description='Desenvolver parcerias para alcance ampliado',
                    responsible='BD Manager',
                    deadline_days=45,
                    effort='medium',
                    kpi='Partner-sourced Revenue',
                    expected_impact='15-25% de leads via parceiros'
                ),
                ActionItem(
                    title='Programa de Referral',
                    description='Incentivar clientes a indicar novos clientes',
                    responsible='Growth Manager',
                    deadline_days=21,
                    effort='medium',
                    kpi='Referral Rate',
                    expected_impact='10-20% de aquisições via referral'
                ),
                ActionItem(
                    title='Escala de Paid Media',
                    description='Aumentar investimento em canais performáticos',
                    responsible='Media Buyer',
                    deadline_days=14,
                    effort='low',
                    kpi='Scaled ROAS',
                    expected_impact='30-50% aumento em volume mantendo ROI'
                )
            ]
        }
    }

    def __init__(self, obsidian_bridge=None):
        """
        Inicializa o Motor de Estratégias.

        Args:
            obsidian_bridge: Instância de ObsidianBridge para escrever estratégias
        """
        self.obsidian_bridge = obsidian_bridge
        logger.info("🧠 MarketingStrategyEngine inicializado")

    def analyze_and_generate_strategy(
        self,
        tenant_id: str,
        tenant_name: str,
        tenant_type: str,
        metrics: Dict[str, float],
        anomalies: Optional[List[Dict]] = None
    ) -> Strategy:
        """
        Analisa métricas e gera estratégia automaticamente.

        Args:
            tenant_id: ID do tenant
            tenant_name: Nome do tenant
            tenant_type: Tipo de negócio (ecommerce, saas, servicos, etc.)
            metrics: Dicionário com métricas atuais
            anomalies: Lista de anomalias detectadas (opcional)

        Returns:
            Strategy: Estratégia gerada
        """
        # Obter benchmarks para o tipo de negócio
        benchmarks = self.BENCHMARKS.get(tenant_type, self.BENCHMARKS['default'])

        # Identificar problemas
        problems = self._identify_problems(metrics, benchmarks)

        # Se há anomalias, adicionar aos problemas
        if anomalies:
            for anomaly in anomalies:
                problems.append({
                    'type': anomaly.get('metric_key'),
                    'severity': anomaly.get('severity'),
                    'z_score': anomaly.get('z_score', 0)
                })

        # Selecionar estratégia baseada nos problemas
        strategy_template = self._select_strategy(problems)

        # Gerar estratégia
        strategy = self._build_strategy(
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            tenant_type=tenant_type,
            metrics=metrics,
            benchmarks=benchmarks,
            problems=problems,
            template=strategy_template
        )

        logger.info(f"📋 Estratégia gerada para {tenant_name}: {strategy.title}")
        return strategy

    def _identify_problems(
        self,
        metrics: Dict[str, float],
        benchmarks: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identifica problemas baseados em métricas vs benchmarks."""
        problems = []

        # CAC
        cac = metrics.get('cac', 0)
        cac_ideal = benchmarks.get('cac_ideal', 50)
        if cac > cac_ideal * 1.5:
            problems.append({
                'type': 'cac_alto',
                'severity': 'critical' if cac > cac_ideal * 2 else 'warning',
                'current': cac,
                'benchmark': cac_ideal,
                'gap_percent': ((cac - cac_ideal) / cac_ideal) * 100
            })

        # LTV
        ltv = metrics.get('ltv', 0)
        ltv_ideal = benchmarks.get('ltv_ideal', 300)
        if ltv < ltv_ideal * 0.7:
            problems.append({
                'type': 'ltv_baixo',
                'severity': 'critical' if ltv < ltv_ideal * 0.5 else 'warning',
                'current': ltv,
                'benchmark': ltv_ideal,
                'gap_percent': ((ltv_ideal - ltv) / ltv_ideal) * 100
            })

        # LTV:CAC Ratio
        if cac > 0 and ltv > 0:
            ratio = ltv / cac
            if ratio < 2:
                problems.append({
                    'type': 'ltv_cac_baixo',
                    'severity': 'critical' if ratio < 1 else 'warning',
                    'current': ratio,
                    'benchmark': 3.0,
                    'gap_percent': ((3.0 - ratio) / 3.0) * 100
                })

        # Conversão
        conversion = metrics.get('conversion_rate', 0)
        conv_ideal = benchmarks.get('conversion_rate_ideal', 3)
        if conversion < conv_ideal * 0.6:
            problems.append({
                'type': 'conversao_baixa',
                'severity': 'critical' if conversion < conv_ideal * 0.4 else 'warning',
                'current': conversion,
                'benchmark': conv_ideal,
                'gap_percent': ((conv_ideal - conversion) / conv_ideal) * 100
            })

        # Churn
        churn = metrics.get('churn_rate', 0)
        churn_ideal = benchmarks.get('churn_ideal', 5)
        if churn > churn_ideal * 1.5:
            problems.append({
                'type': 'churn_alto',
                'severity': 'critical' if churn > churn_ideal * 2 else 'warning',
                'current': churn,
                'benchmark': churn_ideal,
                'gap_percent': ((churn - churn_ideal) / churn_ideal) * 100
            })

        # ROI
        roi = metrics.get('roi', 0)
        roi_ideal = benchmarks.get('roi_ideal', 4)
        if roi < roi_ideal * 0.5:
            problems.append({
                'type': 'crescimento_lento',
                'severity': 'warning',
                'current': roi,
                'benchmark': roi_ideal,
                'gap_percent': ((roi_ideal - roi) / roi_ideal) * 100
            })

        return problems

    def _select_strategy(
        self,
        problems: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Seleciona template de estratégia baseado nos problemas."""
        if not problems:
            # Sem problemas críticos - estratégia de manutenção/otimização
            return {
                'title': 'Estratégia de Otimização Contínua',
                'type': StrategyType.OPTIMIZATION,
                'diagnosis': 'Métricas dentro do esperado - foco em otimização',
                'objective': 'Manter performance e identificar oportunidades de melhoria',
                'actions': [
                    ActionItem(
                        title='Revisão de Processos',
                        description='Auditoria completa de processos de marketing',
                        responsible='Marketing Director',
                        deadline_days=14,
                        effort='medium',
                        kpi='Process Efficiency',
                        expected_impact='Identificar 10-15% de ganho de eficiência'
                    ),
                    ActionItem(
                        title='Testes de Inovação',
                        description='Alocar 10% do budget para testes de novos canais',
                        responsible='Growth Manager',
                        deadline_days=30,
                        effort='low',
                        kpi='Test Success Rate',
                        expected_impact='Descobrir 1-2 novos canais performáticos'
                    )
                ]
            }

        # Ordenar problemas por severidade
        severity_order = {'critical': 0, 'warning': 1}
        problems.sort(key=lambda x: severity_order.get(x.get('severity', 'warning'), 2))

        # Selecionar template baseado no problema mais crítico
        primary_problem = problems[0]['type']
        template = self.STRATEGY_TEMPLATES.get(
            primary_problem,
            self.STRATEGY_TEMPLATES['crescimento_lento']
        )

        return template

    def _build_strategy(
        self,
        tenant_id: str,
        tenant_name: str,
        tenant_type: str,
        metrics: Dict[str, float],
        benchmarks: Dict[str, float],
        problems: List[Dict[str, Any]],
        template: Dict[str, Any]
    ) -> Strategy:
        """Constrói objeto Strategy completo."""
        # Gerar contexto
        context = self._generate_context(metrics, benchmarks, problems, tenant_type)

        # Calcular budget estimado (baseado no tamanho do problema)
        budget_estimate = self._estimate_budget(metrics, problems)

        # Calcular ROI esperado
        expected_roi = self._estimate_roi(problems)

        # Timeline baseada na complexidade
        timeline_weeks = len(template['actions']) * 2  # 2 semanas por ação em média

        return Strategy(
            title=template['title'],
            strategy_type=template['type'].value,
            priority='critical' if any(p.get('severity') == 'critical' for p in problems) else 'high',
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            context=context,
            diagnosis=template['diagnosis'],
            objective=template['objective'],
            key_results=self._generate_okr(problems),
            action_plan=template['actions'],
            budget_estimate=budget_estimate,
            expected_roi=expected_roi,
            timeline_weeks=timeline_weeks,
            created_at=datetime.now().isoformat()
        )

    def _generate_context(
        self,
        metrics: Dict[str, float],
        benchmarks: Dict[str, float],
        problems: List[Dict[str, Any]],
        tenant_type: str
    ) -> str:
        """Gera texto de contexto para a estratégia."""
        context_parts = []

        context_parts.append(f"Análise para {tenant_type.upper()}:")
        context_parts.append("")

        # Métricas atuais
        context_parts.append("**Métricas Atuais:**")
        if 'cac' in metrics:
            context_parts.append(f"- CAC: R$ {metrics['cac']:.2f} (benchmark: R$ {benchmarks['cac_ideal']:.2f})")
        if 'ltv' in metrics:
            context_parts.append(f"- LTV: R$ {metrics['ltv']:.2f} (benchmark: R$ {benchmarks['ltv_ideal']:.2f})")
        if 'conversion_rate' in metrics:
            context_parts.append(f"- Conversão: {metrics['conversion_rate']:.2f}% (benchmark: {benchmarks['conversion_rate_ideal']:.2f}%)")
        if 'churn_rate' in metrics:
            context_parts.append(f"- Churn: {metrics['churn_rate']:.2f}% (benchmark: {benchmarks['churn_ideal']:.2f}%)")
        if 'roi' in metrics:
            context_parts.append(f"- ROI: {metrics['roi']:.2f}x (benchmark: {benchmarks['roi_ideal']:.2f}x)")

        context_parts.append("")

        # Problemas identificados
        if problems:
            context_parts.append("**Problemas Identificados:**")
            for problem in problems[:5]:
                gap = problem.get('gap_percent', 0)
                context_parts.append(
                    f"- {problem['type'].replace('_', ' ').title()}: "
                    f"{gap:.1f}% {'acima' if 'alto' in problem['type'] or 'baixo' not in problem['type'] else 'abaixo'} do benchmark"
                )

        return "\n".join(context_parts)

    def _generate_okr(self, problems: List[Dict[str, Any]]) -> List[str]:
        """Gera Key Results para a estratégia."""
        key_results = []

        problem_types = [p['type'] for p in problems]

        if 'cac_alto' in problem_types:
            key_results.append("Reduzir CAC em 30% nos próximos 60 dias")
        if 'ltv_baixo' in problem_types:
            key_results.append("Aumentar LTV em 50% nos próximos 90 dias")
        if 'conversao_baixa' in problem_types:
            key_results.append("Aumentar taxa de conversão em 50% nos próximos 45 dias")
        if 'churn_alto' in problem_types:
            key_results.append("Reduzir churn em 40% nos próximos 60 dias")
        if 'crescimento_lento' in problem_types:
            key_results.append("Acelerar crescimento de receita em 2x nos próximos 90 dias")

        # Adicionar KR de LTV:CAC se relevante
        if 'ltv_cac_baixo' in problem_types:
            key_results.append("Alcançar ratio LTV:CAC de 3:1 nos próximos 90 dias")

        return key_results if key_results else ["Manter métricas dentro do benchmark"]

    def _estimate_budget(
        self,
        metrics: Dict[str, float],
        problems: List[Dict[str, Any]]
    ) -> float:
        """Estima budget necessário para a estratégia."""
        # Base: 10-20% da receita mensal baseada em LTV e número de clientes
        base_revenue = metrics.get('ltv', 300) * metrics.get('active_customers', 100)
        
        # Multiplicador baseado na severidade dos problemas
        severity_multiplier = 1.0
        for problem in problems:
            if problem.get('severity') == 'critical':
                severity_multiplier += 0.3
            elif problem.get('severity') == 'warning':
                severity_multiplier += 0.15

        # Budget = 15% da receita * severity_multiplier
        budget = base_revenue * 0.15 * severity_multiplier
        
        return round(budget, 2)

    def _estimate_roi(self, problems: List[Dict[str, Any]]) -> float:
        """Estima ROI esperado da estratégia."""
        # ROI base esperado: 3-5x
        base_roi = 4.0

        # Ajustar baseado no número e severidade de problemas
        # Mais problemas = mais oportunidade de melhoria = ROI potencial maior
        critical_count = sum(1 for p in problems if p.get('severity') == 'critical')
        warning_count = sum(1 for p in problems if p.get('severity') == 'warning')

        roi_adjustment = (critical_count * 0.5) + (warning_count * 0.2)
        
        return round(base_roi + roi_adjustment, 2)

    def write_strategy_to_obsidian(
        self,
        strategy: Strategy,
        obsidian_path: str
    ) -> str:
        """
        Escreve estratégia no Obsidian.

        Args:
            strategy: Estratégia gerada
            obsidian_path: Caminho para o vault do Obsidian

        Returns:
            Caminho para o arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        strategies_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "04 - Estratégias",
            strategy.tenant_name
        )
        os.makedirs(strategies_path, exist_ok=True)

        # Formatar plano de ação
        action_plan_content = ""
        for i, action in enumerate(strategy.action_plan, 1):
            action_plan_content += f"""
#### {i}. {action.title}

| Campo | Detalhe |
| :---- | :------ |
| **Responsável** | {action.responsible} |
| **Prazo** | {action.deadline_days} dias |
| **Esforço** | {action.effort.title()} |
| **KPI** | {action.kpi} |
| **Impacto Esperado** | {action.expected_impact} |

**Descrição:** {action.description}

---
"""

        # Formatar Key Results
        kr_content = ""
        for i, kr in enumerate(strategy.key_results, 1):
            kr_content += f"- [ ] KR{i}: {kr}\n"

        # Conteúdo da nota
        content = f"""---
tags: [estrategia, {strategy.tenant_id}, exocortex, {strategy.strategy_type}]
priority: {strategy.priority}
status: criada
criado: {timestamp}
---

# 🎯 {strategy.title}

**Tenant:** {strategy.tenant_name}

**Tipo:** {strategy.strategy_type.title()}

**Prioridade:** {'🔴' if strategy.priority == 'critical' else '🟡' if strategy.priority == 'high' else '🟢'}

**Criado em:** {timestamp}

---

## 📊 Contexto

{strategy.context}

---

## 🧠 Diagnóstico

{strategy.diagnosis}

---

## 🎯 Objetivo

{strategy.objective}

---

## 📈 Key Results

{kr_content}

---

## 💰 Investimento

| Item | Valor |
| :--- | :---- |
| **Budget Estimado** | R$ {strategy.budget_estimate:,.2f} |
| **ROI Esperado** | {strategy.expected_roi:.1f}x |
| **Timeline** | {strategy.timeline_weeks} semanas |

---

## 📋 Plano de Ação

{action_plan_content}

---

## 📅 Timeline

"""

        # Adicionar timeline visual
        content += self._generate_timeline_visual(strategy)

        content += f"""
---

## ✅ Checklist de Implementação

- [ ] Revisar estratégia com stakeholders
- [ ] Definir responsáveis por cada ação
- [ ] Alocar budget
- [ ] Iniciar execução
- [ ] Medir resultados semanalmente
- [ ] Ajustar conforme necessário

---

*Estratégia gerada automaticamente pelo Exocórtex v5.0 — Marketing Strategy Engine*
"""

        # Salvar arquivo
        safe_name = strategy.tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Estratégia-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(strategies_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📝 Estratégia escrita no Obsidian: {filepath}")
        return filepath

    def _generate_timeline_visual(self, strategy: Strategy) -> str:
        """Gera timeline visual em ASCII/Gantt simples."""
        timeline = "```\n"
        timeline += "Semana: "
        
        # Header
        for i in range(1, strategy.timeline_weeks + 1, 2):
            timeline += f"W{i:2d} "
        timeline += "\n"
        timeline += "|" + "-" * (strategy.timeline_weeks * 4) + "|\n"

        # Barras de ações
        current_week = 1
        for action in strategy.action_plan[:5]:  # Máximo 5 ações
            action_weeks = max(1, action.deadline_days // 7)
            bar = "█" * min(action_weeks, strategy.timeline_weeks)
            padding = " " * (strategy.timeline_weeks - len(bar))
            short_title = action.title[:20].ljust(20)
            timeline += f"{short_title}|{bar}{padding}|\n"

        timeline += "```\n"
        return timeline

    def generate_all_strategies(
        self,
        tenants_data: List[Dict[str, Any]],
        obsidian_path: str
    ) -> List[str]:
        """
        Gera estratégias para todos os tenants.

        Args:
            tenants_data: Lista de tenants com métricas
            obsidian_path: Caminho para o vault do Obsidian

        Returns:
            Lista de caminhos para arquivos criados
        """
        created_files = []

        for tenant in tenants_data:
            try:
                # Extrair métricas
                metrics = self._extract_metrics(tenant.get('metrics', []))

                # Gerar estratégia
                strategy = self.analyze_and_generate_strategy(
                    tenant_id=tenant.get('id', 'unknown'),
                    tenant_name=tenant.get('name', 'Unknown'),
                    tenant_type=tenant.get('type', 'default'),
                    metrics=metrics
                )

                # Escrever no Obsidian
                filepath = self.write_strategy_to_obsidian(strategy, obsidian_path)
                created_files.append(filepath)

            except Exception as e:
                logger.error(f"❌ Erro ao gerar estratégia para {tenant.get('name')}: {e}")

        return created_files

    def _extract_metrics(self, metrics_list: List[Dict]) -> Dict[str, float]:
        """Extrai métricas de uma lista para um dicionário."""
        metrics = {}
        
        metric_mapping = {
            'cac': ['cac', 'customer_acquisition_cost', 'custo_aquisicao'],
            'ltv': ['ltv', 'lifetime_value', 'valor_vida'],
            'conversion_rate': ['conversion_rate', 'taxa_conversao', 'conversao'],
            'churn_rate': ['churn_rate', 'churn', 'taxa_cancelamento'],
            'roi': ['roi', 'return_on_investment', 'retorno'],
            'active_customers': ['active_customers', 'clientes_ativos', 'num_customers']
        }

        for metric in metrics_list:
            key = metric.get('key', metric.get('metric_key', '')).lower()
            value = metric.get('value', 0)

            for standard_key, variations in metric_mapping.items():
                if key in variations or standard_key in key:
                    metrics[standard_key] = float(value)
                    break

        return metrics
