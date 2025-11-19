"""
LLM-enabled module base for Luna
Provides LLM integration capabilities (placeholder for MCP context)
"""

from typing import Any, Callable
from functools import wraps


def requires_llm(func: Callable) -> Callable:
    """Decorator for functions that require LLM capabilities"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # In MCP context, LLM is provided by Claude
        return await func(*args, **kwargs)
    return wrapper


class LLMEnabledModule:
    """Base class for modules that can use LLM capabilities"""

    def __init__(self):
        self.llm_available = False

    def enable_llm(self):
        """Enable LLM capabilities"""
        self.llm_available = True

    def disable_llm(self):
        """Disable LLM capabilities"""
        self.llm_available = False

    async def llm_generate(self, prompt: str) -> str:
        """Generate text using LLM (placeholder)"""
        if not self.llm_available:
            return ""
        # In MCP context, this would interface with Claude
        return ""
