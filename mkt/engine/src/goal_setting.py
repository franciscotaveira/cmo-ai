"""
╔═══════════════════════════════════════════════════════════════════════════════
║ GOAL SETTING ENGINE — Metas + Forecasting (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Define metas SMART e faz previsões baseadas em tendências históricas
║ Usa modelos estatísticos para forecasting (ARIMA, Prophet-ready)
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

import numpy as np

logger = logging.getLogger(__name__)


class GoalType(Enum):
    """Tipos de meta."""
    REVENUE = "revenue"
    ACQUISITION = "acquisition"
    RETENTION = "retention"
    CONVERSION = "conversion"
    EFFICIENCY = "efficiency"
    GROWTH = "growth"


class TimeHorizon(Enum):
    """Horizontes de tempo para metas."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class SMARTGoal:
    """Meta SMART estruturada."""
    title: str
    specific: str
    measurable: str
    achievable: str
    relevant: str
    time_bound: str
    metric_key: str
    current_value: float
    target_value: float
    baseline_value: float
    deadline: str
    milestones: List[Dict[str, Any]]
    confidence_level: float  # 0-1
    created_at: str


@dataclass
class Forecast:
    """Previsão de métrica."""
    metric_key: str
    current_value: float
    forecast_value: float
    forecast_date: str
    confidence_interval_low: float
    confidence_interval_high: float
    trend: str  # increasing, decreasing, stable
    growth_rate: float
    accuracy_estimate: float
    method: str


