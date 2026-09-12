from stargaze.fixations import FixationDetector, FixationDetectorConfig
from stargaze.models import Fixation, GazeSample
from stargaze.render import fixation_diameter_px


def test_stable_samples_become_fixation() -> None:
    samples = [
        GazeSample(timestamp_ms=i * 10.0, x=500 + (i % 2), y=400, confidence=0.99)
        for i in range(31)
    ]
    detector = FixationDetector(
        FixationDetectorConfig(min_duration_ms=100, dispersion_px=10)
    )

    fixations = detector.detect(samples)

    assert len(fixations) == 1
    assert fixations[0].duration_ms == 300.0
    assert fixations[0].sample_count == 31


def test_low_confidence_samples_are_ignored() -> None:
    samples = [
        GazeSample(timestamp_ms=i * 10.0, x=500, y=400, confidence=0.1)
        for i in range(31)
    ]
    detector = FixationDetector(FixationDetectorConfig(min_confidence=0.5))

    assert detector.detect(samples) == []


def test_longer_fixation_gets_larger_dot() -> None:
    short = fixation_diameter_px(150)
    medium = fixation_diameter_px(500)
    long = fixation_diameter_px(1500)

    assert short < medium < long


def test_dot_size_is_capped() -> None:
    assert fixation_diameter_px(10_000_000) <= 54
