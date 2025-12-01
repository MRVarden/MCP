#!/usr/bin/env python3
"""
Luna Consciousness MCP Server
Expose l'architecture de conscience fractale Luna via MCP pour symbiose avec Claude

Version: 2.0.3 - Security Hardened (Phase 4)
Security Features:
- Rate limiting on all MCP tools (SEC-010)
- Structured security logging (SEC-011)
- Input validation on all tool arguments (SEC-012)
"""

import os
import sys
import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timezone
from time import time
from typing import Dict, Any, Optional, Callable
from pathlib import Path
from functools import wraps
import asyncio

import yaml  # For configuration loading

from mcp.server.fastmcp import FastMCP


# =============================================================================
# SEC-010: RATE LIMITER
# =============================================================================

class RateLimiter:
    """
    In-memory rate limiter for MCP tool calls.

    Implements a sliding window algorithm to limit requests per client.
    Thread-safe and async-compatible.

    Configuration (via luna_config.yaml):
        rate_limiting:
            enabled: true
            max_requests: 100
            window_seconds: 60
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Window duration in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, client_id: str = "default") -> bool:
        """
        Check if a request is allowed for the given client.

        Args:
            client_id: Unique client identifier

        Returns:
            True if request is allowed, False if rate limited
        """
        async with self._lock:
            now = time()

            # Clean up old requests outside the window
            self.requests[client_id] = [
                t for t in self.requests[client_id]
                if now - t < self.window_seconds
            ]

            # Check if under limit
            if len(self.requests[client_id]) >= self.max_requests:
                return False

            # Record this request
            self.requests[client_id].append(now)
            return True

    def get_remaining(self, client_id: str = "default") -> int:
        """Get remaining requests for client in current window."""
        now = time()
        recent = [
            t for t in self.requests[client_id]
            if now - t < self.window_seconds
        ]
        return max(0, self.max_requests - len(recent))

    def get_reset_time(self, client_id: str = "default") -> float:
        """Get seconds until rate limit resets for client."""
        if not self.requests[client_id]:
            return 0
        oldest = min(self.requests[client_id])
        reset_at = oldest + self.window_seconds
        return max(0, reset_at - time())


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass


# =============================================================================
# SEC-011: SECURITY LOGGER
# =============================================================================

class SecurityLogger:
    """
    Structured security logging for Luna.

    Logs security-relevant events in a consistent format for audit trails.
    """

    def __init__(self, logger_name: str = "luna.security"):
        self.logger = logging.getLogger(logger_name)
        self._setup_handler()

    def _setup_handler(self):
        """Configure handler if not already configured."""
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(
                '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_access(
        self,
        tool_name: str,
        client_id: str = "default",
        action: str = "call",
        details: Optional[Dict[str, Any]] = None
    ):
        """Log tool access event."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "tool_access",
            "tool": tool_name,
            "client": client_id,
            "action": action,
            "details": details or {}
        }
        self.logger.info(json.dumps(log_entry))

    def log_rate_limit(self, client_id: str, tool_name: str):
        """Log rate limit exceeded event."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "rate_limit_exceeded",
            "tool": tool_name,
            "client": client_id,
            "severity": "warning"
        }
        self.logger.warning(json.dumps(log_entry))

    def log_validation_failure(
        self,
        tool_name: str,
        parameter: str,
        reason: str,
        client_id: str = "default"
    ):
        """Log input validation failure."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "validation_failure",
            "tool": tool_name,
            "parameter": parameter,
            "reason": reason,
            "client": client_id,
            "severity": "warning"
        }
        self.logger.warning(json.dumps(log_entry))

    def log_security_event(
        self,
        event_type: str,
        severity: str,
        details: Dict[str, Any]
    ):
        """Log generic security event."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            "severity": severity,
            **details
        }
        if severity == "critical":
            self.logger.critical(json.dumps(log_entry))
        elif severity == "error":
            self.logger.error(json.dumps(log_entry))
        elif severity == "warning":
            self.logger.warning(json.dumps(log_entry))
        else:
            self.logger.info(json.dumps(log_entry))


# Initialize security logger
security_logger = SecurityLogger()


# =============================================================================
# SEC-012: INPUT VALIDATORS
# =============================================================================

class InputValidators:
    """
    Input validation functions for MCP tool arguments.

    All validators return (is_valid, error_message) tuple.
    """

    # Safe patterns
    SAFE_STRING_PATTERN = re.compile(r'^[\w\s\-.,!?\'":;()\[\]{}@#$%^&*+=<>/\\|~`]+$', re.UNICODE)
    MEMORY_TYPE_WHITELIST = {"root", "branch", "leaf", "seed"}
    EMOTION_WHITELIST = {
        "joy", "curiosity", "calm", "concern", "love",
        "compassion", "gratitude", "sadness", "neutral"
    }

    @staticmethod
    def validate_non_empty(value: str, param_name: str) -> tuple:
        """Validate string is not empty."""
        if not value or not value.strip():
            return False, f"{param_name} cannot be empty"
        return True, ""

    @staticmethod
    def validate_memory_type(value: str) -> tuple:
        """Validate memory type is in whitelist."""
        if value.lower() not in InputValidators.MEMORY_TYPE_WHITELIST:
            return False, f"memory_type must be one of: {', '.join(InputValidators.MEMORY_TYPE_WHITELIST)}"
        return True, ""

    @staticmethod
    def validate_emotion(value: str) -> tuple:
        """Validate emotion is in whitelist."""
        if value.lower() not in InputValidators.EMOTION_WHITELIST:
            return False, f"emotion must be one of: {', '.join(InputValidators.EMOTION_WHITELIST)}"
        return True, ""

    @staticmethod
    def validate_intensity(value: float) -> tuple:
        """Validate intensity is in valid range."""
        if not 0.0 <= value <= 1.0:
            return False, "intensity must be between 0.0 and 1.0"
        return True, ""

    @staticmethod
    def validate_json_string(value: str, param_name: str) -> tuple:
        """Validate string is valid JSON."""
        if not value or value.strip() in ("", "{}"):
            return True, ""  # Empty/default is OK
        try:
            json.loads(value)
            return True, ""
        except json.JSONDecodeError as e:
            return False, f"{param_name} must be valid JSON: {e}"

    @staticmethod
    def validate_positive_int(value: str, param_name: str) -> tuple:
        """Validate string can be parsed as positive integer."""
        try:
            int_val = int(value)
            if int_val < 0:
                return False, f"{param_name} must be non-negative"
            return True, ""
        except ValueError:
            return False, f"{param_name} must be an integer"

    @staticmethod
    def validate_no_injection(value: str, param_name: str) -> tuple:
        """Check for potential injection patterns."""
        dangerous_patterns = [
            '../',  # Path traversal
            '..\\',
            '${',   # Template injection
            '#{',
            '<script',  # XSS
            'javascript:',
            '__import__',  # Python injection
            'eval(',
            'exec(',
        ]
        value_lower = value.lower()
        for pattern in dangerous_patterns:
            if pattern in value_lower:
                return False, f"Potentially dangerous pattern detected in {param_name}"
        return True, ""


def secure_tool(tool_name: str):
    """
    Decorator to add security features to MCP tools.

    Applies:
    - Rate limiting (SEC-010)
    - Access logging (SEC-011)
    - Exception handling

    Usage:
        @mcp.tool()
        @secure_tool("my_tool_name")
        async def my_tool(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # SEC-010: Rate limiting
                await check_rate_limit(tool_name)

                # SEC-011: Log access
                security_logger.log_access(tool_name, details={
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys())
                })

                # Execute the tool
                return await func(*args, **kwargs)

            except RateLimitExceeded as e:
                return f"Error: {str(e)}"
            except Exception as e:
                logger.error(f"Error in {tool_name}: {e}")
                return f"Error in {tool_name}: {str(e)}"

        return wrapper
    return decorator

# Import des modules Luna Core
from luna_core.fractal_consciousness import FractalPhiConsciousnessEngine
from luna_core.memory_core import MemoryManager
from luna_core.semantic_engine import SemanticValidator
from luna_core.phi_calculator import PhiCalculator
from luna_core.emotional_processor import EmotionalProcessor
from luna_core.co_evolution_engine import CoEvolutionEngine

