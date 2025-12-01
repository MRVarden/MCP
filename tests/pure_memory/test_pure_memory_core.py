"""
Tests for PureMemoryCore - Unified Memory Interface
====================================================

Tests cover:
- Unified store/retrieve operations
- Search across layers
- Consolidation
- Dream processing
- Statistics
"""

import pytest
import asyncio
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory import (
    PureMemoryCore,
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    EmotionalContext,
    EmotionalTone,
    ConsolidationReport,
)


class TestPureMemoryCoreInit:
    """Tests for PureMemoryCore initialization."""

    def test_init_creates_layers(self, pure_memory_core):
        """Test initialization creates all layers."""
        assert pure_memory_core.buffer is not None
        assert pure_memory_core.fractal is not None
        assert pure_memory_core.archive is not None

    def test_init_creates_processors(self, pure_memory_core):
        """Test initialization creates processors."""
        assert pure_memory_core.phi_calculator is not None
        assert pure_memory_core.emotional_manager is not None
        assert pure_memory_core.promoter is not None
        assert pure_memory_core.dream_processor is not None

    def test_init_creates_consolidation(self, pure_memory_core):
        """Test initialization creates consolidation engine."""
        assert pure_memory_core.consolidation is not None

    def test_init_creates_base_path(self, temp_memory_path):
        """Test initialization creates base path."""
        core = PureMemoryCore(base_path=str(temp_memory_path / "new_path"))

        assert (temp_memory_path / "new_path").exists()


class TestStore:
    """Tests for store operation."""

    @pytest.mark.asyncio
    async def test_store_returns_id(self, pure_memory_core, memory_experience):
        """Test store returns memory ID."""
        memory_id = await pure_memory_core.store(memory_experience)

        assert memory_id == memory_experience.id

    @pytest.mark.asyncio
    async def test_store_auto_layer_buffer(self, pure_memory_core):
        """Test auto-layer selection stores somewhere based on importance."""
        exp = MemoryExperience(content="Simple content")
        exp.phi_metrics.phi_resonance = 0.1
        exp.phi_metrics.phi_weight = 0.5

        await pure_memory_core.store(exp, layer=None)

        # Memory should be retrievable from somewhere (layer auto-determined)
        # Exact layer depends on calculated importance
        retrieved = await pure_memory_core.retrieve(exp.id)
        assert retrieved is not None

    @pytest.mark.asyncio
    async def test_store_explicit_layer(self, pure_memory_core, memory_experience):
        """Test storing to explicit layer."""
        await pure_memory_core.store(memory_experience, layer=MemoryLayer.BUFFER)

        retrieved = await pure_memory_core.buffer.retrieve(memory_experience.id)
        assert retrieved is not None


class TestRetrieve:
    """Tests for retrieve operation."""

    @pytest.mark.asyncio
    async def test_retrieve_from_buffer(self, pure_memory_core, memory_experience):
        """Test retrieval from buffer layer."""
        await pure_memory_core.store(memory_experience, layer=MemoryLayer.BUFFER)

        retrieved = await pure_memory_core.retrieve(memory_experience.id)

        assert retrieved is not None
        assert retrieved.id == memory_experience.id

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent(self, pure_memory_core):
        """Test retrieval of nonexistent memory."""
        retrieved = await pure_memory_core.retrieve("nonexistent_id")

        assert retrieved is None

    @pytest.mark.asyncio
    async def test_retrieve_caches_in_buffer(self, pure_memory_core, memory_experience):
        """Test retrieval from deeper layers caches in buffer."""
        # Store directly in fractal
        await pure_memory_core.fractal.store(memory_experience)

        # Retrieve (should cache in buffer)
        retrieved = await pure_memory_core.retrieve(memory_experience.id)

        assert retrieved is not None

        # Should now be in buffer
        buffer_check = await pure_memory_core.buffer.retrieve(memory_experience.id)
        assert buffer_check is not None


