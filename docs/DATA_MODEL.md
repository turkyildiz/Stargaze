# Stargaze data model

The data model is designed for reproducibility, offline reprocessing, and later algorithm comparison.

## General rules

- all timestamps used for interval math are `timestamp_ns` from a monotonic clock
- all persisted schemas include `schema_version`
- all coordinates carry an explicit coordinate space
- all derived artifacts reference their source session/calibration
- invalid tracking is recorded, not omitted silently
- raw samples are append-only and immutable after session close

## Coordinate spaces

Use an enum such as:

```python
class CoordinateSpace(str, Enum):
    CAMERA_LEFT = "camera_left_px"
    CAMERA_RIGHT = "camera_right_px"
    DESKTOP = "desktop_px"
    MONITOR = "monitor_px"
    VIEWPORT = "viewport_px"
    IMAGE = "image_px"
    NORMALIZED_SCREEN = "normalized_screen"
    PATIENT = "patient_mm"  # future
```

Coordinate-bearing structures should include the corresponding space.

## GazeSample

Required fields:

```text
schema_version
sample_id
session_id
calibration_id
timestamp_ns
x
y
coordinate_space
valid
confidence
left_eye_valid
right_eye_valid
uncertainty_x_px (nullable)
uncertainty_y_px (nullable)
source_frame_left_seq (nullable)
source_frame_right_seq (nullable)
raw_x (optional unfiltered estimate)
raw_y
filter_name (nullable)
```

Rules:
- `confidence` range 0..1
- coordinates may be null when invalid; do not fake `(0,0)`
- filtered and unfiltered gaze should be distinguishable

## EyeFeatures

Per eye/camera:

```text
frame_sequence
timestamp_ns
eye_side
roi_x, roi_y, roi_w, roi_h
pupil_x, pupil_y
pupil_major_axis
pupil_minor_axis
pupil_angle_deg
glint_points[]
selected_glint_x/y
blink_or_occluded
confidence
head_yaw/pitch/roll (optional shared fields)
head_tx/ty/tz (optional/relative)
```

Store only if study/debug configuration enables feature persistence.

## CameraFrameMeta

```text
camera_id
sequence
timestamp_ns
width
height
requested_fps
exposure
capture_ok
dropped_since_previous
recording_file_offset/index (optional)
```

## Fixation

```text
schema_version
fixation_id
session_id
algorithm
algorithm_version
start_timestamp_ns
end_timestamp_ns
duration_ms
centroid_x
centroid_y
coordinate_space
sample_count
first_sample_id
last_sample_id
dispersion_px
mean_confidence
min_confidence
valid_fraction
```

Optional:
- sample IDs or compressed ranges
- uncertainty ellipse summary
- ROI/image mapping if computed later

Derived fixation outputs should be reproducible from raw samples plus algorithm config.

## CalibrationArtifact

```text
schema_version
calibration_id
created_utc
monitor_id
monitor_geometry
pattern_type
feature_definition_version
model_type
model_parameters
training_targets[]
validation_targets[]
fit_metrics
validation_metrics
track_box_summary
viewing_distance_mm (nullable)
physical_monitor_width_mm (nullable)
physical_monitor_height_mm (nullable)
```

Never persist only a pickle as the sole calibration representation. Store a human-inspectable/versioned representation of the model/config where practical.

## MonitorGeometry

```text
monitor_id
desktop_x
desktop_y
width_px
height_px
dpi_scale_x
dpi_scale_y
physical_width_mm (nullable)
physical_height_mm (nullable)
primary
```

## CalibrationTargetObservation

```text
target_index
target_x_px
target_y_px
sample_start_ns
sample_end_ns
accepted_sample_count
rejected_sample_count
feature_summary
predicted_x_px
predicted_y_px
error_px
error_mm (nullable)
error_deg (nullable)
```

## ViewportTransformState

This state is timestamped because the image can move during a session.

```text
timestamp_ns
viewport_id
desktop_rect
source_image_width
source_image_height
rendered_rect
zoom
pan_x
pan_y
rotation_deg
flip_horizontal
flip_vertical
crop_rect (nullable)
```

## ImageMappedFixation

Do not overwrite the original fixation. Produce a derived mapping record:

```text
fixation_id
viewport_state_id
image_x
image_y
inside_image
mapping_confidence
```

## SessionManifest

```text
schema_version
session_id
study_id (nullable)
participant_id (pseudonymous)
case_id (nullable)
started_utc
ended_utc
software_version
git_commit
platform
camera_configuration
monitor_configuration
calibration_id
fixation_configuration
visualization_configuration
storage_flags
notes
```

Do not require patient name/MRN/DOB.

## Event log

Use JSONL for structured runtime events:

```text
camera_connected
camera_disconnected
tracking_lost
tracking_recovered
blink_start/end
calibration_started/completed/failed
recording_started/stopped
drift_warning
viewport_changed
export_created
```

Each event:

```json
{
  "timestamp_ns": 123,
  "event_type": "tracking_lost",
  "severity": "warning",
  "payload": {}
}
```

## File formats

MVP:
- JSON for manifest/calibration
- CSV for gaze/fixations/camera metadata
- JSONL for events

Later:
- Parquet for large tabular sessions
- MP4/MKV or frame archive for optional raw camera data

Keep readers/writers behind interfaces so format migration does not affect domain code.

## Schema evolution

Readers must:
- check schema version
- reject future incompatible versions clearly
- provide explicit migration functions for supported historical versions

Never silently reinterpret columns whose units or coordinate spaces have changed.
