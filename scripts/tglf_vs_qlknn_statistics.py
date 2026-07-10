from pathlib import Path

import numpy as np
import xarray as xr


TGLF_FILE = Path(
    "torax_outputs/full_baseline_tglf/state_history_20260710_115025.nc"
)
QLKNN_FILE = Path(
    "torax_outputs/full_baseline_qlknn/state_history_20260710_114536.nc"
)

# The plasma variables are stored in the profiles group.
tglf_profiles = xr.open_dataset(TGLF_FILE, group="profiles")
qlknn_profiles = xr.open_dataset(QLKNN_FILE, group="profiles")

# The radial coordinates are stored in the root group.
tglf_root = xr.open_dataset(TGLF_FILE)
qlknn_root = xr.open_dataset(QLKNN_FILE)

variables = {
    "T_e": ("Electron Temperature", "keV", "rho_norm"),
    "T_i": ("Ion Temperature", "keV", "rho_norm"),
    "n_e": ("Electron Density", "m^-3", "rho_norm"),
    "n_i": ("Ion Density", "m^-3", "rho_norm"),
    "q": ("Safety Factor", "unitless", "rho_face_norm"),
}

ranges = [
    (0.0, 1.0),
    (0.1, 0.9),
    (0.5, 1.0),
]

print("TGLF :", TGLF_FILE)
print("QLKNN:", QLKNN_FILE)

for rho_min, rho_max in ranges:
    print("\n" + "=" * 74)
    print(f"RADIAL RANGE: rho = {rho_min:.1f} to {rho_max:.1f}")
    print("=" * 74)

    for variable, (label, unit, rho_name) in variables.items():
        tglf_profile = np.asarray(
            tglf_profiles[variable].isel(time=-1).values,
            dtype=float,
        )
        qlknn_profile = np.asarray(
            qlknn_profiles[variable].isel(time=-1).values,
            dtype=float,
        )

        tglf_rho = np.asarray(tglf_root[rho_name].values, dtype=float)
        qlknn_rho = np.asarray(qlknn_root[rho_name].values, dtype=float)

        if not np.allclose(tglf_rho, qlknn_rho):
            raise ValueError(
                f"{rho_name} grids do not match between TGLF and QLKNN."
            )

        rho = tglf_rho

        if len(rho) != len(tglf_profile):
            raise ValueError(
                f"{variable}: radial grid has {len(rho)} points, "
                f"but profile has {len(tglf_profile)} points."
            )

        mask = (rho >= rho_min) & (rho <= rho_max)

        if not np.any(mask):
            raise ValueError(
                f"No radial points found for rho={rho_min} to {rho_max}."
            )

        tglf_selected = tglf_profile[mask]
        qlknn_selected = qlknn_profile[mask]
        rho_selected = rho[mask]

        difference = tglf_selected - qlknn_selected
        absolute_difference = np.abs(difference)

        max_index = int(np.argmax(absolute_difference))
        rms_difference = np.sqrt(np.mean(difference**2))

        print(f"\n{label}")
        print("-" * 52)
        print(
            f"Maximum difference : "
            f"{absolute_difference[max_index]:.6g} {unit}"
        )
        print(
            f"Mean difference    : "
            f"{np.mean(absolute_difference):.6g} {unit}"
        )
        print(
            f"RMS difference     : "
            f"{rms_difference:.6g} {unit}"
        )
        print(f"rho at maximum     : {rho_selected[max_index]:.3f}")
        print(
            f"TGLF value at max  : "
            f"{tglf_selected[max_index]:.6g} {unit}"
        )
        print(
            f"QLKNN value at max : "
            f"{qlknn_selected[max_index]:.6g} {unit}"
        )
        print(
            f"Signed difference  : "
            f"{difference[max_index]:.6g} {unit}"
        )
