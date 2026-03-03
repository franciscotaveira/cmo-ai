#!/usr/bin/env python3
"""
LUNA OS Project Creator
Creates the complete LUNA Core v2.0 project structure
"""

import os
import json

BASE_DIR = "/Users/franciscotaveira.ads/LUNA OS"

def create_file(path: str, content: str):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {os.path.relpath(path, BASE_DIR)}")

def main():
    print("\n🌙 Creating LUNA OS v2.0 project...\n")
    
    # ========== .env.example ==========
    create_file(f"{BASE_DIR}/.env.example", '''# ===========================================
# LUNA CORE v2.0 - Environment Variables
# ===========================================

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8081
EVOLUTION_API_KEY=your-evolution-key
EVOLUTION_INSTANCE=haven

# Anthropic (Claude)
ANTHROPIC_API_KEY=your-anthropic-key

# OpenRouter (alternativa)
OPENROUTER_API_KEY=your-openrouter-key

# Belasis (futuro)
BELASIS_API_URL=https://api.belasis.com.br
BELASIS_API_KEY=

# App
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=your-secret-key-here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
''')
    
    # ========== docker-compose.yml ==========
    create_file(f"{BASE_DIR}/docker-compose.yml", '''version: '3.8'

services:
  # Backend FastAPI
  luna-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: luna-backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - EVOLUTION_API_URL=${EVOLUTION_API_URL}
      - EVOLUTION_API_KEY=${EVOLUTION_API_KEY}
      - EVOLUTION_INSTANCE=${EVOLUTION_INSTANCE}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    volumes:
      - ./backend:/app
    restart: unless-stopped
    networks:
      - luna-network

  # Frontend Next.js
  luna-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: luna-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://luna-backend:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    restart: unless-stopped
    networks:
      - luna-network
    depends_on:
      - luna-backend

networks:
  luna-network:
    driver: bridge
''')
    
    # ========== backend/requirements.txt ==========
    create_file(f"{BASE_DIR}/backend/requirements.txt", '''# FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic-settings==2.1.0

# Supabase
supabase==2.3.4

# Anthropic
anthropic==0.18.1

# HTTP Client
httpx==0.26.0
aiohttp==3.9.3

# Data Processing
pydantic==2.5.3
pandas==2.2.0

# Utilities
python-dateutil==2.8.2
pytz==2024.1

# File Processing
openpyxl==3.1.2
python-docx==1.1.0
PyPDF2==3.0.1
''')
    
    # ========== backend/Dockerfile ==========
    create_file(f"{BASE_DIR}/backend/Dockerfile", '''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
''')
    
    # ========== backend/app/config.py ==========
    create_file(f"{BASE_DIR}/backend/app/config.py", '''"""
LUNA CORE - Configuration
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # App
    app_name: str = "Luna Core"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("APP_DEBUG", "false").lower() == "true"
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    
    # Evolution API
    evolution_url: str = os.getenv("EVOLUTION_API_URL", "http://localhost:8081")
    evolution_key: str = os.getenv("EVOLUTION_API_KEY", "")
    evolution_instance: str = os.getenv("EVOLUTION_INSTANCE", "haven")
    
    # Anthropic
    anthropic_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # OpenRouter
    openrouter_key: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # Belasis
    belasis_url: str = os.getenv("BELASIS_API_URL", "")
    belasis_key: str = os.getenv("BELASIS_API_KEY", "")
    
    # Models
    model_quick: str = "claude-3-haiku-20240307"
    model_standard: str = "claude-3-5-sonnet-20241022"
    
    class Config:
        env_file = ".env"

settings = Settings()
''')
    
    # ========== backend/app/main.py ==========
    create_file(f"{BASE_DIR}/backend/app/main.py", '''"""
LUNA CORE v2.0 - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api import webhooks, conversations, clients, analytics, campaigns, knowledge, settings as settings_api
from app.integrations.supabase_client import init_supabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🌙 Luna Core v2.0 starting...")
    await init_supabase()
    print("✅ Supabase connected")
    print(f"✅ Luna Core ready on port 8000")
    yield
    # Shutdown
    print("🌙 Luna Core shutting down...")

app = FastAPI(
    title="Luna Core",
    description="Sistema de Atendimento IA para Haven Escovaria & Esmalteria",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["Settings"])

@app.get("/")
async def root():
    return {
        "name": "Luna Core",
        "version": "2.0.0",
        "status": "operational",
        "modules": ["brain", "memory", "analytics", "campaigns", "knowledge"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}
''')
    
    # ========== backend/app/integrations/supabase_client.py ==========
    create_file(f"{BASE_DIR}/backend/app/integrations/supabase_client.py", '''"""
Supabase Client
"""
from supabase import create_client, Client
from app.config import settings

supabase: Client = None

async def init_supabase():
    global supabase
    supabase = create_client(settings.supabase_url, settings.supabase_key)
    return supabase

def get_supabase() -> Client:
    global supabase
    if supabase is None:
        supabase = create_client(settings.supabase_url, settings.supabase_key)
    return supabase
''')
    
    # ========== backend/app/integrations/evolution.py ==========
    create_file(f"{BASE_DIR}/backend/app/integrations/evolution.py", '''"""
Evolution API Integration (WhatsApp)
"""
import httpx
from app.config import settings

class EvolutionAPI:
    def __init__(self):
        self.base_url = settings.evolution_url
        self.api_key = settings.evolution_key
        self.instance = settings.evolution_instance
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}
    
    async def send_text(self, to: str, text: str) -> dict:
        """Send text message"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendText/{self.instance}",
                headers=self.headers,
                json={"number": to.replace("@s.whatsapp.net", ""), "text": text}
            )
            return response.json()
    
    async def send_buttons(self, to: str, text: str, buttons: list) -> dict:
        """Send buttons message"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendButtons/{self.instance}",
                headers=self.headers,
                json={
                    "number": to.replace("@s.whatsapp.net", ""),
                    "title": "Opções",
                    "description": text,
                    "buttons": [{"buttonId": f"btn_{i}", "buttonText": {"displayText": b}} for i, b in enumerate(buttons)]
                }
            )
            return response.json()
    
    async def send_location(self, to: str, lat: float, lng: float, name: str, address: str) -> dict:
        """Send location"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendLocation/{self.instance}",
                headers=self.headers,
                json={
                    "number": to.replace("@s.whatsapp.net", ""),
                    "latitude": lat,
                    "longitude": lng,
                    "name": name,
                    "address": address
                }
            )
            return response.json()
    
    async def get_instance_status(self) -> dict:
        """Get instance connection status"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/instance/connectionState/{self.instance}",
                headers=self.headers
            )
            return response.json()

evolution = EvolutionAPI()
''')
    
    # ========== backend/app/integrations/anthropic.py ==========
    create_file(f"{BASE_DIR}/backend/app/integrations/anthropic.py", '''"""
Anthropic Claude Integration
"""
import anthropic
import httpx
from app.config import settings

class ClaudeAPI:
    def __init__(self):
        self.use_openrouter = bool(settings.openrouter_key)
        
        if self.use_openrouter:
            self.base_url = "https://openrouter.ai/api/v1/chat/completions"
            self.api_key = settings.openrouter_key
        else:
            self.client = anthropic.Anthropic(api_key=settings.anthropic_key)
    
    async def complete(
        self,
        messages: list,
        system: str = "",
        model: str = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """Generate completion"""
        model = model or settings.model_quick
        
        if self.use_openrouter:
            return await self._openrouter_complete(messages, system, model, max_tokens, temperature)
        else:
            return await self._anthropic_complete(messages, system, model, max_tokens, temperature)
    
    async def _anthropic_complete(self, messages, system, model, max_tokens, temperature):
        """Direct Anthropic API"""
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages
        )
        return response.content[0].text
    
    async def _openrouter_complete(self, messages, system, model, max_tokens, temperature):
        """OpenRouter API"""
        # Prepend system message
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)
        
        # Map model names
        model_map = {
            "claude-3-haiku-20240307": "anthropic/claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022": "anthropic/claude-3-5-sonnet-20241022"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://haven.mct.com.br",
                    "X-Title": "Luna Core"
                },
                json={
                    "model": model_map.get(model, model),
                    "messages": full_messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=60.0
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]

claude = ClaudeAPI()
''')
    
    print("\n✅ Core backend files created!")
    
    # ========== backend/app/api/webhooks.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/webhooks.py", '''"""
