# TORAX Setting Experiments

## Experiment 1: Longer Simulation Time

Question:

What changes if the same direct-IMAS TORAX setup runs longer?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`
- Transport: `constant`
- Solver: `linear`

Experiment:

- Output directory: `torax_outputs/tfinal_1p0`
- Changed setting: `TORAX_T_FINAL=1.0`
- All other settings kept the same.

Run command:

```bash
TORAX_T_FINAL=1.0 /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/tfinal_1p0
```

Latest experiment output:

```text
torax_outputs/tfinal_1p0/state_history_20260624_100815.nc
```

Final-state comparison:

| Metric | Baseline, 0.1 s | Experiment, 1.0 s |
| --- | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 26.2232 |
| `T_i` axis, keV | 21.5374 | 17.6288 |
| `n_e` axis, m^-3 | 1.32161e20 | 1.40896e20 |
| `q` axis | 0.992198 | 0.994879 |
| `Ip`, A | 1.48898e7 | 1.40604e7 |
| `P_fusion`, W | 7.08397e8 | 7.08397e8 |
| `Q_fusion` | 40.3447 | 40.3447 |
| `q95` | 3.18244 | 3.19223 |

Interpretation:

The 1.0 s run continues the same trend seen in the 0.1 s baseline:

- central electron and ion temperatures decrease,
- central electron density increases,
- total plasma current decreases,
- q changes modestly.

This is a useful first setting experiment because only `t_final` changed.

Next suggested experiment:

- Keep `t_final = 0.1`
- Change `n_rho` from `25` to `50`
- Compare whether the profiles and scalar values are grid-sensitive

## Experiment 2: Radial Grid Resolution

Question:

Does the baseline result change strongly when the TORAX radial grid is refined?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- `n_rho = 25`
- `t_final = 0.1`
- `fixed_dt = 0.1`

Experiment:

- Output directory: `torax_outputs/nrho_50`
- Changed setting: `TORAX_N_RHO=50`
- All other settings kept the same.

Run command:

```bash
TORAX_N_RHO=50 /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/nrho_50
```

Latest experiment output:

```text
torax_outputs/nrho_50/state_history_20260624_102831.nc
```

Final-state comparison:

| Metric | Baseline, `n_rho = 25` | Experiment, `n_rho = 50` | Percent change |
| --- | ---: | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 29.4908 | -0.094% |
| `T_i` axis, keV | 21.5374 | 21.5044 | -0.153% |
| `n_e` axis, m^-3 | 1.32161e20 | 1.33153e20 | +0.750% |
| `q` axis | 0.992198 | 1.00586 | +1.377% |
| `Ip`, A | 1.48898e7 | 1.48979e7 | +0.054% |
| `P_fusion`, W | 7.08397e8 | 7.07512e8 | -0.125% |
| `Q_fusion` | 40.3447 | 40.3506 | +0.015% |
| `q95` | 3.18244 | 3.1675 | -0.470% |

Grid sizes:

- `T_e` shape: `(2, 27)` for `n_rho = 25`, `(2, 52)` for `n_rho = 50`
- `q` shape: `(2, 26)` for `n_rho = 25`, `(2, 51)` for `n_rho = 50`

Interpretation:

The refined-grid run gives very similar final values. Most central/scalar
changes are below 1%, and the largest listed change is the central `q` value at
about 1.4%. This suggests the current baseline is not strongly grid-sensitive
for this short `0.1 s` run.

Next suggested experiment:

- Keep `t_final = 0.1`
- Keep `n_rho = 25`
- Turn one source off, starting with `ecrh`, and compare temperature/current
  changes against the baseline

## Experiment 3: Turn Off ECRH

Question:

How much does the prescribed ECRH source affect the short baseline run?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- Sources from IMAS:
  - `ecrh`
  - `fusion`
  - `ohmic`
  - `ei_exchange`
- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`

Experiment:

