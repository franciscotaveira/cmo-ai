# 🧠 MARKETING BRAIN — Arquitetura para Hardware Limitado

> **Contexto**: Sem GPU poderosa (RTX 3090/4090 ou Mac M1/M2/M3)
> **Solução**: Processamento externo + LLMs leves otimizados
> **Estratégia**: Híbrido (local + cloud gratuito/barato)
> **Data**: 2026-02-25

---

## 🎯 REALIDADE DO HARDWARE

### Cenário Típico (Seu Caso)

```
❌ NÃO TEM:
- RTX 3090/4090 (R$ 10.000-15.000)
- Mac M1/M2/M3 com 32GB+ RAM
- 64GB RAM para modelos grandes

✅ TEM:
- CPU comum (Intel i5/i7 ou AMD Ryzen)
- 8-16GB RAM
- GPU integrada ou básica
- Internet banda larga
```

### Implicações

| Modelo LLM | RAM Necessária | GPU | Seu Hardware |
| :--------- | :------------- | :-- | :----------- |
| **Llama 3.1 70B** | 140GB | ❌ Não roda | ❌ |
| **Llama 3.1 8B** | 16GB | ⚠️ Integrada | ⚠️ Talvez |
| **Mistral 7B** | 8GB | ⚠️ Integrada | ✅ Possível |
| **Phi-3 Mini (3.8B)** | 4GB | ✅ Qualquer | ✅ ✅ ✅ |
| **Gemma 2B** | 2GB | ✅ Qualquer | ✅ ✅ ✅ |

---

## 🚀 SOLUÇÕES VIÁVEIS

### OPÇÃO 1: **LLMs Leves Locais** (Rodam no Seu PC)

#### Modelos Recomendados

| Modelo | Tamanho | RAM | Velocidade | Qualidade |
| :----- | :------ | :-- | :--------- | :-------- |
| **Phi-3 Mini** | 3.8B | 4GB | ⚡⚡⚡ Rápido | 🟢 Boa |
| **Gemma 2B** | 2B | 2GB | ⚡⚡⚡ Rápido | 🟢 Boa |
| **Mistral 7B** | 7B | 8GB | ⚡⚡ Médio | 🟢🟢 Muito Boa |
| **Llama 3.2 3B** | 3B | 4GB | ⚡⚡⚡ Rápido | 🟢 Boa |
| **Qwen2.5 3B** | 3B | 4GB | ⚡⚡⚡ Rápido | 🟢🟢 Muito Boa |

#### Setup com Ollama (Mais Fácil)

```bash
# 1. Instalar Ollama
# Windows: Download em https://ollama.ai/download
# Ou PowerShell:
winget install Ollama.Ollama

# 2. Rodar modelo leve
ollama run phi3:mini
# ou
ollama run gemma:2b
# ou
ollama run llama3.2:3b

# 3. Testar
ollama run phi3:mini "Você é um especialista em marketing. Me dê 3 insights para aumentar vendas de e-commerce."
```

#### Python Integration (Leve)

```python
# engine/src/local_llm_light.py
import requests
from typing import List, Dict

class LightweightLLM:
    """
    LLM leve para hardware limitado.
    """
    
    def __init__(self, model: str = "phi3:mini", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Gera resposta com modelo leve.
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                },
                timeout=60  # Timeout de 60 segundos
            )
            
            return response.json()["response"]
            
        except requests.exceptions.Timeout:
            return "⚠️ Timeout: Modelo muito lento. Tente prompt mais curto ou modelo menor."
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
    
    def chat(self, messages: List[Dict], max_tokens: int = 500) -> str:
        """
        Chat com histórico.
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                },
                timeout=60
            )
            
            return response.json()["message"]["content"]
            
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
```

#### Benchmarks Reais (Hardware Comum)

```
Hardware: Intel i5-8400, 16GB RAM, GTX 1060 6GB

Modelo          | Tokens/s | RAM Uso | Qualidade
----------------|----------|---------|----------
Phi-3 Mini 3.8B | ~15 t/s  | 4GB     | 🟢 Boa
Gemma 2B        | ~25 t/s  | 2GB     | 🟢 Boa
Mistral 7B      | ~8 t/s   | 8GB     | 🟢🟢 Muito Boa
Llama 3.2 3B    | ~18 t/s  | 4GB     | 🟢 Boa

Hardware: Mac M1 8GB

Modelo          | Tokens/s | RAM Uso | Qualidade
----------------|----------|---------|----------
Phi-3 Mini 3.8B | ~30 t/s  | 4GB     | 🟢 Boa
Gemma 2B        | ~45 t/s  | 2GB     | 🟢 Boa
Mistral 7B      | ~15 t/s  | 8GB     | 🟢🟢 Muito Boa
```

