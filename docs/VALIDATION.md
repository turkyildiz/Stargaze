# Stargaze validation protocol

## Why this exists

Eye-tracker performance must be measured end-to-end. Camera specifications, frame rate, or calibration fit do not establish actual gaze accuracy.

## Metrics

Report these separately:

### Accuracy
Distance between known target location and estimated gaze center.

Report:
- pixels
- millimeters on screen when display geometry is known
- degrees of visual angle when viewing distance is known

For small angles:

```text
angle_deg ≈ atan(error_mm / viewing_distance_mm) * 180/pi
```

### Precision
Within-fixation sample dispersion.

Report at least one clearly defined metric such as:
- RMS sample-to-centroid distance
- SD horizontal/vertical
- BCEA if later added

### Availability
Fraction of study time/samples with valid gaze.

### Latency
Capture-to-render or capture-to-gaze-output latency.

### Drift
Change in error over time after initial calibration.

## Calibration validation design

Do not evaluate calibration solely on points used to fit the model.

Recommended sequence:
1. fit using 9 or 16 calibration targets
2. present 5+ held-out validation targets
3. collect stable fixation samples per target
4. compute robust median predicted position
5. compute error to target
6. summarize mean, median, 95th percentile, and worst-case

Report center and edge/corner performance separately.

## Target collection window

Suggested starting values:
- target settle time: 400–700 ms
- collection time: 500–1000 ms
- reject blink/invalid/low-confidence samples
- require minimum valid-sample count

Tune based on empirical behavior.

## Prototype performance bands

These are engineering targets, not guaranteed claims:

```text
Exploratory prototype: <= 1.0° median validation error
Good research prototype: <= 0.5° median validation error
Stretch target: ~0.3° median validation error under controlled conditions
```

Always report 95th percentile and tracking availability so a good median does not hide failure regions.

## Test conditions

At minimum record:
- participant ID (pseudonymous)
- glasses/contact/no correction
- display dimensions and resolution
- viewing distance
- ambient lighting condition
- camera/lens configuration
- IR illumination revision/configuration
- calibration pattern
- head-restraint status (normally none)
- head movement condition

## Test matrix

### A. Static head
Subject holds normal comfortable posture.

Goal: best-case calibrated performance.

### B. Natural head movement
Subject intentionally shifts several centimeters and changes normal yaw/pitch.

Goal: quantify robustness.

### C. Glasses
Test reflection-prone frames/lenses separately.

### D. Screen zones
Evaluate:
- center
- four quadrants
- edges
- corners

### E. Time/drift
Validate immediately after calibration, then after:
- 5 minutes
- 15 minutes
- 30 minutes
- longer if intended session demands it

### F. Lighting
At minimum:
- dim radiology-like room
- normal office lighting
- brighter ambient condition

## Fixation detector validation

Generate synthetic traces with:
- known stationary clusters
- known saccades
- noise
- invalid gaps
- repeated visits

Test:
- detected fixation count
- centroid error
- duration error
- treatment of gaps
- monotonic dot-size mapping

Use recorded human gaze later for comparison against manually reviewed events, but do not pretend fixation segmentation has a single universally correct ground truth.

## Visual overlay validation

For a static image and known fixation set:
- verify rendered center matches source coordinates
- verify duration ordering matches dot diameter ordering
- verify min/max caps
- verify background image checksum remains unchanged
- verify deterministic export

## Viewport transform validation

Use synthetic checkerboard/reference image with known points.

Test combinations of:
- fit-to-window
- zoom
- pan
- rotation
- flip
- crop
- high-DPI scale

Transform math target: <=1 px numerical error, independent of gaze-estimation error.

## Camera performance validation

Measure:
- requested FPS vs actual FPS
- frame interval distribution
- dropped frame percentage
- exposure time if available
- CPU/GPU usage
- memory stability over 30+ minutes

## Pass/fail philosophy

A validation run should produce machine-readable metrics plus a concise human summary. Never emit only a green/red result.

## Dataset discipline

Retain test dataset version/hash, configuration, git commit, and calibration artifact so benchmark results are reproducible.

## Claim discipline

Documentation/UI must not advertise a measured accuracy until:
- test method is documented
- sample size is stated
- hardware/configuration is stated
- metric definition is stated
- results can be reproduced
