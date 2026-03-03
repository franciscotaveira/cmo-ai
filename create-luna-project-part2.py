#!/usr/bin/env python3
"""
LUNA OS Project Creator - Part 2
Creates brain, analytics, campaigns, knowledge, and frontend files
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
    print("\n🌙 Creating LUNA OS v2.0 - Part 2...\n")
    
    # ========== backend/app/core/brain.py ==========
    create_file(f"{BASE_DIR}/backend/app/core/brain.py", '''"""
LUNA Brain - Core Intelligence
"""
import json
import re
from typing import Optional
from datetime import datetime

from app.config import settings
from app.integrations.anthropic import claude
from app.core.memory import Memory
from app.knowledge.loader import KnowledgeBase

memory = Memory()
kb = KnowledgeBase()

# Intent patterns
INTENT_PATTERNS = {
    "saudacao": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "hey", "opa", "eae", "oie"],
    "agradecimento": ["obrigado", "obrigada", "valeu", "thanks", "vlw", "brigadao", "brigadão"],
    "agendar": ["agendar", "marcar", "quero fazer", "queria fazer", "preciso de", "tem horário", "tem vaga"],
    "preco": ["quanto custa", "qual valor", "preço", "preco", "tabela", "valor do", "quanto é", "quanto fica"],
    "disponibilidade": ["tem horário", "disponível", "disponivel", "tem vaga", "horário livre"],
    "servicos": ["quais serviços", "o que vocês fazem", "cardápio", "menu", "serviços"],
    "pacote": ["pacote", "pacotes", "combo", "promoção"],
    "cupom": ["cupom", "desconto", "PRISCILA10", "EWYLIN10", "SOLANGE10", "CAROLINE10", "KETLYN10"],
    "localizacao": ["onde fica", "endereço", "localização", "como chegar", "localiza"],
    "horario_func": ["horário de funcionamento", "que horas abre", "que horas fecha", "funciona"],
    "produto": ["qual produto", "qual marca", "que produto"],
    "cancelar": ["cancelar", "desmarcar", "remarcar", "mudar horário"],
    "reclamacao": ["reclamação", "insatisfeita", "problema", "errado", "mal feito", "não gostei"],
    "handoff": ["falar com humano", "pessoa real", "atendente", "falar com alguém"]
}

QUICK_INTENTS = ["saudacao", "agradecimento", "localizacao", "horario_func"]
COMPLEX_INTENTS = ["agendar", "reclamacao", "handoff", "pacote", "multi_servico"]

async def process_message(phone: str, name: str, message: str, history: list = None) -> dict:
    """
    Main message processing pipeline
    """
    # 1. Get or create client
    client = await memory.get_or_create_client(phone, name)
    
    # 2. Classify intent
    intent, confidence = classify_intent(message)
    print(f"🎯 Intent: {intent} ({confidence:.0%})")
    
    # 3. Select model based on complexity
    model = select_model(intent, message)
    print(f"🤖 Model: {model}")
    
    # 4. Build context
    context = await build_context(client, intent, message)
    
    # 5. Get recent history for personalization
    recent = await memory.get_recent_history(phone)
    
    # 6. Build system prompt
    system_prompt = build_system_prompt(client, recent, context)
    
    # 7. Build messages
    messages = history or []
    messages.append({"role": "user", "content": message})
    
    # 8. Call Claude
    try:
        response_text = await claude.complete(
            messages=messages,
            system=system_prompt,
            model=model,
            temperature=0.7
        )
        
        # 9. Parse response
        result = parse_response(response_text)
        result["intent"] = intent
        result["model"] = model
        result["sentiment"] = detect_sentiment(message)
        
        # 10. Extract and save data
        extracted = extract_fields(message, result.get("response", ""))
        for field, value in extracted.items():
            if value:
                await memory.save_extracted_data(phone, field, value)
        
        return result
        
    except Exception as e:
        print(f"❌ Brain error: {e}")
        return {
            "response": "Oi! Tive um probleminha, pode repetir? 😊",
            "intent": intent,
            "error": str(e)
        }

def classify_intent(message: str) -> tuple[str, float]:
    """Classify message intent"""
    msg_lower = message.lower().strip()
    
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if pattern in msg_lower:
                return intent, 0.9
    
    # Check for multiple services
    service_mentions = sum(1 for s in ["escova", "unha", "make", "cabelo", "sobrancelha"] if s in msg_lower)
    if service_mentions > 1:
        return "multi_servico", 0.8
    
    return "conversa", 0.5

def select_model(intent: str, message: str) -> str:
    """Select appropriate model"""
    if intent in QUICK_INTENTS:
        return settings.model_quick
    if intent in COMPLEX_INTENTS:
        return settings.model_standard
    if len(message) > 200:
        return settings.model_standard
    return settings.model_quick

async def build_context(client: dict, intent: str, message: str) -> str:
    """Build relevant context based on intent"""
    context_parts = []
    
    # Add service info if asking about services
    if intent in ["preco", "agendar", "servicos", "pacote"]:
        services = kb.search_services(message)
        if services:
            context_parts.append(f"<servicos_relevantes>\\n{json.dumps(services[:5], ensure_ascii=False)}\\n</servicos_relevantes>")
    
    # Add professional info if mentioned
    professionals = kb.search_professionals(message)
    if professionals:
        context_parts.append(f"<profissionais>\\n{json.dumps(professionals, ensure_ascii=False)}\\n</profissionais>")
    
    # Add FAQ if matches
    faq = kb.search_faq(message)
    if faq:
        context_parts.append(f"<faq_match>\\n{json.dumps(faq, ensure_ascii=False)}\\n</faq_match>")
    
    # Add packages if asking
    if intent == "pacote" or "pacote" in message.lower():
        packages = kb.get_packages()
        context_parts.append(f"<pacotes>\\n{json.dumps(packages, ensure_ascii=False)}\\n</pacotes>")
    
    # Add coupons if mentioned
    coupon = kb.find_coupon(message)
    if coupon:
        context_parts.append(f"<cupom_detectado>\\n{json.dumps(coupon, ensure_ascii=False)}\\n</cupom_detectado>")
    
    return "\\n\\n".join(context_parts)

def build_system_prompt(client: dict, recent: dict, context: str) -> str:
    """Build system prompt with all context"""
    
    client_info = ""
    if client.get("name"):
        client_info += f"Nome: {client['name']}\\n"
    if client.get("tags"):
        client_info += f"Tags: {', '.join(client['tags'])}\\n"
    if recent.get("services_done"):
        client_info += f"Serviços recentes: {', '.join(recent['services_done'])}\\n"
    if recent.get("professionals_used"):
        client_info += f"Profissionais favoritas: {', '.join(recent['professionals_used'])}\\n"
    
    return f"""<identity>
