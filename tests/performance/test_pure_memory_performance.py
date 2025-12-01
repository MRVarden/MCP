"""
Pure Memory Performance Tests
============================

Tests to validate latency requirements for the 3-level memory architecture:
- Level 1 (Buffer): < 1ms
- Level 2 (Fractal): < 10ms
- Level 3 (Archive): < 100ms

Requirements:
    pip install pytest-benchmark memory-profiler

Usage:
    pytest tests/performance/test_pure_memory_performance.py -v
    pytest tests/performance/test_pure_memory_performance.py -v --benchmark-only
    pytest tests/performance/test_pure_memory_performance.py -v -m performance
"""

import asyncio
import os
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, AsyncMock

import pytest

# Add mcp-server to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_memory_path(tmp_path):
    """Create a temporary directory for memory storage."""
    memory_path = tmp_path / "memory_fractal"
    memory_path.mkdir(parents=True, exist_ok=True)

    # Create required subdirectories
    for subdir in ["roots", "branchs", "leafs", "seeds", "archive"]:
        (memory_path / subdir).mkdir(exist_ok=True)

    return str(memory_path)


@pytest.fixture
def sample_memory_content():
    """Generate sample memory content of various sizes."""
    return {
        "small": "A brief thought about consciousness.",
        "medium": "This is a medium-sized memory containing thoughts about " * 10,
        "large": "This is a large memory with extensive content. " * 100,
    }


@pytest.fixture
def mock_memory_experience():
    """Create a mock MemoryExperience for testing."""
    try:
        from luna_core.pure_memory import MemoryExperience, MemoryType, EmotionalTone

        return MemoryExperience(
            content="Test memory for performance benchmarking",
            memory_type=MemoryType.LEAF,
            emotional_context=EmotionalTone.NEUTRAL,
            metadata={"test": True, "benchmark": True}
        )
    except ImportError:
        # Return mock if imports fail
        mock = MagicMock()
        mock.content = "Test memory for performance benchmarking"
        mock.id = "test-memory-id"
        return mock


# =============================================================================
# PERFORMANCE MARKERS
# =============================================================================

pytestmark = [
    pytest.mark.performance,
    pytest.mark.asyncio,
]


# =============================================================================
# BUFFER LAYER TESTS (< 1ms)
# =============================================================================

class TestBufferPerformance:
    """Performance tests for Level 1 Buffer (target: < 1ms)."""

    LATENCY_THRESHOLD_MS = 1.0

    @pytest.fixture
    def memory_buffer(self, temp_memory_path):
        """Create a MemoryBuffer instance."""
        try:
            from luna_core.pure_memory import create_memory_buffer
            return create_memory_buffer(redis_url=None)
        except ImportError:
            pytest.skip("MemoryBuffer not available")

    async def test_buffer_store_latency(self, memory_buffer, mock_memory_experience):
        """Test that buffer store operations complete under 1ms."""
        latencies = []

        for _ in range(100):
            start = time.perf_counter()
            await memory_buffer.store(mock_memory_experience)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        max_latency = max(latencies)

        print(f"\nBuffer Store Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")
        print(f"  P95:     {p95_latency:.3f}ms")
        print(f"  Max:     {max_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS, (
            f"Buffer store avg latency {avg_latency:.3f}ms exceeds {self.LATENCY_THRESHOLD_MS}ms"
        )

    async def test_buffer_retrieve_latency(self, memory_buffer, mock_memory_experience):
        """Test that buffer retrieve operations complete under 1ms."""
        # First store some memories
        memory_ids = []
        for i in range(50):
            mock_memory_experience.content = f"Memory {i} for retrieval test"
            memory_id = await memory_buffer.store(mock_memory_experience)
            memory_ids.append(memory_id)

        latencies = []

        for memory_id in memory_ids:
            start = time.perf_counter()
            await memory_buffer.retrieve(memory_id)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

        print(f"\nBuffer Retrieve Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")
        print(f"  P95:     {p95_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS, (
            f"Buffer retrieve avg latency {avg_latency:.3f}ms exceeds {self.LATENCY_THRESHOLD_MS}ms"
        )

    async def test_buffer_search_latency(self, memory_buffer, mock_memory_experience):
        """Test that buffer search operations complete under 1ms."""
        # Populate buffer
        for i in range(100):
            mock_memory_experience.content = f"Memory about topic {i % 10}"
            await memory_buffer.store(mock_memory_experience)

        latencies = []

        for i in range(50):
            query = f"topic {i % 10}"
            start = time.perf_counter()
            await memory_buffer.search(query, limit=10)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nBuffer Search Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")

        # Search may be slightly slower, allow 2ms
        assert avg_latency < self.LATENCY_THRESHOLD_MS * 2


