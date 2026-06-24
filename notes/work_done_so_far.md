# Work Done So Far

This document explains the main work done in the project so far. It is written
as a simple progress summary.

## Main Goal

The goal is to run TORAX using IMAS data files directly. The important point is
that TORAX should read the plasma data from the IMAS files instead of using a
manual mapping script as the main workflow.

The IMAS files are in the `data/` folder:

- `data/equilibrium.h5`
- `data/core_profiles.h5`
- `data/core_sources.h5`
- `data/master.h5`

## Direct IMAS Loading

We confirmed that TORAX can read the IMAS data directly. The config uses this
IMAS URI:

```python
IMAS_URI = "imas:hdf5?path=data"
```

The TORAX config loads these IDSs:

- `equilibrium`
- `core_profiles`
- `core_sources`

The IMAS files use DD version `3.42.0`, but TORAX expects DD version `4.0.0`.
Because of that, the loader must use:

```python
explicit_convert=True
```

This lets IMAS convert the data before TORAX uses it.

## Files Changed

### `scripts/imas_torax_config.py`

This file is now the main direct IMAS TORAX config.

It does these things:

- loads `equilibrium` from IMAS,
- loads `core_profiles` from IMAS,
- loads `core_sources` from IMAS,
- builds TORAX profile conditions using TORAX IMAS tools,
- builds plasma composition using TORAX IMAS tools,
- builds sources using TORAX IMAS tools,
- uses IMAS geometry from the equilibrium file,
- runs a short baseline simulation.

The baseline settings are:

- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`
- transport model: `constant`
- solver: `linear`

The file also supports setting changes from the terminal. For example:

```bash
TORAX_T_FINAL=1.0
TORAX_N_RHO=50
TORAX_FIXED_DT=0.05
```

This makes it easier to test TORAX settings without changing the baseline
config every time.

### `scripts/map_torax_to_imas.py`

This file reads TORAX NetCDF output files.

It was changed so it can read either:

- the initial TORAX state with `time_index=0`,
- the final TORAX state with `time_index=-1`.

This is important because the initial state proves TORAX started from the IMAS
data. The final state shows what happened after TORAX evolved the plasma.

### `scripts/plot_imas_torax_profiles.py`

This file makes plots comparing IMAS and TORAX.

The plots now show three curves:

- IMAS input,
- TORAX initial state,
- TORAX final state.

This helps show that TORAX starts close to the IMAS data and then changes after
the simulation runs.

The plots are saved in:

```text
plots/imas_vs_torax/
```

### `scripts/summarize_torax_output.py`

This file summarizes TORAX output.

It now reads the latest output from the direct IMAS TORAX output folder instead
of using an old hard-coded file path.

It prints useful information like:

- profile variable shapes,
- final plasma current,
- fusion power,
- fusion gain,
- q95,
- total thermal stored energy.

### `notes/direct_imas_torax_baseline.md`

This note explains the baseline run.

It records:

- which IMAS files are used,
- which TORAX IMAS functions are used,
- the baseline TORAX settings,
- which sources are included,
- which source was excluded,
- how the initial TORAX state compares to the IMAS input.

### `notes/torax_setting_experiments.md`

This note records TORAX setting experiments.

So far, it includes:

- a longer simulation time test,
- a radial grid resolution test.

## Important Results

### TORAX Starts From the IMAS Data

We compared the IMAS input with the TORAX initial state.

The values were very close:

| Quantity | IMAS | TORAX initial |
| --- | ---: | ---: |
| Electron temperature at axis | 31.949 keV | 31.9169 keV |
| Ion temperature at axis | 23.6679 keV | 23.6535 keV |
| Electron density at axis | 1.16706e20 | 1.16707e20 |
| Plasma current | 1.5e7 A | 1.5e7 A |

This shows that TORAX is really using the IMAS data files.

### Baseline Run

The baseline run uses:

- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`

This gives a short simulation that is useful as a reference case.

### Longer Time Experiment

We ran a longer case with:

```bash
TORAX_T_FINAL=1.0
```

This changed the run from `0.1 s` to `1.0 s`.

Compared to the baseline, the longer run showed:

- electron temperature went down more,
- ion temperature went down more,
- electron density went up,
- plasma current went down.

This makes sense because the plasma had more time to evolve.

### Grid Resolution Experiment

We ran a grid test with:

```bash
TORAX_N_RHO=50
```

This changed the radial grid from `n_rho = 25` to `n_rho = 50`.

The results stayed close to the baseline. Most changes were less than about
1 percent. This is good because it means the short baseline run is not strongly
dependent on the radial grid size.

## What This Means

The project has moved past just trying to make TORAX run. Now there is a real
workflow:

1. Load IMAS files directly into TORAX.
2. Run a baseline TORAX simulation.
3. Check that TORAX starts from the IMAS data.
4. Change one TORAX setting at a time.
5. Save each output in a separate folder.
6. Compare the new run to the baseline.
7. Write down what changed.

This is useful because it makes the work easier to explain and easier to repeat.

## Good Files to Put on GitHub

These files are useful to commit:

- `scripts/imas_torax_config.py`
- `scripts/map_torax_to_imas.py`
- `scripts/plot_imas_torax_profiles.py`
- `scripts/summarize_torax_output.py`
- `notes/direct_imas_torax_baseline.md`
- `notes/torax_setting_experiments.md`
- `notes/work_done_so_far.md`

The TORAX NetCDF output files in `torax_outputs/` are generated files. They may
be large, so they usually should not be committed unless the mentor asks for
them.

## Next Suggested Step

The next good experiment is to turn off one source, such as `ecrh`, and compare
the result to the baseline. This would show how much that source affects the
temperature, current, and fusion results.
