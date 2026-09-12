# Research scope, clinical boundary, and standards notes

## Intended initial use

Stargaze is initially intended for observational research and education: measuring where an expert looks, for how long, and in what sequence while viewing medical images.

The initial system does not diagnose disease, recommend treatment, prioritize patients, or alert a clinician to a suspected finding.

## Why the boundary matters

The U.S. FDA's January 2026 Clinical Decision Support Software guidance explains that some software functions are excluded from the device definition while other functions remain device software. FDA's policy navigator specifically notes that software intended to acquire, process, or analyze a medical image or assess the clinical implications of a medical image may fall under device oversight.

Therefore, until a dedicated regulatory strategy exists, Stargaze should not add clinical interpretation features merely because gaze and image coordinates are available.

Reference:
- FDA, Clinical Decision Support Software, Final Guidance, January 2026: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
- FDA Digital Health Policy Navigator, Step 6: https://www.fda.gov/medical-devices/digital-health-center-excellence/step-6-software-function-intended-provide-clinical-decision-support

## Medical display considerations

DICOM PS3.14 defines the Grayscale Standard Display Function (GSDF), a standardized display function intended to support consistent grayscale presentation. Stargaze does not replace or modify display calibration. Overlays should remain separate from diagnostic image pixels and should not be assumed to preserve a diagnostic display's intended grayscale behavior if shown over the image during interpretation.

Reference:
- DICOM PS3.14 current standard: https://dicom.nema.org/medical/dicom/current/output/chtml/part14/chapter_1.html

## Study design considerations

Before research involving real patient images or human participants, the study owner is responsible for determining applicable institutional review, consent, privacy, security, and data-handling requirements.

The software should facilitate responsible study practice by supporting:
- pseudonymous participant IDs
- local-first processing
- optional omission of raw camera video
- no required patient identifiers
- explicit data-retention/deletion workflows
- immutable raw gaze data with derived-analysis provenance

## Human factors

A visible gaze cursor can change the subject's behavior. Therefore the study configuration must distinguish:
- **setup/debug overlay**: subject can see live pink cursor
- **study-hidden overlay**: gaze is recorded but not shown to subject
- **post-session review**: fixation dots/scan path/heat map shown after interpretation

## Near-IR hardware safety

The project may use near-infrared illumination to generate corneal glints. No arbitrary IR LED, CCTV illuminator, wavelength, or power setting should be described as safe for prolonged eye exposure without appropriate optical characterization and independent safety evaluation.

Software development should support recorded/offline data so algorithm work is not blocked on live NIR exposure.

## Claims

Do not claim:
- diagnostic performance
- prevention of missed diagnoses
- FDA clearance/approval
- a specific gaze accuracy
- eye safety

unless the relevant validation or regulatory work has actually been completed and documented.
