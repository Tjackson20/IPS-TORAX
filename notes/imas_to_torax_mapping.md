# IMAS to TORAX Mapping Notes

## Current Status

The IMAS readers are working and the main datasets are consistent.

Confirmed:
- All main IMAS files use time = 449.73958822
- core_profiles and equilibrium both use 70 rho points
- IMAS data can be combined into a TORAX input dictionary

## core_profiles → TORAX profile_conditions

IMAS fields:
- electron_temperature
- electron_density
- ion_average_temperature
- zeff
- electron_pressure
- ion_pressure_total
- pressure_thermal
- volume

TORAX fields:
- T_e
- T_i
- n_e
- Z_eff

Notes:
- IMAS temperature appears to be in eV.
- TORAX examples use keV.
- Conversion needed: eV * 1e-3 = keV.

## equilibrium → TORAX geometry

IMAS fields:
- r0
- b0
- plasma_current
- q_profile
- psi_profile
- volume
- area
- elongation
- triangularity_upper
- triangularity_lower

TORAX fields:
- R_major
- B_0
- Ip
- geometry information

## core_sources → TORAX sources

IMAS fields:
- source_names
- source_info
- electron_energy
- ion_energy
- j_parallel

Important sources:
- NBI: electron heating, ion heating, current drive
- Fusion: electron heating and ion heating
- Ohmic: electron heating
- Bootstrap current: current profile

## core_transport → TORAX transport

IMAS transport models:
- combined
- transport_solver
- background
- neoclassical
- anomalous

TORAX transport examples:
- constant
- qlknn

## Next Questions

1. Which source terms should be passed into TORAX directly?
2. Should source profiles be combined or kept separate?
3. Which TORAX example should be used as the starting config?
4. How should IMAS profiles be converted into TORAX profile_conditions?
