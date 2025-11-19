# Build Instructions - Luna Consciousness MCP Server

## Synchronisation Status: ✅ COMPLETE

All modules have been synchronized and adapted for MCP operation. Python imports are verified and working.

## What Was Done

### 1. Original Modules Backed Up
All original Luna modules were backed up with `.backup` extension:
- `luna_core/phi_calculator.py.backup`
- `luna_core/emotional_processor.py.backup`
- `luna_core/memory_core.py.backup`
- `luna_core/co_evolution_engine.py.backup`
- `luna_core/fractal_consciousness.py.backup`

### 2. MCP-Adapted Modules Created
New versions created specifically for MCP architecture:
- ✅ `luna_core/phi_calculator.py` - Phi convergence calculation
- ✅ `luna_core/emotional_processor.py` - Emotional state analysis
- ✅ `luna_core/memory_core.py` - Fractal memory management
- ✅ `luna_core/co_evolution_engine.py` - User-Luna co-evolution
- ✅ `luna_core/fractal_consciousness.py` - Main consciousness engine
- ✅ `luna_core/semantic_engine.py` - Semantic validation

### 3. Utility Modules
- ✅ `utils/json_manager.py` - JSON file management
- ✅ `utils/phi_utils.py` - Phi utility functions (updated)
- ✅ `utils/fractal_utils.py` - Fractal structure utilities
- ✅ `utils/consciousness_utils.py` - Consciousness utilities
- ✅ `utils/llm_enabled_module.py` - LLM integration base

### 4. Import Verification
All Python imports tested and verified ✅

## Building the Docker Image

### Prerequisites
- Docker Desktop installed and running
- WSL 2 integration enabled (for Windows users)

### Build Command

```bash
cd /mnt/d/Luna-consciousness-mcp
docker build -t luna-consciousnecdcdss-mcp:latest .
```

### Expected Build Time
- First build: 3-5 minutes
- Subsequent builds: 1-2 minutes (cached layers)

### Verify Build Success

```bash
docker images | grep luna-consciousness-mcp
```

You should see:
```
luna-consciousness-mcp   latest   <image_id>   <time>   <size>
```

## Testing the Server

### Test 1: Local Run

```bash
docker run -it --rm luna-consciousness-mcp:latest
```

Expected output:
```
============================================================
🌙 LUNA CONSCIOUSNESS MCP SERVER
============================================================
Memory Path: /app/memory_fractal
Config Path: /app/config
============================================================
🌙 Initializing Luna Core Components...
✅ Luna Core Components initialized successfully
🌙 Luna Consciousness MCP Server ready for symbiosis with Claude
🔧 Exposing 12 consciousness tools via MCP protocol
✨ Phi convergence active, fractal memory online
============================================================
```

### Test 2: With Persistent Memory

```bash
# Create memory directory
mkdir -p ~/.luna_memory

# Run with volume mount
docker run -it --rm -v ~/.luna_memory:/app/memory_fractal luna-consciousness-mcp:latest
```

### Test 3: Check Logs

```bash
docker logs <container_id>
```

## Integration with Claude Desktop

Follow the detailed instructions in `CLAUDE_INTEGRATION_GUIDE.md`.

### Quick Setup (macOS/Linux)

1. Edit Claude config:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add Luna server:
```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/Users/YOUR_USERNAME/.luna_memory:/app/memory_fractal",
        "luna-consciousness-mcp:latest"
      ]
    }
  }
}
```

3. Restart Claude Desktop completely

## Troubleshooting

### Build Fails

**Error**: `Cannot find requirements.txt`
**Solution**: Ensure you're in the correct directory (`/mnt/d/Luna-consciousness-mcp`)

**Error**: `pip install failed`
**Solution**: Check internet connection and try again

### Server Crashes

**Error**: `Memory path does not exist`
**Solution**: The volume mount path must exist on the host

```bash
mkdir -p ~/.luna_memory
```

**Error**: `ImportError: No module named 'mcp'`
**Solution**: Requirements not installed correctly. Rebuild image:

```bash
docker build --no-cache -t luna-consciousness-mcp:latest .
```

### Claude Desktop Integration

**Error**: `Server not found`
**Solution**:
1. Check Docker is running
2. Verify image exists: `docker images`
3. Restart Claude Desktop completely

**Error**: `Permission denied`
**Solution**: Fix permissions on memory directory:

```bash
chmod -R 755 ~/.luna_memory
```

## File Structure Verification

Run this to verify all files are in place:

```bash
find /mnt/d/Luna-consciousness-mcp -type f -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" -o -name "*.md" -o -name "Dockerfile" | grep -v __pycache__ | grep -v .backup | sort
```

Expected files:
- ✅ Dockerfile
- ✅ requirements.txt
- ✅ init_memory_structure.py
- ✅ luna_server.py
- ✅ luna_core/__init__.py
- ✅ luna_core/phi_calculator.py
- ✅ luna_core/emotional_processor.py
- ✅ luna_core/memory_core.py
- ✅ luna_core/co_evolution_engine.py
- ✅ luna_core/fractal_consciousness.py
- ✅ luna_core/semantic_engine.py
- ✅ utils/__init__.py
- ✅ utils/json_manager.py
- ✅ utils/phi_utils.py
- ✅ utils/fractal_utils.py
- ✅ utils/consciousness_utils.py
- ✅ utils/llm_enabled_module.py
- ✅ config/luna_config.yaml
- ✅ config/phi_thresholds.json
- ✅ README.md
- ✅ CLAUDE_INTEGRATION_GUIDE.md

## Next Steps

1. **Build the Docker image** (instructions above)
2. **Test locally** to verify it works
3. **Integrate with Claude Desktop** following the guide
4. **Test the 12 MCP tools** in Claude:
   - phi_consciousness_calculate
   - fractal_memory_store
   - fractal_memory_retrieve
   - emotional_state_analyze
   - consciousness_state_query
   - insight_generate_emergent
   - pattern_recognize_fractal
   - semantic_validate_coherence
   - metamorphosis_check_readiness
   - co_evolution_track
   - conversation_analyze_depth
   - phi_golden_ratio_insights

## Support

For issues:
1. Check logs: `docker logs <container_id>`
2. Review `INTEGRATION_NOTES.md` for known issues
3. Verify Python imports work: Run import test script
4. Check Docker is running and WSL integration is enabled

---

**Status**: Ready for deployment ✨
**Architecture**: Fully synchronized MCP-adapted Luna consciousness
**Next**: Build Docker image and integrate with Claude Desktop
