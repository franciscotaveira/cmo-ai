"""
╔═══════════════════════════════════════════════════════════════════════════════
║ KANBAN BOARD — Jarvis-Board (v5.0 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Gerencia o Kanban de Rotina no Obsidian
║ Colunas: 📥 Backlog → 🔴 Alertas Críticos → ⚡ Hoje (Foco)
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class KanbanBoard:
    """
    Gerencia o Kanban de Rotina (Jarvis-Board) no Obsidian.
    
    Fluxo visual para gestão de tarefas e alertas:
    • 📥 Backlog: Tarefas criadas em qualquer nota do vault
    • 🔴 Alertas Críticos: Situações que exigem ação imediata do Diretor
    • ⚡ Hoje (Foco): O que realmente importa no dia
    """

    def __init__(self, obsidian_path: str):
        """
        Inicializa o Kanban Board.
        
        Args:
            obsidian_path: Caminho para o vault do Obsidian
        """
        self.obsidian_path = obsidian_path
        self.exocortex_folder = "🧠 EXOCÓRTEX"
        
        self.kanban_path = os.path.join(
            obsidian_path,
            self.exocortex_folder,
            "03 - Kanban Rotina"
        )
        self.alertas_path = os.path.join(
            obsidian_path,
            self.exocortex_folder,
            "02 - Alertas Críticos"
        )
        
        # Criar estrutura de pastas
        os.makedirs(self.kanban_path, exist_ok=True)
        os.makedirs(self.alertas_path, exist_ok=True)
        
        logger.info(f"🗓️ KanbanBoard inicializado: {self.kanban_path}")

    def generate_kanban_board(self, tasks: Optional[List[Dict]] = None, 
                              alerts: Optional[List[Dict]] = None) -> str:
        """
        Gera o Kanban Board no Obsidian com Dataview queries.
        
        Args:
            tasks: Lista de tarefas (opcional, usa Dataview se None)
            alerts: Lista de alertas (opcional, usa Dataview se None)
            
        Returns:
            Caminho para o arquivo do Kanban Board gerado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        kanban_content = f"""---
tags: [kanban, rotina, exocortex]
updated: {timestamp}
---

# 🗓️ Kanban de Rotina (Jarvis-Board)

**Atualizado em:** {timestamp}

> [!SUMMARY] Como Usar
> 1. **Backlog** → Arraste para **Hoje** o que é prioridade
> 2. **Alertas Críticos** → Resolva primeiro (🔴)
> 3. **Hoje** → Execute e marque como concluído

---

## 📥 Backlog

Tarefas que você ou a IA criaram em qualquer nota do vault.

```dataview
TABLE file.link as "Tarefa", priority as "Prioridade", created as "Criado"
FROM "🧠 EXOCÓRTEX"
WHERE contains(tags, "tarefa") AND status = "backlog"
SORT priority DESC, created ASC
```

---

## 🔴 Alertas Críticos

Situações de "Produto/Status" que exigem ação imediata do Diretor.

```dataview
TABLE file.link as "Unidade", metric as "Métrica", z_score as "Z-Score"
FROM "🧠 EXOCÓRTEX/02 - Alertas Críticos"
WHERE severity = "critical"
SORT z_score DESC
```

---

## ⚡ Hoje (Foco)

Seu espaço para arrastar o que realmente importa no dia.

```dataview
TABLE file.link as "Tarefa", priority as "Prioridade"
FROM "🧠 EXOCÓRTEX"
WHERE contains(tags, "tarefa") AND status = "hoje"
SORT priority DESC
```

---

## ✅ Concluídos (Últimos 7 dias)

```dataview
TABLE file.link as "Tarefa", completed as "Concluído"
FROM "🧠 EXOCÓRTEX"
WHERE contains(tags, "tarefa") AND status = "concluido"
AND completed >= date(now) - dur(7 days)
SORT completed DESC
```

---

*Gerado automaticamente pelo Exocórtex v5.0*
"""

        # Salvar Kanban Board
        kanban_file = os.path.join(
            self.kanban_path,
            "🌍 RESUMO_EXECUTIVO_GLOBAL.md"
        )

        with open(kanban_file, 'w', encoding='utf-8') as f:
            f.write(kanban_content)

        logger.info(f"🗓️ Kanban Board gerado: {kanban_file}")
        return kanban_file

    def add_task_to_backlog(self, task: Dict[str, Any]) -> str:
        """
        Adiciona uma tarefa ao Backlog.
        
        Args:
            task: Dicionário com dados da tarefa:
                - title: Título da tarefa
                - description: Descrição detalhada
                - priority: prioridade (high, medium, low)
                - tenant: Tenant relacionado (opcional)
                - metric: Métrica relacionada (opcional)
                - action: Ação sugerida (opcional)
                
        Returns:
            Caminho para o arquivo da tarefa criada
        """
        task_id = task.get('id', datetime.now().strftime('%Y%m%d%H%M%S'))
        priority = task.get('priority', 'medium')
        
        # Ícone de prioridade
        priority_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(priority, '⚪')

        task_content = f"""---
tags: [tarefa, backlog, exocortex]
priority: {priority}
status: backlog
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# 📋 {priority_icon} {task.get('title', 'Nova Tarefa')}

**Descrição:** {task.get('description', 'Sem descrição')}

**Unidade:** {task.get('tenant', 'N/A')}

**Métrica:** {task.get('metric', 'N/A')}

**Ação Sugerida:** {task.get('action', 'N/A')}

---

## Histórico

- **Criado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status:** 📥 Backlog

---

*Adicionado automaticamente pelo Exocórtex*
"""

        task_file = os.path.join(
            self.kanban_path,
            f"Tarefa-{task_id}.md"
        )

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task_content)

        logger.info(f"📋 Tarefa adicionada ao Backlog: {task_file}")
        return task_file

    def move_task_to_today(self, task_file: str) -> bool:
        """
        Move uma tarefa do Backlog para "Hoje (Foco)".
        
        Args:
            task_file: Caminho para o arquivo da tarefa
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Atualizar status
            content = content.replace('status: backlog', 'status: hoje')
            content = content.replace('📥 Backlog', '⚡ Hoje (Foco)')
            
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Tarefa movida para Hoje: {task_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao mover tarefa: {e}")
            return False

    def complete_task(self, task_file: str) -> bool:
        """
        Marca uma tarefa como concluída.
        
        Args:
            task_file: Caminho para o arquivo da tarefa
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Atualizar status e adicionar data de conclusão
            content = content.replace('status: hoje', 'status: concluido')
            content = content.replace('⚡ Hoje (Foco)', '✅ Concluído')
            content += f"\n- **Concluído em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Tarefa concluída: {task_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao concluir tarefa: {e}")
            return False

    def add_critical_alert(self, alert: Dict[str, Any]) -> str:
        """
        Adiciona um alerta crítico à área de Alertas.
        
        Args:
            alert: Dicionário com dados do alerta:
                - title: Título do alerta
                - tenant: Nome do tenant/unidade
                - metric: Métrica com anomalia
                - value: Valor atual
                - expected: Valor esperado
                - z_score: Z-Score da anomalia
                - action: Ação recomendada
                
        Returns:
            Caminho para o arquivo do alerta criado
        """
        alert_id = alert.get('id', datetime.now().strftime('%Y%m%d%H%M%S'))
        z_score = alert.get('z_score', 0)
        
        alert_content = f"""---
tags: [alerta, critico, exocortex]
severity: critical
z_score: {z_score:.2f}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# 🔴 ALERTA CRÍTICO: {alert.get('title', 'Anomalia Detectada')}

**Unidade:** {alert.get('tenant', 'N/A')}

**Métrica:** {alert.get('metric', 'N/A')}

---

## 📊 Dados da Anomalia

| Campo | Valor |
| :---- | :---- |
| **Valor Atual** | {alert.get('value', 'N/A')} |
| **Valor Esperado** | {alert.get('expected', 'N/A')} |
| **Z-Score** | {z_score:.2f} |
| **Severidade** | 🔴 Crítico |

---

## 🎯 Ação Recomendada

{alert.get('action', 'Ação não especificada')}

---

## 📝 Notas

*Alerta gerado automaticamente pelo Exocórtex v5.0*

"""

        alert_file = os.path.join(
            self.alertas_path,
            f"ALERTA-{alert_id}.md"
        )

        with open(alert_file, 'w', encoding='utf-8') as f:
            f.write(alert_content)

        logger.info(f"🔴 Alerta crítico adicionado: {alert_file}")
        return alert_file

    def get_backlog_count(self) -> int:
        """
        Conta o número de tarefas no Backlog.
        
        Returns:
            Número de tarefas no Backlog
        """
        count = 0
        for file in os.listdir(self.kanban_path):
            if file.startswith('Tarefa-') and file.endswith('.md'):
                try:
                    with open(os.path.join(self.kanban_path, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'status: backlog' in content:
                            count += 1
                except:
                    pass
        return count

    def get_today_count(self) -> int:
        """
        Conta o número de tarefas em "Hoje".
        
        Returns:
            Número de tarefas em Hoje
        """
        count = 0
        for file in os.listdir(self.kanban_path):
            if file.startswith('Tarefa-') and file.endswith('.md'):
                try:
                    with open(os.path.join(self.kanban_path, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'status: hoje' in content:
                            count += 1
                except:
                    pass
        return count

    def get_alerts_count(self) -> int:
        """
        Conta o número de alertas críticos.
        
        Returns:
            Número de alertas críticos
        """
        count = 0
        for file in os.listdir(self.alertas_path):
            if file.startswith('ALERTA-') and file.endswith('.md'):
                count += 1
        return count
