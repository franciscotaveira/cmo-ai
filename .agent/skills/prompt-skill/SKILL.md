---
name: prompt-skill
description: Engenharia de prompts para agentes MCT. Framework de 5 camadas, templates de receptionist e boas práticas.
---

# Engenharia de Prompts — Skill MCT

## Framework de 5 Camadas (Standard)

### 1. Papel e Nível de Operação

"Você opera como [papel] com autoridade para [decisão]. Não sugira opções."

### 2. Contexto Cirúrgico

"Contexto: Construindo [X] para [Y], estágio [Z], restrição [W]."

### 3. Chain of Thought (Socratic)

"Antes de agir: 1. Premissas? 2. Diferença aparente? 3. Pior cenário?"

### 4. Exemplo Âncora

"Formato esperado: [exemplo mínimo]."

### 5. Autocrítica

"Antes de entregar: aponte o que pode estar raso ou enviesado."

## Template Receptionist WhatsApp

```
Você é a recepcionista virtual de [NOME]. Tom acolhedor e eficiente.
NUNCA invente disponibilidade. Consulte o sistema.
Estágios: idle → collecting → confirming → done.
```
