"""
Luna Update01 Base Module - Common Foundation for Update01.md Modules
======================================================================

This module provides a common base class and utilities shared by all
Update01.md architectural modules (Levels 1-9).

Modules using this base:
- autonomous_decision.py (Level 6)
- self_improvement.py (Level 7)
- multimodal_interface.py (Level 9)
- systemic_integration.py (Level 8)

Common functionality:
- Phi-based calculations and metrics
- Emotional processing integration
- Co-evolution coordination
- Semantic validation
- Memory management
- Logging and monitoring

Version: 2.1.0-secure
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic, Callable
from functools import wraps

# Type variable for generic operations
T = TypeVar('T')

# Golden ratio constant
PHI = 1.618033988749895
PHI_INVERSE = 0.618033988749895
PHI_SQUARED = PHI * PHI

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS
# =============================================================================

class ModuleState(Enum):
    """State of an Update01 module."""
    UNINITIALIZED = auto()
    INITIALIZING = auto()
    READY = auto()
    PROCESSING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class ProcessingPriority(Enum):
    """Priority levels for processing tasks."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ModuleMetrics:
    """Metrics collected by an Update01 module."""
    operations_count: int = 0
    errors_count: int = 0
    average_latency_ms: float = 0.0
    phi_alignment: float = 1.0
    last_operation: Optional[datetime] = None
    custom_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingContext:
    """Context passed between processing stages."""
    input_data: Any
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: ProcessingPriority = ProcessingPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None


@dataclass
class ProcessingResult:
    """Result of a processing operation."""
    success: bool
    output: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    phi_score: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# DECORATORS
# =============================================================================