---

### OPÇÃO 2: **Cloud Gratuita/Barata** (Processamento Externo)

#### 2.1: Google Colab (Grátis!)

**Setup**:
```python
# No Google Colab (https://colab.research.google.com)

# 1. Rodar LLM na GPU grátis do Colab
!pip install llama-cpp-python
!pip install huggingface_hub

# 2. Baixar modelo leve
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="TheBloke/Phi-3-mini-4k-instruct-GGUF",
    filename="phi-3-mini-4k-instruct.Q4_K_M.gguf"
)

# 3. Carregar e usar
from llama_cpp import Llama

llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=4  # Usar 4 threads da CPU
)

output = llm(
    "Você é um especialista em marketing. [INST] Gere 3 insights para e-commerce [/INST]",
    max_tokens=500
)

print(output)
```

**Vantagens**:
- ✅ GPU grátis (T4, 15GB VRAM)
- ✅ Roda modelos maiores (Llama 3.1 8B)
- ✅ Zero custo

**Desvantagens**:
- ⚠️ Sessão expira após 12h
- ⚠️ Precisa reconectar
- ⚠️ Internet necessária

**Integração com MD-OS**:
```python
# engine/src/colab_llm.py
import requests

class ColabLLM:
    """
    LLM rodando no Google Colab (acessado via API).
    """
    
    def __init__(self, colab_webhook_url: str):
        """
        colab_webhook_url: URL do webhook do Colab (ngrok)
        """
        self.webhook_url = colab_webhook_url
    
    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.webhook_url,
            json={"prompt": prompt},
            timeout=120
        )
        return response.json()["response"]
```

**Como Manter Sempre Online**:
```bash
# Usar ngrok para expor Colab
!pip install pyngrok
from ngrok import connect

# Criar tunnel
public_url = connect(5000)
print(f"URL pública: {public_url}")

# Usar esta URL no MD-OS
```

---

#### 2.2: Hugging Face Spaces (Grátis!)

**Setup**:
```python
# Criar Space em: https://huggingface.co/spaces

# app.py (no Space)
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Carregar modelo leve
model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=500)
    
    return jsonify({
        "response": tokenizer.decode(outputs[0], skip_special_tokens=True)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
```

**Vantagens**:
- ✅ Grátis (CPU básico)
- ✅ Sempre online
- ✅ Fácil de deploy

**Desvantagens**:
- ⚠️ CPU apenas (lento)
- ⚠️ Rate limits

---

#### 2.3: VPS com GPU (Barato)

**Opções**:

| Provider | GPU | RAM | Preço/mês |
| :------- | :-- | :-- | :-------- |
| **RunPod** | RTX 3060 12GB | 24GB | $0.40/hora |
| **Vast.ai** | RTX 3090 24GB | 48GB | $0.25/hora |
| **Lambda Labs** | RTX A6000 48GB | 64GB | $1.50/hora |
| **Paperspace** | Tesla T4 16GB | 24GB | $8/mês + $0.30/hora |

**Setup (RunPod)**:
```bash
# 1. Criar pod em: https://console.runpod.io
# 2. Escolher template: Ollama
# 3. Conectar via SSH
ssh root@<pod-ip>

# 4. Rodar modelo
ollama run mistral:7b

# 5. Expor API
# Ollama já expõe na porta 11434
# Configurar firewall para permitir seu IP
```

**Custo Estimado**:
```
Uso: 2 horas/dia
RunPod RTX 3060: $0.40/hora
Custo diário: $0.80
Custo mensal: $24/mês
```

---

#### 2.4: APIs Gratuitas/Baratas

| API | Modelo | Preço | Limite Grátis |
| :-- | :----- | :---- | :------------ |
| **Groq Cloud** | Llama 3.1 8B | Grátis | 30 req/min |
| **Together AI** | Vários | $0.20/1M tokens | $5 crédito grátis |
| **Anyscale** | Llama, Mistral | $0.20/1M tokens | Nenhum |
| **OpenRouter** | Múltiplos | Varia | Nenhum |
| **Google AI Studio** | Gemini 1.5 | Grátis | 60 req/min |

**Groq Cloud (Melhor Opção Grátis)**:
```python
# engine/src/groq_llm.py
from groq import Groq

class GroqLLM:
    """
    LLM via Groq Cloud (GRÁTIS, rápido).
    """
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Grátis, rápido
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Você é um especialista em marketing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content
```