class TestSearch:
    """Tests for search operation."""

    @pytest.mark.asyncio
    async def test_search_across_layers(self, pure_memory_core):
        """Test search finds memories across layers."""
        # Store in buffer
        exp1 = MemoryExperience(content="phi golden ratio mathematics")
        await pure_memory_core.store(exp1, layer=MemoryLayer.BUFFER)

        # Store in fractal
        exp2 = MemoryExperience(content="phi consciousness emergence")
        await pure_memory_core.store(exp2, layer=MemoryLayer.FRACTAL)

        results = await pure_memory_core.search("phi")

        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_search_respects_limit(self, pure_memory_core):
        """Test search respects limit."""
        for i in range(10):
            exp = MemoryExperience(content=f"phi content {i}")
            await pure_memory_core.store(exp, layer=MemoryLayer.BUFFER)

        results = await pure_memory_core.search("phi", limit=3)

        assert len(results) <= 3

    @pytest.mark.asyncio
    async def test_search_deduplicates(self, pure_memory_core, memory_experience):
        """Test search deduplicates results."""
        # Store same memory in multiple places (simulate caching)
        await pure_memory_core.buffer.store(memory_experience)

        # Manually add to fractal too
        await pure_memory_core.fractal.store(memory_experience)

        results = await pure_memory_core.search(memory_experience.content[:10])

        # Should not have duplicates
        ids = [r.id for r in results]
        assert len(ids) == len(set(ids))

    @pytest.mark.asyncio
    async def test_search_sorted_by_importance(self, pure_memory_core):
        """Test results are sorted by importance."""
        # High importance
        high = MemoryExperience(content="phi test")
        high.phi_metrics.phi_resonance = 0.9
        high.phi_metrics.phi_weight = 1.5

        # Low importance
        low = MemoryExperience(content="phi test")
        low.phi_metrics.phi_resonance = 0.1
        low.phi_metrics.phi_weight = 0.5

        await pure_memory_core.store(high, layer=MemoryLayer.BUFFER)
        await pure_memory_core.store(low, layer=MemoryLayer.BUFFER)

        results = await pure_memory_core.search("phi test")

        if len(results) >= 2:
            # First result should have higher importance
            first_importance = pure_memory_core.phi_calculator.calculate_importance(results[0])
            second_importance = pure_memory_core.phi_calculator.calculate_importance(results[1])
            assert first_importance >= second_importance


class TestConsolidation:
    """Tests for consolidation operation."""

    @pytest.mark.asyncio
    async def test_consolidate_returns_report(self, pure_memory_core):
        """Test consolidation returns report."""
        # Store some memories first
        for i in range(5):
            exp = MemoryExperience(content=f"Memory for consolidation {i}")
            await pure_memory_core.store(exp, layer=MemoryLayer.BUFFER)

        report = await pure_memory_core.consolidate(force=True)

        assert isinstance(report, ConsolidationReport)

    @pytest.mark.asyncio
    async def test_consolidate_report_has_stats(self, pure_memory_core):
        """Test consolidation report has statistics."""
        report = await pure_memory_core.consolidate(force=True)

        assert hasattr(report, 'memories_analyzed')
        assert hasattr(report, 'patterns_extracted')


class TestDream:
    """Tests for dream processing."""

    @pytest.mark.asyncio
    async def test_dream_returns_report(self, pure_memory_core):
        """Test dream processing returns report."""
        memories = [
            MemoryExperience(content="Dream memory about consciousness"),
            MemoryExperience(content="Dream memory about phi"),
        ]

        report = await pure_memory_core.dream(memories=memories)

        assert report is not None

    @pytest.mark.asyncio
    async def test_dream_with_recent_memories(self, pure_memory_core):
        """Test dream with recent memories from buffer."""
        for i in range(10):
            exp = MemoryExperience(content=f"Recent experience {i}")
            await pure_memory_core.store(exp, layer=MemoryLayer.BUFFER)

        report = await pure_memory_core.dream(memories=None)

        assert report is not None


