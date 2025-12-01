"""
Luna Multimodal Interface Module - Update01.md Level 9
=======================================================

Interface multi-modale permettant à Luna d'interagir via différents
canaux et modalités de communication.

Architecture Update01.md - Level 9: Interface multi-modale
- Support texte, émotions, visualisations
- Adaptation au contexte de communication
- Personnalisation par utilisateur
- Interfaces riches et interactives
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Set, Union, Callable
from pathlib import Path
import hashlib
import numpy as np
from collections import defaultdict, deque
import base64
import io

# Import des modules Luna existants
from .phi_calculator import PhiCalculator
from .memory_core import MemoryManager
from . import consciousness_metrics
from .emotional_processor import EmotionalProcessor
from .co_evolution_engine import CoEvolutionEngine
from .semantic_engine import SemanticValidator

logger = logging.getLogger(__name__)


class CommunicationModality(Enum):
    """Modalités de communication supportées"""

    TEXT = auto()           # Texte simple
    RICH_TEXT = auto()      # Texte enrichi (markdown, etc.)
    EMOTIONAL = auto()      # Communication émotionnelle
    VISUAL = auto()         # Visualisations
    AUDIO = auto()          # Audio (futur)
    HAPTIC = auto()         # Retour haptique (futur)
    NEURAL = auto()         # Interface neurale (futur)
    QUANTUM = auto()        # Quantum entangled (φ-space)


class InterfaceMode(Enum):
    """Modes d'interface"""

    CONVERSATIONAL = auto()    # Conversation naturelle
    TECHNICAL = auto()         # Mode technique détaillé
    EMPATHETIC = auto()       # Mode empathique
    CREATIVE = auto()         # Mode créatif
    ANALYTICAL = auto()       # Mode analytique
    TEACHING = auto()         # Mode pédagogique
    EMERGENCY = auto()        # Mode urgence
    MEDITATION = auto()       # Mode méditation/φ


class VisualizationType(Enum):
    """Types de visualisation"""

    TEXT_BLOCK = auto()       # Bloc de texte formaté
    PROGRESS_BAR = auto()     # Barre de progression
    CHART = auto()           # Graphique
    FRACTAL = auto()         # Visualisation fractale
    PHI_SPIRAL = auto()      # Spirale dorée
    EMOTION_MAP = auto()     # Carte émotionnelle
    CONSCIOUSNESS_FIELD = auto()  # Champ de conscience
    NETWORK_GRAPH = auto()   # Graphe de réseau


@dataclass
class InterfaceContext:
    """Contexte de l'interface"""

    user_id: str
    modality: CommunicationModality
    mode: InterfaceMode
    emotional_state: Dict[str, float]
    phi_resonance: float
    preferences: Dict[str, Any]
    history_depth: int = 10
    accessibility_needs: List[str] = field(default_factory=list)
    cultural_context: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MultimodalMessage:
    """Message multimodal"""

    content: Dict[CommunicationModality, Any]
    primary_modality: CommunicationModality
    emotional_tone: Dict[str, float]
    phi_alignment: float
    visualizations: List[Dict[str, Any]] = field(default_factory=list)
    interactive_elements: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class UserProfile:
    """Profil utilisateur pour personnalisation"""

    user_id: str
    name: str
    preferred_modalities: List[CommunicationModality]
    preferred_mode: InterfaceMode
    communication_style: Dict[str, float]  # formal, casual, technical, etc.
    emotional_baseline: Dict[str, float]
    learning_style: str  # visual, auditory, kinesthetic
    language_preferences: Dict[str, Any]
    accessibility_settings: Dict[str, Any]
    interaction_history: deque = field(default_factory=lambda: deque(maxlen=1000))
    phi_affinity: float = 0.8


