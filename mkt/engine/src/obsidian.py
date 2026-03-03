"""
╔═══════════════════════════════════════════════════════════════════════════════
║ OBSIDIAN BRIDGE — Integração com Obsidian (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Escreve notas e dashboards no vault do Obsidian
║ v5.0: Todo o sistema encapsulado em 🧠 EXOCÓRTEX
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .database import DatabaseHandler

logger = logging.getLogger(__name__)


class ObsidianBridge:
    """
    Ponte de integração com o Obsidian — v5.0 EXOCÓRTEX.

    Todo o sistema é encapsulado na pasta 🧠 EXOCÓRTEX,
    mantendo o vault do usuário limpo e organizado.
    """

    def __init__(self, obsidian_path: str, db: Optional[DatabaseHandler] = None):
        self.obsidian_path = obsidian_path
        self.db = db or DatabaseHandler()

        # v5.0: Prefixo universal para encapsulamento
        self.exocortex_folder = "🧠 EXOCÓRTEX"

        # Estrutura de pastas v5.0 — tudo encapsulado
        self.folder_structure = {
            'dashboards': f"{self.exocortex_folder}/00 - Dashboards",
            'unidades': f"{self.exocortex_folder}/01 - Unidades",
            'alertas': f"{self.exocortex_folder}/02 - Alertas Críticos",
            'kanban': f"{self.exocortex_folder}/03 - Kanban Rotina",
            'arquivos': f"{self.exocortex_folder}/99 - Arquivos",
        }

        # Criar estrutura de pastas ao inicializar
        self._create_folder_structure()

        logger.info(f"🧠 Exocórtex v5.0 inicializado: {self.exocortex_folder}")

    def _create_folder_structure(self):
        """Cria a estrutura de pastas encapsulada do Exocórtex."""
        for folder_name, folder_path in self.folder_structure.items():
            full_path = os.path.join(self.obsidian_path, folder_path)
            os.makedirs(full_path, exist_ok=True)
        logger.info(f"✅ Estrutura de pastas criada: {self.exocortex_folder}")

    def write_dashboard_note(self, tenant_slug: str, tenant_name: str,
                            metrics: List[Dict[str, Any]],
                            insights: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Escreve uma nota de dashboard para um tenant.
        v5.0: Salvo dentro de 🧠 EXOCÓRTEX/01 - Unidades/
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        content = f"""---
tags: [dashboard, {tenant_slug}, exocortex]
atualizado: {timestamp}
---

# 📊 Dashboard: {tenant_name}

**Última atualização:** {timestamp}

---

## 📈 Métricas Principais

"""

        # Agrupar métricas por tipo
        metrics_by_type = self._group_metrics_by_type(metrics)

        for metric_type, values in metrics_by_type.items():
            content += f"### {metric_type.replace('_', ' ').title()}\n\n"
            content += "| Métrica | Valor | Data |\n"
            content += "| :------ | :---- | :--- |\n"

            for metric in values[:10]:
                value = metric.get('metric_value', 0)
                date_ref = metric.get('date_ref', 'N/A')
                key = metric.get('metric_key', 'unknown')

                value_str = f"{value:,.2f}" if isinstance(value, float) else str(value)
                content += f"| {key.replace('_', ' ').title()} | {value_str} | {date_ref} |\n"

            content += "\n"

        if insights and len(insights) > 0:
            content += """---

## 🧠 Insights da IA