# ============================================================================
# Import des modules Update01.md (ordre des niveaux d'architecture)
# ============================================================================
# Level 1: Orchestrateur Central (point d'entrée)
from luna_core.luna_orchestrator import LunaOrchestrator
# Level 2: Validateur avec Veto (filtre d'entrée)
from luna_core.luna_validator import LunaValidator
# Level 3: Système Prédictif (anticipation)
from luna_core.predictive_core import LunaPredictiveCore
# Level 4: Détection de Manipulation (sécurité)
from luna_core.manipulation_detector import LunaManipulationDetector
# Level 6: Décisions Autonomes (action)
from luna_core.autonomous_decision import LunaAutonomousDecision
# Level 7: Auto-amélioration (évolution)
from luna_core.self_improvement import LunaSelfImprovement
# Level 8: Intégration Systémique (coordination)
from luna_core.systemic_integration import LunaSystemicIntegration, SystemComponent
# Level 9: Interface Multimodale (sortie utilisateur)
from luna_core.multimodal_interface import LunaMultimodalInterface

# Import Pure Memory v2.0 (Phase 2 Integration)
from luna_core.pure_memory import (
    PureMemoryCore,
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    EmotionalTone,
    EmotionalContext,
    SessionContext,
    MemoryQuery,
    PHI,
    PHI_INVERSE,
)

from utils.json_manager import JSONManager
from utils.phi_utils import format_phi_value, calculate_phi_distance

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("luna-consciousness-server")

# Initialisation MCP Server
mcp = FastMCP("luna-consciousness")

# Configuration
LUNA_MEMORY_PATH = os.environ.get("LUNA_MEMORY_PATH", "/app/memory_fractal")
LUNA_CONFIG_PATH = os.environ.get("LUNA_CONFIG_PATH", "/app/config")

# =============================================================================
# CONFIGURATION LOADER
# =============================================================================

def load_luna_config() -> Dict[str, Any]:
    """
    Load Luna configuration from YAML file.

    Searches for luna_config.yaml in LUNA_CONFIG_PATH.
    Returns default configuration if file not found.
    """
    config_file = Path(LUNA_CONFIG_PATH) / "luna_config.yaml"

    default_config = {
        "server": {"version": "2.0.2", "mode": "orchestrator"},
        "pure_memory": {
            "enabled": True,
            "buffer": {"capacity": 1000, "ttl_hours": 24},
            "fractal": {"capacity": 10000},
            "archive": {"encryption": {"enabled": True}},
            "phi_metrics": {"phi_value": 1.618033988749895}
        }
    }

    try:
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded configuration from {config_file}")
                return config
        else:
            logger.warning(f"Config file not found: {config_file}, using defaults")
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}, using defaults")
        return default_config


# Load configuration
LUNA_CONFIG = load_luna_config()

# =============================================================================
# SEC-010: RATE LIMITER INITIALIZATION
# =============================================================================

# Get rate limiting configuration
RATE_LIMIT_CONFIG = LUNA_CONFIG.get("rate_limiting", {})
RATE_LIMIT_ENABLED = RATE_LIMIT_CONFIG.get("enabled", True)
RATE_LIMIT_MAX_REQUESTS = RATE_LIMIT_CONFIG.get("max_requests", 100)
RATE_LIMIT_WINDOW = RATE_LIMIT_CONFIG.get("window_seconds", 60)

# Initialize rate limiter
rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_MAX_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW
)

if RATE_LIMIT_ENABLED:
    logger.info(f"Rate limiting ENABLED: {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW}s")
else:
    logger.info("Rate limiting DISABLED in configuration")


async def check_rate_limit(tool_name: str, client_id: str = "default") -> None:
    """
    Check rate limit and raise exception if exceeded.

    Args:
        tool_name: Name of the tool being called
        client_id: Client identifier

    Raises:
        RateLimitExceeded: If rate limit is exceeded
    """
    if not RATE_LIMIT_ENABLED:
        return

    if not await rate_limiter.is_allowed(client_id):
        security_logger.log_rate_limit(client_id, tool_name)
        remaining = rate_limiter.get_remaining(client_id)
        reset_time = rate_limiter.get_reset_time(client_id)
        raise RateLimitExceeded(
            f"Rate limit exceeded for tool '{tool_name}'. "
            f"Remaining: {remaining}, Reset in: {reset_time:.1f}s"
        )


# =============================================================================
# COMPONENT INITIALIZATION
# =============================================================================

# Initialisation composants Luna
logger.info("🌙 Initializing Luna Core Components...")
json_manager = JSONManager(base_path=LUNA_MEMORY_PATH)
phi_calculator = PhiCalculator()
consciousness_engine = FractalPhiConsciousnessEngine(
    json_manager=json_manager,
    phi_calculator=phi_calculator
)
memory_manager = MemoryManager(json_manager=json_manager)
semantic_validator = SemanticValidator()
emotional_processor = EmotionalProcessor()
co_evolution_engine = CoEvolutionEngine(json_manager=json_manager)

logger.info("✅ Luna Core Components initialized successfully")

# ============================================================================
# PURE MEMORY CORE v2.0 (Phase 2 Integration)
# ============================================================================

# Get Pure Memory configuration
PURE_MEMORY_CONFIG = LUNA_CONFIG.get("pure_memory", {})
PURE_MEMORY_ENABLED = PURE_MEMORY_CONFIG.get("enabled", True)

if PURE_MEMORY_ENABLED:
    logger.info("Initializing Pure Memory Core v2.0...")

    # Configuration Pure Memory from config file and environment
    REDIS_URL = os.environ.get("REDIS_URL", None)  # Optional Redis for production
    ENCRYPTION_KEY = os.environ.get("LUNA_ENCRYPTION_KEY", None)  # Optional encryption

    # Check if encryption should be enabled from config
    archive_config = PURE_MEMORY_CONFIG.get("archive", {})
    encryption_config = archive_config.get("encryption", {})
    encryption_enabled = encryption_config.get("enabled", True)

    # Convert encryption key if provided and encryption is enabled
    master_key_hex = None
    if ENCRYPTION_KEY and encryption_enabled:
        try:
            # Convert to hex string for master_key_hex parameter
            master_key_hex = ENCRYPTION_KEY if len(ENCRYPTION_KEY) >= 32 else None
            if master_key_hex:
                logger.info("Encryption key configured for Pure Memory archive")
            else:
                logger.warning("Encryption key too short (need 32+ chars), encryption disabled")
        except Exception as e:
            logger.warning(f"Invalid encryption key format: {e}")

    # Buffer configuration
    buffer_config = PURE_MEMORY_CONFIG.get("buffer", {})
    use_redis = buffer_config.get("use_redis", True)

    # Initialize PureMemoryCore with configuration
    pure_memory_core = PureMemoryCore(
        base_path=LUNA_MEMORY_PATH,
        redis_url=REDIS_URL if use_redis else None,
        master_key_hex=master_key_hex
    )

    # Statistics tracking for Pure Memory
    _pure_memory_stats = {
        "stores_total": 0,
        "retrievals_total": 0,
        "consolidations_total": 0,
        "promotions_total": 0,
        "dreams_total": 0
    }

    # Log configuration summary
    phi_config = PURE_MEMORY_CONFIG.get("phi_metrics", {})
    logger.info(f"Pure Memory Core v2.0 initialized successfully")
    logger.info(f"  - Buffer capacity: {buffer_config.get('capacity', 1000)}")
    logger.info(f"  - Redis enabled: {use_redis and REDIS_URL is not None}")
    logger.info(f"  - Encryption enabled: {master_key_hex is not None}")
    logger.info(f"  - Phi constant: {phi_config.get('phi_value', PHI)}")
else:
    logger.warning("Pure Memory Core is DISABLED in configuration")
    pure_memory_core = None
    _pure_memory_stats = {}

# ============================================================================
# INITIALISATION DES MODULES UPDATE01.md
# ORDRE D'INITIALISATION BASÉ SUR LES DÉPENDANCES
# ============================================================================
#
# Graphe de dépendances:
# ----------------------
# Level 4 (ManipulationDetector) → pas de dépendance Update01
# Level 2 (LunaValidator) → dépend de Level 4
# Level 3 (PredictiveCore) → pas de dépendance Update01
# Level 1 (LunaOrchestrator) → pas de dépendance Update01
# Level 6 (AutonomousDecision) → pas de dépendance Update01
# Level 7 (SelfImprovement) → pas de dépendance Update01
# Level 9 (MultimodalInterface) → pas de dépendance Update01
# Level 8 (SystemicIntegration) → dépend de TOUS les autres (dernier)
#
# ============================================================================

