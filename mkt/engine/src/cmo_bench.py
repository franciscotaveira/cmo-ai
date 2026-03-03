"""
╔═══════════════════════════════════════════════════════════════════════════════
║ CMO-BENCH — INTELIGÊNCIA TIPO SWE-BENCH PARA MARKETING
╠═══════════════════════════════════════════════════════════════════════════════
║ Aplica padrões do SWE-bench para inteligência de marketing
║ • Contexto completo (não apenas métricas isoladas)
║ • Verificação executável (ações validadas como testes)
║ • Gold standard learning (aprende com casos resolvidos)
║ • Multi-file reasoning (conecta dados fragmentados)
║ • Feedback loop automático (melhora continuamente)
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# MODELOS DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class BusinessIssue:
    """Issue de negócio (como issue do GitHub no SWE-bench)."""
    id: str
    title: str
    description: str
    tenant_id: str
    tenant_type: str
    severity: str  # critical, high, medium, low
    detected_at: str
    metrics_involved: List[str]
    external_factors: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionPlan:
    """Plano de ação (como patch no SWE-bench)."""
    issue_id: str
    actions: List[Dict[str, Any]]
    expected_impact: Dict[str, float]
    confidence: float
    similar_cases: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VerificationResult:
    """Resultado de verificação (como testes no SWE-bench)."""
    issue_id: str
    action_plan_id: str
    resolved: bool
    tests_passed: int
    tests_total: int
    metrics_before: Dict[str, float]
    metrics_after: Dict[str, float]
    details: Dict[str, bool]
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GoldCase:
    """Caso resolvido (como gold patch no SWE-bench)."""
    issue: BusinessIssue
    action_plan: ActionPlan
    verification: VerificationResult
    confidence: float
    similarity_vector: np.ndarray


# ═══════════════════════════════════════════════════════════════════════════════
# CMO-BENCH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class CMOKnowledgeBase:
    """
    Base de conhecimento com casos resolvidos.
    Aprende com ações passadas (como gold patches do SWE-bench).
    """

    def __init__(self):
        self.cases: List[GoldCase] = []
        self.vectors: Dict[str, np.ndarray] = {}

    def add_resolved_case(
        self,
        issue: BusinessIssue,
        action_plan: ActionPlan,
        verification: VerificationResult
    ):
        """Adiciona caso resolvido à base de conhecimento."""
        if not verification.resolved:
            logger.warning(f"⚠️  Tentativa de adicionar caso não resolvido: {issue.id}")
            return

        # Criar vetor de similaridade
        vector = self._create_similarity_vector(issue, verification.metrics_before)

        # Calcular confiança baseada no resultado
        confidence = self._calculate_confidence(verification)

        gold_case = GoldCase(
            issue=issue,
            action_plan=action_plan,
            verification=verification,
            confidence=confidence,
            similarity_vector=vector
        )

        self.cases.append(gold_case)
        logger.info(f"✅ Caso resolvido adicionado: {issue.id} (confiança: {confidence:.2f})")

    def find_similar_cases(
        self,
        current_issue: BusinessIssue,
        current_metrics: Dict[str, float],
        top_k: int = 5
    ) -> List[Tuple[float, GoldCase]]:
        """Encontra casos similares (como retrieval do SWE-bench)."""
        if not self.cases:
            return []

        # Criar vetor atual
        current_vector = self._create_similarity_vector(current_issue, current_metrics)

        # Calcular similaridades
        similarities = []
        for case in self.cases:
            similarity = cosine_similarity(
                [current_vector],
                [case.similarity_vector]
            )[0][0]
            similarities.append((similarity, case))

        # Ordenar por similaridade
        similarities.sort(key=lambda x: x[0], reverse=True)

        return similarities[:top_k]

    def get_gold_action(self, similar_cases: List[Tuple[float, GoldCase]]) -> Optional[ActionPlan]:
        """Extrai ação ideal dos casos similares."""
        if not similar_cases:
            return None

        # Filtrar apenas casos resolvidos
        resolved_cases = [
            (sim, case) for sim, case in similar_cases
            if case.verification.resolved
        ]

        if not resolved_cases:
            return None

        # Pegar caso com maior similaridade e confiança
        best = max(
            resolved_cases,
            key=lambda x: x[0] * x[1].confidence
        )[1]

        return best.action_plan

    def _create_similarity_vector(
        self,
        issue: BusinessIssue,
        metrics: Dict[str, float]
    ) -> np.ndarray:
        """Cria vetor numérico para similaridade."""
        # Features para similaridade
        features = []

        # Tipo de issue
        issue_type_map = {
            'cac_alto': 0, 'ltv_baixo': 1, 'conversao_baixa': 2,
            'churn_alto': 3, 'roas_baixo': 4, 'revenue_queda': 5
        }
        issue_type = issue_type_map.get(issue.title.split()[0].lower(), 0)
        features.append(issue_type)

        # Severidade
        severity_map = {'critical': 1.0, 'high': 0.75, 'medium': 0.5, 'low': 0.25}
        features.append(severity_map.get(issue.severity, 0.5))

        # Tipo de tenant
        tenant_type_map = {'ecommerce': 0, 'saas': 1, 'servicos': 2, 'imobiliario': 3}
        features.append(tenant_type_map.get(issue.tenant_type, 0))

        # Métricas normalizadas
        for key in ['cac', 'ltv', 'conversion_rate', 'churn_rate', 'roas']:
            value = metrics.get(key, 0)
            features.append(value / 1000.0)  # Normalizar

        # Número de métricas envolvidas
        features.append(len(issue.metrics_involved) / 10.0)

        return np.array(features).reshape(1, -1)

    def _calculate_confidence(self, verification: VerificationResult) -> float:
        """Calcula confiança baseada no resultado da verificação."""
        if not verification.resolved:
            return 0.0

        # Confiança baseada em quantos testes passaram
        test_ratio = verification.tests_passed / verification.tests_total

        # Confiança baseada na magnitude da melhoria
        improvements = []
        for key in verification.metrics_after:
            before = verification.metrics_before.get(key, 0)
            after = verification.metrics_after.get(key, 0)
            if before > 0:
                # Para CAC, churn: menor é melhor
                if 'cac' in key.lower() or 'churn' in key.lower():
                    improvement = (before - after) / before
                # Para LTV, ROAS, conversão: maior é melhor
                elif 'ltv' in key.lower() or 'roas' in key.lower() or 'conversion' in key.lower():
                    improvement = (after - before) / before
                else:
                    improvement = 0
                improvements.append(improvement)

        avg_improvement = np.mean(improvements) if improvements else 0

        # Combina testes + melhoria
        confidence = (test_ratio * 0.6) + (min(avg_improvement, 0.5) * 0.4)

        return min(1.0, max(0.0, confidence))


class CMOVerification:
    """
    Verificação executável de ações.
    Similar aos testes do SWE-bench - passa/falha baseado em métricas reais.
    """

    def __init__(
        self,
        action_plan: ActionPlan,
        baseline_metrics: Dict[str, float],
        success_criteria: Dict[str, Any]
    ):
        self.action_plan = action_plan
        self.baseline_metrics = baseline_metrics
        self.success_criteria = success_criteria
        self.current_metrics = baseline_metrics.copy()
        self.execution_results = []

    def execute_action(self) -> List[Dict[str, Any]]:
        """Executa ações do plano (simulado - na prática integra com APIs)."""
        results = []

        for action in self.action_plan.actions:
            result = self._execute_single_action(action)
            self.execution_results.append(result)
            results.append(result)

        return results

    def _execute_single_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Executa ação individual."""
        action_type = action.get('type', 'unknown')

        # Simulação - na prática integra com Google Ads, Meta Ads, etc.
        if action_type == 'pause_campaign':
            return {
                'action': action,
                'status': 'executed',
                'impact': {'type': 'cost_reduction', 'estimated': 0.3}
            }
        elif action_type == 'increase_budget':
            return {
                'action': action,
                'status': 'executed',
                'impact': {'type': 'scale', 'estimated': 0.2}
            }
        elif action_type == 'optimize_landing_page':
            return {
                'action': action,
                'status': 'executed',
                'impact': {'type': 'conversion_lift', 'estimated': 0.15}
            }
        else:
            return {
                'action': action,
                'status': 'unknown_action',
                'impact': {}
            }

    def verify_success(self, days: int = 14) -> VerificationResult:
        """
        Verifica se ação funcionou (como testes do SWE-bench).
        Compara métricas antes/depois com critérios de sucesso.
        """
        # Na prática, busca métricas reais do período
        # Aqui simulamos baseado em critérios

        tests = {}

        for metric, criteria in self.success_criteria.items():
            before = self.baseline_metrics.get(metric, 0)
            after = self.current_metrics.get(metric, 0)

            # Critérios podem ser:
            # - {"type": "decrease", "threshold": 0.2}  # Reduzir 20%
            # - {"type": "increase", "threshold": 0.1}  # Aumentar 10%
            # - {"type": "below", "value": 50}         # Abaixo de 50
            # - {"type": "above", "value": 3.0}        # Acima de 3.0

            if criteria['type'] == 'decrease':
                threshold = criteria.get('threshold', 0.2)
                passed = after < before * (1 - threshold)
            elif criteria['type'] == 'increase':
                threshold = criteria.get('threshold', 0.1)
                passed = after > before * (1 + threshold)
            elif criteria['type'] == 'below':
                value = criteria.get('value', 0)
                passed = after < value
            elif criteria['type'] == 'above':
                value = criteria.get('value', 0)
                passed = after > value
            else:
                passed = False

            tests[metric] = passed

        # Contar testes passados
        passed_count = sum(tests.values())
        total_count = len(tests)

        # Sucesso = 80%+ dos testes passaram (como SWE-bench)
        resolved = passed_count >= total_count * 0.8

        return VerificationResult(
            issue_id=self.action_plan.issue_id,
            action_plan_id=self.action_plan.id if hasattr(self.action_plan, 'id') else 'unknown',
            resolved=resolved,
            tests_passed=passed_count,
            tests_total=total_count,
            metrics_before=self.baseline_metrics,
            metrics_after=self.current_metrics,
            details=tests
        )