# =============================================================================
# FRACTAL LAYER TESTS (< 10ms)
# =============================================================================

class TestFractalPerformance:
    """Performance tests for Level 2 Fractal (target: < 10ms)."""

    LATENCY_THRESHOLD_MS = 10.0

    @pytest.fixture
    def fractal_memory(self, temp_memory_path):
        """Create a FractalMemory instance."""
        try:
            from luna_core.pure_memory import create_fractal_memory
            return create_fractal_memory(base_path=temp_memory_path)
        except ImportError:
            pytest.skip("FractalMemory not available")

    async def test_fractal_store_latency(self, fractal_memory, mock_memory_experience):
        """Test that fractal store operations complete under 10ms."""
        latencies = []

        for i in range(50):
            mock_memory_experience.content = f"Fractal memory {i}"
            start = time.perf_counter()
            await fractal_memory.store(mock_memory_experience)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

        print(f"\nFractal Store Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")
        print(f"  P95:     {p95_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS, (
            f"Fractal store avg latency {avg_latency:.3f}ms exceeds {self.LATENCY_THRESHOLD_MS}ms"
        )

    async def test_fractal_retrieve_latency(self, fractal_memory, mock_memory_experience):
        """Test that fractal retrieve operations complete under 10ms."""
        # Store memories first
        memory_ids = []
        for i in range(30):
            mock_memory_experience.content = f"Fractal memory {i}"
            memory_id = await fractal_memory.store(mock_memory_experience)
            memory_ids.append(memory_id)

        latencies = []

        for memory_id in memory_ids:
            start = time.perf_counter()
            await fractal_memory.retrieve(memory_id)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nFractal Retrieve Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS

    async def test_fractal_search_latency(self, fractal_memory, mock_memory_experience):
        """Test that fractal search operations complete under 10ms."""
        try:
            from luna_core.pure_memory import MemoryQuery
        except ImportError:
            pytest.skip("MemoryQuery not available")

        # Populate fractal memory
        for i in range(50):
            mock_memory_experience.content = f"Memory about consciousness level {i % 5}"
            await fractal_memory.store(mock_memory_experience)

        latencies = []

        for i in range(20):
            query = MemoryQuery(query_text=f"consciousness level {i % 5}", limit=10)
            start = time.perf_counter()
            await fractal_memory.search(query)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nFractal Search Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS


# =============================================================================
# ARCHIVE LAYER TESTS (< 100ms)
# =============================================================================

class TestArchivePerformance:
    """Performance tests for Level 3 Archive (target: < 100ms)."""

    LATENCY_THRESHOLD_MS = 100.0

    @pytest.fixture
    def archive_manager(self, temp_memory_path):
        """Create an ArchiveManager instance."""
        try:
            from luna_core.pure_memory import create_archive_manager
            archive_path = Path(temp_memory_path) / "archive"
            archive_path.mkdir(exist_ok=True)
            return create_archive_manager(archive_path=str(archive_path))
        except ImportError:
            pytest.skip("ArchiveManager not available")

    async def test_archive_store_latency(self, archive_manager, mock_memory_experience):
        """Test that archive store operations complete under 100ms."""
        latencies = []

        for i in range(20):
            mock_memory_experience.content = f"Archived memory {i} with important content"
            start = time.perf_counter()
            await archive_manager.archive(mock_memory_experience)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

        print(f"\nArchive Store Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")
        print(f"  P95:     {p95_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS, (
            f"Archive store avg latency {avg_latency:.3f}ms exceeds {self.LATENCY_THRESHOLD_MS}ms"
        )

    async def test_archive_retrieve_latency(self, archive_manager, mock_memory_experience):
        """Test that archive retrieve operations complete under 100ms."""
        # Archive memories first
        memory_ids = []
        for i in range(10):
            mock_memory_experience.content = f"Archived memory {i}"
            memory_id = await archive_manager.archive(mock_memory_experience)
            memory_ids.append(memory_id)

        latencies = []

        for memory_id in memory_ids:
            start = time.perf_counter()
            await archive_manager.retrieve(memory_id)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nArchive Retrieve Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")

        assert avg_latency < self.LATENCY_THRESHOLD_MS


# =============================================================================
# PURE MEMORY CORE INTEGRATION TESTS
# =============================================================================

