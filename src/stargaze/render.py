from __future__ import annotations

import math

import cv2
import numpy as np

from .models import Fixation

# OpenCV uses BGR. This is intentionally a vivid research-overlay pink.
PINK_BGR = (180, 80, 255)


def fixation_diameter_px(
    duration_ms: float,
    *,
    min_px: int = 8,
    max_px: int = 54,
    scale: float = 16.0,
) -> int:
    """Map dwell time to dot diameter without letting long fixations dominate.

    A logarithmic mapping preserves visible differences among short fixations
    while capping unusually long dwell events.
    """

    duration_ms = max(0.0, duration_ms)
    diameter = min_px + scale * math.log10(1.0 + duration_ms / 100.0)
    return int(round(min(max_px, max(min_px, diameter))))


def render_fixations(
    image: np.ndarray,
    fixations: list[Fixation],
    *,
    alpha: float = 0.58,
    show_sequence: bool = False,
) -> np.ndarray:
    """Render duration-sized pink fixation dots on a copy of an image."""

    output = image.copy()
    overlay = image.copy()

    for fixation in fixations:
        diameter = fixation_diameter_px(fixation.duration_ms)
        radius = max(2, diameter // 2)
        center = (int(round(fixation.x)), int(round(fixation.y)))
        cv2.circle(overlay, center, radius, PINK_BGR, thickness=-1, lineType=cv2.LINE_AA)

        if show_sequence:
            cv2.putText(
                overlay,
                str(fixation.fixation_id),
                (center[0] + radius + 2, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                PINK_BGR,
                1,
                cv2.LINE_AA,
            )

    cv2.addWeighted(overlay, alpha, output, 1.0 - alpha, 0.0, output)
    return output
