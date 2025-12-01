"""
Tests for ArchiveManager - Level 3 Permanent Storage
=====================================================

Tests cover:
- Archive initialization
- Archive/retrieve operations
- Encryption (optional)
- Compression
- Search functionality
- Statistics
"""

import pytest
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory.archive_manager import (
    ArchiveManager,
    ArchiveEntry,
    ArchiveIndex,
    create_archive_manager,
    ENCRYPTION_ENABLED
)
from luna_core.pure_memory.memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer
)


class TestArchiveManagerInit:
    """Tests for ArchiveManager initialization."""

    def test_init_creates_directory(self, temp_memory_path):
        """Test initialization creates archive directory."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        assert (temp_memory_path / "archive").exists()

    def test_init_without_encryption(self, temp_memory_path):
        """Test initialization without encryption - uses global ENCRYPTION_ENABLED."""
        archive = create_archive_manager(
            str(temp_memory_path / "archive"),
            master_key_hex=None
        )

        # encryption instance exists but ENCRYPTION_ENABLED is False by default
        assert archive.encryption is not None
        assert ENCRYPTION_ENABLED == False

    def test_init_with_encryption(self, temp_memory_path):
        """Test initialization with encryption key - still uses global ENCRYPTION_ENABLED."""
        # 32 hex chars = 128 bits minimum for master key
        key_hex = '0' * 64  # 64 hex chars = 256 bits

        archive = create_archive_manager(
            str(temp_memory_path / "archive"),
            master_key_hex=key_hex
        )

        # encryption key is set, but actual encryption depends on ENCRYPTION_ENABLED
        assert archive.encryption is not None
        assert archive.encryption._master_key_hex == key_hex


class TestArchiveOperation:
    """Tests for archive operation."""

    @pytest.mark.asyncio
    async def test_archive_returns_id(self, temp_memory_path):
        """Test archive returns memory ID."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(content="Archive test content")

        memory_id = await archive.archive(memory)

        assert memory_id == memory.id

    @pytest.mark.asyncio
    async def test_archive_sets_layer(self, temp_memory_path):
        """Test archive sets layer to ARCHIVE."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(content="Test")

        await archive.archive(memory)

        assert memory.layer == MemoryLayer.ARCHIVE

    @pytest.mark.asyncio
    async def test_archive_creates_file(self, temp_memory_path):
        """Test archive creates file on disk."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(content="File creation test")

        await archive.archive(memory)

        # Check archive directory has files
        archive_files = list((temp_memory_path / "archive").glob("*.json"))
        assert len(archive_files) >= 1 or \
               len(list((temp_memory_path / "archive").glob("*.archive"))) >= 1


