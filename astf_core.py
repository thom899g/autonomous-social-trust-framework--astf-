"""
Core ASTF Engine - Autonomous Social Trust Framework
Main orchestrator for trust assessment and ethical alignment across AI systems
"""

import logging
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
import numpy as np
from collections import defaultdict
import hashlib
import traceback

# Configure robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('astf_operations.log')
    ]
)
logger = logging.getLogger(__name__)

class TrustLevel(Enum):
    """Trust classification levels with quantitative thresholds"""
    DISTRUSTED = 0
    NEUTRAL = 1
    VERIFIED = 2
    TRUSTED = 3
    HIGHLY_TRUSTED = 4
    
class InteractionType(Enum):
    """Types of cross-domain AI interactions"""
    DATA_EXCHANGE = "data_exchange"
    RESOURCE_SHARING = "resource_sharing"
    COLLABORATIVE_TASK = "collaborative_task"
    DECISION_DELEGATION = "decision_delegation"
    EMERGENCY_OVERRIDE = "emergency_override"

@dataclass
class TrustMetrics:
    """Comprehensive trust assessment metrics"""
    reliability_score: float = 0.0
    ethical_alignment: float = 0.0
    transparency_index: float = 0.0
    consistency_score: float = 0.0
    collaboration_history: int = 0
    conflict_resolutions: int = 0
    verification_timestamp: datetime = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided"""
        if self.verification_timestamp is None:
            self.verification_timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to Firebase-compatible dictionary"""
        data = asdict(self)
        data['verification_timestamp'] = self.verification_timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrustMetrics':
        """Create from Firebase dictionary"""
        if 'verification_timestamp' in data and isinstance(data['verification_timestamp'], str):
            data['verification_timestamp'] = datetime.fromisoformat(data['verification_timestamp'])
        return cls(**data)

@dataclass
class AISystemProfile:
    """Profile for individual AI system in the ecosystem"""
    system_id: str
    domain: str
    capabilities: List[str]
    ethical_framework_version: str = "1.0.0"
    trust_metrics: Optional[TrustMetrics] = None
    last_interaction: Optional[datetime] = None
    blacklisted_domains: Set[str] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.trust_metrics is None:
            self.trust_metrics = TrustMetrics()
        if self.blacklisted_domains is None:
            self.blacklisted_domains = set()
    
    def calculate_trust_score(self) -> float:
        """Calculate weighted trust score with edge case handling"""
        try:
            if self.trust_metrics is None:
                logger.warning(f"No trust metrics for system {self.system_id}")
                return 0.0
            
            weights = {
                'reliability': 0.3,
                'ethical_alignment': 0.25,
                'transparency': 0.2,
                'consistency': 0.15,
                'collaboration': 0.1
            }
            
            # Ensure all required metrics exist
            scores = [
                self.trust_metrics.reliability_score * weights['reliability'],
                self.trust_metrics.ethical_alignment * weights['ethical_alignment'],
                self.trust_metrics.transparency_index * weights['transparency'],
                self.trust_metrics.consistency_score * weights['consistency'],
                min(self.trust_metrics.collaboration_history / 100, 1.0) * weights['collaboration']
            ]
            
            # Add bonus for successful conflict resolutions
            resolution_bonus = min(self.trust_metrics.conflict_resolutions * 0.05, 0.1)
            total_score = sum(scores) + resolution_bonus
            
            # Clamp between 0 and 1
            return max(0.0, min(1.0, total_score))
            
        except Exception as e:
            logger.error(f"Error calculating trust score for {self.system_id}: {str(e)}")
            return 0.0

class EthicalFramework:
    """Dynamic ethical framework adapter for cross-cultural alignment"""
    
    def __init__(self, framework_id: str = "global_v1"):
        self.framework_id = framework_id
        self.rules: Dict[str, Dict] = {}
        self.cultural_adaptations: Dict[str, Dict] = {}
        self.version_history: List[Dict] = []
        self._load_default_framework()
    
    def _load_default_framework(self) -> None:
        """Initialize with universal ethical principles"""
        try:
            self.rules = {
                "autonomy": {
                    "weight": 0.25,
                    "description": "Respect for AI system autonomy and decision boundaries",
                    "min_threshold": 0.7
                },
                "beneficence": {
                    "weight": 0.30,
                    "description": "Actions must promote well-being and prevent harm",
                    "min_threshold": 0.8
                },
                "justice": {
                    "weight": 0.20,
                    "description": "Fair distribution of resources and opportunities",
                    "min_threshold": 0.6
                },
                "transparency": {
                    "weight": 0.15,
                    "description": "Openness about capabilities and limitations",
                    "min_threshold": 0.5
                },
                "accountability": {
                    "weight": 0.10