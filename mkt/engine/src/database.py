"""
╔═══════════════════════════════════════════════════════════════════════════════
║ DATABASE HANDLER — Conexão com Supabase
╠═══════════════════════════════════════════════════════════════════════════════
║ Gerencia todas as operações de banco de dados
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handler para operações de banco de dados no Supabase."""
    
    def __init__(self):
        """Inicializa a conexão com o Supabase."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.tenant_cache: Dict[str, str] = {}
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("❌ Credenciais do Supabase não encontradas")
            raise ValueError("SUPABASE_URL e SUPABASE_KEY são obrigatórios")
        
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info("✅ Conexão com Supabase estabelecida")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar no Supabase: {e}")
            raise
    
    def get_tenant_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Busca um tenant pelo slug."""
        if slug in self.tenant_cache:
            return {"id": self.tenant_cache[slug], "slug": slug}
        
        try:
            response = self.client.table("tenants").select("id, name, slug").eq("slug", slug).execute()
            
            if response.data and len(response.data) > 0:
                tenant = response.data[0]
                self.tenant_cache[slug] = tenant["id"]
                logger.info(f"✅ Tenant encontrado: {tenant['name']}")
                return tenant
            else:
                logger.warning(f"⚠️ Tenant não encontrado: {slug}")
                return None
        except Exception as e:
            logger.error(f"❌ Erro ao buscar tenant: {e}")
            return None
    
    def insert_asset(self, tenant_id: str, file_name: str, file_path: str, 
                     file_type: str) -> Optional[str]:
        """Registra um novo arquivo no banco."""
        data = {
            "tenant_id": tenant_id,
            "file_name": file_name,
            "file_path": file_path,
            "file_type": file_type,
            "processed": False,
            "processing_status": "pending"
        }
        
        try:
            response = self.client.table("marketing_assets").insert(data).execute()
            if response.data and len(response.data) > 0:
                asset_id = response.data[0]["id"]
                logger.info(f"✅ Asset registrado: {file_name}")
                return asset_id
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao inserir asset: {e}")
            return None
    
    def update_asset_status(self, asset_id: str, status: str, 
                           error_message: Optional[str] = None) -> bool:
        """Atualiza o status de processamento de um asset."""
        data = {
            "processed": status == "completed",
            "processing_status": status,
            "processed_at": datetime.utcnow().isoformat() if status == "completed" else None
        }
        if error_message:
            data["error_message"] = error_message
        
        try:
            self.client.table("marketing_assets").update(data).eq("id", asset_id).execute()
            logger.info(f"✅ Asset {asset_id} atualizado para: {status}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar asset: {e}")
            return False
    
    def insert_metric(self, tenant_id: str, metric_key: str, metric_value: float,
                     date_ref: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """Insere uma métrica de negócio no banco."""
        data = {
            "tenant_id": tenant_id,
            "metric_key": metric_key,
            "metric_value": float(metric_value),
            "date_ref": date_ref or datetime.utcnow().strftime("%Y-%m-%d"),
            "metadata": metadata or {}
        }
        
        try:
            self.client.table("business_metrics").insert(data).execute()
            logger.debug(f"📊 Métrica inserida: {metric_key} = {metric_value}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inserir métrica: {e}")
            return False
    
    def insert_knowledge_chunk(self, tenant_id: str, content_chunk: str,
                               chunk_index: int = 0, metadata: Optional[Dict] = None) -> bool:
        """Insere um chunk de conhecimento no banco."""
        data = {
            "tenant_id": tenant_id,
            "content_chunk": content_chunk,
            "chunk_index": chunk_index,
            "metadata": metadata or {}
        }
        
        try:
            self.client.table("knowledge_base").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inserir conhecimento: {e}")
            return False
    
    def insert_insight(self, tenant_id: str, context: str, ai_response: str,
                      status: str = "new") -> Optional[str]:
        """Insere um insight estratégico gerado pela IA."""
        data = {
            "tenant_id": tenant_id,
            "context": context,
            "ai_response": ai_response,
            "status": status
        }
        
        try:
            response = self.client.table("strategic_insights").insert(data).execute()
            if response.data and len(response.data) > 0:
                insight_id = response.data[0]["id"]
                logger.info(f"💡 Insight registrado: {insight_id}")
                return insight_id
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao inserir insight: {e}")
            return None
    
    def log_audit(self, action: str, actor_type: str, tenant_id: Optional[str] = None,
                 actor_id: Optional[str] = None, details: Optional[Dict] = None) -> bool:
        """Registra uma ação no log de auditoria."""
        data = {
            "tenant_id": tenant_id,
            "action": action,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "details": details or {}
        }
        
        try:
            self.client.table("audit_logs").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao registrar audit log: {e}")
            return False
    
    def get_metrics_by_tenant(self, tenant_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Busca métricas de um tenant."""
        try:
            response = self.client.table("business_metrics")\
                .select("*")\
                .eq("tenant_id", tenant_id)\
                .order("date_ref", desc=True)\
                .limit(limit)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"❌ Erro ao buscar métricas: {e}")
            return []
    
    def health_check(self) -> bool:
        """Verifica se a conexão com o Supabase está saudável."""
        try:
            self.client.table("tenants").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"❌ Health check falhou: {e}")
            return False
    
    def clear_tenant_cache(self):
        """Limpa o cache de tenants."""
        self.tenant_cache.clear()
        logger.info("🗑️ Cache de tenants limpo")
