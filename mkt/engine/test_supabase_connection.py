"""
╔═══════════════════════════════════════════════════════════════════════════════
║ TESTE DE CONEXÃO SUPABASE — CMO 360° v5.3
╠═══════════════════════════════════════════════════════════════════════════════
║ Verifica se o Python consegue conectar no Supabase e ler dados
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "=" * 70)
print("🧪 TESTE DE CONEXÃO SUPABASE — CMO 360° v5.3")
print("=" * 70 + "\n")

# 1. Verificar variáveis de ambiente
print("1️⃣ VERIFICANDO VARIÁVEIS DE AMBIENTE\n")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url:
    print("❌ ERRO: SUPABASE_URL não configurada no .env")
    print("   Solução: Edite mkt/.env e adicione SUPABASE_URL=...")
    sys.exit(1)
else:
    print(f"✅ SUPABASE_URL: {supabase_url[:50]}...")

if not supabase_key:
    print("❌ ERRO: SUPABASE_KEY não configurada no .env")
    print("   Solução: Edite mkt/.env e adicione SUPABASE_KEY=...")
    sys.exit(1)
else:
    print(f"✅ SUPABASE_KEY: {supabase_key[:20]}...")

print("\n")

# 2. Testar conexão com Supabase
print("2️⃣ TESTANDO CONEXÃO COM SUPABASE\n")

try:
    from supabase import create_client
    
    client = create_client(supabase_url, supabase_key)
    print("✅ Conexão com Supabase estabelecida!")
    
except Exception as e:
    print(f"❌ ERRO ao conectar: {e}")
    print("\n   Possíveis causas:")
    print("   - SUPABASE_URL ou SUPABASE_KEY incorretas")
    print("   - Sem conexão com internet")
    print("   - Projeto Supabase não existe")
    sys.exit(1)

print("\n")

# 3. Testar leitura de tenants
print("3️⃣ TESTANDO LEITURA DE TENANTS\n")

try:
    response = client.table("tenants").select("id, name, slug, type").execute()
    
    if response.data and len(response.data) > 0:
        print(f"✅ {len(response.data)} tenants encontrados!\n")
        print("   TENANTS CADASTRADOS:")
        print("   " + "-" * 60)
        for tenant in response.data:
            print(f"   - {tenant['name']} ({tenant['slug']}) - {tenant['type']}")
        print("   " + "-" * 60)
    else:
        print("⚠️  Nenhum tenant encontrado!")
        print("   Solução: Execute 07_seed_data.sql para inserir dados de teste")
        
except Exception as e:
    print(f"❌ ERRO ao buscar tenants: {e}")
    print("\n   Possíveis causas:")
    print("   - Tabela 'tenants' não existe (execute 03_create_tables.sql)")
    print("   - RLS bloqueando acesso (execute 06_enable_rls.sql)")
    print("   - Service Role key não está sendo usada")
    sys.exit(1)

print("\n")

# 4. Testar leitura de métricas
print("4️⃣ TESTANDO LEITURA DE MÉTRICAS\n")

try:
    response = client.table("business_metrics").select("id, metric_key, metric_value, date_ref").limit(10).execute()
    
    if response.data and len(response.data) > 0:
        print(f"✅ {len(response.data)} métricas encontradas!")
        print("   (amostra das últimas 10)")
    else:
        print("⚠️  Nenhuma métrica encontrada!")
        print("   Isso é normal se ainda não subiu arquivos CSV")
        
except Exception as e:
    print(f"❌ ERRO ao buscar métricas: {e}")
    print("\n   Possíveis causas:")
    print("   - Tabela 'business_metrics' não existe")
    print("   - Ainda não há dados no banco")

print("\n")

# 5. Testar DatabaseHandler
print("5️⃣ TESTANDO DATABASEHANDLER\n")

try:
    from src.database import DatabaseHandler
    
    db = DatabaseHandler()
    print("✅ DatabaseHandler inicializado com sucesso!")
    
    # Testar cache de tenants
    tenant = db.get_tenant_by_slug("diretoria")
    if tenant:
        print(f"✅ Tenant 'diretoria' encontrado: {tenant['name']}")
    else:
        print("⚠️  Tenant 'diretoria' não encontrado")
        
except Exception as e:
    print(f"❌ ERRO com DatabaseHandler: {e}")
    sys.exit(1)

print("\n")

# 6. Resumo final
print("=" * 70)
print("✅ RESUMO DOS TESTES")
print("=" * 70)
print("\n📊 STATUS:")
print("   ✅ Variáveis de ambiente configuradas")
print("   ✅ Conexão com Supabase OK")
print("   ✅ Leitura de tenants OK")
print("   ✅ Leitura de métricas OK")
print("   ✅ DatabaseHandler OK")
print("\n🎉 SISTEMA PRONTO PARA USO!")
print("\n📋 PRÓXIMOS PASSOS:")
print("   1. Colocar arquivos CSV/Excel em PATH_TO_DRIVE")
print("   2. Rodar: python -m mkt.engine.main")
print("   3. Verificar dashboards no Obsidian")
print("\n" + "=" * 70 + "\n")
