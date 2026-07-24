# Work Done So Far

This document provides a high-level summary of the completed work, current
development efforts, and remaining tasks for the IMAS–TORAX project. A
detailed chronological record of the project can be found in
`project_history.md`.

## Completed

### IMAS–TORAX Workflow

- Developed a complete IMAS-driven TORAX read–run–write workflow.
- Read plasma profiles, equilibrium data, and source terms directly from IMAS.
- Mapped IMAS data into TORAX inputs.
- Mapped TORAX outputs back into IMAS-compatible structures.
- Validated the bidirectional IMAS ↔ TORAX workflow.

### Baseline Validation

- Verified baseline transport simulations against IMAS reference profiles.
- Built comparison tools for initial and final TORAX states.
- Added profile-difference metrics and validation plots.
- Performed time-step and radial-resolution studies.

### Source Studies

- Investigated IMAS source mapping.
- Evaluated the effects of ECRH, fusion, ohmic heating, radiation, synchrotron
  radiation, and bootstrap current.
- Performed controlled source-sensitivity experiments.

### QuaLiKiz Integration

- Integrated QuaLiKiz into the IMAS-driven TORAX workflow.
- Ran QuaLiKiz transport simulations.
- Generated IMAS vs. QuaLiKiz comparison and difference plots.

### TGLF Integration

- Installed and configured TGLF through GACODE.
- Connected TGLF to TORAX.
- Resolved execution-path issues.
- Successfully ran coupled TORAX–TGLF simulations.
- Generated IMAS vs. TGLF comparison plots.

### Sawtooth Studies

- Developed the framework for sawtooth transport studies.
- Implemented sawtooth-on and sawtooth-off simulations.
- Created comparison and diagnostic plotting tools.
- Began investigating mixing-radius and flattening-factor configurations.

### Pedestal Studies

- Developed pedestal detection and analysis tools.
- Implemented pedestal comparison utilities.
- Began investigating pedestal location and evolution.

### Pellet Studies

- Developed a configurable pellet source for TORAX.
- Created parameter studies for pellet strength, width, and deposition
  location.
- Built comparison and optimization utilities.

### Density Evolution

- Verified electron and ion density evolution.
- Developed particle-source diagnostics.
- Investigated source balance throughout simulations.

### Documentation

- Wrote comprehensive project documentation.
- Documented the complete IMAS–TORAX workflow.
- Created a detailed project history covering the full internship.
- Maintained progress notes and development summaries.
- Improved repository readability for future contributors.

### Repository Improvements

- Organized scripts, experiment outputs, and supporting files.
- Added reusable plotting and comparison utilities.
- Improved repository structure and version control.
- Cleaned and organized commits into logical project milestones.

---

# Current Work

- Finalizing sawtooth transport analysis.
- Refining pedestal location and optimization.
- Completing pellet parameter studies.
- Comparing baseline, QuaLiKiz, and TGLF transport models using consistent
  numerical settings.
- Investigating high-resolution q-profile convergence behavior.
- Continuing repository cleanup, documentation, and code organization.

---

# Upcoming Work

- Complete remaining sawtooth analysis.
- Finalize pedestal optimization.
- Finalize pellet optimization.
- Finish transport-model comparisons.
- Consolidate duplicate and experimental scripts.
- Organize plots and documentation.
- Integrate the completed IMAS-driven TORAX workflow into the IPS framework
  for whole-device modeling.

---

## Project Status

The core IMAS-driven TORAX workflow has been completed and validated. Current
efforts focus on extending the workflow through additional physics studies,
including sawtooth, pedestal, pellet, and transport-model comparisons, while
preparing the project for future integration into the Integrated Plasma
Simulator (IPS).
