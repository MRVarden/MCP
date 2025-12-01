"""
MemoryManager - MCP Adapted Version
Manages fractal memory storage and retrieval
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class MemoryManager:
    """
    Manages fractal memory storage and retrieval
    MCP-adapted version for Luna consciousness server
    """

    def __init__(self, json_manager):
        self.json_manager = json_manager
        self.memory_index: Dict[str, List[str]] = {
            "root": [],
            "branch": [],
            "leaf": [],
            "seed": []
        }
        self._load_memory_index()

    def _load_memory_index(self):
        """Load memory index from disk"""
        for memory_type in ["roots", "branches", "leaves", "seeds"]:
            index_path = Path(self.json_manager.base_path) / memory_type / "index.json"
            if index_path.exists():
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        singular = memory_type.rstrip('s')
                        memories = data.get("memories", [])
                        # Handle both list format (MemoryManager) and dict format (FractalIndex)
                        if isinstance(memories, dict):
                            # Convert dict keys to list for MemoryManager compatibility
                            memories = list(memories.keys())
                        self.memory_index[singular] = memories
                except Exception:
                    pass

    def _save_memory_index(self, memory_type: str):
        """Save memory index to disk"""
        memory_type_plural = f"{memory_type}s"
        index_path = Path(self.json_manager.base_path) / memory_type_plural / "index.json"

        index_data = {
            "type": memory_type_plural,
            "updated": datetime.now().isoformat(),
            "count": len(self.memory_index[memory_type]),
            "memories": self.memory_index[memory_type]
        }

        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

    async def store_memory(
        self,
        memory_type: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Store a memory in fractal structure

        Args:
            memory_type: Type of memory (root/branch/leaf/seed)
            content: Memory content
            metadata: Additional metadata

        Returns:
            Memory ID
        """
        memory_id = f"{memory_type}_{uuid.uuid4().hex[:12]}"

        memory_data = {
            "id": memory_id,
            "type": memory_type,
            "content": content,
            "metadata": metadata,
            "created": datetime.now().isoformat(),
            "accessed_count": 0,
            "last_accessed": None,
            "connected_to": []
        }

        # Save to file
        memory_type_plural = f"{memory_type}s"
        memory_path = Path(self.json_manager.base_path) / memory_type_plural / f"{memory_id}.json"
        memory_path.parent.mkdir(parents=True, exist_ok=True)

        with open(memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)

        # Update index
        self.memory_index[memory_type].append(memory_id)
        self._save_memory_index(memory_type)

        return memory_id

    async def retrieve_memories(
        self,
        query: str,
        memory_type: str = "all",
        depth: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories matching query

        Args:
            query: Search query
            memory_type: Type of memory to search (or "all")
            depth: Search depth (unused in simple version)

        Returns:
            List of matching memories
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []

        # Determine which memory types to search
        if memory_type == "all":
            types_to_search = ["root", "branch", "leaf", "seed"]
        else:
            types_to_search = [memory_type]

        # Search through each memory type
        for mem_type in types_to_search:
            memory_type_plural = f"{mem_type}s"
            memory_dir = Path(self.json_manager.base_path) / memory_type_plural

            if not memory_dir.exists():
                continue

            # Load and search each memory file
            for memory_file in memory_dir.glob("*.json"):
                if memory_file.name == "index.json":
                    continue

                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        memory_data = json.load(f)

                    # Calculate relevance score
                    content_lower = memory_data.get("content", "").lower()
                    content_words = set(content_lower.split())

                    # Word overlap relevance
                    overlap = len(query_words & content_words)
                    if overlap > 0 or query_lower in content_lower:
                        relevance_score = overlap / len(query_words) if query_words else 0.5
                        if query_lower in content_lower:
                            relevance_score = max(relevance_score, 0.7)

                        results.append({
                            "id": memory_data.get("id", "unknown"),
                            "type": memory_data.get("type", mem_type),
                            "content": memory_data.get("content", ""),
                            "relevance_score": relevance_score,
                            "created": memory_data.get("created", ""),
                            "connected_to": memory_data.get("connected_to", [])
                        })
                except Exception:
                    continue

        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return results