Webhooks API - Evolution WhatsApp
"""
from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import json

from app.core.brain import process_message
from app.core.memory import Memory
from app.integrations.evolution import evolution

router = APIRouter()
memory = Memory()

class WebhookPayload(BaseModel):
    event: str
    instance: str
    data: dict

@router.post("/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook receiver for Evolution API
    """
    try:
        body = await request.json()
        event = body.get("event", "")
        instance = body.get("instance", "")
        data = body.get("data", {})
        
        print(f"📩 Webhook: {event} from {instance}")
        
        # Process only incoming messages
        if event == "messages.upsert":
            message_data = data.get("message", {})
            key = data.get("key", {})
            
            # Skip outgoing messages
            if key.get("fromMe", False):
                return {"status": "ignored", "reason": "outgoing message"}
            
            # Extract info
            remote_jid = key.get("remoteJid", "")
            push_name = data.get("pushName", "")
            
            # Get message content
            text = None
            if "conversation" in message_data:
                text = message_data["conversation"]
            elif "extendedTextMessage" in message_data:
                text = message_data["extendedTextMessage"].get("text", "")
            
            if text and remote_jid:
                # Process in background
                background_tasks.add_task(
                    handle_message,
                    remote_jid,
                    push_name,
                    text
                )
                return {"status": "processing"}
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}

