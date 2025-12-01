"""
Archive Manager - Pure Memory Architecture v2.0
Level 3: Deep Archive with encryption support.

This module manages the permanent memory archive layer with optional
encryption for sensitive memories and long-term storage.
"""

import asyncio
import json
import logging
import hashlib
import base64
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
import threading
import os

from .memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    PureMemoryStats,
    PHI,
    PHI_INVERSE
)

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Archive settings
ARCHIVE_CHUNK_SIZE = 100  # Memories per archive file
COMPRESSION_ENABLED = True
ENCRYPTION_ENABLED = False  # Set to True when encryption is configured

# File extensions
ARCHIVE_EXTENSION = ".luna.archive"
ENCRYPTED_EXTENSION = ".luna.enc"
COMPRESSED_EXTENSION = ".gz"


# =============================================================================
# ARCHIVE ENTRY
# =============================================================================

@dataclass
class ArchiveEntry:
    """Represents an entry in the archive index."""
    memory_id: str
    archive_file: str
    offset: int  # Position in archive file
    size: int    # Size in bytes
    created_at: datetime
    memory_type: str
    checksum: str
    encrypted: bool = False
    compressed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "memory_id": self.memory_id,
            "archive_file": self.archive_file,
            "offset": self.offset,
            "size": self.size,
            "created_at": self.created_at.isoformat(),
            "memory_type": self.memory_type,
            "checksum": self.checksum,
            "encrypted": self.encrypted,
            "compressed": self.compressed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArchiveEntry':
        """Create from dictionary."""
        return cls(
            memory_id=data["memory_id"],
            archive_file=data["archive_file"],
            offset=data["offset"],
            size=data["size"],
            created_at=datetime.fromisoformat(data["created_at"]),
            memory_type=data["memory_type"],
            checksum=data["checksum"],
            encrypted=data.get("encrypted", False),
            compressed=data.get("compressed", False)
        )


# =============================================================================
# SECURE ENCRYPTION (AES-256 via Fernet with PBKDF2)
# =============================================================================

# Import cryptography modules for secure encryption
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    logger.warning("cryptography module not available - encryption disabled")


