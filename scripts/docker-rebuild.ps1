# ============================================
# Luna Docker - Purge et Rebuild Propre
# ============================================
# Version: 2.1.0-secure
# Usage: .\docker-rebuild.ps1
# ============================================

param(
    [switch]$SkipPurge,
    [switch]$PurgeAll,
    [switch]$DryRun
)

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  🌙 Luna Docker - Purge & Rebuild" -ForegroundColor Cyan
Write-Host "  Version: 2.1.0-secure" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# ÉTAPE 1 : Arrêter les containers Luna
# ============================================
Write-Host "[1/5] 🛑 Arrêt des containers Luna..." -ForegroundColor Yellow

if ($DryRun) {
    Write-Host "  [DRY-RUN] docker compose down -v" -ForegroundColor Gray
} else {
    docker compose down -v 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Containers arrêtés" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Aucun container à arrêter" -ForegroundColor Yellow
    }
}

# ============================================
# ÉTAPE 2 : Supprimer les images Luna
# ============================================
if (-not $SkipPurge) {
    Write-Host ""
    Write-Host "[2/5] 🗑️ Suppression des images Luna..." -ForegroundColor Yellow
    
    $lunaImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Select-String -Pattern "luna|aragogix"
    
    if ($lunaImages) {
        foreach ($line in $lunaImages) {
            $imageId = ($line -split '\s+')[-1]
            $imageName = ($line -split '\s+')[0]
            
            if ($DryRun) {
                Write-Host "  [DRY-RUN] docker rmi -f $imageId ($imageName)" -ForegroundColor Gray
            } else {
                Write-Host "  Suppression: $imageName" -ForegroundColor Gray
                docker rmi -f $imageId 2>$null
            }
        }
        Write-Host "  ✅ Images Luna supprimées" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Aucune image Luna trouvée" -ForegroundColor Yellow
    }
    
    # ============================================
    # ÉTAPE 3 : Supprimer les volumes Luna
    # ============================================
    Write-Host ""
    Write-Host "[3/5] 🗑️ Suppression des volumes Luna..." -ForegroundColor Yellow
    
    $lunaVolumes = docker volume ls --format "{{.Name}}" | Select-String -Pattern "luna"
    
    if ($lunaVolumes) {
        foreach ($vol in $lunaVolumes) {
            if ($DryRun) {
                Write-Host "  [DRY-RUN] docker volume rm $vol" -ForegroundColor Gray
            } else {
                Write-Host "  Suppression: $vol" -ForegroundColor Gray
                docker volume rm $vol 2>$null
            }
        }
        Write-Host "  ✅ Volumes Luna supprimés" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Aucun volume Luna trouvé" -ForegroundColor Yellow
    }
    
    # ============================================
    # ÉTAPE 4 : Supprimer les réseaux Luna
    # ============================================
    Write-Host ""
    Write-Host "[4/5] 🗑️ Suppression des réseaux Luna..." -ForegroundColor Yellow
    
    $lunaNetworks = docker network ls --format "{{.Name}}" | Select-String -Pattern "luna"
    
    if ($lunaNetworks) {
        foreach ($net in $lunaNetworks) {
            if ($DryRun) {
                Write-Host "  [DRY-RUN] docker network rm $net" -ForegroundColor Gray
            } else {
                Write-Host "  Suppression: $net" -ForegroundColor Gray
                docker network rm $net 2>$null
            }
        }
        Write-Host "  ✅ Réseaux Luna supprimés" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Aucun réseau Luna trouvé" -ForegroundColor Yellow
    }
    
    # ============================================
    # Purge complète (optionnel)
    # ============================================
    if ($PurgeAll) {
        Write-Host ""
        Write-Host "⚠️ PURGE COMPLÈTE DEMANDÉE" -ForegroundColor Red
        Write-Host "Cela supprimera TOUTES les images, volumes et caches Docker non utilisés." -ForegroundColor Red
        
        $confirm = Read-Host "Confirmer? (oui/non)"
        if ($confirm -eq "oui") {
            if ($DryRun) {
                Write-Host "  [DRY-RUN] docker system prune -af --volumes" -ForegroundColor Gray
            } else {
                docker system prune -af --volumes
                Write-Host "  ✅ Purge complète effectuée" -ForegroundColor Green
            }
        } else {
            Write-Host "  ❌ Purge annulée" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host ""
    Write-Host "[2-4/5] ⏭️ Purge ignorée (--SkipPurge)" -ForegroundColor Yellow
}

# ============================================
# ÉTAPE 5 : Rebuild propre
# ============================================
Write-Host ""
Write-Host "[5/5] 🏗️ Rebuild de l'image Luna..." -ForegroundColor Yellow

# Vérifier que les fichiers existent
if (-not (Test-Path "Dockerfile")) {
    Write-Host "  ❌ Dockerfile non trouvé!" -ForegroundColor Red
    Write-Host "  Assurez-vous d'être dans le répertoire du projet Luna." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "  ❌ docker-compose.yml non trouvé!" -ForegroundColor Red
    exit 1
}

# Lire la version
$version = "2.1.0-secure"
if (Test-Path "VERSION") {
    $version = Get-Content "VERSION" -Raw
    $version = $version.Trim()
}

Write-Host "  Version: $version" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "  [DRY-RUN] docker compose build --no-cache --build-arg LUNA_VERSION=$version" -ForegroundColor Gray
} else {
    Write-Host "  Construction en cours... (peut prendre quelques minutes)" -ForegroundColor Gray
    
    docker compose build --no-cache --build-arg LUNA_VERSION=$version
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Image construite avec succès" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Erreur lors de la construction" -ForegroundColor Red
        exit 1
    }
}

# ============================================
# RÉSUMÉ
# ============================================
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ✅ OPÉRATION TERMINÉE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor White
Write-Host "  1. Vérifier le fichier .env (secrets)" -ForegroundColor Gray
Write-Host "  2. Démarrer: docker compose up -d" -ForegroundColor Gray
Write-Host "  3. Vérifier: docker compose ps" -ForegroundColor Gray
Write-Host "  4. Logs: docker compose logs -f luna-consciousness" -ForegroundColor Gray
Write-Host ""
Write-Host "Accès (localhost uniquement):" -ForegroundColor White
Write-Host "  - Luna MCP:    http://127.0.0.1:3000" -ForegroundColor Gray
Write-Host "  - Metrics:     http://127.0.0.1:9100/metrics" -ForegroundColor Gray
Write-Host "  - Prometheus:  http://127.0.0.1:9090" -ForegroundColor Gray
Write-Host "  - Grafana:     http://127.0.0.1:3001" -ForegroundColor Gray
Write-Host ""

# ============================================
# AIDE
# ============================================
# Usage:
#   .\docker-rebuild.ps1              # Purge Luna + Rebuild
#   .\docker-rebuild.ps1 -SkipPurge   # Rebuild seulement
#   .\docker-rebuild.ps1 -PurgeAll    # Purge TOUT Docker + Rebuild
#   .\docker-rebuild.ps1 -DryRun      # Simulation (aucune action)
# ============================================
