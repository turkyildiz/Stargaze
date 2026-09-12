# Stargaze

Stargaze is an experimental gaze-mapping platform for studying expert visual search on medical images.

The first milestone is intentionally narrow:

1. ingest timestamped gaze coordinates,
2. identify fixations from the dense raw gaze stream,
3. render each fixation as a pink overlay dot,
4. scale dot diameter by fixation duration,
5. preserve raw samples and fixations for later study/replay.

> Research prototype only. Stargaze is not a diagnostic medical device and should not be used for clinical decision-making.

## Visualization contract

- **Position** = fixation centroid on the displayed image.
- **Diameter** = fixation duration using a logarithmic, capped mapping.
- **Pink** = expert-attention overlay.
- **Raw samples are never discarded** when fixations are derived.
- Repeated visits remain separate fixation events; aggregation is a later visualization option.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
stargaze demo --output demo.png
pytest
```

The demo generates a synthetic gaze trace across a mock radiograph-like canvas, detects fixations, and writes the pink-dot overlay to `demo.png` plus session CSV data.

## Current architecture

```text
raw gaze samples
      |
      v
FixationDetector
      |
      +--> raw_samples.csv
      |
      v
fixation events
      |
      +--> fixations.csv
      |
      v
PinkDotRenderer
      |
      v
overlay/replay visualization
```

## Near-term roadmap

- [x] Core gaze/fixation data model
- [x] Dispersion-based fixation detector
- [x] Duration-sized pink-dot renderer
- [x] CSV session persistence
- [x] Synthetic gaze demo
- [ ] Dual OV9281 camera capture
- [ ] Pupil + corneal-glint detection
- [ ] 9/16-point screen calibration
- [ ] Live transparent desktop overlay
- [ ] Calibration drift/quality metrics
- [ ] DICOM/PACS viewport coordinate mapping
- [ ] Session replay UI and expert comparison

## Why raw gaze and fixations are separate

At 120 Hz, a 20-second read produces roughly 2,400 raw gaze samples. Those samples should remain available for future algorithms. The visible pink-dot study map is based on fixations rather than drawing thousands of identical samples on top of one another.

A fixation can therefore be represented as:

```text
x, y          -> where the expert was looking
duration_ms   -> how long the expert looked there
start/end     -> when it occurred
sample_count  -> supporting raw observations
confidence    -> tracker confidence summary
```

This lets Stargaze later support scan paths, playback, heat maps, revisits, expert-vs-trainee comparisons, and alternative fixation algorithms without recollecting the study.