async def handle_message(remote_jid: str, push_name: str, text: str):
    """
    Process incoming message
    """
    try:
        print(f"💬 Processing: {push_name} ({remote_jid}): {text[:50]}...")
        
        # Get conversation history
        history = await memory.get_conversation_context(remote_jid)
        
        # Process with brain
        result = await process_message(
            phone=remote_jid,
            name=push_name,
            message=text,
            history=history
        )
        
        # Send response
        if result.get("response"):
            await evolution.send_text(remote_jid, result["response"])
        
        # Handle special actions
        if result.get("action") == "send_location":
            await evolution.send_location(
                remote_jid,
                lat=-27.0922,
                lng=-52.6158,
                name="Haven Escovaria & Esmalteria",
                address="Rua Mato Grosso, 837E - Jardim Itália, Chapecó - SC"
            )
        
        # Update memory
        await memory.save_message(
            phone=remote_jid,
            direction="inbound",
            content=text,
            intent=result.get("intent"),
            sentiment=result.get("sentiment")
        )
        await memory.save_message(
            phone=remote_jid,
            direction="outbound",
            content=result.get("response", ""),
            model_used=result.get("model")
        )
        
        print(f"✅ Response sent to {push_name}")
        
    except Exception as e:
        print(f"❌ Message handling error: {e}")
        # Send fallback message
        await evolution.send_text(
            remote_jid,
            "Oi! Tive um probleminha técnico. Pode repetir sua mensagem? 😊"
        )
''')
    
    # ========== backend/app/api/conversations.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/conversations.py", '''"""Conversations API"""
from fastapi import APIRouter
from app.integrations.supabase_client import get_supabase

router = APIRouter()

@router.get("/")
async def list_conversations(status: str = None, limit: int = 50):
    db = get_supabase()
    query = db.table("conversations").select("*, client:clients(name, phone)").order("started_at", desc=True).limit(limit)
    if status:
        query = query.eq("status", status)
    return query.execute().data or []

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    db = get_supabase()
    conv = db.table("conversations").select("*").eq("id", conversation_id).execute()
    messages = db.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
    return {"conversation": conv.data[0] if conv.data else None, "messages": messages.data or []}

@router.get("/active")
async def get_active_conversations():
    db = get_supabase()
    return db.table("conversations").select("*, client:clients(name, phone)").eq("status", "active").execute().data or []

@router.get("/handoffs")
async def get_handoffs():
    db = get_supabase()
    return db.table("handoffs").select("*, conversation:conversations(*), client:clients(*)").eq("status", "pending").execute().data or []
''')
    
    # ========== backend/app/api/clients.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/clients.py", '''"""Clients API"""
