# ============================================================
#  subir_a_github.ps1  -  Cuadrante Personal -> GitHub
# ============================================================

$ErrorActionPreference = "Continue"
$REPO    = "devai82/Cuadrantepersonal"
$BRANCH  = "main"
$CARPETA = "C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal"
$MENSAJE = "Actualizacion cuadrante: pinpad PIN, usuarios online, presencia minima, descanso, export Excel"

Clear-Host
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   Cuadrante Personal -> GitHub" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# ── Ir a la carpeta del proyecto ─────────────────────────────
if (-not (Test-Path $CARPETA)) {
    Write-Host "ERROR: No encuentro la carpeta:" -ForegroundColor Red
    Write-Host "  $CARPETA" -ForegroundColor Yellow
    Read-Host "`nPulsa Enter para cerrar"
    exit
}
Set-Location $CARPETA
Write-Host "Carpeta: $CARPETA" -ForegroundColor Gray

# ── Comprobar que existe index.html ──────────────────────────
if (-not (Test-Path "index.html")) {
    Write-Host "`nERROR: No encuentro index.html en la carpeta." -ForegroundColor Red
    Read-Host "`nPulsa Enter para cerrar"
    exit
}
Write-Host "Archivo index.html encontrado OK" -ForegroundColor Green

# ── Comprobar git ─────────────────────────────────────────────
Write-Host "`n[1/4] Comprobando git..." -ForegroundColor Yellow
$gitPath = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitPath) {
    Write-Host "      Git no esta instalado." -ForegroundColor Red
    Write-Host "      Descargalo en: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "`nPulsa Enter para cerrar"
    exit
}
Write-Host "      git OK -> $($gitPath.Source)" -ForegroundColor Green

# ── Comprobar / instalar GitHub CLI ──────────────────────────
Write-Host "`n[2/4] Comprobando GitHub CLI (gh)..." -ForegroundColor Yellow
$ghPath = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghPath) {
    Write-Host "      GitHub CLI no instalado. Instalando via winget..." -ForegroundColor Yellow
    winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements
    # Refrescar PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
    $ghPath = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $ghPath) {
        Write-Host "      No se pudo instalar gh automaticamente." -ForegroundColor Red
        Write-Host "      Instalalo manualmente: https://cli.github.com/" -ForegroundColor Yellow
        Read-Host "`nPulsa Enter para cerrar"
        exit
    }
}
Write-Host "      gh OK -> $($ghPath.Source)" -ForegroundColor Green

# ── Login en GitHub ───────────────────────────────────────────
Write-Host "`n[3/4] Comprobando sesion GitHub..." -ForegroundColor Yellow
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      Abriendo navegador para iniciar sesion..." -ForegroundColor Cyan
    Write-Host "      (Usa tu cuenta de Gmail asociada a GitHub)" -ForegroundColor Gray
    gh auth login --web --git-protocol https
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ERROR al iniciar sesion en GitHub." -ForegroundColor Red
        Read-Host "`nPulsa Enter para cerrar"
        exit
    }
}
Write-Host "      Sesion GitHub OK" -ForegroundColor Green

# ── Git: init, remote, commit, push ──────────────────────────
Write-Host "`n[4/4] Subiendo archivos a GitHub..." -ForegroundColor Yellow

# Configurar nombre y email para git (necesario para commit)
git config user.email "jm_olmeda@hotmail.com" 2>$null
git config user.name "Jose" 2>$null

# ── Limpiar estado git corrupto (rebase/merge colgado) ───────
Write-Host "      Limpiando estado git..." -ForegroundColor Gray
$gitFiles = @("AUTO_MERGE","MERGE_HEAD","MERGE_MSG","CHERRY_PICK_HEAD","REVERT_HEAD")
foreach ($f in $gitFiles) {
    $fp = Join-Path ".git" $f
    if (Test-Path $fp) { Remove-Item $fp -Force; Write-Host "      Eliminado: $f" -ForegroundColor Gray }
}
$rebaseDirs = @("rebase-merge","rebase-apply")
foreach ($d in $rebaseDirs) {
    $dp = Join-Path ".git" $d
    if (Test-Path $dp) { Remove-Item $dp -Recurse -Force; Write-Host "      Eliminado: $d" -ForegroundColor Gray }
}

# Init si no existe
if (-not (Test-Path ".git")) {
    git init
    git branch -M $BRANCH
}

# Remote
$remoteExists = git remote 2>$null | Where-Object { $_ -eq "origin" }
$remoteUrl = "https://github.com/$REPO.git"
if ($remoteExists) {
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
}

# Configurar gh como credential helper
gh auth setup-git 2>$null

# Pull para sincronizar
Write-Host "      Sincronizando con GitHub..." -ForegroundColor Gray
git fetch origin $BRANCH 2>$null
git pull origin $BRANCH --rebase --allow-unrelated-histories 2>$null

# Añadir archivos
git add "index.html"
git add "Cuadrante_Personal_2026.html"
if (Test-Path "newsletter_cobertura.py") { git add "newsletter_cobertura.py" }

# Mostrar qué cambia
Write-Host ""
Write-Host "      Cambios detectados:" -ForegroundColor Gray
git status --short

# Commit
$fecha = Get-Date -Format "dd/MM/yyyy HH:mm"
git commit -m "$MENSAJE [$fecha]" 2>&1 | Out-String | Write-Host

if ($LASTEXITCODE -eq 128) {
    Write-Host "      (nada nuevo que subir)" -ForegroundColor Yellow
}

# Push
Write-Host "      Enviando a GitHub..." -ForegroundColor Gray
git push origin $BRANCH --force-with-lease 2>&1 | Out-String | Write-Host
$pushOK = $LASTEXITCODE

# ── Resultado final ───────────────────────────────────────────
Write-Host ""
if ($pushOK -eq 0) {
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "   SUBIDO CORRECTAMENTE" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Web (actualiza en ~2 min):" -ForegroundColor Cyan
    Write-Host "  https://devai82.github.io/Cuadrantepersonal/" -ForegroundColor White
    Write-Host ""
    Write-Host "  Repositorio:" -ForegroundColor Cyan
    Write-Host "  https://github.com/devai82/Cuadrantepersonal" -ForegroundColor White
} else {
    Write-Host "=======================================" -ForegroundColor Red
    Write-Host "   ERROR AL SUBIR" -ForegroundColor Red
    Write-Host "=======================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - Sesion de GitHub caducada -> vuelve a ejecutar" -ForegroundColor Gray
    Write-Host "  - Sin conexion a internet" -ForegroundColor Gray
    Write-Host "  - El repositorio no existe o no tienes acceso" -ForegroundColor Gray
}

Write-Host ""
Read-Host "Pulsa Enter para cerrar"