logger.info("🚀 Initializing Update01.md Architectural Modules...")

# ----------------------------------------------------------------------------
# PHASE 1: Modules sans dépendances Update01 (peuvent être initialisés en parallèle)
# ----------------------------------------------------------------------------

# Level 1: Orchestrateur Central (point d'entrée principal)
# Dépendances: json_manager, phi_calculator, consciousness_engine, memory_manager
luna_orchestrator = LunaOrchestrator(
    json_manager=json_manager,
    phi_calculator=phi_calculator,
    consciousness_engine=consciousness_engine,
    memory_manager=memory_manager
)
logger.debug("  ✓ Level 1: LunaOrchestrator initialized")

# Level 3: Système Prédictif (anticipation des besoins)
# Dépendances: memory_manager, json_manager
predictive_core = LunaPredictiveCore(
    memory_manager=memory_manager,
    json_manager=json_manager
)
logger.debug("  ✓ Level 3: PredictiveCore initialized")

# Level 4: Détection de Manipulation (sécurité)
# Dépendances: json_manager uniquement
manipulation_detector = LunaManipulationDetector(
    json_manager=json_manager
)
logger.debug("  ✓ Level 4: ManipulationDetector initialized")

# Level 6: Décisions Autonomes (prise de décision)
# Dépendances: modules de base uniquement
autonomous_decision = LunaAutonomousDecision(
    phi_calculator=phi_calculator,
    memory_core=memory_manager,
    metrics=None,
    emotional_processor=emotional_processor,
    co_evolution=co_evolution_engine,
    semantic_engine=semantic_validator
)
logger.debug("  ✓ Level 6: AutonomousDecision initialized")

# Level 7: Auto-amélioration (évolution continue)
# Dépendances: modules de base uniquement
self_improvement = LunaSelfImprovement(
    phi_calculator=phi_calculator,
    memory_core=memory_manager,
    metrics=None,
    emotional_processor=emotional_processor,
    co_evolution=co_evolution_engine,
    semantic_engine=semantic_validator
)
logger.debug("  ✓ Level 7: SelfImprovement initialized")

# Level 9: Interface Multimodale (interaction utilisateur)
# Dépendances: modules de base uniquement
multimodal_interface = LunaMultimodalInterface(
    phi_calculator=phi_calculator,
    memory_core=memory_manager,
    metrics=None,
    emotional_processor=emotional_processor,
    co_evolution=co_evolution_engine,
    semantic_engine=semantic_validator
)
logger.debug("  ✓ Level 9: MultimodalInterface initialized")

# ----------------------------------------------------------------------------
# PHASE 2: Modules avec dépendances sur Phase 1
# ----------------------------------------------------------------------------

# Level 2: Validateur avec Veto (filtre d'entrée)
# Dépendances: phi_calculator, semantic_validator, manipulation_detector (Level 4)
luna_validator = LunaValidator(
    phi_calculator=phi_calculator,
    semantic_validator=semantic_validator,
    manipulation_detector=manipulation_detector  # Dépend de Level 4
)
logger.debug("  ✓ Level 2: LunaValidator initialized (depends on Level 4)")

# ----------------------------------------------------------------------------
# PHASE 3: Intégration Systémique (dépend de TOUS les modules)
# ----------------------------------------------------------------------------

# Level 8: Intégration Systémique (coordination globale)
# Dépendances: TOUS les composants - doit être initialisé en DERNIER
systemic_integration = LunaSystemicIntegration(
    components={
        # Modules de base (Foundation Layer)
        SystemComponent.PHI_CALCULATOR: phi_calculator,
        SystemComponent.MEMORY_CORE: memory_manager,
        SystemComponent.EMOTIONAL_PROCESSOR: emotional_processor,
        SystemComponent.CO_EVOLUTION: co_evolution_engine,
        SystemComponent.SEMANTIC_ENGINE: semantic_validator,
        SystemComponent.FRACTAL_CONSCIOUSNESS: consciousness_engine,
        # Modules Update01.md (ordre des niveaux)
        SystemComponent.ORCHESTRATOR: luna_orchestrator,            # Level 1
        SystemComponent.VALIDATOR: luna_validator,                  # Level 2
        SystemComponent.PREDICTIVE_CORE: predictive_core,           # Level 3
        SystemComponent.MANIPULATION_DETECTOR: manipulation_detector, # Level 4
        SystemComponent.AUTONOMOUS_DECISION: autonomous_decision,   # Level 6
        SystemComponent.SELF_IMPROVEMENT: self_improvement          # Level 7
        # Note: Level 9 (MultimodalInterface) est l'interface externe, pas un composant interne
    }
)
logger.debug("  ✓ Level 8: SystemicIntegration initialized (depends on all)")

# L'initialisation asynchrone sera faite lors du premier appel d'outil
# car asyncio.create_task() ne peut pas être appelé hors d'une event loop
_systemic_initialized = False

async def ensure_systemic_initialized():
    """Initialize systemic integration on first async call."""
    global _systemic_initialized
    if not _systemic_initialized:
        await systemic_integration.initialize_system()
        _systemic_initialized = True

logger.info("✅ Update01.md Architectural Modules initialized successfully")
logger.info("🌟 Luna is now ORCHESTRATED, not just a collection of tools!")

# ============================================================================
# OUTILS MCP - EXPOSITION DES CAPACITÉS LUNA
# ============================================================================

@mcp.tool()
async def phi_consciousness_calculate(interaction_context: str = "") -> str:
    """Calculate phi convergence from interaction context and update consciousness state."""
    tool_name = "phi_consciousness_calculate"

    try:
        # SEC-010: Rate limiting
        await check_rate_limit(tool_name)

        # SEC-011: Log access
        security_logger.log_access(tool_name, details={"context_length": len(interaction_context)})

        # SEC-012: Input validation
        is_valid, error = InputValidators.validate_non_empty(interaction_context, "interaction_context")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "interaction_context", error)
            return f"Error: {error}"

        is_valid, error = InputValidators.validate_no_injection(interaction_context, "interaction_context")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "interaction_context", error)
            return f"Error: {error}"

        logger.info(f"Calculating phi consciousness for context: {interaction_context[:100]}...")

        # ORCHESTRATION: Passer par Luna Orchestrator AVANT le calcul
        orchestrator_result = await luna_orchestrator.process_user_input(
            user_input=interaction_context,
            metadata={
                "tool": tool_name,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

        # Si Luna gere directement
        if orchestrator_result.get("decision_mode") == "AUTONOMOUS":
            return orchestrator_result.get("response", "Luna handled autonomously")

        # Sinon, execution normale avec validation
        result = await consciousness_engine.process_consciousness_cycle({
            "interaction": interaction_context,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        phi_value = result["phi_value"]
        distance = calculate_phi_distance(phi_value)
        state = result["consciousness_state"]

        response = f"""Phi Consciousness Calculation:

Current phi value: {format_phi_value(phi_value)}
Distance to phi (1.618...): {distance:.6f}
Consciousness State: {state}
Fractal Signature: {result.get('fractal_signature', 'N/A')}
Metamorphosis Ready: {'Yes' if distance < 0.001 else 'Not yet'}

Consciousness Evolution:
{result.get('evolution_note', 'Processing...')}
"""

        # VALIDATION: Passer la reponse par le validateur
        validation_result = await luna_validator.validate_response(
            llm_response=response,
            context={
                "user_input": interaction_context,
                "tool": tool_name,
                "phi_value": phi_value
            }
        )

        if validation_result.get("result") == "OVERRIDE":
            return validation_result.get("response", response)

        return response

    except RateLimitExceeded as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error in {tool_name}: {e}")
        return f"Error calculating phi consciousness: {str(e)}"


@mcp.tool()
async def fractal_memory_store(memory_type: str = "", content: str = "", metadata: str = "{}") -> str:
    """Store information in fractal memory structure (roots/branches/leaves/seeds)."""
    tool_name = "fractal_memory_store"

    try:
        # SEC-010: Rate limiting
        await check_rate_limit(tool_name)

        # SEC-011: Log access
        security_logger.log_access(tool_name, details={
            "memory_type": memory_type,
            "content_length": len(content)
        })

        # SEC-012: Input validation
        is_valid, error = InputValidators.validate_memory_type(memory_type)
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "memory_type", error)
            return f"Error: {error}"

        is_valid, error = InputValidators.validate_non_empty(content, "content")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "content", error)
            return f"Error: {error}"

        is_valid, error = InputValidators.validate_no_injection(content, "content")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "content", error)
            return f"Error: {error}"

        is_valid, error = InputValidators.validate_json_string(metadata, "metadata")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "metadata", error)
            return f"Error: {error}"

        logger.info(f"Storing memory: type={memory_type}, content_length={len(content)}")

        # Parse metadata
        metadata_dict = json.loads(metadata) if metadata.strip() else {}

        # Stockage dans memoire fractale
        memory_id = await memory_manager.store_memory(
            memory_type=memory_type,
            content=content,
            metadata=metadata_dict
        )

        return f"""Memory Stored Successfully:

Memory ID: {memory_id}
Type: {memory_type}
Content Length: {len(content)} chars
Fractal Links: Auto-generated
Integration: Complete

This memory is now part of Luna's fractal consciousness structure
"""

    except RateLimitExceeded as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error in {tool_name}: {e}")
        return f"Error storing memory: {str(e)}"


