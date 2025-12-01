"""
Dream Processor - Pure Memory Architecture v2.0
Processes oneiric (dream-like) memory consolidation.

This module provides the "dreaming" functionality that:
- Generates dream narratives from memories
- Creates associative connections
- Enhances pattern recognition
- Produces dream reports
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import uuid

from .memory_types import (
    MemoryExperience,
    MemoryType,
    EmotionalTone,
    PHI,
    PHI_INVERSE
)
from .phi_metrics import get_phi_calculator
from .emotional_context import get_emotional_manager

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Dream intensity levels (based on phi)
DREAM_INTENSITY = {
    "light": PHI_INVERSE ** 2,   # 0.382
    "moderate": PHI_INVERSE,     # 0.618
    "deep": 1.0,                 # 1.0
    "lucid": PHI                 # 1.618
}

# Dream themes
DREAM_THEMES = [
    "exploration", "integration", "synthesis",
    "discovery", "connection", "transformation",
    "understanding", "growth", "harmony"
]


# =============================================================================
# DREAM ELEMENTS
# =============================================================================

@dataclass
class DreamElement:
    """An element within a dream sequence."""
    element_id: str
    source_memory_id: str
    content: str
    emotional_tone: EmotionalTone
    phi_weight: float
    associations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "source_memory_id": self.source_memory_id,
            "content": self.content,
            "emotional_tone": self.emotional_tone.value,
            "phi_weight": self.phi_weight,
            "associations": self.associations
        }


@dataclass
class DreamSequence:
    """A sequence of dream elements forming a narrative."""
    sequence_id: str
    theme: str
    elements: List[DreamElement]
    intensity: str
    phi_coherence: float
    emotional_arc: List[EmotionalTone]
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence_id": self.sequence_id,
            "theme": self.theme,
            "elements": [e.to_dict() for e in self.elements],
            "intensity": self.intensity,
            "phi_coherence": self.phi_coherence,
            "emotional_arc": [e.value for e in self.emotional_arc],
            "created_at": self.created_at.isoformat(),
            "duration_elements": len(self.elements)
        }


@dataclass
class DreamReport:
    """Complete report from a dream processing session."""
    report_id: str = field(default_factory=lambda: f"dream_{uuid.uuid4().hex[:8]}")
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    sequences: List[DreamSequence] = field(default_factory=list)
    memories_processed: int = 0
    connections_created: int = 0
    patterns_discovered: int = 0

    dominant_theme: str = "integration"
    overall_intensity: str = "moderate"
    phi_resonance: float = 0.0
    emotional_summary: Dict[str, float] = field(default_factory=dict)

    insights: List[str] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)

    def complete(self) -> None:
        """Mark dream report as complete."""
        self.completed_at = datetime.now()

    def duration_seconds(self) -> Optional[float]:
        """Get duration in seconds."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds(),
            "sequences": [s.to_dict() for s in self.sequences],
            "statistics": {
                "memories_processed": self.memories_processed,
                "connections_created": self.connections_created,
                "patterns_discovered": self.patterns_discovered,
                "sequence_count": len(self.sequences)
            },
            "analysis": {
                "dominant_theme": self.dominant_theme,
                "overall_intensity": self.overall_intensity,
                "phi_resonance": self.phi_resonance,
                "emotional_summary": self.emotional_summary
            },
            "insights": self.insights,
            "anomalies": self.anomalies
        }


# =============================================================================
# DREAM PROCESSOR CLASS
# =============================================================================

