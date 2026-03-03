---
name: supabase-skill
description: Banco de dados Supabase para projetos MCT. Schema beleza, RLS e princípio Truth in Data.
---

# Supabase — Skill MCT

## Projeto MCT

```yaml
url:      https://vkcusycstkgnitwefrfg.supabase.co
anon:     frontend (público)
service:  backend (privado)
```

## Princípio Truth in Data (P0)

- **ZERO** dados mock em produção.
- Estado vazio → "Sem dados ainda".
- Erro de fetch → Mostrar erro, não simulação.

## Schema Base (Beleza)

```sql
-- Clientes
CREATE TABLE customers (
  id uuid PRIMARY KEY,
  phone text UNIQUE,
  name text
);

-- Agendamentos
CREATE TABLE appointments (
  id uuid PRIMARY KEY,
  customer_id uuid REFERENCES customers(id),
  status text CHECK (status IN ('pending','confirmed','done','cancelled'))
);
```

## Row Level Security (RLS)

Sempre habilitar RLS. Negar por padrão. Permitir via políticas explícitas.
