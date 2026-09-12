# Stargaze

Stargaze is an experimental gaze-mapping platform for studying expert visual search on medical images.

The first milestone is intentionally narrow:

1. ingest timestamped gaze coordinates,
2. identify fixations from the dense raw gaze stream,
3. render each fixation as a pink overlay dot,
4. scale dot diameter by fixation duration,
5. preserve raw samples and fixations for later study/replay.

> Research prototype only. Stargaze is not a diagnostic medical device and should not be used for clinical decision-making.

## Codex: start here

The repository now contains a full implementation blueprint.

1. [`AGENTS.md`](AGENTS.md) — primary implementation contract and non-negotiable rules.
2. [`docs/CODEX_EXECUTION.md`](docs/CODEX_EXECUTION.md) — coding batches Codex should execute in order.
3. [`docs/ROADMAP.md`](docs/ROADMAP.md) — complete milestone checklist and acceptance criteria.
4. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — subsystem architecture and package layout.
5. [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — canonical schemas, timestamps, coordinate spaces, persistence.
6. [`docs/VISUALIZATION.md`](docs/VISUALIZATION.md) — pink-dot, replay, scan-path, heat-map, and comparison behavior.
7. [`docs/HARDWARE.md`](docs/HARDWARE.md) — dual-camera prototype assumptions and future hardware path.
8. [`docs/VALIDATION.md`](docs/VALIDATION.md) — accuracy, precision, latency, drift, and calibration validation protocol.
9. [`docs/RESEARCH_SCOPE.md`](docs/RESEARCH_SCOPE.md) — research-only clinical boundary, privacy, display, and NIR safety notes.

Codex should read `AGENTS.md` first and implement the earliest incomplete milestone in `docs/ROADMAP.md`.

## Visualization contract

- **Position** = fixation centroid on the displayed image.
- **Diameter** = fixation duration using a logarithmic, capped mapping.
- **Pink** = expert-attention overlay.
- **Raw samples are never discarded** when fixations are derived.
- Repeated visits remain separate fixation events; aggregation is a later visualization option.

Experts may inspect nearly the entire medical image, so hundreds of fixation events and thousands of raw gaze samples per case are expected. The review tooling must therefore support filtering, time playback, scan paths, and dense visualization rather than assuming sparse annotations.

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

## Target architecture

```text
Dual eye cameras
      |
      v
frame acquisition + timestamps
      |
      v
pupil + corneal glint + head pose
      |
      v
calibration / gaze estimator
      |
      v
raw gaze stream --------------------> immutable session recorder
      |
      v
fixation detector
      |
      +--> pink fixation dots
      +--> scan path
      +--> heat map
      +--> timed replay
      |
      v
screen/viewport/image coordinate mapping
      |
      v
research review + multi-expert analysis
```

## Current status

Initial scaffold exists for:

- [x] Python package/repository initialization
- [x] Core gaze/fixation model foundation
- [x] Dispersion-based fixation concept
- [x] Duration-sized pink-dot renderer concept
- [x] CSV session persistence concept
- [x] Synthetic gaze demo concept
- [x] Full architecture and Codex execution specification
- [ ] Repository CI/lint/type hardening
- [ ] Canonical schema/coordinate-space refactor
- [ ] Complete visualization engine
- [ ] Dual OV9281/UVC camera capture
- [ ] Pupil + corneal-glint detection
- [ ] Head-pose compensation
- [ ] 9/16-point screen calibration
- [ ] Live transparent desktop overlay
- [ ] Calibration drift/quality metrics
- [ ] Medical-image viewport coordinate mapping
- [ ] Session replay UI and expert comparison

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the authoritative sequence.

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

This lets Stargaze later support scan paths, playback, heat maps, revisits, expert-vs-trainee comparisons, alternative fixation algorithms, and reprocessing without recollecting the study.
