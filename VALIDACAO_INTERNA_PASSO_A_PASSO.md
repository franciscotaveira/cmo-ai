# 🚀 GUIA DE VALIDAÇÃO INTERNA: CMO 360° (30 DIAS)

Este documento orienta sua jornada de validação interna para provar o ROI do **Marketing Data Command Center** dentro da sua própria operação.

---

## 📅 ROTEIRO DE 30 DIAS

### Semana 1: Setup & Data Ingest

- [ ] **Configurar .env**: Suas credenciais Supabase e Groq.
- [ ] **Data Seeding**: Popular o banco com dados reais dos últimos 3 meses (Use os scripts SQL na pasta `/sql`).
- [ ] **Obsidian Sync**: Garantir que as pastas `🧠 EXOCÓRTEX` estão mapeadas no seu Vault.
- [ ] **Ativação**: Rodar o `main.py` em uma máquina dedicada ou servidor 24/7.

### Semana 2-4: Coleta de Inteligência

- [ ] **Insights de IA**: Monitorar quantos insights valiosos foram gerados por semana.
- [ ] **Alertas Críticos**: Registrar cada vez que o sistema detectou uma anomalia antes de você.
- [ ] **Decisões**: Documentar ações tomadas baseadas nos dashboards (ex: pausei campanha X, escalei canal Y).

### Dia 30: Veredito Final

- [ ] **Cálculo de ROI**: Comparar tempo gasto manual vs automático.
- [ ] **Case Interno**: Criar um arquivo Markdown com os melhores resultados.
- [ ] **Decisão**: Sistema pronto para escala comercial ou precisa de ajustes?

---

## 🛠️ PASSO 1: CONFIGURAÇÃO AGORA

1. Vá até `c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\`
2. Abra o arquivo `.env.example`
3. Preencha com sua **SUPABASE_URL** e **SUPABASE_KEY**
4. Ajuste os caminhos `PATH_TO_DRIVE` e `PATH_TO_OBSIDIAN`
5. Salve o arquivo como `.env` (sem o .example)

## ⚖️ TESTE DE SUCESSO

Após configurar, abra o terminal e rode:

```powershell
.\testar_sistema_completo.bat
```

Se todos os itens ficarem ✅, você está pronto para o lançamento interno!

---
*Antigravity Engine — Transformando Dados em Decisões.*
