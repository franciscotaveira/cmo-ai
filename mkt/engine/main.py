"""
╔═══════════════════════════════════════════════════════════════════════════════
║ MARKETING DIRECTOR OS — MAIN.PY
╠═══════════════════════════════════════════════════════════════════════════════
║ Ponto de entrada principal do Marketing Engine
║ Inicia o watcher de arquivos e mantém o sistema rodando
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import logging
import time
import threading
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Request
import uvicorn

from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger("marketing_engine")

# Importar módulos do engine
from src.database import DatabaseHandler
from src.processor import FileProcessor
from src.watcher import DriveWatcher, WatcherManager
from src.obsidian import ObsidianBridge
from src.kanban_board import KanbanBoard
from src.priority_engine import PriorityEngine
from src.marketing_strategy import MarketingStrategyEngine
from src.goal_setting import GoalSettingEngine, TimeHorizon
from src.marketing_calendar import MarketingCalendar
from src.budget_tracker import BudgetTracker
from src.ai_insights import AIInsightsEngine, LLMProvider
from src.growth_marketing import GrowthMarketingEngine
from src.brand_communication import BrandCommunicationEngine
from src.executive_dashboard import ExecutiveDashboard
from src.cmo_bench import CMOLearningLoop, BusinessIssue
from src.notification_dispatcher import NotificationDispatcher

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

DRIVE_PATH = os.getenv("PATH_TO_DRIVE", "/app/drive_input")
OBSIDIAN_PATH = os.getenv("PATH_TO_OBSIDIAN", "/app/obsidian_output")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ═══════════════════════════════════════════════════════════════════════════════
# WEBHOOK SERVER & API (FastAPI)
# ═══════════════════════════════════════════════════════════════════════════════

from src.api_routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CMO 360° - Webhook & API Receiver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.post("/webhook/approve")
async def approve_action(request: Request):
    """Recebe aprovações vindas do Obsidian."""
    try:
        data = await request.json()
        logger.info(f"📥 Webhook recebido: {data}")
        tenant = data.get("tenant", "desconhecido")
        action = data.get("action_type", "no-action")
        logger.info(f"🚀 EXECUTANDO: {action} para {tenant}")
        return {"status": "success", "message": f"Ação {action} iniciada para {tenant}"}
    except Exception as e:
        logger.error(f"❌ Erro no webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    Função principal de inicialização do engine — v5.0 EXOCÓRTEX.

    Novidades v5.0:
    • Estrutura de pastas encapsulada (🧠 EXOCÓRTEX)
    • Kanban de Rotina (Jarvis-Board)
    • Priorização por Z-Score (gestão por risco)
    """

    # Imprimir banner
    logger.info("=" * 70)
    logger.info("🚀 MARKETING ENGINE v5.3 — CMO 360° COMPLETO")
    logger.info("=" * 70)

    # Validar ambiente
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        logger.error("❌ Credenciais do Supabase não encontradas no .env")
        sys.exit(1)

    # Criar pastas se não existirem
    os.makedirs(DRIVE_PATH, exist_ok=True)
    os.makedirs(OBSIDIAN_PATH, exist_ok=True)

    # Inicializar componentes
    logger.info("🔧 Inicializando componentes...")

    try:
        # Database
        db = DatabaseHandler()
        logger.info("✅ DatabaseHandler inicializado")

        # Processor
        processor = FileProcessor(db)
        logger.info("✅ FileProcessor inicializado")

        # Obsidian Bridge (v5.0: com estrutura encapsulada)
        obsidian = ObsidianBridge(OBSIDIAN_PATH, db)
        logger.info("✅ ObsidianBridge inicializado (v5.0)")

        # Kanban Board (v5.0: NOVO)
        kanban = KanbanBoard(OBSIDIAN_PATH)
        logger.info("✅ KanbanBoard inicializado (v5.0)")

        # Priority Engine (v5.0: NOVO)
        priority = PriorityEngine()
        logger.info("✅ PriorityEngine inicializado (v5.0)")

        # Marketing Strategy Engine (v5.1: NOVO)
        strategy = MarketingStrategyEngine()
        logger.info("📋 MarketingStrategyEngine inicializado (v5.1)")

        # Goal Setting Engine (v5.1: NOVO)
        goals = GoalSettingEngine()
        logger.info("🎯 GoalSettingEngine inicializado (v5.1)")

        # Marketing Calendar (v5.1: NOVO)
        calendar = MarketingCalendar()
        logger.info("📅 MarketingCalendar inicializado (v5.1)")

        # Budget Tracker (v5.1: NOVO)
        budget = BudgetTracker()
        logger.info("💰 BudgetTracker inicializado (v5.1)")

        # AI Insights Engine (v5.2: Smart Routing)
        llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()
        provider_enum = getattr(LLMProvider, llm_provider.upper(), LLMProvider.GROQ)
        ai_insights = AIInsightsEngine(
            llm_provider=provider_enum,
            obsidian_copilot_enabled=True
        )
        logger.info(f"🤖 AIInsightsEngine inicializado ({llm_provider.upper()})")

        # Growth Marketing Engine (v5.3: NOVO - CMO 360°)
        growth = GrowthMarketingEngine()
        logger.info("📈 GrowthMarketingEngine inicializado (v5.3)")

        # Brand Communication Engine (v5.3: NOVO - CMO 360°)
        brand = BrandCommunicationEngine()
        logger.info("🏛️ BrandCommunicationEngine inicializado (v5.3)")

        # Executive Dashboard (v5.3: NOVO - CMO 360°)
        cmo_dashboard = ExecutiveDashboard()
        logger.info("📊 ExecutiveDashboard inicializado (v5.3)")

        # CMO-Bench (v6.0: NOVO - Aprendizado tipo SWE-bench)
        cmo_bench = CMOLearningLoop(db)
        logger.info("🧠 CMOLearningLoop inicializado (v6.0)")

        # Notification Dispatcher (v6.1: NOVO - Notificações multi-canal)
        notifications = NotificationDispatcher()
        logger.info("📬 NotificationDispatcher inicializado (v6.1)")

    except Exception as e:
        logger.error(f"❌ Erro ao inicializar componentes: {e}")
        sys.exit(1)

    # Health check inicial
    logger.info("🏥 Executando health check...")
    if db.health_check():
        logger.info("✅ Supabase conectado")
    else:
        logger.error("❌ Erro de conexão com Supabase")
        sys.exit(1)

    # Iniciar watcher
    logger.info(f"🚀 Iniciando watcher para: {DRIVE_PATH}")

    def on_file_processed(result):
        """Callback chamado após processar cada arquivo."""
        if result.get("success"):
            logger.info(
                f"✅ Processado: {result.get('filename', 'N/A')} | "
                f"Métricas: {result.get('metrics_count', 0)}"
            )

            # v5.0: Adicionar tarefa ao Backlog automaticamente
            tenant_id = result.get('tenant_id')
            if tenant_id:
                tenant = db.get_tenant_by_slug(result.get('tenant_slug', ''))
                if tenant:
                    kanban.add_task_to_backlog({
                        'id': f"proc-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'title': f"Arquivo processado: {result.get('filename', 'N/A')}",
                        'description': f"Novo arquivo processado com {result.get('metrics_count', 0)} métricas",
                        'priority': 'low',
                        'tenant': tenant.get('name', 'N/A'),
                        'metric': 'file_processing',
                        'action': 'Revisar dashboard atualizado'
                    })
        else:
            logger.warning(
                f"❌ Erro: {result.get('filename', 'N/A')} - "
                f"{result.get('error', 'N/A')}"
            )

    # Iniciar watcher em thread separada
    try:
        def start_watcher():
            manager = WatcherManager(
                drive_path=DRIVE_PATH,
                obsidian_path=OBSIDIAN_PATH,
                db=db,
                on_file_processed=on_file_processed
            )
            logger.info(f"🚀 Watcher iniciado em {DRIVE_PATH}")
            manager.run_forever()

        watcher_thread = threading.Thread(target=start_watcher, daemon=True)
        watcher_thread.start()

        # v5.0: Loop de atualização do Kanban e Priorização
        def background_tasks():
            """Executa tarefas em segundo plano (a cada 5 minutos)."""
            while True:
                try:
                    logger.info("🔄 Atualizando Kanban, Priorização e Planejamento...")

                    # Obter todas as unidades e métricas
                    all_tenants = db.client.table("tenants").select("id, name, slug, type").execute()

                    units_data = []
                    for tenant in all_tenants.data:
                        metrics = db.get_metrics_by_tenant(tenant['id'], limit=50)
                        units_data.append({
                            'id': tenant['id'],
                            'name': tenant['name'],
                            'slug': tenant['slug'],
                            'type': tenant.get('type', 'default'),
                            'metrics': [{'key': m['metric_key'], 'value': m['metric_value']} for m in metrics]
                        })

                    # v5.0: Priorizar unidades por Z-Score
                    prioritized_units = priority.prioritize_units(units_data)

                    # v5.0: Gerar resumo executivo com priorização
                    priority.generate_summary_with_priority(prioritized_units, OBSIDIAN_PATH)

                    # v5.0: Atualizar Kanban Board
                    kanban.generate_kanban_board()

                    # v5.0: Adicionar alertas críticos ao Kanban
                    for unit in prioritized_units:
                        try:
                            if unit.get('severity') == 'critical':
                                for metric in unit.get('critical_metrics', [])[:1]:
                                    kanban.add_critical_alert({
                                        'id': f"alert-{unit['slug']}-{metric['metric_key']}",
                                        'title': f"Anomalia em {unit['name']}",
                                        'tenant': unit['name'],
                                        'metric': metric['metric_key'],
                                        'value': metric['current_value'],
                                        'expected': metric['historical_mean'],
                                        'z_score': metric['z_score'],
                                        'action': metric['recommendation']
                                    })
                        except Exception as e:
                            logger.error(f"⚠️ Erro ao processar alertas para {unit.get('slug')}: {e}")

                    # v5.1: NOVO - Gerar estratégias automáticas
                    logger.info("📋 Gerando estratégias automáticas...")
                    strategy.generate_all_strategies(units_data, OBSIDIAN_PATH)

                    # v5.1: NOVO - Gerar metas e forecasting
                    logger.info("🎯 Gerando metas e previsões...")
                    goals.generate_all_goals_and_forecasts(units_data, OBSIDIAN_PATH, TimeHorizon.MONTHLY)

                    # v5.1: NOVO - Gerar calendário de marketing
                    logger.info("📅 Gerando calendário de marketing...")
                    calendar.generate_calendar_for_all_tenants(units_data, OBSIDIAN_PATH)

                    # v5.1: NOVO - Gerar relatório de budget e ROI
                    logger.info("💰 Gerando relatório de budget e ROI...")
                    budget.generate_budget_report_for_all_tenants(units_data, OBSIDIAN_PATH)

                    # v5.2: NOVO - Gerar AI Insights
                    logger.info("🤖 Gerando AI Insights...")
                    ai_insights.generate_insights_for_all_tenants(
                        tenants_data=units_data,
                        anomalies=[],  # v5.3: Todo - extrair anomalias reais do priority engine
                        obsidian_path=OBSIDIAN_PATH
                    )

                    # Iteração por tenant para relatórios específicos v5.3
                    for tenant in units_data:
                        try:
                            tenant_name = tenant.get('name', 'Unknown')
                            tenant_id = tenant.get('id')
                            
                            logger.info(f"📈 Processando relatórios 360° para: {tenant_name}")

                            # v5.3: Growth & Performance (Tentando dados reais)
                            # Se não houver dados, o engine deve lidar ou mostrar N/A
                            metrics_dict = {m['key']: m['value'] for m in tenant.get('metrics', [])}
                            
                            growth.track_channel_performance(
                                channel='google_ads',
                                period=datetime.now().strftime('%Y-%m'),
                                spend=metrics_dict.get('google_ads_spend', 0),
                                impressions=int(metrics_dict.get('google_ads_impressions', 0)),
                                clicks=int(metrics_dict.get('google_ads_clicks', 0)),
                                leads=int(metrics_dict.get('google_ads_leads', 0)),
                                customers=int(metrics_dict.get('google_ads_customers', 0)),
                                revenue=metrics_dict.get('google_ads_revenue', 0)
                            )
                            growth.write_growth_report_to_obsidian(tenant_name, OBSIDIAN_PATH)

                            # v5.3: Brand & Communication
                            brand.track_brand_health(
                                period=datetime.now().strftime('%Y-%m'),
                                unaided_awareness=metrics_dict.get('brand_awareness_unaided', 0),
                                aided_awareness=metrics_dict.get('brand_awareness_aided', 0),
                                consideration=metrics_dict.get('brand_consideration', 0),
                                nps=metrics_dict.get('nps', 0),
                                sov=metrics_dict.get('sov', 0),
                                positive_sentiment=metrics_dict.get('sentiment_positive', 0),
                                negative_sentiment=metrics_dict.get('sentiment_negative', 0),
                                retention_rate=metrics_dict.get('retention_rate', 0),
                                share_of_search=metrics_dict.get('share_of_search', 0)
                            )
                            brand.write_brand_report_to_obsidian(tenant_name, OBSIDIAN_PATH)

                            # v6.0: CMO-Bench — Processar alertas com aprendizado
                            logger.info(f"🧠 CMO-Bench: Processando alertas para {tenant_name}...")
                            critical_alerts = db.get_critical_alerts(tenant_id=tenant_id, limit=5)
                            for alert in critical_alerts:
                                try:
                                    business_issue = BusinessIssue(
                                        id=alert.get('id'),
                                        title=f"{alert.get('metric_key')} {alert.get('severity')}",
                                        description=f"{alert.get('metric_key')} está {alert.get('z_score', 0):.2f} desvios acima",
                                        tenant_id=tenant_id,
                                        tenant_type='default',
                                        severity=alert.get('severity', 'medium'),
                                        detected_at=alert.get('detected_at'),
                                        metrics_involved=[alert.get('metric_key')]
                                    )
                                    result = cmo_bench.process_business_issue(business_issue, tenant_id)
                                    if result.get('learned'):
                                        logger.info(f"✅ CMO-Bench aprendeu com alerta: {alert.get('id')}")
                                except Exception as e:
                                    logger.error(f"⚠️ Erro no CMO-Bench para {tenant_name}: {e}")

                            # v6.1: Notification Dispatcher — Enviar alertas por e-mail
                            logger.info(f"📬 Notifications: Verificando alertas para {tenant_name}...")
                            critical_alerts = db.get_critical_alerts(tenant_id=tenant_id, status='new', limit=10)
                            if critical_alerts:
                                try:
                                    # Obter e-mail do tenant (simplificado - na prática viria do banco)
                                    tenant_owner_email = "admin@empresa.com"  # Substituir por busca real

                                    for alert in critical_alerts:
                                        notifications.send_critical_alert(
                                            alert=alert,
                                            channels=['email'],
                                            user_preferences={'email': tenant_owner_email}
                                        )
                                        # Marcar como notificado
                                        db.update_alert_status(alert.get('id'), 'acknowledged')

                                    logger.info(f"✅ {len(critical_alerts)} alertas notificados para {tenant_name}")
                                except Exception as e:
                                    logger.error(f"⚠️ Erro ao enviar notificações para {tenant_name}: {e}")
                            else:
                                logger.info(f"✅ Sem novos alertas para {tenant_name}")

                            # v5.3: CMO Executive Dashboard (Integrado com dados reais)
                            cmo_dashboard.generate_cmo_dashboard(
                                tenant_name=tenant_name,
                                obsidian_path=OBSIDIAN_PATH,
                                growth_data=growth.get_channel_insights('google_ads'),
                                brand_data=None,  # Brand health é rastreado mas insights precisam de agregação
                                budget_data={'total': 10000, 'spent': 5000, 'remaining': 5000, 'utilization': 50, 'roi': 2.5, 'allocations': []}, # Simplificado
                                strategy_data={'active_count': 2, 'active': [], 'goals': []}, # Simplificado
                                ai_insights=[]
                            )
                        except Exception as e:
                            logger.error(f"❌ Erro ao processar tenant {tenant.get('name')}: {e}")

                    logger.info("✅ Ciclo de atualização de background concluído")

                except Exception as e:
                    logger.error(f"❌ Erro em background tasks: {e}")

                # Aguardar 5 minutos
                time.sleep(300)

        # Iniciar thread de background tasks
        background_thread = threading.Thread(target=background_tasks, daemon=True)
        background_thread.start()
        logger.info("🔄 Background tasks iniciadas (atualização a cada 5 min)")

        # Iniciar Web Server (Blocking)
        logger.info("✅" * 30)
        logger.info("🎯 MARKETING ENGINE v6.1 — CMO 360° 100% INTEGRADO")
        logger.info(f"🌐 Servidor de Webhooks: http://0.0.0.0:8088")
        logger.info(f"🧠 Exocórtex: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX")
        logger.info("")
        logger.info("📊 ÁREAS DE MARKETING (10/10):")
        logger.info(f"📈 Growth: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/09 - Growth & Performance")
        logger.info(f"🏛️ Brand: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/10 - Brand & Communication")
        logger.info(f"📋 Estratégia: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/04 - Estratégias")
        logger.info(f"💰 Budget: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/07 - Budget & ROI")
        logger.info(f"🎯 Metas: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/05 - Metas & Forecasting")
        logger.info(f"📅 Calendário: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/06 - Calendário")
        logger.info(f"🤖 AI: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/08 - AI Insights")
        logger.info(f"📋 Kanban: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/03 - Kanban Rotina")
        logger.info(f"🚨 Alertas: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/02 - Alertas Críticos")
        logger.info(f"📊 Dashboards: {OBSIDIAN_PATH}/🧠 EXOCÓRTEX/00 - Dashboards")
        logger.info("")
        logger.info("🆕 NOVO na v6.1:")
        logger.info(f"🧠 CMO-Bench: Aprendizado com casos passados")
        logger.info(f"📬 Notifications: E-mails automáticos de alertas")
        logger.info(f"🎨 Frontend: React + Vite + BGPattern")
        logger.info("✅" * 30)

        uvicorn.run(app, host="0.0.0.0", port=8088)
        
    except KeyboardInterrupt:
        logger.info("\n⌨️ Interrupt recebido")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
    finally:
        logger.info("👋 Marketing Engine encerrado")


# ═══════════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
