# Codex execution plan

This file translates the product blueprint into implementation batches that Codex can execute with minimal ambiguity.

## Ground rules for Codex

Before coding:
1. read `AGENTS.md`
2. read `docs/ARCHITECTURE.md`
3. read `docs/DATA_MODEL.md`
4. read `docs/VISUALIZATION.md`
5. read `docs/VALIDATION.md`
6. check `docs/ROADMAP.md` and select the earliest incomplete milestone

For every batch:
- keep changes scoped
- add/update tests
- update docs if implementation differs from design
- do not introduce clinical decision support behavior
- do not destroy raw data
- do not burn overlays into medical source images

## Batch 1 — repository hardening

Implement M0 completely.

Deliverables:
- lint/format/type/test configuration
- CI workflow
- deterministic demo seed
- clean install instructions

Completion test:
```bash
pip install -e ".[dev]"
ruff check .
pytest
```
plus selected type checker.

## Batch 2 — domain model refactor

Implement M1.

Focus on explicit coordinate spaces and schema versioning.

Deliverables:
- domain package
- typed IDs/models
- session reader/writer
- round-trip tests

Do not add camera dependencies yet.

## Batch 3 — visualization engine

Implement M2 fully.

Must produce:
- raw sample plot
- fixation-dot plot
- scan path
- heat map
- deterministic PNG/SVG exports where supported
- timeline/replay abstraction independent of GUI

Add golden/synthetic tests for dot positions and sizes.

## Batch 4 — camera abstraction

Implement M3 with simulated camera first, then OpenCV UVC.

Required interfaces:

```python
class CameraSource(Protocol):
    def start(self) -> None: ...
    def read(self) -> CameraFrame: ...
    def stop(self) -> None: ...
    def capabilities(self) -> CameraCapabilities: ...
```

Do not expose raw `cv2.VideoCapture` outside adapter package.

Add fake source for tests.

## Batch 5 — eye-feature research pipeline

Implement M4.

Start with offline images/video fixtures.

Pipeline stages should be separately testable:
- ROI extraction
- pupil segmentation
- ellipse fitting
- glint candidates
- glint selection
- confidence

Build debug frame renderer that annotates features.

Do not couple feature detector to calibration UI.

## Batch 6 — movement/head pose

Implement M5.

Head-pose provider must be replaceable. Store pose features and tracking-quality states.

## Batch 7 — calibration application

Implement M6.

Build model fitting before GUI, with synthetic tests. Then implement fullscreen target presentation.

Required model API:

```python
class GazeCalibrationModel(Protocol):
    def fit(self, observations): ...
    def predict(self, features): ...
    def serialize(self): ...
```

Baseline model must be simple and explainable. Add more complex estimator only if validation improves.

## Batch 8 — end-to-end gaze service

Implement M7.

Wire:

```text
camera -> eye features -> binocular fusion -> calibration -> gaze sample -> recorder
```

Instrument timing for every stage.

## Batch 9 — overlay and recording UI

Implement M8.

Windows should be first-class because typical radiology workstations are Windows, but keep core logic portable.

Ensure click-through overlay mode cannot intercept normal viewer interaction when enabled.

## Batch 10 — study review desktop UI

Implement M9.

Researcher workflow:
1. choose session
2. choose/recover background image
3. inspect fixation dots
4. scrub replay
5. switch raw/fixation/scanpath/heatmap views
6. select fixation for metadata
7. export

Keep UI responsive by moving heavy loading/render preprocessing off UI thread.

## Batch 11 — image coordinate mapping

Implement M10.

Build transform library with exhaustive unit tests before integrating any PACS/viewer-specific code.

## Batch 12 — DICOM research adapter

Implement M11 using optional dependencies.

Rules:
- read-only by default
- no original-file mutation
- gaze overlay stored separately
- avoid PHI in test fixtures

## Batch 13 — multi-expert analysis

Implement M12.

Start with descriptive metrics only.

Suggested metrics:
- total dwell per region
- fixation count
- revisit count
- coverage fraction
- first-fixation latency
- scan-path length
- pairwise spatial similarity with documented formula

Do not imply clinical superiority from a metric without a study design.

## Batch 14 — study metadata and retention

Implement M13.

Add pseudonymous participant/study/case identifiers and deletion/export utilities.

## PR structure recommendation

Prefer one PR per batch or coherent sub-batch.

PR description should contain:
- milestone/task IDs
- what changed
- tests run
- known limitations
- screenshots/exports when visual behavior changes
- measured performance only if benchmark methodology is included

## Test fixtures to build early

Create synthetic fixtures:
- stationary gaze cluster
- two fixations separated by saccade
- fixation + blink gap
- repeated visit
- dense full-screen scan
- edge/corner gaze
- low-confidence samples
- deterministic calibration targets
- viewport transforms

Later add de-identified/non-clinical image fixtures. Avoid committing real patient data.

## Coding decisions Codex should not improvise

These are fixed unless documentation is deliberately changed:
- pink dots encode fixation duration by diameter
- raw gaze remains preserved
- repeated visits are separate events
- monotonic timestamps drive timing
- overlay is a separate layer
- research-only intended use
- local-first architecture
- coordinate spaces are explicit
- held-out points validate calibration

## What Codex may choose

Codex may select reasonable implementation details for:
- exact Python UI toolkit if existing dependencies do not constrain it
- exact lint/type tooling
- algorithm internals behind documented interfaces
- file organization refinements
- bounded queue implementation
- exact logarithmic visualization constants, if config-driven and tested

## Stop conditions

Codex should stop and document rather than invent when:
- a hardware capability is unavailable
- a camera driver does not expose requested controls
- physical display dimensions are unknown for mm/degree calculations
- IR safety would require assuming an unknown optical output
- a clinical feature would cross beyond the research scope

## Final MVP demonstration

The first complete demonstration should be:

1. launch Stargaze
2. identify two cameras
3. calibrate subject to one monitor
4. display a static research image
5. subject views normally
6. record gaze at target cadence
7. stop recording
8. open review
9. show hundreds of pink fixation dots across the image
10. larger dots visibly correspond to longer dwell
11. scrub time to replay search order
12. switch to heat map and scan path
13. inspect a selected fixation's raw metadata
14. export overlay and event data
15. rerun the same session through the fixation engine and obtain deterministic derived output for the same configuration
