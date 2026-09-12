# AGENTS.md — Stargaze implementation contract

This repository is an experimental research platform for measuring and visualizing expert gaze while viewing medical images. Codex and other coding agents should treat this file as the primary implementation contract.

## Product definition

Stargaze records dense gaze samples from a remote eye-tracking rig and converts them into study artifacts:

1. timestamped raw gaze samples,
2. fixation events,
3. a pink-dot overlay in which each fixation's position represents where the expert looked and the dot diameter represents fixation duration,
4. replay, scan-path, heat-map, and comparison views,
5. later, coordinate mapping from monitor space to medical-image space.

Stargaze is a research/education tool. Do not implement diagnostic alerts, lesion recommendations, clinical triage, or autonomous clinical decisions unless a future specification explicitly changes the intended use.

## Core invariant

**Never discard raw acquisition data.** Derived gaze coordinates, fixations, calibration results, overlays, heat maps, and future model outputs must be reproducible from preserved source samples and metadata.

## Implementation order

Implement phases in `docs/ROADMAP.md` in sequence unless a task explicitly says otherwise.

### Phase 0 — foundation
- packaging, linting, typing, tests, CLI
- canonical domain models
- deterministic synthetic datasets
- session storage

### Phase 1 — visualization MVP
- fixation detector
- pink-dot renderer
- scan path
- replay
- heat map
- export PNG/SVG/CSV/JSON

### Phase 2 — camera acquisition
- dual UVC camera abstraction
- independent timestamps plus common monotonic session clock
- dropped-frame accounting
- synchronized frame metadata
- raw recording toggle

### Phase 3 — eye features
- face/eye ROI
- pupil ellipse/center detection
- corneal-glint detection
- binocular confidence
- head-pose estimation
- debug visualization

### Phase 4 — calibration/gaze
- screen geometry model
- calibration target UI
- 9-point and 16-point calibration
- feature-to-screen mapping
- validation points
- drift detection
- confidence/uncertainty estimates

### Phase 5 — desktop live overlay
- transparent click-through pink dot
- optional visibility to subject; research mode may hide overlay from subject while still recording
- multi-monitor support
- recording controls

### Phase 6 — medical image mapping
- viewport abstraction
- screen-to-image transform
- image dimensions, zoom, pan, crop, rotation/flip metadata
- DICOM metadata layer where available
- overlay remains separate from source image pixels

### Phase 7 — study/review app
- session browser
- synchronized replay
- expert comparison
- region-of-interest analysis
- statistics
- exportable research reports/data

## Engineering principles

### Python first
Use Python 3.11+ for research velocity. Prefer:
- numpy
- scipy
- opencv-python
- pydantic/dataclasses where appropriate
- pandas only in analysis/export paths, not in hot loops
- PySide6 or another well-supported desktop UI toolkit if a UI is required

Performance-critical components may later move to C++/CUDA, but only after profiling.

### Time model
Use a monotonic high-resolution clock for relative timing. Persist both:
- session-relative `timestamp_ns`
- wall-clock UTC session start metadata

Do not use wall-clock timestamps for fixation interval math.

### Coordinate conventions
All APIs must state coordinate space explicitly. Use typed structures/enums for:
- camera pixels
- normalized eye ROI
- desktop pixels
- monitor-local pixels
- viewport pixels
- medical-image pixels
- patient coordinates (future)

Never pass naked `(x, y)` tuples across subsystem boundaries without the coordinate space being structurally evident.

### Confidence
Every derived gaze point must include a confidence or validity state. Invalid/missing tracking samples must be represented explicitly, not silently interpolated into valid gaze.

### Fixations
Preserve raw gaze samples. A fixation is a derived event referencing its contributing sample range or sample IDs.

The default first implementation may use I-DT (dispersion threshold), but the interface must allow alternative algorithms such as I-VT later.

### Pink-dot contract
For a fixation:
- center = fixation centroid
- hue = pink by default
- diameter = monotonic function of duration
- default scaling = logarithmic and capped to avoid very long fixations obscuring large regions
- opacity may represent confidence only if explicitly enabled
- source image pixels must never be modified; overlays are composited separately

Repeated visits to the same location remain distinct fixation events. An aggregate view may merge them visually but must never overwrite event-level data.

## Quality gates

Every feature should include tests where meaningful.

Minimum CI gates:
- formatting
- linting
- static typing
- unit tests
- deterministic rendering test or image metadata test where practical

Important numeric algorithms should include synthetic ground-truth tests.

## Accuracy terminology

Keep these separate:
- **accuracy**: angular/positional bias from true target
- **precision**: sample-to-sample dispersion
- **availability**: fraction of time valid gaze is produced
- **latency**: capture-to-coordinate delay
- **calibration residual**: target vs predicted coordinate error

Do not claim a precision/accuracy level unless measured using the validation protocol in `docs/VALIDATION.md`.

## Safety and intended use

This repository must label the software as research-only until a separate regulatory program changes that status.

Do not add features that interpret an X-ray clinically or tell a radiologist what diagnosis to make. FDA guidance distinguishes certain non-device CDS from functions that acquire/process/analyze medical images; analysis of medical images for clinical relevance can fall under medical-device oversight. Keep the MVP focused on observational gaze research.

Near-IR illumination must be treated as a hardware safety concern. Software must not imply an arbitrary illuminator is safe. Hardware documentation must require independent photobiological/ocular safety verification before prolonged human exposure.

## Privacy

Avoid patient identifiers in generated demo data. Real study mode should support pseudonymous session IDs. Do not require cloud storage. Default architecture should be local-first.

## Documentation

When changing architecture or schemas, update the relevant document under `docs/` in the same PR.

## Definition of done

A feature is not done merely because a UI exists. It is done when:
1. behavior is implemented,
2. tests cover the core behavior,
3. failure states are explicit,
4. data is persisted reproducibly where applicable,
5. docs reflect the actual implementation.
