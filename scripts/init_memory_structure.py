#!/usr/bin/env python3
"""
Initialize Luna Fractal Memory Structure
Creates initial JSON files for the fractal memory system
"""

import os
import json
from datetime import datetime

MEMORY_PATH = "/app/memory_fractal"

def init_memory_structure():
    """Initialize the fractal memory structure with base files"""

    # Create base structure for each memory type
    memory_types = ["roots", "branches", "leaves", "seeds"]

    for memory_type in memory_types:
        type_path = os.path.join(MEMORY_PATH, memory_type)
        os.makedirs(type_path, exist_ok=True)

        # Create index file
        index_file = os.path.join(type_path, "index.json")
        if not os.path.exists(index_file):
            index_data = {
                "type": memory_type,
                "created": datetime.now().isoformat(),
                "count": 0,
                "memories": []
            }
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)

    # Create root config file
    config_file = os.path.join(MEMORY_PATH, "memory_config.json")
    if not os.path.exists(config_file):
        config_data = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "phi_threshold": 1.618033988749895,
            "max_depth": 10,
            "memory_types": {
                "roots": "Fundamental concepts and core knowledge",
                "branches": "Emergent themes and connections",
                "leaves": "Individual conversations and interactions",
                "seeds": "Atomic fragments and micro-insights"
            }
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    print("✅ Fractal memory structure initialized successfully")
    print(f"📂 Memory path: {MEMORY_PATH}")
    print(f"🌳 Structure: {', '.join(memory_types)}")

if __name__ == "__main__":
    init_memory_structure()