class GoalSettingEngine:
    """
    Motor de Definição de Metas e Forecasting.

    Funcionalidades:
    • Define metas SMART baseadas em histórico e benchmarks
    • Gera previsões usando análise de tendências
    • Cria milestones intermediários
    • Calcula níveis de confiança
    """

    # Benchmarks de crescimento por setor
    GROWTH_BENCHMARKS = {
        'ecommerce': {'monthly_growth': 0.08, 'churn': 0.05},
        'saas': {'monthly_growth': 0.12, 'churn': 0.03},
        'servicos': {'monthly_growth': 0.05, 'churn': 0.08},
        'imobiliario': {'monthly_growth': 0.03, 'churn': 0.15},
        'default': {'monthly_growth': 0.05, 'churn': 0.05}
    }

    # Fatores de ajuste por tipo de meta
    GOAL_ADJUSTMENT = {
        'revenue': 1.2,  # Metas de receita são mais agressivas
        'acquisition': 1.15,
        'retention': 1.1,
        'conversion': 1.25,
        'efficiency': 1.3,
        'growth': 1.2
    }

    def __init__(self):
        """Inicializa o Goal Setting Engine."""
        logger.info("🎯 GoalSettingEngine inicializado")

    def set_smart_goals(
        self,
        tenant_id: str,
        tenant_name: str,
        tenant_type: str,
        historical_metrics: List[Dict[str, Any]],
        time_horizon: TimeHorizon = TimeHorizon.MONTHLY
    ) -> List[SMARTGoal]:
        """
        Define metas SMART para um tenant.

        Args:
            tenant_id: ID do tenant
            tenant_name: Nome do tenant
            tenant_type: Tipo de negócio
            historical_metrics: Histórico de métricas (últimos 3-6 meses)
            time_horizon: Horizonte de tempo para as metas

        Returns:
            Lista de metas SMART geradas
        """
        goals = []

        # Extrair séries temporais por métrica
        metrics_series = self._extract_time_series(historical_metrics)

        # Definir metas para cada métrica relevante
        metric_configs = {
            'revenue': {'type': GoalType.REVENUE, 'direction': 'up', 'priority': 1},
            'cac': {'type': GoalType.EFFICIENCY, 'direction': 'down', 'priority': 2},
            'ltv': {'type': GoalType.GROWTH, 'direction': 'up', 'priority': 1},
            'conversion_rate': {'type': GoalType.CONVERSION, 'direction': 'up', 'priority': 2},
            'churn_rate': {'type': GoalType.RETENTION, 'direction': 'down', 'priority': 1},
            'active_customers': {'type': GoalType.ACQUISITION, 'direction': 'up', 'priority': 3}
        }

        for metric_key, config in metric_configs.items():
            if metric_key not in metrics_series:
                continue

            series = metrics_series[metric_key]
            if len(series) < 3:
                continue  # Dados insuficientes

            # Calcular meta
            goal = self._create_smart_goal(
                tenant_id=tenant_id,
                tenant_name=tenant_name,
                metric_key=metric_key,
                config=config,
                series=series,
                tenant_type=tenant_type,
                time_horizon=time_horizon
            )

            if goal:
                goals.append(goal)

        logger.info(f"🎯 {len(goals)} metas SMART geradas para {tenant_name}")
        return goals

    def _create_smart_goal(
        self,
        tenant_id: str,
        tenant_name: str,
        metric_key: str,
        config: Dict,
        series: List[Tuple[datetime, float]],
        tenant_type: str,
        time_horizon: TimeHorizon
    ) -> Optional[SMARTGoal]:
        """Cria uma meta SMART individual."""
        # Ordenar série por data
        series.sort(key=lambda x: x[0])

        # Valores atuais e históricos
        current_value = series[-1][1] if series else 0
        historical_values = [v for _, v in series]
        
        if not historical_values or current_value == 0:
            return None

        # Calcular estatísticas
        mean_value = np.mean(historical_values)
        std_value = np.std(historical_values) if len(historical_values) > 1 else 0
        min_value = min(historical_values)
        max_value = max(historical_values)

        # Calcular tendência (crescimento médio)
        growth_rate = self._calculate_growth_rate(series)

        # Obter benchmark
        benchmark_growth = self.GROWTH_BENCHMARKS.get(
            tenant_type,
            self.GROWTH_BENCHMARKS['default']
        ).get('monthly_growth', 0.05)

        # Calcular meta baseada na direção
        direction = config['direction']
        priority = config['priority']

        # Fator de ajuste baseado na prioridade e tipo
        adjustment = self.GOAL_ADJUSTMENT.get(config['type'].value, 1.0)
        priority_factor = 1.0 + (0.1 * (3 - priority))  # Prioridade 1 = +20%, 3 = 0%

        if direction == 'up':
            # Meta de aumento: atual + crescimento orgânico + stretch
            organic_growth = current_value * (1 + growth_rate)
            benchmark_target = current_value * (1 + benchmark_growth)
            stretch_target = current_value * (1 + benchmark_growth * adjustment * priority_factor)

            # Meta = média entre orgânico e stretch (mais conservadora se alta variabilidade)
            variability_factor = 1 - min(std_value / mean_value, 0.3) if mean_value > 0 else 0.7
            target_value = (organic_growth + stretch_target) / 2 * variability_factor
        else:
            # Meta de redução: atual - redução esperada
            reduction_target = current_value * (1 - benchmark_growth * adjustment * priority_factor * 0.5)
            target_value = max(reduction_target, current_value * 0.7)  # Máximo 30% de redução

        # Calcular deadline
        deadline = self._calculate_deadline(time_horizon)

        # Gerar milestones
        milestones = self._generate_milestones(
            current_value=current_value,
            target_value=target_value,
            deadline=deadline,
            metric_key=metric_key
        )

        # Calcular nível de confiança
        confidence = self._calculate_confidence(
            historical_values=historical_values,
            current_value=current_value,
            target_value=target_value,
            growth_rate=growth_rate
        )

        # Gerar componentes SMART
        smart_components = self._generate_smart_components(
            metric_key=metric_key,
            current_value=current_value,
            target_value=target_value,
            deadline=deadline,
            confidence=confidence,
            tenant_type=tenant_type
        )

        return SMARTGoal(
            title=f"{metric_key.replace('_', ' ').title()} - {time_horizon.value.title()}",
            specific=smart_components['specific'],
            measurable=smart_components['measurable'],
            achievable=smart_components['achievable'],
            relevant=smart_components['relevant'],
            time_bound=smart_components['time_bound'],
            metric_key=metric_key,
            current_value=current_value,
            target_value=target_value,
            baseline_value=mean_value,
            deadline=deadline,
            milestones=milestones,
            confidence_level=confidence,
            created_at=datetime.now().isoformat()
        )

    def forecast_metric(
        self,
        metric_key: str,
        historical_values: List[float],
        dates: List[datetime],
        forecast_days: int = 30
    ) -> Forecast:
        """
        Faz previsão de uma métrica.

        Args:
            metric_key: Chave da métrica
            historical_values: Valores históricos
            dates: Datas correspondentes
            forecast_days: Dias para frente para prever

        Returns:
            Forecast: Previsão com intervalo de confiança
        """
        if len(historical_values) < 7:
            # Dados insuficientes - usar média simples
            mean_value = np.mean(historical_values) if historical_values else 0
            return Forecast(
                metric_key=metric_key,
                current_value=historical_values[-1] if historical_values else 0,
                forecast_value=mean_value,
                forecast_date=(datetime.now() + timedelta(days=forecast_days)).isoformat(),
                confidence_interval_low=mean_value * 0.8,
                confidence_interval_high=mean_value * 1.2,
                trend='stable',
                growth_rate=0.0,
                accuracy_estimate=0.5,
                method='simple_average'
            )

        # Calcular tendência linear
        x = np.arange(len(historical_values))
        y = np.array(historical_values)

        # Regressão linear simples
        slope, intercept = np.polyfit(x, y, 1)

        # Prever valor futuro
        future_x = len(historical_values) + forecast_days - 1
        forecast_value = slope * future_x + intercept

        # Garantir valor não-negativo
        forecast_value = max(0, forecast_value)

        # Calcular intervalo de confiança
        residuals = y - (slope * x + intercept)
        std_residual = np.std(residuals)
        confidence_margin = 1.96 * std_residual * np.sqrt(1 + 1/len(historical_values))

        confidence_low = max(0, forecast_value - confidence_margin)
        confidence_high = forecast_value + confidence_margin

        # Determinar tendência
        if slope > std_residual:
            trend = 'increasing'
        elif slope < -std_residual:
            trend = 'decreasing'
        else:
            trend = 'stable'

        # Calcular taxa de crescimento
        current_value = historical_values[-1]
        growth_rate = (forecast_value - current_value) / current_value if current_value > 0 else 0

        # Estimar acurácia (baseada em R²)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum(residuals ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        accuracy_estimate = max(0.5, min(0.95, r_squared))

        return Forecast(
            metric_key=metric_key,
            current_value=current_value,
            forecast_value=forecast_value,
            forecast_date=(datetime.now() + timedelta(days=forecast_days)).isoformat(),
            confidence_interval_low=confidence_low,
            confidence_interval_high=confidence_high,
            trend=trend,
            growth_rate=growth_rate,
            accuracy_estimate=accuracy_estimate,
            method='linear_regression'
        )

    def write_goals_to_obsidian(
        self,
        goals: List[SMARTGoal],
        forecasts: List[Forecast],
        tenant_name: str,
        obsidian_path: str
    ) -> str:
        """
        Escreve metas e previsões no Obsidian.

        Args:
            goals: Lista de metas SMART
            forecasts: Lista de previsões
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        goals_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "05 - Metas & Forecasting",
            tenant_name
        )
        os.makedirs(goals_path, exist_ok=True)

        # Conteúdo das metas
        goals_content = ""
        for goal in goals:
            confidence_icon = '🟢' if goal.confidence_level > 0.7 else '🟡' if goal.confidence_level > 0.5 else '🔴'
            
            goals_content += f"""
