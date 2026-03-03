"""
╔═══════════════════════════════════════════════════════════════════════════════
║ NOTIFICATION DISPATCHER — Notificações Sob Demanda
╠═══════════════════════════════════════════════════════════════════════════════
║ Envia notificações APENAS quando necessário (sem processos 24/7)
║ Canais: E-mail (principal), Slack, Telegram, WhatsApp, Push
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
import smtplib
from typing import Dict, List, Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.html import MIMEHtml
import requests

from .email_templates import (
    create_critical_alert_email,
    create_daily_digest_email,
    create_weekly_summary_email
)

logger = logging.getLogger(__name__)


class NotificationDispatcher:
    """
    Dispatcher de notificações sob demanda.
    Sem processos rodando 24/7.
    Sem tokens gastos desnecessariamente.
    """

    def __init__(self):
        """Inicializa dispatcher com configurações do ambiente."""
        # E-mail (SMTP)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.email_from = os.getenv("EMAIL_FROM", "alertas@cmo360.com")
        self.email_from_name = os.getenv("EMAIL_FROM_NAME", "CMO 360° Alertas")

        # Slack
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

        # Telegram
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

        # WhatsApp (Twilio)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        # Push (Firebase/OneSignal)
        self.push_endpoint = os.getenv("PUSH_SERVICE_URL")

        logger.info("📬 NotificationDispatcher inicializado")

    def send_critical_alert(
        self,
        alert: Dict,
        channels: List[str] = None,
        user_preferences: Optional[Dict] = None
    ) -> Dict[str, bool]:
        """
        Envia alerta crítico SOB DEMANDA.

        Args:
            alert: Dados do alerta (metric_key, metric_value, z_score, tenant_name, etc.)
            channels: Lista de canais ['email', 'slack', 'telegram', 'whatsapp', 'push']
            user_preferences: Preferências do usuário (email, phone, etc.)

        Returns:
            Dicionário com status de cada canal
        """
        if not channels:
            channels = ['email']  # Default: só e-mail

        if not user_preferences:
            user_preferences = {}

        results = {
            'email': False,
            'slack': False,
            'telegram': False,
            'whatsapp': False,
            'push': False
        }

        for channel in channels:
            try:
                if channel == 'email':
                    results['email'] = self._send_email_alert(alert, user_preferences)
                elif channel == 'slack':
                    results['slack'] = self._send_slack_alert(alert)
                elif channel == 'telegram':
                    results['telegram'] = self._send_telegram_alert(alert, user_preferences)
                elif channel == 'whatsapp':
                    results['whatsapp'] = self._send_whatsapp_alert(alert, user_preferences)
                elif channel == 'push':
                    results['push'] = self._send_push_notification(alert, user_preferences)

            except Exception as e:
                logger.error(f"❌ Erro ao enviar via {channel}: {e}")
                results[channel] = False

        # Log resumo
        sent_count = sum(results.values())
        logger.info(f"📤 Alerta enviado para {sent_count}/{len(channels)} canal(is)")

        return results

    def send_daily_digest(
        self,
        alerts: List[Dict],
        tenant_name: str,
        user_email: str
    ) -> bool:
        """
        Envia resumo diário de alertas (uma vez por dia).

        Args:
            alerts: Lista de alertas do dia
            tenant_name: Nome do tenant
            user_email: E-mail do destinatário

        Returns:
            True se enviado com sucesso
        """
        if not alerts:
            return False

        try:
            subject = f"📊 Resumo Diário de Alertas — {tenant_name} — {datetime.now().strftime('%d/%m')}"

            # Criar HTML do digest
            html_content = create_daily_digest_email(alerts, tenant_name)

            # Enviar e-mail
            self._send_email(
                to_email=user_email,
                subject=subject,
                html_content=html_content
            )

            logger.info(f"✅ Daily digest enviado para {tenant_name} ({len(alerts)} alertas)")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao enviar daily digest: {e}")
            return False

    def send_weekly_summary(
        self,
        summary: Dict,
        tenant_name: str,
        user_email: str
    ) -> bool:
        """
        Envia resumo semanal (toda segunda-feira).

        Args:
            summary: Resumo da semana (métricas, insights, ações)
            tenant_name: Nome do tenant
            user_email: E-mail do destinatário

        Returns:
            True se enviado com sucesso
        """
        try:
            subject = f"📈 Resumo Semanal — {tenant_name} — Semana {datetime.now().isocalendar()[1]}"

            # Criar HTML do resumo
            html_content = create_weekly_summary_email(summary, tenant_name)

            # Enviar e-mail
            self._send_email(
                to_email=user_email,
                subject=subject,
                html_content=html_content
            )

            logger.info(f"✅ Weekly summary enviado para {tenant_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao enviar weekly summary: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS PRIVADOS — CANAIS
    # ═══════════════════════════════════════════════════════════════════════════

    def _send_email_alert(self, alert: Dict, user_preferences: Dict) -> bool:
        """Envia alerta crítico por e-mail."""
        to_email = user_preferences.get('email')

        if not to_email:
            logger.warning(f"⚠️  E-mail não configurado para usuário")
            return False

        # Assunto
        severity = alert.get('severity', 'critical').upper()
        metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()
        subject = f"🔴 [{severity}] {metric_key} — {alert.get('tenant_name', 'N/A')}"

        # Corpo do e-mail (HTML)
        html_content = create_critical_alert_email(alert)

        # Enviar
        return self._send_email(to_email, subject, html_content)

    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Envia e-mail via SMTP."""
        if not self.smtp_user or not self.smtp_password:
            logger.warning("⚠️  SMTP não configurado (SMTP_USER, SMTP_PASSWORD)")
            return False

        try:
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.email_from_name} <{self.email_from}>"
            msg['To'] = to_email

            # Versão HTML
            html_part = MIMEHtml(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Conectar e enviar
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.smtp_user, self.smtp_password)

            server.send_message(msg)
            server.quit()

            logger.info(f"✅ E-mail enviado para {to_email} — {subject}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao enviar e-mail: {e}")
            return False

    def _send_slack_alert(self, alert: Dict) -> bool:
        """Envia alerta via Slack webhook."""
        if not self.slack_webhook:
            return False

        severity = alert.get('severity', 'critical').upper()
        metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()
        metric_value = alert.get('metric_value', 0)
        expected_value = alert.get('expected_value', 'N/A')
        z_score = alert.get('z_score', 0)
        tenant_name = alert.get('tenant_name', 'N/A')

        # Slack blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🔴 ALERTA {severity}: {metric_key}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Tenant:*\n{tenant_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Z-Score:*\n{z_score:.2f}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Valor Atual:*\n{metric_value:.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Valor Esperado:*\n{expected_value}"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Ver Dashboard"},
                        "url": "http://localhost:5173",
                        "action_id": "view_dashboard"
                    }
                ]
            }
        ]

        payload = {"blocks": blocks}

        response = requests.post(self.slack_webhook, json=payload, timeout=10)

        if response.status_code == 200:
            logger.info("✅ Slack enviado")
            return True
        else:
            logger.error(f"❌ Slack falhou: {response.text}")
            return False

    def _send_telegram_alert(self, alert: Dict, user_preferences: Dict) -> bool:
        """Envia alerta via Telegram Bot API."""
        if not self.telegram_token:
            return False

        chat_id = user_preferences.get('telegram_chat_id')
        if not chat_id:
            logger.warning("⚠️  Telegram chat_id não configurado")
            return False

        metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()
        metric_value = alert.get('metric_value', 0)
        expected_value = alert.get('expected_value', 'N/A')
        z_score = alert.get('z_score', 0)
        tenant_name = alert.get('tenant_name', 'N/A')

        message = (
            f"🔴 *ALERTA CRÍTICO*\n\n"
            f"*{metric_key}*\n"
            f"Tenant: {tenant_name}\n\n"
            f"Valor: `{metric_value:.2f}`\n"
            f"Esperado: `{expected_value}`\n"
            f"Z-Score: `{z_score:.2f}`\n\n"
            f"[Ver Dashboard](http://localhost:5173)"
        )

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            logger.info(f"✅ Telegram enviado para {chat_id}")
            return True
        else:
            logger.error(f"❌ Telegram falhou: {response.text}")
            return False

    def _send_whatsapp_alert(self, alert: Dict, user_preferences: Dict) -> bool:
        """Envia alerta via WhatsApp (Twilio)."""
        if not self.twilio_account_sid or not self.twilio_auth_token:
            return False

        to_phone = user_preferences.get('whatsapp_number')
        if not to_phone:
            logger.warning("⚠️  WhatsApp número não configurado")
            return False

        metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()
        metric_value = alert.get('metric_value', 0)
        z_score = alert.get('z_score', 0)
        tenant_name = alert.get('tenant_name', 'N/A')

        message = (
            f"🔴 ALERTA {alert.get('severity', 'critical').upper()}\n\n"
            f"{metric_key}\n"
            f"Tenant: {tenant_name}\n\n"
            f"Valor: {metric_value:.2f}\n"
            f"Z-Score: {z_score:.2f}\n\n"
            f"Ver: http://localhost:5173"
        )

        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"

        payload = {
            'From': f'whatsapp:{self.twilio_whatsapp_number}',
            'To': f'whatsapp:+55{to_phone}',
            'Body': message
        }

        response = requests.post(
            url,
            auth=(self.twilio_account_sid, self.twilio_auth_token),
            data=payload,
            timeout=10
        )

        if response.status_code in [200, 201]:
            logger.info(f"✅ WhatsApp enviado para +55{to_phone}")
            return True
        else:
            logger.error(f"❌ WhatsApp falhou: {response.text}")
            return False

    def _send_push_notification(self, alert: Dict, user_preferences: Dict) -> bool:
        """Envia push notification (Firebase/OneSignal)."""
        if not self.push_endpoint:
            return False

        metric_key = alert.get('metric_key', 'unknown').replace('_', ' ').title()

        payload = {
            'user_id': user_preferences.get('user_id'),
            'title': f"🔴 {metric_key}",
            'body': f"Valor: {alert.get('metric_value', 0):.2f}",
            'data': {
                'type': 'critical_alert',
                'alert_id': alert.get('id'),
                'tenant_id': alert.get('tenant_id'),
                'severity': alert.get('severity')
            }
        }

        response = requests.post(self.push_endpoint, json=payload, timeout=10)

        if response.status_code == 200:
            logger.info(f"✅ Push enviado para {user_preferences.get('user_id')}")
            return True
        else:
            logger.error(f"❌ Push falhou: {response.text}")
            return False