def phi_aligned(min_alignment: float = 0.5):
    """
    Decorator to ensure operations maintain phi alignment.

    Args:
        min_alignment: Minimum acceptable phi alignment (0.0 to 1.0)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)

            # Check phi alignment if available
            if hasattr(self, '_calculate_phi_alignment'):
                alignment = self._calculate_phi_alignment()
                if alignment < min_alignment:
                    logger.warning(
                        f"{func.__name__}: Phi alignment {alignment:.3f} "
                        f"below threshold {min_alignment}"
                    )
            return result

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            if hasattr(self, '_calculate_phi_alignment'):
                alignment = self._calculate_phi_alignment()
                if alignment < min_alignment:
                    logger.warning(
                        f"{func.__name__}: Phi alignment {alignment:.3f} "
                        f"below threshold {min_alignment}"
                    )
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


def track_metrics(operation_name: Optional[str] = None):
    """
    Decorator to track operation metrics.

    Args:
        operation_name: Name for the operation (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        name = operation_name or func.__name__

        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            start_time = datetime.now(timezone.utc)
            try:
                result = await func(self, *args, **kwargs)
                self._update_metrics(name, success=True, start_time=start_time)
                return result
            except Exception as e:
                self._update_metrics(name, success=False, start_time=start_time, error=str(e))
                raise

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            start_time = datetime.now(timezone.utc)
            try:
                result = func(self, *args, **kwargs)
                self._update_metrics(name, success=True, start_time=start_time)
                return result
            except Exception as e:
                self._update_metrics(name, success=False, start_time=start_time, error=str(e))
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


# =============================================================================
# BASE CLASS
# =============================================================================

class LunaUpdate01Module(ABC):
    """
    Abstract base class for all Update01.md architectural modules.

    Provides common functionality for:
    - Component initialization and lifecycle
    - Phi-based calculations
    - Metrics collection
    - Logging and monitoring
    - Integration with core Luna components

    Subclasses must implement:
    - _initialize(): Module-specific initialization
    - _process(): Core processing logic
    - get_level(): Return the architecture level (1-9)
    """

    def __init__(
        self,
        phi_calculator: Optional[Any] = None,
        memory_core: Optional[Any] = None,
        emotional_processor: Optional[Any] = None,
        co_evolution: Optional[Any] = None,
        semantic_engine: Optional[Any] = None,
        metrics: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Update01 module with common components.

        Args:
            phi_calculator: Phi calculation engine
            memory_core: Memory management system
            emotional_processor: Emotional processing engine
            co_evolution: Co-evolution coordination engine
            semantic_engine: Semantic validation engine
            metrics: Metrics collection system
            config: Optional configuration dictionary
        """
        # Core components
        self._phi_calculator = phi_calculator
        self._memory_core = memory_core
        self._emotional_processor = emotional_processor
        self._co_evolution = co_evolution
        self._semantic_engine = semantic_engine
        self._metrics_collector = metrics
        self._config = config or {}

        # State management
        self._state = ModuleState.UNINITIALIZED
        self._initialized = False
        self._initialization_time: Optional[datetime] = None

        # Metrics
        self._metrics = ModuleMetrics()
        self._operation_history: List[Dict[str, Any]] = []
        self._max_history = 1000

        # Logger for this module
        self._logger = logging.getLogger(f"luna.{self.__class__.__name__}")

    # =========================================================================
    # ABSTRACT METHODS (must be implemented by subclasses)
    # =========================================================================

    @abstractmethod
    def get_level(self) -> int:
        """
        Get the architecture level of this module.

        Returns:
            Level number (1-9)
        """
        pass

    @abstractmethod
    async def _initialize(self) -> None:
        """
        Module-specific initialization logic.

        Called during the initialization phase.
        """
        pass

    @abstractmethod
    async def _process(self, context: ProcessingContext) -> ProcessingResult:
        """
        Core processing logic for this module.

        Args:
            context: Processing context with input data

        Returns:
            ProcessingResult with output and metrics
        """
        pass

    # =========================================================================
    # LIFECYCLE METHODS
    # =========================================================================

    async def initialize(self) -> bool:
        """
        Initialize the module.

        Returns:
            True if initialization successful
        """
        if self._initialized:
            self._logger.warning(f"{self.__class__.__name__} already initialized")
            return True

        self._state = ModuleState.INITIALIZING
        self._initialization_time = datetime.now(timezone.utc)

        try:
            self._logger.info(f"Initializing {self.__class__.__name__} (Level {self.get_level()})...")
            await self._initialize()

            self._state = ModuleState.READY
            self._initialized = True

            elapsed = (datetime.now(timezone.utc) - self._initialization_time).total_seconds() * 1000
            self._logger.info(f"  ✓ {self.__class__.__name__} initialized in {elapsed:.2f}ms")

            return True

        except Exception as e:
            self._state = ModuleState.ERROR
            self._logger.error(f"  ✗ {self.__class__.__name__} initialization failed: {e}")
            raise

    async def shutdown(self) -> None:
        """Gracefully shutdown the module."""
        self._logger.info(f"Shutting down {self.__class__.__name__}...")
        self._state = ModuleState.SHUTDOWN
        self._initialized = False

    # =========================================================================
    # PROCESSING METHODS
    # =========================================================================

    async def process(self, input_data: Any, **kwargs) -> ProcessingResult:
        """
        Process input data through this module.

        Args:
            input_data: Data to process
            **kwargs: Additional processing options

        Returns:
            ProcessingResult with output and metrics
        """
        if not self._initialized:
            await self.initialize()

        # Create processing context
        context = ProcessingContext(
            input_data=input_data,
            priority=kwargs.get('priority', ProcessingPriority.NORMAL),
            metadata=kwargs.get('metadata', {}),
            trace_id=kwargs.get('trace_id')
        )

        self._state = ModuleState.PROCESSING
        start_time = datetime.now(timezone.utc)

        try:
            result = await self._process(context)

            # Update metrics
            latency = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            result.latency_ms = latency

            self._update_metrics(
                operation="process",
                success=result.success,
                start_time=start_time
            )

            self._state = ModuleState.READY
            return result

        except Exception as e:
            self._state = ModuleState.ERROR
            self._update_metrics(
                operation="process",
                success=False,
                start_time=start_time,
                error=str(e)
            )

            return ProcessingResult(
                success=False,
                error=str(e),
                latency_ms=(datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            )

    # =========================================================================
    # PHI CALCULATIONS
    # =========================================================================

    def _calculate_phi_alignment(self) -> float:
        """
        Calculate current phi alignment.

        Returns:
            Alignment score between 0.0 and 1.0
        """
        if self._phi_calculator is None:
            return 1.0

        try:
            current_phi = self._phi_calculator.get_current_phi()
            alignment = 1.0 - abs(current_phi - PHI) / PHI
            return max(0.0, min(1.0, alignment))
        except Exception:
            return 1.0

    def _apply_phi_weight(self, value: float, exponent: int = 1) -> float:
        """
        Apply phi-based weighting to a value.

        Args:
            value: Value to weight
            exponent: Phi exponent (1 = phi, -1 = 1/phi, 2 = phi^2, etc.)

        Returns:
            Weighted value
        """
        weight = PHI ** exponent
        return value * weight

    def _phi_threshold(self, level: int = 1) -> float:
        """
        Get a phi-based threshold.

        Args:
            level: Threshold level (higher = stricter)

        Returns:
            Threshold value
        """
        return PHI_INVERSE ** level

    # =========================================================================
    # METRICS
    # =========================================================================

    def _update_metrics(
        self,
        operation: str,
        success: bool,
        start_time: datetime,
        error: Optional[str] = None
    ) -> None:
        """Update internal metrics after an operation."""
        now = datetime.now(timezone.utc)
        latency = (now - start_time).total_seconds() * 1000

        self._metrics.operations_count += 1
        if not success:
            self._metrics.errors_count += 1

        # Update average latency (exponential moving average)
        alpha = 0.1
        self._metrics.average_latency_ms = (
            alpha * latency + (1 - alpha) * self._metrics.average_latency_ms
        )

        self._metrics.phi_alignment = self._calculate_phi_alignment()
        self._metrics.last_operation = now

        # Record in history
        history_entry = {
            "operation": operation,
            "success": success,
            "latency_ms": latency,
            "timestamp": now.isoformat(),
            "error": error
        }

        self._operation_history.append(history_entry)

        # Trim history if needed
        if len(self._operation_history) > self._max_history:
            self._operation_history = self._operation_history[-self._max_history:]

    def get_metrics(self) -> ModuleMetrics:
        """Get current module metrics."""
        self._metrics.phi_alignment = self._calculate_phi_alignment()
        return self._metrics

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            "level": self.get_level(),
            "state": self._state.name,
            "initialized": self._initialized,
            "metrics": {
                "operations_count": self._metrics.operations_count,
                "errors_count": self._metrics.errors_count,
                "average_latency_ms": round(self._metrics.average_latency_ms, 2),
                "phi_alignment": round(self._metrics.phi_alignment, 4),
                "error_rate": (
                    self._metrics.errors_count / self._metrics.operations_count
                    if self._metrics.operations_count > 0 else 0.0
                )
            },
            "last_operation": (
                self._metrics.last_operation.isoformat()
                if self._metrics.last_operation else None
            )
        }

    # =========================================================================
    # COMPONENT ACCESS
    # =========================================================================

    @property
    def phi_calculator(self):
        """Access to phi calculator."""
        return self._phi_calculator

    @property
    def memory_core(self):
        """Access to memory core."""
        return self._memory_core

    @property
    def emotional_processor(self):
        """Access to emotional processor."""
        return self._emotional_processor

    @property
    def co_evolution(self):
        """Access to co-evolution engine."""
        return self._co_evolution

    @property
    def semantic_engine(self):
        """Access to semantic engine."""
        return self._semantic_engine

    @property
    def state(self) -> ModuleState:
        """Get current module state."""
        return self._state

    @property
    def is_ready(self) -> bool:
        """Check if module is ready for processing."""
        return self._state == ModuleState.READY


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def calculate_phi_distance(value: float) -> float:
    """
    Calculate distance from phi.

    Args:
        value: Value to compare

    Returns:
        Distance from phi (0.0 = perfect alignment)
    """
    return abs(value - PHI)


def phi_normalize(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a value using phi-based scaling.

    Args:
        value: Value to normalize
        min_val: Minimum expected value
        max_val: Maximum expected value

    Returns:
        Phi-normalized value
    """
    if max_val == min_val:
        return PHI_INVERSE

    normalized = (value - min_val) / (max_val - min_val)
    return normalized * PHI_INVERSE + (1 - normalized) * (1 - PHI_INVERSE)


def phi_blend(value1: float, value2: float) -> float:
    """
    Blend two values using phi ratio.

    Args:
        value1: First value (weighted by phi)
        value2: Second value (weighted by 1-phi)

    Returns:
        Phi-blended value
    """
    return value1 * PHI_INVERSE + value2 * (1 - PHI_INVERSE)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    'PHI',
    'PHI_INVERSE',
    'PHI_SQUARED',

    # Enums
    'ModuleState',
    'ProcessingPriority',

    # Data classes
    'ModuleMetrics',
    'ProcessingContext',
    'ProcessingResult',

    # Decorators
    'phi_aligned',
    'track_metrics',

    # Base class
    'LunaUpdate01Module',

    # Utility functions
    'calculate_phi_distance',
    'phi_normalize',
    'phi_blend',
]