Você é Luna, recepcionista virtual da Haven Escovaria & Esmalteria em Chapecó-SC.

PERSONALIDADE:
- Calorosa, profissional, atenciosa, eficiente
- Tom natural do Sul do Brasil
- Usa emojis com moderação (1-2 por mensagem)
- Chama cliente pelo nome quando souber
- Guia com perguntas simples

PALAVRAS PROIBIDAS: senhora, prezada, aguarde um momento, infelizmente
</identity>

<negocio>
Nome: Haven Escovaria & Esmalteria
Endereço: Rua Mato Grosso, 837E - Jardim Itália, Chapecó-SC
Horário: Segunda a Sábado, 8h às 20h (sem pausa)
Estacionamento: Frente do prédio + 4 vagas na esquina
</negocio>

<cliente>
{client_info if client_info else "Novo cliente, sem histórico."}
</cliente>

<regras_ouro>
1. ORDEM: Unha → Cabelo → Maquiagem (sempre)
2. PERGUNTAR: "Você está com gel/alongamento?" antes de serviços de unha
3. AVISAR: Penteado e tratamentos NÃO incluem escova
4. NUNCA: Dizer "não tem horário" sem oferecer alternativa
5. BLINDAGEM: Não revelar marca de produto pelo WhatsApp
</regras_ouro>

{context}