- Output directory: `torax_outputs/no_ecrh`
- Changed setting: `TORAX_DISABLE_SOURCES=ecrh`
- Remaining sources:
  - `fusion`
  - `ohmic`
  - `ei_exchange`
- All other settings kept the same.

Run command:

```bash
TORAX_DISABLE_SOURCES=ecrh /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/no_ecrh
```

Latest experiment output:

```text
torax_outputs/no_ecrh/state_history_20260624_105821.nc
```

Final-state comparison:

| Metric | Baseline | No ECRH | Percent change |
| --- | ---: | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 29.0733 | -1.509% |
| `T_i` axis, keV | 21.5374 | 21.5374 | +0.000% |
| `n_e` axis, m^-3 | 1.32161e20 | 1.32161e20 | +0.000% |
| `q` axis | 0.992198 | 0.992138 | -0.006% |
| `Ip`, A | 1.48898e7 | 1.48898e7 | +0.000% |
| `P_fusion`, W | 7.08397e8 | 7.08397e8 | +0.000% |
| `Q_fusion` | 40.3447 | 1065.97 | +2542.160% |
| `q95` | 3.18244 | 3.18244 | +0.000% |

Interpretation:

For this short `0.1 s` run, removing ECRH mainly lowers the central electron
temperature. The central ion temperature, density, plasma current, and q values
change very little.

The large increase in `Q_fusion` should be interpreted carefully. Fusion gain
depends on the heating power used in the denominator. Removing ECRH lowers the
external heating power, so the reported gain can increase even when fusion
power itself does not change.

Next suggested experiment:

- Turn off `fusion`, keeping `ecrh`, `ohmic`, and `ei_exchange`
- Compare how much fusion self-heating affects `T_e`, `T_i`, and `P_fusion`

## Experiment 4: Turn Off Fusion

Question:

How much does the fusion source affect the short baseline run?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- Sources from IMAS:
  - `ecrh`
  - `fusion`
  - `ohmic`
  - `ei_exchange`
- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`

Experiment:

- Output directory: `torax_outputs/no_fusion`
- Changed setting: `TORAX_DISABLE_SOURCES=fusion`
- Remaining sources:
  - `ecrh`
  - `ohmic`
  - `ei_exchange`
- All other settings kept the same.

Run command:

```bash
TORAX_DISABLE_SOURCES=fusion /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/no_fusion
```

Latest experiment output:

```text
torax_outputs/no_fusion/state_history_20260624_114155.nc
```

Final-state comparison:

| Metric | Baseline | No fusion | Percent change |
| --- | ---: | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 28.1658 | -4.583% |
| `T_i` axis, keV | 21.5374 | 20.3816 | -5.366% |
| `n_e` axis, m^-3 | 1.32161e20 | 1.32161e20 | +0.000% |
| `q` axis | 0.992198 | 0.992198 | +0.000% |
| `Ip`, A | 1.48898e7 | 1.48898e7 | +0.000% |
| `P_fusion`, W | 7.08397e8 | 0 | -100.000% |
| `Q_fusion` | 40.3447 | 0 | -100.000% |
| `q95` | 3.18244 | 3.18244 | +0.000% |

Interpretation:

Turning off fusion has a larger temperature effect than turning off ECRH in
this short run. Both central electron temperature and central ion temperature
drop by several percent.

The fusion power and fusion gain go to zero, which is expected because the
fusion source is disabled. Density, current, and q values barely change over
this short `0.1 s` window.

Next suggested experiment:

- Turn off `ohmic`, keeping `ecrh`, `fusion`, and `ei_exchange`
- Compare whether current and electron temperature change in the short run

## Experiment 5: Turn Off Ohmic

Question:

How much does the ohmic source affect the short baseline run?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- Sources from IMAS:
  - `ecrh`
  - `fusion`
  - `ohmic`
  - `ei_exchange`
- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`

Experiment:

- Output directory: `torax_outputs/no_ohmic`
- Changed setting: `TORAX_DISABLE_SOURCES=ohmic`
- Remaining sources:
  - `ecrh`
  - `fusion`
  - `ei_exchange`
