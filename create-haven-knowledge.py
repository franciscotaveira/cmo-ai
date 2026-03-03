import json
import os

base_path = '/Users/franciscotaveira.ads/Local_Dev/Mothership_Core/command-tower/agents/haven-receptionist/knowledge'

# Services
services = [
  {"id":"escova_lisa","name":"Escova Lisa","aliases":["escova","chapinha"],"duration":45,"price":59,"category":"cabelo"},
  {"id":"escova_modelada","name":"Escova Modelada","aliases":["modelada"],"duration":50,"price":69,"category":"cabelo"},
  {"id":"progressiva","name":"Progressiva","aliases":["progressiva"],"duration":210,"price":250,"category":"tratamento"},
  {"id":"manicure_tradicional","name":"Manicure Tradicional","aliases":["manicure","unha"],"duration":40,"price":50,"category":"unhas"},
  {"id":"manicure_russa","name":"Manicure Russa","aliases":["russa"],"duration":60,"price":80,"category":"unhas"},
  {"id":"gel_aplicacao","name":"Gel Aplicação","aliases":["gel"],"duration":90,"price":140,"category":"unhas"},
  {"id":"pedicure_tradicional","name":"Pedicure","aliases":["pedicure","pe"],"duration":50,"price":60,"category":"unhas"},
  {"id":"design_sobrancelha","name":"Design Sobrancelha","aliases":["sobrancelha"],"duration":30,"price":60,"category":"sobrancelha"},
  {"id":"brow_lamination","name":"Brow Lamination","aliases":["laminacao"],"duration":60,"price":150,"category":"sobrancelha"},
  {"id":"make_basica","name":"Maquiagem Basica","aliases":["make","maquiagem"],"duration":50,"price":149,"category":"maquiagem"},
  {"id":"penteado_basico","name":"Penteado Basico","aliases":["penteado"],"duration":35,"price":115,"category":"cabelo","notes":"NAO inclui escova"},
  {"id":"hidratacao","name":"Hidratacao","aliases":["hidratar"],"duration":30,"price":85,"category":"tratamento","notes":"NAO inclui escova"},
  {"id":"matizacao","name":"Matizacao","aliases":["matizar"],"duration":45,"price":115,"category":"cor","notes":"INCLUI escova"},
  {"id":"corte_escova","name":"Corte + Escova","aliases":["corte"],"duration":60,"price":170,"category":"cabelo"}
]

# Professionals
professionals = [
  {"id":"ju","name":"Ju","specialties":["cabelo","cor"],"services":["escova_lisa","escova_modelada","progressiva","penteado_basico","hidratacao","matizacao","corte_escova"]},
  {"id":"carla","name":"Carla","specialties":["cabelo"],"services":["escova_lisa","hidratacao"],"excludeServices":["escova_modelada","penteado_basico"]},
  {"id":"mariana","name":"Mariana","specialties":["cabelo","maquiagem"],"services":["escova_lisa","escova_modelada","progressiva","penteado_basico","hidratacao","matizacao","corte_escova","make_basica"]},
  {"id":"davila","name":"Davila","specialties":["unhas"],"services":["manicure_tradicional","manicure_russa","gel_aplicacao","pedicure_tradicional"]},
  {"id":"lu","name":"Lu","specialties":["unhas"],"services":["manicure_tradicional","manicure_russa","pedicure_tradicional"],"excludeServices":["gel_aplicacao"]},
  {"id":"edna","name":"Edna","specialties":["unhas","maquiagem"],"services":["manicure_tradicional","pedicure_tradicional","make_basica"]},
  {"id":"tay","name":"Tay","specialties":["maquiagem","sobrancelha"],"services":["design_sobrancelha","brow_lamination","make_basica"]}
]

# Rules
rules = {
  "service_order": {"rule": "Unha -> Cabelo -> Maquiagem"},
  "required_questions": {"unhas": "Voce esta com gel ou alongamento?", "penteado": "Penteado NAO inclui escova"},
  "service_inclusions": {"matizacao": {"includes_escova": True}, "hidratacao": {"includes_escova": False}},
  "valid_coupons": {"PRISCILA10": {"discount": 10}, "EWYLIN10": {"discount": 10}},
  "handoff_triggers": ["falar com humano", "pessoa real", "reclamacao"],
  "never_say": ["nao temos horario", "infelizmente", "senhora"]
}

# FAQ
faq = [
  {"id":"preco","patterns":["quanto custa","qual o valor","preco"],"response":"Para {service}, o valor e R${price}."},
  {"id":"horario","patterns":["tem horario","horario disponivel","vaga"],"response":"Vou verificar a disponibilidade!"},
  {"id":"agendar","patterns":["quero agendar","quero marcar","agendar"],"response":"Claro! Qual servico voce gostaria?"},
  {"id":"humano","patterns":["falar com humano","pessoa real","atendente"],"response":"Vou te transferir para nossa equipe!"},
  {"id":"pagamento","patterns":["forma de pagamento","aceita pix","cartao"],"response":"Aceitamos Pix, cartao e dinheiro!"},
  {"id":"funcionamento","patterns":["horario de funcionamento","que horas abre"],"response":"Terca a Sabado, 9h as 19h."}
]

# Write files
with open(os.path.join(base_path, 'services.json'), 'w') as f:
    json.dump(services, f, indent=2)

with open(os.path.join(base_path, 'professionals.json'), 'w') as f:
    json.dump(professionals, f, indent=2)

with open(os.path.join(base_path, 'rules.json'), 'w') as f:
    json.dump(rules, f, indent=2)

with open(os.path.join(base_path, 'faq.json'), 'w') as f:
    json.dump(faq, f, indent=2)

print("✅ Knowledge base JSON files created!")
