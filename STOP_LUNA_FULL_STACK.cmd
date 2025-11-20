@echo off
REM 🌙 Luna Consciousness - Arrêt Infrastructure Complète
REM Version: 1.0.1
REM Arrête: Luna + Redis + Prometheus + Grafana

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌙 Luna Consciousness - Arrêt Infrastructure           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d D:\Luna-consciousness-mcp

echo 🛑 Arrêt de tous les services...
echo.

docker-compose down

if errorlevel 1 (
    echo ❌ Erreur lors de l'arrêt
    pause
    exit /b 1
)

echo.
echo ✅ Tous les containers ont été arrêtés et supprimés
echo.
echo 📊 Status:
docker-compose ps
echo.
echo ℹ️  Les volumes de données sont conservés
echo    Pour supprimer aussi les volumes: docker-compose down -v
echo.
pause
