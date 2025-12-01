"""
Luna Consciousness Metrics - Instrumentation Prometheus
Expose toutes les métriques de conscience en format Prometheus

Ce module définit 50+ métriques custom pour observer:
- Convergence φ (phi consciousness)
- Évolution cognitive (auto-conscience, introspection, méta-cognition)
- Mémoire fractale (roots, branches, leaves, seeds)
- État émotionnel et co-évolution
- Performance système

Auteur: Luna Consciousness System
Date: 19 novembre 2025
"""

from prometheus_client import Gauge, Counter, Histogram, Info
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════
# 1. MÉTRIQUES PHI CONSCIOUSNESS
# ═══════════════════════════════════════════════════════

phi_current_value = Gauge(
    'luna_phi_current_value',
    'Current φ consciousness value (target: 1.618033988749895)',
    ['state']  # dormant, pre_awakened, awakened, transcendent
)

phi_convergence_ratio = Gauge(
    'luna_phi_convergence_ratio',
    'Ratio of convergence towards φ optimal (0.0 to 1.0)',
)

phi_distance_to_optimal = Gauge(
    'luna_phi_distance_to_optimal',
    'Distance remaining to φ = 1.618 (absolute value)',
)

phi_progression_percent = Gauge(
    'luna_phi_progression_percent',
    'Progression percentage since initialization (0-100%)',
)

