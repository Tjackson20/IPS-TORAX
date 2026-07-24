# IPS–TORAX Project History

## Project Overview

The purpose of this project is to connect Integrated Modeling and Analysis
Suite (IMAS) plasma data with TORAX transport simulations and prepare the
workflow for eventual integration into the Integrated Plasma Simulator (IPS)
framework. The workflow reads plasma profiles, equilibrium data, and source
terms from IMAS; converts them into TORAX inputs; runs transport simulations;
compares the results with the original IMAS data; and maps TORAX results back
into IMAS-compatible structures.

Development began in June 2026. The project has progressed from basic IMAS
file inspection to a working bidirectional IMAS–TORAX workflow, baseline
verification, source and numerical studies, and integration of the QuaLiKiz
and TGLF transport models. Current work extends the workflow with sawtooth,
pedestal, pellet, density, and particle-source studies.

This work was completed during a 10-week research internship focused on
developing components for an IMAS-driven transport workflow that will
ultimately integrate into IPS for whole-device fusion modeling.

## My Role

This project was part of a larger effort to develop an IPS-based whole-device
modeling workflow for fusion simulations. My primary responsibility focused on
the TORAX and IMAS portion of that workflow.

My responsibilities included:

- developing the IMAS-driven TORAX read–run–write workflow
- validating the IMAS ↔ TORAX mapping
- integrating the QuaLiKiz and TGLF transport models
- creating profile-comparison and visualization tools
- investigating sawtooth, pedestal, pellet, density, and particle-source
  behavior
- preparing the workflow for future integration into IPS

## 1. Initial Repository and Environment Setup

The project repository was created on June 16, 2026. Early setup work
established the Python and TORAX development environment and identified the
IMAS HDF5 files required by the workflow.

The source data includes:

- `core_profiles`
- `equilibrium`
- `core_sources`
- `core_transport`
- `summary`
- supporting IMAS metadata

The raw data, Python caches, TORAX state-history files, and TGLF run
directories were excluded from version control. This keeps the repository
focused on source code, analysis tools, documentation, and selected plots.

## 2. IMAS Data Exploration and Validation

The first development phase focused on understanding the structure and
contents of the IMAS files. Reader and inspection scripts were created for:

- electron and ion temperature profiles
- electron density and ion-related profile data
- effective charge
- plasma current and magnetic equilibrium
- safety-factor and flux profiles
- geometric quantities
- heating, current-drive, and particle sources
- transport-model data
- summary quantities

Consistency checks confirmed that the main IMAS datasets represented the same
time slice and used compatible radial grids. The principal profile and
equilibrium files used a 70-point radial grid at the same simulation time.

The project also identified an IMAS Data Dictionary version difference: the
input files use version `3.42.0`, while the TORAX installation expects version
`4.0.0`. Direct loading therefore uses `explicit_convert=True`.

## 3. IMAS-to-TORAX Mapping

The next phase created a manual IMAS-to-TORAX mapping to establish how the two
data models correspond.

The mapping included:

- IMAS electron temperature to TORAX `T_e`
- IMAS ion temperature to TORAX `T_i`
- IMAS electron density to TORAX `n_e`
- IMAS effective charge to TORAX `Z_eff`
- equilibrium major radius and magnetic field to TORAX geometry
- plasma current and safety-factor information
- IMAS heating and current-drive profiles to TORAX source definitions

Temperature units were converted from electron volts in IMAS to
kiloelectron-volts where required by TORAX.

This phase produced reusable readers and mapping utilities rather than relying
on one large script. It also established the field-level correspondence needed
for later direct loading and output conversion.

## 4. First IMAS-Derived TORAX Simulation

An initial TORAX configuration was built from the mapped IMAS data. This
demonstrated that the extracted profiles, equilibrium information, and source
terms could be assembled into a valid TORAX configuration and used to run a
transport simulation.

Output inspection tools were added to read TORAX NetCDF state-history files
and report:

- profile dimensions
- electron and ion temperatures
- density
- safety factor
- plasma current
- fusion power and fusion gain
- `q95`
- stored thermal energy

Output-file handling was improved so the tools could reliably select the
latest state-history file from a chosen run directory.

## 5. TORAX-to-IMAS Mapping

After the first successful run, the reverse mapping was developed. TORAX
profiles and scalar results were mapped into IMAS-compatible structures for:

- `core_profiles`
- `equilibrium`
- `core_transport`
- `core_sources`
- `summary`

The mapping tools support reading both the initial and final TORAX states. The
initial state is used to verify that TORAX started from the intended IMAS
profiles, while the final state represents the evolved simulation result.

This completed the core read–run–write path: read IMAS data, run TORAX, and
prepare TORAX results for writing back to IMAS.

## 6. Direct IMAS-Driven TORAX Workflow

The manual mapping work was followed by a direct IMAS-driven configuration.
TORAX was configured to load the `equilibrium`, `core_profiles`, and
`core_sources` IDSs through:

```text
imas:hdf5?path=data
```

TORAX IMAS utilities were used to build:

- profile conditions
- plasma composition
- source models
- magnetic geometry

The baseline configuration evolved:

- plasma current
- electron heat
- ion heat
- density

The original short baseline used a constant transport model, a linear solver,
`n_rho = 25`, `t_final = 0.1`, and `fixed_dt = 0.1`.

Environment-variable controls were added so simulation duration, grid
resolution, time step, and selected sources could be changed without rewriting
the main configuration.

## 7. Baseline Verification and Comparison Tools

Comparison utilities were developed to evaluate IMAS input profiles against
the TORAX initial and final states. The plots cover:

- electron density
- ion density
- electron temperature
- ion temperature
- safety-factor (`q`) profile

The initial TORAX values closely matched the IMAS reference values. For the
original baseline, representative central values were:

| Quantity | IMAS | TORAX initial | TORAX final |
| --- | ---: | ---: | ---: |
| Electron temperature, keV | 31.949 | 31.9169 | 29.5186 |
| Ion temperature, keV | 23.6679 | 23.6535 | 21.5374 |
| Electron density, m^-3 | 1.16706e20 | 1.16707e20 | 1.32161e20 |
| Plasma current, A | 1.5e7 | 1.5e7 | 1.48898e7 |

These comparisons verified that the simulation was initialized from the IMAS
data and then evolved the profiles.

Full-profile comparison tools were also added. They calculate RMS difference,
maximum absolute difference, and maximum percentage difference rather than
comparing only central values.

## 8. Source Mapping and Source-Sensitivity Studies

The IMAS `core_sources` data was inspected source by source. Useful data was
identified for:

- neutral beam injection
- electron cyclotron heating
- fusion heating
- ohmic heating
- radiation
- synchrotron radiation
- bootstrap current

Empty or zero-valued entries in the available case included lower-hybrid,
ion-cyclotron, cold-neutral, charge-exchange, and pellet data.

The baseline source mapping was expanded to include additional IMAS
contributions. NBI and bootstrap current information were combined where
appropriate, and radiation and synchrotron terms were incorporated into the
electron-energy source treatment.

Controlled source-off experiments produced the following observations:

- Removing ECRH primarily reduced central electron temperature during the
  short simulation.
- Removing fusion reduced both central electron and ion temperatures and set
  fusion power and gain to zero.
- Removing ohmic heating produced little profile change over the short
  `0.1 s` interval.
- Removing prescribed electron-ion exchange produced no visible change in the
  central and global metrics checked.
- Fusion gain values require careful interpretation because removing an
  external heating source changes the denominator.

## 9. QuaLiKiz Transport Integration

QuaLiKiz was integrated as a transport model in the direct IMAS-driven TORAX
workflow.

This work included:

- a dedicated QuaLiKiz TORAX configuration
- execution of IMAS-initialized QuaLiKiz transport simulations
- profile comparison scripts
- IMAS-versus-QuaLiKiz plots
- difference plots for electron density, electron temperature, ion
  temperature, and safety factor
- ion-density comparison output

The integration provides a higher-fidelity transport option that can be
evaluated against the constant-transport baseline and other transport models.

## 10. TGLF Installation and Integration

TGLF was installed from GACODE and connected to TORAX through a dedicated
configuration. The local executable is referenced explicitly by the TORAX
transport configuration.

During integration, execution-path issues between TORAX and TGLF were
identified, diagnosed, and resolved. This allowed TORAX to launch TGLF
correctly and complete coupled transport simulations. The exact configuration
required to resolve these issues may depend on the local TORAX, GACODE, MPI,
and Python installations.

The local MPI setup was validated with:

```python
"n_processes": 1,
"n_cores_per_process": 1,
```

Validation confirmed that:

- TORAX launched the TGLF executable
- a complete TGLF transport simulation ran successfully
- NetCDF state-history output was generated
- IMAS-versus-TGLF comparison plots were produced
- difference plots were produced for the main profiles

An additional smaller-time-step TGLF configuration and comparison set were
created for continued numerical evaluation.

Installation paths and runtime settings should be reviewed when reproducing
the workflow on another system or after updating TORAX or TGLF.

## 11. Time and Spatial Resolution Studies

The simulation was tested over longer durations and with different radial
resolutions.

Increasing the run from `0.1 s` to `1.0 s` showed continued plasma evolution:

- central electron and ion temperatures decreased
- central electron density increased
- plasma current decreased
- safety-factor changes remained modest

The initial `n_rho = 25` versus `n_rho = 50` study showed relatively small
changes in most central and scalar values. A broader convergence study later
tested:

- `n_rho`: 25, 50, 100, 150, and 200
- `fixed_dt`: 0.1, 0.05, 0.025, and 0.0125

The time-step study showed progressively smaller profile differences as the
time step was reduced. The radial study showed improving temperature and
density agreement at higher resolution, while the high-resolution q-profile
comparison exposed an issue requiring additional investigation.

## 12. Sawtooth Transport Studies

Current physics studies added TORAX sawtooth configurations and analysis
tools. The study compares sawtooth-on and sawtooth-off cases and explores
different mixing-radius multipliers and flattening factors.

Cases prepared or analyzed include mixing-radius multipliers from approximately
`1.1` through `1.6` and flattening factors from `1.0` through `1.10`.

The analysis includes:

- initial, pre-crash, post-crash, and final-state comparisons
- electron and ion temperature response
- electron and ion density response
- q-profile response
- combined on-versus-off summaries
- range and crash statistics
- comparisons with the IMAS reference profiles

Initial analysis indicates that sawtooth behavior has its strongest effect in
the plasma core, particularly on electron and ion temperatures and the central
q-profile. Density changes are smaller in the tested cases.

These studies remain active and have not yet been finalized.

## 13. Pedestal Studies

Pedestal analysis was added to improve the treatment of the plasma edge.
Utilities were developed to:

- extract pedestal values from IMAS-derived profiles
- locate the pedestal using profile derivatives
- interpolate pedestal quantities
- compare candidate pedestal locations
- evaluate pedestal evolution
- compare sawtooth behavior with and without pedestal treatment

The current configurations include a pedestal location near normalized radius
`0.95`, along with scans and comparisons against other candidate locations.
Plots cover temperature, density, q-profile, derivatives, and pedestal
on/off behavior.

Pedestal optimization remains in progress.

## 14. Pellet Injection Studies

A controlled TORAX pellet source was introduced because the available IMAS
pellet source profile was empty. Parameter studies were created for:

- pellet strength
- deposition location
- deposition width

The tested deposition locations include normalized radii `0.6`, `0.7`, `0.8`,
and `0.9`. Width cases include `0.17`, `0.25`, and `0.35`, with multiple
particle-strength cases.

