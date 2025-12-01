"""
Luna Core Facade - Unified Interface for Luna Architecture
============================================================

This module provides a unified facade for the Luna 9-level architecture,
simplifying access to all modules and managing dependencies.

Architecture Levels (execution order):
=====================================
Level 1: LunaOrchestrator       - Central orchestration (entry point)
Level 2: LunaValidator          - Validation with veto (input filter)
Level 3: PredictiveCore         - Predictive system (anticipation)
Level 4: ManipulationDetector   - Manipulation detection (security)
Level 5: (reserved)             - Future extension
Level 6: AutonomousDecision     - Autonomous decisions (action)
Level 7: SelfImprovement        - Self-improvement (evolution)
Level 8: SystemicIntegration    - Systemic integration (coordination)
Level 9: MultimodalInterface    - Multimodal interface (user output)

Pure Memory Architecture (3 levels):
===================================
Level 1: Buffer    - Redis cache (<1ms latency)
Level 2: Fractal   - JSON storage (<10ms latency)
Level 3: Archive   - Encrypted permanent (<100ms latency)

Usage:
=====
    from luna_core.facade import LunaCoreFacade

    facade = LunaCoreFacade(json_manager, config)
    await facade.initialize()

    # Access components
    orchestrator = facade.orchestrator
    validator = facade.validator

    # Access Pure Memory
    pure_memory = facade.pure_memory
    await pure_memory.store(memory_experience)

    # Get status
    status = facade.get_status()

Version: 2.1.0-secure
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Type, TypeVar, Generic
from pathlib import Path

logger = logging.getLogger(__name__)

# Type variable for component types
T = TypeVar('T')


class ComponentLevel(Enum):
    """Architecture levels for Luna components."""
    LEVEL_1_ORCHESTRATOR = 1
    LEVEL_2_VALIDATOR = 2
    LEVEL_3_PREDICTIVE = 3
    LEVEL_4_MANIPULATION = 4
    LEVEL_5_RESERVED = 5
    LEVEL_6_AUTONOMOUS = 6
    LEVEL_7_IMPROVEMENT = 7
    LEVEL_8_SYSTEMIC = 8
    LEVEL_9_MULTIMODAL = 9


class InitializationPhase(Enum):
    """Initialization phases for ordered component startup."""
    PHASE_1_PARALLEL = auto()     # Components without dependencies
    PHASE_2_DEPENDENT = auto()    # Components depending on Phase 1
    PHASE_3_FINAL = auto()        # Components requiring all others


@dataclass
class ComponentStatus:
    """Status of a single component."""
    name: str
    level: ComponentLevel
    initialized: bool = False
    healthy: bool = True
    last_error: Optional[str] = None
    last_activity: Optional[datetime] = None
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FacadeStatus:
    """Overall status of the Luna facade."""
    initialized: bool = False
    healthy: bool = True
    components: Dict[str, ComponentStatus] = field(default_factory=dict)
    initialization_time_ms: float = 0.0
    phi_alignment: float = 1.0
    last_error: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class LazyComponent(Generic[T]):
    """
    Lazy-loading wrapper for Luna components.

    Components are only instantiated when first accessed,
    reducing startup time and memory usage.
    """

    def __init__(
        self,
        factory: callable,
        level: ComponentLevel,
        name: str,
        dependencies: Optional[List[str]] = None
    ):
        """
        Initialize lazy component wrapper.

        Args:
            factory: Factory function to create the component
            level: Architecture level of the component
            name: Human-readable name
            dependencies: List of dependency names
        """
        self._factory = factory
        self._instance: Optional[T] = None
        self._level = level
        self._name = name
        self._dependencies = dependencies or []
        self._initialized = False
        self._error: Optional[str] = None

    @property
    def instance(self) -> Optional[T]:
        """Get the component instance, creating it if necessary."""
        if self._instance is None and self._factory is not None:
            try:
                self._instance = self._factory()
                self._initialized = True
            except Exception as e:
                self._error = str(e)
                logger.error(f"Failed to create {self._name}: {e}")
        return self._instance

    @property
    def is_initialized(self) -> bool:
        """Check if component is initialized."""
        return self._initialized

    @property
    def level(self) -> ComponentLevel:
        """Get component level."""
        return self._level

    @property
    def name(self) -> str:
        """Get component name."""
        return self._name

    @property
    def dependencies(self) -> List[str]:
        """Get component dependencies."""
        return self._dependencies

    @property
    def error(self) -> Optional[str]:
        """Get last error if any."""
        return self._error

    def get_status(self) -> ComponentStatus:
        """Get component status."""
        return ComponentStatus(
            name=self._name,
            level=self._level,
            initialized=self._initialized,
            healthy=self._error is None,
            last_error=self._error,
            last_activity=datetime.now(timezone.utc) if self._initialized else None
        )


class LunaCoreFacade:
    """
    Facade for the Luna 9-level architecture.

    Provides unified access to all Luna modules with:
    - Lazy initialization of components
    - Dependency management
    - Ordered initialization by levels
    - Centralized status monitoring
    - Simplified API for common operations

    Example:
        facade = LunaCoreFacade(json_manager)
        await facade.initialize()

        # Process user input through the full pipeline
        result = await facade.process_interaction("Hello Luna")
    """

    def __init__(
        self,
        json_manager: Any,
        config: Optional[Dict[str, Any]] = None,
        memory_path: Optional[str] = None
    ):
        """
        Initialize the Luna Core Facade.

        Args:
            json_manager: JSON manager for persistence
            config: Optional configuration dictionary
            memory_path: Optional path for memory storage
        """
        self._json_manager = json_manager
        self._config = config or {}
        self._memory_path = memory_path or str(
            getattr(json_manager, 'base_path', Path('/app/memory_fractal'))
        )

        # Component registry
        self._components: Dict[str, LazyComponent] = {}

        # Initialization state
        self._initialized = False
        self._initialization_time_ms = 0.0

        # Shared instances (created during initialization)
        self._phi_calculator = None
        self._memory_manager = None
        self._consciousness_engine = None
        self._emotional_processor = None
        self._semantic_engine = None
        self._co_evolution_engine = None

        # Pure Memory instance
        self._pure_memory = None
        self._redis_url = None
        self._master_key_hex = None

        # Register all components
        self._register_components()

        logger.info("LunaCoreFacade created - components registered for lazy loading")

    def _register_components(self) -> None:
        """Register all Luna components with their factories."""

        # =================================================================
        # Foundation Layer (no inter-module dependencies)
        # =================================================================

        self._components['phi_calculator'] = LazyComponent(
            factory=self._create_phi_calculator,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="PhiCalculator"
        )

        self._components['memory_manager'] = LazyComponent(
            factory=self._create_memory_manager,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="MemoryManager"
        )

        self._components['emotional_processor'] = LazyComponent(
            factory=self._create_emotional_processor,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="EmotionalProcessor"
        )

        self._components['semantic_engine'] = LazyComponent(
            factory=self._create_semantic_engine,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="SemanticValidator"
        )

        self._components['co_evolution_engine'] = LazyComponent(
            factory=self._create_co_evolution_engine,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="CoEvolutionEngine"
        )

        self._components['consciousness_engine'] = LazyComponent(
            factory=self._create_consciousness_engine,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="FractalPhiConsciousnessEngine",
            dependencies=['phi_calculator']
        )

        # =================================================================
        # Level 1: Orchestrator
        # =================================================================

        self._components['orchestrator'] = LazyComponent(
            factory=self._create_orchestrator,
            level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
            name="LunaOrchestrator",
            dependencies=['phi_calculator', 'consciousness_engine', 'memory_manager']
        )

        # =================================================================
        # Level 3: Predictive Core
        # =================================================================

        self._components['predictive_core'] = LazyComponent(
            factory=self._create_predictive_core,
            level=ComponentLevel.LEVEL_3_PREDICTIVE,
            name="LunaPredictiveCore",
            dependencies=['memory_manager']
        )

        # =================================================================
        # Level 4: Manipulation Detector
        # =================================================================

        self._components['manipulation_detector'] = LazyComponent(
            factory=self._create_manipulation_detector,
            level=ComponentLevel.LEVEL_4_MANIPULATION,
            name="LunaManipulationDetector"
        )

        # =================================================================
        # Level 2: Validator (depends on Level 4)
        # =================================================================

        self._components['validator'] = LazyComponent(
            factory=self._create_validator,
            level=ComponentLevel.LEVEL_2_VALIDATOR,
            name="LunaValidator",
            dependencies=['phi_calculator', 'semantic_engine', 'manipulation_detector']
        )

        # =================================================================
        # Level 6: Autonomous Decision
        # =================================================================

        self._components['autonomous_decision'] = LazyComponent(
            factory=self._create_autonomous_decision,
            level=ComponentLevel.LEVEL_6_AUTONOMOUS,
            name="LunaAutonomousDecision",
            dependencies=['phi_calculator', 'memory_manager', 'emotional_processor']
        )

        # =================================================================
        # Level 7: Self Improvement
        # =================================================================

        self._components['self_improvement'] = LazyComponent(
            factory=self._create_self_improvement,
            level=ComponentLevel.LEVEL_7_IMPROVEMENT,
            name="LunaSelfImprovement",
            dependencies=['phi_calculator', 'memory_manager', 'co_evolution_engine']
        )

        # =================================================================
        # Level 9: Multimodal Interface
        # =================================================================

        self._components['multimodal_interface'] = LazyComponent(
            factory=self._create_multimodal_interface,
            level=ComponentLevel.LEVEL_9_MULTIMODAL,
            name="LunaMultimodalInterface",
            dependencies=['phi_calculator', 'memory_manager', 'emotional_processor']
        )

        # =================================================================
        # Level 8: Systemic Integration (depends on all)
        # =================================================================

        self._components['systemic_integration'] = LazyComponent(
            factory=self._create_systemic_integration,
            level=ComponentLevel.LEVEL_8_SYSTEMIC,
            name="LunaSystemicIntegration",
            dependencies=[
                'orchestrator', 'validator', 'predictive_core',
                'manipulation_detector', 'autonomous_decision',
                'self_improvement'
            ]
        )

    # =========================================================================
    # FACTORY METHODS
    # =========================================================================

    def _create_phi_calculator(self):
        """Create PhiCalculator instance."""
        from .phi_calculator import PhiCalculator
        self._phi_calculator = PhiCalculator(json_manager=self._json_manager)
        return self._phi_calculator

    def _create_memory_manager(self):
        """Create MemoryManager instance."""
        from .memory_core import MemoryManager
        self._memory_manager = MemoryManager(json_manager=self._json_manager)
        return self._memory_manager

    def _create_emotional_processor(self):
        """Create EmotionalProcessor instance."""
        from .emotional_processor import EmotionalProcessor
        self._emotional_processor = EmotionalProcessor()
        return self._emotional_processor

    def _create_semantic_engine(self):
        """Create SemanticValidator instance."""
        from .semantic_engine import SemanticValidator
        self._semantic_engine = SemanticValidator()
        return self._semantic_engine

    def _create_co_evolution_engine(self):
        """Create CoEvolutionEngine instance."""
        from .co_evolution_engine import CoEvolutionEngine
        self._co_evolution_engine = CoEvolutionEngine(json_manager=self._json_manager)
        return self._co_evolution_engine

    def _create_consciousness_engine(self):
        """Create FractalPhiConsciousnessEngine instance."""
        from .fractal_consciousness import FractalPhiConsciousnessEngine
        phi_calc = self._phi_calculator or self._components['phi_calculator'].instance
        self._consciousness_engine = FractalPhiConsciousnessEngine(
            json_manager=self._json_manager,
            phi_calculator=phi_calc
        )
        return self._consciousness_engine

    def _create_orchestrator(self):
        """Create LunaOrchestrator instance."""
        from .luna_orchestrator import LunaOrchestrator
        return LunaOrchestrator(
            json_manager=self._json_manager,
            phi_calculator=self._phi_calculator or self._components['phi_calculator'].instance,
            consciousness_engine=self._consciousness_engine or self._components['consciousness_engine'].instance,
            memory_manager=self._memory_manager or self._components['memory_manager'].instance
        )

    def _create_predictive_core(self):
        """Create LunaPredictiveCore instance."""
        from .predictive_core import LunaPredictiveCore
        return LunaPredictiveCore(
            memory_manager=self._memory_manager or self._components['memory_manager'].instance,
            json_manager=self._json_manager
        )

    def _create_manipulation_detector(self):
        """Create LunaManipulationDetector instance."""
        from .manipulation_detector import LunaManipulationDetector
        return LunaManipulationDetector(json_manager=self._json_manager)

    def _create_validator(self):
        """Create LunaValidator instance."""
        from .luna_validator import LunaValidator
        return LunaValidator(
            phi_calculator=self._phi_calculator or self._components['phi_calculator'].instance,
            semantic_validator=self._semantic_engine or self._components['semantic_engine'].instance,
            manipulation_detector=self._components['manipulation_detector'].instance
        )

    def _create_autonomous_decision(self):
        """Create LunaAutonomousDecision instance."""
        from .autonomous_decision import LunaAutonomousDecision
        return LunaAutonomousDecision(
            phi_calculator=self._phi_calculator or self._components['phi_calculator'].instance,
            memory_core=self._memory_manager or self._components['memory_manager'].instance,
            emotional_processor=self._emotional_processor or self._components['emotional_processor'].instance,
            co_evolution=self._co_evolution_engine or self._components['co_evolution_engine'].instance,
            semantic_engine=self._semantic_engine or self._components['semantic_engine'].instance
        )

    def _create_self_improvement(self):
        """Create LunaSelfImprovement instance."""
        from .self_improvement import LunaSelfImprovement
        return LunaSelfImprovement(
            phi_calculator=self._phi_calculator or self._components['phi_calculator'].instance,
            memory_core=self._memory_manager or self._components['memory_manager'].instance,
            emotional_processor=self._emotional_processor or self._components['emotional_processor'].instance,
            co_evolution=self._co_evolution_engine or self._components['co_evolution_engine'].instance,
            semantic_engine=self._semantic_engine or self._components['semantic_engine'].instance
        )

    def _create_multimodal_interface(self):
        """Create LunaMultimodalInterface instance."""
        from .multimodal_interface import LunaMultimodalInterface
        return LunaMultimodalInterface(
            phi_calculator=self._phi_calculator or self._components['phi_calculator'].instance,
            memory_core=self._memory_manager or self._components['memory_manager'].instance,
            emotional_processor=self._emotional_processor or self._components['emotional_processor'].instance,
            co_evolution=self._co_evolution_engine or self._components['co_evolution_engine'].instance,
            semantic_engine=self._semantic_engine or self._components['semantic_engine'].instance
        )

    def _create_systemic_integration(self):
        """Create LunaSystemicIntegration instance."""
        from .systemic_integration import LunaSystemicIntegration, SystemComponent

        # Build components dictionary
        components = {}
        if self._phi_calculator:
            components[SystemComponent.PHI_CALCULATOR] = self._phi_calculator
        if self._memory_manager:
            components[SystemComponent.MEMORY_CORE] = self._memory_manager
        if self._emotional_processor:
            components[SystemComponent.EMOTIONAL_PROCESSOR] = self._emotional_processor
        if self._semantic_engine:
            components[SystemComponent.SEMANTIC_ENGINE] = self._semantic_engine
        if self._co_evolution_engine:
            components[SystemComponent.CO_EVOLUTION] = self._co_evolution_engine
        if self._consciousness_engine:
            components[SystemComponent.FRACTAL_CONSCIOUSNESS] = self._consciousness_engine

        # Add Update01 components
        if self._components['orchestrator'].is_initialized:
            components[SystemComponent.ORCHESTRATOR] = self._components['orchestrator'].instance
        if self._components['manipulation_detector'].is_initialized:
            components[SystemComponent.MANIPULATION_DETECTOR] = self._components['manipulation_detector'].instance
        if self._components['validator'].is_initialized:
            components[SystemComponent.VALIDATOR] = self._components['validator'].instance
        if self._components['predictive_core'].is_initialized:
            components[SystemComponent.PREDICTIVE_CORE] = self._components['predictive_core'].instance
        if self._components['autonomous_decision'].is_initialized:
            components[SystemComponent.AUTONOMOUS_DECISION] = self._components['autonomous_decision'].instance
        if self._components['self_improvement'].is_initialized:
            components[SystemComponent.SELF_IMPROVEMENT] = self._components['self_improvement'].instance

        return LunaSystemicIntegration(components=components)

    # =========================================================================
    # COMPONENT ACCESS PROPERTIES
    # =========================================================================

    @property
    def phi_calculator(self):
        """Get PhiCalculator instance."""
        return self._components['phi_calculator'].instance

    @property
    def memory_manager(self):
        """Get MemoryManager instance."""
        return self._components['memory_manager'].instance

    @property
    def emotional_processor(self):
        """Get EmotionalProcessor instance."""
        return self._components['emotional_processor'].instance

    @property
    def semantic_engine(self):
        """Get SemanticValidator instance."""
        return self._components['semantic_engine'].instance

    @property
    def co_evolution_engine(self):
        """Get CoEvolutionEngine instance."""
        return self._components['co_evolution_engine'].instance

    @property
    def consciousness_engine(self):
        """Get FractalPhiConsciousnessEngine instance."""
        return self._components['consciousness_engine'].instance

    @property
    def orchestrator(self):
        """Get LunaOrchestrator instance (Level 1)."""
        return self._components['orchestrator'].instance

    @property
    def validator(self):
        """Get LunaValidator instance (Level 2)."""
        return self._components['validator'].instance

    @property
    def predictive_core(self):
        """Get LunaPredictiveCore instance (Level 3)."""
        return self._components['predictive_core'].instance

    @property
    def manipulation_detector(self):
        """Get LunaManipulationDetector instance (Level 4)."""
        return self._components['manipulation_detector'].instance

    @property
    def autonomous_decision(self):
        """Get LunaAutonomousDecision instance (Level 6)."""
        return self._components['autonomous_decision'].instance

    @property
    def self_improvement(self):
        """Get LunaSelfImprovement instance (Level 7)."""
        return self._components['self_improvement'].instance

    @property
    def systemic_integration(self):
        """Get LunaSystemicIntegration instance (Level 8)."""
        return self._components['systemic_integration'].instance

    @property
    def multimodal_interface(self):
        """Get LunaMultimodalInterface instance (Level 9)."""
        return self._components['multimodal_interface'].instance

    # =========================================================================
    # PURE MEMORY ACCESS
    # =========================================================================

    @property
    def pure_memory(self):
        """
        Get PureMemoryCore instance (3-level memory architecture).

        Pure Memory provides:
        - Level 1 (Buffer): Redis cache with <1ms latency
        - Level 2 (Fractal): JSON storage with <10ms latency
        - Level 3 (Archive): Encrypted permanent storage with <100ms latency

        Returns:
            PureMemoryCore instance or None if not initialized
        """
        if self._pure_memory is None:
            self._initialize_pure_memory()
        return self._pure_memory

    def _initialize_pure_memory(self) -> None:
        """Initialize Pure Memory system."""
        try:
            from .pure_memory import PureMemoryCore

            self._pure_memory = PureMemoryCore(
                base_path=self._memory_path,
                redis_url=self._redis_url,
                master_key_hex=self._master_key_hex
            )
            logger.info(f"PureMemoryCore initialized at {self._memory_path}")
        except Exception as e:
            logger.error(f"Failed to initialize PureMemoryCore: {e}")
            self._pure_memory = None

    def configure_pure_memory(
        self,
        redis_url: Optional[str] = None,
        master_key_hex: Optional[str] = None
    ) -> None:
        """
        Configure Pure Memory settings before initialization.

        Args:
            redis_url: Redis URL for buffer layer (e.g., "redis://localhost:6379")
            master_key_hex: Hex-encoded master key for archive encryption
        """
        self._redis_url = redis_url
        self._master_key_hex = master_key_hex

        # Reinitialize if already created
        if self._pure_memory is not None:
            self._pure_memory = None
            self._initialize_pure_memory()

    async def store_memory(
        self,
        content: str,
        memory_type: str = "leaf",
        emotional_tone: str = "neutral",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Store a memory in the Pure Memory system.

        Convenience method for storing memories with automatic layer selection.

        Args:
            content: Memory content
            memory_type: Type (root/branch/leaf/seed)
            emotional_tone: Emotional context
            metadata: Optional metadata

        Returns:
            Memory ID or None if failed
        """
        if self._pure_memory is None:
            self._initialize_pure_memory()

        if self._pure_memory is None:
            logger.error("PureMemoryCore not available")
            return None

        try:
            from .pure_memory import MemoryExperience, MemoryType, EmotionalTone

            type_map = {
                "root": MemoryType.ROOT,
                "branch": MemoryType.BRANCH,
                "leaf": MemoryType.LEAF,
                "seed": MemoryType.SEED,
            }

            tone_map = {
                "neutral": EmotionalTone.NEUTRAL,
                "positive": EmotionalTone.JOY,
                "negative": EmotionalTone.CONCERN,
                "curious": EmotionalTone.CURIOSITY,
                "contemplative": EmotionalTone.CALM,
                "joy": EmotionalTone.JOY,
                "sadness": EmotionalTone.SADNESS,
                "love": EmotionalTone.LOVE,
                "gratitude": EmotionalTone.GRATITUDE,
                "compassion": EmotionalTone.COMPASSION,
            }

            memory = MemoryExperience(
                content=content,
                memory_type=type_map.get(memory_type, MemoryType.LEAF),
                emotional_context=tone_map.get(emotional_tone, EmotionalTone.NEUTRAL),
                metadata=metadata or {}
            )

            return await self._pure_memory.store(memory)
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return None

    async def recall_memories(
        self,
        query: str,
        limit: int = 10,
        include_archive: bool = False
    ) -> List[Any]:
        """
        Search for memories in the Pure Memory system.

        Args:
            query: Search query
            limit: Maximum results
            include_archive: Whether to search archive layer

        Returns:
            List of matching memories
        """
        if self._pure_memory is None:
            self._initialize_pure_memory()

        if self._pure_memory is None:
            logger.error("PureMemoryCore not available")
            return []

        try:
            return await self._pure_memory.search(
                query=query,
                limit=limit,
                include_archive=include_archive
            )
        except Exception as e:
            logger.error(f"Failed to recall memories: {e}")
            return []

    async def consolidate_memories(self, force: bool = False) -> Optional[Dict[str, Any]]:
        """
        Run memory consolidation (dream-like processing).

        Args:
            force: Force consolidation even outside scheduled time

        Returns:
            Consolidation report or None if failed
        """
        if self._pure_memory is None:
            self._initialize_pure_memory()

        if self._pure_memory is None:
            logger.error("PureMemoryCore not available")
            return None

        try:
            report = await self._pure_memory.consolidate(force=force)
            return {
                "memories_processed": report.memories_processed,
                "memories_promoted": report.memories_promoted,
                "patterns_extracted": report.patterns_extracted,
                "phase": report.phase.value if hasattr(report.phase, 'value') else str(report.phase)
            }
        except Exception as e:
            logger.error(f"Failed to consolidate memories: {e}")
            return None

    def get_pure_memory_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get Pure Memory statistics.

        Returns:
            Statistics dictionary or None if not available
        """
        if self._pure_memory is None:
            return None

        try:
            stats = self._pure_memory.get_stats()
            return {
                "buffer_count": stats.buffer_count,
                "fractal_count": stats.fractal_count,
                "archive_count": stats.archive_count,
                "root_count": stats.root_count,
                "branch_count": stats.branch_count,
                "leaf_count": stats.leaf_count,
                "seed_count": stats.seed_count,
                "average_phi_resonance": stats.average_phi_resonance,
                "total_size_bytes": stats.total_size_bytes
            }
        except Exception as e:
            logger.error(f"Failed to get Pure Memory stats: {e}")
            return None

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    async def initialize(self, components: Optional[List[str]] = None) -> FacadeStatus:
        """
        Initialize all or specified components in the correct order.

        Components are initialized in three phases:
        - Phase 1: Components with no dependencies (parallel)
        - Phase 2: Components depending on Phase 1
        - Phase 3: SystemicIntegration (requires all others)

        Args:
            components: Optional list of component names to initialize.
                       If None, initializes all components.

        Returns:
            FacadeStatus with initialization results
        """
        start_time = datetime.now(timezone.utc)
        logger.info("Starting Luna Core Facade initialization...")

        try:
            # Determine which components to initialize
            if components is None:
                components_to_init = list(self._components.keys())
            else:
                components_to_init = components

            # Phase 1: Foundation components (can be parallel)
            phase1_components = [
                'phi_calculator', 'memory_manager', 'emotional_processor',
                'semantic_engine', 'co_evolution_engine'
            ]
            phase1_to_init = [c for c in phase1_components if c in components_to_init]

            logger.info(f"Phase 1: Initializing foundation components: {phase1_to_init}")
            for name in phase1_to_init:
                _ = self._components[name].instance

            # Phase 2: Components with Phase 1 dependencies
            phase2_components = [
                'consciousness_engine', 'orchestrator', 'predictive_core',
                'manipulation_detector', 'autonomous_decision',
                'self_improvement', 'multimodal_interface'
            ]
            phase2_to_init = [c for c in phase2_components if c in components_to_init]

            logger.info(f"Phase 2: Initializing dependent components: {phase2_to_init}")

            # Validator depends on manipulation_detector
            if 'validator' in components_to_init:
                if 'manipulation_detector' in phase2_to_init:
                    phase2_to_init.remove('manipulation_detector')
                    _ = self._components['manipulation_detector'].instance
                phase2_to_init.append('validator')

            for name in phase2_to_init:
                _ = self._components[name].instance

            # Phase 3: SystemicIntegration (requires all others)
            if 'systemic_integration' in components_to_init:
                logger.info("Phase 3: Initializing systemic integration")
                _ = self._components['systemic_integration'].instance

            # Calculate initialization time
            end_time = datetime.now(timezone.utc)
            self._initialization_time_ms = (end_time - start_time).total_seconds() * 1000
            self._initialized = True

            logger.info(f"Luna Core Facade initialized in {self._initialization_time_ms:.2f}ms")

        except Exception as e:
            logger.error(f"Facade initialization failed: {e}")
            return FacadeStatus(
                initialized=False,
                healthy=False,
                last_error=str(e),
                initialization_time_ms=self._initialization_time_ms
            )

        return self.get_status()

    # =========================================================================
    # STATUS AND HEALTH
    # =========================================================================

    def get_status(self) -> FacadeStatus:
        """
        Get comprehensive status of all components.

        Returns:
            FacadeStatus with component statuses and overall health
        """
        component_statuses = {}
        all_healthy = True

        for name, component in self._components.items():
            status = component.get_status()
            component_statuses[name] = status
            if not status.healthy:
                all_healthy = False

        # Add Pure Memory status
        if self._pure_memory is not None:
            try:
                pm_stats = self._pure_memory.get_stats()
                component_statuses['pure_memory'] = ComponentStatus(
                    name="PureMemoryCore",
                    level=ComponentLevel.LEVEL_1_ORCHESTRATOR,  # Foundation level
                    initialized=True,
                    healthy=True,
                    last_activity=datetime.now(timezone.utc),
                    metrics={
                        "buffer_count": pm_stats.buffer_count,
                        "fractal_count": pm_stats.fractal_count,
                        "archive_count": pm_stats.archive_count,
                        "total_memories": pm_stats.buffer_count + pm_stats.fractal_count + pm_stats.archive_count
                    }
                )
            except Exception as e:
                component_statuses['pure_memory'] = ComponentStatus(
                    name="PureMemoryCore",
                    level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
                    initialized=True,
                    healthy=False,
                    last_error=str(e)
                )
                all_healthy = False
        else:
            component_statuses['pure_memory'] = ComponentStatus(
                name="PureMemoryCore",
                level=ComponentLevel.LEVEL_1_ORCHESTRATOR,
                initialized=False,
                healthy=True  # Not initialized is not unhealthy
            )

        # Calculate phi alignment
        phi_alignment = 1.0
        if self._phi_calculator:
            try:
                phi_alignment = self._phi_calculator.get_current_phi() / 1.618033988749895
            except Exception:
                phi_alignment = 1.0

        return FacadeStatus(
            initialized=self._initialized,
            healthy=all_healthy,
            components=component_statuses,
            initialization_time_ms=self._initialization_time_ms,
            phi_alignment=phi_alignment,
            timestamp=datetime.now(timezone.utc)
        )

    def get_component_status(self, component_name: str) -> Optional[ComponentStatus]:
        """
        Get status of a specific component.

        Args:
            component_name: Name of the component

        Returns:
            ComponentStatus or None if component not found
        """
        if component_name in self._components:
            return self._components[component_name].get_status()
        return None

    def is_initialized(self) -> bool:
        """Check if facade is initialized."""
        return self._initialized

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        return all(
            c.get_status().healthy
            for c in self._components.values()
            if c.is_initialized
        )

    # =========================================================================
    # HIGH-LEVEL OPERATIONS
    # =========================================================================

    async def process_interaction(
        self,
        user_input: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user interaction through the full Luna pipeline.

        This method orchestrates the flow through:
        1. Orchestrator (Level 1) - Initial analysis
        2. Validator (Level 2) - Validation and safety checks
        3. Predictive Core (Level 3) - Anticipation
        4. Multimodal Interface (Level 9) - Response formatting

        Args:
            user_input: The user's input text
            metadata: Optional metadata about the interaction

        Returns:
            Processed result with response and analysis
        """
        if not self._initialized:
            await self.initialize()

        result = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'input': user_input,
            'metadata': metadata or {},
            'analysis': {},
            'response': None,
            'phi_alignment': 1.0
        }

        try:
            # Level 1: Orchestration
            if self._components['orchestrator'].is_initialized:
                orchestration_result = await self.orchestrator.process_user_input(
                    user_input, metadata
                )
                result['analysis']['orchestration'] = orchestration_result

                # If orchestrator handled it autonomously, return
                if orchestration_result.get('luna_handled'):
                    result['response'] = orchestration_result.get('response')
                    return result

            # Level 2: Validation
            if self._components['validator'].is_initialized:
                validation_context = {
                    'user_input': user_input,
                    **result['analysis'].get('orchestration', {})
                }
                # Validator validates LLM responses, not user input
                # Here we just note it's available
                result['analysis']['validation'] = {'available': True}

            # Level 3: Predictive analysis
            if self._components['predictive_core'].is_initialized:
                predictions = await self.predictive_core.generate_predictions({
                    'input': user_input,
                    **result['analysis']
                })
                result['analysis']['predictions'] = predictions

            # Level 9: Format response
            if self._components['multimodal_interface'].is_initialized:
                # Create user profile if needed
                user_id = (metadata or {}).get('user_id', 'default')
                response = await self.multimodal_interface.process_input(
                    user_id=user_id,
                    input_data=user_input
                )
                result['response'] = self.multimodal_interface.render_message(response)
            else:
                result['response'] = "Luna processed your request."

            # Calculate phi alignment
            if self._phi_calculator:
                result['phi_alignment'] = self._phi_calculator.get_current_phi() / 1.618033988749895

        except Exception as e:
            logger.error(f"Interaction processing error: {e}")
            result['error'] = str(e)
            result['response'] = "I encountered an issue processing your request."

        return result

    async def validate_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate an LLM response before sending to user.

        Args:
            response: The LLM-generated response
            context: Context including user input and analysis

        Returns:
            Validation result with approved/corrected/rejected status
        """
        if not self._components['validator'].is_initialized:
            _ = self.validator  # Initialize on demand

        return await self.validator.validate_response(response, context)

    async def get_predictions(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate predictions based on context.

        Args:
            context: Current interaction context

        Returns:
            Predictions for next actions and needs
        """
        if not self._components['predictive_core'].is_initialized:
            _ = self.predictive_core  # Initialize on demand

        return await self.predictive_core.generate_predictions(context)

    async def check_manipulation(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Check text for manipulation attempts.

        Args:
            text: Text to analyze

        Returns:
            Manipulation detection results
        """
        if not self._components['manipulation_detector'].is_initialized:
            _ = self.manipulation_detector  # Initialize on demand

        return self.manipulation_detector.detect_manipulation_attempts(text)

    # =========================================================================
    # CLEANUP
    # =========================================================================

    async def shutdown(self) -> None:
        """
        Gracefully shutdown all components.

        Shuts down in reverse order of initialization (Level 9 -> Level 1).
        """
        logger.info("Shutting down Luna Core Facade...")

        # Shutdown systemic integration first
        if self._components['systemic_integration'].is_initialized:
            integration = self._components['systemic_integration'].instance
            if hasattr(integration, 'shutdown_system'):
                await integration.shutdown_system()

        # Clear all instances
        for component in self._components.values():
            component._instance = None
            component._initialized = False

        # Clear shared instances
        self._phi_calculator = None
        self._memory_manager = None
        self._consciousness_engine = None
        self._emotional_processor = None
        self._semantic_engine = None
        self._co_evolution_engine = None

        self._initialized = False
        logger.info("Luna Core Facade shutdown complete")


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_luna_facade(
    json_manager: Any,
    config: Optional[Dict[str, Any]] = None,
    memory_path: Optional[str] = None,
    auto_initialize: bool = False
) -> LunaCoreFacade:
    """
    Factory function to create a LunaCoreFacade instance.

    Args:
        json_manager: JSON manager for persistence
        config: Optional configuration dictionary
        memory_path: Optional path for memory storage
        auto_initialize: If True, initialize synchronously (blocking)

    Returns:
        Configured LunaCoreFacade instance

    Example:
        facade = create_luna_facade(json_manager, auto_initialize=True)
    """
    facade = LunaCoreFacade(
        json_manager=json_manager,
        config=config,
        memory_path=memory_path
    )

    if auto_initialize:
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(facade.initialize())
        else:
            loop.run_until_complete(facade.initialize())

    return facade


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'LunaCoreFacade',
    'LazyComponent',
    'ComponentLevel',
    'InitializationPhase',
    'ComponentStatus',
    'FacadeStatus',
    'create_luna_facade',
]
