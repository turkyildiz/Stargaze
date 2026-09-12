"""Stargaze gaze-research toolkit."""

from .models import Fixation, GazeSample
from .fixations import FixationDetector, FixationDetectorConfig

__all__ = [
    "Fixation",
    "GazeSample",
    "FixationDetector",
    "FixationDetectorConfig",
]