"""
            for insight in insights[:5]:
                content += f"### {insight.get('context', 'Insight')[:100]}...\n\n"
                content += f"> {insight.get('ai_response', '')}\n\n"

        content += f"\n---\n\n*Nota gerada automaticamente pelo Exocórtex v5.0*\n"

        # v5.0: Salvar dentro da estrutura encapsulada
        tenant_path = os.path.join(
            self.obsidian_path,
            self.folder_structure['unidades'],
            tenant_slug
        )
        os.makedirs(tenant_path, exist_ok=True)

        filename = "Dashboard.md"
        filepath = os.path.join(tenant_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📝 Dashboard escrito em: {filepath}")
        return filepath
    
    def write_strategy_note(self, tenant_slug: str, strategy_title: str,
                           strategy_content: str, context: Optional[str] = None) -> str:
        """
        Escreve uma nota de estratégia.
        v5.0: Salvo dentro de 🧠 EXOCÓRTEX/99 - Arquivos/
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        content = f"""---
tags: [{tenant_slug}, estrategia, exocortex]
criado: {timestamp}
---

# 🎯 {strategy_title}

**Criado em:** {timestamp}

"""

        if context:
            content += f"""
## Contexto

{context}

---

"""

        content += f"""
## Estratégia

{strategy_content}

---

## Plano de Ação

- [ ] Revisar estratégia
- [ ] Definir responsáveis
- [ ] Estabelecer prazos
- [ ] Executar
- [ ] Medir resultados

---

*Estratégia gerada pelo Exocórtex v5.0*
"""

        # v5.0: Salvar dentro da estrutura encapsulada
        strategies_path = os.path.join(
            self.obsidian_path,
            self.folder_structure['arquivos'],
            'Estrategias'
        )
        os.makedirs(strategies_path, exist_ok=True)

        safe_title = strategy_title[:50].replace(' ', '_').replace('/', '_')
        filename = f"{safe_title}_{tenant_slug}.md"
        filepath = os.path.join(strategies_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📝 Estratégia escrita: {filepath}")
        return filepath

    def update_summary_note(self, summary_data: Dict[str, Any]) -> str:
        """
        Atualiza a nota de resumo geral.
        v5.0: Salvo em 🧠 EXOCÓRTEX/00 - Dashboards/
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        content = f"""---
tags: [resumo, diretoria, visao-geral, exocortex]
atualizado: {timestamp}
---

# 📊 Resumo Geral do Ecossistema

**Atualizado em:** {timestamp}

---

## 🏢 Empresas Monitoradas

| Empresa | Tipo | Métricas | Últ. Atualização |
| :------ | :--- | :------- | :--------------- |
"""
        
        tenants = summary_data.get('tenants', [])
        for tenant in tenants:
            name = tenant.get('name', 'N/A')
            type_ = tenant.get('type', 'N/A')
            metrics_count = tenant.get('metrics_count', 0)
            last_update = tenant.get('last_update', 'N/A')
            
            content += f"| {name} | {type_} | {metrics_count} | {last_update} |\n"
        
        content += f"\n---\n\n*Resumo gerado automaticamente pelo Exocórtex v5.0*\n"

        # v5.0: Salvar dentro da estrutura encapsulada
        filepath = os.path.join(
            self.obsidian_path,
            self.folder_structure['dashboards'],
            '🌍 RESUMO_GERAL.md'
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📝 Resumo geral atualizado: {filepath}")
        return filepath
    
    def _group_metrics_by_type(self, metrics: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Agrupa métricas por tipo."""
        grouped = {}
        
        for metric in metrics:
            key = metric.get('metric_key', 'unknown')
            metric_type = key.rsplit('_', 1)[-1] if '_' in key else key
            
            if metric_type not in grouped:
                grouped[metric_type] = []
            
            grouped[metric_type].append(metric)
        
        return grouped
    
    def delete_note(self, filename: str) -> bool:
        """Deleta uma nota do Obsidian."""
        try:
            filepath = os.path.join(self.obsidian_path, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"🗑️ Nota deletada: {filepath}")
                return True
            else:
                logger.warning(f"⚠️ Arquivo não encontrado: {filepath}")
                return False
        except Exception as e:
            logger.error(f"❌ Erro ao deletar nota: {e}")
            return False
    
    def get_all_notes(self) -> List[str]:
        """Lista todas as notas do vault."""
        notes = []
        
        for root, dirs, files in os.walk(self.obsidian_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.md') or file.endswith('.canvas'):
                    notes.append(os.path.relpath(
                        os.path.join(root, file),
                        self.obsidian_path
                    ))
        
        return notes
