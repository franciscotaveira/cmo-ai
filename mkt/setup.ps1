# ═══════════════════════════════════════════════════════════════════════════════
# MARKETING DIRECTOR OS — SETUP AUTOMÁTICO (POWERSHELL)
# ═══════════════════════════════════════════════════════════════════════════════
# Este script automatiza a configuração inicial do sistema
#
# Uso: .\setup.ps1
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 MARKETING DIRECTOR OS v4.0 - SETUP AUTOMÁTICO                             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Docker
Write-Host "[1/6] Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Docker instalado: $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Docker não encontrado!" -ForegroundColor Red
        Write-Host "  💡 Instale Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ❌ Erro ao verificar Docker: $_" -ForegroundColor Red
    exit 1
}

# 2. Criar estrutura de pastas
Write-Host ""
Write-Host "[2/6] Criando estrutura de pastas..." -ForegroundColor Yellow

$pastas = @(
    "drive_data",
    "drive_data/salao-esposa",
    "drive_data/franquia-chapeco",
    "drive_data/diretoria",
    "obsidian_data",
    "logs"
)

foreach ($pasta in $pastas) {
    $caminhoCompleto = Join-Path $PSScriptRoot $pasta
    if (-not (Test-Path $caminhoCompleto)) {
        New-Item -ItemType Directory -Path $caminhoCompleto -Force | Out-Null
        Write-Host "  ✅ Criada: $pasta" -ForegroundColor Green
    } else {
        Write-Host "  📁 Já existe: $pasta" -ForegroundColor Gray
    }
}

# 3. Configurar .env
Write-Host ""
Write-Host "[3/6] Configurando arquivo .env..." -ForegroundColor Yellow

$envExample = Join-Path $PSScriptRoot ".env.example"
$envFile = Join-Path $PSScriptRoot ".env"

if (Test-Path $envFile) {
    Write-Host "  📄 Arquivo .env já existe!" -ForegroundColor Yellow
} else {
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "  ✅ .env criado a partir de .env.example" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "  ⚠️  ATENÇÃO: Você precisa editar o .env agora!" -ForegroundColor Red
        Write-Host "  💡 Execute: notepad .env" -ForegroundColor Cyan
        Write-Host ""
        
        $resposta = Read-Host "  Quer abrir o .env agora? (S/N)"
        if ($resposta -eq 'S' -or $resposta -eq 's') {
            notepad $envFile
        }
    }
}

# 4. Criar arquivos de teste
Write-Host ""
Write-Host "[4/6] Criando arquivos de teste..." -ForegroundColor Yellow

$csvContent = @"
data,produto,valor,cliente
2024-01-15,Corte,150.00,Maria Silva
2024-01-15,Hidratacao,200.00,Ana Costa
2024-01-16,Manicure,80.00,Joana Santos
"@

$csvPath = Join-Path $PSScriptRoot "drive_data\salao-esposa\teste_vendas.csv"
$csvContent | Out-File -FilePath $csvPath -Encoding UTF8
Write-Host "  ✅ CSV de teste criado" -ForegroundColor Green

# 5. Verificar Docker Desktop
Write-Host ""
Write-Host "[5/6] Verificando Docker Desktop..." -ForegroundColor Yellow

try {
    $dockerPs = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Docker Desktop está rodando" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Docker Desktop não está rodando!" -ForegroundColor Red
        Write-Host "  💡 Abra o Docker Desktop e aguarde o ícone ficar verde" -ForegroundColor Yellow
        
        $resposta = Read-Host "  Docker Desktop já está aberto? (S/N)"
        if ($resposta -ne 'S' -and $resposta -ne 's') {
            Write-Host "  💡 Execute o script novamente após abrir o Docker Desktop" -ForegroundColor Yellow
            exit 1
        }
    }
} catch {
    Write-Host "  ❌ Erro ao verificar Docker: $_" -ForegroundColor Red
    exit 1
}

# 6. Instruções finais
Write-Host ""
Write-Host "[6/6] Configuração concluída!" -ForegroundColor Green
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📋 PRÓXIMOS PASSOS                                                           ║" -ForegroundColor Cyan
Write-Host "╠═══════════════════════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║  1️⃣  Configure o Supabase:                                                    ║" -ForegroundColor White
Write-Host "║     • Acesse: https://supabase.com/dashboard                                  ║" -ForegroundColor Gray
Write-Host "║     • Execute: init_supabase.sql                                              ║" -ForegroundColor Gray
Write-Host "║                                                                               ║" -ForegroundColor Cyan
Write-Host "║  2️⃣  Edite o .env com suas credenciais:                                       ║" -ForegroundColor White
Write-Host "║     • notepad .env                                                            ║" -ForegroundColor Gray
Write-Host "║     • Preencha SUPABASE_URL e SUPABASE_KEY                                    ║" -ForegroundColor Gray
Write-Host "║                                                                               ║" -ForegroundColor Cyan
Write-Host "║  3️⃣  Inicie o sistema:                                                        ║" -ForegroundColor White
Write-Host "║     • docker-compose up --build                                               ║" -ForegroundColor Gray
Write-Host "║                                                                               ║" -ForegroundColor Cyan
Write-Host "║  4️⃣  Acesse o Windmill:                                                       ║" -ForegroundColor White
Write-Host "║     • http://localhost:8000                                                   ║" -ForegroundColor Gray
Write-Host "╚═══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host ""
$resposta = Read-Host "Iniciar sistema agora? (S/N)"

if ($resposta -eq 'S' -or $resposta -eq 's') {
    Write-Host ""
    Write-Host "🚀 Iniciando Docker Compose..." -ForegroundColor Green
    docker-compose up --build
} else {
    Write-Host ""
    Write-Host "💡 Para iniciar manualmente: docker-compose up --build" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "✅ Setup concluído!" -ForegroundColor Green