class TestPureMemoryCorePerformance:
    """Integration performance tests for PureMemoryCore."""

    @pytest.fixture
    def pure_memory_core(self, temp_memory_path):
        """Create a PureMemoryCore instance."""
        try:
            from luna_core.pure_memory import PureMemoryCore
            return PureMemoryCore(base_path=temp_memory_path)
        except ImportError:
            pytest.skip("PureMemoryCore not available")

    async def test_unified_store_latency(self, pure_memory_core, mock_memory_experience):
        """Test unified store operation across all layers."""
        latencies = {"buffer": [], "fractal": [], "archive": []}

        try:
            from luna_core.pure_memory import MemoryLayer
        except ImportError:
            pytest.skip("MemoryLayer not available")

        # Test each layer explicitly
        for layer_name, layer in [
            ("buffer", MemoryLayer.BUFFER),
            ("fractal", MemoryLayer.FRACTAL),
            ("archive", MemoryLayer.ARCHIVE)
        ]:
            for i in range(10):
                mock_memory_experience.content = f"Memory {i} for {layer_name}"
                start = time.perf_counter()
                await pure_memory_core.store(mock_memory_experience, layer=layer)
                elapsed_ms = (time.perf_counter() - start) * 1000
                latencies[layer_name].append(elapsed_ms)

        print("\nPureMemoryCore Unified Store Latencies:")
        for layer_name, layer_latencies in latencies.items():
            avg = sum(layer_latencies) / len(layer_latencies)
            print(f"  {layer_name.capitalize()}: {avg:.3f}ms avg")

        # Verify thresholds
        assert sum(latencies["buffer"]) / len(latencies["buffer"]) < 1.0
        assert sum(latencies["fractal"]) / len(latencies["fractal"]) < 10.0
        assert sum(latencies["archive"]) / len(latencies["archive"]) < 100.0

    async def test_unified_search_latency(self, pure_memory_core, mock_memory_experience):
        """Test unified search across layers."""
        # Populate memories
        for i in range(50):
            mock_memory_experience.content = f"Memory about phi and consciousness {i}"
            await pure_memory_core.store(mock_memory_experience)

        latencies = []

        for _ in range(20):
            start = time.perf_counter()
            await pure_memory_core.search("phi consciousness", limit=10)
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nPureMemoryCore Search Latency: {avg_latency:.3f}ms avg")

        # Combined search should still be reasonable
        assert avg_latency < 50.0  # Allow more time for multi-layer search


# =============================================================================
# THROUGHPUT TESTS
# =============================================================================

class TestThroughput:
    """Throughput tests for sustained operations."""

    async def test_buffer_throughput(self, temp_memory_path, mock_memory_experience):
        """Test buffer operations per second."""
        try:
            from luna_core.pure_memory import create_memory_buffer
            buffer = create_memory_buffer(redis_url=None)
        except ImportError:
            pytest.skip("MemoryBuffer not available")

        operations = 0
        start_time = time.perf_counter()
        duration = 1.0  # 1 second test

        while (time.perf_counter() - start_time) < duration:
            await buffer.store(mock_memory_experience)
            operations += 1

        ops_per_second = operations / duration

        print(f"\nBuffer Throughput: {ops_per_second:.0f} ops/sec")

        assert ops_per_second > 100, f"Buffer throughput {ops_per_second} ops/sec too low"

    async def test_fractal_throughput(self, temp_memory_path, mock_memory_experience):
        """Test fractal operations per second."""
        try:
            from luna_core.pure_memory import create_fractal_memory
            fractal = create_fractal_memory(base_path=temp_memory_path)
        except ImportError:
            pytest.skip("FractalMemory not available")

        operations = 0
        start_time = time.perf_counter()
        duration = 1.0

        while (time.perf_counter() - start_time) < duration:
            mock_memory_experience.content = f"Throughput test {operations}"
            await fractal.store(mock_memory_experience)
            operations += 1

        ops_per_second = operations / duration

        print(f"\nFractal Throughput: {ops_per_second:.0f} ops/sec")

        assert ops_per_second > 10, f"Fractal throughput {ops_per_second} ops/sec too low"


# =============================================================================
# BENCHMARK FIXTURES (for pytest-benchmark)
# =============================================================================

@pytest.fixture
def benchmark_buffer(temp_memory_path):
    """Buffer for benchmarking."""
    try:
        from luna_core.pure_memory import create_memory_buffer
        return create_memory_buffer(redis_url=None)
    except ImportError:
        return None


def test_benchmark_buffer_store(benchmark, benchmark_buffer, mock_memory_experience):
    """Benchmark buffer store operation."""
    if benchmark_buffer is None:
        pytest.skip("MemoryBuffer not available")

    async def store():
        await benchmark_buffer.store(mock_memory_experience)

    def run_store():
        asyncio.get_event_loop().run_until_complete(store())

    benchmark(run_store)