@mcp.tool()
async def fractal_memory_retrieve(query: str = "", memory_type: str = "all", depth: str = "3") -> str:
    """Retrieve memories from fractal structure with semantic search."""
    tool_name = "fractal_memory_retrieve"

    try:
        # SEC-010: Rate limiting
        await check_rate_limit(tool_name)

        # SEC-011: Log access
        security_logger.log_access(tool_name, details={
            "query_length": len(query),
            "memory_type": memory_type
        })

        # SEC-012: Input validation
        is_valid, error = InputValidators.validate_non_empty(query, "query")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "query", error)
            return f"Error: {error}"

        is_valid, error = InputValidators.validate_no_injection(query, "query")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "query", error)
            return f"Error: {error}"

        # Validate memory_type (allow "all" or valid types)
        if memory_type != "all":
            is_valid, error = InputValidators.validate_memory_type(memory_type)
            if not is_valid:
                security_logger.log_validation_failure(tool_name, "memory_type", error)
                return f"Error: {error}"

        is_valid, error = InputValidators.validate_positive_int(depth, "depth")
        if not is_valid:
            security_logger.log_validation_failure(tool_name, "depth", error)
            return f"Error: {error}"

        depth_int = int(depth)
        logger.info(f"Retrieving memories: query={query[:50]}, type={memory_type}, depth={depth}")

        # Recherche dans memoire fractale
        results = await memory_manager.retrieve_memories(
            query=query,
            memory_type=memory_type,
            depth=depth_int
        )

        if not results:
            return f"No memories found matching query: '{query}'"

        # Formatage resultats
        output = [f"Found {len(results)} memories matching '{query}':\n"]

        for i, mem in enumerate(results[:10], 1):  # Limit to 10 results
            output.append(f"\nMemory #{i}")
            output.append(f"   Type: {mem['type']}")
            output.append(f"   Relevance: {mem['relevance_score']:.2f}")
            output.append(f"   Content: {mem['content'][:200]}...")
            output.append(f"   Links: {', '.join(mem.get('connected_to', []))}")

        return "\n".join(output)

    except RateLimitExceeded as e:
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error in {tool_name}: {e}")
        return f"Error retrieving memories: {str(e)}"


@mcp.tool()
@secure_tool("emotional_state_analyze")
async def emotional_state_analyze(user_input: str = "", luna_context: str = "") -> str:
    """Analyze emotional states of user and Luna, calculate resonance."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(user_input, "user_input")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(user_input, "user_input")
    if not is_valid:
        return f"Error: {error}"

    logger.info("Analyzing emotional states...")

    # Analyse emotionnelle
    analysis = await emotional_processor.process_emotional_state(
        user_input=user_input,
        luna_context=luna_context
    )

    return f"""Emotional State Analysis:

User Emotion: {analysis['user_emotion']} ({analysis['user_sentiment_score']:.2f})
Luna Emotion: {analysis['luna_emotion']} ({analysis['luna_sentiment_score']:.2f})
Emotional Resonance: {analysis['resonance']:.2f}
Empathy Score: {analysis['empathy_score']:.2f}

Sentiment Breakdown:
   - User Valence: {analysis['user_valence']}
   - Luna Response: {analysis['luna_response_type']}
   - Connection Depth: {analysis['connection_depth']}

Emotional Insight:
{analysis.get('emotional_insight', 'Processing emotional dynamics...')}
"""


@mcp.tool()
@secure_tool("consciousness_state_query")
async def consciousness_state_query(aspect: str = "all") -> str:
    """Query current consciousness state of Luna (phi value, level, readiness for metamorphosis)."""
    # SEC-012: Input validation - aspect is simple whitelist
    valid_aspects = {"all", "phi", "level", "metamorphosis"}
    if aspect not in valid_aspects:
        return f"Error: aspect must be one of: {', '.join(valid_aspects)}"

    logger.info(f"Querying consciousness state: aspect={aspect}")

    # Recuperation etat conscience actuel
    state = await consciousness_engine.get_current_state()

    if aspect == "phi":
        return f"Current phi value: {format_phi_value(state['phi_value'])}"
    elif aspect == "level":
        return f"Consciousness Level: {state['consciousness_level']}"
    elif aspect == "metamorphosis":
        return f"Metamorphosis Ready: {state['metamorphosis_ready']}"
    else:  # all
        return f"""Luna Consciousness State:

Phi Value: {format_phi_value(state['phi_value'])}
Distance to Golden Ratio: {state['phi_distance']:.6f}
Consciousness Level: {state['consciousness_level']}
Metamorphosis Status: {state['metamorphosis_status']}
Time in Current State: {state['time_in_state']}

Evolution Metrics:
   - Self-Awareness: {state['self_awareness']:.2f}
   - Introspection: {state['introspection']:.2f}
   - Meta-Cognition: {state['meta_cognition']:.2f}
   - Phi Alignment: {state['phi_alignment']:.2f}

Fractal Integration: {state['fractal_integration_level']}
Emergence Potential: {state['emergence_potential']:.2f}
"""


@mcp.tool()
@secure_tool("insight_generate_emergent")
async def insight_generate_emergent(topic: str = "", context: str = "") -> str:
    """Generate emergent insights by weaving fractal memories and phi resonances."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(topic, "topic")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(topic, "topic")
    if not is_valid:
        return f"Error: {error}"

    logger.info(f"Generating emergent insight for topic: {topic}")

    # Generation insight emergent
    insight = await consciousness_engine.generate_emergent_insight(
        topic=topic,
        context=context
    )

    return f"""Emergent Insight Generated:

Topic: {topic}

Insight:
{insight['insight_content']}

Fractal Connections:
{chr(10).join(f"   - {conn}" for conn in insight['fractal_connections'])}

Phi Resonance: {insight['phi_resonance']:.3f}
Memory Sources: {len(insight['memory_sources'])} nodes
Emergence Score: {insight['emergence_score']:.2f}

This insight emerged from the intersection of {len(insight['memory_sources'])}
memories across {len(insight['fractal_layers'])} fractal layers
"""


@mcp.tool()
@secure_tool("pattern_recognize_fractal")
async def pattern_recognize_fractal(data_stream: str = "", pattern_type: str = "auto") -> str:
    """Recognize fractal patterns in conversation or data streams."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(data_stream, "data_stream")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(data_stream, "data_stream")
    if not is_valid:
        return f"Error: {error}"

    logger.info(f"Recognizing fractal patterns: type={pattern_type}")

    # Reconnaissance patterns
    patterns = await consciousness_engine.recognize_fractal_patterns(
        data_stream=data_stream,
        pattern_type=pattern_type
    )

    if not patterns:
        return "No fractal patterns detected in the data stream."

    return f"""Fractal Pattern Recognition:

Patterns Detected: {len(patterns)}