class CMOLearningLoop:
    """
    Loop de aprendizado contínuo.
    Processo completo tipo SWE-bench.
    """

    def __init__(self, db_client=None, llm_client=None):
        self.db = db_client
        self.llm = llm_client
        self.knowledge_base = CMOKnowledgeBase()
        self.retriever = None  # Implementar retriever de contexto

    def process_business_issue(
        self,
        issue: BusinessIssue,
        tenant_id: str
    ) -> Dict[str, Any]:
        """
        Processa issue completa (como SWE-bench instance).
        """
        logger.info(f"🧠 Processando issue: {issue.title}")

        # 1. Recuperar contexto completo
        context = self._retrieve_full_context(tenant_id, issue)

        # 2. Encontrar cases similares
        similar_cases = self.knowledge_base.find_similar_cases(
            issue,
            context['current_metrics']
        )

        # 3. Gerar ação baseada em cases + IA
        gold_action = self.knowledge_base.get_gold_action(similar_cases)
        ai_action = self._generate_ai_action(issue, context)

        # 4. Combinar aprendizado + IA
        final_action = self._combine_actions(gold_action, ai_action)

        # 5. Executar ação
        verification = CMOVerification(
            action_plan=final_action,
            baseline_metrics=context['current_metrics'],
            success_criteria=self._define_success_criteria(issue)
        )
        execution_results = verification.execute_action()

        # 6. Aguardar período de verificação (na prática: 14 dias)
        # Aqui simulamos
        verification_result = verification.verify_success(days=14)

        # 7. Aprender com resultado
        if verification_result.resolved:
            self.knowledge_base.add_resolved_case(
                issue=issue,
                action_plan=final_action,
                verification=verification_result
            )

        return {
            'issue': issue,
            'action': final_action,
            'execution': execution_results,
            'verification': verification_result,
            'similar_cases_found': len(similar_cases),
            'learned': verification_result.resolved
        }

    def _retrieve_full_context(self, tenant_id: str, issue: BusinessIssue) -> Dict[str, Any]:
        """Recupera contexto completo (como codebase do SWE-bench)."""
        # Na prática, busca do Supabase
        return {
            'tenant': {'id': tenant_id, 'type': issue.tenant_type},
            'current_metrics': {
                'cac': 65.0,
                'ltv': 350.0,
                'conversion_rate': 2.5,
                'roas': 2.8
            },
            'historical_metrics': [],
            'past_actions': [],
            'external_factors': issue.external_factors
        }

    def _generate_ai_action(self, issue: BusinessIssue, context: Dict[str, Any]) -> ActionPlan:
        """Gera ação usando IA (LLM)."""
        # Na prática, chama LLM com contexto completo
        return ActionPlan(
            issue_id=issue.id,
            actions=[
                {'type': 'optimize_campaigns', 'target': 'meta_ads', 'change': -0.3},
                {'type': 'increase_budget', 'target': 'google_ads', 'change': 0.2}
            ],
            expected_impact={'cac': -0.25, 'roas': 0.15},
            confidence=0.75,
            similar_cases=[]
        )

    def _combine_actions(
        self,
        gold_action: Optional[ActionPlan],
        ai_action: ActionPlan
    ) -> ActionPlan:
        """Combina ação aprendida + ação gerada por IA."""
        if not gold_action:
            return ai_action

        # Ponderar entre aprendizado e IA
        # Se gold_action tem alta confiança, usar mais
        gold_confidence = self.knowledge_base.cases[-1].confidence if self.knowledge_base.cases else 0

        if gold_confidence > 0.8:
            # Aprendizado mais confiável
            return gold_action
        elif gold_confidence > 0.5:
            # Combinar ambos
            return self._merge_action_plans(gold_action, ai_action)
        else:
            # IA mais confiável
            return ai_action

    def _merge_action_plans(self, plan1: ActionPlan, plan2: ActionPlan) -> ActionPlan:
        """Funde dois planos de ação."""
        # Implementar lógica de merge
        return plan1  # Simplificado

    def _define_success_criteria(self, issue: BusinessIssue) -> Dict[str, Any]:
        """Define critérios de sucesso para verificação."""
        criteria = {}

        if 'cac' in issue.title.lower():
            criteria['cac'] = {'type': 'decrease', 'threshold': 0.2}
        if 'ltv' in issue.title.lower():
            criteria['ltv'] = {'type': 'increase', 'threshold': 0.1}
        if 'conversion' in issue.title.lower():
            criteria['conversion_rate'] = {'type': 'increase', 'threshold': 0.15}
        if 'roas' in issue.title.lower():
            criteria['roas'] = {'type': 'increase', 'threshold': 0.2}

        return criteria


