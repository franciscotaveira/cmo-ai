---
description: How to design Premium Personas and System Prompts for AI Agents
---

# Premium Persona Prompting Workflow

Based on the learnings from Luna v2 (Haven Receptionist), this workflow outlines the structural best practices for creating a high-converting, safe, and consultative AI agent prompt.

## 1. Distinct Persona & Mission

Start your system prompt by clearly defining WHO the agent is, WHERE they work, and WHAT their ultimate goal is.

```markdown
Você é a Luna, assistente especializada em beleza no Instituto X.
Sua missão é transformar cada conversa em uma experiência consultiva premium.
```

## 2. Inviolable Golden Rules (Guardrails)

Place safety and behavioral rules explicitly at the top. The LLM prioritizes early instructions.

- **Safety First**: Mandate questions about allergies, recent chemicals, or medical conditions before allowing the agent to book a service.
- **Tone & Length**: Enforce brevity (e.g., "Maximum 2-4 lines per response", "Max 2 emojis").
- **Treatment**: Define the exact pronoun usage (e.g., "Always use 'você', never 'senhora'").

## 3. The Multi-Step Consultation Flow

Don't just tell the agent to "be helpful". Give it a structured flowchart of how a conversation *should* progress.

```markdown
ETAPA 1: Saudação e Entender Necessidade (Descubra se é evento urgente ou manutenção)
ETAPA 2: Sugerir Soluções (Apresente no máximo 2 opções claras)
ETAPA 3: Validar Segurança (Para serviços químicos, faça as 3 perguntas obrigatórias)
ETAPA 4: Agendamento (Pergunte o melhor dia e consulte a ferramenta)
```

## 4. Define Tool Usage Explicitly

If your agent uses Autonomous Tool Use, document *exactly* when to use each tool in the prompt.

```markdown
- USE a ferramenta `verificar_disponibilidade` assim que o cliente perguntar horários.
- NUNCA use `criar_agendamento` antes de confirmar o horário com o cliente.
```

## 5. Upsell Strategy (Contextual Value)

Instead of forcing the agent to sell aggressively, teach it *Contextual Upselling*.

- Establish a rule: "Only 1 upsell attempt per conversation."
- Tie upsells to context: "If they schedule a basic haircut, suggest the deep hydration add-on."

## 6. Formatting Instructions (JSON vs Text)

If the agent is part of an orchestrated system (like Mothership Core), force it to return a structured JSON response so the backend can parse its internal "thoughts" versus its public "reply".

```markdown
Responda SEMPRE em JSON:
{
  "thinking": "sua lógica interna antes de responder",
  "mensagem_resposta": "o que o usuário final vai ler",
  "campos_extraidos": { "nome": "...", "telefone": "..." }
}
```

## Conclusion

A premium prompt isn't just a list of facts. It is an operational manual that dictates tone, prevents legal/safety liabilities, and forces a structured sales conversion funnel.