from fastapi import APIRouter
from app.integrations.supabase_client import get_supabase

router = APIRouter()

@router.get("/")
async def list_clients(limit: int = 50):
    db = get_supabase()
    return db.table("clients").select("*").order("last_contact", desc=True).limit(limit).execute().data or []

@router.get("/{client_id}")
async def get_client(client_id: str):
    db = get_supabase()
    client = db.table("clients").select("*").eq("id", client_id).execute()
    conversations = db.table("conversations").select("*").eq("client_id", client_id).order("started_at", desc=True).limit(20).execute()
    appointments = db.table("appointments").select("*").eq("client_id", client_id).order("date", desc=True).limit(20).execute()
    return {
        "client": client.data[0] if client.data else None,
        "conversations": conversations.data or [],
        "appointments": appointments.data or []
    }
''')
    
    # ========== backend/app/api/analytics.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/analytics.py", '''"""
Analytics API Endpoints
"""
from fastapi import APIRouter, Query
from app.analytics.insights import insights

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(days: int = Query(7, ge=1, le=90)):
    """Get dashboard metrics"""
    return await insights.get_dashboard_metrics(days)

@router.get("/hourly")
async def get_hourly(days: int = Query(30, ge=1, le=90)):
    """Get hourly distribution"""
    return await insights.get_hourly_distribution(days)

@router.get("/services")
async def get_services(days: int = Query(30, ge=1, le=90), limit: int = Query(10, ge=1, le=50)):
    """Get top services"""
    return await insights.get_top_services(days, limit)

@router.get("/professionals")
async def get_professionals(days: int = Query(30, ge=1, le=90), limit: int = Query(10, ge=1, le=50)):
    """Get top professionals"""
    return await insights.get_top_professionals(days, limit)

@router.get("/intents")
async def get_intents(days: int = Query(30, ge=1, le=90)):
    """Get intent distribution"""
    return await insights.get_intent_distribution(days)

@router.get("/sentiment")
async def get_sentiment(days: int = Query(30, ge=1, le=90)):
    """Get sentiment distribution"""
    return await insights.get_sentiment_distribution(days)
''')
    
    # ========== backend/app/api/campaigns.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/campaigns.py", '''"""
Campaigns API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.campaigns.manager import campaign_manager

router = APIRouter()

class CampaignCreate(BaseModel):
    name: str
    type: str  # seasonal, followup, reactivation
    start_date: Optional[str]
    end_date: Optional[str]
    discount_percent: Optional[int]
    discount_fixed: Optional[float]
    services: Optional[List[str]] = []
    trigger_keywords: Optional[List[str]] = []
    message_template: Optional[str]
    target_segment: Optional[str] = "all"

@router.post("/")
async def create_campaign(campaign: CampaignCreate):
    """Create new campaign"""
    return await campaign_manager.create_campaign(campaign.dict())

@router.get("/")
async def list_campaigns():
    """List all campaigns"""
    from app.integrations.supabase_client import get_supabase
    db = get_supabase()
    result = db.table("campaigns").select("*").order("created_at", desc=True).execute()
    return result.data or []

@router.get("/active")
async def list_active_campaigns():
    """List active campaigns"""
    return await campaign_manager.get_active_campaigns()

@router.patch("/{campaign_id}/status")
async def update_campaign_status(campaign_id: str, status: str):
    """Update campaign status"""
    from app.integrations.supabase_client import get_supabase
    db = get_supabase()
    result = db.table("campaigns").update({"status": status}).eq("id", campaign_id).execute()
    return result.data[0] if result.data else {"error": "Campaign not found"}
''')
    
    # ========== backend/app/api/knowledge.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/knowledge.py", '''"""Knowledge Base API"""
from fastapi import APIRouter, UploadFile, File
from app.integrations.supabase_client import get_supabase
import json

router = APIRouter()

@router.get("/")
async def get_knowledge():
    db = get_supabase()
    return db.table("knowledge_base").select("*").execute().data or []

@router.get("/{category}")
async def get_knowledge_category(category: str):
    db = get_supabase()
    return db.table("knowledge_base").select("*").eq("category", category).execute().data or []

@router.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """Upload JSON or Excel file to update knowledge base"""
    content = await file.read()
    if file.filename.endswith('.json'):
        data = json.loads(content)
        # Process and save to Supabase
        return {"status": "uploaded", "records": len(data)}
    return {"error": "Unsupported file type"}

@router.put("/{category}/{key}")
async def update_knowledge(category: str, key: str, data: dict):
    db = get_supabase()
    db.table("knowledge_base").upsert({
        "category": category,
        "key": key,
        "data": data
    }).execute()
    return {"status": "updated"}
''')
    
    # ========== backend/app/api/settings.py ==========
    create_file(f"{BASE_DIR}/backend/app/api/settings.py", '''"""Settings API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_settings():
    return {
        "bot": {
            "name": "Luna",
            "greeting": "Oi! Sou a Luna, sua assistente virtual da Haven 🌙",
            "fallback": "Desculpa, não entendi. Pode reformular?",
            "handoff_trigger": "falar com humano"
        },
        "models": {
            "quick": "claude-3-haiku-20240307",
            "standard": "claude-3-5-sonnet-20241022"
        },
        "business": {
            "name": "Haven Escovaria & Esmalteria",
            "hours": "Segunda a Sábado, 8h às 20h"
        }
    }

