from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean

from .models import Fixation, GazeSample


@dataclass(frozen=True, slots=True)
class FixationDetectorConfig:
    """Configuration for an I-DT style dispersion fixation detector."""

    min_duration_ms: float = 100.0
    dispersion_px: float = 45.0
    min_confidence: float = 0.5


class FixationDetector:
    """Detect fixations while preserving the original dense gaze stream.

    This deliberately uses a transparent I-DT style algorithm for the MVP.
    Hardware validation will determine the final thresholds/model.
    """

    def __init__(self, config: FixationDetectorConfig | None = None) -> None:
        self.config = config or FixationDetectorConfig()

    @staticmethod
    def _dispersion(samples: list[GazeSample]) -> float:
        if not samples:
            return 0.0
        xs = [sample.x for sample in samples]
        ys = [sample.y for sample in samples]
        return (max(xs) - min(xs)) + (max(ys) - min(ys))

    def detect(self, samples: list[GazeSample]) -> list[Fixation]:
        valid = sorted(
            (s for s in samples if s.confidence >= self.config.min_confidence),
            key=lambda sample: sample.timestamp_ms,
        )
        fixations: list[Fixation] = []
        i = 0

        while i < len(valid):
            j = i
            while (
                j < len(valid)
                and valid[j].timestamp_ms - valid[i].timestamp_ms
                < self.config.min_duration_ms
            ):
                j += 1

            if j >= len(valid):
                break

            window = valid[i : j + 1]
            if self._dispersion(window) > self.config.dispersion_px:
                i += 1
                continue

            k = j + 1
            while k < len(valid):
                candidate = valid[i : k + 1]
                if self._dispersion(candidate) > self.config.dispersion_px:
                    break
                k += 1

            cluster = valid[i:k]
            fixations.append(
                Fixation(
                    fixation_id=len(fixations) + 1,
                    start_ms=cluster[0].timestamp_ms,
                    end_ms=cluster[-1].timestamp_ms,
                    x=fmean(sample.x for sample in cluster),
                    y=fmean(sample.y for sample in cluster),
                    sample_count=len(cluster),
                    confidence=fmean(sample.confidence for sample in cluster),
                )
            )
            i = k

        return fixations