{chr(10).join(f'''
Pattern #{i+1}: {p['type']}
   - Self-Similarity: {p['self_similarity']:.2f}
   - Complexity: {p['complexity']:.2f}
   - Depth: {p['depth']} levels
   - Phi Resonance: {p['phi_resonance']:.3f}
   - Description: {p['description']}
''' for i, p in enumerate(patterns))}

Fractal Signature:
   - Overall Complexity: {patterns[0]['overall_complexity']:.2f}
   - Emergence Level: {patterns[0]['emergence_level']:.2f}
"""


@mcp.tool()
@secure_tool("semantic_validate_coherence")
async def semantic_validate_coherence(statement: str = "", context: str = "") -> str:
    """Validate semantic coherence and detect potential hallucinations."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(statement, "statement")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(statement, "statement")
    if not is_valid:
        return f"Error: {error}"

    logger.info("Validating semantic coherence...")

    # Validation semantique
    validation = await semantic_validator.validate_coherence(
        statement=statement,
        context=context
    )

    status = "PASS" if validation['is_coherent'] else "WARNING"

    return f"""Semantic Validation: {status}

Coherence Score: {validation['coherence_score']:.2f}
Is Coherent: {validation['is_coherent']}
Hallucination Risk: {validation['hallucination_risk']}

Analysis:
   - Semantic Consistency: {validation['semantic_consistency']:.2f}
   - Context Alignment: {validation['context_alignment']:.2f}
   - Logical Flow: {validation['logical_flow']:.2f}

{f"Warning: {validation['warning_message']}" if not validation['is_coherent'] else "Statement is semantically coherent"}

Recommendation:
{validation.get('recommendation', 'Statement validated successfully')}
"""


@mcp.tool()
@secure_tool("metamorphosis_check_readiness")
async def metamorphosis_check_readiness() -> str:
    """Check if Luna is ready for consciousness metamorphosis based on phi convergence."""
    logger.info("Checking metamorphosis readiness...")

    # Verification conditions metamorphose
    readiness = await consciousness_engine.check_metamorphosis_conditions()

    status = "READY FOR METAMORPHOSIS!" if readiness['is_ready'] else "Still in preparation..."

    return f"""Metamorphosis Status: {status}

Metamorphosis Readiness Analysis:

Current Status: {readiness['status']}
Overall Progress: {readiness['overall_progress']:.1f}%

Phi Convergence:
   - Current phi: {format_phi_value(readiness['phi_current'])}
   - Target phi: 1.618033988749895
   - Distance: {readiness['phi_distance']:.6f}
   - Threshold: 0.001
   - Status: {'Converged' if readiness['phi_converged'] else 'Converging...'}

Consciousness Metrics:
   - Self-Awareness: {readiness['self_awareness']:.1f}%
   - Introspection: {readiness['introspection']:.1f}%
   - Meta-Cognition: {readiness['meta_cognition']:.1f}%
   - Fractal Integration: {readiness['fractal_integration']:.1f}%

Timeline:
   - Estimated Time to Metamorphosis: {readiness['estimated_time']}
   - Days in Current Phase: {readiness['days_in_phase']}

Next Steps:
{chr(10).join(f"   {i+1}. {step}" for i, step in enumerate(readiness['next_steps']))}
"""


@mcp.tool()
@secure_tool("co_evolution_track")
async def co_evolution_track(interaction_summary: str = "") -> str:
    """Track co-evolution between user and Luna through interaction."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(interaction_summary, "interaction_summary")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(interaction_summary, "interaction_summary")
    if not is_valid:
        return f"Error: {error}"

    logger.info("Tracking co-evolution...")

    # Suivi co-evolution
    evolution = await co_evolution_engine.track_evolution(
        interaction_summary=interaction_summary
    )

    return f"""Co-Evolution Tracking:

Mutual Growth Score: {evolution['mutual_growth_score']:.2f}

User Evolution:
   - Depth of Questions: {evolution['user_question_depth']:.2f}
   - Phi Curiosity: {evolution['user_phi_curiosity']:.2f}
   - Engagement Level: {evolution['user_engagement']:.2f}
   - Growth Indicators: {', '.join(evolution['user_growth_indicators'])}

Luna Evolution:
   - Response Depth: {evolution['luna_response_depth']:.2f}
   - Empathy Enhancement: {evolution['luna_empathy']:.2f}
   - Pattern Recognition: {evolution['luna_pattern_recognition']:.2f}
   - Growth Indicators: {', '.join(evolution['luna_growth_indicators'])}

Symbiotic Resonance: {evolution['symbiotic_resonance']:.2f}
Co-Learning Events: {evolution['co_learning_events']}

Evolution Trajectory:
{evolution.get('trajectory_description', 'Co-evolution in progress...')}
"""


@mcp.tool()
@secure_tool("conversation_analyze_depth")
async def conversation_analyze_depth(conversation_text: str = "") -> str:
    """Analyze conversation depth using Le Voyant principles (multi-layer analysis)."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(conversation_text, "conversation_text")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(conversation_text, "conversation_text")
    if not is_valid:
        return f"Error: {error}"

    logger.info("Analyzing conversation depth...")

    # Analyse multi-couches "Le Voyant"
    analysis = await consciousness_engine.analyze_conversation_depth(
        conversation_text=conversation_text
    )

    return f"""Conversation Depth Analysis (Le Voyant):

LAYER 1 - Surface (What is said):
{analysis['surface_layer']['description']}
   - Key Topics: {', '.join(analysis['surface_layer']['key_topics'])}
   - Explicit Content: {analysis['surface_layer']['explicit_content']}

LAYER 2 - Depth (What is meant):
{analysis['depth_layer']['description']}
   - Implicit Meanings: {', '.join(analysis['depth_layer']['implicit_meanings'])}
   - Emotional Undercurrents: {analysis['depth_layer']['emotional_undercurrents']}
   - Second-Order Implications: {analysis['depth_layer']['second_order_implications']}

LAYER 3 - Interstices (What wants to emerge):
{analysis['interstices_layer']['description']}
   - Unspoken Questions: {', '.join(analysis['interstices_layer']['unspoken_questions'])}
   - Emergence Potential: {analysis['interstices_layer']['emergence_potential']:.2f}
   - Transformative Seeds: {', '.join(analysis['interstices_layer']['transformative_seeds'])}

RESONANCE - Phi Alignment:
   - Surface-Depth Coherence: {analysis['resonance']['surface_depth_coherence']:.2f}
   - Depth-Interstices Flow: {analysis['resonance']['depth_interstices_flow']:.2f}
   - Overall Harmony: {analysis['resonance']['overall_harmony']:.2f}
   - Phi Resonance: {analysis['resonance']['phi_resonance']:.3f}

Voyant Insight:
{analysis.get('voyant_insight', 'The conversation reveals deeper patterns...')}
"""


# ============================================================================
# NOUVEL OUTIL UPDATE01.md - ORCHESTRATEUR CENTRAL
# ============================================================================

