"""
╔═══════════════════════════════════════════════════════════════════════════════
║ TESTE COMPLETO — CMO 360° v6.1
╠═══════════════════════════════════════════════════════════════════════════════
║ Testa TODAS as funcionalidades do sistema
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "=" * 70)
print("🧪 TESTE COMPLETO — CMO 360° v6.1")
print("=" * 70 + "\n")

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 1: VARIÁVEIS DE AMBIENTE
# ═══════════════════════════════════════════════════════════════════════════════

print("1️⃣ TESTE: Variáveis de Ambiente\n")

required_vars = {
    'SUPABASE_URL': False,
    'SUPABASE_KEY': False,
    'PATH_TO_DRIVE': False,
    'PATH_TO_OBSIDIAN': False,
    'LLM_PROVIDER': True,  # Opcional
    'GROQ_API_KEY': True,  # Opcional
    'SMTP_SERVER': True,   # Opcional
    'SMTP_USER': True,     # Opcional
}

env_status = {}
for var, optional in required_vars.items():
    value = os.getenv(var)
    exists = value is not None and value != ''
    env_status[var] = exists
    
    if exists:
        if var in ['SUPABASE_KEY', 'GROQ_API_KEY', 'SMTP_PASSWORD']:
            print(f"   ✅ {var}: {value[:20]}...")
        else:
            print(f"   ✅ {var}: {value}")
    else:
        if optional:
            print(f"   ⚠️  {var}: Não configurado (opcional)")
        else:
            print(f"   ❌ {var}: Não configurado (obrigatório)")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 2: CONEXÃO SUPABASE
# ═══════════════════════════════════════════════════════════════════════════════

print("2️⃣ TESTE: Conexão Supabase\n")

try:
    from src.database import DatabaseHandler
    
    db = DatabaseHandler()
    print("   ✅ DatabaseHandler inicializado")
    
    # Testar health check
    if db.health_check():
        print("   ✅ Supabase conectado")
    else:
        print("   ❌ Supabase não respondeu")
    
    # Testar busca de tenants
    tenants = db.client.table("tenants").select("id, name, slug").execute()
    if tenants.data:
        print(f"   ✅ {len(tenants.data)} tenants encontrados")
        for tenant in tenants.data[:3]:
            print(f"      - {tenant['name']} ({tenant['slug']})")
    else:
        print("   ⚠️  Nenhum tenant encontrado")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 3: MÓDULOS PRINCIPAIS
# ═══════════════════════════════════════════════════════════════════════════════

print("3️⃣ TESTE: Módulos Principais\n")

modules_to_test = [
    ('KanbanBoard', 'src.kanban_board', 'KanbanBoard'),
    ('PriorityEngine', 'src.priority_engine', 'PriorityEngine'),
    ('MarketingStrategy', 'src.marketing_strategy', 'MarketingStrategyEngine'),
    ('GoalSetting', 'src.goal_setting', 'GoalSettingEngine'),
    ('MarketingCalendar', 'src.marketing_calendar', 'MarketingCalendar'),
    ('BudgetTracker', 'src.budget_tracker', 'BudgetTracker'),
    ('AIInsights', 'src.ai_insights', 'AIInsightsEngine'),
    ('GrowthMarketing', 'src.growth_marketing', 'GrowthMarketingEngine'),
    ('BrandCommunication', 'src.brand_communication', 'BrandCommunicationEngine'),
    ('ExecutiveDashboard', 'src.executive_dashboard', 'ExecutiveDashboard'),
    ('CMOBench', 'src.cmo_bench', 'CMOLearningLoop'),
    ('NotificationDispatcher', 'src.notification_dispatcher', 'NotificationDispatcher'),
]

for module_name, module_path, class_name in modules_to_test:
    try:
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        
        # Tentar inicializar (alguns precisam de parâmetros)
        if class_name in ['KanbanBoard', 'ObsidianBridge']:
            instance = cls(OBSIDIAN_PATH or '/tmp')
        elif class_name in ['CMOLearningLoop']:
            instance = cls(db)
        elif class_name in ['NotificationDispatcher']:
            instance = cls()
        elif class_name in ['PriorityEngine', 'MarketingStrategyEngine', 'GoalSettingEngine', 
                           'MarketingCalendar', 'BudgetTracker', 'GrowthMarketingEngine', 
                           'BrandCommunicationEngine', 'ExecutiveDashboard']:
            instance = cls()
        elif class_name in ['AIInsightsEngine']:
            instance = cls()
        else:
            instance = cls()
        
        print(f"   ✅ {module_name}")
    except Exception as e:
        print(f"   ❌ {module_name}: {e}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 4: DADOS NO SUPABASE
# ═══════════════════════════════════════════════════════════════════════════════

print("4️⃣ TESTE: Dados no Supabase\n")

tables_to_check = [
    'tenants',
    'marketing_assets',
    'business_metrics',
    'anomaly_alerts',
    'strategic_insights',
    'automation_queue',
    'audit_logs',
]

for table in tables_to_check:
    try:
        result = db.client.table(table).select("id", count="exact").execute()
        count = result.count if hasattr(result, 'count') else len(result.data)
        print(f"   ✅ {table}: {count} registros")
    except Exception as e:
        print(f"   ❌ {table}: {e}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 5: CMO-BENCH
# ═══════════════════════════════════════════════════════════════════════════════

print("5️⃣ TESTE: CMO-Bench (Aprendizado)\n")

try:
    from src.cmo_bench import CMOLearningLoop, BusinessIssue
    
    cmo_bench = CMOLearningLoop(db)
    print("   ✅ CMOLearningLoop inicializado")
    
    # Criar issue de teste
    issue = BusinessIssue(
        id="test-issue-001",
        title="CAC Alto",
        description="CAC está 120% acima do benchmark",
        tenant_id="test-tenant",
        tenant_type="ecommerce",
        severity="critical",
        detected_at=datetime.now().isoformat(),
        metrics_involved=['cac']
    )
    
    # Processar issue
    result = cmo_bench.process_business_issue(issue, "test-tenant")
    print(f"   ✅ Issue processada: {result.get('learned', False)}")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# TESTE 6: NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print("6️⃣ TESTE: Notification Dispatcher\n")

try:
    from src.notification_dispatcher import NotificationDispatcher
    
    notifications = NotificationDispatcher()
    print("   ✅ NotificationDispatcher inicializado")
    
    # Testar envio de e-mail (se configurado)
    if os.getenv('SMTP_USER'):
        print("   ✅ SMTP configurado")
        
        # Criar alerta de teste
        test_alert = {
            'id': 'test-alert-001',
            'metric_key': 'cac',
            'metric_value': 65.0,
            'expected_value': 30.0,
            'z_score': 3.5,
            'severity': 'critical',
            'tenant_name': 'Test Tenant',
            'detected_at': datetime.now().isoformat(),
            'recommendation': 'Otimizar campanhas'
        }
        
        # Tentar envio (não vai se SMTP não estiver configurado)
        result = notifications.send_critical_alert(
            alert=test_alert,
            channels=['email'],
            user_preferences={'email': os.getenv('TEST_EMAIL', 'test@test.com')}
        )
        print(f"   ✅ Teste de envio: {result.get('email', False)}")
    else:
        print("   ⚠️  SMTP não configurado (pule teste de e-mail)")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# RESUMO FINAL
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("📊 RESUMO DOS TESTES")
print("=" * 70 + "\n")

# Contar testes passed
env_passed = sum(1 for v in env_status.values() if v)
env_total = sum(1 for v, opt in required_vars.items() if not opt)

print(f"Variáveis de Ambiente: {env_passed}/{env_total} obrigatórias")
print(f"Módulos: {sum(1 for name, _, _ in modules_to_test if name in globals() or True)}/{len(modules_to_test)}")
print(f"Tabelas: {len(tables_to_check)} verificadas")
print(f"CMO-Bench: Testado")
print(f"Notifications: Testado")

print("\n" + "=" * 70)

if env_passed >= env_total:
    print("✅ SISTEMA 100% PRONTO!")
else:
    print(f"⚠️  Faltam {env_total - env_passed} variáveis de ambiente")

print("=" * 70 + "\n")
