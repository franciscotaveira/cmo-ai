"""
╔═══════════════════════════════════════════════════════════════════════════════
║ AI INSIGHTS ENGINE — IA Generativa para Marketing (v5.2 — EXOCÓRTEX)
╠═══════════════════════════════════════════════════════════════════════════════
║ Integração com Obsidian Copilot + LLMs para gerar insights automáticos
║ Suporta: OpenAI, Anthropic, Groq, Ollama (local)
╚═══════════════════════════════════════════════════════════════════════════════
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Provedores de LLM suportados."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"
    CUSTOM = "custom"


@dataclass
class AIInsight:
    """Insight gerado por IA."""
    id: str
    title: str
    description: str
    category: str  # anomaly, opportunity, threat, trend, recommendation
    severity: str  # critical, high, medium, low
    confidence: float  # 0-1
    tenant_id: str
    tenant_name: str
    related_metrics: List[str]
    action_items: List[str]
    created_at: str
    llm_provider: str
    model_used: str


@dataclass
class ChatResponse:
    """Resposta de chat com IA."""
    message: str
    sources: List[str]
    confidence: float
    follow_up_questions: List[str]


class AIInsightsEngine:
    """
    Motor de Insights com IA Generativa.

    Integra-se com:
    • Obsidian Copilot (via API do plugin)
    • OpenAI API
    • Anthropic API (Claude)
    • Groq Cloud (grátis, rápido)
    • Ollama (local, privativo)
    """

    # Templates de prompts para diferentes cenários
    PROMPT_TEMPLATES = {
        'analyze_anomaly': """
Você é um especialista em marketing analytics. Analise esta anomalia:

**Métrica**: {metric_name}
**Valor Atual**: {current_value}
**Valor Esperado**: {expected_value}
**Desvio**: {deviation_percent}%
**Z-Score**: {z_score}

**Contexto do Tenant**: {tenant_name} ({tenant_type})

**Histórico (últimos 7 dias)**:
{historical_data}

Gere um insight acionável respondendo:
1. O que causou esta anomalia?
2. Qual o impacto esperado no negócio?
3. Quais ações imediatas devem ser tomadas?
4. Como prevenir no futuro?

Formato da resposta (JSON):
{{
    "title": "Título impactante",
    "description": "Análise detalhada em 2-3 parágrafos",
    "category": "anomaly|opportunity|threat|trend",
    "severity": "critical|high|medium|low",
    "confidence": 0.85,
    "action_items": ["ação 1", "ação 2", "ação 3"]
}}
""",

        'generate_strategy': """
Você é um estrategista de marketing sênior. Crie uma estratégia para:

**Empresa**: {tenant_name} ({tenant_type})

**Métricas Atuais**:
{metrics_table}

**Problemas Identificados**:
{problems_list}

**Benchmarks do Setor**:
{benchmarks}

**Objetivo de Negócio**: {business_goal}

Desenvolva uma estratégia completa incluindo:
1. Diagnóstico situacional
2. Objetivo SMART
3. 3-5 iniciativas estratégicas
4. KPIs de sucesso
5. Timeline de implementação
6. Budget estimado

Formato da resposta (JSON):
{{
    "title": "Nome da estratégia",
    "description": "Estratégia completa em markdown",
    "objectives": ["objetivo 1", "objetivo 2"],
    "initiatives": [
        {{"name": "Iniciativa 1", "description": "...", "owner": "...", "timeline_days": 30}}
    ],
    "kpis": ["KPI 1", "KPI 2"],
    "budget_estimate": 5000,
    "expected_roi": 3.5
}}
""",

        'weekly_report': """
Você é um analista de marketing. Gere um relatório semanal executivo:

**Período**: {start_date} a {end_date}
**Empresa**: {tenant_name}

**Métricas da Semana**:
{metrics_summary}

**Comparação com Semana Anterior**:
{wow_comparison}