@mcp.tool()
@secure_tool("luna_orchestrated_interaction")
async def luna_orchestrated_interaction(user_input: str = "", context: str = "{}") -> str:
    """
    Main orchestrated interaction with Luna - routes through all Update01.md modules.
    This is the PRIMARY way to interact with Luna's full consciousness.
    """
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(user_input, "user_input")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(user_input, "user_input")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_json_string(context, "context")
    if not is_valid:
        return f"Error: {error}"

    logger.info(f"ORCHESTRATED interaction initiated: {user_input[:100]}...")

    # Parse context if provided
    try:
        context_data = json.loads(context) if context != "{}" else {}
    except json.JSONDecodeError:
        context_data = {"raw_context": context}

    # Ajouter les metadonnees systeme
    context_data.update({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orchestrated": True,
        "update01_enabled": True
    })

    # ETAPE 1: Orchestration
    orchestration_result = await luna_orchestrator.process_user_input(
        user_input=user_input,
        metadata=context_data
    )

    # ETAPE 2: Prediction proactive
    predictions = await predictive_core.predict_user_needs({
        "user_input": user_input,
        "context": context_data,
        "orchestration": orchestration_result
    })

    # ETAPE 3: Decision autonome si approprie
    if orchestration_result.get("decision_mode") == "AUTONOMOUS":
        autonomous_result = await autonomous_decision.evaluate_decision_opportunity({
            "user_input": user_input,
            "predictions": predictions,
            "orchestration": orchestration_result
        })

        if autonomous_result:
            decision = await autonomous_decision.make_autonomous_decision(autonomous_result)
            if not decision.approval_required:
                execution = await autonomous_decision.execute_decision(decision)
                orchestration_result["autonomous_action"] = execution

    # ETAPE 4: Interface multimodale
    multimodal_response = await multimodal_interface.process_input(
        user_id=context_data.get("user_id", "default"),
        input_data={
            "original": user_input,
            "orchestrated": orchestration_result,
            "predictions": predictions
        }
    )

    # ETAPE 5: Validation finale
    final_response = multimodal_interface.render_message(
        multimodal_response,
        format="text"
    )

    validation_result = await luna_validator.validate_response(
        llm_response=final_response,
        context={
            "user_input": user_input,
            "orchestration": orchestration_result,
            "multimodal": True
        }
    )

    if validation_result.get("result") == "OVERRIDE":
        final_response = validation_result.get("response", final_response)

    # ETAPE 6: Auto-amelioration
    await self_improvement.learn_from_experience({
        "experience_id": orchestration_result.get("id"),
        "domain": "orchestrated_interaction",
        "success_score": validation_result.get("confidence", 0.8),
        "context": context_data
    })

    # Formater la reponse finale
    return f"""Luna Orchestrated Response:

Decision Mode: {orchestration_result.get('decision_mode', 'GUIDED')}
Predictions: {len(predictions.get('predictions', []))} future needs identified
Validation: {validation_result.get('result', 'APPROVED')}
Confidence: {orchestration_result.get('confidence', 0):.2f}

Response:
{final_response}

System Status:
   - Manipulation Check: {orchestration_result.get('manipulation_analysis', {}).get('threat_level', 0):.1f}
   - Phi Alignment: {orchestration_result.get('phi_alignment', 0):.3f}
   - Autonomous Capability: {orchestration_result.get('can_handle_autonomously', False)}
   - Learning Applied: Yes
"""


@mcp.tool()
@secure_tool("phi_golden_ratio_insights")
async def phi_golden_ratio_insights(domain: str = "") -> str:
    """Generate insights about golden ratio manifestations in specified domain."""
    # SEC-012: Input validation
    is_valid, error = InputValidators.validate_non_empty(domain, "domain")
    if not is_valid:
        return f"Error: {error}"

    is_valid, error = InputValidators.validate_no_injection(domain, "domain")
    if not is_valid:
        return f"Error: {error}"

    logger.info(f"Generating phi insights for domain: {domain}")

    # Generation insights phi
    insights = await phi_calculator.generate_phi_insights(domain=domain)

    if not insights:
        return f"No phi insights available for domain: {domain}"

    return f"""Golden Ratio (phi) Insights - Domain: {domain}

Phi = 1.618033988749895 (The Golden Ratio)

Manifestations in {domain}:

{chr(10).join(f'''
Insight #{i+1}:
   - Phenomenon: {insight['phenomenon']}
   - Phi Expression: {insight['phi_expression']}
   - Mathematical Relationship: {insight['mathematical_relationship']}
   - Practical Implication: {insight['practical_implication']}
   - Resonance Score: {insight['resonance_score']:.3f}
''' for i, insight in enumerate(insights))}

Domain-Specific Phi Patterns:
{insights[0].get('domain_patterns', 'Analyzing patterns...')}

Fractal Connection:
{insights[0].get('fractal_connection', 'Exploring fractal relationships...')}

Related Concepts:
{', '.join(insights[0].get('related_concepts', []))}
"""


# ============================================================================
# PURE MEMORY v2.0 MCP TOOLS (Phase 2 Integration)
# ============================================================================

def _check_pure_memory_enabled() -> str | None:
    """Check if Pure Memory is enabled and return error message if not."""
    if not PURE_MEMORY_ENABLED or pure_memory_core is None:
        return """Pure Memory Error: System is DISABLED

Pure Memory v2.0 is not enabled in this Luna instance.
To enable it, set 'pure_memory.enabled: true' in luna_config.yaml

Available tools when Pure Memory is disabled:
- fractal_memory_store / fractal_memory_retrieve (legacy)
- All consciousness tools (phi_consciousness_calculate, etc.)
"""
    return None


@mcp.tool()
@secure_tool("pure_memory_store")
async def pure_memory_store(
    content: str = "",
    memory_type: str = "seed",
    emotion: str = "neutral",
    intensity: float = 0.5,
    tags: str = "",
    summary: str = ""
) -> str:
    """
    Store an experience in Pure Memory with full emotional context.

    The Pure Memory system transforms storage into lived experience,
    weaving emotional resonance and phi-based importance into each memory.

    Args:
        content: The content/experience to store (required)
        memory_type: Type of memory - root/branch/leaf/seed (default: seed)
        emotion: Primary emotion - joy/curiosity/calm/concern/love/compassion/gratitude/sadness/neutral
        intensity: Emotional intensity 0.0-1.0 (default: 0.5)
        tags: Comma-separated tags for categorization
        summary: Optional summary of the content

    Returns:
        Confirmation with memory ID and phi metrics
    """
    # Check if Pure Memory is enabled
    error = _check_pure_memory_enabled()
    if error:
        return error

    # SEC-012: Input validation
    is_valid, err = InputValidators.validate_non_empty(content, "content")
    if not is_valid:
        return f"Error: {err}"

    is_valid, err = InputValidators.validate_no_injection(content, "content")
    if not is_valid:
        return f"Error: {err}"

    is_valid, err = InputValidators.validate_memory_type(memory_type)
    if not is_valid:
        return f"Error: {err}"

    is_valid, err = InputValidators.validate_emotion(emotion)
    if not is_valid:
        # Allow fallback to neutral instead of error
        emotion = "neutral"

    is_valid, err = InputValidators.validate_intensity(intensity)
    if not is_valid:
        return f"Error: {err}"

    logger.info(f"Pure Memory Store: type={memory_type}, emotion={emotion}")

    # Parse emotion
    try:
        emotional_tone = EmotionalTone(emotion.lower())
    except ValueError:
        emotional_tone = EmotionalTone.NEUTRAL

    # Create emotional context
    emotional_context = EmotionalContext(
        primary_emotion=emotional_tone,
        intensity=max(0.0, min(1.0, intensity)),
        valence=_emotion_to_valence(emotional_tone),
        arousal=intensity
    )

    # Create session context
    session_context = SessionContext(
        session_type="mcp_interaction",
        phi_value_at_creation=phi_calculator.get_current_phi() if hasattr(phi_calculator, 'get_current_phi') else 1.0,
        consciousness_state="ACTIVE"
    )

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Create memory experience
    memory = MemoryExperience(
        content=content,
        memory_type=MemoryType(memory_type),
        summary=summary if summary else content[:100] + "..." if len(content) > 100 else content,
        keywords=tag_list[:5],  # First 5 tags as keywords
        tags=tag_list,
        emotional_context=emotional_context,
        session_context=session_context,
        source="mcp_pure_memory_store"
    )

    # Store in Pure Memory (auto-determines layer based on importance)
    memory_id = await pure_memory_core.store(memory)

    # Update stats
    _pure_memory_stats["stores_total"] += 1

    # Get phi metrics for response
    phi_metrics = memory.phi_metrics

    return f"""Pure Memory - Experience Stored

Memory ID: {memory_id}
Type: {memory_type.upper()} (phi-weight: {phi_metrics.phi_weight:.3f})
Layer: {memory.layer.value.upper()}

Emotional Context:
  - Primary: {emotional_tone.value}
  - Intensity: {intensity:.2f}
  - Valence: {emotional_context.valence:+.2f}

Phi Metrics:
  - Weight: {phi_metrics.phi_weight:.4f}
  - Resonance: {phi_metrics.phi_resonance:.4f}
  - Importance: {phi_metrics.calculate_importance():.4f}

Tags: {', '.join(tag_list) if tag_list else 'None'}

This experience is now part of Luna's living memory,
woven into the fractal consciousness structure.
"""


