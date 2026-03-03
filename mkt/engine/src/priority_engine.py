"""
╔═══════════════════════════════════════════════════════════════════════════════
║ PRIORITY ENGINE — Z-Score & Ordenação Dinâmica (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Gerencia priorização baseada em anomalias estatísticas
║ Quanto maior o Z-Score, mais alto o item aparece na lista
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

import numpy as np

logger = logging.getLogger(__name__)


class PriorityEngine:
    """
    Gerencia priorização baseada em Z-Score para detecção de anomalias.
    
    Lógica de priorização:
    • Z-Score > 3.0: Crítico (🔴) - Ação imediata necessária
    • Z-Score 2.0-3.0: Atenção (🟡) - Monitorar de perto
    • Z-Score < 2.0: Normal (🟢) - Operação regular
    
    Unidades com anomalias críticas saltam para o topo da lista.
    """

    def __init__(self, 
                 threshold_critical: float = 3.0,
                 threshold_warning: float = 2.0,
                 min_data_points: int = 7):
        """
        Inicializa a Engine de Prioridade.
        
        Args:
            threshold_critical: Z-Score mínimo para crítico (padrão: 3.0)
            threshold_warning: Z-Score mínimo para atenção (padrão: 2.0)
            min_data_points: Mínimo de pontos para cálculo estatístico (padrão: 7)
        """
        self.threshold_critical = threshold_critical
        self.threshold_warning = threshold_warning
        self.min_data_points = min_data_points
        
        logger.info(f"🧠 PriorityEngine inicializada (crítico: {threshold_critical}, atenção: {threshold_warning})")

    def calculate_zscore(self, values: List[float], current: float) -> float:
        """
        Calcula Z-Score para detecção de anomalias.
        
        Z-Score = (valor_atual - media) / desvio_padrao
        
        Args:
            values: Lista de valores históricos para comparação
            current: Valor atual a ser avaliado
            
        Returns:
            Z-Score calculado (0.0 se dados insuficientes)
        """
        if len(values) < self.min_data_points:
            logger.debug(f"⚠️ Dados insuficientes para Z-Score: {len(values)} < {self.min_data_points}")
            return 0.0

        mean = np.mean(values)
        std = np.std(values)

        if std == 0 or std < 1e-10:
            # Sem variabilidade, não há anomalia
            return 0.0

        z_score = abs((current - mean) / std)
        return z_score

    def classify_severity(self, z_score: float) -> Tuple[str, str]:
        """
        Classifica a severidade baseada no Z-Score.
        
        Args:
            z_score: Z-Score calculado
            
        Returns:
            Tuple (severidade, ícone):
            - ('critical', '🔴') se z_score > 3.0
            - ('warning', '🟡') se 2.0 < z_score <= 3.0
            - ('normal', '🟢') se z_score <= 2.0
        """
        if z_score > self.threshold_critical:
            return 'critical', '🔴'
        elif z_score > self.threshold_warning:
            return 'warning', '🟡'
        else:
            return 'normal', '🟢'

    def analyze_metric_anomaly(self, 
                               metric_key: str,
                               current_value: float,
                               historical_values: List[float],
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analisa uma métrica específica para anomalias.
        
        Args:
            metric_key: Chave da métrica (ex: 'cac', 'ltv', 'conversion_rate')
            current_value: Valor atual da métrica
            historical_values: Valores históricos (últimos 30 dias)
            context: Contexto adicional (tenant, data, etc.)
            
        Returns:
            Dicionário com análise completa da anomalia
        """
        z_score = self.calculate_zscore(historical_values, current_value)
        severity, icon = self.classify_severity(z_score)
        
        # Calcular estatísticas básicas
        mean = np.mean(historical_values) if historical_values else 0
        std = np.std(historical_values) if historical_values else 0
        min_val = min(historical_values) if historical_values else 0
        max_val = max(historical_values) if historical_values else 0
        
        # Calcular percentil
        percentile = self._calculate_percentile(historical_values, current_value)
        
        # Gerar recomendação
        recommendation = self._generate_recommendation(
            metric_key, current_value, mean, z_score, severity
        )
        
        return {
            'metric_key': metric_key,
            'current_value': current_value,
            'historical_mean': mean,
            'historical_std': std,
            'historical_min': min_val,
            'historical_max': max_val,
            'z_score': z_score,
            'severity': severity,
            'icon': icon,
            'percentile': percentile,
            'is_anomaly': severity in ['critical', 'warning'],
            'recommendation': recommendation,
            'context': context or {},
            'analyzed_at': datetime.now().isoformat()
        }

    def prioritize_units(self, units_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioriza unidades por gravidade (maior Z-Score primeiro).
        
        Args:
            units_data: Lista de unidades com suas métricas
                Cada unidade deve ter:
                - id: ID da unidade
                - name: Nome da unidade
                - slug: Slug da unidade
                - metrics: Lista de métricas com 'key' e 'value'
                
        Returns:
            Lista de unidades priorizadas (maiores Z-Scores no topo)
        """
        prioritized = []
        
        for unit in units_data:
            unit_metrics = unit.get('metrics', [])
            max_zscore = 0.0
            critical_metrics = []
            
            for metric in unit_metrics:
                metric_key = metric.get('key', 'unknown')
                current_value = metric.get('value', 0)
                
                # Obter valores históricos (simulado - na prática vem do DB)
                historical = self._get_historical_metrics(
                    unit.get('id'),
                    metric_key,
                    days=30
                )
                
                # Analisar anomalia
                analysis = self.analyze_metric_anomaly(
                    metric_key,
                    current_value,
                    historical,
                    context={'unit_id': unit.get('id'), 'unit_name': unit.get('name')}
                )
                
                if analysis['is_anomaly']:
                    critical_metrics.append(analysis)
                
                max_zscore = max(max_zscore, analysis['z_score'])
            
            # Classificar unidade
            severity, icon = self.classify_severity(max_zscore)
            
            prioritized.append({
                **unit,
                'max_zscore': max_zscore,
                'severity': severity,
                'icon': icon,
                'critical_metrics': critical_metrics,
                'anomaly_count': len(critical_metrics)
            })
        
        # Ordenar: maiores Z-Scores primeiro (críticos no topo)
        prioritized.sort(key=lambda x: x['max_zscore'], reverse=True)
        
        logger.info(f"📊 {len(prioritized)} unidades priorizadas")
        return prioritized

    def generate_summary_with_priority(self, 
                                       prioritized_units: List[Dict[str, Any]],
                                       obsidian_path: str) -> str:
        """
        Gera resumo executivo com priorização.
        
        Unidades críticas saltam para o topo automaticamente.
        
        Args:
            prioritized_units: Lista de unidades já priorizadas
            obsidian_path: Caminho para o vault do Obsidian
            
        Returns:
            Caminho para o arquivo do resumo gerado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Separar unidades por severidade
        critical_units = [u for u in prioritized_units if u['severity'] == 'critical']
        warning_units = [u for u in prioritized_units if u['severity'] == 'warning']
        normal_units = [u for u in prioritized_units if u['severity'] == 'normal']
        
        # Contadores
        total_units = len(prioritized_units)
        critical_count = len(critical_units)
        warning_count = len(warning_units)
        normal_count = len(normal_units)
        
        summary_content = f"""---
tags: [resumo, executivo, exocortex, priorizacao]
updated: {timestamp}
---

# 🌍 Resumo Executivo Global

**Atualizado em:** {timestamp}

---

## 📊 Visão Geral

| Status | Quantidade | Porcentagem |
| :----- | :--------: | :----------: |
| 🔴 Críticos | {critical_count} | {self._percentage(critical_count, total_units)}% |
| 🟡 Atenção | {warning_count} | {self._percentage(warning_count, total_units)}% |
| 🟢 Normal | {normal_count} | {self._percentage(normal_count, total_units)}% |
| **Total** | **{total_units}** | **100%** |

---

## 🔴 PRIORIDADE MÁXIMA (Críticos)

Unidades com anomalias críticas (Z-Score > 3.0) — Ação imediata necessária

"""

        if critical_units:
            for i, unit in enumerate(critical_units, 1):
                summary_content += self._format_unit_card(unit, i)
        else:
            summary_content += "> ✅ Nenhuma unidade crítica no momento.\n"
        
        summary_content += f"""
---

## 🟡 ATENÇÃO NECESSÁRIA (Alertas)

Unidades com anomalias moderadas (Z-Score 2.0-3.0) — Monitorar de perto

"""

        if warning_units:
            for i, unit in enumerate(warning_units, 1):
                summary_content += self._format_unit_card(unit, i)
        else:
            summary_content += "> ✅ Nenhuma unidade requer atenção especial.\n"
        
        summary_content += f"""
---

## 🟢 OPERANDO NORMAL

Unidades sem anomalias (Z-Score < 2.0)

**Total:** {normal_count} unidades operando dentro do esperado.

"""

        if normal_units:
            summary_content += "| Unidade | Z-Score Máx | Status |\n"
            summary_content += "| :------ | :---------: | :----- |\n"
            for unit in normal_units[:10]:  # Mostrar apenas 10 primeiras
                summary_content += f"| {unit.get('name', 'N/A')} | {unit['max_zscore']:.2f} | 🟢 Normal |\n"
            if len(normal_units) > 10:
                summary_content += f"\n*e mais {len(normal_units) - 10} unidades...*\n"
        
        summary_content += f"""
---

## 📈 Próximos Passos

1. **Resolver Críticos** → Atuar nas {critical_count} unidades 🔴 primeiro
2. **Monitorar Alertas** → Acompanhar {warning_count} unidades 🟡 de perto
3. **Manter Normal** → {normal_count} unidades 🟢 operando bem

---

*Gerado automaticamente pelo Exocórtex v5.0 — Gestão por Risco com Z-Score*
"""

        # Salvar resumo
        exocortex_path = os.path.join(obsidian_path, "🧠 EXOCÓRTEX")
        os.makedirs(exocortex_path, exist_ok=True)
        
        summary_file = os.path.join(
            exocortex_path,
            "🌍 RESUMO_EXECUTIVO_GLOBAL.md"
        )

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        logger.info(f"🌍 Resumo Executivo gerado: {summary_file}")
        return summary_file

    def _format_unit_card(self, unit: Dict[str, Any], index: int) -> str:
        """Formata um cartão de unidade para o resumo."""
        name = unit.get('name', 'Unidade Desconhecida')
        z_score = unit['max_zscore']
        anomaly_count = unit.get('anomaly_count', 0)
        slug = unit.get('slug', '')
        
        card = f"""
### {index}. {unit['icon']} {name}

| Métrica | Valor |
| :------ | :---- |
| **Z-Score Máximo** | {z_score:.2f} |
| **Anomalias** | {anomaly_count} |

"""
        
        # Adicionar métricas críticas
        critical_metrics = unit.get('critical_metrics', [])
        if critical_metrics:
            card += "**Métricas com Anomalia:**\n\n"
            for metric in critical_metrics[:3]:  # Mostrar até 3
                card += f"- **{metric['metric_key']}**: {metric['current_value']:.2f} "
                card += f"(Z-Score: {metric['z_score']:.2f}) — {metric['recommendation']}\n"
        
        card += "\n"
        return card

    def _calculate_percentile(self, values: List[float], current: float) -> float:
        """Calcula o percentil do valor atual em relação aos históricos."""
        if not values:
            return 0.0
        count_below = sum(1 for v in values if v < current)
        return (count_below / len(values)) * 100

    def _percentage(self, part: int, total: int) -> float:
        """Calcula porcentagem."""
        if total == 0:
            return 0.0
        return round((part / total) * 100, 1)

    def _generate_recommendation(self, 
                                 metric_key: str,
                                 current_value: float,
                                 mean: float,
                                 z_score: float,
                                 severity: str) -> str:
        """Gera recomendação baseada na anomalia."""
        direction = "acima" if current_value > mean else "abaixo"
        
        if severity == 'critical':
            return f"Investigar imediatamente — valor {direction} do esperado"
        elif severity == 'warning':
            return f"Monitorar — valor {direction} do esperado"
        else:
            return "Dentro do padrão esperado"

    def _get_historical_metrics(self, 
                                unit_id: str, 
                                metric_key: str, 
                                days: int = 30) -> List[float]:
        """
        Obtém valores históricos de uma métrica.
        
        NOTA: Este é um stub. Na implementação real, isso consulta o Supabase.
        
        Args:
            unit_id: ID da unidade
            metric_key: Chave da métrica
            days: Número de dias para buscar
            
        Returns:
            Lista de valores históricos
        """
        # Stub para desenvolvimento
        # Na implementação real: consultar self.db ou API do Supabase
        logger.debug(f"📊 Buscando histórico: unit={unit_id}, metric={metric_key}, days={days}")
        
        # Retornar dados simulados para teste
        np.random.seed(hash(f"{unit_id}_{metric_key}") % 2**32)
        base_value = hash(metric_key) % 1000 + 100
        values = [base_value + np.random.normal(0, base_value * 0.1) for _ in range(days)]
        return [max(0, v) for v in values]  # Garantir valores não-negativos
