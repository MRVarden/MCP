"""
Tests for FractalMemory - Level 2 Memory Storage
=================================================

Tests cover:
- Fractal initialization
- Store/retrieve operations
- Index management
- Type hierarchy
- Search functionality
"""

import pytest
import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory.fractal_memory import (
    FractalMemory,
    FractalIndex,
    create_fractal_memory
)
from luna_core.pure_memory.memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    MemoryQuery
)


class TestFractalMemoryInit:
    """Tests for FractalMemory initialization."""

    def test_init_creates_directories(self, temp_memory_path):
        """Test initialization creates necessary directories."""
        fractal = create_fractal_memory(str(temp_memory_path))

        assert (temp_memory_path / "roots").exists()
        assert (temp_memory_path / "branches").exists()
        assert (temp_memory_path / "leaves").exists()
        assert (temp_memory_path / "seeds").exists()

    def test_init_creates_indexes(self, temp_memory_path):
        """Test initialization creates index files."""
        fractal = create_fractal_memory(str(temp_memory_path))

        assert (temp_memory_path / "roots" / "index.json").exists()


class TestFractalStore:
    """Tests for store operations."""

    @pytest.mark.asyncio
    async def test_store_root_memory(self, temp_memory_path):
        """Test storing root memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(
            content="Root identity memory",
            memory_type=MemoryType.ROOT
        )

        memory_id = await fractal.store(memory)

        assert memory_id == memory.id
        assert (temp_memory_path / "roots" / f"{memory_id}.json").exists()

    @pytest.mark.asyncio
    async def test_store_branch_memory(self, temp_memory_path):
        """Test storing branch memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(
            content="Branch extension memory",
            memory_type=MemoryType.BRANCH
        )

        memory_id = await fractal.store(memory)

        assert memory_id == memory.id

    @pytest.mark.asyncio
    async def test_store_leaf_memory(self, temp_memory_path):
        """Test storing leaf memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(
            content="Daily interaction leaf",
            memory_type=MemoryType.LEAF
        )

        memory_id = await fractal.store(memory)

        assert memory_id == memory.id

    @pytest.mark.asyncio
    async def test_store_seed_memory(self, temp_memory_path):
        """Test storing seed memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(
            content="Potential idea seed",
            memory_type=MemoryType.SEED
        )

        memory_id = await fractal.store(memory)

        assert memory_id == memory.id

    @pytest.mark.asyncio
    async def test_store_sets_layer(self, temp_memory_path):
        """Test store sets layer to FRACTAL."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(content="Test")
        memory.layer = MemoryLayer.BUFFER

        await fractal.store(memory)

        assert memory.layer == MemoryLayer.FRACTAL


class TestFractalRetrieve:
    """Tests for retrieve operations."""

    @pytest.mark.asyncio
    async def test_retrieve_stored_memory(self, temp_memory_path):
        """Test retrieving stored memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(content="Test content for retrieval")
        await fractal.store(memory)

        retrieved = await fractal.retrieve(memory.id)

        assert retrieved is not None
        assert retrieved.id == memory.id
        assert retrieved.content == memory.content

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent(self, temp_memory_path):
        """Test retrieving nonexistent memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        retrieved = await fractal.retrieve("nonexistent_id")

        assert retrieved is None

    @pytest.mark.asyncio
    async def test_retrieve_preserves_metadata(self, temp_memory_path):
        """Test retrieval preserves all metadata."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(
            content="Content with metadata",
            keywords=["test", "phi"],
            tags=["important"]
        )
        await fractal.store(memory)

        retrieved = await fractal.retrieve(memory.id)

        assert retrieved.keywords == memory.keywords
        assert retrieved.tags == memory.tags


class TestFractalSearch:
    """Tests for search operations."""

    @pytest.mark.asyncio
    async def test_search_by_content(self, temp_memory_path):
        """Test searching by content."""
        fractal = create_fractal_memory(str(temp_memory_path))

        await fractal.store(MemoryExperience(content="phi golden ratio"))
        await fractal.store(MemoryExperience(content="other content"))

        query = MemoryQuery(query_text="phi")
        results = await fractal.search(query)

        assert len(results) >= 1
        assert any("phi" in r.content.lower() for r in results)

    @pytest.mark.asyncio
    async def test_search_by_type(self, temp_memory_path):
        """Test searching by memory type."""
        fractal = create_fractal_memory(str(temp_memory_path))

        await fractal.store(MemoryExperience(
            content="Root content phi",
            memory_type=MemoryType.ROOT
        ))
        await fractal.store(MemoryExperience(
            content="Leaf content phi",
            memory_type=MemoryType.LEAF
        ))

        query = MemoryQuery(
            query_text="phi",
            memory_types=[MemoryType.ROOT]
        )
        results = await fractal.search(query)

        assert all(r.memory_type == MemoryType.ROOT for r in results)

    @pytest.mark.asyncio
    async def test_search_respects_limit(self, temp_memory_path):
        """Test search respects limit."""
        fractal = create_fractal_memory(str(temp_memory_path))

        for i in range(20):
            await fractal.store(MemoryExperience(content=f"phi content {i}"))

        query = MemoryQuery(query_text="phi", limit=5)
        results = await fractal.search(query)

        assert len(results) <= 5

    @pytest.mark.asyncio
    async def test_search_by_tags(self, temp_memory_path):
        """Test searching by tags."""
        fractal = create_fractal_memory(str(temp_memory_path))

        await fractal.store(MemoryExperience(
            content="Tagged content",
            tags=["important", "phi"]
        ))

        query = MemoryQuery(tags=["important"])
        results = await fractal.search(query)

        assert len(results) >= 1