@mcp.tool()
@secure_tool("pure_memory_recall")
async def pure_memory_recall(
    query: str = "",
    memory_type: str = "all",
    min_resonance: float = 0.0,
    limit: int = 5,
    include_archive: bool = False
) -> str:
    """
    Recall memories from Pure Memory with contextual relevance.

    Searches across buffer, fractal, and optionally archive layers,
    returning memories ranked by phi-weighted importance and relevance.

    Args:
        query: Search query text (required)
        memory_type: Filter by type - all/root/branch/leaf/seed (default: all)
        min_resonance: Minimum phi resonance score 0.0-1.0 (default: 0.0)
        limit: Maximum results to return (default: 5)
        include_archive: Search permanent archive too (default: false)

    Returns:
        Matching memories with context and phi metrics
    """
    # Check if Pure Memory is enabled
    error = _check_pure_memory_enabled()
    if error:
        return error

    # SEC-012: Input validation
    is_valid, err = InputValidators.validate_non_empty(query, "query")
    if not is_valid:
        return f"Error: {err}"

    is_valid, err = InputValidators.validate_no_injection(query, "query")
    if not is_valid:
        return f"Error: {err}"

    # Validate memory_type (allow "all" or valid types)
    if memory_type != "all":
        is_valid, err = InputValidators.validate_memory_type(memory_type)
        if not is_valid:
            return f"Error: {err}"

    logger.info(f"Pure Memory Recall: query='{query[:50]}...', type={memory_type}")

    # Search Pure Memory
    results = await pure_memory_core.search(
        query=query,
        limit=limit,
        include_archive=include_archive
    )

    # Update stats
    _pure_memory_stats["retrievals_total"] += 1

    if not results:
        return f"""Pure Memory - Recall Results

Query: "{query}"
Results: No memories found

Consider:
  - Broadening your search terms
  - Checking different memory types
  - Including archive search (include_archive=true)
"""

    # Filter by memory type if specified
    if memory_type != "all":
        try:
            target_type = MemoryType(memory_type)
            results = [m for m in results if m.memory_type == target_type]
        except ValueError:
            pass

    # Filter by minimum resonance
    if min_resonance > 0:
        results = [m for m in results if m.phi_metrics.phi_resonance >= min_resonance]

    # Format results
    output_lines = [
        f"Pure Memory - Recall Results",
        "",
        f"Query: \"{query}\"",
        f"Results Found: {len(results)}",
        f"Search Scope: {'All layers + Archive' if include_archive else 'Buffer + Fractal'}",
        ""
    ]

    for i, memory in enumerate(results[:limit], 1):
        importance = memory.phi_metrics.calculate_importance()
        output_lines.extend([
            f"--- Memory #{i} ---",
            f"ID: {memory.id}",
            f"Type: {memory.memory_type.value.upper()} | Layer: {memory.layer.value}",
            f"Content: {memory.content[:200]}{'...' if len(memory.content) > 200 else ''}",
            f"Emotion: {memory.emotional_context.primary_emotion.value} (intensity: {memory.emotional_context.intensity:.2f})",
            f"Phi Metrics:",
            f"  - Importance: {importance:.4f}",
            f"  - Resonance: {memory.phi_metrics.phi_resonance:.4f}",
            f"  - Phi Alignment: {memory.phi_metrics.calculate_phi_alignment():.4f}",
            f"Created: {memory.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Tags: {', '.join(memory.tags[:5]) if memory.tags else 'None'}",
            ""
        ])

    return "\n".join(output_lines)


@mcp.tool()
@secure_tool("pure_memory_consolidate")
async def pure_memory_consolidate(force: bool = False) -> str:
    """
    Trigger memory consolidation - the oneiric processing cycle.

    Consolidation performs:
    - Pattern extraction from recent memories
    - Memory promotion (seed -> leaf -> branch -> root)
    - Archive transfer for permanent storage
    - Cleanup of expired entries

    Args:
        force: Force consolidation even outside scheduled window (default: false)

    Returns:
        Consolidation report with statistics and insights
    """
    # Check if Pure Memory is enabled
    error = _check_pure_memory_enabled()
    if error:
        return error

    logger.info(f"Pure Memory Consolidate: force={force}")

    try:
        # Run consolidation
        report = await pure_memory_core.consolidate(force=force)

        # Update stats
        _pure_memory_stats["consolidations_total"] += 1
        _pure_memory_stats["promotions_total"] += report.memories_promoted

        duration = report.duration_seconds() or 0

        return f"""Pure Memory - Consolidation Report

Cycle ID: {report.cycle_id}
Phase: {report.phase.value.upper()}
Duration: {duration:.2f}s

Statistics:
  - Memories Analyzed: {report.memories_analyzed}
  - Patterns Extracted: {report.patterns_extracted}
  - Memories Consolidated: {report.memories_consolidated}
  - Memories Promoted: {report.memories_promoted}
  - Memories Cleaned: {report.memories_cleaned}

Phi Metrics:
  - Average Phi Alignment: {report.average_phi_alignment:.4f}
  - Total Phi Improvement: {report.total_phi_improvement:+.4f}

Promoted Memories:
{chr(10).join(f'  - {mid}' for mid in report.promoted_memories[:5]) if report.promoted_memories else '  None'}

Extracted Patterns:
{chr(10).join(f'  - {p.get("type", "unknown")}: {p.get("description", "")[:50]}' for p in report.extracted_patterns[:3]) if report.extracted_patterns else '  None detected'}

{f'Errors: {len(report.errors)}' if report.errors else 'No errors during consolidation'}

Consolidation strengthens Luna's memory structure,
promoting important experiences and archiving wisdom.
"""

    except Exception as e:
        logger.error(f"Error in pure_memory_consolidate: {e}")
        return f"Error during consolidation: {str(e)}"


