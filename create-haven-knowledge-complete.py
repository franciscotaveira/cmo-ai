import json
import os

base_path = '/Users/franciscotaveira.ads/Local_Dev/Mothership_Core/command-tower/agents/haven-receptionist/knowledge'

# Business
business = {
  "name": "Haven Escovaria & Esmalteria",
  "type": "beauty_salon",
  "positioning": "Espaço sofisticado, moderno e acolhedor, com valores competitivos. Não é franquia.",
  "tagline": "Sua beleza em boas mãos",
  "address": {
    "street": "Rua Mato Grosso",
    "number": "837E",
    "neighborhood": "Jardim Itália",
    "city": "Chapecó",
    "state": "SC",
    "zip": "89816-000",
    "country": "Brasil",
    "reference": "Próximo ao centro"
  },
  "contact": {
    "whatsapp": "primary_channel",
    "instagram": "@haven.escovaria"
  },
  "hours": {
    "monday": {"open": "08:00", "close": "20:00"},
    "tuesday": {"open": "08:00", "close": "20:00"},
    "wednesday": {"open": "08:00", "close": "20:00"},
    "thursday": {"open": "08:00", "close": "20:00"},
    "friday": {"open": "08:00", "close": "20:00"},
    "saturday": {"open": "08:00", "close": "20:00"},
    "sunday": "closed"
  },
  "hours_note": "Funcionamos de segunda a sábado, das 8h às 20h, sem pausa para almoço",
  "parking": {
    "front": {"available": True, "description": "Estacionamento em frente ao prédio"},
    "corner": {"available": True, "spots": 4, "description": "4 vagas na esquina"}
  },
  "payment_methods": ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"],
  "packages_payment_note": "Pacotes são somente à vista (Pix ou dinheiro)"
}

# Packages
packages = {
  "escova": {
    "name": "Pacotes de Escova",
    "min_quantity": 4,
    "payment": "a_vista",
    "payment_methods": ["pix", "dinheiro"],
    "tiers": [
      {"quantity": 4, "validity_days": 30, "prices": {"lisa": {"regular": 59, "package": 55}, "modelada": {"regular": 69, "package": 65}}},
      {"quantity": 8, "validity_days": 60, "prices": {"lisa": {"regular": 59, "package": 52}, "modelada": {"regular": 69, "package": 59}}}
    ],
    "premium_addons": {"coreano": {"per_escova": 30}, "labrisa": {"per_escova": 25}, "kerastase": {"per_escova": 30}}
  },
  "gel": {
    "name": "Pacotes de Esmaltação em Gel",
    "min_quantity": 3,
    "payment": "a_vista",
    "tiers": [
      {"quantity": 3, "validity_days": 60, "prices": {"lu": {"regular": 120, "package": 99}, "davila": {"regular": 140, "package": 120}}},
      {"quantity": 6, "validity_days": 120, "prices": {"lu": {"regular": 120, "package": 99}, "davila": {"regular": 140, "package": 120}}}
    ]
  },
  "tradicional": {
    "name": "Pacotes de Unha Tradicional",
    "payment": "a_vista",
    "options": [
      {"maos": 4, "pes": 0, "validity_days": 30},
      {"maos": 4, "pes": 1, "validity_days": 30},
      {"maos": 4, "pes": 2, "validity_days": 40}
    ],
    "prices": {"davila": {"mao": 45, "pe": 55}, "outras": {"mao": 38, "pe": 40}}
  }
}

# Upsells
upsells = {
  "lavatorio": {
    "name": "Upgrades de Lavatório",
    "base": {"brand": "Cadiveu", "note": "Produtos da casa"},
    "premium_options": [
      {"id": "coreano", "name": "Produtos Coreanos", "addon": 30, "applies_to": ["escova", "tratamentos"]},
      {"id": "labrisa", "name": "Produtos La Brisa", "addon": 25, "applies_to": ["escova", "tratamentos"]},
      {"id": "kerastase", "name": "Produtos Kérastase", "addon": 30, "applies_to": ["escova", "tratamentos"]}
    ],
    "rules": ["Promoções valem somente para produtos da casa", "Upgrades não entram em promo", "Secretária não fecha comanda de upsell"]
  },
  "adicionais": [
    {"id": "adicional_mega", "name": "Adicional Mega Hair", "price": 20, "applies_to": ["escova_lisa", "escova_modelada"]},
    {"id": "tintura_sobrancelha", "name": "Tintura de Sobrancelha", "price": 20, "applies_to": ["design_sobrancelha"]}
  ]
}

# Coupons
coupons = {
  "influencers": [
    {"name": "Priscila Kuhn", "coupon": "PRISCILA10", "discount_percent": 10},
    {"name": "Ewylin Salvatori", "coupon": "EWYLIN10", "discount_percent": 10},
    {"name": "Solange", "coupon": "SOLANGE10", "discount_percent": 10},
    {"name": "Caroline", "coupon": "CAROLINE10", "discount_percent": 10},
    {"name": "Ketlyn", "coupon": "KETLYN10", "discount_percent": 10}
  ],
  "rules": ["Cupom dá 10% de desconto", "Não acumula com outras promoções", "Registrar que veio pelo cupom"]
}

# Write files
with open(os.path.join(base_path, 'business.json'), 'w', encoding='utf-8') as f:
    json.dump(business, f, indent=2, ensure_ascii=False)

with open(os.path.join(base_path, 'packages.json'), 'w', encoding='utf-8') as f:
    json.dump(packages, f, indent=2, ensure_ascii=False)

with open(os.path.join(base_path, 'upsells.json'), 'w', encoding='utf-8') as f:
    json.dump(upsells, f, indent=2, ensure_ascii=False)

with open(os.path.join(base_path, 'coupons.json'), 'w', encoding='utf-8') as f:
    json.dump(coupons, f, indent=2, ensure_ascii=False)

print("✅ Knowledge Base JSON files created!")
print("  - business.json")
print("  - packages.json")
print("  - upsells.json")
print("  - coupons.json")
