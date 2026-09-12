# Stargaze roadmap and Codex task breakdown

This document is intentionally implementation-oriented. Complete milestones in order unless a dependency is already satisfied.

## M0 — repository quality baseline

### Tasks
- [ ] Add Ruff config and formatting command.
- [ ] Add MyPy or Pyright configuration.
- [ ] Add pytest coverage configuration.
- [ ] Add GitHub Actions CI for Python 3.11/3.12.
- [ ] Ensure `stargaze demo` remains deterministic with seed support.
- [ ] Add architecture-level smoke test.

### Acceptance criteria
- clean checkout installs with `pip install -e ".[dev]"`
- lint/type/test workflow passes
- no test depends on a physical camera

## M1 — canonical domain and storage

### Tasks
- [ ] Create explicit coordinate-space types.
- [ ] Finalize `GazeSample`, `Fixation`, `Calibration`, `MonitorGeometry`, `CameraFrameMeta`, `SessionManifest`.
- [ ] Add version fields to persisted schemas.
- [ ] Add UUIDs/IDs for sessions, calibrations, samples, fixations.
- [ ] Implement append-safe session writer.
- [ ] Add JSONL/CSV first; structure code for Parquet later.
- [ ] Add session reader with schema/version validation.

### Acceptance criteria
- a session can round-trip without numeric/time changes
- malformed/unsupported schema versions fail clearly
- each fixation can be traced back to a source sample range

## M2 — fixation analytics and visualizations

### Tasks
- [ ] Harden I-DT implementation.
- [ ] Add configurable minimum fixation duration and dispersion threshold.
- [ ] Add invalid-sample gap behavior.
- [ ] Add scan-path renderer.
- [ ] Add raw-sample renderer.
- [ ] Add heat-map renderer.
- [ ] Add fixation-dot renderer using duration-scaled pink dots.
- [ ] Add optional aggregate dwell view.
- [ ] Add time-window filtering.
- [ ] Add PNG and SVG export.
- [ ] Add replay timeline abstraction.

### Acceptance criteria
Synthetic trace with known fixations produces centroids/durations inside declared tolerances.

Pink-dot renderer must satisfy:
- longer duration => never smaller diameter
- min/max cap honored
- source image unchanged
- repeated visits preserved as separate dots in event view

## M3 — dual-camera acquisition

### Tasks
- [ ] Define `CameraSource` protocol/ABC.
- [ ] Implement OpenCV UVC adapter.
- [ ] Enumerate cameras and select by stable descriptor where platform permits.
- [ ] Configure target 1280x800 / 120 FPS when supported.
- [ ] Add actual FPS reporting.
- [ ] Add sequence numbers and timestamp_ns.
- [ ] Detect/drop accounting.
- [ ] Add bounded frame queues.
- [ ] Add raw-video recording option.
- [ ] Build side-by-side debug preview.

### Acceptance criteria
- two cameras can stream simultaneously for 30 minutes without unbounded memory growth
- observed FPS, dropped frames, and latency stats available
- disconnect is handled without corrupting the session

## M4 — eye feature extraction

### Tasks
- [ ] Detect/track face and both eye ROIs.
- [ ] Implement grayscale/contrast preprocessing suitable for NIR.
- [ ] Implement pupil segmentation and ellipse fitting.
- [ ] Reject impossible pupil geometry.
- [ ] Implement bright/dark pupil configurable mode if useful.
- [ ] Implement corneal-glint candidate detection.
- [ ] Pair/select glints robustly.
- [ ] Add blink/occlusion state.
- [ ] Add feature confidence.
- [ ] Add visual debugger showing pupil ellipse, centers, glints, eye ROI.

### Acceptance criteria
Offline labeled test frames demonstrate measurable pupil/glint detection performance. Do not claim gaze accuracy at this stage.

## M5 — head pose / movement robustness

### Tasks
- [ ] Add facial landmarks/head-pose estimation.
- [ ] Record yaw/pitch/roll and approximate translation features.
- [ ] Include head features in calibration vector.
- [ ] Detect when user exits calibrated track box.
- [ ] Add tracking quality state machine.

### Acceptance criteria
Moderate head movement changes confidence/validity appropriately rather than silently producing extreme coordinates.

## M6 — calibration

### Tasks
- [ ] Enumerate monitor geometry and DPI scaling.
- [ ] Build fullscreen calibration UI.
- [ ] Implement 9-point pattern.
- [ ] Implement 16-point pattern.
- [ ] At each target: settle interval + sample interval.
- [ ] Reject blinks/outliers/low confidence.
- [ ] Extract robust feature summary per target.
- [ ] Implement baseline polynomial mapping.
- [ ] Add ridge regression option.
- [ ] Add gradient-boosted or compact ML mapping only if validation improves.
- [ ] Serialize model + feature definition + monitor geometry.
- [ ] Add validation points not used for fitting.