class SecureEncryption:
    """
    Secure encryption wrapper using AES-256 via Fernet.

    Uses PBKDF2 with 480,000 iterations for key derivation,
    providing strong protection against brute-force attacks.

    SEC-001 FIX: Replaced insecure XOR encryption with AES-256.
    """

    # PBKDF2 iterations (OWASP 2023 recommendation)
    PBKDF2_ITERATIONS = 480000

    def __init__(self, master_key_hex: Optional[str] = None):
        """
        Initialize secure encryption.

        Args:
            master_key_hex: Hex-encoded master key (min 32 chars = 128 bits).
                           If None, reads from LUNA_MASTER_KEY env var.
        """
        self._master_key_hex = master_key_hex or os.environ.get('LUNA_MASTER_KEY')
        self._fernet_cache: Dict[bytes, Fernet] = {}

        if not CRYPTOGRAPHY_AVAILABLE:
            logger.error("Cryptography module not installed - encryption unavailable")
            self._master_key_hex = None
        elif not self._master_key_hex or len(self._master_key_hex) < 32:
            logger.warning(
                "LUNA_MASTER_KEY not set or too short (min 32 hex chars). "
                "Encryption will be disabled."
            )
            self._master_key_hex = None

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive a Fernet key from master key using PBKDF2.

        Args:
            salt: 16-byte random salt

        Returns:
            URL-safe base64-encoded 32-byte key for Fernet
        """
        if not self._master_key_hex:
            raise ValueError("Master key not configured")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS,
        )

        key = kdf.derive(bytes.fromhex(self._master_key_hex))
        return base64.urlsafe_b64encode(key)

    def _get_fernet(self, salt: bytes) -> Fernet:
        """Get or create a Fernet instance for the given salt."""
        if salt not in self._fernet_cache:
            key = self._derive_key(salt)
            self._fernet_cache[salt] = Fernet(key)
        return self._fernet_cache[salt]

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data using AES-256 via Fernet.

        Format: [16-byte salt][Fernet ciphertext]

        Args:
            data: Plaintext bytes to encrypt

        Returns:
            Salt + ciphertext bytes
        """
        if not ENCRYPTION_ENABLED:
            return data

        if not self._master_key_hex or not CRYPTOGRAPHY_AVAILABLE:
            logger.warning("Encryption requested but not available - returning plaintext")
            return data

        # Generate random salt for this encryption
        salt = os.urandom(16)

        # Get Fernet instance and encrypt
        fernet = self._get_fernet(salt)
        ciphertext = fernet.encrypt(data)

        # Prepend salt to ciphertext
        return salt + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt data encrypted with this class.

        Args:
            data: Salt + ciphertext bytes

        Returns:
            Decrypted plaintext bytes
        """
        if not ENCRYPTION_ENABLED:
            return data

        if not self._master_key_hex or not CRYPTOGRAPHY_AVAILABLE:
            logger.warning("Decryption requested but not available - returning data as-is")
            return data

        if len(data) < 17:  # 16-byte salt + at least 1 byte
            raise ValueError("Invalid encrypted data: too short")

        # Extract salt and ciphertext
        salt = data[:16]
        ciphertext = data[16:]

        # Get Fernet instance and decrypt
        fernet = self._get_fernet(salt)
        return fernet.decrypt(ciphertext)

    def is_available(self) -> bool:
        """Check if encryption is properly configured."""
        return bool(self._master_key_hex and CRYPTOGRAPHY_AVAILABLE)


# Backward compatibility alias
SimpleEncryption = SecureEncryption


# =============================================================================
# ARCHIVE INDEX
# =============================================================================

class ArchiveIndex:
    """
    Manages the archive index for efficient lookup.
    """

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self._entries: Dict[str, ArchiveEntry] = {}
        self._lock = threading.RLock()

    def load(self) -> None:
        """Load index from disk."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for entry_data in data.get("entries", []):
                    entry = ArchiveEntry.from_dict(entry_data)
                    self._entries[entry.memory_id] = entry

                logger.info(f"Loaded archive index: {len(self._entries)} entries")

            except Exception as e:
                logger.error(f"Failed to load archive index: {e}")

    def save(self) -> None:
        """Save index to disk."""
        with self._lock:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "version": "2.0.0",
                "updated": datetime.now().isoformat(),
                "count": len(self._entries),
                "entries": [e.to_dict() for e in self._entries.values()]
            }

            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, entry: ArchiveEntry) -> None:
        """Add an entry to the index."""
        with self._lock:
            self._entries[entry.memory_id] = entry
            self.save()

    def remove(self, memory_id: str) -> Optional[ArchiveEntry]:
        """Remove an entry from the index."""
        with self._lock:
            entry = self._entries.pop(memory_id, None)
            if entry:
                self.save()
            return entry

    def get(self, memory_id: str) -> Optional[ArchiveEntry]:
        """Get an entry by memory ID."""
        return self._entries.get(memory_id)

    def get_all(self) -> List[ArchiveEntry]:
        """Get all entries."""
        return list(self._entries.values())

    def count(self) -> int:
        """Count entries."""
        return len(self._entries)

    def search_by_type(self, memory_type: str) -> List[ArchiveEntry]:
        """Search entries by memory type."""
        return [e for e in self._entries.values() if e.memory_type == memory_type]


# =============================================================================
# ARCHIVE MANAGER CLASS
# =============================================================================

