# 🚀 SUBIR NO GITHUB — GUIA PASSO A PASSO

---

## 📋 **PRÉ-REQUISITOS**

- [ ] Conta no GitHub ([github.com](https://github.com))
- [ ] Git instalado no computador
- [ ] Todos os arquivos preparados (README, LICENSE, .gitignore)

---

## 🔑 **PASSO 1: CRIAR REPOSITÓRIO NO GITHUB**

1. **Acesse**: https://github.com/new

2. **Preencha**:
   ```
   Repository name: cmo-360-platform
   Description: Platform de Inteligência de Marketing para C-Level
   Public: ✅ (recomendado para open source)
   Initialize with README: ❌ (NÃO MARQUE - já temos README)
   Add .gitignore: ❌ (NÃO MARQUE - já temos)
   Add license: ❌ (NÃO MARQUE - já temos)
   ```

3. **Clique**: "Create repository"

4. **Copie a URL** do repositório:
   ```
   https://github.com/SEU-USUARIO/cmo-360-platform.git
   ```

---

## 🔧 **PASSO 2: CONFIGURAR GIT LOCAL**

```bash
# No terminal (Prompt/PowerShell):
cd c:\Users\Marketing\Documents\Antigravity\antigravity-kit

# Configurar seu nome e e-mail (se for a primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

---

## 📦 **PASSO 3: ADICIONAR REMOTE**

```bash
# Adicionar repositório remoto (substitua SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/cmo-360-platform.git

# Verificar se adicionou
git remote -v
```

**Saída esperada**:
```
origin  https://github.com/SEU-USUARIO/cmo-360-platform.git (fetch)
origin  https://github.com/SEU-USUARIO/cmo-360-platform.git (push)
```

---

## ✅ **PASSO 4: VERIFICAR .GITIGNORE**

```bash
# Verificar o que será ignorado
git status

# Arquivos importantes que DEVEM estar no .gitignore:
# ✅ .env
# ✅ .venv/
# ✅ __pycache__/
# ✅ *.log
# ✅ node_modules/
# ✅ drive_input/
# ✅ obsidian_vault/
```

---

## 📝 **PASSO 5: ADICIONAR ARQUIVOS**

```bash
# Adicionar TODOS os arquivos (respeitando .gitignore)
git add .

# OU adicionar apenas arquivos específicos (recomendado):
git add README.md
git add LICENSE
git add CHANGELOG.md
git add .gitignore
git add mkt/
git add sql/
git add frontend/
git add docker-compose.yml

# Verificar o que foi adicionado
git status
```

---

## 💾 **PASSO 6: COMMIT INICIAL**

```bash
# Fazer commit
git commit -m "feat: CMO 360° v6.1 — Platform de Inteligência de Marketing

- CMO-Bench: Aprendizado tipo SWE-bench
- Notification Dispatcher: E-mails, Slack, Telegram
- 10 áreas de marketing cobertas
- Custo zero de infra (free tiers)
- Dashboards automáticos no Obsidian

Versão: 6.1.0
Autor: Seu Nome
"
```

---

## 🚀 **PASSO 7: PUSH PARA GITHUB**

```bash
# Enviar para GitHub
git push -u origin main

# Se pedir credenciais:
# Username: seu-usuario-github
# Password: seu-token-ou-senha
```

**Se der erro de autenticação**:

1. **Crie um Token no GitHub**:
   - Acesse: https://github.com/settings/tokens
   - Clique: "Generate new token (classic)"
   - Marque: `repo`, `workflow`
   - Copie o token

2. **Use o token ao invés da senha**:
   ```
   Username: seu-usuario
   Password: ghp_xxxxxxxxxxxx (token)
   ```

---

## ✅ **PASSO 8: VERIFICAR NO GITHUB**

1. **Acesse**: https://github.com/SEU-USUARIO/cmo-360-platform

2. **Verifique**:
   - [ ] README.md aparece na página inicial
   - [ ] Todos os arquivos estão lá
   - [ ] .gitignore está funcionando (não mostra .env, .venv, etc.)

---

## 🔄 **COMO ATUALIZAR DEPOIS**

### **Fazer mudanças e subir**:

```bash
# 1. Fazer mudanças nos arquivos

# 2. Adicionar mudanças
git add .

# 3. Commitar
git commit -m "fix: Descrição da mudança"

# 4. Push
git push origin main
```

### **Puxar mudanças do GitHub**:

```bash
# Se mexeu em outro computador:
git pull origin main
```

---

## 📊 **ESTRUTURA DO REPOSITÓRIO**

Após subir, seu repositório terá:

```
cmo-360-platform/
├── 📄 README.md                 ⭐ Página principal
├── 📄 LICENSE                   ⭐ Licença MIT
├── 📄 CHANGELOG.md              ⭐ Histórico de versões
├── 📄 .gitignore                ⭐ Arquivos ignorados
├── 📄 docker-compose.yml        # Docker
│
├── 📂 mkt/engine/               # Motor principal
│   ├── main.py
│   ├── src/                     # 15+ módulos Python
│   └── test_*.py                # Testes
│
├── 📂 sql/                      # Banco de dados
│   └── 01-08_create_*.sql
│
├── 📂 frontend/                 # Web Platform
│   └── src/
│
└── 📚 Documentação/             # Docs completas
    └── *.md
```

---

## 🏷️ **ADICIONAR TAGS (OPCIONAL)**

```bash
# Criar tag para versão
git tag -a v6.1.0 -m "CMO 360° v6.1.0 — Notificações por E-mail"

# Enviar tags
git push origin --tags
```

---

## 📝 **DICAS DE BOAS PRÁTICAS**

### **Commits**

Use formato convencional:
```
feat: Nova funcionalidade
fix: Correção de bug
docs: Mudança em documentação
style: Formatação, sem mudança de código
refactor: Refatoração
test: Adicionar testes
chore: Configuração, build, etc.
```

### **Branches**

```bash
# Criar branch para feature
git checkout -b feature/nome-da-feature

# Voltar para main
git checkout main

# Deletar branch
git branch -d feature/nome-da-feature
```

---

## 🐛 **SOLUÇÃO DE PROBLEMAS**

### "fatal: remote origin already exists"

```bash
# Remover e adicionar de novo
git remote remove origin
git remote add origin https://github.com/SEU-USUARIO/cmo-360-platform.git
```

### "Authentication failed"

```bash
# Criar novo token em:
https://github.com/settings/tokens

# Usar token ao invés de senha
```

### "Changes not staged"

```bash
# Adicionar tudo
git add .

# Ou arquivos específicos
git add README.md
```

### "Please tell me who you are"

```bash
# Configurar nome e e-mail
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## 📞 **CHECKLIST FINAL**

- [ ] Criou repositório no GitHub
- [ ] Copiou URL do repositório
- [ ] Configurou remote origin
- [ ] Adicionou arquivos (git add)
- [ ] Commitou (git commit)
- [ ] Enviou (git push)
- [ ] Verificou no GitHub
- [ ] README.md aparece corretamente
- [ ] .gitignore funciona (não subiu .env)

---

## 🎯 **PRÓXIMOS PASSOS**

### **Depois de subir**:

1. **Adicione badges** no README:
   - Stars
   - Forks
   - Issues
   - License

2. **Configure GitHub Pages** (opcional):
   - Docs em: https://seu-usuario.github.io/cmo-360-platform

3. **Adicione colaboradores** (opcional):
   - Settings → Collaborators

4. **Crie Issues** para features futuras

---

<div align="center">

**🚀 REPOSITÓRIO NO GITHUB!**

*8 passos • 10 minutos • Pronto para compartilhar*

**URL: https://github.com/SEU-USUARIO/cmo-360-platform**

</div>
