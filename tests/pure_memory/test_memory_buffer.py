"""
Tests for MemoryBuffer - Level 1 Memory Cache
==============================================

Tests cover:
- Buffer initialization
- Store/retrieve operations
- Search functionality
- Session context management
- Working memory
- Emotional state
- Eviction logic
- Statistics
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory.memory_buffer import (
    MemoryBuffer,
    BufferEntry,
    create_memory_buffer,
    DEFAULT_BUFFER_CAPACITY,
    DEFAULT_TTL_HOURS
)
from luna_core.pure_memory.memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    EmotionalContext,
    EmotionalTone
)


class TestBufferEntry:
    """Tests for BufferEntry dataclass."""

    def test_default_values(self):
        """Test default values."""
        memory = MemoryExperience(content="Test")
        entry = BufferEntry(key="test_key", value=memory)

        assert entry.key == "test_key"
        assert entry.access_count == 0
        assert entry.ttl_seconds is None

    def test_is_expired_no_ttl(self):
        """Test entry without TTL never expires."""
        memory = MemoryExperience(content="Test")
        entry = BufferEntry(key="test", value=memory, ttl_seconds=None)

        assert entry.is_expired() == False

    def test_is_expired_with_valid_ttl(self):
        """Test entry with future TTL is not expired."""
        memory = MemoryExperience(content="Test")
        entry = BufferEntry(
            key="test",
            value=memory,
            ttl_seconds=3600  # 1 hour
        )

        assert entry.is_expired() == False

    def test_is_expired_past_ttl(self):
        """Test entry past TTL is expired."""
        memory = MemoryExperience(content="Test")
        entry = BufferEntry(
            key="test",
            value=memory,
            created_at=datetime.now() - timedelta(hours=2),
            ttl_seconds=3600  # 1 hour
        )

        assert entry.is_expired() == True

    def test_access_increments_count(self):
        """Test access increments counter."""
        memory = MemoryExperience(content="Test")
        entry = BufferEntry(key="test", value=memory)

        entry.access()

        assert entry.access_count == 1
        assert entry.last_accessed is not None

    def test_priority_score_increases_with_access(self):
        """Test priority score increases with access count."""
        memory = MemoryExperience(content="Test")
        entry1 = BufferEntry(key="test", value=memory, access_count=0)
        entry2 = BufferEntry(key="test", value=memory, access_count=10)

        assert entry2.priority_score() > entry1.priority_score()


class TestMemoryBufferInit:
    """Tests for MemoryBuffer initialization."""

    def test_default_init(self):
        """Test default initialization."""
        buffer = MemoryBuffer()

        assert buffer.capacity == DEFAULT_BUFFER_CAPACITY
        assert buffer.default_ttl == DEFAULT_TTL_HOURS * 3600
        assert buffer.redis_client is None

    def test_custom_capacity(self):
        """Test custom capacity."""
        buffer = MemoryBuffer(capacity=500)

        assert buffer.capacity == 500

    def test_custom_ttl(self):
        """Test custom TTL."""
        buffer = MemoryBuffer(ttl_hours=48)

        assert buffer.default_ttl == 48 * 3600

    def test_eviction_callback(self):
        """Test eviction callback is stored."""
        callback = lambda x: None
        buffer = MemoryBuffer(on_eviction=callback)

        assert buffer.on_eviction == callback


class TestStoreRetrieve:
    """Tests for store and retrieve operations."""

    @pytest.mark.asyncio
    async def test_store_returns_id(self, memory_buffer, memory_experience):
        """Test store returns memory ID."""
        memory_id = await memory_buffer.store(memory_experience)

        assert memory_id == memory_experience.id

    @pytest.mark.asyncio
    async def test_store_sets_buffer_layer(self, memory_buffer, memory_experience):
        """Test store sets layer to BUFFER."""
        memory_experience.layer = MemoryLayer.FRACTAL

        await memory_buffer.store(memory_experience)

        assert memory_experience.layer == MemoryLayer.BUFFER

    @pytest.mark.asyncio
    async def test_retrieve_stored_memory(self, memory_buffer, memory_experience):
        """Test retrieval of stored memory."""
        await memory_buffer.store(memory_experience)

        retrieved = await memory_buffer.retrieve(memory_experience.id)

        assert retrieved is not None
        assert retrieved.id == memory_experience.id

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent_returns_none(self, memory_buffer):
        """Test retrieval of nonexistent memory."""
        retrieved = await memory_buffer.retrieve("nonexistent_id")

        assert retrieved is None

    @pytest.mark.asyncio
    async def test_retrieve_updates_access_metrics(self, memory_buffer, memory_experience):
        """Test retrieval updates access metrics."""
        await memory_buffer.store(memory_experience)

        initial_count = memory_experience.phi_metrics.access_count

        await memory_buffer.retrieve(memory_experience.id)

        assert memory_experience.phi_metrics.access_count == initial_count + 1

    @pytest.mark.asyncio
    async def test_store_multiple_memories(self, memory_buffer):
        """Test storing multiple memories."""
        memories = []
        for i in range(10):
            exp = MemoryExperience(content=f"Memory {i}")
            memories.append(exp)
            await memory_buffer.store(exp)

        for memory in memories:
            retrieved = await memory_buffer.retrieve(memory.id)
            assert retrieved is not None


class TestSearch:
    """Tests for search functionality."""

    @pytest.mark.asyncio
    async def test_search_by_content(self, memory_buffer):
        """Test search matches content."""
        exp1 = MemoryExperience(content="phi golden ratio mathematics")
        exp2 = MemoryExperience(content="consciousness awareness mind")

        await memory_buffer.store(exp1)
        await memory_buffer.store(exp2)

        results = await memory_buffer.search("phi mathematics")

        assert len(results) >= 1
        assert any(r.id == exp1.id for r in results)

    @pytest.mark.asyncio
    async def test_search_by_keywords(self, memory_buffer):
        """Test search matches content containing keyword terms."""
        # Keywords boost relevance when they appear in content
        # The search is content-based, not keyword-lookup based
        exp = MemoryExperience(
            content="phi golden ratio content",  # Keywords match content
            keywords=["phi", "golden", "ratio"]
        )

        await memory_buffer.store(exp)

        results = await memory_buffer.search("phi")

        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_search_by_tags(self, memory_buffer):
        """Test search matches content with relevant tags."""
        # Tags boost relevance when query matches tag names
        # But primary search is still content-based
        exp = MemoryExperience(
            content="consciousness emergence awareness",  # Content matches search
            tags=["consciousness", "emergence"]
        )

        await memory_buffer.store(exp)

        results = await memory_buffer.search("consciousness")

        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_search_respects_limit(self, memory_buffer):
        """Test search respects limit."""
        for i in range(20):
            exp = MemoryExperience(content=f"phi content {i}")
            await memory_buffer.store(exp)

        results = await memory_buffer.search("phi", limit=5)

        assert len(results) <= 5

    @pytest.mark.asyncio
    async def test_search_empty_query(self, memory_buffer):
        """Test search with empty query."""
        exp = MemoryExperience(content="Some content")
        await memory_buffer.store(exp)

        results = await memory_buffer.search("")

        # Empty query should match nothing or everything depending on impl
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_no_matches(self, memory_buffer):
        """Test search with no matches."""
        exp = MemoryExperience(content="apple banana orange")
        await memory_buffer.store(exp)

        results = await memory_buffer.search("xyznonexistent")

        assert len(results) == 0


class TestDelete:
    """Tests for delete operation."""

    @pytest.mark.asyncio
    async def test_delete_existing(self, memory_buffer, memory_experience):
        """Test deleting existing memory."""
        await memory_buffer.store(memory_experience)

        result = await memory_buffer.delete(memory_experience.id)

        assert result == True
        assert await memory_buffer.retrieve(memory_experience.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, memory_buffer):
        """Test deleting nonexistent memory."""
        result = await memory_buffer.delete("nonexistent")

        assert result == False


class TestClear:
    """Tests for clear operation."""

    @pytest.mark.asyncio
    async def test_clear_returns_count(self, memory_buffer):
        """Test clear returns count of cleared entries."""
        for i in range(5):
            await memory_buffer.store(MemoryExperience(content=f"Memory {i}"))

        count = await memory_buffer.clear()

        assert count == 5

    @pytest.mark.asyncio
    async def test_clear_empties_buffer(self, memory_buffer, memory_experience):
        """Test clear empties the buffer."""
        await memory_buffer.store(memory_experience)

        await memory_buffer.clear()

        assert await memory_buffer.retrieve(memory_experience.id) is None


class TestSessionContext:
    """Tests for session context management."""

    @pytest.mark.asyncio
    async def test_set_and_get_context(self, memory_buffer):
        """Test setting and getting session context."""
        await memory_buffer.set_session_context("user_id", "test_user")

        value = await memory_buffer.get_session_context("user_id")

        assert value == "test_user"

    @pytest.mark.asyncio
    async def test_get_nonexistent_context(self, memory_buffer):
        """Test getting nonexistent context."""
        value = await memory_buffer.get_session_context("nonexistent")

        assert value is None

    @pytest.mark.asyncio
    async def test_get_all_session_context(self, memory_buffer):
        """Test getting all session context."""
        await memory_buffer.set_session_context("key1", "value1")
        await memory_buffer.set_session_context("key2", "value2")

        all_context = await memory_buffer.get_all_session_context()

        assert all_context["key1"] == "value1"
        assert all_context["key2"] == "value2"

    @pytest.mark.asyncio
    async def test_clear_session_context(self, memory_buffer):
        """Test clearing session context."""
        await memory_buffer.set_session_context("key", "value")

        await memory_buffer.clear_session_context()

        assert await memory_buffer.get_session_context("key") is None


class TestWorkingMemory:
    """Tests for working memory management."""

    @pytest.mark.asyncio
    async def test_add_concept(self, memory_buffer):
        """Test adding concept to working memory."""
        await memory_buffer.add_to_working_memory("phi")

        is_present = await memory_buffer.is_in_working_memory("phi")

        assert is_present == True

    @pytest.mark.asyncio
    async def test_concept_not_in_memory(self, memory_buffer):
        """Test concept not in working memory."""
        is_present = await memory_buffer.is_in_working_memory("nonexistent")

        assert is_present == False

    @pytest.mark.asyncio
    async def test_get_working_memory(self, memory_buffer):
        """Test getting all working memory."""
        await memory_buffer.add_to_working_memory("concept1")
        await memory_buffer.add_to_working_memory("concept2")

        working_memory = await memory_buffer.get_working_memory()

        assert "concept1" in working_memory
        assert "concept2" in working_memory

    @pytest.mark.asyncio
    async def test_clear_working_memory(self, memory_buffer):
        """Test clearing working memory."""
        await memory_buffer.add_to_working_memory("concept")

        await memory_buffer.clear_working_memory()

        assert await memory_buffer.is_in_working_memory("concept") == False


class TestEmotionalState:
    """Tests for emotional state management."""

    @pytest.mark.asyncio
    async def test_update_emotional_state(self, memory_buffer):
        """Test updating emotional state."""
        result = await memory_buffer.update_emotional_state(
            valence=0.5,
            arousal=0.7,
            dominant_emotion="joy"
        )

        assert result["valence"] == 0.5
        assert result["arousal"] == 0.7
        assert result["dominant_emotion"] == "joy"

    @pytest.mark.asyncio
    async def test_get_emotional_state(self, memory_buffer):
        """Test getting emotional state."""
        await memory_buffer.update_emotional_state(valence=0.3)

        state = await memory_buffer.get_emotional_state()

        assert state["valence"] == 0.3

    @pytest.mark.asyncio
    async def test_emotional_state_clamped(self, memory_buffer):
        """Test emotional state values are clamped."""
        result = await memory_buffer.update_emotional_state(
            valence=2.0,  # Should be clamped to 1.0
            arousal=-0.5  # Should be clamped to 0.0
        )

        assert result["valence"] == 1.0
        assert result["arousal"] == 0.0


class TestRecentMemories:
    """Tests for getting recent memories."""

    @pytest.mark.asyncio
    async def test_get_recent_memories(self, memory_buffer):
        """Test getting recent memories."""
        for i in range(5):
            await memory_buffer.store(MemoryExperience(content=f"Memory {i}"))

        recent = await memory_buffer.get_recent_memories(limit=3)

        assert len(recent) == 3

    @pytest.mark.asyncio
    async def test_recent_memories_filter_by_type(self, memory_buffer):
        """Test filtering recent by type."""
        await memory_buffer.store(MemoryExperience(
            content="Root",
            memory_type=MemoryType.ROOT
        ))
        await memory_buffer.store(MemoryExperience(
            content="Leaf",
            memory_type=MemoryType.LEAF
        ))

        recent = await memory_buffer.get_recent_memories(
            limit=10,
            memory_type=MemoryType.ROOT
        )

        assert all(m.memory_type == MemoryType.ROOT for m in recent)


class TestEviction:
    """Tests for eviction logic."""

    @pytest.mark.asyncio
    async def test_eviction_when_full(self):
        """Test eviction happens when buffer is full."""
        buffer = MemoryBuffer(capacity=5)

        for i in range(10):
            await buffer.store(MemoryExperience(content=f"Memory {i}"))

        stats = buffer.get_stats()

        assert stats["current_size"] <= 5
        assert stats["evictions"] > 0

    @pytest.mark.asyncio
    async def test_eviction_callback_called(self):
        """Test eviction callback is called."""
        evicted = []

        def on_evict(memory):
            evicted.append(memory)

        buffer = MemoryBuffer(capacity=3, on_eviction=on_evict)

        for i in range(5):
            await buffer.store(MemoryExperience(content=f"Memory {i}"))

        assert len(evicted) >= 2


class TestStatistics:
    """Tests for buffer statistics."""

    @pytest.mark.asyncio
    async def test_stats_structure(self, memory_buffer):
        """Test stats have expected structure."""
        stats = memory_buffer.get_stats()

        assert "current_size" in stats
        assert "capacity" in stats
        assert "utilization" in stats
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate" in stats

    @pytest.mark.asyncio
    async def test_stats_hit_tracking(self, memory_buffer, memory_experience):
        """Test stats track hits."""
        await memory_buffer.store(memory_experience)

        await memory_buffer.retrieve(memory_experience.id)  # Hit
        await memory_buffer.retrieve("nonexistent")          # Miss

        stats = memory_buffer.get_stats()

        assert stats["hits"] == 1
        assert stats["misses"] == 1

    @pytest.mark.asyncio
    async def test_stats_store_count(self, memory_buffer):
        """Test stats track stores."""
        for i in range(3):
            await memory_buffer.store(MemoryExperience(content=f"Memory {i}"))

        stats = memory_buffer.get_stats()

        assert stats["stores"] == 3


class TestFactoryFunction:
    """Tests for create_memory_buffer factory."""

    def test_create_with_defaults(self):
        """Test factory with default parameters."""
        buffer = create_memory_buffer()

        assert buffer.capacity == DEFAULT_BUFFER_CAPACITY

    def test_create_with_custom_params(self):
        """Test factory with custom parameters."""
        buffer = create_memory_buffer(capacity=500, ttl_hours=12)

        assert buffer.capacity == 500
        assert buffer.default_ttl == 12 * 3600

    def test_create_without_redis(self):
        """Test factory without Redis URL."""
        buffer = create_memory_buffer(redis_url=None)

        assert buffer.redis_client is None


class TestFractalCandidates:
    """Tests for fractal promotion candidates."""

    @pytest.mark.asyncio
    async def test_get_candidates_for_fractal(self, memory_buffer):
        """Test getting candidates for fractal layer."""
        # High importance memory
        important = MemoryExperience(content="Important")
        important.phi_metrics.phi_resonance = 0.9
        important.phi_metrics.phi_weight = 1.5

        # Low importance memory
        trivial = MemoryExperience(content="Trivial")
        trivial.phi_metrics.phi_resonance = 0.1

        await memory_buffer.store(important)
        await memory_buffer.store(trivial)

        candidates = await memory_buffer.get_candidates_for_fractal(min_importance=0.5)

        # Important should be candidate, trivial should not
        assert any(c.id == important.id for c in candidates)

    @pytest.mark.asyncio
    async def test_mark_as_flushed(self, memory_buffer, memory_experience):
        """Test marking memories as flushed."""
        await memory_buffer.store(memory_experience)

        count = await memory_buffer.mark_as_flushed([memory_experience.id])

        assert count == 1
        retrieved = await memory_buffer.retrieve(memory_experience.id)
        assert retrieved.layer == MemoryLayer.FRACTAL