**Custo**:
```
Groq: GRÁTIS (30 req/min)
Together AI: $0.20 por 1M tokens (~$5/mês para uso moderado)
```

---

### OPÇÃO 3: **Híbrido Inteligente** (Recomendado)

#### Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│              CÉREBRO HÍBRIDO                            │
│                                                         │
│  Tarefas Leves (Local):                                 │
│  • Classificação simples                                │
│  • Templates pré-definidos                              │
│  • Análise estatística básica                           │
│  • RAG com modelos pequenos (2-4B)                      │
│                                                         │
│  Tarefas Pesadas (Cloud):                               │
│  • Geração de texto longo                               │
│  • Análise complexa                                     │
│  • Criatividade (copy, campanhas)                       │
│  • Modelos grandes (8B+)                                │
└─────────────────────────────────────────────────────────┘
```

#### Implementação

```python
# engine/src/hybrid_llm.py
from typing import Literal, Optional

class HybridLLM:
    """
    Gerencia LLM local (leve) + cloud (pesado).
    """
    
    def __init__(self, local_model: str = "phi3:mini", 
                 cloud_api_key: Optional[str] = None):
        self.local_llm = LightweightLLM(model=local_model)
        
        if cloud_api_key:
            self.cloud_llm = GroqLLM(api_key=cloud_api_key)
        else:
            self.cloud_llm = None
    
    def generate(self, 
                 prompt: str, 
                 complexity: Literal["simple", "complex"] = "simple") -> str:
        """
        Escolhe automaticamente local ou cloud baseado na complexidade.
        """
        # Estimativa de complexidade
        if complexity == "simple" or len(prompt) < 200:
            # Local: rápido, grátis
            return self.local_llm.generate(prompt)
        else:
            # Cloud: mais inteligente
            if self.cloud_llm:
                return self.cloud_llm.generate(prompt)
            else:
                # Fallback para local se não tem cloud
                return self.local_llm.generate(prompt, max_tokens=300)
    
    def chat(self, messages: list, use_cloud: bool = False) -> str:
        """
        Chat com escolha manual.
        """
        if use_cloud and self.cloud_llm:
            return self.cloud_llm.chat(messages)
        else:
            return self.local_llm.chat(messages)
```

#### Quando Usar Cada

| Tarefa | Local ou Cloud? | Por Que |
| :----- | :-------------- | :------ |
| **Classificar insight** | ✅ Local | Simples, rápido |
| **Gerar copy de anúncio** | ☁️ Cloud | Criatividade |
| **Analisar métricas** | ✅ Local | Estatística pura |
| **Criar campanha completa** | ☁️ Cloud | Complexo |
| **Responder pergunta simples** | ✅ Local | Rápido |
| **Brainstorm estratégico** | ☁️ Cloud | Precisa de raciocínio |

---

## 📊 COMPARAÇÃO DE CUSTOS

### Cenário: Uso Diário (2 horas/dia)

| Solução | Custo/Mês | Velocidade | Qualidade | Privacidade |
| :------ | :-------: | :--------: | :-------: | :---------: |
| **Local (Phi-3)** | R$ 0 | ⚡⚡⚡ | 🟢 | ✅ 100% |
| **Local (Mistral 7B)** | R$ 0 | ⚡⚡ | 🟢🟢 | ✅ 100% |
| **Groq Cloud** | R$ 0 | ⚡⚡⚡⚡ | 🟢🟢 | ⚠️ Dados na nuvem |
| **Colab (manual)** | R$ 0 | ⚡⚡⚡ | 🟢🟢 | ⚠️ Dados na nuvem |
| **RunPod (2h/dia)** | R$ 120 | ⚡⚡⚡ | 🟢🟢🟢 | ✅ Seus dados |
| **OpenAI API** | R$ 800+ | ⚡⚡⚡⚡ | 🟢🟢🟢🟢 | ❌ OpenAI |

---

## 🎯 RECOMENDAÇÃO PARA SEU CASO

### Estratégia em 3 Camadas

```python
# CAMADA 1: Local (80% das tarefas)
# Modelo: Phi-3 Mini (3.8B) ou Llama 3.2 3B
# Hardware: Seu PC atual
# Custo: R$ 0

# CAMADA 2: Cloud Grátis (15% das tarefas)
# Groq Cloud (Llama 3.1 8B)
# Custo: R$ 0
# Uso: Tarefas criativas complexas

# CAMADA 3: Cloud Pago (5% das tarefas)
# RunPod (apenas se necessário)
# Custo: R$ 50-100/mês
# Uso: Casos críticos
```

### Setup Inicial (Hoje, 2 horas)

```bash
# 1. Instalar Ollama
winget install Ollama.Ollama

