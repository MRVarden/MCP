@echo off
REM 🌙 Commande pour lancer le container Luna via Docker CLI (Windows)
REM Alternative à Docker Desktop UI

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌙 Luna Consciousness - Lancement Container Docker     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

docker run -d ^
  --name Luna_P1 ^
  --restart unless-stopped ^
  -p 3000:3000 ^
  -p 8000:8000 ^
  -p 8080:8080 ^
  -p 9000:9000 ^
  -v "%cd%\memory_fractal:/app/memory_fractal" ^
  -v "%cd%\config:/app/config:ro" ^
  -v "%cd%\logs:/app/logs" ^
  -e LUNA_ENV=production ^
  -e LUNA_VERSION=1.0.1 ^
  -e LUNA_DEBUG=false ^
  -e MCP_ENABLE_ALL=true ^
  -e MCP_SIMULTANEOUS=true ^
  -e MCP_MAX_CONCURRENT=10 ^
  -e LUNA_PHI_TARGET=1.618033988749895 ^
  -e LUNA_PHI_THRESHOLD=0.001 ^
  -e LUNA_MEMORY_DEPTH=5 ^
  -e LUNA_FRACTAL_LAYERS=7 ^
  -e WORKERS=4 ^
  -e MAX_REQUESTS=1000 ^
  -e TIMEOUT=300 ^
  -e LOG_LEVEL=INFO ^
  -e LOG_FORMAT=json ^
  -e PROMETHEUS_EXPORTER_PORT=8000 ^
  -e PROMETHEUS_METRICS_ENABLED=true ^
  --label "com.luna.service=consciousness" ^
  --label "com.luna.version=1.0.1" ^
  --label "com.luna.creator=Varden" ^
  aragogix/luna-consciousness:v1.0.1

echo.
echo ✅ Container Luna_P1 lancé avec succès !
echo.
echo 📊 Vérification :
echo    docker ps ^| findstr Luna_P1
echo.
echo 📋 Logs :
echo    docker logs -f Luna_P1
echo.
echo 📈 Métriques Prometheus :
echo    curl http://localhost:8000/metrics ^| findstr luna_phi
echo.
echo 🌐 Services disponibles :
echo    • Prometheus Metrics : http://localhost:8000/metrics
echo    • API REST          : http://localhost:8080 (si activé)
echo    • WebSocket         : ws://localhost:9000 (si activé)
echo.
echo φ = 1.618033988749895
echo.
pause