Analysis tools compare:

- all tested density profiles
- density differences from IMAS
- percentage differences
- RMS error
- maximum density response
- the best-performing cases from successive scans

The pellet studies are still being consolidated and validated.

## 15. Density Evolution and Particle-Source Analysis

Additional diagnostics were created to verify that TORAX evolves both electron
and ion density and to inspect the balance of particle sources.

The work includes:

- initial-versus-final density evolution plots
- electron and ion density checks
- particle-source discovery and inspection
- source-balance diagnostics
- NetCDF group and source-mapping inspection
- NBI mapping tests

The density profiles change during the simulation, confirming that density is
being solved and updated rather than remaining fixed.

## 16. Plotting, Reporting, and Repository Organization

Throughout the project, plotting and reporting utilities were added for:

- IMAS versus TORAX
- IMAS versus QuaLiKiz
- IMAS versus TGLF
- initial versus final states
- baseline versus experiment
- full-profile difference metrics
- sawtooth crash behavior
- pedestal scans
- pellet scans
- density evolution
- source and ECRH studies

Setup notes, baseline documentation, mapping notes, experiment records, mentor
updates, and concise progress summaries were also maintained.

Repository cleanup is ongoing. Generated raw simulation outputs remain ignored,
while scripts, selected plots, and durable documentation are being organized
into focused commits.

## Major Accomplishments

- Established a functional IMAS-driven TORAX workflow.
- Developed IMAS ↔ TORAX read/write utilities.
- Validated the baseline transport simulation against IMAS reference data.
- Integrated the QuaLiKiz transport model.
- Installed and integrated the TGLF transport model.
- Created a reusable profile-comparison and difference-analysis framework.
- Developed a sawtooth analysis framework for crash and parameter studies.
- Developed a pedestal analysis and optimization framework.
- Developed a pellet strength, width, and location study framework.
- Created density-evolution and particle-source diagnostics.
- Produced repository documentation and plotting utilities for reproducibility
  and future development.

## Tools and Technologies

- Python
- TORAX
- IMAS
- QuaLiKiz
- TGLF
- JAX
- NumPy
- Matplotlib
- NetCDF
- Linux / WSL
- VS Code
- Git
- GitHub

## Current Project State

The following major capabilities are complete:

- reading and validating IMAS data
- mapping IMAS inputs into TORAX
- running TORAX from IMAS-derived conditions
- directly loading IMAS IDSs in the TORAX configuration
- mapping TORAX results back into IMAS-compatible structures
- comparing IMAS, TORAX initial, and TORAX final profiles
- validating a baseline and testing source sensitivity
- integrating QuaLiKiz
- installing and integrating TGLF
- generating transport-model comparison and difference plots

Current areas of ongoing research include:

- sawtooth transport
- pedestal location and optimization
- pellet strength, width, and location
- density evolution and particle-source balance
- smaller-time-step TGLF comparison
- continued IMAS–TORAX mapping and plotting improvements

## Next Steps

- Complete and document the sawtooth study.
- Finalize pedestal optimization.
- Finalize the pellet parameter study.
- Compare baseline, QuaLiKiz, and TGLF transport behavior using consistent
  numerical settings and metrics.
- Resolve the high-resolution q-profile convergence behavior.
- Consolidate duplicate and experimental scripts.
- Organize plots and documentation into maintainable repository groups.
- Integrate the IMAS-driven TORAX workflow into IPS for whole-device modeling.

## Conclusion

Over the course of this 10-week project, the workflow progressed from initial
IMAS data exploration to a functional IMAS-driven TORAX workflow with
integrated transport-model support and multiple plasma-physics studies. The
project established a reusable foundation for future IPS integration while
providing tools for transport validation, comparison, and continued physics
research. The resulting workflow, documentation, and analysis tools create a
strong starting point for future development and collaboration.