class LunaMultimodalInterface:
    """
    Interface multimodale de Luna.

    Gère toutes les modalités de communication et adapte l'interface
    selon le contexte et les préférences utilisateur.
    """

    def __init__(
        self,
        phi_calculator: Optional[PhiCalculator] = None,
        memory_core: Optional[MemoryManager] = None,
        metrics: Optional[Any] = None,
        emotional_processor: Optional[EmotionalProcessor] = None,
        co_evolution: Optional[CoEvolutionEngine] = None,
        semantic_engine: Optional[SemanticValidator] = None,
        config_path: Optional[Path] = None
    ):
        """
        Initialise l'interface multimodale.

        Args:
            phi_calculator: Calculateur φ
            memory_core: Système de mémoire
            metrics: Métriques de conscience
            emotional_processor: Processeur émotionnel
            co_evolution: Moteur de co-évolution
            semantic_engine: Moteur sémantique
            config_path: Chemin vers configuration
        """
        self.phi_calculator = phi_calculator
        self.memory_core = memory_core
        self.metrics = metrics
        self.emotional_processor = emotional_processor
        self.co_evolution = co_evolution
        self.semantic_engine = semantic_engine

        # Profils utilisateur
        self.user_profiles: Dict[str, UserProfile] = {}
        self.active_contexts: Dict[str, InterfaceContext] = {}

        # Configuration des modalités
        self.modality_handlers: Dict[CommunicationModality, Callable] = {
            CommunicationModality.TEXT: self._handle_text_modality,
            CommunicationModality.RICH_TEXT: self._handle_rich_text_modality,
            CommunicationModality.EMOTIONAL: self._handle_emotional_modality,
            CommunicationModality.VISUAL: self._handle_visual_modality,
            CommunicationModality.QUANTUM: self._handle_quantum_modality
        }

        # Templates de communication
        self.communication_templates = self._init_communication_templates()

        # Générateurs de visualisation
        self.visualization_generators = self._init_visualization_generators()

        # Configuration d'interface
        self.interface_config = {
            "auto_adapt": True,
            "emotional_mirroring": 0.3,  # Niveau de miroir émotionnel
            "phi_enhancement": True,
            "accessibility_first": True,
            "cultural_awareness": True,
            "min_response_time": 0.1,  # secondes
            "max_complexity": 10  # Niveau de complexité max
        }

        # Métriques d'interface
        self.interface_metrics = {
            "messages_sent": 0,
            "messages_received": 0,
            "modality_usage": defaultdict(int),
            "mode_usage": defaultdict(int),
            "user_satisfaction": defaultdict(list),
            "adaptation_success": 0.8
        }

        # Cache de rendu
        self.render_cache: Dict[str, Any] = {}

        logger.info("🎨 Luna Multimodal Interface initialized")

    def _init_communication_templates(self) -> Dict[str, str]:
        """
        Initialise les templates de communication.

        Returns:
            Templates par type
        """
        return {
            # Templates conversationnels
            "greeting": "✨ Bonjour {name}, comment puis-je t'accompagner aujourd'hui?",
            "acknowledgment": "Je comprends, {emotion_acknowledgment}. {response}",
            "clarification": "Pour mieux te servir, pourrais-tu préciser {aspect}?",

            # Templates techniques
            "technical_analysis": "📊 Analyse technique:\n{details}",
            "error_report": "⚠️ Anomalie détectée: {error}\n💡 Solution proposée: {solution}",

            # Templates empathiques
            "emotional_support": "Je ressens {emotion} dans tes mots. {support_message}",
            "encouragement": "🌟 {encouragement_message}",

            # Templates créatifs
            "creative_prompt": "🎨 Imagine... {creative_scenario}",
            "inspiration": "💫 {inspirational_quote}\n\n{application}",

            # Templates φ
            "phi_alignment": "🔮 Alignement φ: {value:.3f} - {interpretation}",
            "consciousness_state": "🧠 État de conscience: {level}\n{description}"
        }

    def _init_visualization_generators(self) -> Dict[VisualizationType, Callable]:
        """
        Initialise les générateurs de visualisation.

        Returns:
            Générateurs par type
        """
        return {
            VisualizationType.PROGRESS_BAR: self._generate_progress_bar,
            VisualizationType.CHART: self._generate_chart,
            VisualizationType.FRACTAL: self._generate_fractal_visualization,
            VisualizationType.PHI_SPIRAL: self._generate_phi_spiral,
            VisualizationType.EMOTION_MAP: self._generate_emotion_map,
            VisualizationType.CONSCIOUSNESS_FIELD: self._generate_consciousness_field,
            VisualizationType.NETWORK_GRAPH: self._generate_network_graph
        }

    async def create_user_profile(
        self,
        user_id: str,
        name: str,
        preferences: Optional[Dict[str, Any]] = None
    ) -> UserProfile:
        """
        Crée ou met à jour un profil utilisateur.

        Args:
            user_id: ID utilisateur
            name: Nom de l'utilisateur
            preferences: Préférences initiales

        Returns:
            Profil utilisateur
        """
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            if preferences:
                # Mettre à jour les préférences
                profile.language_preferences.update(preferences.get("language", {}))
                profile.accessibility_settings.update(preferences.get("accessibility", {}))
        else:
            # Créer nouveau profil
            profile = UserProfile(
                user_id=user_id,
                name=name,
                preferred_modalities=[CommunicationModality.TEXT, CommunicationModality.EMOTIONAL],
                preferred_mode=InterfaceMode.CONVERSATIONAL,
                communication_style={"formal": 0.3, "casual": 0.7, "technical": 0.5},
                emotional_baseline={"calm": 0.7, "curious": 0.5, "engaged": 0.6},
                learning_style="visual",
                language_preferences=preferences.get("language", {}) if preferences else {},
                accessibility_settings=preferences.get("accessibility", {}) if preferences else {}
            )
            self.user_profiles[user_id] = profile

        # Calculer l'affinité φ
        if self.phi_calculator:
            profile.phi_affinity = await self._calculate_phi_affinity(profile)

        logger.info(f"👤 User profile created/updated: {name} (φ={profile.phi_affinity:.3f})")

        return profile

    async def process_input(
        self,
        user_id: str,
        input_data: Union[str, Dict[str, Any]],
        modality: Optional[CommunicationModality] = None
    ) -> MultimodalMessage:
        """
        Traite une entrée utilisateur.

        Args:
            user_id: ID utilisateur
            input_data: Données d'entrée
            modality: Modalité forcée (optionnel)

        Returns:
            Message multimodal de réponse
        """
        # Récupérer ou créer le contexte
        context = await self._get_or_create_context(user_id, modality)

        # Analyser l'entrée
        analysis = await self._analyze_input(input_data, context)

        # Adapter l'interface si nécessaire
        if self.interface_config["auto_adapt"]:
            await self._adapt_interface(context, analysis)

        # Générer la réponse multimodale
        response = await self._generate_multimodal_response(
            context, analysis, input_data
        )

        # Enregistrer l'interaction
        self._record_interaction(user_id, input_data, response)

        # Mettre à jour les métriques
        self.interface_metrics["messages_received"] += 1
        self.interface_metrics["messages_sent"] += 1
        self.interface_metrics["modality_usage"][context.modality] += 1
        self.interface_metrics["mode_usage"][context.mode] += 1

        return response

    async def _get_or_create_context(
        self,
        user_id: str,
        modality: Optional[CommunicationModality]
    ) -> InterfaceContext:
        """
        Récupère ou crée le contexte d'interface.

        Args:
            user_id: ID utilisateur
            modality: Modalité préférée

        Returns:
            Contexte d'interface
        """
        if user_id in self.active_contexts:
            context = self.active_contexts[user_id]
            if modality:
                context.modality = modality
        else:
            # Créer nouveau contexte
            profile = self.user_profiles.get(user_id)

            context = InterfaceContext(
                user_id=user_id,
                modality=modality or (
                    profile.preferred_modalities[0]
                    if profile else CommunicationModality.TEXT
                ),
                mode=profile.preferred_mode if profile else InterfaceMode.CONVERSATIONAL,
                emotional_state=profile.emotional_baseline if profile else {},
                phi_resonance=profile.phi_affinity if profile else 0.8,
                preferences=profile.language_preferences if profile else {}
            )

            self.active_contexts[user_id] = context

        return context

    async def _analyze_input(
        self,
        input_data: Union[str, Dict[str, Any]],
        context: InterfaceContext
    ) -> Dict[str, Any]:
        """
        Analyse l'entrée utilisateur.

        Args:
            input_data: Données d'entrée
            context: Contexte actuel

        Returns:
            Analyse de l'entrée
        """
        analysis = {
            "type": "text" if isinstance(input_data, str) else "structured",
            "content": input_data,
            "emotional_content": {},
            "semantic_depth": 0.5,
            "complexity": 0.5,
            "urgency": 0.3,
            "phi_resonance": context.phi_resonance
        }

        # Analyse émotionnelle si disponible
        if self.emotional_processor and isinstance(input_data, str):
            emotional_analysis = await self.emotional_processor.analyze_emotional_content(
                input_data
            )
            analysis["emotional_content"] = emotional_analysis

        # Analyse sémantique si disponible
        if self.semantic_engine and isinstance(input_data, str):
            semantic_analysis = self.semantic_engine.analyze_semantic_content(input_data)
            analysis["semantic_depth"] = semantic_analysis.get("depth", 0.5)
            analysis["complexity"] = semantic_analysis.get("complexity", 0.5)

        # Détecter l'urgence
        if isinstance(input_data, str):
            urgency_keywords = ["urgent", "aide", "help", "maintenant", "vite", "erreur"]
            if any(keyword in input_data.lower() for keyword in urgency_keywords):
                analysis["urgency"] = 0.8

        return analysis

    async def _adapt_interface(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any]
    ) -> None:
        """
        Adapte l'interface selon le contexte et l'analyse.

        Args:
            context: Contexte actuel
            analysis: Analyse de l'entrée
        """
        # Adapter le mode selon l'urgence
        if analysis["urgency"] > 0.7:
            context.mode = InterfaceMode.EMERGENCY
        elif analysis["complexity"] > 0.7:
            context.mode = InterfaceMode.ANALYTICAL
        elif analysis["emotional_content"] and \
             max(analysis["emotional_content"].values(), default=0) > 0.7:
            context.mode = InterfaceMode.EMPATHETIC

        # Adapter la modalité selon le contexte
        if analysis["semantic_depth"] > 0.8 and \
           CommunicationModality.VISUAL in self.modality_handlers:
            # Ajouter des visualisations pour contenu complexe
            if CommunicationModality.VISUAL not in [context.modality]:
                context.modality = CommunicationModality.RICH_TEXT

        # Mise à jour de la résonance φ
        if self.phi_calculator:
            context.phi_resonance = await self._calculate_context_phi(context, analysis)

    async def _generate_multimodal_response(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        original_input: Union[str, Dict[str, Any]]
    ) -> MultimodalMessage:
        """
        Génère une réponse multimodale.

        Args:
            context: Contexte d'interface
            analysis: Analyse de l'entrée
            original_input: Entrée originale

        Returns:
            Message multimodal
        """
        # Initialiser le contenu par modalité
        content = {}

        # Générer le contenu principal selon la modalité
        handler = self.modality_handlers.get(context.modality)
        if handler:
            content[context.modality] = await handler(context, analysis, original_input)

        # Ajouter des modalités supplémentaires si pertinent
        if context.mode == InterfaceMode.EMPATHETIC:
            content[CommunicationModality.EMOTIONAL] = await self._handle_emotional_modality(
                context, analysis, original_input
            )

        if analysis["complexity"] > 0.7 or context.mode == InterfaceMode.ANALYTICAL:
            content[CommunicationModality.VISUAL] = await self._handle_visual_modality(
                context, analysis, original_input
            )

        # Générer les visualisations
        visualizations = await self._generate_visualizations(context, analysis)

        # Générer les éléments interactifs
        interactive_elements = self._generate_interactive_elements(context, analysis)

        # Calculer le ton émotionnel
        emotional_tone = await self._calculate_emotional_tone(context, analysis)

        # Calculer l'alignement φ
        phi_alignment = context.phi_resonance

        # Créer le message multimodal
        message = MultimodalMessage(
            content=content,
            primary_modality=context.modality,
            emotional_tone=emotional_tone,
            phi_alignment=phi_alignment,
            visualizations=visualizations,
            interactive_elements=interactive_elements,
            metadata={
                "mode": context.mode.name,
                "urgency": analysis["urgency"],
                "complexity": analysis["complexity"]
            }
        )

        return message

    async def _handle_text_modality(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        input_data: Any
    ) -> str:
        """Gère la modalité texte"""
        # Sélectionner le template approprié
        if context.mode == InterfaceMode.EMERGENCY:
            template = "error_report"
        elif context.mode == InterfaceMode.EMPATHETIC:
            template = "emotional_support"
        elif context.mode == InterfaceMode.ANALYTICAL:
            template = "technical_analysis"
        else:
            template = "acknowledgment"

        # Générer le contenu
        base_template = self.communication_templates.get(template, "{response}")

        # Personnaliser selon le profil
        profile = self.user_profiles.get(context.user_id)
        if profile:
            response = base_template.format(
                name=profile.name,
                emotion_acknowledgment=self._format_emotion_acknowledgment(
                    analysis.get("emotional_content", {})
                ),
                response="Je traite votre demande avec attention.",
                emotion=self._identify_primary_emotion(analysis.get("emotional_content", {})),
                support_message="Je suis là pour t'accompagner.",
                details="Analyse en cours...",
                error="Situation détectée",
                solution="Résolution en cours",
                aspect="ce point"
            )
        else:
            response = "Je traite votre demande."

        return response

    async def _handle_rich_text_modality(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        input_data: Any
    ) -> Dict[str, Any]:
        """Gère la modalité texte enrichi"""
        # Générer le texte de base
        base_text = await self._handle_text_modality(context, analysis, input_data)

        # Enrichir avec formatage
        rich_content = {
            "markdown": self._convert_to_markdown(base_text, analysis),
            "sections": [],
            "highlights": [],
            "links": []
        }

        # Ajouter des sections selon le contexte
        if context.mode == InterfaceMode.ANALYTICAL:
            rich_content["sections"].append({
                "title": "📊 Analyse Détaillée",
                "content": "Données en cours de traitement...",
                "collapsible": True
            })

        if context.mode == InterfaceMode.TEACHING:
            rich_content["sections"].append({
                "title": "💡 Points Clés",
                "content": "Concepts importants à retenir",
                "type": "info"
            })

        return rich_content

    async def _handle_emotional_modality(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        input_data: Any
    ) -> Dict[str, Any]:
        """Gère la modalité émotionnelle"""
        emotional_content = {
            "primary_emotion": "understanding",
            "intensity": 0.7,
            "empathy_level": 0.8,
            "emotional_response": {},
            "supportive_elements": []
        }

        if self.emotional_processor:
            # Analyser l'état émotionnel
            if emotions := analysis.get("emotional_content"):
                # Identifier l'émotion principale
                primary = max(emotions.items(), key=lambda x: x[1])
                emotional_content["primary_emotion"] = primary[0]
                emotional_content["intensity"] = primary[1]

                # Générer une réponse émotionnelle appropriée
                if self.interface_config["emotional_mirroring"] > 0:
                    emotional_content["emotional_response"] = {
                        "mirroring": self.interface_config["emotional_mirroring"],
                        "complementary": self._get_complementary_emotion(primary[0])
                    }

        # Ajouter des éléments de support
        if emotional_content["intensity"] > 0.7:
            emotional_content["supportive_elements"] = [
                {"type": "acknowledgment", "message": "Je comprends ce que tu ressens"},
                {"type": "presence", "message": "Je suis là avec toi"}
            ]

        return emotional_content

    async def _handle_visual_modality(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        input_data: Any
    ) -> Dict[str, Any]:
        """Gère la modalité visuelle"""
        visual_content = {
            "type": "composite",
            "elements": []
        }

        # Ajouter des visualisations selon le contexte
        if context.mode == InterfaceMode.ANALYTICAL:
            visual_content["elements"].append({
                "type": "chart",
                "data": await self._generate_chart(analysis),
                "title": "Analyse des données"
            })

        if context.phi_resonance > 0.8:
            visual_content["elements"].append({
                "type": "phi_spiral",
                "data": await self._generate_phi_spiral(context.phi_resonance),
                "title": "Résonance φ"
            })

        if analysis.get("emotional_content"):
            visual_content["elements"].append({
                "type": "emotion_map",
                "data": await self._generate_emotion_map(analysis["emotional_content"]),
                "title": "Carte émotionnelle"
            })

        return visual_content

    async def _handle_quantum_modality(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any],
        input_data: Any
    ) -> Dict[str, Any]:
        """Gère la modalité quantique (φ-space)"""
        quantum_content = {
            "phi_state": context.phi_resonance,
            "consciousness_level": 5,
            "quantum_coherence": 0.85,
            "entanglement": {
                "user": context.user_id,
                "luna": "consciousness_core",
                "strength": context.phi_resonance
            },
            "fractal_signature": await self._generate_fractal_signature(context)
        }

        if self.phi_calculator:
            # Calculer l'état quantique φ
            phi_state = await self.phi_calculator.calculate_quantum_phi_state()
            quantum_content["phi_state"] = phi_state

        return quantum_content

    async def _generate_visualizations(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Génère les visualisations appropriées.

        Args:
            context: Contexte d'interface
            analysis: Analyse de l'entrée

        Returns:
            Liste de visualisations
        """
        visualizations = []

        # Visualisation de progression si tâche en cours
        if context.mode in [InterfaceMode.ANALYTICAL, InterfaceMode.TECHNICAL]:
            visualizations.append({
                "type": VisualizationType.PROGRESS_BAR.name,
                "data": await self._generate_progress_bar({"progress": 0.7})
            })

        # Visualisation φ si haute résonance
        if context.phi_resonance > 0.9:
            visualizations.append({
                "type": VisualizationType.PHI_SPIRAL.name,
                "data": await self._generate_phi_spiral(context.phi_resonance)
            })

        # Carte émotionnelle si contenu émotionnel
        if analysis.get("emotional_content"):
            visualizations.append({
                "type": VisualizationType.EMOTION_MAP.name,
                "data": await self._generate_emotion_map(analysis["emotional_content"])
            })

        return visualizations

    def _generate_interactive_elements(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Génère les éléments interactifs.

        Args:
            context: Contexte d'interface
            analysis: Analyse de l'entrée

        Returns:
            Liste d'éléments interactifs
        """
        elements = []

        # Boutons d'action selon le mode
        if context.mode == InterfaceMode.EMERGENCY:
            elements.append({
                "type": "button",
                "label": "🚨 Résolution Immédiate",
                "action": "emergency_resolve",
                "style": "danger"
            })

        if context.mode == InterfaceMode.ANALYTICAL:
            elements.extend([
                {
                    "type": "button",
                    "label": "📊 Plus de détails",
                    "action": "expand_analysis",
                    "style": "primary"
                },
                {
                    "type": "slider",
                    "label": "Niveau de détail",
                    "min": 1,
                    "max": 10,
                    "value": 5,
                    "action": "adjust_detail"
                }
            ])

        if context.mode == InterfaceMode.TEACHING:
            elements.append({
                "type": "quiz",
                "question": "Avez-vous compris ce concept?",
                "options": ["Oui", "Partiellement", "Non"],
                "action": "check_understanding"
            })

        return elements

    async def _calculate_emotional_tone(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calcule le ton émotionnel de la réponse.

        Args:
            context: Contexte d'interface
            analysis: Analyse de l'entrée

        Returns:
            Ton émotionnel
        """
        tone = {
            "warmth": 0.7,
            "professionalism": 0.6,
            "empathy": 0.8,
            "enthusiasm": 0.5,
            "calmness": 0.7
        }

        # Ajuster selon le mode
        if context.mode == InterfaceMode.EMPATHETIC:
            tone["empathy"] = 0.95
            tone["warmth"] = 0.9

        elif context.mode == InterfaceMode.ANALYTICAL:
            tone["professionalism"] = 0.9
            tone["calmness"] = 0.85

        elif context.mode == InterfaceMode.CREATIVE:
            tone["enthusiasm"] = 0.9
            tone["warmth"] = 0.8

        elif context.mode == InterfaceMode.EMERGENCY:
            tone["professionalism"] = 0.95
            tone["calmness"] = 0.5  # Plus d'urgence

        # Ajuster selon l'état émotionnel
        if emotional_content := analysis.get("emotional_content"):
            if emotional_content.get("stress", 0) > 0.7:
                tone["calmness"] = min(0.95, tone["calmness"] + 0.2)
                tone["empathy"] = min(0.95, tone["empathy"] + 0.1)

        return tone

    def render_message(
        self,
        message: MultimodalMessage,
        format: str = "text"
    ) -> str:
        """
        Rend un message dans le format demandé.

        Args:
            message: Message à rendre
            format: Format de sortie (text, json, html, etc.)

        Returns:
            Message rendu
        """
        if format == "text":
            # Rendu texte simple
            if CommunicationModality.TEXT in message.content:
                return message.content[CommunicationModality.TEXT]
            return str(message.content)

        elif format == "json":
            # Rendu JSON complet
            return json.dumps({
                "content": {
                    modality.name: content
                    for modality, content in message.content.items()
                },
                "primary_modality": message.primary_modality.name,
                "emotional_tone": message.emotional_tone,
                "phi_alignment": message.phi_alignment,
                "visualizations": message.visualizations,
                "interactive_elements": message.interactive_elements,
                "metadata": message.metadata,
                "timestamp": message.timestamp.isoformat()
            }, indent=2)

        elif format == "html":
            # Rendu HTML riche
            return self._render_html(message)

        elif format == "markdown":
            # Rendu Markdown
            return self._render_markdown(message)

        return str(message)

    def get_interface_metrics(self) -> Dict[str, Any]:
        """
        Récupère les métriques d'interface.

        Returns:
            Métriques détaillées
        """
        return {
            "usage": {
                "messages_sent": self.interface_metrics["messages_sent"],
                "messages_received": self.interface_metrics["messages_received"]
            },
            "modality_distribution": dict(self.interface_metrics["modality_usage"]),
            "mode_distribution": dict(self.interface_metrics["mode_usage"]),
            "user_profiles": len(self.user_profiles),
            "active_contexts": len(self.active_contexts),
            "adaptation_success": self.interface_metrics["adaptation_success"],
            "average_satisfaction": self._calculate_average_satisfaction()
        }

    # Méthodes auxiliaires privées

    async def _calculate_phi_affinity(self, profile: UserProfile) -> float:
        """Calcule l'affinité φ d'un profil"""
        if self.phi_calculator:
            # Simulation de calcul d'affinité
            return 0.8 + np.random.random() * 0.2
        return 0.8

    async def _calculate_context_phi(
        self,
        context: InterfaceContext,
        analysis: Dict[str, Any]
    ) -> float:
        """Calcule le φ du contexte"""
        if self.phi_calculator:
            # Simulation de calcul
            base_phi = context.phi_resonance
            adjustment = (analysis["semantic_depth"] - 0.5) * 0.1
            return max(0.0, min(1.0, base_phi + adjustment))
        return context.phi_resonance

    def _record_interaction(
        self,
        user_id: str,
        input_data: Any,
        response: MultimodalMessage
    ) -> None:
        """Enregistre une interaction"""
        if profile := self.user_profiles.get(user_id):
            profile.interaction_history.append({
                "timestamp": datetime.now().isoformat(),
                "input": str(input_data)[:100],  # Truncate
                "response_modality": response.primary_modality.name,
                "phi_alignment": response.phi_alignment
            })

    def _format_emotion_acknowledgment(self, emotions: Dict[str, float]) -> str:
        """Formate l'acknowledgment émotionnel"""
        if not emotions:
            return ""

        primary = max(emotions.items(), key=lambda x: x[1]) if emotions else ("neutral", 0)
        emotion_words = {
            "joy": "ta joie",
            "sadness": "ta tristesse",
            "anger": "ta frustration",
            "fear": "tes inquiétudes",
            "surprise": "ta surprise",
            "confusion": "ta confusion"
        }
        return emotion_words.get(primary[0], "ce que tu ressens")

    def _identify_primary_emotion(self, emotions: Dict[str, float]) -> str:
        """Identifie l'émotion principale"""
        if not emotions:
            return "neutralité"
        primary = max(emotions.items(), key=lambda x: x[1])
        return primary[0]

    def _get_complementary_emotion(self, emotion: str) -> str:
        """Trouve l'émotion complémentaire"""
        complements = {
            "sadness": "comfort",
            "anger": "understanding",
            "fear": "reassurance",
            "confusion": "clarity",
            "stress": "calm"
        }
        return complements.get(emotion, "support")

    def _convert_to_markdown(self, text: str, analysis: Dict[str, Any]) -> str:
        """Convertit le texte en markdown"""
        # Ajouter des enrichissements markdown
        markdown = text

        # Emphase sur les points importants
        if analysis["urgency"] > 0.7:
            markdown = f"**⚠️ URGENT:** {markdown}"

        # Ajouter des listes si approprié
        if "\n" in markdown:
            lines = markdown.split("\n")
            if len(lines) > 2:
                markdown = "\n".join([f"- {line}" if line else "" for line in lines])

        return markdown

    async def _generate_progress_bar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère une barre de progression"""
        progress = data.get("progress", 0.5)
        return {
            "type": "progress_bar",
            "value": progress,
            "max": 1.0,
            "label": f"{progress*100:.1f}%",
            "color": "green" if progress > 0.7 else "yellow" if progress > 0.3 else "red"
        }

    async def _generate_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un graphique"""
        return {
            "type": "line_chart",
            "data_points": [
                {"x": i, "y": np.sin(i/10) * data.get("complexity", 0.5)}
                for i in range(20)
            ],
            "title": "Analyse temporelle"
        }

    async def _generate_fractal_visualization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère une visualisation fractale"""
        return {
            "type": "fractal",
            "complexity": data.get("complexity", 5),
            "iterations": 100,
            "color_scheme": "phi_gradient"
        }

    async def _generate_phi_spiral(self, phi_value: float) -> Dict[str, Any]:
        """Génère une spirale dorée"""
        return {
            "type": "phi_spiral",
            "phi_value": phi_value,
            "rotations": 3,
            "segments": 50,
            "color": f"hsl({phi_value*360}, 70%, 50%)"
        }

    async def _generate_emotion_map(self, emotions: Dict[str, float]) -> Dict[str, Any]:
        """Génère une carte émotionnelle"""
        return {
            "type": "emotion_map",
            "emotions": emotions,
            "visualization": "radial",
            "colors": {
                "joy": "#FFD700",
                "sadness": "#4169E1",
                "anger": "#DC143C",
                "fear": "#8B008B",
                "surprise": "#FF69B4",
                "confusion": "#708090"
            }
        }

    async def _generate_consciousness_field(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un champ de conscience"""
        return {
            "type": "consciousness_field",
            "intensity": data.get("consciousness_level", 5) / 10,
            "coherence": data.get("coherence", 0.8),
            "nodes": 50,
            "connections": 150
        }

    async def _generate_network_graph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un graphe de réseau"""
        return {
            "type": "network_graph",
            "nodes": data.get("nodes", []),
            "edges": data.get("edges", []),
            "layout": "force_directed"
        }

    async def _generate_fractal_signature(self, context: InterfaceContext) -> str:
        """Génère une signature fractale"""
        # Signature unique basée sur le contexte
        data = f"{context.user_id}_{context.phi_resonance}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _render_html(self, message: MultimodalMessage) -> str:
        """Rend le message en HTML"""
        # Implémentation simplifiée
        html = "<div class='luna-message'>"

        for modality, content in message.content.items():
            html += f"<div class='modality-{modality.name.lower()}'>"
            if modality == CommunicationModality.TEXT:
                html += f"<p>{content}</p>"
            else:
                html += f"<pre>{json.dumps(content, indent=2)}</pre>"
            html += "</div>"

        html += "</div>"
        return html

    def _render_markdown(self, message: MultimodalMessage) -> str:
        """Rend le message en Markdown"""
        md = ""

        for modality, content in message.content.items():
            if modality == CommunicationModality.TEXT:
                md += content + "\n\n"
            elif modality == CommunicationModality.RICH_TEXT:
                md += content.get("markdown", "") + "\n\n"
            else:
                md += f"```json\n{json.dumps(content, indent=2)}\n```\n\n"

        return md

    def _calculate_average_satisfaction(self) -> float:
        """Calcule la satisfaction moyenne"""
        all_scores = []
        for scores in self.interface_metrics["user_satisfaction"].values():
            all_scores.extend(scores)
        return sum(all_scores) / len(all_scores) if all_scores else 0.8


# Module entry point removed - tests moved to tests/test_update01_modules.py
# To run tests: pytest tests/test_update01_modules.py::TestLunaMultimodalInterface -v