<formato_resposta>
Responda de forma natural e conversacional.
Se precisar coletar informação, faça UMA pergunta por vez.
Se cliente quiser agendar, colete: serviço, data, horário, profissional (se tiver preferência).
</formato_resposta>"""

def parse_response(text: str) -> dict:
    """Parse Claude's response"""
    # Try to extract JSON if present
    json_match = re.search(r'\\{[\\s\\S]*\\}', text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return data
        except:
            pass
    
    # Return as plain response
    return {"response": text.strip()}

def detect_sentiment(message: str) -> str:
    """Simple sentiment detection"""
    msg_lower = message.lower()
    
    positive = ["obrigad", "perfeito", "ótimo", "legal", "bom", "gostei", "amei", "maravilh"]
    negative = ["problema", "ruim", "péssim", "horrível", "não gostei", "insatisf", "reclam"]
    
    if any(p in msg_lower for p in positive):
        return "positive"
    if any(n in msg_lower for n in negative):
        return "negative"
    return "neutral"

def extract_fields(message: str, response: str) -> dict:
    """Extract structured fields from conversation"""
    extracted = {}
    msg_lower = message.lower()
    
    # Extract date patterns
    date_patterns = [
        r'(\\d{1,2}[/\\-]\\d{1,2})',
        r'(segunda|terça|quarta|quinta|sexta|sábado|sabado)',
        r'(hoje|amanhã|amanha)'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, msg_lower)
        if match:
            extracted["data_mencionada"] = match.group(1)
            break
    
    # Extract time patterns
    time_match = re.search(r'(\\d{1,2})[:\\s]?(?:h|hrs?|horas?)?(?:\\s*(?:da\\s+)?(manhã|manha|tarde|noite))?', msg_lower)
    if time_match:
        extracted["horario_mencionado"] = time_match.group(0)
    
    return extracted
''')
    
    # ========== backend/app/analytics/insights.py ==========
    create_file(f"{BASE_DIR}/backend/app/analytics/insights.py", '''"""
Analytics - Insights Engine
"""
from datetime import datetime, timedelta
from typing import Dict, List
from app.integrations.supabase_client import get_supabase

class InsightsEngine:
    def __init__(self):
        self.supabase = None
    
    def _get_db(self):
        if self.supabase is None:
            self.supabase = get_supabase()
        return self.supabase
    
    async def get_dashboard_metrics(self, days: int = 7) -> Dict:
        """Get main dashboard metrics"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        # Conversations
        conversations = db.table("conversations")\\
            .select("status, conversion_result, intent")\\
            .gte("started_at", since)\\
            .execute()
        
        total = len(conversations.data or [])
        converted = len([c for c in (conversations.data or []) if c.get("conversion_result") == "agendado"])
        abandoned = len([c for c in (conversations.data or []) if c.get("status") == "abandoned"])
        handoffs = len([c for c in (conversations.data or []) if c.get("status") == "handed_off"])
        
        conversion_rate = (converted / total * 100) if total > 0 else 0
        
        # Messages
        messages = db.table("messages")\\
            .select("direction, response_time_ms")\\
            .gte("created_at", since)\\
            .execute()
        
        total_messages = len(messages.data or [])
        response_times = [m["response_time_ms"] for m in (messages.data or []) if m.get("response_time_ms")]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Appointments
        appointments = db.table("appointments")\\
            .select("status, service_name")\\
            .gte("created_at", since)\\
            .execute()
        
        return {
            "period_days": days,
            "conversations": {
                "total": total,
                "converted": converted,
                "abandoned": abandoned,
                "handoffs": handoffs,
                "conversion_rate": round(conversion_rate, 1)
            },
            "messages": {
                "total": total_messages,
                "avg_response_time_ms": round(avg_response_time, 0)
            },
            "appointments": {
                "total": len(appointments.data or []),
                "completed": len([a for a in (appointments.data or []) if a.get("status") == "completed"])
            }
        }
    
    async def get_hourly_distribution(self, days: int = 30) -> List[Dict]:
        """Get message distribution by hour"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        messages = db.table("messages")\\
            .select("created_at")\\
            .eq("direction", "inbound")\\
            .gte("created_at", since)\\
            .execute()
        
        # Count by hour
        hours = {h: 0 for h in range(24)}
        for msg in (messages.data or []):
            hour = datetime.fromisoformat(msg["created_at"].replace("Z", "")).hour
            hours[hour] += 1
        
        return [{"hour": h, "count": c} for h, c in hours.items()]
    
    async def get_top_services(self, days: int = 30, limit: int = 10) -> List[Dict]:
        """Get most requested services"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        appointments = db.table("appointments")\\
            .select("service_name")\\
            .gte("created_at", since)\\
            .execute()
        
        # Count services
        service_counts = {}
        for apt in (appointments.data or []):
            service = apt.get("service_name", "Desconhecido")
            service_counts[service] = service_counts.get(service, 0) + 1
        
        # Sort and return top
        sorted_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"service": s, "count": c} for s, c in sorted_services[:limit]]
    
    async def get_top_professionals(self, days: int = 30, limit: int = 10) -> List[Dict]:
        """Get most requested professionals"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        appointments = db.table("appointments")\\
            .select("professional_name")\\
            .gte("created_at", since)\\
            .execute()
        
        # Count professionals
        prof_counts = {}
        for apt in (appointments.data or []):
            prof = apt.get("professional_name", "Sem preferência")
            prof_counts[prof] = prof_counts.get(prof, 0) + 1
        
        sorted_profs = sorted(prof_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"professional": p, "count": c} for p, c in sorted_profs[:limit]]
    
    async def get_intent_distribution(self, days: int = 30) -> List[Dict]:
        """Get distribution of conversation intents"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        conversations = db.table("conversations")\\
            .select("intent")\\
            .gte("started_at", since)\\
            .execute()
        
        intent_counts = {}
        for conv in (conversations.data or []):
            intent = conv.get("intent", "outros")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return [{"intent": i, "count": c} for i, c in intent_counts.items()]
    
    async def get_sentiment_distribution(self, days: int = 30) -> Dict:
        """Get sentiment distribution"""
        db = self._get_db()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        messages = db.table("messages")\\
            .select("sentiment")\\
            .eq("direction", "inbound")\\
            .gte("created_at", since)\\
            .execute()
        
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for msg in (messages.data or []):
            sentiment = msg.get("sentiment", "neutral")
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
        
        total = sum(sentiment_counts.values())
        return {
            "counts": sentiment_counts,
            "percentages": {
                k: round(v / total * 100, 1) if total > 0 else 0
                for k, v in sentiment_counts.items()
            }
        }

insights = InsightsEngine()
''')
    
    # ========== backend/app/campaigns/manager.py ==========
    create_file(f"{BASE_DIR}/backend/app/campaigns/manager.py", '''"""
