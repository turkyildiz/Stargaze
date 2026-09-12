from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from .fixations import FixationDetector, FixationDetectorConfig
from .models import GazeSample
from .render import render_fixations
from .session import save_fixations, save_raw_samples


def _synthetic_session(width: int, height: int, hz: int = 120) -> list[GazeSample]:
    rng = np.random.default_rng(42)
    # (normalized x, normalized y, fixation duration ms)
    path = [
        (0.39, 0.22, 180),
        (0.59, 0.24, 310),
        (0.35, 0.37, 220),
        (0.62, 0.39, 760),
        (0.45, 0.52, 280),
        (0.66, 0.57, 430),
        (0.37, 0.67, 190),
        (0.57, 0.72, 980),
        (0.49, 0.82, 350),
    ]
    dt = 1000.0 / hz
    timestamp = 0.0
    samples: list[GazeSample] = []

    for nx, ny, duration in path:
        count = max(1, int(duration / dt))
        cx, cy = nx * width, ny * height
        for _ in range(count):
            samples.append(
                GazeSample(
                    timestamp_ms=timestamp,
                    x=float(cx + rng.normal(0, 4.0)),
                    y=float(cy + rng.normal(0, 4.0)),
                    confidence=float(rng.uniform(0.91, 0.995)),
                )
            )
            timestamp += dt

        # Synthetic fast transition/saccade. Its large dispersion should keep it
        # from being classified as a fixation.
        timestamp += 35.0

    return samples


def _demo_canvas(width: int = 1400, height: int = 1700) -> np.ndarray:
    canvas = np.full((height, width, 3), 28, dtype=np.uint8)
    # A deliberately non-clinical, radiograph-like silhouette for testing.
    cv2.ellipse(canvas, (510, 820), (285, 650), 3, 0, 360, (72, 72, 72), -1)
    cv2.ellipse(canvas, (890, 820), (285, 650), -3, 0, 360, (72, 72, 72), -1)
    cv2.rectangle(canvas, (670, 180), (730, 1460), (48, 48, 48), -1)
    return canvas


def run_demo(output: Path) -> None:
    canvas = _demo_canvas()
    samples = _synthetic_session(canvas.shape[1], canvas.shape[0])
    detector = FixationDetector(
        FixationDetectorConfig(min_duration_ms=100.0, dispersion_px=45.0)
    )
    fixations = detector.detect(samples)
    rendered = render_fixations(canvas, fixations, show_sequence=True)

    output.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output), rendered):
        raise RuntimeError(f"Could not write {output}")

    session_dir = output.with_suffix("")
    save_raw_samples(session_dir / "raw_samples.csv", samples)
    save_fixations(session_dir / "fixations.csv", fixations)

    print(f"Raw samples: {len(samples)}")
    print(f"Fixations: {len(fixations)}")
    print(f"Overlay: {output}")
    print(f"Session data: {session_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="stargaze")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="Generate a synthetic fixation overlay")
    demo.add_argument("--output", type=Path, default=Path("demo.png"))

    args = parser.parse_args()
    if args.command == "demo":
        run_demo(args.output)


if __name__ == "__main__":
    main()
