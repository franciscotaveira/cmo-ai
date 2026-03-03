"""
╔═══════════════════════════════════════════════════════════════════════════════
║ AI ENGINE — Motor de Inteligência Artificial
╠═══════════════════════════════════════════════════════════════════════════════
║ Gera insights estratégicos com RAG
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional

from dotenv import load_dotenv

from .database import DatabaseHandler

load_dotenv()
logger = logging.getLogger(__name__)


class AIEngine:
    """Motor de IA para geração de insights."""
    
    def __init__(self, db: DatabaseHandler, provider: str = "openai"):
        self.db = db
        self.provider = provider
        self.client = None
        self.model = ""
        
        if provider == "openai":
            self._init_openai()
        elif provider == "gemini":
            self._init_gemini()
        else:
            logger.warning(f"⚠️ Provider desconhecido: {provider}, usando OpenAI")
            self._init_openai()
    
    def _init_openai(self):
        """Inicializa cliente OpenAI."""
        try:
            from openai import OpenAI
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("⚠️ OPENAI_API_KEY não encontrada")
                return
            
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4-turbo-preview"
            
            logger.info(f"✅ OpenAI inicializada (modelo: {self.model})")
            
        except ImportError:
            logger.error("❌ openai não instalado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar OpenAI: {e}")
    
    def _init_gemini(self):
        """Inicializa cliente Gemini."""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("⚠️ GEMINI_API_KEY não encontrada")
                return
            
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-pro')
            self.model = "gemini-pro"
            
            logger.info(f"✅ Gemini inicializado (modelo: {self.model})")
            
        except ImportError:
            logger.error("❌ google-generativeai não instalado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Gemini: {e}")
    
    def generate_strategic_insight(self, tenant_id: str, tenant_name: str,
                                   question: Optional[str] = None,
                                   metrics: Optional[List[Dict[str, Any]]] = None,
                                   auto_save: bool = True) -> Dict[str, Any]:
        """Gera um insight estratégico baseado nos dados do tenant."""
        # Recuperar contexto do RAG
        context_chunks = self._retrieve_context(tenant_id)
        
        # Construir prompt
        prompt = self._build_insight_prompt(
            tenant_name=tenant_name,
            question=question,
            metrics=metrics,
            context_chunks=context_chunks
        )
        
        # Gerar resposta com IA
        response = self._generate_response(prompt)
        
        insight = {
            "tenant_id": tenant_id,
            "context": question or "Análise estratégica automática",
            "ai_response": response,
            "source_model": self.model,
            "context_used": len(context_chunks)
        }
        
        if auto_save:
            insight_id = self.db.insert_insight(**insight)
            insight["id"] = insight_id
        
        logger.info(f"💡 Insight gerado para {tenant_name}")
        
        return insight
    
    def analyze_metrics_anomaly(self, tenant_id: str, tenant_name: str,
                               current_metrics: List[Dict[str, Any]],
                               historical_metrics: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Analisa anomalias nas métricas e gera alertas."""
        prompt = f"""Você é um analista de marketing sênior especializado em detecção de anomalias.

EMPRESA: {tenant_name}

MÉTRICAS ATUAIS:
{self._format_metrics(current_metrics)}

"""
        
        if historical_metrics:
            prompt += f"""
MÉTRICAS HISTÓRICAS (para comparação):
{self._format_metrics(historical_metrics)}

"""
        
        prompt += """
IDENTIFIQUE:
1. Quedas bruscas de performance (>20% vs período anterior)
2. Picos anormais de custo
3. Tendências preocupantes
4. Oportunidades não exploradas

Para cada anomalia encontrada, explique:
- O que está acontecendo
- Possível causa
- Ação recomendada
- Urgência (Baixa, Média, Alta)

Seja direto e prático. Use formatação Markdown."""
        
        response = self._generate_response(prompt)
        
        analysis = {
            "tenant_id": tenant_id,
            "context": "Análise de anomalias nas métricas",
            "ai_response": response,
            "source_model": self.model,
            "metrics_analyzed": len(current_metrics)
        }
        
        insight_id = self.db.insert_insight(**analysis)
        analysis["id"] = insight_id
        
        logger.info(f"🔍 Análise de anomalias gerada para {tenant_name}")
        
        return analysis
    
    def generate_marketing_campaign(self, tenant_id: str, tenant_name: str,
                                   campaign_type: str, target_audience: str,
                                   budget: Optional[float] = None) -> Dict[str, Any]:
        """Gera uma campanha de marketing completa."""
        context_chunks = self._retrieve_context(tenant_id)
        
        prompt = f"""Você é um estrategista de marketing sênior com 20 anos de experiência.

EMPRESA: {tenant_name}

CONTEXTO DO NEGÓCIO:
{chr(10).join([chunk['content_chunk'][:200] + '...' for chunk in context_chunks[:3]])}

DADOS DA CAMPANHA:
- Tipo: {campaign_type}
- Público-alvo: {target_audience}
- Orçamento: R$ {budget:,.2f} if budget else 'Não especificado'

GERE UMA CAMPANHA COMPLETA INCLUINDO:

1. **Nome da Campanha** (criativo e memorável)

2. **Objetivo Principal** (SMART)

3. **Público-Alvo Detalhado** (persona)

4. **Canais Recomendados** (com justificativa)

5. **Cronograma** (timeline de execução)

6. **Orçamento Sugerido** (alocação por canal)

7. **Métricas de Sucesso** (KPIs)

8. **Riscos e Mitigações**

9. **Próximos Passos Imediatos**

Use formatação Markdown. Seja prático e acionável."""
        
        response = self._generate_response(prompt)
        
        campaign = {
            "tenant_id": tenant_id,
            "context": f"Campanha de {campaign_type} para {target_audience}",
            "ai_response": response,
            "source_model": self.model,
            "campaign_type": campaign_type
        }
        
        insight_id = self.db.insert_insight(**campaign)
        campaign["id"] = insight_id
        
        logger.info(f"🎯 Campanha gerada: {tenant_name}")
        
        return campaign
    
    def _retrieve_context(self, tenant_id: str, max_chunks: int = 5) -> List[Dict[str, Any]]:
        """Recupera chunks de conhecimento relevantes do banco."""
        try:
            response = self.db.client.table("knowledge_base")\
                .select("id, content_chunk, metadata")\
                .eq("tenant_id", tenant_id)\
                .order("created_at", desc=True)\
                .limit(max_chunks)\
                .execute()
            
            chunks = response.data if response.data else []
            logger.debug(f"📚 {len(chunks)} chunks de contexto recuperados")
            
            return chunks
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar contexto: {e}")
            return []
    
    def _build_insight_prompt(self, tenant_name: str, question: Optional[str],
                             metrics: Optional[List[Dict[str, Any]]],
                             context_chunks: List[Dict[str, Any]]) -> str:
        """Constrói o prompt para geração de insights."""
        prompt = f"""Você é um consultor estratégico de marketing sênior.

EMPRESA: {tenant_name}

"""
        
        if context_chunks:
            prompt += "CONTEXTO DO NEGÓCIO:\n"
            for i, chunk in enumerate(context_chunks, 1):
                prompt += f"[{i}] {chunk['content_chunk'][:300]}...\n"
            prompt += "\n"
        
        if metrics:
            prompt += f"""MÉTRICAS ATUAIS:
{self._format_metrics(metrics)}

"""
        
        if question:
            prompt += f"PERGUNTA: {question}\n"
        else:
            prompt += """PERGUNTA: Com base nos dados acima, quais são as 3 ações mais importantes que esta empresa deveria tomar NOS PRÓXIMOS 7 DIAS?

Para cada ação, inclua:
1. O que fazer (específico)
2. Por que fazer (justificativa baseada em dados)
3. Como fazer (passos práticos)
4. Resultado esperado (métrica de sucesso)

"""
        
        prompt += """
Seja direto, prático e baseado em dados. Use formatação Markdown."""
        
        return prompt
    
    def _generate_response(self, prompt: str) -> str:
        """Gera uma resposta usando o modelo de IA configurado."""
        if not self.client:
            return "⚠️ IA não configurada. Verifique as chaves de API no .env"
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Você é um consultor estratégico de marketing sênior, prático e direto ao ponto."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.provider == "gemini":
                response = self.client.generate_content(prompt)
                return response.text
            
            else:
                return "⚠️ Provider de IA não suportado"
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta da IA: {e}")
            return f"⚠️ Erro ao gerar resposta: {str(e)}"
    
    def _format_metrics(self, metrics: List[Dict[str, Any]]) -> str:
        """Formata métricas para exibição no prompt."""
        if not metrics:
            return "Nenhuma métrica disponível"
        
        formatted = ""
        for metric in metrics[:20]:
            key = metric.get('metric_key', 'unknown')
            value = metric.get('metric_value', 0)
            date_ref = metric.get('date_ref', 'N/A')
            
            value_str = f"{value:,.2f}" if isinstance(value, float) and value >= 1000 else str(value)
            formatted += f"- {key.replace('_', ' ').title()}: {value_str} ({date_ref})\n"
        
        return formatted
    
    def health_check(self) -> bool:
        """Verifica se a IA está configurada e saudável."""
        if not self.client:
            return False
        
        try:
            response = self._generate_response("Responda apenas 'OK' se estiver funcionando.")
            return "OK" in response
        except:
            return False