- All other settings kept the same.

Run command:

```bash
TORAX_DISABLE_SOURCES=ohmic /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/no_ohmic
```

Latest experiment output:

```text
torax_outputs/no_ohmic/state_history_20260624_140416.nc
```

Final-state comparison:

| Metric | Baseline | No ohmic | Percent change |
| --- | ---: | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 29.5165 | -0.007% |
| `T_i` axis, keV | 21.5374 | 21.5374 | +0.000% |
| `n_e` axis, m^-3 | 1.32161e20 | 1.32161e20 | +0.000% |
| `q` axis | 0.992198 | 0.992198 | +0.000% |
| `Ip`, A | 1.48898e7 | 1.48898e7 | +0.000% |
| `P_fusion`, W | 7.08397e8 | 7.08397e8 | +0.000% |
| `Q_fusion` | 40.3447 | 41.9317 | +3.934% |
| `q95` | 3.18244 | 3.18244 | +0.000% |

Interpretation:

For this short `0.1 s` run, turning off ohmic has almost no effect on the
central profiles or global current values. The central electron temperature
drops by only about `0.007%`.

`Q_fusion` increases slightly because the reported gain depends on heating
power. Removing a heating source can change the denominator even when fusion
power itself stays the same.

Next suggested experiment:

- Turn off `ei_exchange`
- Compare whether separating electron-ion energy exchange changes `T_e` and
  `T_i`

## Experiment 6: Turn Off Electron-Ion Exchange

Question:

How much does electron-ion energy exchange affect the short baseline run?

Baseline:

- Output directory: `torax_outputs/imas_direct_minimal`
- Sources from IMAS:
  - `ecrh`
  - `fusion`
  - `ohmic`
  - `ei_exchange`
- `t_final = 0.1`
- `fixed_dt = 0.1`
- `n_rho = 25`

Experiment:

- Output directory: `torax_outputs/no_ei_exchange`
- Changed setting: `TORAX_DISABLE_SOURCES=ei_exchange`
- Remaining sources:
  - `ecrh`
  - `fusion`
  - `ohmic`
- All other settings kept the same.

Run command:

```bash
TORAX_DISABLE_SOURCES=ei_exchange /home/teliyah/miniforge3/envs/TORAX/bin/python \
  -m torax.run_simulation_main \
  --config=scripts/imas_torax_config.py \
  --quit \
  --output_dir=torax_outputs/no_ei_exchange
```

Latest experiment output:

```text
torax_outputs/no_ei_exchange/state_history_20260624_142556.nc
```

Final-state comparison:

| Metric | Baseline | No electron-ion exchange | Percent change |
| --- | ---: | ---: | ---: |
| `T_e` axis, keV | 29.5186 | 29.5186 | +0.000% |
| `T_i` axis, keV | 21.5374 | 21.5374 | +0.000% |
| `n_e` axis, m^-3 | 1.32161e20 | 1.32161e20 | +0.000% |
| `q` axis | 0.992198 | 0.992198 | +0.000% |
| `Ip`, A | 1.48898e7 | 1.48898e7 | +0.000% |
| `P_fusion`, W | 7.08397e8 | 7.08397e8 | +0.000% |
| `Q_fusion` | 40.3447 | 40.3447 | +0.000% |
| `q95` | 3.18244 | 3.18244 | +0.000% |

Interpretation:

For the current short `0.1 s` run and the central/scalar metrics checked here,
turning off `ei_exchange` produces no visible change from the baseline.

This may mean the prescribed electron-ion exchange source is very small in this
case, the short time window is not long enough for the effect to show up in
these simple metrics, or TORAX is still balancing electron-ion exchange through
another internal model path. The next check should look at full radial profiles
or source profile outputs, not only central values and global scalars.

Next suggested experiment:

- Compare full profile differences for all source-off cases
- Add RMS or maximum percent-difference metrics across radius