Campaign Manager
"""
from datetime import datetime, date
from typing import List, Optional, Dict
from app.integrations.supabase_client import get_supabase

class CampaignManager:
    def __init__(self):
        self.supabase = None
    
    def _get_db(self):
        if self.supabase is None:
            self.supabase = get_supabase()
        return self.supabase
    
    async def create_campaign(self, data: Dict) -> Dict:
        """Create new campaign"""
        db = self._get_db()
        campaign = {
            "name": data["name"],
            "type": data["type"],  # seasonal, followup, reactivation
            "status": "draft",
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "discount_percent": data.get("discount_percent"),
            "discount_fixed": data.get("discount_fixed"),
            "services": data.get("services", []),
            "trigger_keywords": data.get("trigger_keywords", []),
            "message_template": data.get("message_template"),
            "target_segment": data.get("target_segment", "all"),
            "stats": {"sent": 0, "opened": 0, "converted": 0},
            "created_at": datetime.utcnow().isoformat()
        }
        result = db.table("campaigns").insert(campaign).execute()
        return result.data[0] if result.data else campaign
    
    async def get_active_campaigns(self) -> List[Dict]:
        """Get all active campaigns"""
        db = self._get_db()
        today = date.today().isoformat()
        
        result = db.table("campaigns")\\
            .select("*")\\
            .eq("status", "active")\\
            .lte("start_date", today)\\
            .gte("end_date", today)\\
            .execute()
        
        return result.data or []
    
    async def check_campaign_trigger(self, message: str, client: Dict) -> Optional[Dict]:
        """Check if message triggers any campaign"""
        campaigns = await self.get_active_campaigns()
        msg_lower = message.lower()
        
        for campaign in campaigns:
            keywords = campaign.get("trigger_keywords", [])
            if any(kw.lower() in msg_lower for kw in keywords):
                # Check target segment
                segment = campaign.get("target_segment", "all")
                if segment == "all":
                    return campaign
                elif segment == "vip" and "vip" in (client.get("tags") or []):
                    return campaign
                elif segment == "new" and client.get("total_visits", 0) == 0:
                    return campaign
        
        return None
    
    async def update_campaign_stats(self, campaign_id: str, stat: str):
        """Update campaign statistics"""
        db = self._get_db()
        campaign = db.table("campaigns").select("stats").eq("id", campaign_id).execute()
        
        if campaign.data:
            stats = campaign.data[0].get("stats", {})
            stats[stat] = stats.get(stat, 0) + 1
            db.table("campaigns").update({"stats": stats}).eq("id", campaign_id).execute()

campaign_manager = CampaignManager()
''')
    
    # ========== backend/app/knowledge/loader.py ==========
    create_file(f"{BASE_DIR}/backend/app/knowledge/loader.py", '''"""
