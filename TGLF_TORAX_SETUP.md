# TGLF Setup and TORAX Integration

## Purpose

These notes document the local setup and code changes required to run the TGLF transport model through TORAX. Some parts of this setup are specific to this computer and may not work exactly the same on another system.

## TGLF installation

TGLF was installed separately from TORAX using the GACODE repository.

The working TGLF executable is located at:

```text
/home/teliyah/gacode/tglf/bin/tglf
```

The TGLF build used GACODE commit:

```text
50a14c88
```

The GACODE platform configuration was modified locally so that the build used the OpenBLAS library installed on this Ubuntu system.

## TORAX transport configuration

The TORAX configuration file is:

```text
scripts/imas_torax_config_tglf.py
```

The transport section is configured as:

```python
"transport": {
    "model_name": "tglf",
    "tglf_exec_path": "/home/teliyah/gacode/tglf/bin/tglf",
    "output_directory": "torax_tglf_runs",
    "n_processes": 1,
    "n_cores_per_process": 1,
    "verbose": True,
},
```

## Local TORAX patch

The default TORAX TGLF interface did not run correctly in this local environment.

TORAX created each TGLF run directory and then launched TGLF with the plan directory set as the current working directory. It also passed a run path that already included the plan directory. TGLF then joined the working directory and run path, causing the directory path to be repeated.

Example of the incorrect path:

```text
.../torax_tglf_run_.../torax_tglf_run_.../tglf_run_0000
```

The local TORAX code was changed so TGLF receives only the individual run-directory name instead of the repeated relative path.

The modified installed file is:

```text
~/miniforge3/envs/TORAX/lib/python3.11/site-packages/torax/_src/transport_model/tglf_transport_model.py
```

The important change was equivalent to using:

```python
os.path.basename(run_directory)
```

for the directory passed after the TGLF `-e` option.

## Important portability warning

This patch was made directly inside the local Python environment and is not automatically included when another person clones this GitHub repository.

Another user may need to:

1. Install GACODE and compile TGLF separately.
2. Update `tglf_exec_path` for their own installation location.
3. Check whether their TORAX version still has the run-directory issue.
4. Reapply the local TORAX patch if needed.
5. Configure MPI for their own system.

The exact setup may differ depending on:

- TORAX version
- GACODE version
- Linux distribution
- MPI implementation
- OpenBLAS installation
- Python or Conda environment
- Local directory paths

## MPI limitation

Running TGLF with more than one MPI task produced an unsupported `--env` option in the current MPI setup.

The verified working settings are:

```python
"n_processes": 1,
"n_cores_per_process": 1,
```

These settings allow TORAX to run multiple TGLF calculations while each individual TGLF calculation uses one core.

## Successful validation

The following steps were completed successfully:

- GACODE and TGLF were compiled.
- The TGLF executable ran manually.
- TORAX launched TGLF automatically.
- A complete TORAX simulation using TGLF finished successfully.
- A NetCDF state-history output was generated.
- TGLF results were compared with QLKNN results.

Successful TGLF output:

```text
torax_outputs/full_baseline_tglf/state_history_20260710_115025.nc
```

QLKNN comparison output:

```text
torax_outputs/full_baseline_qlknn/state_history_20260710_114536.nc
```

## Related project files

```text
scripts/imas_torax_config_tglf.py
scripts/imas_torax_config_qlknn.py
scripts/tglf_vs_qlknn_statistics.py
```

## Reinstallation warning

Updating or reinstalling TORAX may replace the modified file inside `site-packages`. If that happens, the patch may need to be applied again.
