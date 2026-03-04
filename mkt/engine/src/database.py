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
            self.client: Client = create_client(
                self.supabase_url, self.supabase_key
            )
            logger.info("✅ Conexão com Supabase estabelecida")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar no Supabase: {e}")
            raise

    def get_tenant_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Busca um tenant pelo slug."""
        if slug in self.tenant_cache:
            return {"id": self.tenant_cache[slug], "slug": slug}

        try:
            response = self.client.table("tenants")\
                .select("id, name, slug")\
                .eq("slug", slug)\
                .execute()

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
            response = self.client.table("marketing_assets")\
                .insert(data).execute()
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
            "processed_at": (
                datetime.utcnow().isoformat()
                if status == "completed" else None
            )
        }
        if error_message:
            data["error_message"] = error_message

        try:
            self.client.table("marketing_assets")\
                .update(data).eq("id", asset_id).execute()
            logger.info(f"✅ Asset {asset_id} atualizado para: {status}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar asset: {e}")
            return False

    def insert_metric(self, tenant_id: str, metric_key: str,
                      metric_value: float,
                      date_ref: Optional[str] = None,
                      metadata: Optional[Dict] = None) -> bool:
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
                               chunk_index: int = 0,
                               metadata: Optional[Dict] = None) -> bool:
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
            response = self.client.table("strategic_insights")\
                .insert(data).execute()
            if response.data and len(response.data) > 0:
                insight_id = response.data[0]["id"]
                logger.info(f"💡 Insight registrado: {insight_id}")
                return insight_id
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao inserir insight: {e}")
            return None

    def log_audit(self, action: str, actor_type: str,
                  tenant_id: Optional[str] = None,
                  actor_id: Optional[str] = None,
                  details: Optional[Dict] = None) -> bool:
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

    def get_metrics_by_tenant(self, tenant_id: str,
                              limit: int = 100) -> List[Dict[str, Any]]:
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

    def get_critical_alerts(self, tenant_id: str = None,
                            status: str = None, limit: int = 10):
        """Busca alertas críticos (anomalias) no banco."""
        try:
            query = self.client.table("alerts").select("*")
            if tenant_id:
                query = query.eq("tenant_id", tenant_id)
            if status:
                query = query.eq("status", status)

            result = query.order("detected_at", desc=True)\
                .limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"❌ Erro ao buscar alertas críticos: {e}")
            return []

    def update_alert_status(self, alert_id: str, status: str):
        """Atualiza o status de um alerta."""
        try:
            self.client.table("alerts").update({"status": status})\
                .eq("id", alert_id).execute()
            return True
        except Exception as e:
            logger.error("❌ Erro ao atualizar alerta %s: %s", alert_id, e)
            return False

    def get_latest_metrics_summary(self, tenant_id: str) -> Dict[str, Any]:
        """
        Retorna um dicionário consolidado das métricas mais recentes do tenant.
        Busca os últimos valores para cada chave de métrica principal.
        """
        try:
            # Pegar os registros mais recentes
            # (últimos 30 dias aprox para garantir os principais)
            response = self.client.table("business_metrics")\
                .select("metric_key, metric_value, date_ref, metadata")\
                .eq("tenant_id", tenant_id)\
                .order("date_ref", desc=True)\
                .limit(100)\
                .execute()

            if not response.data:
                return {}

            summary = {}
            for row in response.data:
                key = row["metric_key"]
                if key not in summary:
                    summary[key] = {
                        "value": row["metric_value"],
                        "date": row["date_ref"],
                        "metadata": row["metadata"]
                    }
            return summary
        except Exception as e:
            logger.error("❌ Erro ao sumarizar métricas: %s", e)
            return {}

    def get_historical_metrics(self, tenant_id: str,
                               months: int = 6) -> List[Dict[str, Any]]:
        """
        Retorna agregação mensal das principais métricas (Revenue, Spend, ROAS).
        """
        try:
            # Busca dados dos últimos N meses
            response = self.client.table("business_metrics")\
                .select("metric_key, metric_value, date_ref")\
                .eq("tenant_id", tenant_id)\
                .in_("metric_key", ["revenue", "spend", "roas"])\
                .order("date_ref", desc=True)\
                .execute()

            if not response.data:
                return []

            # Lógica de agrupamento por Mês/Ano
            history = {}
            for row in response.data:
                # 2026-03-04 -> "2026-03"
                month_key = row["date_ref"][:7]
                if month_key not in history:
                    history[month_key] = {
                        "name": month_key,
                        "revenue": 0.0,
                        "spend": 0.0,
                        "roas": 0.0,
                        "cnt_roas": 0
                    }

                key = row["metric_key"]
                val = row["metric_value"]
                if key in ["revenue", "spend"]:
                    history[month_key][key] += val
                elif key == "roas":
                    history[month_key]["roas"] += val
                    history[month_key]["cnt_roas"] += 1

            # Finalizar médias de ROAS e formatar lista
            result = []
            for m in sorted(history.keys()):
                h = history[m]
                if h["cnt_roas"] > 0:
                    h["roas"] = round(h["roas"] / h["cnt_roas"], 2)
                del h["cnt_roas"]
                result.append(h)

            return result
        except Exception as e:
            logger.error(f"❌ Erro ao buscar histórico: {e}")
            return []

    def get_metric_trends(self, tenant_id: str,
                          metric_key: str) -> Dict[str, Any]:
        """
        Calcula a tendência de uma métrica comparando o período atual
        com o anterior (ex: Últimos 30 dias vs 30 dias anteriores).
        """
        try:
            # Busca os últimos 60 dias de dados para a métrica
            response = self.client.table("business_metrics")\
                .select("metric_value, date_ref")\
                .eq("tenant_id", tenant_id)\
                .eq("metric_key", metric_key)\
                .order("date_ref", desc=True)\
                .limit(60)\
                .execute()

            if not response.data or len(response.data) < 2:
                return {"trend": "0%", "isPositive": True}

            # Simplificação: últimos 30 registros vs 30 anteriores
            data = response.data
            mid = len(data) // 2
            current_period = sum(r["metric_value"] for r in data[:mid])
            prev_period = sum(r["metric_value"] for r in data[mid:])

            if prev_period == 0:
                return {"trend": "+100%", "isPositive": True}

            diff = ((current_period - prev_period) / prev_period) * 100
            trend_str = f"{'+' if diff >= 0 else ''}{round(diff, 1)}%"
            return {"trend": trend_str, "isPositive": diff >= 0}

        except Exception as e:
            logger.error(f"❌ Erro ao calcular tendências: {e}")
            return {"trend": "n/a", "isPositive": True}

    def get_metric_lineage(self, tenant_id: str,
                           metric_key: str) -> Dict[str, Any]:
        """
        Busca a linhagem (origem) do último dado de uma métrica específica.
        Tenta correlacionar a métrica com o asset (arquivo) de origem via metadados.
        """
        try:
            # 1. Pegar a última entrada da métrica
            response = self.client.table("business_metrics")\
                .select("metadata, date_ref")\
                .eq("tenant_id", tenant_id)\
                .eq("metric_key", metric_key)\
                .order("date_ref", desc=True)\
                .limit(1)\
                .execute()

            if not response.data:
                return {"source": "Desconhecido", "confidence": "baixa"}

            metric_data = response.data[0]
            metadata = metric_data.get("metadata", {})
            asset_id = metadata.get("asset_id")

            lineage = {
                "date": metric_data["date_ref"],
                "source": metadata.get("source", "Processamento Interno"),
                "confidence": metadata.get("confidence", "média")
            }
            
            # 2. Se houver asset_id, buscar detalhes do arquivo
            if asset_id:
                asset_resp = self.client.table("marketing_assets")\
                    .select("file_name, file_type, created_at")\
                    .eq("id", asset_id)\
                    .execute()
                
                if asset_resp.data:
                    asset = asset_resp.data[0]
                    lineage["file_name"] = asset["file_name"]
                    lineage["file_type"] = asset["file_type"]
                    lineage["ingested_at"] = asset["created_at"]
                    lineage["source"] = "Planilha / CSV"

            return lineage
        except Exception as e:
            logger.error("❌ Erro ao buscar linhagem: %s", e)
            return {
                "source": "Erro ao recuperar linhagem",
                "confidence": "n/a"
            }