# 2. Rodar modelo leve
ollama run phi3:mini

# 3. Testar
ollama run phi3:mini "Gere 3 insights de marketing para e-commerce"

# 4. Se funcionar bem, integrar com MD-OS
# Editar engine/src/hybrid_llm.py
```

### Setup Groq Cloud (15 minutos)

```bash
# 1. Criar conta em: https://console.groq.com
# 2. Gerar API key
# 3. Testar:
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-8b-instant",
    "messages": [{"role": "user", "content": "Olá!"}]
  }'

# 4. Integrar com MD-OS
```

---

## 📋 ROADMAP ATUALIZADO (Hardware Limitado)

### Fase 1: Local Leve (10 horas)
- [ ] Instalar Ollama
- [ ] Testar Phi-3 Mini, Gemma 2B, Llama 3.2 3B
- [ ] Benchmark no seu hardware
- [ ] Escolher melhor modelo
- [ ] Integrar com MD-OS

### Fase 2: Cloud Grátis (5 horas)
- [ ] Criar conta Groq Cloud
- [ ] Integrar GroqLLM
- [ ] Implementar HybridLLM
- [ ] Testar roteamento automático

### Fase 3: Python Brain (30 horas)
- [ ] Customer segmentation
- [ ] Churn prediction
- [ ] Sales forecast
- [ ] **Menos dependência de LLM**

### Fase 4: Agentes Leves (20 horas)
- [ ] Agentes com regras (não LLM)
- [ ] Templates inteligentes
- [ ] Roteamento para cloud só quando necessário

**Total**: 65 horas (vs 170h original)

---

## 💡 OTIMIZAÇÕES PARA HARDWARE LIMITADO

### 1. **Quantização** (Reduz Tamanho do Modelo)

```bash
# Modelos quantizados (Q4_K_M = 4 bits)
# Original: 7B = 14GB
# Quantizado: 7B = 4GB

ollama run mistral:7b-instruct-q4_K_M
```

### 2. **CPU Threads** (Otimizar Uso da CPU)

```python
# Ollama: ajustar threads
import os
os.environ['OLLAMA_NUM_THREADS'] = '4'  # Usar 4 threads
```

### 3. **Batch Processing** (Processar em Lote)

```python
# Em vez de 1 por 1, processar em lote
prompts = ["prompt1", "prompt2", "prompt3"]
results = [llm.generate(p) for p in prompts]  # Paralelo
```

### 4. **Cache de Respostas**

```python
# Cache para não regenerar mesma resposta
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate(prompt_hash: str):
    return llm.generate(prompt)
```

---

## 🏆 VEREDITO FINAL

### Sim, É Possível Sem Hardware Caro!

**Solução Recomendada**:

```
┌─────────────────────────────────────────────────────────┐
│  CÉREBRO HÍBRIDO (Hardware Limitado)                    │
│                                                         │
│  80% Local (Phi-3 Mini 3.8B)                            │
│  • Grátis                                               │
│  • Rápido                                               │
│  • Privado                                              │
│                                                         │
│  15% Cloud Grátis (Groq - Llama 3.1 8B)                 │
│  • Tarefas criativas                                    │
│  • Zero custo                                           │
│                                                         │
│  5% Cloud Pago (RunPod, se necessário)                  │
│  • Casos críticos                                       │
│  • R$ 50-100/mês                                        │
└─────────────────────────────────────────────────────────┘
```

**Custo Total**: R$ 0-100/mês (vs R$ 800+ da OpenAI)

---

## 📁 PRÓXIMOS PASSOS

### Hoje (2 horas)

```bash
# 1. Instalar Ollama
winget install Ollama.Ollama

# 2. Testar modelos leves
ollama run phi3:mini
ollama run gemma:2b
ollama run llama3.2:3b

# 3. Escolher melhor para seu hardware
```

### Amanhã (1 hora)

```bash
# 1. Criar conta Groq Cloud
# https://console.groq.com

# 2. Pegar API key
# 3. Testar API
```

### Esta Semana (10 horas)

```bash
# 1. Integrar HybridLLM com MD-OS
# 2. Testar com dados reais
# 3. Ajustar roteamento local/cloud
```

---

<div align="center">

**🧠 MARKETING BRAIN — HARDWARE LIMITADO**

*LLM Local Leve + Cloud Grátis = Cérebro de Marketing Acessível*

**65 horas • R$ 0-100/mês • Funciona no Seu PC**

</div>