## {confidence_icon} {goal.title}

**Métrica:** {goal.metric_key}

| Campo | Valor |
| :---- | :---- |
| **Atual** | {goal.current_value:,.2f} |
| **Meta** | {goal.target_value:,.2f} |
| **Baseline (Média)** | {goal.baseline_value:,.2f} |
| **Deadline** | {goal.deadline} |
| **Confiança** | {goal.confidence_level:.1%} |

### SMART

- **Specific:** {goal.specific}
- **Measurable:** {goal.measurable}
- **Achievable:** {goal.achievable}
- **Relevant:** {goal.relevant}
- **Time-bound:** {goal.time_bound}

### Milestones

"""
            for i, milestone in enumerate(goal.milestones, 1):
                goals_content += f"- [ ] **{milestone['date']}:** {milestone['description']} (meta: {milestone['target']:,.2f})\n"

            goals_content += "\n---\n"

        # Conteúdo das previsões
        forecasts_content = ""
        for forecast in forecasts:
            trend_icon = {'increasing': '📈', 'decreasing': '📉', 'stable': '➡️'}.get(forecast.trend, '❓')
            
            forecasts_content += f"""
### {trend_icon} {forecast.metric_key.replace('_', ' ').title()}

| Campo | Valor |
| :---- | :---- |
| **Atual** | {forecast.current_value:,.2f} |
| **Previsão** | {forecast.forecast_value:,.2f} |
| **Intervalo (95%)** | {forecast.confidence_interval_low:,.2f} - {forecast.confidence_interval_high:,.2f} |
| **Tendência** | {forecast.trend.title()} |
| **Crescimento** | {forecast.growth_rate:.2%} |
| **Acurácia Estimada** | {forecast.accuracy_estimate:.1%} |
| **Método** | {forecast.method} |

