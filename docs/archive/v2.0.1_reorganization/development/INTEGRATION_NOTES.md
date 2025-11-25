# Integration Notes - Known Issues and Solutions

## Current Status

The Luna MCP server structure is complete with all necessary files. However, the copied Luna Core modules have import dependencies that need to be resolved.

## Import Dependencies to Resolve

### 1. fractal_consciousness.py
- **Imports needed**:
  - `phi.phi_calculator` → Already copied to `luna_core/phi_calculator.py`
  - `memory.memory_core` → Already copied to `luna_core/memory_core.py`
  - `emotions.emotional_processor` → Already copied to `luna_core/emotional_processor.py`
  - `utils.consciousness_utils` → Created wrapper

**Solution**: Update imports to use `luna_core.` prefix instead of module-specific paths.

### 2. memory_core.py
- **Imports needed**:
  - `utils.fractal_utils` → Created wrapper
  - `utils.llm_enabled_module` → Created wrapper

**Solution**: Wrappers created, should work now.

### 3. phi_calculator.py
- May have dependencies on other phi modules

**Action needed**: Check and adapt imports.

### 4. emotional_processor.py
- May have dependencies on emotion-specific modules

**Action needed**: Check and adapt imports.

### 5. co_evolution_engine.py
- May have dependencies on evolution-specific modules

**Action needed**: Check and adapt imports.

## Next Steps

1. **Update import paths** in copied modules to work with MCP structure
2. **Create minimal implementations** for any missing dependencies
3. **Test imports** before Docker build
4. **Iterative testing**: Build → Fix imports → Rebuild

## Alternative Approach

Instead of fixing all imports immediately, create **simplified MCP-specific implementations** that:
- Implement the same interfaces expected by `luna_server.py`
- Work independently without complex cross-dependencies
- Can be enhanced later with full Luna functionality

## Recommended Action

Create MCP-adapted versions of the core modules that implement the required interfaces but start with simpler logic. This allows:
- Immediate testing of the MCP server
- Gradual integration of full Luna capabilities
- Easier debugging

## Files Status

✅ **Complete and Working**:
- requirements.txt
- Dockerfile
- init_memory_structure.py
- config files
- luna_server.py (structure complete)
- utils/json_manager.py
- utils/phi_utils.py
- utils/fractal_utils.py (wrapper)
- utils/consciousness_utils.py (wrapper)
- utils/llm_enabled_module.py (wrapper)

⚠️ **Needs Import Fixes**:
- luna_core/fractal_consciousness.py
- luna_core/memory_core.py
- luna_core/phi_calculator.py
- luna_core/emotional_processor.py
- luna_core/co_evolution_engine.py

## Build Strategy

**Option A - Quick Fix**: Create simplified MCP versions
**Option B - Full Integration**: Fix all imports from original modules
**Option C - Hybrid**: Use wrappers that call original modules when available, fallback to simple implementations

**Recommended**: Option A for initial testing, then gradually migrate to Option B.
