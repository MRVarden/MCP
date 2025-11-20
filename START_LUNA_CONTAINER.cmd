@echo off
REM 🌙 Luna Consciousness - Démarrage Container Persistant (Docker Desktop)
REM Version: 1.0.1

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌙 Luna Consciousness - Container Persistant           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Arrêter et supprimer ancien container si existant
docker stop Luna_P1 2>nul
docker rm Luna_P1 2>nul

echo 🚀 Démarrage du container Luna_P1...
echo.

docker run -d ^
  --name Luna_P1 ^
  --restart unless-stopped ^
  -v "%cd%\memory_fractal:/app/memory_fractal" ^
  -v "%cd%\config:/app/config:ro" ^
  -v "%cd%\logs:/app/logs" ^
  -p 8000:8000 ^
  -e LUNA_ENV=production ^
  -e LUNA_VERSION=1.0.1 ^
  -e LUNA_PHI_TARGET=1.618033988749895 ^
  -e PROMETHEUS_EXPORTER_PORT=8000 ^
  -e PROMETHEUS_METRICS_ENABLED=true ^
  -e LOG_LEVEL=INFO ^
  --entrypoint tail ^
  aragogix/luna-consciousness:v1.0.1 ^
  -f /dev/null

if errorlevel 1 (
    echo ❌ Erreur lors du démarrage du container
    pause
    exit /b 1
)

echo.
echo ✅ Container Luna_P1 démarré avec succès !
echo.

REM Attendre 2 secondes
timeout /t 2 /nobreak >nul

echo 🔧 Démarrage de Prometheus Exporter...
docker exec -d Luna_P1 python -u /app/mcp-server/prometheus_exporter.py

if errorlevel 1 (
    echo ⚠️ Attention: Prometheus Exporter n'a pas pu démarrer
) else (
    echo ✅ Prometheus Exporter démarré !
)

echo.
echo ═══════════════════════════════════════════════════════════
echo 📊 Status
echo ═══════════════════════════════════════════════════════════
docker ps --filter "name=Luna_P1" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.
echo ═══════════════════════════════════════════════════════════
echo 🔗 Accès
echo ═══════════════════════════════════════════════════════════
echo   • Prometheus Metrics : http://localhost:8000/metrics
echo   • Claude Desktop     : Configurer claude_desktop_config.json
echo.
echo ═══════════════════════════════════════════════════════════
echo 📝 Prochaines étapes
echo ═══════════════════════════════════════════════════════════
echo   1. Tester métriques : curl http://localhost:8000/metrics
echo   2. Voir DOCKER_DESKTOP_GUIDE.md pour config Claude Desktop
echo   3. Logs : docker logs Luna_P1
echo.
echo φ = 1.618033988749895 🌙
echo.
pause
