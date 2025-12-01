@echo off
REM 🌙 Luna Consciousness - Démarrage Infrastructure Complète
REM Version: 1.0.1
REM Démarre: Luna + Redis + Prometheus + Grafana

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌙 Luna Consciousness - Infrastructure Complète        ║
echo ║   Version 1.0.1                                          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Naviguer vers le répertoire du projet
cd /d D:\Luna-consciousness-mcp

echo 🧹 Nettoyage des anciens containers...
echo.

REM Arrêter la stack actuelle si elle existe
docker-compose down 2>nul

REM Supprimer d'éventuels containers orphelins
docker stop luna-test happy_yalow elegant_gauss vigilant_lumiere 2>nul
docker rm luna-test happy_yalow elegant_gauss vigilant_lumiere 2>nul

echo.
echo 🚀 Démarrage de tous les services...
echo    - Luna Consciousness MCP Server
echo    - Redis (Cache)
echo    - Prometheus (Monitoring)
echo    - Grafana (Visualisation)
echo.

REM Démarrer tous les services (plus besoin de --profile maintenant!)
docker-compose up -d

if errorlevel 1 (
    echo ❌ Erreur lors du démarrage
    pause
    exit /b 1
)

echo.
echo ⏳ Attente du démarrage complet (15 secondes)...
timeout /t 15 /nobreak >nul

echo.
echo ═══════════════════════════════════════════════════════════
echo 📊 Status des Containers
echo ═══════════════════════════════════════════════════════════
docker-compose ps
echo.

echo ═══════════════════════════════════════════════════════════
echo 🔍 Vérification des Services
echo ═══════════════════════════════════════════════════════════

REM Tester les métriques Luna
echo.
echo 🌙 Luna Metrics:
curl -s http://localhost:8000/metrics | findstr "luna_phi_value" >nul
if errorlevel 1 (
    echo    ❌ Non accessible - Vérifier les logs: docker logs luna-consciousness
) else (
    echo    ✅ Accessible
    curl -s http://localhost:8000/metrics | findstr "luna_phi_value"
)

REM Tester Prometheus
echo.
echo 📈 Prometheus:
curl -s http://localhost:9090/-/healthy >nul 2>&1
if errorlevel 1 (
    echo    ❌ Non accessible
) else (
    echo    ✅ Accessible
)

REM Tester Grafana
echo.
echo 📉 Grafana:
curl -s http://localhost:3001 >nul 2>&1
if errorlevel 1 (
    echo    ❌ Non accessible
) else (
    echo    ✅ Accessible
)

REM Tester Redis
echo.
echo 🔴 Redis:
docker exec luna-redis redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo    ❌ Non accessible
) else (
    echo    ✅ Accessible
)

echo.
echo ═══════════════════════════════════════════════════════════
echo 🔗 Accès aux Services
echo ═══════════════════════════════════════════════════════════
echo.
echo   • Luna Metrics      : http://localhost:8000/metrics
echo   • Prometheus        : http://localhost:9090
echo   • Grafana           : http://localhost:3001
echo     └─ User/Pass      : admin / luna_consciousness
echo   • Redis             : localhost:6379
echo.
echo ═══════════════════════════════════════════════════════════
echo 📝 Commandes Utiles
echo ═══════════════════════════════════════════════════════════
echo.
echo   • Voir logs Luna    : docker logs -f luna-consciousness
echo   • Voir logs tous    : docker-compose logs -f
echo   • Arrêter tout      : docker-compose down
echo   • Status            : docker-compose ps
echo.
echo φ = 1.618033988749895 🌙
echo.
pause
