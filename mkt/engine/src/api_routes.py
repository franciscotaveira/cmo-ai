import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import (
    APIRouter, Header, HTTPException, Depends, Request
)
from pydantic import BaseModel

from src.database import DatabaseHandler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


# Dependência do BD
def get_db():
    try:
        return DatabaseHandler()
    except Exception as e:
        logger.error(
            f"O banco de dados não pôde ser inicializado para a API: {e}"
        )
        raise HTTPException(
            status_code=500, detail="Erro interno do banco de dados"
        )


# Modelos Pydantic
class MetricPayload(BaseModel):
    tenant_slug: str
    metrics: Dict[str, float]
    date_ref: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def verify_api_key(x_api_key: str = Header(None)):
    expected = os.getenv("API_SECRET_KEY", "cmo-360-secret")
    if not x_api_key or x_api_key != expected:
        logger.warning("Tentativa de acesso à API com token inválido.")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


@router.post("/metrics/ingest")
def ingest_metrics(
    payload: MetricPayload,
    db: DatabaseHandler = Depends(get_db),
    _api_key: str = Depends(verify_api_key)
):
    """Recebe métricas via API diretamente."""
    tenant = db.get_tenant_by_slug(payload.tenant_slug)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")

    tenant_id = tenant['id']
    inserted = 0

    # Data de referência formatada
    date_ref = payload.date_ref or datetime.utcnow().strftime("%Y-%m-%d")

    logger.info(
        f"📥 Recebendo métricas para {tenant['name']} via API."
    )

    for key, val in payload.metrics.items():
        success = db.insert_metric(
            tenant_id=tenant_id,
            metric_key=key,
            metric_value=val,
            date_ref=date_ref,
            metadata=payload.metadata
        )
        if success:
            inserted += 1

    # Registrar evento de ingestão (audit)
    db.log_audit(
        action="api_ingestion",
        actor_type="api_client",
        tenant_id=tenant_id,
        details={"metrics_count": inserted, "source": "direct_api"}
    )

    return {
        "status": "success",
        "message": f"{inserted} métricas processadas.",
        "tenant": tenant['name']
    }


@router.post("/webhooks/incoming/{source}")
async def receive_webhook(
    source: str, request: Request, db: DatabaseHandler = Depends(get_db)
):
    """
    Recebe eventos de webhooks externos (ex: Meta, Google, n8n, Make).
    Não exige API Key estrita para facilitar integrações de terceiros.
    """
    try:
        payload = await request.json()
    except Exception:
        body = await request.body()
        payload = {"raw_body": body.decode('utf-8', errors='ignore')}

    logger.info(f"🔔 Webhook recebido da fonte: {source}")

    tenant_slug = request.query_params.get("tenant", "default")
    tenant = db.get_tenant_by_slug(tenant_slug)

    tenant_id = tenant['id'] if tenant else None

    # Inserir na fila de automação para processamento assíncrono
    try:
        data = {
            "tenant_id": tenant_id,
            "automation_type": f"webhook_{source}",
            "status": "pending",
            "trigger_source": f"webhook:{source}",
            "payload": payload
        }
        db.client.table("automation_queue").insert(data).execute()

        if tenant_id:
            db.log_audit(
                action="webhook_received",
                actor_type="webhook",
                tenant_id=tenant_id,
                details={"source": source}
            )

    except Exception as e:
        logger.error(f"❌ Erro ao enfileirar webhook: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao registrar webhook na fila"
        ) from e

    return {
        "status": "queued",
        "message": f"Evento de {source} enfileirado."
    }


