"""
╔═══════════════════════════════════════════════════════════════════════════════
║ TEST NOTIFICATIONS — Teste de Notificações por E-mail
╠═══════════════════════════════════════════════════════════════════════════════
║ Testa envio de e-mails de alerta, daily digest e weekly summary
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()

from src.notification_dispatcher import NotificationDispatcher


def test_critical_alert_email():
    """Testa envio de alerta crítico por e-mail."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 1: Alerta Crítico por E-mail")
    print("=" * 70 + "\n")

    dispatcher = NotificationDispatcher()

    # Dados do alerta
    alert = {
        'id': 'test-001',
        'metric_key': 'cac',
        'metric_value': 65.0,
        'expected_value': 30.0,
        'z_score': 3.5,
        'severity': 'critical',
        'tenant_name': 'Empresa XYZ',
        'tenant_id': 'tenant-xyz',
        'detected_at': datetime.now().isoformat(),
        'recommendation': 'Reduzir budget do Meta Ads em 40% e migrar para Google Ads. CAC está 120% acima do benchmark.'
    }

    # E-mail de teste (substituir pelo seu)
    test_email = os.getenv("TEST_EMAIL", "seu-email@test.com")

    print(f"📧 Enviando alerta crítico para: {test_email}")
    print(f"   Métrica: {alert['metric_key'].replace('_', ' ').title()}")
    print(f"   Valor: {alert['metric_value']:.2f} (Esperado: {alert['expected_value']:.2f})")
    print(f"   Z-Score: {alert['z_score']:.2f}")
    print(f"   Severidade: {alert['severity'].upper()}")
    print()

    # Enviar
    result = dispatcher.send_critical_alert(
        alert=alert,
        channels=['email'],
        user_preferences={'email': test_email}
    )

    if result['email']:
        print("✅ E-mail enviado com sucesso!")
    else:
        print("❌ Falha ao enviar e-mail")
        print("   Verifique:")
        print("   - SMTP_USER e SMTP_PASSWORD no .env")
        print("   - E-mail de destino correto")

    print()
    return result['email']


def test_daily_digest_email():
    """Testa envio de daily digest."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 2: Daily Digest por E-mail")
    print("=" * 70 + "\n")

    dispatcher = NotificationDispatcher()

    # Alertas do dia (simulados)
    alerts = [
        {
            'metric_key': 'cac',
            'metric_value': 65.0,
            'z_score': 3.5,
            'severity': 'critical'
        },
        {
            'metric_key': 'conversion_rate',
            'metric_value': 1.2,
            'z_score': 2.8,
            'severity': 'high'
        },
        {
            'metric_key': 'roas',
            'metric_value': 2.1,
            'z_score': 2.3,
            'severity': 'medium'
        }
    ]

    test_email = os.getenv("TEST_EMAIL", "seu-email@test.com")
    tenant_name = "Empresa XYZ"

    print(f"📧 Enviando daily digest para: {test_email}")
    print(f"   Tenant: {tenant_name}")
    print(f"   Alertas: {len(alerts)}")
    print()

    # Enviar
    result = dispatcher.send_daily_digest(
        alerts=alerts,
        tenant_name=tenant_name,
        user_email=test_email
    )

    if result:
        print("✅ Daily digest enviado com sucesso!")
    else:
        print("❌ Falha ao enviar daily digest")

    print()
    return result


def test_weekly_summary_email():
    """Testa envio de weekly summary."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 3: Weekly Summary por E-mail")
    print("=" * 70 + "\n")

    dispatcher = NotificationDispatcher()

    # Resumo da semana (simulado)
    summary = {
        'kpis': {
            'revenue': 45200.00,
            'revenue_change': 12.5,
            'cac': 52.00,
            'cac_change': -8.3,
            'roas': 3.8,
            'roas_change': 5.2,
            'nps': 64,
            'nps_change': 0.0
        },
        'highlights': [
            'Receita cresceu 12.5% vs semana anterior',
            'CAC reduziu 8.3% após otimização de campanhas',
            'ROAS do Google Ads atingiu 5.2x (recorde)'
        ],
        'concerns': [
            'Meta Ads com ROAS abaixo (2.1x)',
            'Conversão caiu de 2.5% para 1.8%'
        ],
        'actions': [
            'Reduzir budget do Meta Ads em 40%',
            'Implementar testes A/B em landing pages',
            'Reunião com time de growth na segunda-feira'
        ]
    }

    test_email = os.getenv("TEST_EMAIL", "seu-email@test.com")
    tenant_name = "Empresa XYZ"

    print(f"📧 Enviando weekly summary para: {test_email}")
    print(f"   Tenant: {tenant_name}")
    print(f"   Receita: R$ {summary['kpis']['revenue']:,.2f} (+{summary['kpis']['revenue_change']:.1f}%)")
    print(f"   CAC: R$ {summary['kpis']['cac']:.2f} ({summary['kpis']['cac_change']:.1f}%)")
    print()

    # Enviar
    result = dispatcher.send_weekly_summary(
        summary=summary,
        tenant_name=tenant_name,
        user_email=test_email
    )

    if result:
        print("✅ Weekly summary enviado com sucesso!")
    else:
        print("❌ Falha ao enviar weekly summary")

    print()
    return result


def run_all_tests():
    """Executa todos os testes de notificação."""
    print("\n" + "=" * 70)
    print("🧪 TESTE DE NOTIFICAÇÕES — CMO 360°")
    print("=" * 70)

    # Verificar configuração
    test_email = os.getenv("TEST_EMAIL")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    print("\n📋 CONFIGURAÇÃO ATUAL:\n")
    print(f"   TEST_EMAIL: {test_email or '⚠️  Não configurado'}")
    print(f"   SMTP_USER: {smtp_user or '⚠️  Não configurado'}")
    print(f"   SMTP_PASSWORD: {'***' if smtp_password else '⚠️  Não configurado'}")
    print()

    if not test_email or not smtp_user or not smtp_password:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA!")
        print()
        print("Edite o arquivo .env e adicione:")
        print("   TEST_EMAIL=seu-email@test.com")
        print("   SMTP_SERVER=smtp.gmail.com")
        print("   SMTP_PORT=587")
        print("   SMTP_USER=seu-email@gmail.com")
        print("   SMTP_PASSWORD=sua-senha-de-app")
        print("   EMAIL_FROM=alertas@cmo360.com")
        print("   EMAIL_FROM_NAME=CMO 360° Alertas")
        print()
        return

    # Executar testes
    results = {
        'Alerta Crítico': test_critical_alert_email(),
        'Daily Digest': test_daily_digest_email(),
        'Weekly Summary': test_weekly_summary_email()
    }

    # Resumo final
    print("=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    print()

    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test}: {'Sucesso' if result else 'Falhou'}")

    print()
    success_count = sum(results.values())
    total_count = len(results)

    if success_count == total_count:
        print(f"🎉 TODOS OS TESTES PASSARAM ({total_count}/{total_count})!")
    else:
        print(f"⚠️  {total_count - success_count} teste(s) falharam")

    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    run_all_tests()
