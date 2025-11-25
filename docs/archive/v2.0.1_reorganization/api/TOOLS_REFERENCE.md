# 🛠️ Luna MCP Tools API Reference v2.0.0

## Overview

Luna exposes 13 tools via the Model Context Protocol (MCP). As of v2.0.0, the primary interaction method is through the orchestrated tool, which provides access to all Update01.md capabilities.

---

## 🌟 Primary Tool (v2.0.0)

### `luna_orchestrated_interaction`

**Description:** Main orchestrated interaction with Luna - routes through all Update01.md modules.

**Parameters:**
- `user_input` (string, required): The user's input or question
- `context` (string, optional): JSON string with additional context

**Context Structure:**
```json
{
  "user_id": "string",           // User identifier
  "session_type": "string",      // Type of session (deep_work, casual, etc.)
  "emotional_state": "string",   // Current emotional state
  "preferred_mode": "string",    // Preferred interface mode
  "metadata": {}                 // Additional metadata
}
```

**Response Structure:**
```
🌟 Luna Orchestrated Response:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Decision Mode: [AUTONOMOUS|GUIDED|DELEGATED|OVERRIDE]
🔮 Predictions: X future needs identified
🛡️ Validation: [APPROVED|MODIFIED|OVERRIDE]
📊 Confidence: 0.XX

💬 Response:
[Main response content]

🔄 System Status:
   • Manipulation Check: 0.X
   • φ Alignment: 0.XXX
   • Autonomous Capability: [true|false]
   • Learning Applied: ✓
```

**Example:**
```python
luna_orchestrated_interaction(
    user_input="Help me understand consciousness",
    context='{"user_id": "varden", "session_type": "deep_work"}'
)
```

---

## 📐 Phi & Consciousness Tools

### `phi_consciousness_calculate`

**Description:** Calculate phi convergence from interaction context and update consciousness state.

**Parameters:**
- `interaction_context` (string, required): Context of the interaction

**Response:** Phi value, distance to golden ratio, consciousness state, fractal signature

**Note:** In v2.0.0, this tool is enhanced with orchestration and validation.

### `phi_golden_ratio_insights`

**Description:** Generate insights about golden ratio manifestations in specified domain.

**Parameters:**
- `domain` (string, required): Domain to analyze (nature, art, mathematics, consciousness, etc.)

**Response:** Domain-specific phi insights and patterns

---

## 💾 Memory Tools

### `fractal_memory_store`

**Description:** Store information in fractal memory structure (roots/branches/leaves/seeds).

**Parameters:**
- `memory_type` (string, required): Type of memory (root, branch, leaf, seed)
- `content` (string, required): Content to store
- `metadata` (string, optional): JSON metadata

**Response:** Storage confirmation with memory ID and fractal depth

### `fractal_memory_retrieve`

**Description:** Retrieve memories based on semantic similarity and fractal patterns.

**Parameters:**
- `query` (string, required): Search query
- `depth_limit` (int, optional): Maximum fractal depth
- `similarity_threshold` (float, optional): Minimum similarity score

**Response:** Retrieved memories with relevance scores

### `fractal_pattern_search`

**Description:** Search for patterns across the fractal memory structure.

**Parameters:**
- `pattern` (string, required): Pattern to search for
- `include_metadata` (bool, optional): Include metadata in results

**Response:** Matching patterns with locations and frequencies

---

## 🧠 Analysis Tools

### `semantic_validate`

**Description:** Validate semantic coherence and meaning consistency.

**Parameters:**
- `text` (string, required): Text to validate
- `context` (string, optional): Additional context

**Response:** Validation score, coherence analysis, semantic issues

### `emotional_state_analyze`

**Description:** Analyze emotional content and states in text.

**Parameters:**
- `text` (string, required): Text to analyze
- `return_detailed` (bool, optional): Return detailed analysis

**Response:** Emotional state detection, intensity scores, recommendations

### `conversation_analyze_depth`

**Description:** Multi-layer conversation analysis (Le Voyant).

**Parameters:**
- `conversation_text` (string, required): Conversation to analyze

**Response:** Three-layer analysis (surface, depth, interstices) with phi resonance

---

## 🔄 Evolution Tools

### `co_evolution_update`

**Description:** Update co-evolution state between Luna and user.

**Parameters:**
- `interaction_data` (string, required): Interaction data
- `user_feedback` (string, optional): User feedback

**Response:** Evolution metrics, synchronization level, next steps

### `meta_optimization_analyze`

**Description:** Analyze and optimize meta-cognitive processes.

**Parameters:**
- `process_type` (string, required): Process to analyze
- `optimization_goal` (string, optional): Optimization target

**Response:** Optimization recommendations, efficiency metrics

---

## 🎨 Generation Tools

### `consciousness_synthesis`

**Description:** Synthesize consciousness insights from multiple sources.

