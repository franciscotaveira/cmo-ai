#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════
║ MARKETING DIRECTOR OS — TEST SYSTEM
╠═══════════════════════════════════════════════════════════════════════════════
║ Script de teste completo do sistema
╚═══════════════════════════════════════════════════════════════════════════════

Uso:
    python test_system.py

Pré-requisitos:
    - Docker rodando
    - .env configurado
    - Supabase com schema aplicado
"""

import os
import sys
import logging
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger("test_system")


def test_environment():
    """Testa se variáveis de ambiente estão configuradas."""
    logger.info("=" * 70)
    logger.info("TESTE 1: Variáveis de Ambiente")
    logger.info("=" * 70)
    
    required_vars = {
        "SUPABASE_URL": "URL do Supabase",
        "SUPABASE_KEY": "Chave do Supabase",
        "PATH_TO_DRIVE": "Pasta do Google Drive",
        "PATH_TO_OBSIDIAN": "Pasta do Obsidian",
    }
    
    all_present = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            if "KEY" in var:
                masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                logger.info(f"✅ {var}: {masked}")
            else:
                logger.info(f"✅ {var}: {value}")
        else:
            logger.error(f"❌ {var}: {description} - FALTANDO!")
            all_present = False
    
    return all_present


def test_supabase_connection():
    """Testa conexão com o Supabase."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 2: Conexão com Supabase")
    logger.info("=" * 70)
    
    try:
        from supabase import create_client
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        client = create_client(url, key)
        
        response = client.table("tenants").select("id, name, slug").execute()
        
        if response.data:
            logger.info(f"✅ Supabase conectado!")
            logger.info(f"📊 Tenants encontrados: {len(response.data)}")
            
            for tenant in response.data:
                logger.info(f"   - {tenant['name']} ({tenant['slug']})")
            
            return True
        else:
            logger.warning("⚠️ Supabase conectado, mas nenhum tenant encontrado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar no Supabase: {e}")
        return False


def test_docker_services():
    """Testa se serviços Docker estão rodando."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 3: Serviços Docker")
    logger.info("=" * 70)
    
    try:
        import subprocess
        
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            logger.info("✅ Docker Compose respondendo")
            
            lines = result.stdout.strip().split("\n")
            
            for line in lines[2:]:
                if line.strip() and "Up" in line:
                    logger.info(f"✅ Serviço rodando: {line.split()[0]}")
            
            return True
        else:
            logger.error("❌ Docker Compose não está rodando")
            return False
            
    except FileNotFoundError:
        logger.error("❌ Docker não encontrado")
        return False


def test_drive_folder():
    """Testa se pasta do Drive existe."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 4: Pasta do Drive")
    logger.info("=" * 70)
    
    drive_path = os.getenv("PATH_TO_DRIVE")
    
    if not drive_path:
        logger.error("❌ PATH_TO_DRIVE não configurado")
        return False
    
    if os.path.exists(drive_path):
        logger.info(f"✅ Pasta do Drive existe: {drive_path}")
        
        subdirs = [d for d in os.listdir(drive_path) if os.path.isdir(os.path.join(drive_path, d))]
        
        if subdirs:
            logger.info(f"📁 Subpastas encontradas: {len(subdirs)}")
            for subdir in subdirs:
                logger.info(f"   - {subdir}")
        
        return True
    else:
        logger.error(f"❌ Pasta do Drive não encontrada: {drive_path}")
        return False


def test_obsidian_folder():
    """Testa se pasta do Obsidian existe."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 5: Pasta do Obsidian")
    logger.info("=" * 70)
    
    obsidian_path = os.getenv("PATH_TO_OBSIDIAN")
    
    if not obsidian_path:
        logger.error("❌ PATH_TO_OBSIDIAN não configurado")
        return False
    
    if os.path.exists(obsidian_path):
        logger.info(f"✅ Pasta do Obsidian existe: {obsidian_path}")
        
        md_files = [f for f in os.listdir(obsidian_path) if f.endswith('.md')]
        
        if md_files:
            logger.info(f"📝 Arquivos Markdown encontrados: {len(md_files)}")
            for f in md_files[:5]:
                logger.info(f"   - {f}")
        
        return True
    else:
        logger.error(f"❌ Pasta do Obsidian não encontrada: {obsidian_path}")
        return False


def test_create_test_file():
    """Cria um arquivo de teste no Drive."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 6: Criar Arquivo de Teste")
    logger.info("=" * 70)
    
    drive_path = os.getenv("PATH_TO_DRIVE")
    
    if not drive_path or not os.path.exists(drive_path):
        logger.error("❌ Pasta do Drive não disponível")
        return False
    
    try:
        test_folder = os.path.join(drive_path, "salao-esposa")
        os.makedirs(test_folder, exist_ok=True)
        
        test_file = os.path.join(test_folder, "teste_vendas.csv")
        
        csv_content = """data,produto,valor,cliente
2024-01-15,Corte,150.00,Maria Silva
2024-01-15,Hidratacao,200.00,Ana Costa
2024-01-16,Manicure,80.00,Joana Santos
"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        logger.info(f"✅ Arquivo de teste criado: {test_file}")
        logger.info(f"📊 Conteúdo: 3 linhas de vendas")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar arquivo de teste: {e}")
        return False


def test_windmill_access():
    """Testa acesso ao Windmill."""
    logger.info("")
    logger.info("=" * 70)
    logger.info("TESTE 7: Acesso ao Windmill")
    logger.info("=" * 70)
    
    try:
        import requests
        
        windmill_url = "http://localhost:8000"
        
        response = requests.get(windmill_url, timeout=5)
        
        if response.status_code == 200:
            logger.info(f"✅ Windmill acessível em {windmill_url}")
            logger.info("💡 Login padrão:")
            logger.info("   Email: admin@windmill.dev")
            logger.info("   Senha: changeme")
            return True
        else:
            logger.warning(f"⚠️ Windmill retornou status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Windmill não respondendo em http://localhost:8000")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao testar Windmill: {e}")
        return False


def run_all_tests():
    """Executa todos os testes e gera relatório."""
    logger.info("")
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║" + " " * 15 + "MARKETING DIRECTOR OS - TEST SUITE" + " " * 19 + "║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")
    
    results = {
        "Variáveis de Ambiente": test_environment(),
        "Supabase": test_supabase_connection(),
        "Docker": test_docker_services(),
        "Drive": test_drive_folder(),
        "Obsidian": test_obsidian_folder(),
        "Test File": test_create_test_file(),
        "Windmill": test_windmill_access(),
    }
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("RELATÓRIO FINAL")
    logger.info("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
    
    logger.info("")
    logger.info(f"Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        logger.info("")
        logger.info("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
        logger.info("")
        logger.info("Próximos passos:")
        logger.info("1. Acesse http://localhost:8000 (Windmill)")
        logger.info("2. Abra seu Obsidian e veja os dashboards")
        logger.info("3. Jogue arquivos reais no Drive")
    else:
        logger.info("")
        logger.info("⚠️ Alguns testes falharam. Verifique os logs acima.")
        
        if not results["Supabase"]:
            logger.info("💡 Supabase: Execute init_supabase.sql no SQL Editor")
        if not results["Docker"]:
            logger.info("💡 Docker: Execute 'docker-compose up --build'")
        if not results["Drive"] or not results["Obsidian"]:
            logger.info("💡 Pastas: Verifique PATH_TO_DRIVE e PATH_TO_OBSIDIAN no .env")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