@router.put("/")
async def update_settings(settings: dict):
    # Save to Supabase or config
    return {"status": "updated", "settings": settings}
''')
    
    print("\n✅ API endpoints created!")
    
    # ========== backend/app/core/memory.py ==========
    create_file(f"{BASE_DIR}/backend/app/core/memory.py", '''"""
LUNA Memory System - Curto, Médio e Longo Prazo
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from app.integrations.supabase_client import get_supabase

class Memory:
    def __init__(self):
        self.supabase = None
    
    def _get_db(self):
        if self.supabase is None:
            self.supabase = get_supabase()
        return self.supabase
    
    # ==================== CLIENT MEMORY (LONGO PRAZO) ====================
    
    async def get_or_create_client(self, phone: str, name: str = None) -> dict:
        """Get or create client profile"""
        db = self._get_db()
        
        # Try to find existing
        result = db.table("clients").select("*").eq("phone", phone).execute()
        
        if result.data:
            client = result.data[0]
            # Update last contact
            db.table("clients").update({
                "last_contact": datetime.utcnow().isoformat(),
                "name": name or client.get("name")
            }).eq("phone", phone).execute()
            return client
        
        # Create new
        new_client = {
            "phone": phone,
            "name": name,
            "first_contact": datetime.utcnow().isoformat(),
            "last_contact": datetime.utcnow().isoformat(),
            "tags": [],
            "preferences": {},
            "total_visits": 0,
            "total_spent": 0
        }
        result = db.table("clients").insert(new_client).execute()
        return result.data[0] if result.data else new_client
    
    async def update_client_profile(self, phone: str, updates: dict) -> dict:
        """Update client profile"""
        db = self._get_db()
        result = db.table("clients").update(updates).eq("phone", phone).execute()
        return result.data[0] if result.data else None
    
    async def add_client_tag(self, phone: str, tag: str):
        """Add tag to client"""
        db = self._get_db()
        client = await self.get_or_create_client(phone)
        tags = client.get("tags", [])
        if tag not in tags:
            tags.append(tag)
            db.table("clients").update({"tags": tags}).eq("phone", phone).execute()
    
    # ==================== CONVERSATION MEMORY (CURTO PRAZO) ====================
    
    async def get_active_conversation(self, phone: str) -> Optional[dict]:
        """Get active conversation for phone"""
        db = self._get_db()
        result = db.table("conversations")\\
            .select("*")\\
            .eq("phone", phone)\\
            .eq("status", "active")\\
            .order("started_at", desc=True)\\
            .limit(1)\\
            .execute()
        return result.data[0] if result.data else None
    
    async def start_conversation(self, phone: str, client_id: str = None) -> dict:
        """Start new conversation"""
        db = self._get_db()
        conversation = {
            "phone": phone,
            "client_id": client_id,
            "status": "active",
            "started_at": datetime.utcnow().isoformat(),
            "messages_count": 0,
            "extracted_data": {}
        }
        result = db.table("conversations").insert(conversation).execute()
        return result.data[0] if result.data else conversation
    
    async def update_conversation(self, conversation_id: str, updates: dict):
        """Update conversation"""
        db = self._get_db()
        db.table("conversations").update(updates).eq("id", conversation_id).execute()
    
    async def end_conversation(self, conversation_id: str, result: str):
        """End conversation with result"""
        db = self._get_db()
        db.table("conversations").update({
            "status": "ended",
            "conversion_result": result,
            "ended_at": datetime.utcnow().isoformat()
        }).eq("id", conversation_id).execute()
    
    # ==================== MESSAGES ====================
    
    async def save_message(
        self,
        phone: str,
        direction: str,
        content: str,
        intent: str = None,
        sentiment: str = None,
        model_used: str = None
    ):
        """Save message to database"""
        db = self._get_db()
        
        # Get or create conversation
        conversation = await self.get_active_conversation(phone)
        if not conversation:
            client = await self.get_or_create_client(phone)
            conversation = await self.start_conversation(phone, client.get("id"))
        
        # Save message
        message = {
            "conversation_id": conversation["id"],
            "direction": direction,
            "content": content,
            "intent_detected": intent,
            "sentiment": sentiment,
            "model_used": model_used,
            "created_at": datetime.utcnow().isoformat()
        }
        db.table("messages").insert(message).execute()
        
        # Update conversation count
        db.table("conversations").update({
            "messages_count": conversation.get("messages_count", 0) + 1,
            "intent": intent or conversation.get("intent"),
            "sentiment": sentiment or conversation.get("sentiment")
        }).eq("id", conversation["id"]).execute()
    
    async def get_conversation_context(self, phone: str, limit: int = 15) -> List[dict]:
        """Get recent messages for context"""
        db = self._get_db()
        
        conversation = await self.get_active_conversation(phone)
        if not conversation:
            return []
        
        result = db.table("messages")\\
            .select("direction, content")\\
            .eq("conversation_id", conversation["id"])\\
            .order("created_at", desc=True)\\
            .limit(limit)\\
            .execute()
        
        # Convert to Claude format
        messages = []
        for msg in reversed(result.data or []):
            role = "user" if msg["direction"] == "inbound" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        return messages
    
    # ==================== MÉDIO PRAZO (30 dias) ====================
    
    async def get_recent_history(self, phone: str, days: int = 30) -> dict:
        """Get client's recent history"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        # Recent conversations
        conversations = db.table("conversations")\\
            .select("*")\\
            .eq("phone", phone)\\
            .gte("started_at", since)\\
            .execute()
        
        # Recent appointments
        appointments = db.table("appointments")\\
            .select("*")\\
            .eq("client_phone", phone)\\
            .gte("date", since[:10])\\
            .execute()
        
        # Analyze patterns
        services_done = []
        professionals_used = []
        preferred_times = []
        
        for apt in (appointments.data or []):
            if apt.get("service_name"):
                services_done.append(apt["service_name"])
            if apt.get("professional_name"):
                professionals_used.append(apt["professional_name"])
            if apt.get("time"):
                preferred_times.append(apt["time"][:2])  # Hour only
        
        return {
            "total_conversations": len(conversations.data or []),
            "total_appointments": len(appointments.data or []),
            "services_done": list(set(services_done)),
            "professionals_used": list(set(professionals_used)),
            "preferred_hours": list(set(preferred_times)),
            "last_visit": appointments.data[0]["date"] if appointments.data else None
        }
    
    # ==================== EXTRACTED DATA ====================
    
    async def save_extracted_data(self, phone: str, field: str, value: any):
        """Save extracted field from conversation"""
        conversation = await self.get_active_conversation(phone)
        if conversation:
            extracted = conversation.get("extracted_data", {})
            extracted[field] = value
            await self.update_conversation(conversation["id"], {"extracted_data": extracted})
    
    async def get_extracted_data(self, phone: str) -> dict:
        """Get all extracted data from current conversation"""
        conversation = await self.get_active_conversation(phone)
        return conversation.get("extracted_data", {}) if conversation else {}
''')
    
    print("\n✅ Memory system created!")

if __name__ == "__main__":
    main()
