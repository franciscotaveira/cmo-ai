"""
╔═══════════════════════════════════════════════════════════════════════════════
║ TEST AI INSIGHTS — Script de Teste para IA Generativa
╠═══════════════════════════════════════════════════════════════════════════════
║ Testa todas as funcionalidades do AI Insights Engine
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()

from ai_insights import AIInsightsEngine, LLMProvider


def test_insight_from_anomaly():
    """Testa geração de insight a partir de anomalia."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 1: Insight de Anomalia")
    print("=" * 70)

    # Inicializar engine
    ai = AIInsightsEngine(
        llm_provider=LLMProvider.GROQ,
        obsidian_copilot_enabled=True
    )

    # Gerar insight
    insight = ai.generate_insight_from_anomaly(
        metric_key='cac',
        current_value=65.0,
        expected_value=30.0,
        z_score=3.5,
        tenant_name='Empresa XYZ',
        tenant_type='ecommerce',
        historical_data=[
            {'date': '2026-02-24', 'value': 58},
            {'date': '2026-02-25', 'value': 62},
            {'date': '2026-02-26', 'value': 68},
            {'date': '2026-02-27', 'value': 65},
            {'date': '2026-03-01', 'value': 63},
            {'date': '2026-03-02', 'value': 65}
        ]
    )

    print(f"\n💡 Título: {insight.title}")
    print(f"📊 Categoria: {insight.category}")
    print(f"🚨 Severidade: {insight.severity}")
    print(f"🎯 Confiança: {insight.confidence:.0%}")
    print(f"\n📝 Descrição:\n{insight.description}")
    print(f"\n✅ Ações Recomendadas:")
    for i, action in enumerate(insight.action_items, 1):
        print(f"  {i}. {action}")

    return insight


def test_weekly_report():
    """Testa geração de relatório semanal."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 2: Relatório Semanal")
    print("=" * 70)

    ai = AIInsightsEngine(
        llm_provider=LLMProvider.GROQ,
        obsidian_copilot_enabled=True
    )

    report = ai.generate_weekly_report(
        tenant_name='Empresa XYZ',
        metrics_summary={
            'revenue': 52000,
            'cac': 58,
            'ltv': 380,
            'conversion_rate': 2.4,
            'churn_rate': 4.2,
            'active_customers': 520
        },
        wow_comparison={
            'revenue': 8.5,
            'cac': -5.2,
            'ltv': 4.1,
            'conversion_rate': 12.5,
            'churn_rate': -15.3
        },
        start_date='2026-02-24',
        end_date='2026-03-02'
    )

    print("\n" + report[:1000] + "..." if len(report) > 1000 else "\n" + report)

    return report


def test_content_ideas():
    """Testa geração de ideias de conteúdo."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 3: Ideias de Conteúdo")
    print("=" * 70)

    ai = AIInsightsEngine(
        llm_provider=LLMProvider.GROQ,
        obsidian_copilot_enabled=True
    )

    ideas = ai.generate_content_ideas(
        tenant_name='Empresa XYZ',
        niche='E-commerce de Moda Sustentável',
        target_audience='Mulheres 25-40 anos, classe AB, conscientes',
        content_goal='Brand awareness + geração de leads',
        keywords=['moda sustentável', 'eco-friendly', 'slow fashion', 'consumo consciente'],
        channels=['instagram', 'pinterest', 'blog', 'email']
    )

    print(f"\n💡 {len(ideas)} ideias geradas:\n")

    for i, idea in enumerate(ideas[:5], 1):
        print(f"{i}. **{idea.get('title', 'N/A')}**")
        print(f"   Formato: {idea.get('format', 'N/A')}")
        print(f"   Canal: {idea.get('channel', 'N/A')}")
        print(f"   CTA: {idea.get('cta', 'N/A')}")
        print()

    return ideas


def test_chat_with_context():
    """Testa chat contextual."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 4: Chat Contextual")
    print("=" * 70)

    ai = AIInsightsEngine(
        llm_provider=LLMProvider.GROQ,
        obsidian_copilot_enabled=True
    )

    response = ai.chat_with_context(
        question="Qual o LTV atual e como melhorar?",
        context={
            'tenant_name': 'Empresa XYZ',
            'current_ltv': 350,
            'benchmark_ltv': 600,
            'tenant_type': 'ecommerce'
        },
        vault_context=[
            "LTV melhorou 15% após programa de fidelidade",
            "Ticket médio: R$ 175, Compra recorrente: 2x/mês",
            "Programa de pontos implementado em janeiro/2026"
        ]
    )

    print(f"\n💬 Resposta:\n{response.message[:500]}...")
    print(f"\n📚 Fontes: {len(response.sources)}")
    print(f"❓ Follow-ups: {response.follow_up_questions[:3]}")

    return response


def test_write_to_obsidian():
    """Testa escrita de insights no Obsidian."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 5: Escrita no Obsidian")
    print("=" * 70)

    ai = AIInsightsEngine(
        llm_provider=LLMProvider.GROQ,
        obsidian_copilot_enabled=True
    )

    # Gerar insights
    insights = []
    for metric in ['cac', 'ltv', 'conversion_rate']:
        try:
            insight = ai.generate_insight_from_anomaly(
                metric_key=metric,
                current_value=65.0 if metric == 'cac' else 350 if metric == 'ltv' else 2.4,
                expected_value=30.0 if metric == 'cac' else 600 if metric == 'ltv' else 3.0,
                z_score=3.5 if metric == 'cac' else 2.1 if metric == 'ltv' else 1.5,
                tenant_name='Empresa Teste',
                tenant_type='ecommerce',
                historical_data=[{'date': '2026-03-01', 'value': 60}]
            )
            insights.append(insight)
        except Exception as e:
            print(f"⚠️ Erro ao gerar insight para {metric}: {e}")

    if insights:
        # Escrever no Obsidian
        obsidian_path = os.getenv("PATH_TO_OBSIDIAN", "C:/temp/obsidian_test")
        filepath = ai.write_insights_to_obsidian(
            insights=insights,
            tenant_name='Empresa Teste',
            obsidian_path=obsidian_path
        )

        print(f"\n✅ Insights escritos em: {filepath}")
        print(f"📂 Pasta: 🧠 EXOCÓRTEX/08 - AI Insights/Empresa Teste/")
    else:
        print("\n⚠️ Nenhum insight gerado para escrever")

    return insights


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "=" * 70)
    print("🤖 AI INSIGHTS ENGINE — TESTE COMPLETO")
    print("=" * 70)

    # Verificar API key
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "gsk-xxxxxxxxxxxxxxxx":
        print("\n⚠️ GROQ_API_KEY não configurada no .env")
        print("📝 Obtenha em: https://console.groq.com/keys")
        print("💡 Ou use LLM_PROVIDER=ollama para teste local")
        return

    print("\n✅ GROQ_API_KEY encontrada")
    print("🚀 Iniciando testes...\n")

    try:
        # Teste 1: Insight de anomalia
        test_insight_from_anomaly()

        # Teste 2: Relatório semanal
        test_weekly_report()

        # Teste 3: Ideias de conteúdo
        test_content_ideas()

        # Teste 4: Chat contextual
        test_chat_with_context()

        # Teste 5: Escrita no Obsidian
        test_write_to_obsidian()

        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
