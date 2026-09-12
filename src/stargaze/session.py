from __future__ import annotations

import csv
from pathlib import Path

from .models import Fixation, GazeSample


def save_raw_samples(path: str | Path, samples: list[GazeSample]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp_ms", "x", "y", "confidence"])
        for sample in samples:
            writer.writerow([sample.timestamp_ms, sample.x, sample.y, sample.confidence])


def save_fixations(path: str | Path, fixations: list[Fixation]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "fixation_id",
                "start_ms",
                "end_ms",
                "duration_ms",
                "x",
                "y",
                "sample_count",
                "confidence",
            ]
        )
        for fixation in fixations:
            writer.writerow(
                [
                    fixation.fixation_id,
                    fixation.start_ms,
                    fixation.end_ms,
                    fixation.duration_ms,
                    fixation.x,
                    fixation.y,
                    fixation.sample_count,
                    fixation.confidence,
                ]
            )