@router.get("/dashboard/executive/{tenant_slug}")
def get_executive_dashboard(
    tenant_slug: str, db: DatabaseHandler = Depends(get_db)
):
    """
    Retorna os KPIs consolidados e dados históricos para o Painel Executivo.
    Implementa a Camada Semântica v7.0 com auditabilidade (Lineage).
    """
    tenant = db.get_tenant_by_slug(tenant_slug)
    is_demo = False

    if not tenant:
        logger.warning(
            "Tenant '%s' não encontrado. Ativando modo Demo.", tenant_slug
        )
        tenant = {
            "id": "mock-id-000",
            "name": "Agência Beta (Modo Demo)",
            "slug": tenant_slug
        }
        is_demo = True

    # 1. Buscar métricas reais sumarizadas
    metrics_summary = db.get_latest_metrics_summary(tenant['id'])

    # 2. Buscar tendências calculadas
    trends = {
        "revenue": db.get_metric_trends(tenant['id'], "revenue"),
        "roas": db.get_metric_trends(tenant['id'], "roas"),
        "cac": db.get_metric_trends(tenant['id'], "cac"),
        "spend": db.get_metric_trends(tenant['id'], "spend")
    }

    # 3. Extrair valores com fallback seguro
    def get_val(key, default):
        return metrics_summary.get(key, {}).get("value", default)

    roas = get_val("roas", 3.37 if is_demo else 0.0)
    revenue = get_val("revenue", 14490.0 if is_demo else 0.0)
    spend = get_val("spend", 4300.0 if is_demo else 0.0)
    cac = get_val("cac", 142.0 if is_demo else 0.0)

    # 4. Buscar linhagem para transparência (auditabilidade)
    lineage_info = {
        "revenue": db.get_metric_lineage(tenant['id'], "revenue"),
        "roas": db.get_metric_lineage(tenant['id'], "roas"),
        "cac": db.get_metric_lineage(tenant['id'], "cac")
    }

    # 5. Buscar histórico real para charts
    real_charts = db.get_historical_metrics(tenant['id'], months=6)

    # Fallback para demo se não houver histórico
    if not real_charts and is_demo:
        real_charts = [
            {"name": "Jan", "revenue": 4000, "spend": 2400, "roas": 1.6},
            {"name": "Fev", "revenue": 3000, "spend": 1398, "roas": 2.1},
            {"name": "Mar", "revenue": 5000, "spend": 9800, "roas": 0.5},
            {"name": "Abr", "revenue": 8780, "spend": 3908, "roas": 2.2},
            {"name": "Mai", "revenue": 11000, "spend": 4800, "roas": 2.4},
            {"name": "Jun", "revenue": 15000, "spend": 3800, "roas": 3.8},
        ]
    # Inserir o mês atual (dinâmico) no final do histórico
    real_charts.append(
        {"name": "Atual", "revenue": revenue, "spend": spend, "roas": roas}
    )

    # 6. Buscar alertas reais
    real_alerts = db.get_critical_alerts(tenant['id'], limit=5)
    anomalies = []
    for a in real_alerts:
        anomalies.append({
            "title": f"Alerta: {a.get('metric_key')}",
            "message": (
                f"Desvio detectado: {a.get('metric_value')}. "
                f"Severidade: {a.get('severity')}"
            ),
            "type": "anomaly"
        })

    if not anomalies and is_demo:
        anomalies = [{
            "title": "Queda no ROAS (Demo)",
            "message": "Anomalia simulada para demonstração.",
            "type": "anomaly"
        }]

    # Registrar evento de auditoria
    db.log_audit(
        action="dashboard_view",
        actor_type="user",
        tenant_id=tenant['id'],
        details={"mode": "demo" if is_demo else "production"}
    )

    return {
        "status": "success",
        "tenant_name": tenant['name'],
        "is_demo": is_demo,
        "kpis": {
            "revenue": {
                "value": revenue,
                "trend": trends["revenue"]["trend"],
                "isPositive": trends["revenue"]["isPositive"],
                "lineage": lineage_info["revenue"]
            },
            "spend": {
                "value": spend,
                "trend": trends["spend"]["trend"],
                "isPositive": trends["spend"]["isPositive"]
            },
            "roas": {
                "value": roas,
                "trend": trends["roas"]["trend"],
                "isPositive": trends["roas"]["isPositive"],
                "lineage": lineage_info["roas"]
            },
            "cac": {
                "value": cac,
                "trend": trends["cac"]["trend"],
                "isPositive": not trends["cac"]["isPositive"],
                "lineage": lineage_info["cac"]
            }
        },
        "charts": real_charts,
        "anomalies": anomalies
    }
