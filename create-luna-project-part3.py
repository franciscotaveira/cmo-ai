#!/usr/bin/env python3
"""
LUNA OS Project Creator - Part 3
Creates haven.json (Knowledge Base) and frontend files
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
    print("\n🌙 Creating LUNA OS v2.0 - Part 3 (Knowledge Base & Frontend)...\n")
    
    # ========== backend/app/knowledge/data/haven.json ==========
    haven_data = {
        "business": {
            "name": "Haven Escovaria & Esmalteria",
            "address": {
                "street": "Rua Mato Grosso, 837E",
                "neighborhood": "Jardim Itália",
                "city": "Chapecó",
                "state": "SC"
            },
            "hours": {
                "weekdays": "08:00-20:00",
                "saturday": "08:00-20:00",
                "sunday": "closed",
                "note": "Sem pausa para almoço"
            },
            "parking": "Estacionamento em frente + 4 vagas na esquina",
            "coordinates": {
                "lat": -27.0922,
                "lng": -52.6158
            }
        },
        
        "professionals": [
            {
                "id": "ju",
                "name": "Yujaira",
                "nickname": "Ju",
                "specialties": ["cabelo", "penteados", "tranças", "cor"],
                "services": ["escova_lisa", "escova_modelada", "penteados", "progressiva", "tintura", "tratamentos"],
                "notes": "Especialista em penteados. Referência para tranças."
            },
            {
                "id": "carla",
                "name": "Carla",
                "specialties": ["progressiva", "cabelo"],
                "services": ["escova_lisa", "escova_modelada_babyliss", "progressiva", "tratamentos"],
                "restrictions": ["Não faz penteados", "Não faz tranças", "Modelada só no babyliss"],
                "dual_role": True,
                "notes": "Também atende no Spa. Especialista em progressiva."
            },
            {
                "id": "mariana",
                "name": "Mariana",
                "specialties": ["cabelo", "cor", "penteados"],
                "services": ["escova", "penteados", "progressiva", "tintura", "corte", "maquiagem_simples"],
                "notes": "Cabelo completo com cor avançada."
            },
            {
                "id": "davila",
                "name": "Dávila",
                "specialties": ["unhas", "gel", "reconstrução"],
                "services": ["manicure", "pedicure", "gel", "reconstrucao"],
                "price_tier": "premium",
                "notes": "Manicure avançada. Faz reconstrução individual."
            },
            {
                "id": "lu",
                "name": "Lu",
                "specialties": ["unhas", "gel"],
                "services": ["manicure", "pedicure", "gel"],
                "restrictions": ["Não faz reconstrução"],
                "price_tier": "standard"
            },
            {
                "id": "edna",
                "name": "Edna",
                "specialties": ["unhas"],
                "services": ["manicure", "pedicure", "maquiagem_leve"],
                "price_tier": "standard"
            },
            {
                "id": "tay",
                "name": "Tay",
                "specialties": ["maquiagem", "sobrancelha"],
                "services": ["maquiagem", "design_sobrancelha", "brow_lamination", "lash_lifting"],
                "notes": "Profissional principal de maquiagem e sobrancelha."
            },
            {
                "id": "suzana",
                "name": "Suzana",
                "type": "owner",
                "specialties": ["alongamento"],
                "services": ["alongamento_unhas"],
                "notes": "Alongamento exclusivo. Inclui gel + cutilagem russa."
            },
            {
                "id": "cintia",
                "name": "Cíntia",
                "type": "freelancer",
                "specialties": ["fitagem", "cachos"],
                "services": ["fitagem"],
                "availability": "Semana até 16h, sábado até 17h",
                "booking_rule": "Confirmar disponibilidade antes de agendar"
            }
        ],
        
        "services": [
            {"id": "escova_lisa", "name": "Escova Lisa", "category": "cabelo", "price": 59, "duration": 45, "keywords": ["escova", "lisa", "liso"]},
            {"id": "escova_modelada", "name": "Escova Modelada", "category": "cabelo", "price": 69, "duration": 50, "keywords": ["modelada", "escova", "cachos"]},
            {"id": "adicional_mega", "name": "Adicional Mega Hair", "category": "adicional", "price": 20, "is_addon": True},
            {"id": "penteado_basico", "name": "Penteado Básico", "category": "cabelo", "price": 115, "duration": 35, "includes_escova": False, "warning": "NÃO inclui escova"},
            {"id": "penteado_plus", "name": "Penteado Plus", "category": "cabelo", "price": 139, "duration": 40, "includes_escova": False, "warning": "NÃO inclui escova"},
            {"id": "penteado_premium", "name": "Penteado Premium", "category": "cabelo", "price": 169, "duration": 60, "includes_escova": False, "warning": "NÃO inclui escova"},
            {"id": "corte_escova", "name": "Corte + Escova", "category": "cabelo", "price": 170, "duration": 60},
            {"id": "corte_simples", "name": "Corte (sem escova)", "category": "cabelo", "price": 120, "duration": 30},
            {"id": "retoque_raiz", "name": "Retoque de Raiz", "category": "cor", "price": 179, "duration": 90},
            {"id": "fitagem", "name": "Fitagem (definição cachos)", "category": "cabelo", "price": 95, "duration": 60, "keywords": ["cachos", "fitagem", "definição"]},
            {"id": "matizacao", "name": "Matização de Loiros", "category": "cor", "price": 115, "duration": 60, "includes_escova": True, "note": "JÁ inclui escova"},
            {"id": "hidratacao", "name": "Hidratação", "category": "tratamento", "price": 85, "duration": 30, "includes_escova": False, "warning": "NÃO inclui escova"},
            {"id": "nutricao", "name": "Nutrição", "category": "tratamento", "price": 95, "duration": 30, "includes_escova": False},
            {"id": "reconstrucao", "name": "Reconstrução", "category": "tratamento", "price": 110, "duration": 40, "includes_escova": False},
            {"id": "hidratacao_coreana", "name": "Hidratação Coreana", "category": "tratamento", "price": 135, "duration": 40, "includes_escova": False},
            {"id": "umectacao", "name": "Umectação", "category": "tratamento", "price": 65, "duration": 30, "includes_escova": False},
            {"id": "progressiva", "name": "Progressiva Perfecta", "category": "quimica", "price_range": "250-450", "duration": 180, "keywords": ["progressiva", "alisar", "liso"]},
            {"id": "cauterizacao", "name": "Cauterização Cauter Gloss", "category": "tratamento", "price": 150, "duration": 60, "description": "Reconstrução + selagem. NÃO alisa."},
            {"id": "manicure", "name": "Manicure Tradicional", "category": "unhas", "price": 50, "price_alt": 42, "duration": 40, "keywords": ["manicure", "unha", "mão"]},
            {"id": "pedicure", "name": "Pedicure Tradicional", "category": "unhas", "price": 60, "price_alt": 45, "duration": 50, "keywords": ["pedicure", "unha", "pé"]},
            {"id": "plastica_pes", "name": "Plástica dos Pés", "category": "unhas", "price": 140, "duration": 90, "includes": "pedicure"},
            {"id": "manicure_russa", "name": "Manicure Russa", "category": "unhas", "price": 80, "duration": 60},
            {"id": "gel_maos", "name": "Esmaltação em Gel (Mãos)", "category": "unhas", "price": 140, "price_alt": 120, "duration": 60, "keywords": ["gel", "unha"]},
            {"id": "gel_pes", "name": "Esmaltação em Gel (Pés)", "category": "unhas", "price": 140, "price_alt": 120, "duration": 60},
            {"id": "remocao_gel", "name": "Remoção de Gel", "category": "unhas", "price": 80, "duration": 30},
            {"id": "remocao_gel_manicure", "name": "Remoção Gel + Manicure", "category": "unhas", "price": 90, "duration": 70},
            {"id": "remocao_gel_pedicure", "name": "Remoção Gel Pé + Pedicure", "category": "unhas", "price": 100, "duration": 80},
            {"id": "remocao_gel_suzana", "name": "Remoção + Manicure (Suzana)", "category": "unhas", "price": 180, "duration": 90},
            {"id": "remocao_alongamento", "name": "Remoção Alongamento (Suzana)", "category": "unhas", "price": 150, "duration": 60},
            {"id": "alongamento", "name": "Alongamento de Unhas", "category": "unhas", "price": 450, "duration": 180, "includes": "gel + cutilagem russa", "professional": "suzana"},
            {"id": "make_casual", "name": "Maquiagem Casual", "category": "maquiagem", "price": 120, "duration": 40, "keywords": ["maquiagem", "make"]},
            {"id": "make_basica", "name": "Maquiagem Básica", "category": "maquiagem", "price": 149, "duration": 50},
            {"id": "make_premium", "name": "Maquiagem Premium", "category": "maquiagem", "price": 195, "duration": 60},
            {"id": "design_sobrancelha", "name": "Design de Sobrancelha", "category": "sobrancelha", "price": 60, "duration": 30, "keywords": ["sobrancelha", "design"]},
            {"id": "design_tintura", "name": "Design + Tintura", "category": "sobrancelha", "price": 80, "duration": 40},
            {"id": "brow_lamination", "name": "Brow Lamination", "category": "sobrancelha", "price": 150, "duration": 60, "addon_tintura": 30},
            {"id": "lash_lifting", "name": "Lash Lifting", "category": "cilios", "price": 165, "duration": 60}
        ],
        
        "packages": {
            "escova": {
                "name": "Pacotes de Escova",
                "payment": "À vista (Pix ou dinheiro)",
                "options": [
                    {"qty": 4, "validity_days": 30, "lisa": 55, "modelada": 65},
                    {"qty": 8, "validity_days": 60, "lisa": 52, "modelada": 59}
                ],
                "addons": {"coreano": 30, "labrisa": 25, "kerastase": 30}
            },
            "gel": {
                "name": "Pacotes de Gel",
                "min_qty": 3,
                "payment": "À vista",
                "options": [
                    {"qty": 3, "validity_days": 60, "lu": 99, "davila": 120},
                    {"qty": 6, "validity_days": 120, "lu": 99, "davila": 120}
                ]
            },
            "tradicional": {
                "name": "Pacotes Tradicional",
                "options": ["4 mãos", "4 mãos + 1 pé", "4 mãos + 2 pés"],
                "prices": {"davila": {"mao": 45, "pe": 55}, "outras": {"mao": 38, "pe": 40}}
            }
        },
        
        "coupons": [
            {"code": "PRISCILA10", "influencer": "Priscila Kuhn", "discount": 10},
            {"code": "EWYLIN10", "influencer": "Ewylin Salvatori", "discount": 10},
            {"code": "SOLANGE10", "influencer": "Solange", "discount": 10},
            {"code": "CAROLINE10", "influencer": "Caroline", "discount": 10},
            {"code": "KETLYN10", "influencer": "Ketlyn", "discount": 10}
        ],
        
        "faq": [
            {
                "id": "produto",
                "patterns": ["qual produto", "qual marca", "que produto"],
                "response": "Trabalhamos com linha profissional de alta performance, livre de formol, sem cheiro forte. A indicação exata confirmamos conforme seu tipo de fio e histórico de química."
            },
            {
                "id": "formol",
                "patterns": ["tem formol", "formol", "sem formol"],
                "response": "Não. A linha que usamos é livre de formol."
            },
            {
                "id": "alisa",
                "patterns": ["alisa 100%", "fica liso", "preciso escovar"],
                "response": "A proposta é alinhar muito e deixar bem liso. Muitas clientes conseguem lavar, secar e o cabelo já fica disciplinado. A raiz cresce natural, então fazemos retoque quando necessário."
            },
            {
                "id": "duracao",
                "patterns": ["quanto tempo dura", "dura quanto"],
                "response": "Dura conforme o crescimento da sua raiz. O comprimento tratado fica alinhado, e quando a raiz começa a aparecer, fazemos o retoque."
            },
            {
                "id": "tratamento_escova",
                "patterns": ["tratamento inclui escova", "inclui escova"],
                "response": "Os tratamentos são só o tratamento. Escova é cobrada à parte. A única exceção é a matização, que já inclui escova."
            },
            {
                "id": "penteado_escova",
                "patterns": ["penteado inclui escova"],
                "response": "Penteado não inclui escova. Se quiser escova antes, a gente agenda os dois e soma o valor."
            },
            {
                "id": "gel_remocao",
                "patterns": ["já tenho gel", "estou com gel", "tenho gel"],
                "response": "Antes de fazer manicure ou gel, precisamos agendar a remoção do gel atual. Leva cerca de 30 minutos e é cobrada à parte. Você está com gel nas mãos, nos pés ou nos dois?"
            },
            {
                "id": "localizacao",
                "patterns": ["onde fica", "endereço", "localização"],
                "response": "Estamos na Rua Mato Grosso, 837E, Jardim Itália, Chapecó - SC. Temos estacionamento em frente e mais 4 vagas na esquina. Quer que eu envie a localização? 📍"
            },
            {
                "id": "horario",
                "patterns": ["horário de funcionamento", "que horas abre", "que horas fecha"],
                "response": "Funcionamos de segunda a sábado, das 8h às 20h, sem pausa para almoço."
            }
        ],
        
        "rules": {
            "service_order": {
                "order": ["unhas", "cabelo", "maquiagem"],
                "note": "Maquiagem SEMPRE por último"
            },
            "removal_required": {
                "question": "Você está com gel ou alongamento nas unhas?",
                "if_yes": "Agendar remoção antes (30min, cobrado à parte)"
            },
            "retention": {
                "never": "Dizer só 'não tem horário'",
                "always": "Oferecer 2 alternativas, tentar encaixe, lista de prioridade"
            },
            "product_protection": {
                "rule": "Não revelar marca pelo WhatsApp",
                "response": "Linha profissional de alta performance, livre de formol"
            }
        }
    }
    
    create_file(f"{BASE_DIR}/backend/app/knowledge/data/haven.json", json.dumps(haven_data, indent=2, ensure_ascii=False))
    
    print("\n✅ Knowledge Base created!")

if __name__ == "__main__":
    main()