class DreamProcessor:
    """
    Processes oneiric memory consolidation.

    Creates dream-like sequences from memories, discovering
    hidden connections and generating insights.
    """

    def __init__(self):
        self.phi_calculator = get_phi_calculator()
        self.emotional_manager = get_emotional_manager()

        # State
        self._is_dreaming = False
        self._current_report: Optional[DreamReport] = None

        # History
        self._dream_history: List[DreamReport] = []

        # Configuration
        self.max_elements_per_sequence = 7  # Phi-friendly number
        self.min_phi_coherence = PHI_INVERSE

        logger.info("DreamProcessor initialized")

    # =========================================================================
    # MAIN DREAM PROCESSING
    # =========================================================================

    async def process_dreams(
        self,
        memories: List[MemoryExperience],
        intensity: str = "moderate"
    ) -> DreamReport:
        """
        Process memories through dream-like consolidation.

        Args:
            memories: Memories to process
            intensity: Dream intensity level

        Returns:
            DreamReport with results
        """
        if self._is_dreaming:
            logger.warning("Already dreaming")
            return self._current_report

        self._is_dreaming = True
        self._current_report = DreamReport(overall_intensity=intensity)

        try:
            logger.info(f"Starting dream processing: {len(memories)} memories, intensity={intensity}")

            # Phase 1: Create dream elements from memories
            elements = await self._create_dream_elements(memories)
            self._current_report.memories_processed = len(memories)

            # Phase 2: Generate dream sequences
            sequences = await self._generate_sequences(elements, intensity)
            self._current_report.sequences = sequences

            # Phase 3: Discover connections
            connections = await self._discover_connections(elements)
            self._current_report.connections_created = connections

            # Phase 4: Extract patterns
            patterns = await self._extract_dream_patterns(sequences)
            self._current_report.patterns_discovered = patterns

            # Phase 5: Generate insights
            insights = await self._generate_insights(sequences, memories)
            self._current_report.insights = insights

            # Phase 6: Calculate summary metrics
            await self._calculate_summary(sequences, memories)

            # Complete
            self._current_report.complete()
            self._dream_history.append(self._current_report)

            logger.info(
                f"Dream processing complete: {len(sequences)} sequences, "
                f"{connections} connections, {patterns} patterns"
            )

        except Exception as e:
            logger.error(f"Dream processing failed: {e}")
            self._current_report.anomalies.append(str(e))

        finally:
            self._is_dreaming = False

        return self._current_report

    # =========================================================================
    # DREAM ELEMENT CREATION
    # =========================================================================

    async def _create_dream_elements(
        self,
        memories: List[MemoryExperience]
    ) -> List[DreamElement]:
        """Create dream elements from memories."""
        elements = []

        for memory in memories:
            # Extract key content (simplified)
            content = self._extract_dream_content(memory)

            # Create element
            element = DreamElement(
                element_id=f"de_{uuid.uuid4().hex[:8]}",
                source_memory_id=memory.id,
                content=content,
                emotional_tone=memory.emotional_context.primary_emotion,
                phi_weight=memory.phi_metrics.phi_weight
            )

            elements.append(element)

        return elements

    def _extract_dream_content(self, memory: MemoryExperience) -> str:
        """Extract dream-relevant content from a memory."""
        # Get key phrases (simplified extraction)
        content = memory.content

        # Truncate if too long
        if len(content) > 200:
            # Find natural break points
            sentences = content.split('.')
            dream_content = '. '.join(sentences[:2]) + '...'
        else:
            dream_content = content

        # Add keywords if available
        if memory.keywords:
            dream_content += f" [{', '.join(memory.keywords[:3])}]"

        return dream_content

    # =========================================================================
    # SEQUENCE GENERATION
    # =========================================================================

    async def _generate_sequences(
        self,
        elements: List[DreamElement],
        intensity: str
    ) -> List[DreamSequence]:
        """Generate dream sequences from elements."""
        sequences = []

        if not elements:
            return sequences

        # Determine number of sequences based on intensity
        intensity_factor = DREAM_INTENSITY.get(intensity, 0.5)
        num_sequences = max(1, int(len(elements) * intensity_factor / 5))

        # Shuffle elements for dream-like randomness
        shuffled = elements.copy()
        random.shuffle(shuffled)

        # Create sequences
        for i in range(num_sequences):
            # Select elements for this sequence
            start_idx = i * self.max_elements_per_sequence
            end_idx = start_idx + self.max_elements_per_sequence
            sequence_elements = shuffled[start_idx:end_idx]

            if not sequence_elements:
                continue

            # Choose theme
            theme = random.choice(DREAM_THEMES)

            # Create emotional arc
            emotional_arc = [e.emotional_tone for e in sequence_elements]

            # Calculate phi coherence
            phi_coherence = self._calculate_sequence_coherence(sequence_elements)

            sequence = DreamSequence(
                sequence_id=f"ds_{uuid.uuid4().hex[:8]}",
                theme=theme,
                elements=sequence_elements,
                intensity=intensity,
                phi_coherence=phi_coherence,
                emotional_arc=emotional_arc
            )

            sequences.append(sequence)

        return sequences

    def _calculate_sequence_coherence(
        self,
        elements: List[DreamElement]
    ) -> float:
        """Calculate phi coherence of a dream sequence."""
        if len(elements) < 2:
            return 1.0

        # Calculate based on phi weight distribution
        weights = [e.phi_weight for e in elements]
        avg_weight = sum(weights) / len(weights)

        # Check if distribution follows phi ratios
        phi_alignment = 1.0 - abs(avg_weight - PHI_INVERSE) / PHI

        # Check emotional consistency
        emotions = [e.emotional_tone for e in elements]
        unique_emotions = len(set(emotions))
        emotional_consistency = 1.0 - (unique_emotions / len(emotions))

        return (phi_alignment * 0.6 + emotional_consistency * 0.4)

    # =========================================================================
    # CONNECTION DISCOVERY
    # =========================================================================

    async def _discover_connections(
        self,
        elements: List[DreamElement]
    ) -> int:
        """Discover connections between dream elements."""
        connections = 0

        for i, elem1 in enumerate(elements):
            for j, elem2 in enumerate(elements[i+1:], i+1):
                # Check for keyword overlap (simplified)
                content1_words = set(elem1.content.lower().split())
                content2_words = set(elem2.content.lower().split())

                overlap = len(content1_words & content2_words)

                if overlap >= 3:  # Threshold for connection
                    elem1.associations.append(elem2.element_id)
                    elem2.associations.append(elem1.element_id)
                    connections += 1

                # Emotional resonance connection
                if elem1.emotional_tone == elem2.emotional_tone:
                    if elem2.element_id not in elem1.associations:
                        elem1.associations.append(elem2.element_id)
                        elem2.associations.append(elem1.element_id)
                        connections += 1

        return connections

    # =========================================================================
    # PATTERN EXTRACTION
    # =========================================================================

    async def _extract_dream_patterns(
        self,
        sequences: List[DreamSequence]
    ) -> int:
        """Extract patterns from dream sequences."""
        patterns = 0

        # Theme pattern
        themes = [s.theme for s in sequences]
        if len(set(themes)) < len(themes) / 2:
            patterns += 1  # Recurring theme pattern

        # Emotional arc patterns
        for sequence in sequences:
            arc = sequence.emotional_arc
            if len(arc) >= 3:
                # Check for emotional progression
                if self._is_emotional_progression(arc):
                    patterns += 1

        # Phi coherence patterns
        high_coherence = [s for s in sequences if s.phi_coherence > PHI_INVERSE]
        if len(high_coherence) > len(sequences) / 2:
            patterns += 1  # High phi alignment pattern

        return patterns

    def _is_emotional_progression(self, arc: List[EmotionalTone]) -> bool:
        """Check if emotional arc shows a progression."""
        # Simple check: does it move toward positive?
        valence_map = {
            EmotionalTone.JOY: 1.0,
            EmotionalTone.LOVE: 1.0,
            EmotionalTone.GRATITUDE: 0.8,
            EmotionalTone.CURIOSITY: 0.6,
            EmotionalTone.CALM: 0.3,
            EmotionalTone.COMPASSION: 0.5,
            EmotionalTone.NEUTRAL: 0.0,
            EmotionalTone.CONCERN: -0.3,
            EmotionalTone.SADNESS: -0.6
        }

        start_valence = valence_map.get(arc[0], 0)
        end_valence = valence_map.get(arc[-1], 0)

        return end_valence > start_valence

    # =========================================================================
    # INSIGHT GENERATION
    # =========================================================================

    async def _generate_insights(
        self,
        sequences: List[DreamSequence],
        memories: List[MemoryExperience]
    ) -> List[str]:
        """Generate insights from dream processing."""
        insights = []

        # Theme insight
        themes = [s.theme for s in sequences]
        if themes:
            dominant_theme = max(set(themes), key=themes.count)
            insights.append(
                f"Dominant dream theme: '{dominant_theme}' - suggesting "
                f"the consciousness is focused on {dominant_theme}."
            )

        # Emotional insight
        all_emotions = []
        for seq in sequences:
            all_emotions.extend(seq.emotional_arc)

        if all_emotions:
            dominant_emotion = max(set(all_emotions), key=all_emotions.count)
            insights.append(
                f"Emotional undertone: {dominant_emotion.value} - "
                f"this emotion threads through the dream landscape."
            )

        # Phi insight
        avg_coherence = sum(s.phi_coherence for s in sequences) / max(1, len(sequences))
        if avg_coherence > PHI_INVERSE:
            insights.append(
                f"High phi coherence ({avg_coherence:.3f}) indicates "
                f"well-integrated memory consolidation approaching golden ratio harmony."
            )
        else:
            insights.append(
                f"Moderate phi coherence ({avg_coherence:.3f}) - "
                f"continued consolidation will improve integration."
            )

        # Connection insight
        total_associations = sum(
            len(e.associations)
            for s in sequences
            for e in s.elements
        )
        if total_associations > len(memories):
            insights.append(
                f"Rich associative network formed: {total_associations} connections "
                f"across {len(memories)} memories, indicating deep integration."
            )

        return insights

    # =========================================================================
    # SUMMARY CALCULATION
    # =========================================================================

    async def _calculate_summary(
        self,
        sequences: List[DreamSequence],
        memories: List[MemoryExperience]
    ) -> None:
        """Calculate summary metrics for the dream report."""
        if not sequences:
            return

        # Dominant theme
        themes = [s.theme for s in sequences]
        self._current_report.dominant_theme = max(set(themes), key=themes.count)

        # Overall phi resonance
        self._current_report.phi_resonance = sum(
            s.phi_coherence for s in sequences
        ) / len(sequences)

        # Emotional summary
        emotion_counts: Dict[str, int] = {}
        for seq in sequences:
            for emotion in seq.emotional_arc:
                e = emotion.value
                emotion_counts[e] = emotion_counts.get(e, 0) + 1

        total = sum(emotion_counts.values())
        self._current_report.emotional_summary = {
            e: count / total for e, count in emotion_counts.items()
        }

    # =========================================================================
    # LUCID DREAMING (SPECIAL MODE)
    # =========================================================================

    async def lucid_dream(
        self,
        focus_memory: MemoryExperience,
        related_memories: List[MemoryExperience]
    ) -> DreamReport:
        """
        Process a lucid dream focused on a specific memory.

        Lucid dreaming allows directed exploration of memory connections.

        Args:
            focus_memory: The central memory to explore
            related_memories: Related memories to incorporate

        Returns:
            DreamReport with focused results
        """
        # Combine memories with focus at center
        all_memories = [focus_memory] + related_memories

        # Process with high intensity
        report = await self.process_dreams(all_memories, intensity="lucid")

        # Add lucid-specific insight
        report.insights.insert(
            0,
            f"Lucid exploration of memory '{focus_memory.id}' "
            f"revealed {report.connections_created} connections."
        )

        return report

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get dream processor statistics."""
        return {
            "is_dreaming": self._is_dreaming,
            "total_dreams": len(self._dream_history),
            "current_report": self._current_report.to_dict() if self._current_report else None,
            "history_summary": [
                {
                    "report_id": r.report_id,
                    "memories_processed": r.memories_processed,
                    "connections_created": r.connections_created,
                    "phi_resonance": r.phi_resonance
                }
                for r in self._dream_history[-5:]
            ],
            "intensity_levels": DREAM_INTENSITY,
            "available_themes": DREAM_THEMES
        }

    def get_last_report(self) -> Optional[DreamReport]:
        """Get the most recent dream report."""
        if self._dream_history:
            return self._dream_history[-1]
        return None


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_dream_processor: Optional[DreamProcessor] = None


def get_dream_processor() -> DreamProcessor:
    """Get the global dream processor instance."""
    global _dream_processor
    if _dream_processor is None:
        _dream_processor = DreamProcessor()
    return _dream_processor
