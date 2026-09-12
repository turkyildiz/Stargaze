# Stargaze hardware assumptions

This document defines the prototype hardware contract. It is not a certification or eye-safety statement.

## Prototype goal

Build a remote, non-contact binocular eye tracker mounted below or near a diagnostic monitor. V1 should use commodity UVC cameras connected directly to a development PC.

## Camera requirements

Preferred characteristics:
- monochrome sensor
- global shutter
- native sensitivity in near infrared
- 120 FPS target
- approximately 1 MP is sufficient for first prototype
- manual exposure/gain control strongly preferred
- M12/S-mount lens system preferred for experimentation
- UVC/USB interface for V1

An OV9281-class camera is a reasonable development target because it is a monochrome global-shutter sensor commonly available in USB camera modules and supports high frame rates suitable for eye tracking.

Do not hard-code behavior to one vendor. The acquisition layer must expose capability detection.

## Two-camera geometry

V1 uses two cameras with adjustable baseline.

Prototype arrangement:

```text
+----------------------------------------------------+
|                   monitor                          |
+----------------------------------------------------+

     [camera L]                    [camera R]
          \                            /
           \                          /
                    subject
                     O  O
```

The exact baseline, toe-in angle, lens focal length, and distance should be measured/configured rather than embedded as magic numbers.

## Lens selection

Use replaceable M12 lenses during experimentation.

Selection objective:
- both eyes remain inside usable tracking volume
- each eye occupies enough pixels for stable pupil/glint estimation
- minimal distortion where practical

Start by testing moderate focal lengths rather than the widest bundled lens. Calibrate camera intrinsics if geometric distortion materially affects feature measurement.

## Near-IR illumination

Target concept: controlled 850 nm near-IR illumination producing corneal reflections/glints.

Important:
- do **not** treat arbitrary CCTV IR illuminators as approved for prolonged ocular exposure
- illuminator design requires optical power characterization and independent eye-safety review/testing before prolonged human-subject use
- software documentation must not claim safety from wavelength alone
- provide a hardware interlock/configuration limit in later productization if appropriate

During early software development, use prerecorded imagery, safe lab arrangements, or illumination systems whose exposure characteristics have been properly evaluated.

## Optical filtering

An 850 nm pass/bandpass filter may improve robustness against room/monitor light depending on camera/lens setup.

Treat filter characteristics as configuration:
- center wavelength
- bandwidth
- transmission
- physical placement

Do not assume an IR-pass filter alone creates a good pupil image; test exposure and glint contrast.

## Camera controls to expose

At minimum:
- device identifier
- resolution
- FPS
- exposure
- gain
- gamma/brightness if supported
- auto-exposure toggle

For research consistency, prefer manual/stable exposure after setup.

## Development PC

V1 should run on a normal Windows/Linux development workstation with USB 3.x ports.

Do not require a Raspberry Pi or Jetson for initial implementation. Embedded compute is a later product decision.

## Mount

Prototype mounting can use:
- 2020 aluminum extrusion
- adjustable mini ball heads or custom brackets
- repeatable camera positions with marked/measured baseline

Later enclosure should fix geometry mechanically once the optimum arrangement is known.

## Hardware metadata

Each session manifest should record when known:
- camera make/model
- device serial/descriptor
- lens focal length/model
- camera baseline
- approximate camera-to-monitor geometry
- illuminator revision/configuration
- optical filter
- requested/actual FPS
- exposure/gain

## Hardware validation tests

Before human gaze accuracy tests:
1. verify both streams remain stable at target frame rate
2. measure actual frame interval distribution
3. quantify dropped frames
4. inspect motion blur during saccade-like eye movement
5. verify pupil contrast throughout expected track box
6. verify glints remain detectable over head movement range
7. test glasses/contact/progressive lens cases separately
8. test different ambient lighting levels

## Future productization

Only after software and optical geometry are validated:
- custom camera carrier/enclosure
- custom NIR emitter PCB
- embedded controller/compute decision
- hardware synchronization or trigger lines
- thermal design
- EMC/electrical safety planning
- formal optical/ocular exposure evaluation
- manufacturing calibration procedure

## Explicit non-assumption

The project must never claim that a camera sensor specification implies a finished-system gaze accuracy. Accuracy is measured end-to-end using the protocol in `VALIDATION.md`.
