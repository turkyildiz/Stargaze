# Stargaze visualization specification

## Purpose

The visualization layer lets researchers study dense expert visual search without losing event timing or overwhelming the screen.

## Primary view: fixation dots

The canonical research overlay uses pink fixation circles.

### Meaning
- center position = fixation centroid
- diameter = fixation duration
- pink = fixation overlay semantic color
- sequence/timestamp remains available in metadata

### Duration mapping

Use a monotonic logarithmic function with configurable bounds:

```python
diameter_px = clamp(
    min_px + scale_px * log1p(duration_ms / duration_tau_ms),
    min_px,
    max_px,
)
```

Recommended starting configuration for a typical high-resolution monitor:

```text
min_px = 6
max_px = 48
scale_px = 12
duration_tau_ms = 100
```

These are visualization defaults, not scientific constants.

### Why not linear scaling

A linear mapping can let a rare multi-second fixation cover a large section of the image. Log scaling preserves ordering while keeping the plot readable.

## Dense data expectation

Experts may inspect nearly the entire image. Hundreds of fixations or thousands of raw samples are expected.

Therefore the review UI must support filtering rather than assuming sparse annotations.

## Required view modes

### 1. Live gaze
One small semi-transparent pink cursor follows current estimated gaze.

This is primarily a setup/debug mode. Study configuration may hide live gaze from the subject to avoid altering search behavior.

### 2. Raw gaze samples
Show every valid gaze sample as a tiny point.

Controls:
- point size
- opacity
- time range
- minimum confidence

This is the densest view.

### 3. Fixation dots
One circle per fixation.

Controls:
- duration scaling
- opacity
- minimum duration
- time range
- confidence threshold
- show/hide revisits

### 4. Scan path
Connect fixation centroids in chronological order.

Options:
- sequence numbers
- arrow direction
- fade older segments
- selected time range

Never infer semantic reasoning from the path itself; it is descriptive gaze behavior.

### 5. Heat map
Accumulate gaze/fixation dwell spatially.

Provide documented kernel parameters. Heat maps are derived views and must never replace event data.

### 6. Playback
Animate gaze/fixation positions according to recorded timestamps.

Controls:
- play/pause
- speed 0.25x to 8x
- scrub timeline
- show recent trail window
- jump to fixation

### 7. Aggregate dwell
Repeated visits to nearby locations may be aggregated for visualization only.

Display total dwell and revisit count separately when possible; one long fixation is behaviorally different from several returns.

### 8. Expert comparison
For multiple experts viewing the same image:
- normalize into common image coordinate space
- allow one expert at a time or comparison modes
- support per-expert legend/style without changing canonical underlying data
- provide common coverage/consensus maps

## Layering

The source medical image is immutable.

Recommended render order:

```text
background medical image
ROI/viewport guides (optional)
heat map (optional)
scan path (optional)
fixation circles
selected fixation highlight
UI chrome
```

## Color

Canonical fixation overlay: pink.

Keep the exact color in a theme/config constant, not scattered literals. Exports should store the visualization config used.

## Accessibility/research concerns

- overlay must be switchable off
- do not rely on color alone when comparing experts; use labels/symbols if necessary
- offer high-contrast selection outlines
- live overlay visibility to subject must be explicit in study settings because visible feedback can alter gaze behavior

## Hit testing

Clicking a fixation should reveal:
- fixation ID
- start/end time
- duration
- centroid
- confidence
- sample count
- revisit/aggregate information if enabled
- mapped image coordinates if available

## Export

Required:
- PNG raster export
- SVG vector overlay/export where practical
- CSV/JSON event export

Export metadata should include:
- session ID
- calibration ID
- fixation algorithm/config
- visualization config
- coordinate system
- image dimensions
- software version/git revision

## Determinism

Given identical:
- background image
- fixation events
- visualization config

the exported fixation circles must have identical positions and sizes.

## Large-session behavior

The UI should remain responsive with at least:
- 100,000 raw samples
- 10,000 fixation events across a study/session collection

Use downsampling/level-of-detail for display only, never destructive persistence.