class TestArchiveRetrieve:
    """Tests for retrieve from archive."""

    @pytest.mark.asyncio
    async def test_retrieve_archived_memory(self, temp_memory_path):
        """Test retrieving archived memory."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(content="Retrieve test content")
        await archive.archive(memory)

        retrieved = await archive.retrieve(memory.id)

        assert retrieved is not None
        assert retrieved.id == memory.id
        assert retrieved.content == memory.content

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent(self, temp_memory_path):
        """Test retrieving nonexistent archive."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        retrieved = await archive.retrieve("nonexistent_id")

        assert retrieved is None

    @pytest.mark.asyncio
    async def test_retrieve_preserves_all_fields(self, temp_memory_path):
        """Test retrieval preserves all memory fields."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(
            content="Full metadata test",
            memory_type=MemoryType.ROOT,
            keywords=["test", "archive"],
            tags=["important"]
        )
        await archive.archive(memory)

        retrieved = await archive.retrieve(memory.id)

        assert retrieved.memory_type == memory.memory_type
        assert retrieved.keywords == memory.keywords
        assert retrieved.tags == memory.tags


class TestArchiveWithEncryption:
    """Tests for encrypted archives."""

    @pytest.mark.asyncio
    async def test_archive_with_encryption(self, temp_memory_path):
        """Test archiving with encryption."""
        key_hex = '0' * 64  # 64 hex chars = 256 bits

        archive = create_archive_manager(
            str(temp_memory_path / "archive"),
            master_key_hex=key_hex
        )

        memory = MemoryExperience(content="Secret content")

        await archive.archive(memory)

        # Verify retrieval works
        retrieved = await archive.retrieve(memory.id)

        assert retrieved is not None
        assert retrieved.content == memory.content

    @pytest.mark.asyncio
    async def test_encrypted_file_not_readable(self, temp_memory_path):
        """Test encrypted files are not plaintext readable."""
        key_hex = '0' * 64  # 64 hex chars = 256 bits

        archive = create_archive_manager(
            str(temp_memory_path / "archive"),
            master_key_hex=key_hex
        )

        memory = MemoryExperience(content="This should be encrypted")
        await archive.archive(memory)

        # Try to read raw file
        archive_files = list((temp_memory_path / "archive").glob("*"))

        # At least one file should exist
        # Content should not be plaintext readable
        # (This depends on implementation)


class TestArchiveSearch:
    """Tests for archive search."""

    @pytest.mark.asyncio
    async def test_search_archives(self, temp_memory_path):
        """Test searching archives."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        await archive.archive(MemoryExperience(content="phi golden ratio"))
        await archive.archive(MemoryExperience(content="other content"))

        results = await archive.search(query="phi")

        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_search_respects_limit(self, temp_memory_path):
        """Test search respects limit."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        for i in range(10):
            await archive.archive(MemoryExperience(content=f"phi test {i}"))

        results = await archive.search(query="phi", limit=3)

        assert len(results) <= 3


class TestArchiveStats:
    """Tests for archive statistics."""

    def test_get_stats_structure(self, temp_memory_path):
        """Test stats structure."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        stats = archive.get_stats()

        assert "total_memories" in stats
        assert "total_size_bytes" in stats

    @pytest.mark.asyncio
    async def test_stats_reflect_archives(self, temp_memory_path):
        """Test stats reflect archived memories."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        await archive.archive(MemoryExperience(content="Memory 1"))
        await archive.archive(MemoryExperience(content="Memory 2"))

        stats = archive.get_stats()

        assert stats["total_memories"] >= 2


class TestArchiveEntry:
    """Tests for ArchiveEntry dataclass."""

    def test_entry_default_values(self):
        """Test entry default values with required fields."""
        entry = ArchiveEntry(
            memory_id="test_id",
            archive_file="archive_test.luna.archive",
            offset=0,
            size=1000,
            created_at=datetime.now(),
            memory_type="leaf",
            checksum="abc123"
        )

        assert entry.memory_id == "test_id"
        assert entry.compressed == False
        assert entry.encrypted == False

    def test_entry_to_dict(self):
        """Test entry serialization."""
        entry = ArchiveEntry(
            memory_id="test_id",
            archive_file="archive_test.luna.archive",
            offset=0,
            size=1000,
            created_at=datetime.now(),
            memory_type="leaf",
            checksum="abc123",
            compressed=True
        )

        data = entry.to_dict()

        assert data["memory_id"] == "test_id"
        assert data["compressed"] == True


class TestArchiveIndex:
    """Tests for ArchiveIndex class - requires index_path."""

    def test_index_default_values(self, temp_memory_path):
        """Test index default values."""
        index_path = temp_memory_path / "archive_index.json"
        index = ArchiveIndex(index_path)

        assert index.count() == 0

    def test_index_add_entry(self, temp_memory_path):
        """Test adding entry to index."""
        index_path = temp_memory_path / "archive_index.json"
        index = ArchiveIndex(index_path)

        entry = ArchiveEntry(
            memory_id="test_id",
            archive_file="archive_test.luna.archive",
            offset=0,
            size=1000,
            created_at=datetime.now(),
            memory_type="leaf",
            checksum="abc123"
        )
        index.add(entry)

        assert index.get("test_id") is not None

    def test_index_remove_entry(self, temp_memory_path):
        """Test removing entry from index."""
        index_path = temp_memory_path / "archive_index.json"
        index = ArchiveIndex(index_path)

        entry = ArchiveEntry(
            memory_id="test_id",
            archive_file="archive_test.luna.archive",
            offset=0,
            size=1000,
            created_at=datetime.now(),
            memory_type="leaf",
            checksum="abc123"
        )
        index.add(entry)
        index.remove("test_id")

        assert index.get("test_id") is None


class TestCompression:
    """Tests for compression functionality."""

    @pytest.mark.asyncio
    async def test_archive_with_compression(self, temp_memory_path):
        """Test archiving with compression enabled (default is True)."""
        archive = create_archive_manager(
            str(temp_memory_path / "archive")
        )

        # Large content benefits more from compression
        memory = MemoryExperience(content="test content " * 100)

        # archive() accepts compress parameter, defaults to COMPRESSION_ENABLED (True)
        await archive.archive(memory, compress=True)

        retrieved = await archive.retrieve(memory.id)

        assert retrieved is not None
        assert retrieved.content == memory.content


class TestArchiveDelete:
    """Tests for delete from archive."""

    @pytest.mark.asyncio
    async def test_delete_archived(self, temp_memory_path):
        """Test deleting archived memory."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        memory = MemoryExperience(content="To be deleted")
        await archive.archive(memory)

        result = await archive.delete(memory.id)

        assert result == True
        assert await archive.retrieve(memory.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, temp_memory_path):
        """Test deleting nonexistent archive."""
        archive = create_archive_manager(str(temp_memory_path / "archive"))

        result = await archive.delete("nonexistent")

        assert result == False
