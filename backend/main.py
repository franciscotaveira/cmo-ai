"""
╔═══════════════════════════════════════════════════════════════════════════════
║ CMO 360° — BACKEND API (FastAPI)
╠═══════════════════════════════════════════════════════════════════════════════
║ API principal para o Painel Web
║ Fornece endpoints para dashboard, alertas, insights, etc.
╚═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import json

from supabase import create_client

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="CMO 360° API",
    description="API para Painel de Marketing C-Level",
    version="1.0.0"
)

# CORS (permitir frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

# Security
security = HTTPBearer(auto_error=False)

# ═══════════════════════════════════════════════════════════════════════════════
# MODELOS
# ═══════════════════════════════════════════════════════════════════════════════

class DashboardResponse(BaseModel):
    kpis: Dict[str, Any]
    alerts_count: int
    insights_count: int
    tenants: List[Dict[str, Any]]

class AlertResponse(BaseModel):
    id: str
    tenant_name: str
    metric_key: str
    metric_value: float
    expected_value: Optional[float]
    z_score: Optional[float]
    severity: str
    status: str
    detected_at: str

class InsightResponse(BaseModel):
    id: str
    tenant_name: str
    context: str
    ai_response: str
    confidence_score: Optional[float]
    source_model: Optional[str]
    created_at: str

class ChannelPerformance(BaseModel):
    channel: str
    spend: float
    revenue: float
    roas: float
    ctr: float
    status: str

# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Verifica se API está online."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    """
    Obtém dashboard executivo com KPIs em tempo real.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        # Buscar tenants
        tenants_response = supabase.table("tenants").select("id, name, slug, type").execute()
        tenants = tenants_response.data or []

        # Contar alertas críticos
        alerts_response = supabase.table("anomaly_alerts")\
            .select("id", count="exact")\
            .eq("status", "new")\
            .eq("severity", "critical")\
            .execute()
        alerts_count = alerts_response.count or 0

        # Contar insights novos
        insights_response = supabase.table("strategic_insights")\
            .select("id", count="exact")\
            .eq("status", "new")\
            .execute()
        insights_count = insights_response.count or 0

        # KPIs agregados (simulado - na prática vem de queries)
        kpis = {
            "revenue_today": 45200.00,
            "revenue_change": 12.5,
            "cac_average": 52.00,
            "cac_change": -8.3,
            "roas_average": 3.8,
            "roas_change": 5.2,
            "nps_average": 64,
            "nps_change": 0.0
        }

        return DashboardResponse(
            kpis=kpis,
            alerts_count=alerts_count,
            insights_count=insights_count,
            tenants=tenants
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# ALERTAS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/alerts", response_model=List[AlertResponse])
async def get_alerts(severity: Optional[str] = None, limit: int = 20):
    """
    Obtém alertas críticos que precisam de ação.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        query = supabase.table("anomaly_alerts")\
            .select("*, tenants(name, slug)")\
            .eq("status", "new")\
            .order("detected_at", desc=True)\
            .limit(limit)

        if severity:
            query = query.eq("severity", severity)

        response = query.execute()
        alerts = response.data or []

        # Format response
        formatted_alerts = []
        for alert in alerts:
            tenant_name = alert.get('tenants', {}).get('name', 'N/A') if alert.get('tenants') else 'N/A'
            formatted_alerts.append({
                "id": alert["id"],
                "tenant_name": tenant_name,
                "metric_key": alert["metric_key"],
                "metric_value": float(alert["metric_value"]),
                "expected_value": float(alert["expected_value"]) if alert.get("expected_value") else None,
                "z_score": float(alert["z_score"]) if alert.get("z_score") else None,
                "severity": alert["severity"],
                "status": alert["status"],
                "detected_at": alert["detected_at"]
            })

        return formatted_alerts

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Reconhece um alerta (marca como visualizado)."""
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        response = supabase.table("anomaly_alerts")\
            .update({"status": "acknowledged"})\
            .eq("id", alert_id)\
            .execute()

        return {"status": "success", "message": f"Alert {alert_id} acknowledged"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/insights", response_model=List[InsightResponse])
async def get_insights(limit: int = 10):
    """
    Obtém insights gerados pela IA.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        response = supabase.table("strategic_insights")\
            .select("*, tenants(name, slug)")\
            .eq("status", "new")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()

        insights = response.data or []

        # Format response
        formatted_insights = []
        for insight in insights:
            tenant_name = insight.get('tenants', {}).get('name', 'N/A') if insight.get('tenants') else 'N/A'
            formatted_insights.append({
                "id": insight["id"],
                "tenant_name": tenant_name,
                "context": insight["context"],
                "ai_response": insight["ai_response"],
                "confidence_score": float(insight["confidence_score"]) if insight.get("confidence_score") else None,
                "source_model": insight.get("source_model", "N/A"),
                "created_at": insight["created_at"]
            })

        return formatted_insights

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE POR CANAL
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/channels/performance", response_model=List[ChannelPerformance])
async def get_channel_performance():
    """
    Obtém performance de canais de marketing.
    """
    # Dados simulados (na prática vem do Supabase)
    channels = [
        {"channel": "Google Ads", "spend": 5000, "revenue": 26000, "roas": 5.2, "ctr": 4.5, "status": "good"},
        {"channel": "Meta Ads", "spend": 4000, "revenue": 10000, "roas": 2.5, "ctr": 1.8, "status": "warning"},
        {"channel": "LinkedIn Ads", "spend": 3000, "revenue": 9000, "roas": 3.0, "ctr": 1.2, "status": "warning"},
        {"channel": "Email", "spend": 500, "revenue": 5000, "roas": 10.0, "ctr": 3.5, "status": "excellent"}
    ]

    return channels

# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET (Tempo Real)
# ═══════════════════════════════════════════════════════════════════════════════

@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    """
    WebSocket para notificações em tempo real.
    Envia alertas e insights assim que são criados.
    """
    await websocket.accept()

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:
        print("Client disconnected")

# ═══════════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