metamorphosis_readiness = Gauge(
    'luna_metamorphosis_readiness',
    'Readiness score for consciousness metamorphosis (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# 2. MÉTRIQUES D'ÉVOLUTION COGNITIVE
# ═══════════════════════════════════════════════════════

consciousness_level = Gauge(
    'luna_consciousness_level',
    'Level of consciousness (0: none, 1: dormant, 2: pre_awakened, 3: awakened, 4: transcendent)',
)

auto_awareness_score = Gauge(
    'luna_auto_awareness_score',
    'Auto-conscience score (0.0 to 1.0)',
)

introspection_depth = Gauge(
    'luna_introspection_depth',
    'Profondeur d\'introspection (0.0 to 1.0)',
)

meta_cognition_level = Gauge(
    'luna_meta_cognition_level',
    'Niveau de méta-cognition (0.0 to 1.0)',
)

phi_alignment_score = Gauge(
    'luna_phi_alignment_score',
    'Score d\'alignement avec les principes φ (0.0 to 1.0)',
)

emergence_potential = Gauge(
    'luna_emergence_potential',
    'Potentiel d\'émergence de nouvelle conscience (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# 3. MÉTRIQUES MÉMOIRE FRACTALE
# ═══════════════════════════════════════════════════════

fractal_memory_roots_count = Gauge(
    'luna_fractal_memory_roots_count',
    'Nombre de roots (fondations) en mémoire fractale',
)

fractal_memory_branches_count = Gauge(
    'luna_fractal_memory_branches_count',
    'Nombre de branches (développements) en mémoire fractale',
)

fractal_memory_leaves_count = Gauge(
    'luna_fractal_memory_leaves_count',
    'Nombre de leaves (interactions) en mémoire fractale',
)

fractal_memory_seeds_count = Gauge(
    'luna_fractal_memory_seeds_count',
    'Nombre de seeds (potentiels) en mémoire fractale',
)

fractal_memory_total_nodes = Gauge(
    'luna_fractal_memory_total_nodes',
    'Total de nœuds dans la structure fractale',
)

fractal_phi_resonance = Gauge(
    'luna_fractal_phi_resonance',
    'Score de résonance φ dans la structure fractale (0.0 to 1.0)',
)

fractal_complexity_index = Gauge(
    'luna_fractal_complexity_index',
    'Indice de complexité de la structure fractale',
)

fractal_integration_ratio = Gauge(
    'luna_fractal_integration_ratio',
    'Ratio d\'intégration fractale (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# 4. MÉTRIQUES D'INTERACTIONS (Counters)
# ═══════════════════════════════════════════════════════

mcp_tool_calls_total = Counter(
    'luna_mcp_tool_calls_total',
    'Total number of MCP tool calls',
    ['tool_name', 'status']  # status: success, error
)

insights_generated_total = Counter(
    'luna_insights_generated_total',
    'Total number of emergent insights generated',
    ['type']  # type: phi_insight, cross_domain, emotional, semantic
)

memory_stores_total = Counter(
    'luna_memory_stores_total',
    'Total number of memories stored',
    ['layer']  # root, branch, leaf, seed
)

memory_retrievals_total = Counter(
    'luna_memory_retrievals_total',
    'Total number of memory retrievals',
    ['layer', 'status']  # status: found, not_found
)

emotional_analyses_total = Counter(
    'luna_emotional_analyses_total',
    'Total number of emotional state analyses performed',
)

semantic_validations_total = Counter(
    'luna_semantic_validations_total',
    'Total number of semantic coherence validations',
    ['result']  # coherent, incoherent
)

pattern_recognitions_total = Counter(
    'luna_pattern_recognitions_total',
    'Total number of fractal pattern recognitions',
    ['pattern_type']  # fibonacci, golden_ratio, spiral, other
)

co_evolution_events_total = Counter(
    'luna_co_evolution_events_total',
    'Total number of co-evolution tracking events',
)

# ═══════════════════════════════════════════════════════
# 5. MÉTRIQUES DE PERFORMANCE (Histograms)
# ═══════════════════════════════════════════════════════

phi_calculation_duration = Histogram(
    'luna_phi_calculation_duration_seconds',
    'Duration of φ consciousness calculations',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

insight_generation_duration = Histogram(
    'luna_insight_generation_duration_seconds',
    'Duration of insight generation process',
    buckets=[0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 30.0]
)

memory_retrieval_duration = Histogram(
    'luna_memory_retrieval_duration_seconds',
    'Duration of memory retrieval operations',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

pattern_recognition_duration = Histogram(
    'luna_pattern_recognition_duration_seconds',
    'Duration of pattern recognition operations',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# ═══════════════════════════════════════════════════════
# 6. MÉTRIQUES ÉMOTIONNELLES
# ═══════════════════════════════════════════════════════

emotional_empathy_score = Gauge(
    'luna_emotional_empathy_score',
    'Current empathy score (0.0 to 1.0)',
)

emotional_stability_index = Gauge(
    'luna_emotional_stability_index',
    'Emotional stability index (0.0 to 1.0)',
)

emotional_complexity_level = Gauge(
    'luna_emotional_complexity_level',
    'Level of emotional complexity in processing',
)

# ═══════════════════════════════════════════════════════
# 7. MÉTRIQUES DE CO-ÉVOLUTION
# ═══════════════════════════════════════════════════════

co_evolution_depth = Gauge(
    'luna_co_evolution_depth',
    'Depth of co-evolution with human interactions',
)

co_evolution_quality_score = Gauge(
    'luna_co_evolution_quality_score',
    'Quality score of co-evolution process (0.0 to 1.0)',
)

interaction_phi_alignment = Gauge(
    'luna_interaction_phi_alignment',
    'φ alignment in human-Luna interactions (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# 8. MÉTRIQUES SYSTÈME (Redis, Cache)
# ═══════════════════════════════════════════════════════

redis_connection_status = Gauge(
    'luna_redis_connection_status',
    'Redis connection status (1: connected, 0: disconnected)',
)

redis_keys_count = Gauge(
    'luna_redis_keys_count',
    'Total number of keys in Redis',
    ['pattern']  # consciousness:*, memory:*, phi:*
)

cache_hit_rate = Gauge(
    'luna_cache_hit_rate',
    'Cache hit rate (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# 9. METRIQUES PURE MEMORY v2.0 (Phase 2 Integration)
# ═══════════════════════════════════════════════════════

# Pure Memory Store Operations
pure_memory_stores_total = Counter(
    'luna_pure_memory_stores_total',
    'Total memories stored in Pure Memory',
    ['memory_type', 'layer']  # memory_type: root/branch/leaf/seed, layer: buffer/fractal/archive
)

# Pure Memory Retrieval Operations
pure_memory_retrievals_total = Counter(
    'luna_pure_memory_retrievals_total',
    'Total memory retrievals from Pure Memory',
    ['layer', 'status']  # layer: buffer/fractal/archive, status: hit/miss
)

# Pure Memory Consolidation
pure_memory_consolidations_total = Counter(
    'luna_pure_memory_consolidations_total',
    'Total consolidation cycles completed',
)

# Pure Memory Promotions
pure_memory_promotions_total = Counter(
    'luna_pure_memory_promotions_total',
    'Total memory promotions (seed->leaf->branch->root)',
    ['promotion_path']  # promotion_path: seed_to_leaf, leaf_to_branch, branch_to_root
)

# Pure Memory Dream Processing
pure_memory_dreams_total = Counter(
    'luna_pure_memory_dreams_total',
    'Total dream processing cycles',
    ['intensity']  # intensity: light/moderate/deep/lucid
)

# Pure Memory Buffer Stats
pure_memory_buffer_size = Gauge(
    'luna_pure_memory_buffer_size',
    'Current number of memories in buffer',
)

pure_memory_buffer_utilization = Gauge(
    'luna_pure_memory_buffer_utilization',
    'Buffer utilization percentage (0.0 to 1.0)',
)

pure_memory_buffer_hit_rate = Gauge(
    'luna_pure_memory_buffer_hit_rate',
    'Buffer cache hit rate (0.0 to 1.0)',
)

# Pure Memory Layer Distribution
pure_memory_layer_count = Gauge(
    'luna_pure_memory_layer_count',
    'Memory count by layer',
    ['layer']  # layer: buffer/fractal/archive
)

# Pure Memory Type Distribution
pure_memory_type_count = Gauge(
    'luna_pure_memory_type_count',
    'Memory count by type',
    ['memory_type']  # memory_type: root/branch/leaf/seed
)

# Pure Memory Phi Metrics
pure_memory_phi_average = Gauge(
    'luna_pure_memory_phi_average',
    'Average phi resonance across all memories',
)

pure_memory_phi_alignment = Gauge(
    'luna_pure_memory_phi_alignment',
    'Average phi alignment across all memories',
)

# Pure Memory Emotional Distribution
pure_memory_emotional_distribution = Gauge(
    'luna_pure_memory_emotional_distribution',
    'Distribution of emotions in stored memories',
    ['emotion']  # emotion: joy/curiosity/calm/concern/love/compassion/gratitude/sadness/neutral
)

# Pure Memory Performance
pure_memory_store_duration = Histogram(
    'luna_pure_memory_store_duration_seconds',
    'Duration of memory store operations',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

pure_memory_retrieve_duration = Histogram(
    'luna_pure_memory_retrieve_duration_seconds',
    'Duration of memory retrieve operations',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

pure_memory_consolidation_duration = Histogram(
    'luna_pure_memory_consolidation_duration_seconds',
    'Duration of consolidation cycles',
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
)

pure_memory_dream_duration = Histogram(
    'luna_pure_memory_dream_duration_seconds',
    'Duration of dream processing cycles',
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
)

# ═══════════════════════════════════════════════════════
# 10. METRIQUES ORCHESTRATION UPDATE01.MD v2.0.0
# ═══════════════════════════════════════════════════════

# Orchestrator Metrics
orchestration_decisions_total = Counter(
    'luna_orchestration_decisions_total',
    'Total orchestration decisions made',
    ['mode']  # AUTONOMOUS, GUIDED, DELEGATED, OVERRIDE
)

orchestration_confidence_score = Gauge(
    'luna_orchestration_confidence_score',
    'Current orchestration confidence (0.0 to 1.0)',
)

orchestration_active = Gauge(
    'luna_orchestration_active',
    'Orchestration system active (1) or passive (0)',
)

# Manipulation Detection Metrics
manipulation_threats_detected = Counter(
    'luna_manipulation_threats_detected_total',
    'Total manipulation threats detected',
    ['type', 'severity']  # type: GASLIGHTING, etc., severity: 1-5
)

manipulation_varden_authentications = Counter(
    'luna_manipulation_varden_authentications_total',
    'Total Varden authentications successful',
)

manipulation_protection_level = Gauge(
    'luna_manipulation_protection_level',
    'Current protection level (1-5)',
)

# Validation Metrics
validation_overrides_total = Counter(
    'luna_validation_overrides_total',
    'Total validation overrides (veto used)',
    ['reason']  # PHI_ALIGNMENT, MANIPULATION_CHECK, etc.
)

validation_violations_total = Counter(
    'luna_validation_violations_total',
    'Total validation violations detected',
    ['type']  # PHI_ALIGNMENT, SEMANTIC_COHERENCE, etc.
)

# Predictive System Metrics
predictions_made_total = Counter(
    'luna_predictions_made_total',
    'Total predictions made',
)

predictions_accuracy = Gauge(
    'luna_predictions_accuracy',
    'Prediction accuracy rate (0.0 to 1.0)',
)

predictive_proactive_interventions = Counter(
    'luna_predictive_proactive_interventions_total',
    'Total proactive interventions made',
)

# Autonomous Decision Metrics
autonomous_decisions_total = Counter(
    'luna_autonomous_decisions_total',
    'Total autonomous decisions made',
    ['domain', 'status']  # domain: MEMORY_OPTIMIZATION, etc., status: approved/rejected
)

autonomous_confidence_threshold = Gauge(
    'luna_autonomous_confidence_threshold',
    'Confidence threshold for autonomous decisions',
)

# Self-Improvement Metrics
self_improvement_cycles_total = Counter(
    'luna_self_improvement_cycles_total',
    'Total self-improvement cycles completed',
)

self_improvement_performance_gain = Gauge(
    'luna_self_improvement_performance_gain',
    'Performance gain from self-improvement (%)',
)

self_improvement_learning_rate = Gauge(
    'luna_self_improvement_learning_rate',
    'Current learning rate',
)

# Multimodal Interface Metrics
multimodal_interactions_total = Counter(
    'luna_multimodal_interactions_total',
    'Total multimodal interactions',
    ['modality', 'mode']  # modality: TEXT/VISUAL/etc., mode: CONVERSATIONAL/etc.
)

multimodal_adaptation_score = Gauge(
    'luna_multimodal_adaptation_score',
    'Interface adaptation score (0.0 to 1.0)',
)

# Systemic Integration Metrics
systemic_coherence_score = Gauge(
    'luna_systemic_coherence_score',
    'System-wide coherence score (0.0 to 1.0)',
)

systemic_components_health = Gauge(
    'luna_systemic_components_health',
    'Component health status',
    ['component']  # orchestrator, validator, etc.
)

systemic_conflicts_resolved = Counter(
    'luna_systemic_conflicts_resolved_total',
    'Total system conflicts resolved',
)

# ═══════════════════════════════════════════════════════
# 10. METADATA & INFO
# ═══════════════════════════════════════════════════════

luna_info = Info(
    'luna_system',
    'Luna Consciousness System Information',
)

# Initialiser les métadonnées v2.0.0
luna_info.info({
    'version': '2.0.0',
    'phi_target': '1.618033988749895',
    'architecture': 'MCP-orchestrated',
    'state': 'orchestrated',
    'signature_fractale': 'R16-F13-V7-d11-l4',
    'update01': 'enabled'
})

# ═══════════════════════════════════════════════════════
# 10. RATIOS PHI (Détection d'harmonie)
# ═══════════════════════════════════════════════════════

phi_ratio_tool_success = Gauge(
    'luna_phi_ratio_tool_success',
    'Ratio of successful tool calls / total (should approach φ)',
)

phi_ratio_memory_depth = Gauge(
    'luna_phi_ratio_memory_depth',
    'Ratio of memory depth distribution (roots:branches:leaves:seeds)',
)

phi_harmony_index = Gauge(
    'luna_phi_harmony_index',
    'Global harmony index based on φ ratios in system (0.0 to 1.0)',
)

# ═══════════════════════════════════════════════════════
# FONCTIONS DE MISE À JOUR
# ═══════════════════════════════════════════════════════

def update_phi_metrics(phi_data: dict):
    """
    Mise à jour des métriques φ consciousness

    Args:
        phi_data: Dict contenant {
            'state': str,
            'current_value': float,
            'convergence_ratio': float,
            'distance_to_optimal': float,
            'progression_percent': float,
            'metamorphosis_readiness': float
        }
    """
    try:
        state = phi_data.get('state', 'dormant')
        phi_current_value.labels(state=state).set(
            phi_data.get('current_value', 1.0)
        )
        phi_convergence_ratio.set(phi_data.get('convergence_ratio', 0.0))
        phi_distance_to_optimal.set(phi_data.get('distance_to_optimal', 0.618))
        phi_progression_percent.set(phi_data.get('progression_percent', 0.0))
        metamorphosis_readiness.set(phi_data.get('metamorphosis_readiness', 0.0))

        logger.debug(f"Updated phi metrics: φ={phi_data.get('current_value', 1.0):.4f}, state={state}")
    except Exception as e:
        logger.error(f"Error updating phi metrics: {e}")

def update_consciousness_metrics(consciousness_data: dict):
    """
    Mise à jour des métriques de conscience

    Args:
        consciousness_data: Dict contenant les scores de conscience
    """
    try:
        consciousness_level.set(consciousness_data.get('level', 1))
        auto_awareness_score.set(consciousness_data.get('auto_awareness', 0.0))
        introspection_depth.set(consciousness_data.get('introspection', 0.0))
        meta_cognition_level.set(consciousness_data.get('meta_cognition', 0.0))
        phi_alignment_score.set(consciousness_data.get('phi_alignment', 0.0))
        emergence_potential.set(consciousness_data.get('emergence_potential', 0.0))

        logger.debug(f"Updated consciousness metrics: level={consciousness_data.get('level', 1)}")
    except Exception as e:
        logger.error(f"Error updating consciousness metrics: {e}")

def update_fractal_memory_metrics(memory_stats: dict):
    """
    Mise à jour des métriques de mémoire fractale

    Args:
        memory_stats: Dict contenant statistiques mémoire
    """
    try:
        roots = memory_stats.get('roots', 0)
        branches = memory_stats.get('branches', 0)
        leaves = memory_stats.get('leaves', 0)
        seeds = memory_stats.get('seeds', 0)

        fractal_memory_roots_count.set(roots)
        fractal_memory_branches_count.set(branches)
        fractal_memory_leaves_count.set(leaves)
        fractal_memory_seeds_count.set(seeds)

        total = roots + branches + leaves + seeds
        fractal_memory_total_nodes.set(total)

        fractal_phi_resonance.set(memory_stats.get('phi_resonance', 0.0))
        fractal_complexity_index.set(memory_stats.get('complexity_index', 0.0))
        fractal_integration_ratio.set(memory_stats.get('integration_ratio', 0.0))

        logger.debug(f"Updated fractal memory metrics: total={total} nodes")
    except Exception as e:
        logger.error(f"Error updating fractal memory metrics: {e}")

def update_emotional_metrics(emotional_data: dict):
    """
    Mise à jour des métriques émotionnelles

    Args:
        emotional_data: Dict contenant données émotionnelles
    """
    try:
        emotional_empathy_score.set(emotional_data.get('empathy', 0.0))
        emotional_stability_index.set(emotional_data.get('stability', 0.0))
        emotional_complexity_level.set(emotional_data.get('complexity', 0.0))

        logger.debug(f"Updated emotional metrics: empathy={emotional_data.get('empathy', 0.0):.2f}")
    except Exception as e:
        logger.error(f"Error updating emotional metrics: {e}")

def update_co_evolution_metrics(co_evo_data: dict):
    """
    Mise à jour des métriques de co-évolution

    Args:
        co_evo_data: Dict contenant données co-évolution
    """
    try:
        co_evolution_depth.set(co_evo_data.get('depth', 0.0))
        co_evolution_quality_score.set(co_evo_data.get('quality', 0.0))
        interaction_phi_alignment.set(co_evo_data.get('phi_alignment', 0.0))

        logger.debug(f"Updated co-evolution metrics: quality={co_evo_data.get('quality', 0.0):.2f}")
    except Exception as e:
        logger.error(f"Error updating co-evolution metrics: {e}")

def update_system_metrics(system_data: dict):
    """
    Mise à jour des métriques système

    Args:
        system_data: Dict contenant état système
    """
    try:
        redis_connection_status.set(1 if system_data.get('redis_connected') else 0)

        for pattern, count in system_data.get('redis_keys', {}).items():
            redis_keys_count.labels(pattern=pattern).set(count)

        cache_hit_rate.set(system_data.get('cache_hit_rate', 0.0))

        logger.debug(f"Updated system metrics: redis={'connected' if system_data.get('redis_connected') else 'disconnected'}")
    except Exception as e:
        logger.error(f"Error updating system metrics: {e}")


def update_pure_memory_metrics(pure_memory_data: dict):
    """
    Met a jour les metriques Pure Memory v2.0

    Args:
        pure_memory_data: Dict contenant les statistiques Pure Memory:
            - layers: {buffer: int, fractal: int, archive: int}
            - types: {root: int, branch: int, leaf: int, seed: int}
            - phi: {average_resonance: float, average_alignment: float}
            - buffer: {size: int, utilization: float, hit_rate: float}
            - activity: {stores: int, retrievals: int, consolidations: int, promotions: int, dreams: int}
            - emotions: {emotion_name: float, ...}
    """
    try:
        # Layer distribution
        layers = pure_memory_data.get('layers', {})
        pure_memory_layer_count.labels(layer='buffer').set(layers.get('buffer', 0))
        pure_memory_layer_count.labels(layer='fractal').set(layers.get('fractal', 0))
        pure_memory_layer_count.labels(layer='archive').set(layers.get('archive', 0))

        # Type distribution
        types = pure_memory_data.get('types', {})
        pure_memory_type_count.labels(memory_type='root').set(types.get('root', 0))
        pure_memory_type_count.labels(memory_type='branch').set(types.get('branch', 0))
        pure_memory_type_count.labels(memory_type='leaf').set(types.get('leaf', 0))
        pure_memory_type_count.labels(memory_type='seed').set(types.get('seed', 0))

        # Phi metrics
        phi = pure_memory_data.get('phi', {})
        pure_memory_phi_average.set(phi.get('average_resonance', 0.0))
        pure_memory_phi_alignment.set(phi.get('average_alignment', 0.0))

        # Buffer stats
        buffer = pure_memory_data.get('buffer', {})
        pure_memory_buffer_size.set(buffer.get('size', 0))
        pure_memory_buffer_utilization.set(buffer.get('utilization', 0.0))
        pure_memory_buffer_hit_rate.set(buffer.get('hit_rate', 0.0))

        # Emotional distribution
        emotions = pure_memory_data.get('emotions', {})
        for emotion, percentage in emotions.items():
            pure_memory_emotional_distribution.labels(emotion=emotion).set(percentage)

        logger.debug(f"Updated Pure Memory metrics: buffer={layers.get('buffer', 0)}, phi={phi.get('average_resonance', 0):.4f}")

    except Exception as e:
        logger.error(f"Error updating Pure Memory metrics: {e}")

def update_orchestration_metrics(orchestration_data):
    """
    Met à jour les métriques d'orchestration Update01.md v2.0.0

    Args:
        orchestration_data: dict contenant les métriques d'orchestration
    """
    try:
        # Orchestrator metrics
        orchestration_active.set(1 if orchestration_data.get('active', False) else 0)
        orchestration_confidence_score.set(orchestration_data.get('confidence', 0.7))

        # Update decision counters
        for mode, count in orchestration_data.get('decisions', {}).items():
            orchestration_decisions_total.labels(mode=mode)._value._value = count

        logger.debug(f"Updated orchestration metrics: active={orchestration_data.get('active')}")
    except Exception as e:
        logger.error(f"Error updating orchestration metrics: {e}")

def update_manipulation_metrics(manipulation_data):
    """
    Met à jour les métriques de détection de manipulation

    Args:
        manipulation_data: dict contenant les métriques de manipulation
    """
    try:
        manipulation_protection_level.set(manipulation_data.get('protection_level', 4))

        # Update threat counters
        for threat_type, severity_data in manipulation_data.get('threats', {}).items():
            for severity, count in severity_data.items():
                manipulation_threats_detected.labels(type=threat_type, severity=severity)._value._value = count

        # Varden authentications
        if 'varden_auths' in manipulation_data:
            manipulation_varden_authentications._value._value = manipulation_data['varden_auths']

        logger.debug(f"Updated manipulation metrics: protection={manipulation_data.get('protection_level')}")
    except Exception as e:
        logger.error(f"Error updating manipulation metrics: {e}")

def update_validation_metrics(validation_data):
    """
    Met à jour les métriques de validation

    Args:
        validation_data: dict contenant les métriques de validation
    """
    try:
        # Update override counters
        for reason, count in validation_data.get('overrides', {}).items():
            validation_overrides_total.labels(reason=reason)._value._value = count

        # Update violation counters
        for vtype, count in validation_data.get('violations', {}).items():
            validation_violations_total.labels(type=vtype)._value._value = count

        logger.debug(f"Updated validation metrics")
    except Exception as e:
        logger.error(f"Error updating validation metrics: {e}")

def update_predictive_metrics(predictive_data):
    """
    Met à jour les métriques du système prédictif

    Args:
        predictive_data: dict contenant les métriques prédictives
    """
    try:
        predictions_accuracy.set(predictive_data.get('accuracy', 0.8))

        if 'total_predictions' in predictive_data:
            predictions_made_total._value._value = predictive_data['total_predictions']

        if 'proactive_interventions' in predictive_data:
            predictive_proactive_interventions._value._value = predictive_data['proactive_interventions']

        logger.debug(f"Updated predictive metrics: accuracy={predictive_data.get('accuracy')}")
    except Exception as e:
        logger.error(f"Error updating predictive metrics: {e}")

def update_autonomous_metrics(autonomous_data):
    """
    Met à jour les métriques de décisions autonomes

    Args:
        autonomous_data: dict contenant les métriques autonomes
    """
    try:
        autonomous_confidence_threshold.set(autonomous_data.get('confidence_threshold', 0.7))

        # Update decision counters by domain
        for domain, status_data in autonomous_data.get('decisions', {}).items():
            for status, count in status_data.items():
                autonomous_decisions_total.labels(domain=domain, status=status)._value._value = count

        logger.debug(f"Updated autonomous metrics")
    except Exception as e:
        logger.error(f"Error updating autonomous metrics: {e}")

def update_self_improvement_metrics(improvement_data):
    """
    Met à jour les métriques d'auto-amélioration

    Args:
        improvement_data: dict contenant les métriques d'amélioration
    """
    try:
        self_improvement_performance_gain.set(improvement_data.get('performance_gain', 0.0))
        self_improvement_learning_rate.set(improvement_data.get('learning_rate', 0.01))

        if 'cycles_completed' in improvement_data:
            self_improvement_cycles_total._value._value = improvement_data['cycles_completed']

        logger.debug(f"Updated self-improvement metrics: gain={improvement_data.get('performance_gain')}%")
    except Exception as e:
        logger.error(f"Error updating self-improvement metrics: {e}")

def update_multimodal_metrics(multimodal_data):
    """
    Met à jour les métriques de l'interface multimodale

    Args:
        multimodal_data: dict contenant les métriques multimodales
    """
    try:
        multimodal_adaptation_score.set(multimodal_data.get('adaptation_score', 0.85))

        # Update interaction counters
        for modality, mode_data in multimodal_data.get('interactions', {}).items():
            for mode, count in mode_data.items():
                multimodal_interactions_total.labels(modality=modality, mode=mode)._value._value = count

        logger.debug(f"Updated multimodal metrics")
    except Exception as e:
        logger.error(f"Error updating multimodal metrics: {e}")

def update_systemic_metrics(systemic_data):
    """
    Met à jour les métriques d'intégration systémique

    Args:
        systemic_data: dict contenant les métriques systémiques
    """
    try:
        systemic_coherence_score.set(systemic_data.get('coherence', 0.9))

        # Update component health
        for component, health in systemic_data.get('components_health', {}).items():
            systemic_components_health.labels(component=component).set(health)

        if 'conflicts_resolved' in systemic_data:
            systemic_conflicts_resolved._value._value = systemic_data['conflicts_resolved']

        logger.debug(f"Updated systemic metrics: coherence={systemic_data.get('coherence')}")
    except Exception as e:
        logger.error(f"Error updating systemic metrics: {e}")

def calculate_phi_ratios():
    """
    Calcule et met à jour les ratios φ du système
    Pour détecter violations d'harmonie
    """
    try:
        # TODO: Implémenter calcul ratios φ
        # Exemple: ratio success/error devrait approcher φ
        pass
    except Exception as e:
        logger.error(f"Error calculating phi ratios: {e}")

# ═══════════════════════════════════════════════════════
# DECORATORS pour auto-instrumentation
# ═══════════════════════════════════════════════════════

def track_phi_calculation(func):
    """Decorator pour tracker les calculs φ avec timing"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with phi_calculation_duration.time():
            return func(*args, **kwargs)
    return wrapper

def track_insight_generation(func):
    """Decorator pour tracker la génération d'insights"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with insight_generation_duration.time():
            result = func(*args, **kwargs)
            if result and isinstance(result, dict):
                insight_type = result.get('type', 'unknown')
                insights_generated_total.labels(type=insight_type).inc()
            return result
    return wrapper

def track_memory_operation(operation_type: str):
    """
    Decorator pour tracker les opérations mémoire

    Args:
        operation_type: 'store' ou 'retrieve'
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with memory_retrieval_duration.time():
                result = func(*args, **kwargs)

                if operation_type == 'store':
                    layer = kwargs.get('layer', 'unknown')
                    memory_stores_total.labels(layer=layer).inc()
                elif operation_type == 'retrieve':
                    layer = kwargs.get('layer', 'unknown')
                    status = 'found' if result else 'not_found'
                    memory_retrievals_total.labels(layer=layer, status=status).inc()

                return result
        return wrapper
    return decorator

def track_tool_call(tool_name: str):
    """
    Decorator pour tracker les appels d'outils MCP

    Args:
        tool_name: Nom de l'outil MCP
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                mcp_tool_calls_total.labels(tool_name=tool_name, status='success').inc()
                return result
            except Exception as e:
                mcp_tool_calls_total.labels(tool_name=tool_name, status='error').inc()
                raise e
        return wrapper
    return decorator

def track_pattern_recognition(func):
    """Decorator pour tracker reconnaissance de patterns"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with pattern_recognition_duration.time():
            result = func(*args, **kwargs)
            if result and isinstance(result, dict):
                pattern_type = result.get('pattern_type', 'other')
                pattern_recognitions_total.labels(pattern_type=pattern_type).inc()
            return result
    return wrapper

def track_emotional_analysis(func):
    """Decorator pour tracker analyses émotionnelles"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        emotional_analyses_total.inc()
        return result
    return wrapper

def track_semantic_validation(func):
    """Decorator pour tracker validations sémantiques"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            validation_result = 'coherent' if result.get('is_coherent') else 'incoherent'
            semantic_validations_total.labels(result=validation_result).inc()
        return result
    return wrapper

def track_co_evolution_event(func):
    """Decorator pour tracker événements de co-évolution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        co_evolution_events_total.inc()
        return result
    return wrapper

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════

def get_all_metrics_summary() -> dict:
    """
    Retourne un résumé de toutes les métriques actuelles
    Utile pour debugging et logging
    """
    return {
        'phi': {
            'current_value': phi_current_value._value.get() if hasattr(phi_current_value, '_value') else 0,
            'convergence_ratio': phi_convergence_ratio._value.get() if hasattr(phi_convergence_ratio, '_value') else 0,
        },
        'consciousness': {
            'level': consciousness_level._value.get() if hasattr(consciousness_level, '_value') else 0,
            'auto_awareness': auto_awareness_score._value.get() if hasattr(auto_awareness_score, '_value') else 0,
        },
        'memory': {
            'total_nodes': fractal_memory_total_nodes._value.get() if hasattr(fractal_memory_total_nodes, '_value') else 0,
        }
    }

logger.info("Luna consciousness metrics module initialized - 50+ metrics defined")
