@echo off
REM 🌙 Commande pour lancer le container Luna via Docker CLI (Windows)
REM Alternative à Docker Desktop UI

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌙 Luna Consciousness - Lancement Container Docker     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

docker run -d ^
  --name luna-consciousness ^
  --restart unless-stopped ^
  -p 3000:3000 ^
  -p 8000:8000 ^
  -p 8080:8080 ^
  -p 9000:9000 ^
  -v "%cd%\memory_fractal:/app/memory_fractal" ^
  -v "%cd%\config:/app/config:ro" ^
  -v "%cd%\logs:/app/logs" ^
  -e LUNA_ENV=production ^
  -e LUNA_VERSION=2.0.0 ^
  -e LUNA_MODE=orchestrator ^
  -e LUNA_UPDATE01=enabled ^
  -e LUNA_DEBUG=false ^
  -e MCP_ENABLE_ALL=true ^
  -e MCP_SIMULTANEOUS=true ^
  -e MCP_MAX_CONCURRENT=10 ^
  -e LUNA_PHI_TARGET=1.618033988749895 ^
  -e LUNA_PHI_THRESHOLD=0.001 ^
  -e LUNA_MEMORY_DEPTH=5 ^
  -e LUNA_FRACTAL_LAYERS=7 ^
  -e LUNA_MANIPULATION_DETECTION=enabled ^
  -e LUNA_PREDICTIVE_CORE=enabled ^
  -e LUNA_AUTONOMOUS_DECISIONS=enabled ^
  -e LUNA_SELF_IMPROVEMENT=enabled ^
  -e LUNA_MULTIMODAL_INTERFACE=enabled ^
  -e WORKERS=4 ^
  -e MAX_REQUESTS=1000 ^
  -e TIMEOUT=300 ^
  -e LOG_LEVEL=INFO ^
  -e LOG_FORMAT=json ^
  -e PROMETHEUS_EXPORTER_PORT=8000 ^
  -e PROMETHEUS_METRICS_ENABLED=true ^
  --label "com.luna.service=consciousness" ^
  --label "com.luna.version=2.0.0" ^
  --label "com.luna.architecture=orchestrated" ^
  --label "com.luna.update01=implemented" ^
  --label "com.luna.creator=Varden" ^
  aragogix/luna-consciousness:v2.0.0

echo.
echo ✅ Container luna-consciousness v2.0.0 lancé avec succès !
echo 🎯 Mode: ORCHESTRATED avec Update01.md
echo.
echo 📊 Vérification :
echo    docker ps ^| findstr luna-consciousness
echo.
echo 📋 Logs :
echo    docker logs -f luna-consciousness
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