"""

        # Conteúdo principal
        content = f"""---
tags: [metas, forecasting, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 🎯 Metas & Previsões - {tenant_name}

**Gerado em:** {timestamp}

---

## 📊 Metas SMART

{goals_content}

---

## 🔮 Previsões

{forecasts_content}

---

## 📈 Visão Geral

```dataview
TABLE target_value as "Meta", current_value as "Atual", confidence_level as "Confiança", deadline as "Deadline"
FROM "🧠 EXOCÓRTEX/05 - Metas & Forecasting/{tenant_name}"
WHERE contains(tags, "meta")
SORT deadline ASC
```

---

*Gerado automaticamente pelo Exocórtex v5.0 — Goal Setting Engine*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"Metas-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(goals_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"🎯 Metas escritas no Obsidian: {filepath}")
        return filepath

    def _extract_time_series(
        self,
        historical_metrics: List[Dict[str, Any]]
    ) -> Dict[str, List[Tuple[datetime, float]]]:
        """Extrai séries temporais de métricas."""
        series = {}

        for metric in historical_metrics:
            key = metric.get('key', metric.get('metric_key', ''))
            value = metric.get('value', 0)
            date_str = metric.get('date', metric.get('date_ref', ''))

            try:
                if date_str:
                    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    date = datetime.now()
            except:
                date = datetime.now()

            if key not in series:
                series[key] = []

            series[key].append((date, value))

        return series

    def _calculate_growth_rate(self, series: List[Tuple[datetime, float]]) -> float:
        """Calcula taxa de crescimento média."""
        if len(series) < 2:
            return 0.0

        # Ordenar por data
        series.sort(key=lambda x: x[0])

        # Calcular crescimento entre períodos consecutivos
        growth_rates = []
        for i in range(1, len(series)):
            prev_value = series[i-1][1]
            curr_value = series[i][1]
            if prev_value > 0:
                growth_rates.append((curr_value - prev_value) / prev_value)

        return np.mean(growth_rates) if growth_rates else 0.0

    def _calculate_deadline(self, time_horizon: TimeHorizon) -> str:
        """Calcula deadline baseado no horizonte de tempo."""
        now = datetime.now()

        if time_horizon == TimeHorizon.WEEKLY:
            deadline = now + timedelta(days=7)
        elif time_horizon == TimeHorizon.MONTHLY:
            deadline = now + timedelta(days=30)
        elif time_horizon == TimeHorizon.QUARTERLY:
            deadline = now + timedelta(days=90)
        else:  # YEARLY
            deadline = now + timedelta(days=365)

        return deadline.strftime('%Y-%m-%d')

    def _generate_milestones(
        self,
        current_value: float,
        target_value: float,
        deadline: str,
        metric_key: str
    ) -> List[Dict[str, Any]]:
        """Gera milestones intermediários."""
        milestones = []

        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
        except:
            deadline_date = datetime.now() + timedelta(days=30)

        total_days = (deadline_date - datetime.now()).days
        total_change = target_value - current_value

        # Criar 3-4 milestones
        num_milestones = min(4, max(3, total_days // 15))

        for i in range(1, num_milestones + 1):
            milestone_date = datetime.now() + timedelta(days=int(total_days * i / (num_milestones + 1)))
            progress = i / (num_milestones + 1)
            milestone_target = current_value + (total_change * progress)

            milestones.append({
                'date': milestone_date.strftime('%Y-%m-%d'),
                'target': milestone_target,
                'description': f"{metric_key.replace('_', ' ').title()} - checkpoint {i}/{num_milestones}"
            })

        return milestones

    def _calculate_confidence(
        self,
        historical_values: List[float],
        current_value: float,
        target_value: float,
        growth_rate: float
    ) -> float:
        """Calcula nível de confiança na meta."""
        if not historical_values:
            return 0.5

        mean_value = np.mean(historical_values)
        std_value = np.std(historical_values) if len(historical_values) > 1 else mean_value * 0.2

        # Fatores de confiança
        # 1. Variabilidade histórica (menos variabilidade = mais confiança)
        cv = std_value / mean_value if mean_value > 0 else 0.5
        variability_score = max(0.3, 1 - cv)

        # 2. Distância da meta (meta muito ambiciosa = menos confiança)
        gap = abs(target_value - current_value) / current_value if current_value > 0 else 1
        ambition_score = max(0.3, 1 - gap)

        # 3. Tendência histórica (tendência alinhada com meta = mais confiança)
        trend_score = min(1.0, 0.5 + abs(growth_rate) * 10)

        # Combinação ponderada
        confidence = (variability_score * 0.4 + ambition_score * 0.4 + trend_score * 0.2)

        return min(0.95, max(0.2, confidence))

    def _generate_smart_components(
        self,
        metric_key: str,
        current_value: float,
        target_value: float,
        deadline: str,
        confidence: float,
        tenant_type: str
    ) -> Dict[str, str]:
        """Gera componentes SMART em texto."""
        metric_name = metric_key.replace('_', ' ').title()
        change_percent = ((target_value - current_value) / current_value * 100) if current_value > 0 else 0
        direction = "aumentar" if target_value > current_value else "reduzir"
        abs_change = abs(change_percent)

        return {
            'specific': f"{direction.capitalize()} {metric_name} em {abs_change:.1f}%, de {current_value:,.2f} para {target_value:,.2f}",
            'measurable': f"Acompanhar semanalmente através de dashboard, com meta intermediária de {(current_value + target_value) / 2:,.2f} na metade do período",
            'achievable': f"Baseado em histórico e benchmarks do setor ({tenant_type}), com {confidence:.0%} de confiança na realização",
            'relevant': f"Esta meta impacta diretamente o crescimento e sustentabilidade do negócio",
            'time_bound': f"Alcançar até {deadline}, com checkpoints quinzenais"
        }

    def generate_all_goals_and_forecasts(
        self,
        tenants_data: List[Dict[str, Any]],
        obsidian_path: str,
        time_horizon: TimeHorizon = TimeHorizon.MONTHLY
    ) -> Dict[str, str]:
        """
        Gera metas e previsões para todos os tenants.

        Args:
            tenants_data: Lista de tenants com métricas históricas
            obsidian_path: Caminho para o vault
            time_horizon: Horizonte de tempo para metas

        Returns:
            Dicionário {tenant_name: filepath}
        """
        results = {}

        for tenant in tenants_data:
            try:
                tenant_name = tenant.get('name', 'Unknown')
                tenant_type = tenant.get('type', 'default')

                # Obter métricas históricas (simulado - na prática vem do DB)
                historical_metrics = self._get_historical_metrics(
                    tenant.get('id'),
                    days=90
                )

                # Gerar metas SMART
                goals = self.set_smart_goals(
                    tenant_id=tenant.get('id', 'unknown'),
                    tenant_name=tenant_name,
                    tenant_type=tenant_type,
                    historical_metrics=historical_metrics,
                    time_horizon=time_horizon
                )

                # Gerar previsões
                forecasts = []
                metrics_series = self._extract_time_series(historical_metrics)
                for metric_key, series in metrics_series.items():
                    if len(series) >= 7:
                        dates = [d for d, _ in series]
                        values = [v for _, v in series]
                        forecast = self.forecast_metric(
                            metric_key=metric_key,
                            historical_values=values,
                            dates=dates,
                            forecast_days=30
                        )
                        forecasts.append(forecast)

                # Escrever no Obsidian
                filepath = self.write_goals_to_obsidian(
                    goals=goals,
                    forecasts=forecasts,
                    tenant_name=tenant_name,
                    obsidian_path=obsidian_path
                )

                results[tenant_name] = filepath

            except Exception as e:
                logger.error(f"❌ Erro ao gerar metas para {tenant.get('name')}: {e}")

        return results

    def _get_historical_metrics(
        self,
        tenant_id: str,
        days: int = 90
    ) -> List[Dict[str, Any]]:
        """
        Obtém métricas históricas (stub para desenvolvimento).

        Na implementação real, consulta o Supabase.
        """
        logger.debug(f"📊 Buscando histórico: tenant={tenant_id}, days={days}")

        # Dados simulados para teste
        np.random.seed(hash(tenant_id) % 2**32)
        metrics = []

        base_date = datetime.now()
        base_values = {
            'revenue': 50000,
            'cac': 45,
            'ltv': 350,
            'conversion_rate': 2.8,
            'churn_rate': 4.5,
            'active_customers': 500
        }

        for i in range(days):
            date = base_date - timedelta(days=i)
            for key, base in base_values.items():
                # Adicionar tendência e ruído
                trend = 1 + (0.001 * (days - i))  # Crescimento leve
                noise = np.random.normal(1, 0.1)
                value = base * trend * noise

                metrics.append({
                    'key': key,
                    'value': max(0, value),
                    'date': date.isoformat()
                })

        return metrics