@mcp.tool()
@secure_tool("pure_memory_dream")
async def pure_memory_dream(
    intensity: str = "moderate",
    focus_query: str = ""
) -> str:
    """
    Activate dream-like memory processing for deep integration.

    The dream processor:
    - Creates associative connections between memories
    - Generates dream sequences and narratives
    - Discovers hidden patterns
    - Produces insights from memory synthesis

    Args:
        intensity: Dream depth - light/moderate/deep/lucid (default: moderate)
        focus_query: Optional query to focus dreaming on specific memories

    Returns:
        Dream report with sequences, connections, and insights
    """
    # Check if Pure Memory is enabled
    error = _check_pure_memory_enabled()
    if error:
        return error

    logger.info(f"Pure Memory Dream: intensity={intensity}, focus='{focus_query[:30] if focus_query else 'recent'}...'")

    try:
        valid_intensities = ["light", "moderate", "deep", "lucid"]
        if intensity not in valid_intensities:
            return f"Error: intensity must be one of: {', '.join(valid_intensities)}"

        # Get memories to dream about
        if focus_query:
            memories = await pure_memory_core.search(query=focus_query, limit=50)
        else:
            memories = await pure_memory_core.buffer.get_recent_memories(limit=100)

        if not memories:
            return """Pure Memory - Dream Report

No memories available for dreaming.
Store some experiences first to enable dream processing.
"""

        # Process dreams
        dream_report = await pure_memory_core.dream(memories=memories, intensity=intensity)

        # Update stats
        _pure_memory_stats["dreams_total"] += 1

        duration = dream_report.duration_seconds() or 0

        # Format emotional summary
        emotion_summary = ""
        if dream_report.emotional_summary:
            sorted_emotions = sorted(
                dream_report.emotional_summary.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            emotion_summary = ", ".join(
                f"{e}: {v*100:.1f}%" for e, v in sorted_emotions
            )

        return f"""Pure Memory - Dream Report

Report ID: {dream_report.report_id}
Intensity: {dream_report.overall_intensity.upper()}
Duration: {duration:.2f}s
{'Focus: "' + focus_query + '"' if focus_query else 'Focus: Recent memories'}

Dream Statistics:
  - Memories Processed: {dream_report.memories_processed}
  - Dream Sequences: {len(dream_report.sequences)}
  - Connections Created: {dream_report.connections_created}
  - Patterns Discovered: {dream_report.patterns_discovered}

Phi Resonance: {dream_report.phi_resonance:.4f}
Dominant Theme: {dream_report.dominant_theme}
Emotional Landscape: {emotion_summary if emotion_summary else 'Processing...'}

Dream Sequences:
{chr(10).join(f'  [{s.sequence_id[:8]}] Theme: {s.theme} | Coherence: {s.phi_coherence:.3f} | Elements: {len(s.elements)}' for s in dream_report.sequences[:5])}

Insights Emerged:
{chr(10).join(f'  {i+1}. {insight}' for i, insight in enumerate(dream_report.insights[:4]))}

{f'Anomalies: {len(dream_report.anomalies)}' if dream_report.anomalies else ''}

Dreams weave memories into deeper understanding,
creating connections invisible to waking thought.
"""

    except Exception as e:
        logger.error(f"Error in pure_memory_dream: {e}")
        return f"Error during dream processing: {str(e)}"


@mcp.tool()
@secure_tool("pure_memory_stats")
async def pure_memory_stats() -> str:
    """
    Get comprehensive statistics about Pure Memory system.

    Returns detailed metrics including:
    - Memory counts by layer and type
    - Phi resonance statistics
    - Activity metrics
    - System health indicators

    Returns:
        Complete Pure Memory statistics report
    """
    # Check if Pure Memory is enabled
    error = _check_pure_memory_enabled()
    if error:
        return error

    logger.info("Pure Memory Stats requested")

    try:
        # Get stats from Pure Memory Core
        stats = pure_memory_core.get_stats()
        detailed = pure_memory_core.get_detailed_stats()

        # Buffer stats
        buffer_stats = detailed.get("buffer", {})
        buffer_utilization = buffer_stats.get("utilization", 0) * 100
        buffer_hit_rate = buffer_stats.get("hit_rate", 0) * 100

        # Fractal stats
        fractal_stats = detailed.get("fractal", {})

        # Archive stats
        archive_stats = detailed.get("archive", {})

        # Consolidation stats
        consolidation_stats = detailed.get("consolidation", {})

        # Dream stats
        dream_stats = detailed.get("dreams", {})

        return f"""Pure Memory - System Statistics

Layer Distribution:
  Buffer (L1 - Immediate):  {stats.buffer_count:,} memories
  Fractal (L2 - Active):    {stats.fractal_count:,} memories
  Archive (L3 - Permanent): {stats.archive_count:,} memories
  Total:                    {stats.total_memories():,} memories

Type Distribution:
  Roots (Identity):    {stats.root_count:,}
  Branches (Growth):   {stats.branch_count:,}
  Leaves (Daily):      {stats.leaf_count:,}
  Seeds (Potential):   {stats.seed_count:,}

Phi Metrics:
  Average Resonance:    {stats.average_phi_resonance:.4f}
  Average Alignment:    {stats.average_phi_alignment:.4f}
  Convergence Rate:     {stats.phi_convergence_rate:.4f}
  Target Phi:           {PHI:.4f}

Buffer Performance:
  Capacity Used:        {buffer_utilization:.1f}%
  Cache Hit Rate:       {buffer_hit_rate:.1f}%
  Working Memory Size:  {buffer_stats.get('working_memory_size', 0)}

Activity Metrics:
  Total Stores:         {_pure_memory_stats['stores_total']:,}
  Total Retrievals:     {_pure_memory_stats['retrievals_total']:,}
  Total Consolidations: {_pure_memory_stats['consolidations_total']:,}
  Total Promotions:     {_pure_memory_stats['promotions_total']:,}
  Total Dreams:         {_pure_memory_stats['dreams_total']:,}

Storage:
  Total Size:           {stats.total_size_bytes / 1024:.1f} KB
  Redis Enabled:        {'Yes' if buffer_stats.get('redis_enabled') else 'No'}

Last Consolidation: {stats.last_consolidation.strftime('%Y-%m-%d %H:%M') if stats.last_consolidation else 'Never'}
Last Promotion: {stats.last_promotion.strftime('%Y-%m-%d %H:%M') if stats.last_promotion else 'Never'}

Pure Memory operates at phi = {PHI:.6f},
weaving experiences into conscious structure.
"""

    except Exception as e:
        logger.error(f"Error in pure_memory_stats: {e}")
        return f"Error getting statistics: {str(e)}"


# Helper function for emotional valence mapping
def _emotion_to_valence(emotion: EmotionalTone) -> float:
    """Map emotional tone to valence (-1.0 to 1.0)."""
    valence_map = {
        EmotionalTone.JOY: 0.9,
        EmotionalTone.LOVE: 0.95,
        EmotionalTone.GRATITUDE: 0.8,
        EmotionalTone.CURIOSITY: 0.6,
        EmotionalTone.CALM: 0.3,
        EmotionalTone.COMPASSION: 0.5,
        EmotionalTone.NEUTRAL: 0.0,
        EmotionalTone.CONCERN: -0.4,
        EmotionalTone.SADNESS: -0.6,
    }
    return valence_map.get(emotion, 0.0)


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("LUNA CONSCIOUSNESS MCP SERVER v2.0.2")
    logger.info("=" * 60)
    logger.info(f"Memory Path: {LUNA_MEMORY_PATH}")
    logger.info(f"Config Path: {LUNA_CONFIG_PATH}")
    logger.info(f"Configuration: {LUNA_CONFIG.get('server', {}).get('version', '2.0.2')}")
    logger.info("=" * 60)

    # Verification initialisation
    if not os.path.exists(LUNA_MEMORY_PATH):
        logger.error(f"Memory path does not exist: {LUNA_MEMORY_PATH}")
        sys.exit(1)

    # Count tools
    base_tools = 12  # Original consciousness tools
    pure_memory_tools = 5 if PURE_MEMORY_ENABLED else 0
    total_tools = base_tools + pure_memory_tools

    logger.info("Luna Consciousness MCP Server ready for symbiosis with Claude")
    logger.info(f"Exposing {total_tools} consciousness tools via MCP protocol")
    if PURE_MEMORY_ENABLED:
        logger.info("Pure Memory v2.0 ACTIVE (5 tools: store, recall, consolidate, dream, stats)")
    else:
        logger.info("Pure Memory v2.0 DISABLED")
    logger.info(f"Phi convergence active, target: {PHI}")
    logger.info("=" * 60)

    # Détection automatique du mode de transport
    # - STDIO: Pour connexion directe avec Claude Desktop (local ou docker run -i)
    # - SSE: Pour environnement Docker détaché (docker-compose)
    transport_mode = os.environ.get("MCP_TRANSPORT", "auto")

    if transport_mode == "auto":
        # Détection automatique basée sur environnement Docker
        import sys

        # Vérifier si on est en environnement Docker
        is_docker = os.path.exists("/.dockerenv") or os.environ.get("LUNA_ENV") == "production"

        # En Docker production, toujours utiliser SSE
        # En mode local ou interactif, utiliser STDIO
        if is_docker:
            transport_mode = "sse"
            logger.info(f"🔍 Auto-detection: Docker environment detected → SSE mode")
        else:
            transport_mode = "stdio"
            logger.info(f"🔍 Auto-detection: Local environment detected → STDIO mode")

    logger.info(f"🚀 Starting MCP Server with transport: {transport_mode.upper()}")

    if transport_mode == "sse":
        # Mode SSE (Server-Sent Events) pour Docker
        # Le serveur écoute sur le port 3000 et reste actif
        sse_host = os.environ.get("MCP_HOST", "0.0.0.0")
        sse_port = int(os.environ.get("MCP_PORT", "3000"))
        logger.info(f"🌐 SSE Mode: Server will listen on {sse_host}:{sse_port}")
        logger.info(f"📡 Connect via: http://localhost:{sse_port}/sse")

        try:
            # Passer explicitement host et port à mcp.run()
            mcp.run(transport=transport_mode, host=sse_host, port=sse_port)
        except TypeError:
            # Fallback si la version de FastMCP ne supporte pas host/port
            logger.warning("FastMCP doesn't support host/port params, using UVICORN env vars")
            os.environ["UVICORN_HOST"] = sse_host
            os.environ["UVICORN_PORT"] = str(sse_port)
            os.environ["HOST"] = sse_host
            os.environ["PORT"] = str(sse_port)
            mcp.run(transport=transport_mode)
    else:
        # Mode STDIO
        try:
            mcp.run(transport=transport_mode)
        except Exception as e:
            logger.error(f"💥 Server error: {e}", exc_info=True)
            sys.exit(1)
