"""
Luna Consciousness - Performance Tests
======================================

This package contains performance tests to validate latency requirements
for the Pure Memory system and other critical components.

Latency Requirements:
- Buffer (Level 1): < 1ms
- Fractal (Level 2): < 10ms
- Archive (Level 3): < 100ms

Usage:
    pytest tests/performance/ -v --benchmark-only
    pytest tests/performance/ -v -m performance
"""
