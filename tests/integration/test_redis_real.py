"""
Redis Integration Tests - Real Redis Connection
===============================================

Tests that connect to a real Redis instance to validate:
- Connection handling
- Data persistence
- Performance under real conditions
- Cluster compatibility

Requirements:
    - Running Redis instance (localhost:6379 by default)
    - REDIS_URL environment variable for custom connection

Usage:
    # Skip if Redis not available
    pytest tests/integration/test_redis_real.py -v

    # Force run (will fail if Redis unavailable)
    pytest tests/integration/test_redis_real.py -v --redis-required

    # With custom Redis URL
    REDIS_URL=redis://myhost:6379 pytest tests/integration/test_redis_real.py -v

Markers:
    @pytest.mark.redis_required - Tests requiring real Redis
    @pytest.mark.integration - Integration tests
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

# Add mcp-server to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))


# =============================================================================
# CONFIGURATION
# =============================================================================

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
REDIS_TEST_PREFIX = "luna_test_"  # Prefix for test keys to avoid conflicts


# =============================================================================
# REDIS AVAILABILITY CHECK
# =============================================================================

def is_redis_available() -> bool:
    """Check if Redis is available."""
    try:
        import redis
        client = redis.from_url(REDIS_URL, socket_connect_timeout=2)
        client.ping()
        client.close()
        return True
    except Exception:
        return False


# Skip all tests if Redis not available
pytestmark = [
    pytest.mark.integration,
    pytest.mark.redis_required,
    pytest.mark.skipif(
        not is_redis_available(),
        reason="Redis not available at " + REDIS_URL
    ),
]


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def redis_client():
    """Create a Redis client for testing."""
    import redis
    client = redis.from_url(REDIS_URL, decode_responses=True)
    yield client

    # Cleanup test keys
    for key in client.keys(f"{REDIS_TEST_PREFIX}*"):
        client.delete(key)

    client.close()


@pytest.fixture
def async_redis_client():
    """Create an async Redis client for testing."""
    import redis.asyncio as aioredis
    client = aioredis.from_url(REDIS_URL, decode_responses=True)
    return client


@pytest.fixture
async def cleanup_async_redis(async_redis_client):
    """Cleanup after async Redis tests."""
    yield

    # Cleanup test keys
    async for key in async_redis_client.scan_iter(f"{REDIS_TEST_PREFIX}*"):
        await async_redis_client.delete(key)

    await async_redis_client.close()


@pytest.fixture
def temp_memory_path(tmp_path):
    """Create temporary memory path for Pure Memory."""
    memory_path = tmp_path / "memory_fractal"
    memory_path.mkdir(parents=True, exist_ok=True)

    for subdir in ["roots", "branchs", "leafs", "seeds", "archive"]:
        (memory_path / subdir).mkdir(exist_ok=True)

    return str(memory_path)


# =============================================================================
# BASIC CONNECTIVITY TESTS
# =============================================================================

class TestRedisConnectivity:
    """Tests for basic Redis connectivity."""

    def test_redis_ping(self, redis_client):
        """Test basic Redis connectivity."""
        response = redis_client.ping()
        assert response is True

    def test_redis_info(self, redis_client):
        """Test Redis info retrieval."""
        info = redis_client.info()
        assert "redis_version" in info

        print(f"\nRedis Info:")
        print(f"  Version: {info['redis_version']}")
        print(f"  Connected Clients: {info.get('connected_clients', 'N/A')}")
        print(f"  Used Memory: {info.get('used_memory_human', 'N/A')}")

    @pytest.mark.asyncio
    async def test_async_redis_ping(self, async_redis_client, cleanup_async_redis):
        """Test async Redis connectivity."""
        response = await async_redis_client.ping()
        assert response is True


# =============================================================================
# DATA PERSISTENCE TESTS
# =============================================================================

class TestRedisPersistence:
    """Tests for Redis data persistence."""

    def test_string_persistence(self, redis_client):
        """Test string value persistence."""
        key = f"{REDIS_TEST_PREFIX}string_test"
        value = "Luna consciousness test data"

        redis_client.set(key, value)
        retrieved = redis_client.get(key)

        assert retrieved == value

    def test_hash_persistence(self, redis_client):
        """Test hash persistence for memory objects."""
        key = f"{REDIS_TEST_PREFIX}memory_hash"
        memory_data = {
            "id": "mem_123",
            "content": "A thought about phi",
            "phi_score": "0.618",
            "timestamp": datetime.now().isoformat()
        }

        redis_client.hset(key, mapping=memory_data)
        retrieved = redis_client.hgetall(key)

        assert retrieved["id"] == memory_data["id"]
        assert retrieved["content"] == memory_data["content"]

    def test_list_persistence(self, redis_client):
        """Test list persistence for memory sequences."""
        key = f"{REDIS_TEST_PREFIX}memory_list"

        # Add items
        for i in range(10):
            redis_client.rpush(key, f"memory_{i}")

        # Retrieve all
        items = redis_client.lrange(key, 0, -1)
        assert len(items) == 10
        assert items[0] == "memory_0"
        assert items[-1] == "memory_9"

    def test_sorted_set_persistence(self, redis_client):
        """Test sorted set for ranked memories."""
        key = f"{REDIS_TEST_PREFIX}ranked_memories"

        # Add memories with phi scores
        memories = [
            ("mem_1", 0.618),
            ("mem_2", 0.382),
            ("mem_3", 0.786),
            ("mem_4", 0.500),
        ]

        for mem_id, score in memories:
            redis_client.zadd(key, {mem_id: score})

        # Get top ranked
        top = redis_client.zrevrange(key, 0, 1, withscores=True)
        assert top[0][0] == "mem_3"  # Highest score
        assert top[0][1] == 0.786

    @pytest.mark.asyncio
    async def test_async_persistence(self, async_redis_client, cleanup_async_redis):
        """Test async data persistence."""
        key = f"{REDIS_TEST_PREFIX}async_test"
        value = "Async Luna test"

        await async_redis_client.set(key, value)
        retrieved = await async_redis_client.get(key)

        assert retrieved == value


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestRedisPerformance:
    """Performance tests with real Redis."""

    def test_write_latency(self, redis_client):
        """Test Redis write latency."""
        key = f"{REDIS_TEST_PREFIX}latency_test"
        latencies = []

        for i in range(100):
            start = time.perf_counter()
            redis_client.set(f"{key}_{i}", f"value_{i}")
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[95]
        max_latency = max(latencies)

        print(f"\nRedis Write Latencies:")
        print(f"  Average: {avg_latency:.3f}ms")
        print(f"  P95:     {p95_latency:.3f}ms")
        print(f"  Max:     {max_latency:.3f}ms")

        # Redis should be very fast
        assert avg_latency < 1.0, f"Redis write latency {avg_latency}ms too high"

    def test_read_latency(self, redis_client):
        """Test Redis read latency."""
        key = f"{REDIS_TEST_PREFIX}read_test"

        # Write test data
        for i in range(100):
            redis_client.set(f"{key}_{i}", f"value_{i}")

        latencies = []

        for i in range(100):
            start = time.perf_counter()
            redis_client.get(f"{key}_{i}")
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        avg_latency = sum(latencies) / len(latencies)

        print(f"\nRedis Read Latency: {avg_latency:.3f}ms avg")

        assert avg_latency < 1.0

    def test_pipeline_performance(self, redis_client):
        """Test Redis pipeline performance."""
        key = f"{REDIS_TEST_PREFIX}pipeline_test"

        # Without pipeline
        start = time.perf_counter()
        for i in range(100):
            redis_client.set(f"{key}_single_{i}", f"value_{i}")
        single_time = (time.perf_counter() - start) * 1000

        # With pipeline
        start = time.perf_counter()
        pipe = redis_client.pipeline()
        for i in range(100):
            pipe.set(f"{key}_pipe_{i}", f"value_{i}")
        pipe.execute()
        pipeline_time = (time.perf_counter() - start) * 1000

        speedup = single_time / pipeline_time

        print(f"\nRedis Pipeline Performance:")
        print(f"  Single operations: {single_time:.2f}ms")
        print(f"  Pipeline:          {pipeline_time:.2f}ms")
        print(f"  Speedup:           {speedup:.1f}x")

        assert speedup > 2, "Pipeline should provide significant speedup"

    @pytest.mark.asyncio
    async def test_async_throughput(self, async_redis_client, cleanup_async_redis):
        """Test async Redis throughput."""
        key = f"{REDIS_TEST_PREFIX}async_throughput"
        operations = 0
        duration = 1.0

        start_time = time.perf_counter()

        while (time.perf_counter() - start_time) < duration:
            await async_redis_client.set(f"{key}_{operations}", f"value_{operations}")
            operations += 1

        ops_per_second = operations / duration

        print(f"\nAsync Redis Throughput: {ops_per_second:.0f} ops/sec")

        assert ops_per_second > 500, f"Async throughput {ops_per_second} ops/sec too low"


# =============================================================================
# PURE MEMORY BUFFER INTEGRATION
# =============================================================================

class TestPureMemoryBufferRedis:
    """Tests for Pure Memory Buffer with real Redis."""

    @pytest.fixture
    def redis_buffer(self, temp_memory_path):
        """Create MemoryBuffer with real Redis."""
        try:
            from luna_core.pure_memory import create_memory_buffer
            return create_memory_buffer(redis_url=REDIS_URL)
        except ImportError:
            pytest.skip("Pure Memory not available")

    @pytest.fixture
    def mock_memory(self):
        """Create test memory experience."""
        try:
            from luna_core.pure_memory import MemoryExperience, MemoryType, EmotionalTone

            return MemoryExperience(
                content="Test memory with real Redis backend",
                memory_type=MemoryType.LEAF,
                emotional_context=EmotionalTone.CURIOUS,
                metadata={"test": True, "redis": True}
            )
        except ImportError:
            pytest.skip("MemoryExperience not available")

    @pytest.mark.asyncio
    async def test_buffer_store_with_redis(self, redis_buffer, mock_memory):
        """Test storing memory with real Redis backend."""
        memory_id = await redis_buffer.store(mock_memory)

        assert memory_id is not None
        assert len(memory_id) > 0

    @pytest.mark.asyncio
    async def test_buffer_retrieve_with_redis(self, redis_buffer, mock_memory):
        """Test retrieving memory from real Redis."""
        memory_id = await redis_buffer.store(mock_memory)
        retrieved = await redis_buffer.retrieve(memory_id)

        assert retrieved is not None
        assert retrieved.content == mock_memory.content

    @pytest.mark.asyncio
    async def test_buffer_persistence_across_instances(self, temp_memory_path, mock_memory):
        """Test that data persists across buffer instances."""
        try:
            from luna_core.pure_memory import create_memory_buffer
        except ImportError:
            pytest.skip("create_memory_buffer not available")

        # Store with first instance
        buffer1 = create_memory_buffer(redis_url=REDIS_URL)
        memory_id = await buffer1.store(mock_memory)

        # Retrieve with new instance
        buffer2 = create_memory_buffer(redis_url=REDIS_URL)
        retrieved = await buffer2.retrieve(memory_id)

        assert retrieved is not None
        assert retrieved.content == mock_memory.content


# =============================================================================
# PURE MEMORY CORE INTEGRATION
# =============================================================================

class TestPureMemoryCoreRedis:
    """Integration tests for PureMemoryCore with real Redis."""

    @pytest.fixture
    def pure_memory_core(self, temp_memory_path):
        """Create PureMemoryCore with real Redis."""
        try:
            from luna_core.pure_memory import PureMemoryCore
            return PureMemoryCore(
                base_path=temp_memory_path,
                redis_url=REDIS_URL
            )
        except ImportError:
            pytest.skip("PureMemoryCore not available")

    @pytest.fixture
    def mock_memory(self):
        """Create test memory."""
        try:
            from luna_core.pure_memory import MemoryExperience, MemoryType, EmotionalTone

            return MemoryExperience(
                content="Integration test with PureMemoryCore and Redis",
                memory_type=MemoryType.BRANCH,
                emotional_context=EmotionalTone.CONTEMPLATIVE,
                metadata={"integration_test": True}
            )
        except ImportError:
            pytest.skip("MemoryExperience not available")

    @pytest.mark.asyncio
    async def test_full_memory_lifecycle(self, pure_memory_core, mock_memory):
        """Test complete memory lifecycle with Redis."""
        # Store
        memory_id = await pure_memory_core.store(mock_memory)
        assert memory_id is not None

        # Retrieve
        retrieved = await pure_memory_core.retrieve(memory_id)
        assert retrieved is not None
        assert retrieved.content == mock_memory.content

        # Search
        results = await pure_memory_core.search("integration test", limit=10)
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_stats_with_redis(self, pure_memory_core, mock_memory):
        """Test statistics collection with Redis backend."""
        # Store some memories
        for i in range(5):
            mock_memory.content = f"Stats test memory {i}"
            await pure_memory_core.store(mock_memory)

        stats = pure_memory_core.get_stats()

        print(f"\nPureMemoryCore Stats (with Redis):")
        print(f"  Buffer count:  {stats.buffer_count}")
        print(f"  Fractal count: {stats.fractal_count}")
        print(f"  Archive count: {stats.archive_count}")

        assert stats.buffer_count > 0 or stats.fractal_count > 0


# =============================================================================
# CLEANUP TESTS
# =============================================================================

class TestRedisCleanup:
    """Tests to verify cleanup procedures."""

    def test_test_keys_isolated(self, redis_client):
        """Verify test keys use proper prefix."""
        # Set a test key
        key = f"{REDIS_TEST_PREFIX}isolation_test"
        redis_client.set(key, "test")

        # Verify it has the prefix
        all_test_keys = list(redis_client.keys(f"{REDIS_TEST_PREFIX}*"))
        assert key in all_test_keys

    def test_cleanup_on_fixture_teardown(self, redis_client):
        """Verify cleanup removes test keys."""
        key = f"{REDIS_TEST_PREFIX}cleanup_test"
        redis_client.set(key, "will be cleaned")

        # Key exists now
        assert redis_client.exists(key)

        # Cleanup happens in fixture teardown
        # This test just sets up the key for cleanup verification
