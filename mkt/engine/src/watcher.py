"""
╔═══════════════════════════════════════════════════════════════════════════════
║ DRIVE WATCHER — Monitoramento de Arquivos
╠═══════════════════════════════════════════════════════════════════════════════
║ Monitora pastas do Drive em tempo real usando watchdog
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import time
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent

from .database import DatabaseHandler
from .processor import FileProcessor

logger = logging.getLogger(__name__)


class DriveWatcher(FileSystemEventHandler):
    """Handler para monitoramento de arquivos no Drive."""
    
    def __init__(self, drive_path: str, obsidian_path: Optional[str] = None,
                 db: Optional[DatabaseHandler] = None,
                 on_file_processed: Optional[Callable[[Dict[str, Any]], None]] = None):
        super().__init__()
        
        self.drive_path = drive_path
        self.obsidian_path = obsidian_path
        self.db = db or DatabaseHandler()
        self.processor = FileProcessor(self.db)
        self.processed_files: set = set()
        self.on_file_processed = on_file_processed
        
        # Mapeamento de pastas para tenants
        self.folder_tenant_mapping = self._load_folder_mapping()
        
        logger.info(f"👀 DriveWatcher inicializado para: {drive_path}")
    
    def _load_folder_mapping(self) -> Dict[str, str]:
        """Carrega o mapeamento de pastas para tenants."""
        mapping = {
            'salao': 'salao-esposa', 'salão': 'salao-esposa', 'beleza': 'salao-esposa',
            'franquia': 'franquia-chapeco', 'franquias': 'franquia-chapeco',
            'unidade': 'franquia-chapeco', 'loja': 'franquia-chapeco',
            'diretoria': 'diretoria', 'geral': 'diretoria', 'hq': 'diretoria'
        }
        
        # Tentar carregar mapeamento personalizado
        mapping_file = os.path.join(self.drive_path, '.folder_mapping.json')
        
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    custom_mapping = json.load(f)
                    mapping.update(custom_mapping)
                    logger.info(f"📦 Mapeamento personalizado carregado")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar mapeamento personalizado: {e}")
        
        return mapping
    
    def on_created(self, event):
        """Chamado quando um arquivo é criado."""
        if event.is_directory:
            return
        
        filepath = event.src_path
        logger.info(f"⚡ Arquivo criado detectado: {filepath}")
        
        self._process_file(filepath)
    
    def on_modified(self, event):
        """Chamado quando um arquivo é modificado."""
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        # Ignorar arquivos temporários
        if self._should_ignore(filepath):
            return
        
        logger.info(f"📝 Arquivo modificado detectado: {filepath}")
        
        # Pequeno delay para garantir que o arquivo foi totalmente salvo
        time.sleep(0.5)
        
        self._process_file(filepath)
    
    def _should_ignore(self, filepath: str) -> bool:
        """Verifica se o arquivo deve ser ignorado."""
        filename = os.path.basename(filepath).lower()
        
        ignore_patterns = [
            '~$', '.tmp', '.temp', 'desktop.ini', '.ds_store',
            '.gitignore', '.folder_mapping.json', '.md', '.canvas'
        ]
        
        for pattern in ignore_patterns:
            if pattern in filename:
                return True
        
        return False
    
    def _process_file(self, filepath: str):
        """Processa um arquivo detectado."""
        # Verificar se já foi processado recentemente
        if filepath in self.processed_files:
            logger.debug(f"⏭️ Arquivo já processado: {filepath}")
            return
        
        # Ignorar arquivos temporários
        if self._should_ignore(filepath):
            return
        
        # Verificar se arquivo existe e tem tamanho > 0
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            logger.warning(f"⚠️ Arquivo não encontrado ou vazio: {filepath}")
            return
        
        # Aguardar arquivo estar completamente disponível
        time.sleep(1)
        
        # Identificar tenant
        tenant_slug = self._detect_tenant(filepath)
        
        if not tenant_slug:
            logger.warning(f"⚠️ Não foi possível identificar tenant para: {filepath}")
            tenant_slug = 'diretoria'  # Default
        
        logger.info(f"🏢 Tenant identificado: {tenant_slug}")
        
        # Processar arquivo
        result = self.processor.process_file(filepath, tenant_slug)
        
        # Marcar como processado
        self.processed_files.add(filepath)
        
        # Callback se definido
        if self.on_file_processed:
            self.on_file_processed(result)
        
        # Escrever no Obsidian se path configurado
        if self.obsidian_path and result.get("success"):
            self._write_obsidian_update(tenant_slug, result)
    
    def _detect_tenant(self, filepath: str) -> Optional[str]:
        """Detecta o tenant baseado no caminho do arquivo."""
        filepath_normalized = filepath.replace('\\', '/').lower()
        drive_path_normalized = self.drive_path.replace('\\', '/').lower()
        
        relative_path = filepath_normalized.replace(drive_path_normalized, '').lstrip('/')
        path_parts = relative_path.split('/')
        
        for part in path_parts:
            if part in self.folder_tenant_mapping:
                return self.folder_tenant_mapping[part]
            
            for folder_keyword, tenant_slug in self.folder_tenant_mapping.items():
                if folder_keyword in part:
                    return tenant_slug
        
        logger.warning(f"⚠️ Tenant não identificado, usando padrão 'diretoria'")
        return 'diretoria'
    
    def _write_obsidian_update(self, tenant_slug: str, result: Dict[str, Any]):
        """Escreve atualização no Obsidian."""
        if not self.obsidian_path:
            return
        
        try:
            from datetime import datetime
            
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            content = f"""# 📊 Atualização Automática: {tenant_slug}