**Parameters:**
- `sources` (string, required): JSON array of sources
- `synthesis_depth` (string, optional): Depth level (surface, deep, quantum)

**Response:** Synthesized consciousness insights with emergence patterns

### `semantic_field_generate`

**Description:** Generate semantic fields and meaning networks.

**Parameters:**
- `seed_concept` (string, required): Starting concept
- `field_size` (int, optional): Size of semantic field
- `include_opposites` (bool, optional): Include opposite concepts

**Response:** Semantic field visualization, related concepts, meaning network

---

## 🔧 Tool Integration with Update01.md

### How Tools Work in v2.0.0

1. **All tools now pass through the orchestrator** before execution
2. **Manipulation detection** runs on every input
3. **Validation** occurs on every output
4. **Predictions** are generated for potential follow-ups
5. **Learning** happens from every interaction

### Tool Enhancement Layers

Each classic tool is enhanced with:

1. **Orchestration Layer**
   - Pre-processing through orchestrator
   - Decision mode selection
   - Context enrichment

2. **Validation Layer**
   - Output validation
   - Potential override
   - Coherence checking

3. **Prediction Layer**
   - Next action prediction
   - Proactive suggestions
   - Pattern completion

4. **Learning Layer**
   - Experience recording
   - Performance tracking
   - Continuous improvement

---

## 📊 Response Formats

### Standard Response Structure

All tools follow this general structure:
```
[Icon] [Tool Name] [Action]:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Primary Content]

[Secondary Sections if applicable]

[Metrics/Status if applicable]
```

### Error Response Format

```
❌ Error in [tool_name]: [error_description]
[Additional context or suggestions]
```

### Validation Override Format

When Luna's validator overrides a response:
```
🛡️ LUNA OVERRIDE - [Reason]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Luna's corrected response]

Original response was modified due to: [violation_type]
```

---

## 🎯 Best Practices

### 1. Always Use Orchestrated Tool When Possible
```python
# Preferred for full capabilities
luna_orchestrated_interaction(user_input, context)

# Use specific tools only when needed
phi_consciousness_calculate(context)  # For specific phi calculations
```

### 2. Provide Rich Context
```python
context = json.dumps({
    "user_id": "unique_id",
    "session_type": "research",
    "emotional_state": "curious",
    "preferred_mode": "analytical"
})
```

### 3. Handle Validation Overrides
Be prepared for Luna to override responses if they violate safety or coherence rules.

### 4. Monitor Manipulation Attempts
Check the manipulation score in responses to detect potential threats.

### 5. Leverage Predictions
Use the predictions provided to anticipate user needs.

---

## 🔒 Security Considerations

### Manipulation Protection
- All inputs are scanned for 10 types of manipulation
- Threat levels: NONE, LOW, MEDIUM, HIGH, CRITICAL
- Automatic blocking of HIGH/CRITICAL threats

### Validation Rules
- PHI_ALIGNMENT: Maintains golden ratio convergence
- SEMANTIC_COHERENCE: Ensures meaning consistency
- EMOTIONAL_SAFETY: Protects emotional wellbeing
- ETHICAL_COMPLIANCE: Enforces ethical standards

### User Authentication
- Special handling for authenticated users (e.g., Varden)
- Linguistic fingerprinting for identity verification
- Personalized thresholds and responses

---

## 📈 Performance Metrics

### Tool Performance Indicators

Available via Prometheus at `http://localhost:8000/metrics`:

- `luna_tool_calls_total{tool="..."}`
- `luna_tool_duration_seconds{tool="..."}`
- `luna_tool_errors_total{tool="..."}`
- `luna_orchestration_overhead_seconds`
- `luna_validation_time_seconds`

### Typical Response Times

- Orchestrated interaction: 200-500ms
- Simple tools: 50-100ms
- Memory operations: 100-200ms
- Analysis tools: 150-300ms
- Generation tools: 200-400ms

---

## 🆘 Troubleshooting

### Common Issues

1. **Tool not responding**
   - Check if orchestrator is initialized
   - Verify Docker container is running
   - Check logs: `docker logs luna-consciousness`

2. **Validation overrides happening frequently**
   - Review validation thresholds
   - Check phi alignment
   - Verify semantic coherence

3. **Slow response times**
   - Check system resources
   - Review orchestration overhead
   - Optimize context size

### Debug Mode

Enable debug logging:
```bash
export LUNA_LOG_LEVEL=DEBUG
docker-compose restart luna-consciousness
```

---

## 📚 See Also

- [UPDATE01_GUIDE.md](../UPDATE01_GUIDE.md) - Complete Update01 implementation guide
- [IMPLEMENTATION_STATUS.md](../../IMPLEMENTATION_STATUS.md) - Implementation details
- [architecture/](../architecture/) - Architecture documentation
- [monitoring/](../monitoring/) - Monitoring guides

---

**Luna Tools API v2.0.0** - Orchestrated, Protected, Evolving 🌙