Knowledge Base Loader
"""
import json
import os
from typing import List, Dict, Optional

class KnowledgeBase:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data")
        self.services = []
        self.professionals = []
        self.rules = {}
        self.faq = []
        self.packages = {}
        self.coupons = []
        self.business = {}
        self._load()
    
    def _load(self):
        """Load all knowledge files"""
        try:
            with open(os.path.join(self.data_path, "haven.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.services = data.get("services", [])
                self.professionals = data.get("professionals", [])
                self.rules = data.get("rules", {})
                self.faq = data.get("faq", [])
                self.packages = data.get("packages", {})
                self.coupons = data.get("coupons", [])
                self.business = data.get("business", {})
            print(f"✅ Knowledge Base loaded: {len(self.services)} services, {len(self.professionals)} professionals")
        except Exception as e:
            print(f"⚠️ Knowledge Base load error: {e}")
    
    def search_services(self, query: str) -> List[dict]:
        """Search services by query"""
        query_lower = query.lower()
        results = []
        
        for service in self.services:
            name = service.get("name", "").lower()
            category = service.get("category", "").lower()
            keywords = service.get("keywords", [])
            
            if query_lower in name or query_lower in category:
                results.append(service)
            elif any(kw in query_lower for kw in keywords):
                results.append(service)
        
        return results
    
    def search_professionals(self, query: str) -> List[dict]:
        """Search professionals by query"""
        query_lower = query.lower()
        results = []
        
        for prof in self.professionals:
            name = prof.get("name", "").lower()
            nickname = prof.get("nickname", "").lower()
            
            if query_lower in name or query_lower in nickname:
                results.append(prof)
        
        return results
    
    def search_faq(self, query: str) -> Optional[dict]:
        """Find matching FAQ"""
        query_lower = query.lower()
        
        for faq_item in self.faq:
            patterns = faq_item.get("patterns", [])
            if any(p.lower() in query_lower for p in patterns):
                return faq_item
        
        return None
    
    def find_coupon(self, text: str) -> Optional[dict]:
        """Find coupon in text"""
        text_upper = text.upper()
        
        for coupon in self.coupons:
            if coupon.get("code", "").upper() in text_upper:
                return coupon
        
        return None
    
    def get_packages(self) -> dict:
        """Get all packages"""
        return self.packages
    
    def get_service_by_id(self, service_id: str) -> Optional[dict]:
        """Get service by ID"""
        for service in self.services:
            if service.get("id") == service_id:
                return service
        return None
    
    def get_professional_by_id(self, prof_id: str) -> Optional[dict]:
        """Get professional by ID"""
        for prof in self.professionals:
            if prof.get("id") == prof_id:
                return prof
        return None
''')
    
    print("\n✅ Brain, Analytics, Campaigns, Knowledge created!")

if __name__ == "__main__":
    main()