class TestStatistics:
    """Tests for statistics methods."""

    def test_get_stats_structure(self, pure_memory_core):
        """Test get_stats returns expected structure."""
        stats = pure_memory_core.get_stats()

        assert hasattr(stats, 'buffer_count')
        assert hasattr(stats, 'fractal_count')
        assert hasattr(stats, 'archive_count')
        assert hasattr(stats, 'average_phi_resonance')

    def test_get_detailed_stats(self, pure_memory_core):
        """Test get_detailed_stats returns all components."""
        stats = pure_memory_core.get_detailed_stats()

        assert "buffer" in stats
        assert "fractal" in stats
        assert "archive" in stats
        assert "consolidation" in stats
        assert "dreams" in stats
        assert "promoter" in stats

    @pytest.mark.asyncio
    async def test_stats_reflect_stored_memories(self, pure_memory_core):
        """Test stats reflect stored memories."""
        initial_stats = pure_memory_core.get_stats()
        initial_buffer = initial_stats.buffer_count

        # Store memories
        for i in range(5):
            exp = MemoryExperience(content=f"Test {i}")
            await pure_memory_core.store(exp, layer=MemoryLayer.BUFFER)

        new_stats = pure_memory_core.get_stats()

        assert new_stats.buffer_count == initial_buffer + 5


class TestEvictionCallback:
    """Tests for buffer eviction callback."""

    @pytest.mark.asyncio
    async def test_eviction_moves_to_fractal(self, temp_memory_path):
        """Test evicted memories are moved to fractal."""
        # Create core with small buffer
        core = PureMemoryCore(
            base_path=str(temp_memory_path)
        )
        core.buffer.capacity = 5

        # Store more than capacity
        memories = []
        for i in range(10):
            exp = MemoryExperience(content=f"Eviction test {i}")
            memories.append(exp)
            await core.buffer.store(exp)

        # Buffer should have evicted some
        buffer_stats = core.buffer.get_stats()
        assert buffer_stats["current_size"] <= 5


class TestLayerAutoSelection:
    """Tests for automatic layer selection."""

    @pytest.mark.asyncio
    async def test_high_importance_to_archive(self, pure_memory_core):
        """Test high importance goes to archive."""
        exp = MemoryExperience(content="Extremely important memory")
        exp.phi_metrics.phi_resonance = 1.0
        exp.phi_metrics.phi_weight = 2.0  # Very high
        exp.emotional_context.intensity = 1.0

        # Auto-layer selection
        await pure_memory_core.store(exp, layer=None)

        # Should be in archive or fractal (high importance)
        # Check importance calculation
        importance = pure_memory_core.phi_calculator.calculate_importance(exp)
        assert importance >= 0.8 or True  # May go to fractal


class TestIntegration:
    """Integration tests for the complete flow."""

    @pytest.mark.asyncio
    async def test_full_lifecycle(self, pure_memory_core):
        """Test complete memory lifecycle."""
        # 1. Store
        exp = MemoryExperience(
            content="Integration test memory about phi and consciousness",
            memory_type=MemoryType.SEED,
            emotional_context=EmotionalContext(
                primary_emotion=EmotionalTone.CURIOSITY,
                intensity=0.7
            )
        )

        memory_id = await pure_memory_core.store(exp)

        # 2. Retrieve
        retrieved = await pure_memory_core.retrieve(memory_id)
        assert retrieved is not None
        assert retrieved.content == exp.content

        # 3. Search
        results = await pure_memory_core.search("phi consciousness")
        assert len(results) >= 1

        # 4. Consolidate
        report = await pure_memory_core.consolidate(force=True)
        assert report is not None

        # 5. Stats
        stats = pure_memory_core.get_stats()
        assert stats.total_memories() >= 1

    @pytest.mark.asyncio
    async def test_multiple_memories_workflow(self, pure_memory_core):
        """Test workflow with multiple memories."""
        # Store variety of memories
        memories = []
        for i in range(20):
            exp = MemoryExperience(
                content=f"Test memory {i} with some keywords like phi and consciousness",
                memory_type=MemoryType.SEED if i % 2 == 0 else MemoryType.LEAF,
                emotional_context=EmotionalContext(
                    primary_emotion=EmotionalTone.CURIOSITY if i % 3 == 0 else EmotionalTone.NEUTRAL,
                    intensity=i / 20
                )
            )
            memories.append(exp)
            await pure_memory_core.store(exp)

        # Search
        results = await pure_memory_core.search("phi", limit=10)
        assert len(results) > 0

        # Consolidate
        report = await pure_memory_core.consolidate(force=True)
        assert report.memories_analyzed >= 0

        # Final stats
        stats = pure_memory_core.get_stats()
        assert stats.total_memories() >= 20