class ArchiveManager:
    """
    Level 3 Archive Manager - Permanent encrypted storage.

    Provides:
    - Permanent memory storage
    - Optional encryption
    - Compression for space efficiency
    - Efficient retrieval via index
    """

    def __init__(
        self,
        archive_path: str,
        master_key_hex: Optional[str] = None
    ):
        """
        Initialize the archive manager.

        Args:
            archive_path: Base path for archive storage
            master_key_hex: Optional hex-encoded master key for encryption.
                           If None, reads from LUNA_MASTER_KEY env var.
        """
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.index = ArchiveIndex(self.archive_path / "archive_index.json")
        self.index.load()

        # SEC-001: Use SecureEncryption with AES-256
        self.encryption = SecureEncryption(master_key_hex)

        # Current archive file
        self._current_archive: Optional[Path] = None
        self._current_archive_count = 0

        self._lock = threading.RLock()

        # Statistics
        self._stats = {
            "total_archived": 0,
            "total_retrieved": 0,
            "total_size_bytes": 0
        }

        logger.info(f"ArchiveManager initialized at {archive_path}")

    # =========================================================================
    # CORE OPERATIONS
    # =========================================================================

    async def archive(
        self,
        memory: MemoryExperience,
        encrypt: bool = ENCRYPTION_ENABLED,
        compress: bool = COMPRESSION_ENABLED
    ) -> str:
        """
        Archive a memory experience.

        Args:
            memory: The memory to archive
            encrypt: Whether to encrypt
            compress: Whether to compress

        Returns:
            Archive entry ID
        """
        # Update layer
        memory.layer = MemoryLayer.ARCHIVE
        memory.archived = True
        memory.update()

        # Serialize
        data = json.dumps(memory.to_dict(), ensure_ascii=False).encode('utf-8')
        original_size = len(data)

        # Compress if enabled
        if compress:
            data = gzip.compress(data)

        # Encrypt if enabled
        if encrypt:
            data = self.encryption.encrypt(data)

        # Calculate checksum
        checksum = hashlib.sha256(data).hexdigest()

        # Get archive file
        archive_file = self._get_current_archive_file()

        # Write to archive
        with self._lock:
            with open(archive_file, 'ab') as f:
                offset = f.tell()
                f.write(data)
                size = len(data)

            self._current_archive_count += 1

        # Create index entry
        entry = ArchiveEntry(
            memory_id=memory.id,
            archive_file=str(archive_file.relative_to(self.archive_path)),
            offset=offset,
            size=size,
            created_at=memory.created_at,
            memory_type=memory.memory_type.value,
            checksum=checksum,
            encrypted=encrypt,
            compressed=compress
        )

        self.index.add(entry)

        # Update stats
        self._stats["total_archived"] += 1
        self._stats["total_size_bytes"] += size

        logger.debug(
            f"Archived memory {memory.id}: {original_size} -> {size} bytes "
            f"(compressed={compress}, encrypted={encrypt})"
        )

        return memory.id

    async def retrieve(self, memory_id: str) -> Optional[MemoryExperience]:
        """
        Retrieve a memory from the archive.

        Args:
            memory_id: The memory ID to retrieve

        Returns:
            The memory if found, None otherwise
        """
        # Get index entry
        entry = self.index.get(memory_id)
        if not entry:
            return None

        # Read from archive
        archive_file = self.archive_path / entry.archive_file

        if not archive_file.exists():
            logger.error(f"Archive file not found: {archive_file}")
            return None

        try:
            with open(archive_file, 'rb') as f:
                f.seek(entry.offset)
                data = f.read(entry.size)

            # Verify checksum
            if hashlib.sha256(data).hexdigest() != entry.checksum:
                logger.error(f"Checksum mismatch for {memory_id}")
                return None

            # Decrypt if needed
            if entry.encrypted:
                data = self.encryption.decrypt(data)

            # Decompress if needed
            if entry.compressed:
                data = gzip.decompress(data)

            # Deserialize
            memory_data = json.loads(data.decode('utf-8'))
            memory = MemoryExperience.from_dict(memory_data)

            self._stats["total_retrieved"] += 1

            return memory

        except Exception as e:
            logger.error(f"Failed to retrieve {memory_id}: {e}")
            return None

    async def search(
        self,
        query: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        limit: int = 100
    ) -> List[MemoryExperience]:
        """
        Search archived memories.

        Note: This is a slower operation as it may need to read from disk.

        Args:
            query: Text query
            memory_type: Filter by type
            created_after: Filter by creation date
            created_before: Filter by creation date
            limit: Maximum results

        Returns:
            List of matching memories
        """
        results = []
        entries = self.index.get_all()

        # Filter by type first (using index)
        if memory_type:
            entries = [e for e in entries if e.memory_type == memory_type.value]

        # Filter by date (using index)
        if created_after:
            entries = [e for e in entries if e.created_at >= created_after]
        if created_before:
            entries = [e for e in entries if e.created_at <= created_before]

        # Retrieve and filter by query
        for entry in entries:
            if len(results) >= limit:
                break

            memory = await self.retrieve(entry.memory_id)
            if not memory:
                continue

            # Query filter
            if query:
                query_lower = query.lower()
                if query_lower not in memory.content.lower():
                    continue

            results.append(memory)

        return results

    async def delete(self, memory_id: str) -> bool:
        """
        Mark a memory as deleted (does not remove from archive file).

        Args:
            memory_id: The memory to delete

        Returns:
            True if deleted from index
        """
        entry = self.index.remove(memory_id)
        if entry:
            logger.info(f"Removed {memory_id} from archive index")
            return True
        return False

    # =========================================================================
    # ARCHIVE FILE MANAGEMENT
    # =========================================================================

    def _get_current_archive_file(self) -> Path:
        """Get the current archive file, creating a new one if needed."""
        # Check if we need a new archive file
        if (
            self._current_archive is None or
            self._current_archive_count >= ARCHIVE_CHUNK_SIZE
        ):
            self._create_new_archive_file()

        return self._current_archive

    def _create_new_archive_file(self) -> None:
        """Create a new archive file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"archive_{timestamp}{ARCHIVE_EXTENSION}"

        self._current_archive = self.archive_path / filename
        self._current_archive_count = 0

        logger.debug(f"Created new archive file: {filename}")

    async def compact_archives(self) -> Dict[str, Any]:
        """
        Compact archive files by removing deleted entries.

        Returns:
            Compaction statistics
        """
        # Get all valid memory IDs from index
        valid_ids = set(entry.memory_id for entry in self.index.get_all())

        # Group by archive file
        files_to_compact = {}
        for entry in self.index.get_all():
            if entry.archive_file not in files_to_compact:
                files_to_compact[entry.archive_file] = []
            files_to_compact[entry.archive_file].append(entry)

        compacted = 0
        space_saved = 0

        for archive_file, entries in files_to_compact.items():
            old_path = self.archive_path / archive_file

            if not old_path.exists():
                continue

            # Create new compacted file
            new_path = old_path.with_suffix('.compact')

            with open(new_path, 'wb') as new_f:
                for entry in entries:
                    if entry.memory_id not in valid_ids:
                        space_saved += entry.size
                        continue

                    # Read from old file
                    with open(old_path, 'rb') as old_f:
                        old_f.seek(entry.offset)
                        data = old_f.read(entry.size)

                    # Write to new file
                    new_offset = new_f.tell()
                    new_f.write(data)

                    # Update entry
                    entry.offset = new_offset
                    compacted += 1

            # Replace old with new
            old_path.unlink()
            new_path.rename(old_path)

        # Save updated index
        self.index.save()

        return {
            "files_compacted": len(files_to_compact),
            "entries_compacted": compacted,
            "space_saved_bytes": space_saved
        }

    # =========================================================================
    # VERIFICATION
    # =========================================================================

    async def verify_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of all archived memories.

        Returns:
            Verification results
        """
        results = {
            "total": 0,
            "valid": 0,
            "corrupted": [],
            "missing": []
        }

        for entry in self.index.get_all():
            results["total"] += 1

            archive_file = self.archive_path / entry.archive_file

            if not archive_file.exists():
                results["missing"].append(entry.memory_id)
                continue

            try:
                with open(archive_file, 'rb') as f:
                    f.seek(entry.offset)
                    data = f.read(entry.size)

                checksum = hashlib.sha256(data).hexdigest()

                if checksum == entry.checksum:
                    results["valid"] += 1
                else:
                    results["corrupted"].append(entry.memory_id)

            except Exception as e:
                results["corrupted"].append(entry.memory_id)
                logger.warning(f"Verification failed for {entry.memory_id}: {e}")

        return results

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get archive statistics."""
        # Calculate actual size
        total_size = 0
        file_count = 0

        for archive_file in self.archive_path.glob(f"*{ARCHIVE_EXTENSION}"):
            total_size += archive_file.stat().st_size
            file_count += 1

        return {
            "total_memories": self.index.count(),
            "total_archived": self._stats["total_archived"],
            "total_retrieved": self._stats["total_retrieved"],
            "archive_files": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "compression_enabled": COMPRESSION_ENABLED,
            "encryption_enabled": ENCRYPTION_ENABLED,
            "memories_by_type": {
                mt.value: len(self.index.search_by_type(mt.value))
                for mt in MemoryType
            }
        }


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_archive_manager(
    archive_path: str,
    master_key_hex: Optional[str] = None
) -> ArchiveManager:
    """
    Factory function to create an ArchiveManager.

    Args:
        archive_path: Base path for archive storage
        master_key_hex: Optional hex-encoded master key for encryption.
                       If None, reads from LUNA_MASTER_KEY env var.

    Returns:
        Configured ArchiveManager instance
    """
    return ArchiveManager(
        archive_path=archive_path,
        master_key_hex=master_key_hex
    )