### Acceptance criteria
Calibration UI reports validation error in pixels, millimeters (when physical display dimensions known), and degrees (when viewing distance is known/estimated).

No calibration is labeled "good" solely because fit error is small; use held-out validation targets.

## M7 — live gaze service

### Tasks
- [ ] Fuse left/right eye feature streams.
- [ ] Apply calibration model.
- [ ] Produce `GazeSample` at acquisition cadence.
- [ ] Add optional light temporal filtering with bounded latency.
- [ ] Preserve unfiltered coordinates too.
- [ ] Compute confidence/validity.
- [ ] Add uncertainty estimate based on validation residual + current feature quality.
- [ ] Add calibration drift check.

### Acceptance criteria
Synthetic and physical-target validation shows no hidden clipping/interpolation. Missing eye data is explicit.

## M8 — live overlay

### Tasks
- [ ] Transparent always-on-top overlay window.
- [ ] Click-through option.
- [ ] Multi-monitor support.
- [ ] Small live pink cursor mode.
- [ ] Hidden-from-subject recording mode.
- [ ] Configurable dot opacity/diameter.
- [ ] Recording indicator separate from diagnostic image area when possible.
- [ ] Hotkeys/start-stop controls.

### Acceptance criteria
Overlay must not alter or save over original medical image pixels.

## M9 — review application

### Tasks
- [ ] Open session.
- [ ] Load background image/screenshot supplied for research.
- [ ] Render raw samples.
- [ ] Render fixation dots.
- [ ] Render scan path with ordering.
- [ ] Playback timeline.
- [ ] Filter by time/confidence/duration.
- [ ] Toggle revisits.
- [ ] Aggregate dwell mode.
- [ ] Export static image + CSV/JSON.
- [ ] Show session quality metrics.

### Acceptance criteria
A researcher can reproduce an export from the same session/config with deterministic coordinates and dot sizes.

## M10 — viewport/image coordinate mapping

### Tasks
- [ ] Define viewport rectangle capture/API.
- [ ] Implement aspect-fit transform.
- [ ] Implement zoom/pan transforms.
- [ ] Implement crop/rotation/flip.
- [ ] Handle OS high-DPI scaling.
- [ ] Convert gaze/fixation centroid from desktop px to source image px.
- [ ] Record transform state with timestamp.

### Acceptance criteria
Known test points round-trip screen<->image within <=1 px numerical transform error (excluding eye-tracker error).

## M11 — DICOM-aware research support

### Tasks
- [ ] Add pydicom optional dependency.
- [ ] Read de-identified research DICOM metadata.
- [ ] Preserve SOP/Series identifiers only when permitted by study configuration.
- [ ] Map fixation to source image pixel coordinates.
- [ ] Future: patient-space coordinate support for modalities where appropriate.
- [ ] Never burn gaze annotations into original DICOM by default.

### Acceptance criteria
Opening/exporting research overlays leaves original DICOM byte content untouched.

## M12 — multi-expert analysis

### Tasks
- [ ] Normalize sessions to same image coordinate system.
- [ ] Overlay expert A/B/C.
- [ ] Compute dwell distribution per ROI.
- [ ] Compute coverage map.
- [ ] Compute revisit counts.
- [ ] Compute scan-path metrics.
- [ ] Add inter-expert similarity metrics with documented definitions.
- [ ] Keep inferential statistics separate from descriptive visualization.

## M13 — study management

### Tasks
- [ ] participant pseudonym
- [ ] study ID
- [ ] case ID
- [ ] operator notes
- [ ] consent/IRB metadata field hooks (not legal workflow)
- [ ] export manifest
- [ ] data retention/deletion utility

## M14 — hardware productization (later)

Do not start until software/optics research proves the approach.

Potential tasks:
- custom enclosure
- fixed camera baseline
- controlled NIR LED board
- optical filters
- embedded compute decision
- electrical/thermal design
- calibrated camera intrinsics
- hardware synchronization
- formal eye-safety verification

## Non-goals for first implementation

Do not spend MVP time on:
- lesion detection
- diagnosis prediction
- clinical alarms
- PACS write-back
- cloud deployment
- custom PCB
- billing/user accounts
- autonomous clinical recommendations

## Definition of MVP

A successful MVP allows a subject to:
1. calibrate on a monitor,
2. view a static medical image naturally,
3. produce valid gaze samples,
4. derive fixations,
5. save the entire session,
6. review an overlay where hundreds of fixation events can be explored and each pink dot's diameter encodes fixation duration,
7. replay the search sequence over time.
