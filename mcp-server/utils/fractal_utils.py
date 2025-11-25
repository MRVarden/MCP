"""
Fractal utilities for Luna consciousness system
Version: 2.0.1 - Orchestrated fractal memory with Update01.md
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid


@dataclass
class FractalNode:
    """Represents a node in the fractal memory structure"""
    id: str
    content: Any
    level: int
    children: List[str]
    parent: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class FractalUtils:
    """Utilities for working with fractal structures"""

    @staticmethod
    def generate_fractal_id(level: int, content_hash: str) -> str:
        """Generate a unique fractal node ID"""
        return f"fractal_{level}_{content_hash[:8]}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def calculate_fractal_depth(node: FractalNode) -> int:
        """Calculate the depth of a fractal node"""
        return node.level

    @staticmethod
    def create_fractal_signature(content: str) -> str:
        """Create a fractal signature for content"""
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()