**Data/Hora:** {timestamp}

## Resumo do Processamento

| Campo | Valor |
| :--- | :--- |
| **Arquivo** | `{result.get('filename', 'N/A')}` |
| **Status** | {'✅ Sucesso' if result.get('success') else '❌ Erro'} |
| **Métricas Extraídas** | {result.get('metrics_count', 0)} |
| **Chunks de Conhecimento** | {result.get('knowledge_chunks', 0)} |

---
*Gerado automaticamente pelo Marketing Engine v4.0*
"""
            
            filename = f"DASHBOARD_AUTO_{tenant_slug.replace('-', '_')}.md"
            filepath = os.path.join(self.obsidian_path, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"📝 Nota Obsidian atualizada: {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao escrever no Obsidian: {e}")
    
    def clear_processed_cache(self):
        """Limpa o cache de arquivos processados."""
        self.processed_files.clear()
        logger.info("🗑️ Cache de arquivos processados limpo")


class WatcherManager:
    """Gerenciador do watcher."""
    
    def __init__(self, drive_path: str, obsidian_path: Optional[str] = None,
                 db: Optional[DatabaseHandler] = None,
                 on_file_processed: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.drive_path = drive_path
        self.obsidian_path = obsidian_path
        self.db = db or DatabaseHandler()
        self.on_file_processed = on_file_processed
        
        self.observer: Optional[Observer] = None
        self.watcher: Optional[DriveWatcher] = None
    
    def start(self, recursive: bool = True):
        """Inicia o watcher."""
        self.watcher = DriveWatcher(
            drive_path=self.drive_path,
            obsidian_path=self.obsidian_path,
            db=self.db,
            on_file_processed=self.on_file_processed
        )
        
        self.observer = Observer()
        self.observer.schedule(
            self.watcher,
            path=self.drive_path,
            recursive=recursive
        )
        
        self.observer.start()
        logger.info(f"🚀 Watcher iniciado para: {self.drive_path}")
    
    def stop(self):
        """Para o watcher."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("🛑 Watcher parado")
    
    def run_forever(self):
        """Inicia o watcher e roda indefinidamente."""
        self.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⌨️ Interrupt recebido, parando watcher...")
            self.stop()