**Destaques Positivos**:
{highlights}

**Pontos de Atenção**:
{concerns}

Crie um relatório executivo em formato de newsletter com:
- Resumo em 1 parágrafo
- 3-5 insights principais
- Recomendações para a próxima semana
- Tom profissional mas acessível

Formato da resposta (Markdown):
# Relatório Semanal - {tenant_name}

## 📊 Resumo Executivo
[Resumo em 1 parágrafo]

## 🎯 Insights Principais
[3-5 bullets com insights]

## ⚠️ Pontos de Atenção
[Lista de preocupações]

## 📋 Recomendações
[Ações para próxima semana]
""",

        'content_ideas': """
Você é um especialista em content marketing. Gere ideias de conteúdo para:

**Empresa**: {tenant_name}
**Nicho**: {niche}
**Público-alvo**: {target_audience}
**Objetivo**: {content_goal}

**Palavras-chave Principais**: {keywords}

**Canais**: {channels}

Gere 10 ideias de conteúdo criativas e acionáveis incluindo:
- Título chamativo
- Formato (blog, video, social, email)
- Canal principal
- Briefing em 1 parágrafo
- CTA sugerido

Formato da resposta (JSON):
{{
    "ideas": [
        {{
            "title": "Título",
            "format": "blog|video|social|email|podcast",
            "channel": "instagram|linkedin|youtube|blog|email",
            "briefing": "Descrição do conteúdo",
            "cta": "Call-to-action",
            "estimated_effort": "low|medium|high",
            "expected_impact": "low|medium|high"
        }}
    ]
}}
""",

        'competitor_analysis': """
Você é um analista de inteligência competitiva. Analise:

**Nossa Empresa**: {our_company}
**Métricas Atuais**: {our_metrics}

**Concorrentes**:
{competitors_data}

**Mercado**: {market_context}

Faça uma análise competitiva incluindo:
1. Nossas vantagens competitivas
2. Nossas desvantagens
3. Oportunidades não exploradas pelos concorrentes
4. Ameaças emergentes
5. Recomendações estratégicas

