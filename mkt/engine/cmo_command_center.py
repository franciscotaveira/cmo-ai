import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Adicionar o diretório pai ao path para importar as engines
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database_handler import DatabaseHandler
from src.ai_insights import AIInsightsEngine, LLMProvider
from src.executive_dashboard import ExecutiveDashboard

class CMOCommandCenter:
    """
    Painel CLI Interativo para o CMO 360°.
    Permite visualizar dashboards, alertas e insights de forma rápida.
    """
    
    def __init__(self):
        self.db = DatabaseHandler()
        self.ai = self._init_ai()
        self.dashboard = ExecutiveDashboard()
        self.current_tenant = "Diretoria Geral" # Default
        
    def _init_ai(self) -> AIInsightsEngine:
        provider_name = os.getenv("LLM_PROVIDER", "openrouter").lower()
        provider = getattr(LLMProvider, provider_name.upper(), LLMProvider.OPENROUTER)
        return AIInsightsEngine(llm_provider=provider)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("╔" + "═" * 60 + "╗")
        print("║" + " " * 18 + "🎯 CMO 360° — COMMAND CENTER" + " " * 14 + "║")
        print("╠" + "═" * 60 + "╣")
        print(f"║  Status: 🟢 Online {' ' * 38}║")
        print(f"║  Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}{' ' * 35}║")
        print(f"║  Tenant: {self.current_tenant[:30]:<30} {' ' * 13}║")
        print("╚" + "═" * 60 + "╝")

    def show_menu(self):
        print("\nMENU PRINCIPAL:")
        print("  [1] 📊 Ver Dashboard Geral")
        print("  [2] 🚨 Ver Alertas Críticos")
        print("  [3] 🤖 Ver Insights da IA (Smart Routing)")
        print("  [4] 📈 Ver Performance por Canal")
        print("  [5] 💰 Ver Budget & ROI")
        print("  [6] 🏛️ Ver Brand Health")
        print("  [7] 🔄 Trocar Tenant")
        print("  [8] 📋 Gerar Relatório Executivo")
        print("  [9] 🔄 Atualizar Dados")
        print("  [0] Sair")
        print("\n" + "─" * 62)

    def run(self):
        while True:
            self.clear_screen()
            self.print_header()
            self.show_menu()
            
            choice = input("Sua escolha: ")
            
            if choice == '1':
                self.view_dashboard()
            elif choice == '2':
                self.view_alerts()
            elif choice == '3':
                self.view_ai_insights()
            elif choice == '7':
                self.switch_tenant()
            elif choice == '0':
                print("\nEncerrando Command Center... 👋")
                break
            else:
                input("\n⚠️ Opção em desenvolvimento ou inválida. Pressione Enter para voltar.")

    def view_dashboard(self):
        self.clear_screen()
        print("\n📊 DASHBOARD GERAL - " + self.current_tenant)
        print("─" * 62)
        # Simulação de dados reais do Supabase
        print(f"Receita Total: R$ 145.200,00 ⬆️ 12%")
        print(f"Investimento:  R$ 12.400,00  ⬇️ 5%")
        print(f"ROAS Geral:    11.7x          ⬆️ 18%")
        print(f"CAC Médio:     R$ 42,50       ⬇️ 8%")
        print("\nPróximo passo: Validar dados do Supabase...")
        input("\nPressione Enter para voltar ao menu.")

    def view_alerts(self):
        self.clear_screen()
        print("\n🚨 ALERTAS CRÍTICOS")
        print("─" * 62)
        print("🔴 [CRÍTICO] Google Ads - ROAS abaixo de 2.0x em Campanha 'Black Friday'")
        print("🟡 [ATENÇÃO] Meta Ads - Frequência > 4.5 em Criativo 'Video_Promo_01'")
        print("🟢 [INFO] Meta Ads - Novo recorde de CPL atingido: R$ 1,20")
        input("\nPressione Enter para voltar ao menu.")

    def view_ai_insights(self):
        self.clear_screen()
        print("\n🤖 INSIGHTS DA IA (Smart Routing)")
        print("─" * 62)
        print("Modelo Suporte: google/gemini-flash-1.5 (Ativo)")
        print("Modelo Primary: openai/gpt-4-turbo (Standby)")
        print("\nÚltimo Insight:")
        print("> 'Identificamos uma oportunidade de realocação de 15% do budget ")
        print("   do canal Display para Search, dado o aumento de intenção de compra.'")
        input("\nPressione Enter para voltar ao menu.")

    def switch_tenant(self):
        print("\nTenants disponíveis:")
        print("1. Diretoria Geral")
        print("2. Salão Lux Beauty")
        print("3. Franquia Chapecó")
        new_choice = input("\nEscolha o número do tenant: ")
        if new_choice == '1': self.current_tenant = "Diretoria Geral"
        elif new_choice == '2': self.current_tenant = "Salão Lux Beauty"
        elif new_choice == '3': self.current_tenant = "Franquia Chapecó"
        
if __name__ == "__main__":
    app = CMOCommandCenter()
    app.run()
