"""
CLAR - VR AI-based tools to support clothing based design fit look and feel
"""

__version__ = "0.1.0"
__author__ = "Tapsprofile"

from .vr.interface import VRInterface
from .ai.fit_analyzer import FitAnalyzer
from .design.customizer import DesignCustomizer
from .ai.look_feel_assessor import LookFeelAssessor

__all__ = [
    "VRInterface",
    "FitAnalyzer",
    "DesignCustomizer",
    "LookFeelAssessor",
]