# ═══════════════════════════════════════════════════════════════════════════════
# EXEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Exemplo de uso do CMO-Bench
    learning_loop = CMOLearningLoop()

    # Criar issue
    issue = BusinessIssue(
        id="issue-001",
        title="CAC 120% acima do benchmark",
        description="CAC subiu de R$ 30 para R$ 65 em 2 semanas",
        tenant_id="tenant-xyz",
        tenant_type="ecommerce",
        severity="critical",
        detected_at=datetime.now().isoformat(),
        metrics_involved=['cac', 'roas', 'meta_ads_spend'],
        external_factors={'seasonality': 'black_friday', 'ios_changes': True}
    )

    # Processar issue
    result = learning_loop.process_business_issue(issue, "tenant-xyz")

    print(f"\n{'='*70}")
    print(f"RESULTADO DO PROCESSAMENTO")
    print(f"{'='*70}")
    print(f"Issue: {result['issue'].title}")
    print(f"Ação: {len(result['action'].actions)} ações")
    print(f"Execução: {len(result['execution'])} resultados")
    print(f"Verificação: {result['verification'].resolved}")
    print(f"Testes: {result['verification'].tests_passed}/{result['verification'].tests_total}")
    print(f"Aprendizado: {result['learned']}")
    print(f"{'='*70}\n")
