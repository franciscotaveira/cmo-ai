"""
╔═══════════════════════════════════════════════════════════════════════════════
║ FILE PROCESSOR — Processamento de Arquivos
╠═══════════════════════════════════════════════════════════════════════════════
║ Processa CSV, PDF, XLSX e extrai métricas
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import pandas as pd

from .database import DatabaseHandler

logger = logging.getLogger(__name__)


class FileProcessor:
    """Processador de arquivos para extração de dados."""
    
    def __init__(self, db: DatabaseHandler):
        self.db = db
        
        # Mapeamento de palavras-chave para tipos de métrica
        self.keyword_mappings = {
            'lead': 'leads', 'leads': 'leads', 'contato': 'leads',
            'venda': 'vendas', 'vendas': 'vendas', 'faturamento': 'faturamento',
            'receita': 'faturamento', 'ticket': 'ticket_medio',
            'custo': 'custo', 'investimento': 'custo', 'gasto': 'custo',
            'clique': 'cliques', 'impressão': 'impressoes', 'alcance': 'alcance',
            'conversão': 'taxa_conversao', 'roi': 'roi', 'roas': 'roas',
            'cac': 'cac', 'ltv': 'ltv', 'churn': 'churn',
            'retenção': 'retencao', 'cancelamento': 'churn'
        }
    
    def process_file(self, filepath: str, tenant_slug: str) -> Dict[str, Any]:
        """Processa um arquivo completo."""
        filename = os.path.basename(filepath)
        file_ext = Path(filepath).suffix.lower().lstrip('.')
        
        logger.info(f"⚙️ Processando: {filename} (tenant: {tenant_slug})")
        
        # Buscar tenant
        tenant = self.db.get_tenant_by_slug(tenant_slug)
        if not tenant:
            logger.error(f"❌ Tenant não encontrado: {tenant_slug}")
            return {"success": False, "error": f"Tenant não encontrado: {tenant_slug}"}
        
        tenant_id = tenant["id"]
        
        # Registrar asset
        asset_id = self.db.insert_asset(tenant_id, filename, filepath, file_ext)
        
        if asset_id:
            self.db.update_asset_status(asset_id, "processing")
        
        result = {
            "success": False, "asset_id": asset_id, "tenant_id": tenant_id,
            "filename": filename, "metrics_count": 0, "knowledge_chunks": 0, "error": None
        }
        
        try:
            if file_ext == 'csv':
                result = self._process_csv(filepath, tenant_id, asset_id, result)
            elif file_ext in ['xlsx', 'xls']:
                result = self._process_excel(filepath, tenant_id, asset_id, result)
            elif file_ext == 'pdf':
                result = self._process_pdf(filepath, tenant_id, asset_id, result)
            elif file_ext == 'txt':
                result = self._process_txt(filepath, tenant_id, asset_id, result)
            else:
                result["error"] = f"Tipo de arquivo não suportado: {file_ext}"
            
            # Atualizar status final
            if asset_id:
                status = "completed" if result["success"] else "error"
                self.db.update_asset_status(asset_id, status, result.get("error"))
            
            # Log de auditoria
            self.db.log_audit(
                action=f"file_processed_{file_ext}",
                actor_type="engine",
                actor_id="marketing_engine",
                tenant_id=tenant_id,
                details={"asset_id": asset_id, "filename": filename, "success": result["success"]}
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar arquivo: {e}", exc_info=True)
            result["error"] = str(e)
            if asset_id:
                self.db.update_asset_status(asset_id, "error", str(e))
        
        return result
    
    def _process_csv(self, filepath: str, tenant_id: str, asset_id: Optional[str],
                    result: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um arquivo CSV."""
        try:
            # Detectar encoding
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    logger.info(f"📖 Encoding detectado: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Não foi possível detectar o encoding do CSV")
            
            logger.info(f"📊 CSV carregado: {len(df)} linhas, {len(df.columns)} colunas")
            
            # Extrair métricas
            metrics = self._extract_metrics_from_dataframe(df, tenant_id, asset_id)
            result["metrics_count"] = len(metrics)
            result["success"] = len(metrics) > 0
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar CSV: {e}")
            result["error"] = str(e)
            return result
    
    def _process_excel(self, filepath: str, tenant_id: str, asset_id: Optional[str],
                      result: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um arquivo Excel."""
        try:
            excel_file = pd.ExcelFile(filepath)
            total_metrics = 0
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                logger.info(f"📊 Aba '{sheet_name}': {len(df)} linhas")
                
                metrics = self._extract_metrics_from_dataframe(df, tenant_id, asset_id)
                total_metrics += len(metrics)
            
            result["metrics_count"] = total_metrics
            result["success"] = total_metrics > 0
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Excel: {e}")
            result["error"] = str(e)
            return result
    
    def _process_pdf(self, filepath: str, tenant_id: str, asset_id: Optional[str],
                    result: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um arquivo PDF."""
        try:
            try:
                from pypdf import PdfReader
            except ImportError:
                result["error"] = "pypdf não instalado"
                return result
            
            reader = PdfReader(filepath)
            full_text = ""
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_text += f"\n[Página {i+1}]\n{text}"
            
            logger.info(f"📄 PDF processado: {len(reader.pages)} páginas")
            
            # Dividir em chunks
            chunks = self._split_text_into_chunks(full_text, chunk_size=1000)
            
            # Inserir chunks
            for i, chunk in enumerate(chunks):
                self.db.insert_knowledge_chunk(
                    tenant_id=tenant_id,
                    content_chunk=chunk,
                    chunk_index=i,
                    asset_id=asset_id,
                    metadata={"source_file": os.path.basename(filepath)}
                )
            
            result["knowledge_chunks"] = len(chunks)
            result["success"] = len(chunks) > 0
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar PDF: {e}")
            result["error"] = str(e)
            return result
    
    def _process_txt(self, filepath: str, tenant_id: str, asset_id: Optional[str],
                    result: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um arquivo de texto."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"📄 TXT processado: {len(content)} caracteres")
            
            chunks = self._split_text_into_chunks(content, chunk_size=1000)
            
            for i, chunk in enumerate(chunks):
                self.db.insert_knowledge_chunk(
                    tenant_id=tenant_id,
                    content_chunk=chunk,
                    chunk_index=i,
                    asset_id=asset_id
                )
            
            result["knowledge_chunks"] = len(chunks)
            result["success"] = len(chunks) > 0
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar TXT: {e}")
            result["error"] = str(e)
            return result
    
    def _extract_metrics_from_dataframe(self, df: pd.DataFrame, tenant_id: str,
                                       asset_id: Optional[str]) -> List[Dict[str, Any]]:
        """Extrai métricas de um DataFrame."""
        metrics = []
        
        # Normalizar nomes de colunas
        df.columns = [str(col).lower().strip() for col in df.columns]
        
        # Identificar coluna de data
        date_col = self._find_date_column(df)
        
        # Processar cada coluna
        for col in df.columns:
            if date_col and col == date_col:
                continue
            
            metric_type = self._identify_metric_type(col)
            
            if metric_type:
                numeric_values = pd.to_numeric(df[col], errors='coerce')
                total = numeric_values.sum()
                
                if pd.notna(total) and total != 0:
                    if date_col and date_col in df.columns:
                        # Agrupar por data
                        grouped = df.groupby(date_col)[col].sum()
                        for date_ref, value in grouped.items():
                            try:
                                date_str = pd.Timestamp(date_ref).strftime('%Y-%m-%d')
                            except:
                                date_str = datetime.utcnow().strftime('%Y-%m-%d')
                            
                            if pd.notna(value) and value != 0:
                                metrics.append({
                                    "metric_key": f"{metric_type}_total",
                                    "metric_value": float(value),
                                    "date_ref": date_str,
                                    "asset_id": asset_id
                                })
                    else:
                        metrics.append({
                            "metric_key": f"{metric_type}_total",
                            "metric_value": float(total),
                            "asset_id": asset_id
                        })
                    
                    logger.info(f"✅ Métrica extraída: {metric_type}_total = {total}")
        
        # Inserir métricas no banco
        for metric in metrics:
            self.db.insert_metric(tenant_id, **metric)
        
        return metrics
    
    def _identify_metric_type(self, column_name: str) -> Optional[str]:
        """Identifica o tipo de métrica baseado no nome da coluna."""
        column_lower = column_name.lower()
        
        for keyword, metric_type in self.keyword_mappings.items():
            if keyword in column_lower:
                return metric_type
        
        return None
    
    def _find_date_column(self, df: pd.DataFrame) -> Optional[str]:
        """Encontra a coluna de data no DataFrame."""
        for col in df.columns:
            if any(k in col.lower() for k in ['data', 'date', 'dia', 'periodo']):
                return col
            
            try:
                pd.to_datetime(df[col].head(10))
                return col
            except:
                continue
        
        return None
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000,
                               overlap: int = 200) -> List[str]:
        """Divide um texto em chunks sobrepostos."""
        if not text or len(text) == 0:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk = text[start:end].strip()
            
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
