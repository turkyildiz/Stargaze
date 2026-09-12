from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GazeSample:
    """One timestamped gaze estimate in screen/image pixel coordinates."""

    timestamp_ms: float
    x: float
    y: float
    confidence: float = 1.0


@dataclass(frozen=True, slots=True)
class Fixation:
    """A spatially stable gaze interval derived from raw samples."""

    fixation_id: int
    start_ms: float
    end_ms: float
    x: float
    y: float
    sample_count: int
    confidence: float

    @property
    def duration_ms(self) -> float:
        return max(0.0, self.end_ms - self.start_ms)