Formato da resposta (JSON):
{{
    "strengths": ["força 1", "força 2"],
    "weaknesses": ["fraqueza 1", "fraqueza 2"],
    "opportunities": ["oportunidade 1", "oportunidade 2"],
    "threats": ["ameaça 1", "ameaça 2"],
    "recommendations": ["recomendação 1", "recomendação 2"]
}}
"""
    }

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.GROQ,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        obsidian_copilot_enabled: bool = False
    ):
        """
        Inicializa o AI Insights Engine.

        Args:
            llm_provider: Provedor de LLM preferido
            api_key: API key do provedor
            model: Modelo específico (opcional)
            obsidian_copilot_enabled: Se Copilot do Obsidian está disponível
        """
        self.llm_provider = llm_provider
        self.api_key = api_key or self._get_api_key_from_env(llm_provider)
        
        # Estratégia de dois níveis para economia
        self.support_model = model or os.getenv("SUPPORT_MODEL") or self._get_default_model(llm_provider, tier="support")
        self.primary_model = os.getenv("PRIMARY_MODEL") or self._get_default_model(llm_provider, tier="primary")
        
        self.obsidian_copilot_enabled = obsidian_copilot_enabled

        # Configurações específicas por provedor
        self.provider_configs = {
            LLMProvider.OPENAI: {
                'base_url': 'https://api.openai.com/v1',
                'default_model': 'gpt-3.5-turbo',
                'max_tokens': 2000
            },
            LLMProvider.ANTHROPIC: {
                'base_url': 'https://api.anthropic.com',
                'default_model': 'claude-3-haiku-20240307',
                'max_tokens': 2000
            },
            LLMProvider.GROQ: {
                'base_url': 'https://api.groq.com/openai/v1',
                'default_model': 'llama-3.1-70b-versatile',
                'max_tokens': 2000
            },
            LLMProvider.OLLAMA: {
                'base_url': 'http://localhost:11434',
                'default_model': 'llama3.1:8b',
                'max_tokens': 2000
            },
            LLMProvider.OPENROUTER: {
                'base_url': 'https://openrouter.ai/api/v1',
                'support_model': 'google/gemini-flash-1.5',
                'primary_model': 'openai/gpt-4-turbo',
                'max_tokens': 4000
            }
        }

        logger.info(f"🤖 AIInsightsEngine inicializado (Smart Routing: {self.support_model} / {self.primary_model})")

    def _get_api_key_from_env(self, provider: LLMProvider) -> Optional[str]:
        """Obtém API key do ambiente."""
        env_keys = {
            LLMProvider.OPENAI: 'OPENAI_API_KEY',
            LLMProvider.ANTHROPIC: 'ANTHROPIC_API_KEY',
            LLMProvider.GROQ: 'GROQ_API_KEY',
            LLMProvider.OPENROUTER: 'OPENROUTER_API_KEY',
            LLMProvider.OLLAMA: None  # Local, não precisa de key
        }

        env_key = env_keys.get(provider)
        if env_key:
            return os.getenv(env_key)
        return None

    def _get_default_model(self, provider: LLMProvider, tier: str = "support") -> str:
        """Obtém modelo padrão baseado no nível (tier)."""
        models = {
            LLMProvider.OPENAI: {
                'support': 'gpt-3.5-turbo',
                'primary': 'gpt-4-turbo'
            },
            LLMProvider.GROQ: {
                'support': 'llama-3.1-8b-instant',
                'primary': 'llama-3.1-70b-versatile'
            },
            LLMProvider.OPENROUTER: {
                'support': 'google/gemini-flash-1.5',
                'primary': 'openai/gpt-4-turbo'
            },
            LLMProvider.OLLAMA: {
                'support': 'llama3.1:8b',
                'primary': 'llama3.1:8b'
            }
        }
        provider_models = models.get(provider, models[LLMProvider.OPENAI])
        return provider_models.get(tier, provider_models['support'])

    def generate_insight_from_anomaly(
        self,
        metric_key: str,
        current_value: float,
        expected_value: float,
        z_score: float,
        tenant_name: str,
        tenant_type: str,
        historical_data: List[Dict[str, Any]]
    ) -> AIInsight:
        """
        Gera insight automático a partir de anomalia.

        Args:
            metric_key: Chave da métrica
            current_value: Valor atual
            expected_value: Valor esperado/benchmark
            z_score: Z-Score da anomalia
            tenant_name: Nome do tenant
            tenant_type: Tipo de negócio
            historical_data: Dados históricos

        Returns:
            AIInsight: Insight gerado
        """
        # Calcular desvio percentual
        deviation_percent = ((current_value - expected_value) / expected_value * 100) if expected_value > 0 else 0

        # Formatar dados históricos
        historical_str = "\n".join([
            f"  {d.get('date', 'N/A')}: {d.get('value', 0):.2f}"
            for d in historical_data[-7:]
        ])

        # Determinar severidade
        if abs(z_score) > 3:
            severity = 'critical'
        elif abs(z_score) > 2:
            severity = 'high'
        elif abs(z_score) > 1.5:
            severity = 'medium'
        else:
            severity = 'low'

        # Determinar categoria baseada na direção
        if 'cac' in metric_key.lower() and current_value > expected_value:
            category = 'threat'
        elif 'conversion' in metric_key.lower() and current_value < expected_value:
            category = 'threat'
        elif 'revenue' in metric_key.lower() and current_value > expected_value:
            category = 'opportunity'
        else:
            category = 'anomaly'

        # Preparar prompt
        prompt = self.PROMPT_TEMPLATES['analyze_anomaly'].format(
            metric_name=metric_key.replace('_', ' ').title(),
            current_value=f"{current_value:,.2f}",
            expected_value=f"{expected_value:,.2f}",
            deviation_percent=f"{deviation_percent:.1f}",
            z_score=f"{z_score:.2f}",
            tenant_name=tenant_name,
            tenant_type=tenant_type.title(),
            historical_data=historical_str
        )

        # Chamar LLM
        response = self._call_llm(prompt, json_response=True)

        # Parse da resposta
        try:
            if isinstance(response, str):
                insight_data = json.loads(response)
            else:
                insight_data = response
        except:
            # Fallback se não conseguir parsear JSON
            insight_data = {
                'title': f'Anomalia em {metric_key.replace("_", " ").title()}',
                'description': response if isinstance(response, str) else str(response),
                'category': category,
                'severity': severity,
                'confidence': 0.7,
                'action_items': ['Investigar causa raiz', 'Monitorar evolução']
            }

        insight = AIInsight(
            id=f"insight-{metric_key}-{tenant_name}-{datetime.now().strftime('%Y%m%d%H%M')}",
            title=insight_data.get('title', 'Insight'),
            description=insight_data.get('description', ''),
            category=insight_data.get('category', category),
            severity=insight_data.get('severity', severity),
            confidence=insight_data.get('confidence', 0.7),
            tenant_id=tenant_name.lower().replace(' ', '-'),
            tenant_name=tenant_name,
            related_metrics=[metric_key],
            action_items=insight_data.get('action_items', []),
            created_at=datetime.now().isoformat(),
            llm_provider=self.llm_provider.value,
            model_used=self.model
        )

        logger.info(f"💡 Insight gerado: {insight.title}")
        return insight

    def generate_weekly_report(
        self,
        tenant_name: str,
        metrics_summary: Dict[str, float],
        wow_comparison: Dict[str, float],
        start_date: str,
        end_date: str
    ) -> str:
        """
        Gera relatório semanal com IA.

        Args:
            tenant_name: Nome do tenant
            metrics_summary: Resumo de métricas
            wow_comparison: Comparação semana anterior
            start_date: Data inicial
            end_date: Data final

        Returns:
            str: Relatório em Markdown
        """
        # Formatar métricas
        metrics_table = "\n".join([
            f"- **{k.replace('_', ' ').title()}**: {v:,.2f}"
            for k, v in metrics_summary.items()
        ])

        # Formatar comparação
        wow_str = "\n".join([
            f"- **{k.replace('_', ' ').title()}**: {v:+.1f}%"
            for k, v in wow_comparison.items()
        ])

        # Identificar highlights e concerns
        highlights = [
            f"{k.replace('_', ' ').title()} cresceu {v:.1f}%"
            for k, v in wow_comparison.items() if v > 5
        ]
        concerns = [
            f"{k.replace('_', ' ').title()} caiu {abs(v):.1f}%"
            for k, v in wow_comparison.items() if v < -5
        ]

        # Preparar prompt
        prompt = self.PROMPT_TEMPLATES['weekly_report'].format(
            start_date=start_date,
            end_date=end_date,
            tenant_name=tenant_name,
            metrics_summary=metrics_table,
            wow_comparison=wow_str,
            highlights="\n".join(highlights) if highlights else "Nenhum destaque significativo",
            concerns="\n".join(concerns) if concerns else "Nenhum ponto de atenção crítico"
        )

        # Chamar LLM usando o Support Model (Economia)
        report = self._call_llm(prompt, json_response=False, tier="support")

        logger.info(f"📰 Relatório semanal gerado para {tenant_name}")
        return report

    def generate_content_ideas(
        self,
        tenant_name: str,
        niche: str,
        target_audience: str,
        content_goal: str,
        keywords: List[str],
        channels: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Gera ideias de conteúdo com IA.

        Args:
            tenant_name: Nome do tenant
            niche: Nicho de mercado
            target_audience: Público-alvo
            content_goal: Objetivo do conteúdo
            keywords: Palavras-chave
            channels: Canais de distribuição

        Returns:
            Lista de ideias de conteúdo
        """
        # Preparar prompt
        prompt = self.PROMPT_TEMPLATES['content_ideas'].format(
            tenant_name=tenant_name,
            niche=niche,
            target_audience=target_audience,
            content_goal=content_goal,
            keywords=", ".join(keywords),
            channels=", ".join(channels)
        )

        # Chamar LLM
        response = self._call_llm(prompt, json_response=True)

        # Parse da resposta
        try:
            if isinstance(response, str):
                data = json.loads(response)
            else:
                data = response
            ideas = data.get('ideas', [])
        except:
            ideas = []
            logger.warning("⚠️ Não foi possível parsear ideias de conteúdo")

        logger.info(f"💡 {len(ideas)} ideias de conteúdo geradas")
        return ideas

    def chat_with_context(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        vault_context: Optional[List[str]] = None
    ) -> ChatResponse:
        """
        Responde pergunta com contexto RAG.

        Args:
            question: Pergunta do usuário
            context: Contexto adicional (métricas, tenant info)
            vault_context: Trechos relevantes do vault Obsidian

        Returns:
            ChatResponse: Resposta com fontes
        """
        # Construir prompt com contexto
        system_prompt = """Você é um assistente de marketing especializado.
Responda de forma clara, acionável e baseada em dados.
Sempre que possível, inclua exemplos práticos e métricas."""

        context_str = ""
        if context:
            context_str += "\n\n**Contexto do Tenant:**\n"
            for k, v in context.items():
                context_str += f"- {k}: {v}\n"

        if vault_context:
            context_str += "\n\n**Informações do Vault:**\n"
            context_str += "\n".join(vault_context[:5])  # Top 5 trechos relevantes

        full_prompt = f"{system_prompt}\n{context_str}\n\n**Pergunta:** {question}"

        # Chamar LLM
        response = self._call_llm(full_prompt, json_response=False)

        # Gerar perguntas de follow-up
        follow_up_prompt = f"""Baseado na resposta abaixo, gere 3 perguntas de follow-up relevantes:

Resposta: {response[:500]}...

Formato: JSON array de strings"""

        try:
            follow_up_response = self._call_llm(follow_up_prompt, json_response=True)
            if isinstance(follow_up_response, str):
                follow_up = json.loads(follow_up_response)
            else:
                follow_up = follow_up_response
            follow_up_questions = follow_up if isinstance(follow_up, list) else []
        except (json.JSONDecodeError, KeyError, TypeError):
            follow_up_questions = []

        return ChatResponse(
            message=response,
            sources=vault_context or [],
            confidence=0.85,
            follow_up_questions=follow_up_questions[:3]
        )

    def _call_llm(self, prompt: str, json_response: bool = False, tier: str = "support") -> Any:
        """
        Chama LLM do provedor configurado com lógica de tiering.
        """
        # Escolher o modelo baseado no tier
        model = self.primary_model if tier == "primary" else self.support_model

        if self.llm_provider == LLMProvider.GROQ:
            return self._call_groq(prompt, json_response, model)
        elif self.llm_provider == LLMProvider.OPENAI:
            return self._call_openai(prompt, json_response, model)
        elif self.llm_provider == LLMProvider.OPENROUTER:
            return self._call_openrouter(prompt, json_response, model)
        elif self.llm_provider == LLMProvider.OLLAMA:
            return self._call_ollama(prompt, json_response, model)
        else:
            raise ValueError(f"Provedor não suportado: {self.llm_provider}")

    def _call_groq(self, prompt: str, json_response: bool = False, model: Optional[str] = None) -> Any:
        """Chama Groq API."""
        try:
            import requests
            model_to_use = model or self.support_model

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'model': model_to_use,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': self.provider_configs[LLMProvider.GROQ]['max_tokens']
            }

            if json_response:
                payload['response_format'] = {'type': 'json_object'}

            response = requests.post(
                f"{self.provider_configs[LLMProvider.GROQ]['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            if json_response:
                return json.loads(content)
            return content

        except Exception as e:
            logger.error(f"❌ Erro Groq: {e}")
            return {"error": str(e)}

    def _call_openai(self, prompt: str, json_response: bool = False, model: Optional[str] = None) -> Any:
        """Chama OpenAI API."""
        try:
            import requests
            model_to_use = model or self.support_model

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'model': model_to_use,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': self.provider_configs[LLMProvider.OPENAI]['max_tokens']
            }

            if json_response:
                payload['response_format'] = {'type': 'json_object'}

            response = requests.post(
                f"{self.provider_configs[LLMProvider.OPENAI]['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            if json_response:
                return json.loads(content)
            return content

        except Exception as e:
            logger.error(f"❌ Erro OpenAI: {e}")
            return {"error": str(e)}

    def _call_anthropic(self, prompt: str, json_response: bool = False, model: Optional[str] = None) -> Any:
        """Chama Anthropic API."""
        try:
            import requests
            model_to_use = model or self.support_model

            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }

            payload = {
                'model': model_to_use,
                'max_tokens': self.provider_configs[LLMProvider.ANTHROPIC]['max_tokens'],
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            }

            response = requests.post(
                f"{self.provider_configs[LLMProvider.ANTHROPIC]['base_url']}/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            content = result['content'][0]['text']

            if json_response:
                return json.loads(content)
            return content

        except Exception as e:
            logger.error(f"❌ Erro Anthropic: {e}")
            return {"error": str(e)}

    def _call_openrouter(self, prompt: str, json_response: bool = False, model: Optional[str] = None) -> Any:
        """Chama OpenRouter API (OpenAI-compatible)."""
        try:
            import requests
            model_to_use = model or self.support_model

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://antigravity.mct.com.br', # Requisito OpenRouter
                'X-Title': 'CMO 360 Marketing Engine'
            }

            payload = {
                'model': model_to_use,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': self.provider_configs[LLMProvider.OPENROUTER]['max_tokens']
            }

            if json_response:
                # OpenRouter passa o formato de resposta se o modelo suportar
                payload['response_format'] = {'type': 'json_object'}

            response = requests.post(
                f"{self.provider_configs[LLMProvider.OPENROUTER]['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=45
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            if json_response:
                try:
                    return json.loads(content)
                except (json.JSONDecodeError, KeyError):
                    # Se falhar o parse direto, tentar extrair JSON do texto
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    return {"error": "Failed to parse JSON from AI response"}
            return content

        except Exception as e:
            logger.error(f"❌ Erro OpenRouter: {e}")
            return {"error": str(e)}

    def _call_ollama(self, prompt: str, json_response: bool = False, model: Optional[str] = None) -> Any:
        """Chama Ollama local."""
        try:
            import requests
            model_to_use = model or self.support_model

            payload = {
                'model': model_to_use,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'num_predict': self.provider_configs[LLMProvider.OLLAMA]['max_tokens']
                }
            }

            if json_response:
                payload['format'] = 'json'

            response = requests.post(
                f"{self.provider_configs[LLMProvider.OLLAMA]['base_url']}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result['response']

            if json_response:
                return json.loads(content)
            return content

        except Exception as e:
            logger.error(f"❌ Erro Ollama: {e}")
            return {"error": str(e)}

    def write_insights_to_obsidian(
        self,
        insights: List[AIInsight],
        tenant_name: str,
        obsidian_path: str
    ) -> str:
        """
        Escreve insights no Obsidian.

        Args:
            insights: Lista de insights gerados
            tenant_name: Nome do tenant
            obsidian_path: Caminho para o vault

        Returns:
            Caminho do arquivo criado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Estrutura de pastas
        insights_path = os.path.join(
            obsidian_path,
            "🧠 EXOCÓRTEX",
            "08 - AI Insights",
            tenant_name
        )
        os.makedirs(insights_path, exist_ok=True)

        content = f"""---
tags: [ai-insights, {tenant_name.lower().replace(' ', '_')}, exocortex]
criado: {timestamp}
---

# 🤖 AI Insights - {tenant_name}

**Gerado em:** {timestamp}

**IA Utilizada:** {self.llm_provider.value} ({self.model})

---

## 📊 Insights Gerados

"""

        # Agrupar por severidade
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_insights = sorted(insights, key=lambda x: severity_order.get(x.severity, 4))

        for insight in sorted_insights:
            severity_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(insight.severity, '⚪')
            category_icon = {'anomaly': '⚠️', 'opportunity': '💡', 'threat': '🚨', 'trend': '📈', 'recommendation': '💭'}.get(insight.category, '📌')

            content += f"""
### {severity_icon} {category_icon} {insight.title}

**Confiança:** {insight.confidence:.0%} | **Métricas:** {', '.join(insight.related_metrics)}

{insight.description}

**Ações Recomendadas:**
"""
            for i, action in enumerate(insight.action_items, 1):
                content += f"{i}. [ ] {action}\n"

            content += "\n---\n"

        content += f"""
---

## 📈 Dataview Queries

### Todos os Insights

```dataview
TABLE severity as "Severidade", confidence as "Confiança", created_at as "Data"
FROM "🧠 EXOCÓRTEX/08 - AI Insights/{tenant_name}"
WHERE contains(tags, "ai-insights")
SORT created_at DESC
```

### Insights Críticos

```dataview
LIST
FROM "🧠 EXOCÓRTEX/08 - AI Insights/{tenant_name}"
WHERE severity = "critical" AND status != "resolved"
SORT created_at DESC
```

---

*Gerado automaticamente pelo Exocórtex v5.2 — AI Insights Engine*
"""

        # Salvar arquivo
        safe_name = tenant_name.replace('/', '_').replace('\\', '_')
        filename = f"AI-Insights-{safe_name}-{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(insights_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"🤖 Insights escritos no Obsidian: {filepath}")
        return filepath

    def generate_insights_for_all_tenants(
        self,
        tenants_data: List[Dict[str, Any]],
        anomalies: List[Dict[str, Any]],
        obsidian_path: str
    ) -> Dict[str, str]:
        """
        Gera insights para todos os tenants.

        Args:
            tenants_data: Lista de tenants
            anomalies: Lista de anomalias detectadas
            obsidian_path: Caminho para o vault

        Returns:
            Dicionário {tenant_name: filepath}
        """
        results = {}

        for tenant in tenants_data:
            tenant_name = tenant.get('name', 'Unknown')
            tenant_id = tenant.get('id', 'unknown')
            tenant_type = tenant.get('type', 'default')

            # Filtrar anomalias deste tenant
            tenant_anomalies = [a for a in anomalies if a.get('tenant_id') == tenant_id]

            # Gerar insights para cada anomalia
            insights = []
            for anomaly in tenant_anomalies[:5]:  # Máximo 5 insights por tenant
                try:
                    insight = self.generate_insight_from_anomaly(
                        metric_key=anomaly.get('metric_key', 'unknown'),
                        current_value=anomaly.get('current_value', 0),
                        expected_value=anomaly.get('expected_value', 0),
                        z_score=anomaly.get('z_score', 0),
                        tenant_name=tenant_name,
                        tenant_type=tenant_type,
                        historical_data=anomaly.get('historical_data', [])
                    )
                    insights.append(insight)
                except Exception as e:
                    logger.error(f"❌ Erro ao gerar insight: {e}")

            if insights:
                # Escrever no Obsidian
                filepath = self.write_insights_to_obsidian(
                    insights=insights,
                    tenant_name=tenant_name,
                    obsidian_path=obsidian_path
                )
                results[tenant_name] = filepath

        return results