class TestFractalIndex:
    """Tests for FractalIndex - requires base_path."""

    def test_index_default_values(self, temp_memory_path):
        """Test index default values."""
        index = FractalIndex(temp_memory_path)

        # _indices is a dict with MemoryType keys
        assert MemoryType.ROOT in index._indices
        assert index.count() == 0

    def test_index_add_memory(self, temp_memory_path):
        """Test adding memory to index."""
        index = FractalIndex(temp_memory_path)

        memory = MemoryExperience(content="Test", memory_type=MemoryType.LEAF)
        index.add(memory)

        assert memory.id in index.get_all_ids(MemoryType.LEAF)

    def test_index_remove_memory(self, temp_memory_path):
        """Test removing memory from index."""
        index = FractalIndex(temp_memory_path)

        memory = MemoryExperience(content="Test", memory_type=MemoryType.LEAF)
        index.add(memory)
        index.remove(MemoryType.LEAF, memory.id)

        assert memory.id not in index.get_all_ids(MemoryType.LEAF)

    def test_index_to_dict(self, temp_memory_path):
        """Test index count reflects added memories."""
        index = FractalIndex(temp_memory_path)

        memory = MemoryExperience(content="Test", memory_type=MemoryType.LEAF)
        index.add(memory)

        assert index.count() == 1
        assert index.count(MemoryType.LEAF) == 1


class TestFractalStats:
    """Tests for statistics."""

    @pytest.mark.asyncio
    async def test_get_stats_structure(self, temp_memory_path):
        """Test stats structure."""
        fractal = create_fractal_memory(str(temp_memory_path))

        stats = fractal.get_stats()

        assert "total_memories" in stats
        assert "types" in stats

    @pytest.mark.asyncio
    async def test_stats_reflect_stored(self, temp_memory_path):
        """Test stats reflect stored memories."""
        fractal = create_fractal_memory(str(temp_memory_path))

        await fractal.store(MemoryExperience(
            content="Root",
            memory_type=MemoryType.ROOT
        ))
        await fractal.store(MemoryExperience(
            content="Leaf",
            memory_type=MemoryType.LEAF
        ))

        stats = fractal.get_stats()

        assert stats["types"]["root"]["count"] >= 1
        assert stats["types"]["leaf"]["count"] >= 1


class TestFractalDelete:
    """Tests for delete operations."""

    @pytest.mark.asyncio
    async def test_delete_existing(self, temp_memory_path):
        """Test deleting existing memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        memory = MemoryExperience(content="To be deleted")
        await fractal.store(memory)

        result = await fractal.delete(memory.id)

        assert result == True
        assert await fractal.retrieve(memory.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, temp_memory_path):
        """Test deleting nonexistent memory."""
        fractal = create_fractal_memory(str(temp_memory_path))

        result = await fractal.delete("nonexistent")

        assert result == False


class TestFractalHierarchy:
    """Tests for hierarchical organization."""

    @pytest.mark.asyncio
    async def test_parent_child_relationship(self, temp_memory_path):
        """Test parent-child relationships."""
        fractal = create_fractal_memory(str(temp_memory_path))

        root = MemoryExperience(content="Root", memory_type=MemoryType.ROOT)
        branch = MemoryExperience(
            content="Branch",
            memory_type=MemoryType.BRANCH,
            parent_id=root.id
        )

        await fractal.store(root)
        await fractal.store(branch)

        # Update root with child
        root.children_ids.append(branch.id)
        await fractal.store(root)

        retrieved_root = await fractal.retrieve(root.id)

        assert branch.id in retrieved_root.children_ids

    @pytest.mark.asyncio
    async def test_get_children(self, temp_memory_path):
        """Test getting children via retrieve and manual lookup."""
        fractal = create_fractal_memory(str(temp_memory_path))

        root = MemoryExperience(content="Root", memory_type=MemoryType.ROOT)
        child1 = MemoryExperience(
            content="Child 1",
            memory_type=MemoryType.BRANCH,
            parent_id=root.id
        )
        child2 = MemoryExperience(
            content="Child 2",
            memory_type=MemoryType.BRANCH,
            parent_id=root.id
        )

        root.children_ids = [child1.id, child2.id]

        await fractal.store(root)
        await fractal.store(child1)
        await fractal.store(child2)

        # Get children via retrieve (no get_children method exists)
        retrieved_root = await fractal.retrieve(root.id)
        children_ids = retrieved_root.children_ids

        assert len(children_ids) == 2
        assert child1.id in children_ids
        assert child2.id in children_ids
