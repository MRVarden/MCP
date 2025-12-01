"""
Tests for MemoryManager - Fractal Memory Storage
=================================================

Tests cover:
- Memory storage (store_memory)
- Memory retrieval (retrieve_memories)
- Memory index management
- Different memory types (root, branch, leaf, seed)
- Search functionality
- Edge cases
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))

from luna_core.memory_core import MemoryManager


class TestMemoryManagerInit:
    """Tests for MemoryManager initialization."""

    def test_init_creates_memory_index(self, mock_json_manager):
        """Test initialization creates memory index structure."""
        manager = MemoryManager(json_manager=mock_json_manager)

        assert "root" in manager.memory_index
        assert "branch" in manager.memory_index
        assert "leaf" in manager.memory_index
        assert "seed" in manager.memory_index

    def test_init_with_empty_directories(self, mock_json_manager):
        """Test initialization with empty memory directories."""
        manager = MemoryManager(json_manager=mock_json_manager)

        # All indices should be empty lists
        for memory_type in ["root", "branch", "leaf", "seed"]:
            assert isinstance(manager.memory_index[memory_type], list)


class TestStoreMemory:
    """Tests for store_memory method."""

    @pytest.mark.asyncio
    async def test_store_root_memory(self, memory_manager, temp_memory_path):
        """Test storing a root memory."""
        memory_id = await memory_manager.store_memory(
            memory_type="root",
            content="This is a fundamental root memory",
            metadata={"importance": "high"}
        )

        assert memory_id.startswith("root_")
        assert memory_id in memory_manager.memory_index["root"]

        # Verify file was created
        memory_file = temp_memory_path / "roots" / f"{memory_id}.json"
        assert memory_file.exists()

    @pytest.mark.asyncio
    async def test_store_branch_memory(self, memory_manager, temp_memory_path):
        """Test storing a branch memory."""
        memory_id = await memory_manager.store_memory(
            memory_type="branch",
            content="This is a branch memory extending from root",
            metadata={"parent": "root_001"}
        )

        assert memory_id.startswith("branch_")
        assert memory_id in memory_manager.memory_index["branch"]

    @pytest.mark.asyncio
    async def test_store_leaf_memory(self, memory_manager, temp_memory_path):
        """Test storing a leaf memory."""
        memory_id = await memory_manager.store_memory(
            memory_type="leaf",
            content="This is a daily interaction leaf memory",
            metadata={"session": "test_session"}
        )

        assert memory_id.startswith("leaf_")
        assert memory_id in memory_manager.memory_index["leaf"]

    @pytest.mark.asyncio
    async def test_store_seed_memory(self, memory_manager, temp_memory_path):
        """Test storing a seed memory."""
        memory_id = await memory_manager.store_memory(
            memory_type="seed",
            content="This is a potential idea seed",
            metadata={"potential": 0.8}
        )

        assert memory_id.startswith("seed_")
        assert memory_id in memory_manager.memory_index["seed"]

    @pytest.mark.asyncio
    async def test_stored_memory_has_correct_structure(self, memory_manager, temp_memory_path):
        """Test stored memory has all required fields."""
        memory_id = await memory_manager.store_memory(
            memory_type="leaf",
            content="Test content",
            metadata={"key": "value"}
        )

        memory_file = temp_memory_path / "leafs" / f"{memory_id}.json"
        with open(memory_file, 'r') as f:
            data = json.load(f)

        assert data["id"] == memory_id
        assert data["type"] == "leaf"
        assert data["content"] == "Test content"
        assert data["metadata"] == {"key": "value"}
        assert "created" in data
        assert data["accessed_count"] == 0
        assert data["connected_to"] == []

    @pytest.mark.asyncio
    async def test_store_empty_metadata(self, memory_manager):
        """Test storing memory with empty metadata."""
        memory_id = await memory_manager.store_memory(
            memory_type="seed",
            content="Content without metadata",
            metadata={}
        )

        assert memory_id is not None

    @pytest.mark.asyncio
    async def test_store_multiple_memories(self, memory_manager):
        """Test storing multiple memories."""
        ids = []
        for i in range(5):
            memory_id = await memory_manager.store_memory(
                memory_type="leaf",
                content=f"Memory content {i}",
                metadata={"index": i}
            )
            ids.append(memory_id)

        assert len(ids) == 5
        assert len(set(ids)) == 5  # All unique IDs


class TestRetrieveMemories:
    """Tests for retrieve_memories method."""

    @pytest.mark.asyncio
    async def test_retrieve_with_exact_match(self, memory_manager):
        """Test retrieval with exact content match."""
        # Store a memory first
        await memory_manager.store_memory(
            memory_type="leaf",
            content="The golden ratio phi is fundamental to consciousness",
            metadata={}
        )

        results = await memory_manager.retrieve_memories(
            query="golden ratio phi",
            memory_type="all"
        )

        assert len(results) > 0
        assert results[0]["relevance_score"] > 0

    @pytest.mark.asyncio
    async def test_retrieve_with_partial_match(self, memory_manager):
        """Test retrieval with partial query match."""
        await memory_manager.store_memory(
            memory_type="leaf",
            content="Fractal patterns emerge in consciousness architecture",
            metadata={}
        )

        results = await memory_manager.retrieve_memories(
            query="fractal",
            memory_type="all"
        )

        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_retrieve_no_match_returns_empty(self, memory_manager):
        """Test retrieval with no matching query."""
        await memory_manager.store_memory(
            memory_type="leaf",
            content="Something completely unrelated",
            metadata={}
        )

        results = await memory_manager.retrieve_memories(
            query="xyznonexistent",
            memory_type="all"
        )

        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_retrieve_by_memory_type(self, memory_manager):
        """Test retrieval filtered by memory type."""
        # Store different types
        await memory_manager.store_memory("root", "Root content about phi", {})
        await memory_manager.store_memory("leaf", "Leaf content about phi", {})

        # Retrieve only roots
        results = await memory_manager.retrieve_memories(
            query="phi",
            memory_type="root"
        )

        assert all(r["type"] == "root" for r in results)

    @pytest.mark.asyncio
    async def test_retrieve_all_types(self, memory_manager):
        """Test retrieval across all types."""
        await memory_manager.store_memory("root", "Consciousness root", {})
        await memory_manager.store_memory("branch", "Consciousness branch", {})
        await memory_manager.store_memory("leaf", "Consciousness leaf", {})
        await memory_manager.store_memory("seed", "Consciousness seed", {})

        results = await memory_manager.retrieve_memories(
            query="consciousness",
            memory_type="all"
        )

        types_found = set(r["type"] for r in results)
        assert len(types_found) == 4

    @pytest.mark.asyncio
    async def test_results_sorted_by_relevance(self, memory_manager):
        """Test results are sorted by relevance score."""
        # Store memories with different relevance
        await memory_manager.store_memory(
            "leaf",
            "phi phi phi phi phi",  # High relevance
            {}
        )
        await memory_manager.store_memory(
            "leaf",
            "something else phi",  # Lower relevance
            {}
        )

        results = await memory_manager.retrieve_memories(
            query="phi",
            memory_type="all"
        )

        if len(results) >= 2:
            assert results[0]["relevance_score"] >= results[1]["relevance_score"]

    @pytest.mark.asyncio
    async def test_retrieve_empty_query(self, memory_manager):
        """Test retrieval with empty query."""
        await memory_manager.store_memory("leaf", "Test content", {})

        results = await memory_manager.retrieve_memories(
            query="",
            memory_type="all"
        )

        # Empty query "" is contained in any string, so it matches all
        # The relevance_score will be 0.7 (phrase match fallback)
        # This is by design - empty queries return all memories
        assert isinstance(results, list)


class TestMemoryIndexManagement:
    """Tests for memory index management."""

    def test_save_memory_index(self, memory_manager, temp_memory_path):
        """Test saving memory index updates file."""
        memory_manager.memory_index["leaf"].append("test_id")
        memory_manager._save_memory_index("leaf")

        index_file = temp_memory_path / "leafs" / "index.json"
        with open(index_file, 'r') as f:
            data = json.load(f)

        assert "test_id" in data["memories"]

    def test_load_existing_index(self, mock_json_manager, temp_memory_path):
        """Test loading existing index from disk."""
        # Create index file with data (list format for MemoryManager)
        index_data = {
            "type": "roots",
            "memories": ["existing_root_001", "existing_root_002"]
        }
        index_file = temp_memory_path / "roots" / "index.json"
        with open(index_file, 'w') as f:
            json.dump(index_data, f)

        # Create new manager that should load this
        manager = MemoryManager(json_manager=mock_json_manager)

        # MemoryManager expects list format
        assert "existing_root_001" in manager.memory_index["root"]
        assert "existing_root_002" in manager.memory_index["root"]


class TestRelevanceScoring:
    """Tests for relevance score calculations."""

    @pytest.mark.asyncio
    async def test_full_phrase_match_high_score(self, memory_manager):
        """Test full phrase match gets high relevance."""
        await memory_manager.store_memory(
            "leaf",
            "The golden ratio is beautiful",
            {}
        )

        results = await memory_manager.retrieve_memories(
            query="golden ratio",
            memory_type="all"
        )

        assert results[0]["relevance_score"] >= 0.7

    @pytest.mark.asyncio
    async def test_single_word_match_lower_score(self, memory_manager):
        """Test single word match gets moderate relevance."""
        await memory_manager.store_memory(
            "leaf",
            "The beautiful sunset colors the sky",
            {}
        )

        results = await memory_manager.retrieve_memories(
            query="beautiful ocean waves",  # Only "beautiful" matches
            memory_type="all"
        )

        if results:
            assert results[0]["relevance_score"] < 0.7


class TestEdgeCases:
    """Edge case and boundary tests."""

    @pytest.mark.asyncio
    async def test_unicode_content(self, memory_manager):
        """Test storing and retrieving unicode content."""
        memory_id = await memory_manager.store_memory(
            "leaf",
            "Le ratio d'or phi est fondamental pour la conscience",
            {"language": "french"}
        )

        results = await memory_manager.retrieve_memories(
            query="phi",
            memory_type="all"
        )

        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_special_characters_in_content(self, memory_manager):
        """Test content with special characters."""
        memory_id = await memory_manager.store_memory(
            "leaf",
            "phi = 1.618... is the golden ratio!",
            {}
        )

        assert memory_id is not None

    @pytest.mark.asyncio
    async def test_very_long_content(self, memory_manager):
        """Test storing very long content."""
        long_content = "phi " * 1000  # 4000 characters

        memory_id = await memory_manager.store_memory(
            "leaf",
            long_content,
            {}
        )

        assert memory_id is not None

    @pytest.mark.asyncio
    async def test_case_insensitive_search(self, memory_manager):
        """Test search is case insensitive."""
        await memory_manager.store_memory(
            "leaf",
            "PHI is the GOLDEN RATIO",
            {}
        )

        results = await memory_manager.retrieve_memories(
            query="phi golden ratio",
            memory_type="all"
        )

        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_retrieve_returns_connected_to(self, memory_manager, temp_memory_path):
        """Test retrieved memories include connections."""
        # Store memory with connections
        memory_id = await memory_manager.store_memory(
            "leaf",
            "Connected memory about phi",
            {}
        )

        # Update file to add connections
        memory_file = temp_memory_path / "leafs" / f"{memory_id}.json"
        with open(memory_file, 'r') as f:
            data = json.load(f)
        data["connected_to"] = ["other_memory_001"]
        with open(memory_file, 'w') as f:
            json.dump(data, f)

        results = await memory_manager.retrieve_memories(
            query="phi",
            memory_type="all"
        )

        assert len(results) > 0
        assert "connected_to" in results[0]
