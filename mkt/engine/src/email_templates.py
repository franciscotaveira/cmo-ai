"""
╔═══════════════════════════════════════════════════════════════════════════════
║ E-MAIL TEMPLATES — Templates HTML para Notificações
╠═══════════════════════════════════════════════════════════════════════════════
║ Templates profissionais e responsivos para e-mails de alerta
╚═══════════════════════════════════════════════════════════════════════════════
"""

from datetime import datetime
from typing import Dict, List


def create_critical_alert_email(alert: Dict) -> str:
    """
    Cria e-mail HTML para alerta crítico.
    """
    severity = alert.get('severity', 'critical').upper()
    metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()
    metric_value = alert.get('metric_value', 0)
    expected_value = alert.get('expected_value', 'N/A')
    z_score = alert.get('z_score', 0)
    tenant_name = alert.get('tenant_name', 'N/A')
    detected_at = alert.get('detected_at', datetime.now().isoformat())
    recommendation = alert.get('recommendation', 'Ver dashboard para mais detalhes.')

    # Cores por severidade
    severity_colors = {
        'CRITICAL': '#ef4444',
        'HIGH': '#f97316',
        'MEDIUM': '#eab308',
        'LOW': '#22c55e'
    }
    severity_color = severity_colors.get(severity, '#ef4444')

    # Format data
    try:
        dt = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
        detected_at_formatted = dt.strftime('%d/%m/%Y às %H:%M')
    except:
        detected_at_formatted = detected_at

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta Crítico — {metric_key}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
        .header {{ background-color: {severity_color}; color: white; padding: 24px; text-align: center; }}
        .header h1 {{ font-size: 24px; font-weight: bold; }}
        .content {{ padding: 32px 24px; }}
        .alert-box {{ background-color: #fef2f2; border-left: 4px solid {severity_color}; padding: 16px; margin-bottom: 24px; }}
        .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }}
        .metric-card {{ background-color: #f9fafb; padding: 16px; border-radius: 8px; }}
        .metric-label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; margin-bottom: 8px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #111827; }}
        .metric-sub {{ font-size: 12px; color: #9ca3af; margin-top: 4px; }}
        .recommendation {{ background-color: #f0f9ff; border-left: 4px solid #3b82f6; padding: 16px; margin-bottom: 24px; }}
        .recommendation h3 {{ font-size: 14px; color: #1e40af; margin-bottom: 8px; }}
        .recommendation p {{ font-size: 14px; color: #1e293b; line-height: 1.6; }}
        .button {{ display: inline-block; background-color: {severity_color}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 500; }}
        .footer {{ background-color: #f9fafb; padding: 24px; text-align: center; border-top: 1px solid #e5e7eb; }}
        .footer p {{ font-size: 12px; color: #6b7280; }}
        @media (max-width: 600px) {{
            .metric-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔴 ALERTA {severity}</h1>
            <p style="margin-top: 8px; font-size: 14px; opacity: 0.9;">{metric_key}</p>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Alert Box -->
            <div class="alert-box">
                <p style="font-size: 14px; color: #7f1d1d;">
                    <strong>Tenant:</strong> {tenant_name}<br>
                    <strong>Detectado:</strong> {detected_at_formatted}
                </p>
            </div>

            <!-- Metrics Grid -->
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Valor Atual</div>
                    <div class="metric-value">{metric_value:.2f}</div>
                    {f'<div class="metric-sub">Z-Score: {z_score:.2f}</div>' if z_score else ''}
                </div>
                <div class="metric-card">
                    <div class="metric-label">Valor Esperado</div>
                    <div class="metric-value" style="color: #6b7280;">{expected_value if isinstance(expected_value, str) else f'{expected_value:.2f}'}</div>
                    <div class="metric-sub">Benchmark</div>
                </div>
            </div>

            <!-- Recommendation -->
            <div class="recommendation">
                <h3>💡 Ação Recomendada</h3>
                <p>{recommendation}</p>
            </div>

            <!-- CTA Button -->
            <div style="text-align: center; margin-top: 32px;">
                <a href="http://localhost:5173" class="button">Ver Dashboard Completo</a>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>CMO 360° Platform</strong></p>
            <p style="margin-top: 8px;">Inteligência de Marketing para C-Level</p>
            <p style="margin-top: 16px; font-size: 11px; color: #9ca3af;">
                Este é um e-mail automático. Não responda.
            </p>
        </div>
    </div>
</body>
</html>
    """.strip()

    return html


def create_daily_digest_email(alerts: List[Dict], tenant_name: str) -> str:
    """
    Cria e-mail HTML para resumo diário de alertas.
    """
    date_str = datetime.now().strftime('%d/%m/%Y')

    # Agrupar por severidade
    critical = [a for a in alerts if a.get('severity') == 'critical']
    high = [a for a in alerts if a.get('severity') == 'high']
    medium = [a for a in alerts if a.get('severity') == 'medium']

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resumo Diário — {tenant_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
        .header {{ background-color: #1e40af; color: white; padding: 24px; text-align: center; }}
        .header h1 {{ font-size: 24px; font-weight: bold; }}
        .content {{ padding: 32px 24px; }}
        .summary-box {{ background-color: #f9fafb; padding: 20px; border-radius: 8px; margin-bottom: 24px; }}
        .alert-item {{ padding: 16px; border-left: 4px solid #e5e7eb; margin-bottom: 12px; background-color: #f9fafb; }}
        .alert-item.critical {{ border-left-color: #ef4444; }}
        .alert-item.high {{ border-left-color: #f97316; }}
        .alert-item.medium {{ border-left-color: #eab308; }}
        .alert-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .alert-title {{ font-size: 14px; font-weight: 600; color: #111827; }}
        .alert-severity {{ font-size: 11px; padding: 4px 8px; border-radius: 4px; font-weight: 500; text-transform: uppercase; }}
        .alert-severity.critical {{ background-color: #fee2e2; color: #991b1b; }}
        .alert-severity.high {{ background-color: #ffedd5; color: #9a3412; }}
        .alert-severity.medium {{ background-color: #fef3c7; color: #92400e; }}
        .alert-metrics {{ font-size: 13px; color: #6b7280; }}
        .button {{ display: inline-block; background-color: #1e40af; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 500; }}
        .footer {{ background-color: #f9fafb; padding: 24px; text-align: center; border-top: 1px solid #e5e7eb; }}
        .footer p {{ font-size: 12px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Resumo Diário</h1>
            <p style="margin-top: 8px; font-size: 14px; opacity: 0.9;">{tenant_name} — {date_str}</p>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Summary -->
            <div class="summary-box">
                <p style="font-size: 14px; color: #374151;">
                    <strong>Total de Alertas:</strong> {len(alerts)}<br>
                    <strong>🔴 Críticos:</strong> {len(critical)} | 
                    <strong>🟠 Altos:</strong> {len(high)} | 
                    <strong>🟡 Médios:</strong> {len(medium)}
                </p>
            </div>

            <!-- Critical Alerts -->
            {f'''
            <h2 style="font-size: 18px; color: #111827; margin-bottom: 16px;">🔴 Alertas Críticos ({len(critical)})</h2>
            ''' if critical else ''}

            {"".join([f"""
            <div class="alert-item critical">
                <div class="alert-header">
                    <span class="alert-title">{a.get('metric_key', 'unknown').replace('_', ' ').title()}</span>
                    <span class="alert-severity critical">Crítico</span>
                </div>
                <div class="alert-metrics">
                    Valor: <strong>{a.get('metric_value', 0):.2f}</strong> | 
                    Z-Score: <strong>{a.get('z_score', 0):.2f}</strong>
                </div>
            </div>
            """ for a in critical])}

            <!-- High Alerts -->
            {f'''
            <h2 style="font-size: 18px; color: #111827; margin-bottom: 16px; margin-top: 24px;">🟠 Alertas Altos ({len(high)})</h2>
            ''' if high else ''}

            {"".join([f"""
            <div class="alert-item high">
                <div class="alert-header">
                    <span class="alert-title">{a.get('metric_key', 'unknown').replace('_', ' ').title()}</span>
                    <span class="alert-severity high">Alto</span>
                </div>
                <div class="alert-metrics">
                    Valor: <strong>{a.get('metric_value', 0):.2f}</strong> | 
                    Z-Score: <strong>{a.get('z_score', 0):.2f}</strong>
                </div>
            </div>
            """ for a in high])}

            <!-- CTA Button -->
            <div style="text-align: center; margin-top: 32px;">
                <a href="http://localhost:5173" class="button">Ver Dashboard Completo</a>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>CMO 360° Platform</strong></p>
            <p style="margin-top: 8px;">Resumo diário automático de alertas</p>
        </div>
    </div>
</body>
</html>
    """.strip()

    return html


def create_weekly_summary_email(summary: Dict, tenant_name: str) -> str:
    """
    Cria e-mail HTML para resumo semanal.
    """
    week_number = datetime.now().isocalendar()[1]

    kpis = summary.get('kpis', {})
    highlights = summary.get('highlights', [])
    concerns = summary.get('concerns', [])
    actions = summary.get('actions', [])

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resumo Semanal — {tenant_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
        .header {{ background-color: #059669; color: white; padding: 24px; text-align: center; }}
        .header h1 {{ font-size: 24px; font-weight: bold; }}
        .content {{ padding: 32px 24px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background-color: #f9fafb; padding: 16px; border-radius: 8px; text-align: center; }}
        .kpi-value {{ font-size: 28px; font-weight: bold; color: #111827; }}
        .kpi-label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }}
        .kpi-change {{ font-size: 12px; margin-top: 8px; }}
        .kpi-change.positive {{ color: #059669; }}
        .kpi-change.negative {{ color: #dc2626; }}
        .section {{ margin-bottom: 24px; }}
        .section h2 {{ font-size: 16px; color: #111827; margin-bottom: 12px; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }}
        .list-item {{ padding: 12px; background-color: #f9fafb; margin-bottom: 8px; border-radius: 6px; font-size: 14px; color: #374151; }}
        .list-item.positive {{ border-left: 4px solid #059669; }}
        .list-item.negative {{ border-left: 4px solid #dc2626; }}
        .button {{ display: inline-block; background-color: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 500; }}
        .footer {{ background-color: #f9fafb; padding: 24px; text-align: center; border-top: 1px solid #e5e7eb; }}
        .footer p {{ font-size: 12px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📈 Resumo Semanal</h1>
            <p style="margin-top: 8px; font-size: 14px; opacity: 0.9;">{tenant_name} — Semana {week_number}</p>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- KPIs -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-value">R$ {kpis.get('revenue', 0):,.2f}</div>
                    <div class="kpi-label">Receita</div>
                    <div class="kpi-change {'positive' if kpis.get('revenue_change', 0) > 0 else 'negative'}">
                        {'↑' if kpis.get('revenue_change', 0) > 0 else '↓'} {abs(kpis.get('revenue_change', 0)):.1f}%
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">R$ {kpis.get('cac', 0):.2f}</div>
                    <div class="kpi-label">CAC</div>
                    <div class="kpi-change {'positive' if kpis.get('cac_change', 0) < 0 else 'negative'}">
                        {'↓' if kpis.get('cac_change', 0) < 0 else '↑'} {abs(kpis.get('cac_change', 0)):.1f}%
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{kpis.get('roas', 0):.2f}x</div>
                    <div class="kpi-label">ROAS</div>
                    <div class="kpi-change {'positive' if kpis.get('roas_change', 0) > 0 else 'negative'}">
                        {'↑' if kpis.get('roas_change', 0) > 0 else '↓'} {abs(kpis.get('roas_change', 0)):.1f}%
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{kpis.get('nps', 0)}</div>
                    <div class="kpi-label">NPS</div>
                    <div class="kpi-change {'positive' if kpis.get('nps_change', 0) > 0 else 'negative'}">
                        {'↑' if kpis.get('nps_change', 0) > 0 else '↓'} {abs(kpis.get('nps_change', 0)):.1f}%
                    </div>
                </div>
            </div>

            <!-- Highlights -->
            {f'''
            <div class="section">
                <h2>✅ Destaques Positivos</h2>
                {"".join([f'<div class="list-item positive">{h}</div>' for h in highlights])}
            </div>
            ''' if highlights else ''}

            <!-- Concerns -->
            {f'''
            <div class="section">
                <h2>⚠️ Pontos de Atenção</h2>
                {"".join([f'<div class="list-item negative">{c}</div>' for c in concerns])}
            </div>
            ''' if concerns else ''}

            <!-- Actions -->
            {f'''
            <div class="section">
                <h2>📋 Ações para Próxima Semana</h2>
                {"".join([f'<div class="list-item">{a}</div>' for a in actions])}
            </div>
            ''' if actions else ''}

            <!-- CTA Button -->
            <div style="text-align: center; margin-top: 32px;">
                <a href="http://localhost:5173" class="button">Ver Dashboard Completo</a>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>CMO 360° Platform</strong></p>
            <p style="margin-top: 8px;">Resumo semanal automático</p>
        </div>
    </div>
</body>
</html>
    """.strip()

    return html
