"""
JSON file management utilities for Luna's fractal memory system.
Version: 2.0.2 - Security hardened with path traversal protection

Security Features (Phase 4):
- Path traversal protection via whitelist and regex validation
- Memory type validation (roots, branchs, leaves, seeds)
- Memory ID validation (alphanumeric pattern)
- Structured security logging
"""

import json
import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
from datetime import datetime, timezone
import hashlib
import shutil
from contextlib import contextmanager
import threading

# Security logging configuration
security_logger = logging.getLogger("luna.security.json_manager")


class PathTraversalError(Exception):
    """Raised when a path traversal attack is detected."""
    pass


class InvalidMemoryTypeError(Exception):
    """Raised when an invalid memory type is provided."""
    pass


class InvalidMemoryIdError(Exception):
    """Raised when an invalid memory ID format is provided."""
    pass

class JSONManager:
    """
    Manages JSON file operations with safety, efficiency, and security.

    Security Features:
    - Path traversal protection (../ detection and containment)
    - Memory type whitelist validation
    - Memory ID format validation (alphanumeric only)
    - All file operations contained within base_path
    """

    # SEC-009: Whitelist of valid memory types
    VALID_MEMORY_TYPES: Set[str] = frozenset({
        "roots", "branchs", "leaves", "seeds",  # Plural forms (directory names)
        "root", "branch", "leaf", "seed"         # Singular forms (for compatibility)
    })

    # SEC-009: Regex pattern for valid memory IDs
    # Format: type_12hexchars (e.g., root_a1b2c3d4e5f6)
    MEMORY_ID_PATTERN = re.compile(r'^[a-z]+_[a-f0-9]{12}$')

    # Alternative pattern for UUIDs and other valid formats
    SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')

    def __init__(self, base_path: Union[str, Path], encoding: str = 'utf-8'):
        """
        Initialize JSON manager with security validation.

        Args:
            base_path: Base directory for JSON operations (all paths must stay within)
            encoding: File encoding (default: utf-8)
        """
        self.base_path = Path(base_path).resolve()  # Resolve to absolute path
        self.encoding = encoding
        self._lock = threading.Lock()
        self._cache = {}
        self._cache_size_limit = 100  # Maximum cached files

        security_logger.info(
            f"JSONManager initialized with base_path: {self.base_path}"
        )

    # =========================================================================
    # SECURITY VALIDATION METHODS (SEC-009)
    # =========================================================================

    def validate_memory_type(self, memory_type: str) -> str:
        """
        Validate memory type against whitelist.

        Args:
            memory_type: Memory type to validate

        Returns:
            Validated memory type (normalized)

        Raises:
            InvalidMemoryTypeError: If memory type is not in whitelist
        """
        if not memory_type:
            raise InvalidMemoryTypeError("Memory type cannot be empty")

        normalized = memory_type.lower().strip()

        if normalized not in self.VALID_MEMORY_TYPES:
            security_logger.warning(
                f"SEC-009: Invalid memory type rejected: '{memory_type}'"
            )
            raise InvalidMemoryTypeError(
                f"Invalid memory type: '{memory_type}'. "
                f"Must be one of: {', '.join(sorted(self.VALID_MEMORY_TYPES))}"
            )

        return normalized

    def validate_memory_id(self, memory_id: str) -> str:
        """
        Validate memory ID format to prevent injection.

        Args:
            memory_id: Memory ID to validate

        Returns:
            Validated memory ID

        Raises:
            InvalidMemoryIdError: If memory ID format is invalid
        """
        if not memory_id:
            raise InvalidMemoryIdError("Memory ID cannot be empty")

        # Check for path traversal attempts in ID
        if '..' in memory_id or '/' in memory_id or '\\' in memory_id:
            security_logger.warning(
                f"SEC-009: Path traversal in memory_id rejected: '{memory_id}'"
            )
            raise InvalidMemoryIdError(
                f"Invalid memory ID: contains forbidden characters"
            )

        # Allow standard Luna memory ID format OR safe filename format
        if not (self.MEMORY_ID_PATTERN.match(memory_id) or
                self.SAFE_FILENAME_PATTERN.match(memory_id)):
            security_logger.warning(
                f"SEC-009: Invalid memory_id format rejected: '{memory_id}'"
            )
            raise InvalidMemoryIdError(
                f"Invalid memory ID format: '{memory_id}'. "
                "Must be alphanumeric with underscores/hyphens only"
            )

        return memory_id

    def validate_path_security(self, file_path: Union[str, Path]) -> Path:
        """
        Validate that path doesn't escape base directory.

        This is the CRITICAL security check that prevents path traversal attacks.

        Args:
            file_path: Path to validate

        Returns:
            Resolved absolute path (guaranteed within base_path)

        Raises:
            PathTraversalError: If path would escape base directory
        """
        path = Path(file_path)

        # Check for obvious traversal patterns BEFORE resolution
        path_str = str(file_path)
        if '..' in path_str:
            security_logger.critical(
                f"SEC-009: Path traversal attempt BLOCKED: '{file_path}'"
            )
            raise PathTraversalError(
                f"Path traversal detected: '..' is forbidden in paths"
            )

        # Resolve to absolute path
        if not path.is_absolute():
            resolved = (self.base_path / path).resolve()
        else:
            resolved = path.resolve()

        # CRITICAL: Ensure resolved path is within base_path
        try:
            resolved.relative_to(self.base_path)
        except ValueError:
            security_logger.critical(
                f"SEC-009: Path escape attempt BLOCKED: "
                f"'{file_path}' resolved to '{resolved}' "
                f"which is outside base_path '{self.base_path}'"
            )
            raise PathTraversalError(
                f"Access denied: path '{file_path}' is outside allowed directory"
            )

        return resolved

    def build_memory_path(
        self,
        memory_type: str,
        memory_id: str,
        extension: str = ".json"
    ) -> Path:
        """
        Safely build a memory file path with full validation.

        This is the RECOMMENDED method for constructing memory paths.

        Args:
            memory_type: Type of memory (roots/branchs/leaves/seeds)
            memory_id: Memory identifier
            extension: File extension (default: .json)

        Returns:
            Validated absolute path to memory file

        Raises:
            InvalidMemoryTypeError: If memory type invalid
            InvalidMemoryIdError: If memory ID invalid
            PathTraversalError: If resulting path is unsafe
        """
        # Validate components
        validated_type = self.validate_memory_type(memory_type)
        validated_id = self.validate_memory_id(memory_id)

        # Normalize to plural form for directory
        if not validated_type.endswith('s'):
            validated_type = validated_type + 's'

        # Build path safely
        filename = f"{validated_id}{extension}"
        relative_path = Path(validated_type) / filename

        # Final security validation
        return self.validate_path_security(relative_path)
        
    def read(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file with caching.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        full_path = self._resolve_path(file_path)
        
        # Check cache first
        cache_key = str(full_path)
        if cache_key in self._cache:
            return self._cache[cache_key].copy()
        
        with self._lock:
            with open(full_path, 'r', encoding=self.encoding) as f:
                data = json.load(f)
                
            # Update cache
            self._update_cache(cache_key, data)
            
        return data.copy()
        
    def write(self, file_path: Union[str, Path], data: Dict[str, Any], 
              create_backup: bool = True) -> None:
        """
        Write JSON file with optional backup.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            create_backup: Whether to create backup before writing
        """
        full_path = self._resolve_path(file_path)
        
        with self._lock:
            # Create backup if requested and file exists
            if create_backup and full_path.exists():
                self._create_backup(full_path)
                
            # Ensure directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write with temporary file for safety
            temp_path = full_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding=self.encoding) as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            # Atomic rename
            temp_path.replace(full_path)
            
            # Update cache
            cache_key = str(full_path)
            self._update_cache(cache_key, data)
            
    def update(self, file_path: Union[str, Path], 
               updates: Dict[str, Any], 
               create_if_missing: bool = True) -> Dict[str, Any]:
        """
        Update existing JSON file.
        
        Args:
            file_path: Path to JSON file
            updates: Dictionary of updates to apply
            create_if_missing: Create file if it doesn't exist
            
        Returns:
            Updated data
        """
        full_path = self._resolve_path(file_path)
        
        try:
            data = self.read(file_path)
        except FileNotFoundError:
            if create_if_missing:
                data = {}
            else:
                raise
                
        # Deep update
        data = self._deep_update(data, updates)
        
        # Write back
        self.write(file_path, data)
        
        return data
        
    def append_to_array(self, file_path: Union[str, Path], 
                       array_path: str, 
                       item: Any,
                       max_items: Optional[int] = None) -> None:
        """
        Append item to array within JSON file.
        
        Args:
            file_path: Path to JSON file
            array_path: Dot-notation path to array (e.g., "data.items")
            item: Item to append
            max_items: Maximum array size (removes oldest if exceeded)
        """
        data = self.read(file_path)
        
        # Navigate to array
        parts = array_path.split('.')
        current = data
        
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
            
        # Ensure array exists
        array_key = parts[-1]
        if array_key not in current:
            current[array_key] = []
            
        # Append item
        current[array_key].append(item)
        
        # Trim if needed
        if max_items and len(current[array_key]) > max_items:
            current[array_key] = current[array_key][-max_items:]
            
        self.write(file_path, data)
        
    def search(self, pattern: str, 
               search_in: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for pattern in JSON files.
        
        Args:
            pattern: Search pattern
            search_in: List of directories to search (relative to base_path)
            
        Returns:
            List of matches with file info
        """
        results = []
        search_dirs = search_in or ['.']
        
        for search_dir in search_dirs:
            dir_path = self.base_path / search_dir
            if not dir_path.exists():
                continue
                
            for json_file in dir_path.rglob('*.json'):
                try:
                    data = self.read(json_file)
                    if self._search_in_data(data, pattern):
                        results.append({
                            'file': str(json_file.relative_to(self.base_path)),
                            'data': data,
                            'matches': self._find_matches(data, pattern)
                        })
                except Exception:
                    # Skip files that can't be read
                    pass
                    
        return results
        
    def get_statistics(self, directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about JSON files.
        
        Args:
            directory: Specific directory to analyze
            
        Returns:
            Statistics dictionary
        """
        stats = {
            'total_files': 0,
            'total_size_bytes': 0,
            'average_size_bytes': 0,
            'largest_file': None,
            'file_types': {}
        }
        
        search_path = self.base_path / directory if directory else self.base_path
        
        for json_file in search_path.rglob('*.json'):
            stats['total_files'] += 1
            size = json_file.stat().st_size
            stats['total_size_bytes'] += size
            
            if not stats['largest_file'] or size > stats['largest_file']['size']:
                stats['largest_file'] = {
                    'path': str(json_file.relative_to(self.base_path)),
                    'size': size
                }
                
            # Categorize by parent directory
            parent = json_file.parent.name
            stats['file_types'][parent] = stats['file_types'].get(parent, 0) + 1
            
        if stats['total_files'] > 0:
            stats['average_size_bytes'] = stats['total_size_bytes'] / stats['total_files']
            
        return stats
        
    @contextmanager
    def transaction(self, file_path: Union[str, Path]):
        """
        Context manager for transactional updates.
        
        Args:
            file_path: Path to JSON file
            
        Yields:
            Data dictionary that will be saved on exit
        """
        data = self.read(file_path)
        original = data.copy()
        
        try:
            yield data
            self.write(file_path, data)
        except Exception:
            # Rollback on error
            self.write(file_path, original)
            raise
            
    def validate_schema(self, file_path: Union[str, Path], 
                       schema: Dict[str, Any]) -> List[str]:
        """
        Validate JSON file against schema.
        
        Args:
            file_path: Path to JSON file
            schema: JSON schema dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        try:
            from jsonschema import validate, ValidationError
        except ImportError:
            return ["jsonschema package not installed"]
            
        data = self.read(file_path)
        errors = []
        
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            errors.append(str(e))
            
        return errors
        
    def merge_files(self, file_paths: List[Union[str, Path]], 
                   output_path: Union[str, Path],
                   merge_arrays: bool = True) -> None:
        """
        Merge multiple JSON files.
        
        Args:
            file_paths: List of files to merge
            output_path: Output file path
            merge_arrays: Whether to concatenate arrays
        """
        merged = {}
        
        for file_path in file_paths:
            data = self.read(file_path)
            if merge_arrays:
                merged = self._deep_merge_with_arrays(merged, data)
            else:
                merged = self._deep_update(merged, data)
                
        self.write(output_path, merged)
        
    # =========================================================================
    # PRIVATE HELPER METHODS
    # =========================================================================

    def _resolve_path(self, file_path: Union[str, Path]) -> Path:
        """
        Resolve file path relative to base path WITH SECURITY VALIDATION.

        This method now includes path traversal protection.

        Args:
            file_path: Path to resolve

        Returns:
            Resolved absolute path (guaranteed within base_path)

        Raises:
            PathTraversalError: If path would escape base directory
        """
        # SEC-009: Use security-validated path resolution
        return self.validate_path_security(file_path)
        
    def _create_backup(self, file_path: Path) -> None:
        """Create backup of file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = file_path.with_suffix(f'.backup_{timestamp}.json')
        shutil.copy2(file_path, backup_path)
        
    def _update_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Update cache with size limit."""
        self._cache[key] = data.copy()
        
        # Evict oldest if cache too large
        if len(self._cache) > self._cache_size_limit:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
            
    def _deep_update(self, base: Dict, updates: Dict) -> Dict:
        """Deep update dictionary."""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._deep_update(base[key], value)
            else:
                base[key] = value
        return base
        
    def _deep_merge_with_arrays(self, base: Dict, updates: Dict) -> Dict:
        """Deep merge dictionaries, concatenating arrays."""
        for key, value in updates.items():
            if key in base:
                if isinstance(value, dict) and isinstance(base[key], dict):
                    base[key] = self._deep_merge_with_arrays(base[key], value)
                elif isinstance(value, list) and isinstance(base[key], list):
                    base[key].extend(value)
                else:
                    base[key] = value
            else:
                base[key] = value
        return base
        
    def _search_in_data(self, data: Any, pattern: str) -> bool:
        """Search for pattern in data structure."""
        pattern_lower = pattern.lower()
        
        if isinstance(data, str):
            return pattern_lower in data.lower()
        elif isinstance(data, (list, tuple)):
            return any(self._search_in_data(item, pattern) for item in data)
        elif isinstance(data, dict):
            return any(self._search_in_data(value, pattern) for value in data.values())
        else:
            return pattern_lower in str(data).lower()
            
    def _find_matches(self, data: Any, pattern: str, path: str = "") -> List[str]:
        """Find all matching paths in data."""
        matches = []
        pattern_lower = pattern.lower()
        
        if isinstance(data, str) and pattern_lower in data.lower():
            matches.append(path)
        elif isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                matches.extend(self._find_matches(value, pattern, new_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                matches.extend(self._find_matches(item, pattern, new_path))
                
        return matches
        
    def calculate_checksum(self, file_path: Union[str, Path]) -> str:
        """Calculate SHA256 checksum of JSON file."""
        full_path = self._resolve_path(file_path)
        
        with open(full_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()