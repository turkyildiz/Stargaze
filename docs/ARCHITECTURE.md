# Stargaze architecture

## Objective

Stargaze is a modular gaze-research platform for experts viewing medical images. The system should work first with synthetic gaze, then commodity USB global-shutter cameras, then custom hardware later without rewriting the research pipeline.

## System diagram

```text
                 +----------------------+
                 |   Camera Left/Right  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Acquisition Service  |
                 | frames + timestamps  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Eye Feature Engine   |
                 | pupil/glint/headpose |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Gaze Estimator       |
                 | calibration model    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Gaze Sample Stream   |
                 | x/y/confidence/time  |
                 +-----+-----------+----+
                       |           |
                       v           v
              +-------------+   +----------------+
              | Fixations   |   | Raw recorder   |
              +------+------+   +----------------+
                     |
                     v
              +--------------------+
              | Visualization      |
              | pink dots/replay   |
              | scan path/heatmap  |
              +---------+----------+
                        |
                        v
              +--------------------+
              | Study Review       |
              | compare/export     |
              +--------------------+
```

## Runtime components

### 1. Acquisition
Responsibilities:
- discover configured UVC cameras
- negotiate resolution/FPS/exposure
- capture frames independently
- assign monotonic timestamps immediately at capture receipt
- record sequence number and dropped-frame estimates
- publish immutable `CameraFrameMeta`
- optionally record raw video/frames for offline reprocessing

The rest of the system must not depend directly on OpenCV `VideoCapture`; hide camera implementation behind an interface.

### 2. Eye feature extraction
Input: camera frame(s).
Output per eye/camera:
- eye ROI
- pupil center
- pupil ellipse axes/orientation
- glint candidates and selected glint(s)
- eyelid/occlusion metric
- feature confidence
- optional head pose

Initial algorithm may be classical CV. Define the interface so a neural detector can replace it later.

### 3. Binocular fusion
Do not assume both eyes are always valid.

States:
- binocular valid
- left-only
- right-only
- invalid

Fusion should provide:
- combined feature vector
- validity mask
- confidence

### 4. Calibration service
Owns:
- monitor geometry
- calibration target sequence
- sample collection windows
- outlier rejection
- model fit
- validation targets
- calibration quality
- model serialization

Calibration is a first-class artifact and must be linked to every gaze session.

### 5. Gaze estimator
Input: synchronized eye features + calibration model.
Output: `GazeSample` in desktop or monitor space.

Must include:
- timestamp_ns
- x_px/y_px
- coordinate space
- confidence
- validity
- source eye validity
- uncertainty estimate where available
- calibration ID

### 6. Fixation engine
Consumes ordered `GazeSample`s.

Default: I-DT-like dispersion algorithm.

The fixation event must retain:
- fixation ID
- start/end timestamps
- duration
- centroid
- dispersion
- average/min confidence
- sample count
- first/last source sample IDs
- optional full list/reference of sample IDs

### 7. Visualization service
Views are derived, never authoritative.

Modes:
- live gaze cursor
- raw samples
- fixation dots
- scan path
- heat map
- time-window playback
- aggregate dwell
- compare multiple experts

Pink fixation rule:

```text
screen position = fixation centroid
dot diameter     = f(duration_ms)
```

Recommended default:

```python
D = clamp(D_MIN + K * log1p(duration_ms / TAU), D_MIN, D_MAX)
```

Exact constants belong in configurable theme/settings and tests.

### 8. Session recorder
The session directory is append-oriented and reproducible.

Suggested layout:

```text
sessions/<session_id>/
  manifest.json
  calibration.json
  raw_gaze.parquet-or-csv
  fixations.parquet-or-csv
  camera_meta.csv
  events.jsonl
  screenshots/            # optional
  raw_video/              # optional
  exports/
```

Do not require raw image/video recording for every study; make it configurable because of storage/privacy.

### 9. Medical-image viewport mapping
Keep separate from generic gaze tracking.

Define a `ViewportTransform` mapping:

```text
desktop px -> monitor-local px -> application viewport px -> image px
```

It must model:
- viewport rectangle
- image source width/height
- rendered width/height
- aspect-fit or aspect-fill behavior
- pan
- zoom
- crop
- rotation
- horizontal/vertical flip
- high-DPI scaling

Medical image content must not be altered merely to render attention overlays.

## Processes/threads

Avoid running camera capture, heavy CV, UI, and disk writes on one event loop.

Suggested prototype:
- camera thread/process per device
- processing worker
- UI main thread
- writer queue/thread

Queues must be bounded. Under load, define whether to drop frames or increase latency. For live gaze, favor bounded latency and explicitly record dropped frames.

## Dependency direction

```text
ui -> application services -> domain <- adapters
```

Domain models/algorithms must not import Qt, OpenCV UI, DICOM viewer SDKs, or OS-specific overlay code.

## Suggested package structure

```text
src/stargaze/
  domain/
    models.py
    coordinates.py
    events.py
  acquisition/
    base.py
    uvc.py
    synchronization.py
  vision/
    eyes.py
    pupil.py
    glint.py
    head_pose.py
    fusion.py
  calibration/
    targets.py
    fitting.py
    validation.py
    drift.py
  gaze/
    estimator.py
    filters.py
  fixation/
    base.py
    idt.py
    ivt.py
  visualization/
    dots.py
    scanpath.py
    heatmap.py
    replay.py
  viewport/
    transforms.py
    dicom.py
  storage/
    session.py
    schemas.py
  ui/
    calibration.py
    overlay.py
    review.py
  cli.py
```

## Configuration

Use explicit config models, not global constants.

Categories:
- camera
- eye detection
- calibration
- gaze filtering
- fixation
- visualization
- storage
- privacy

Persist the effective configuration into each session manifest.

## Failure handling

Tracking can fail routinely. Expected states include:
- camera disconnected
- one eye missing
- glint missing
- blink
- head outside track box
- calibration expired/drifted
- target outside monitor bounds
- disk writer behind

The system should emit structured events for these conditions rather than crash or fabricate valid gaze.

## Security/privacy default

- local-only processing by default
- no telemetry unless explicitly enabled
- pseudonymous participant IDs
- no patient identifiers required for core pipeline
- optional encryption is future work

## Performance targets

Prototype goals, not claims:
- acquisition target: 120 Hz where hardware supports it
- live visualization target: <= 50 ms median pipeline latency after optimization
- no unbounded queue growth
- raw sample persistence loss: zero unless explicitly documented by dropped acquisition frames

Accuracy targets live in `VALIDATION.md` and must be measured rather than assumed.
