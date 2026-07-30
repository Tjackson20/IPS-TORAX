from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np

from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


plots_dir = Path("plots/imas_vs_tglf_rho05_095")
plots_dir.mkdir(parents=True, exist_ok=True)

diff_dir = Path("plots/imas_vs_tglf_rho05_095_difference")
diff_dir.mkdir(parents=True, exist_ok=True)

profiles = read_profiles()
equilibrium = read_equilibrium()

tglf_output = (
    "torax_outputs/tglf_modified_rho05_095/"
    "state_history_20260730_132029.nc"
)

torax_initial = read_torax_output(
    output_file=tglf_output,
    time_index=0,
)

torax_final = read_torax_output(
    output_file=tglf_output,
    time_index=-1,
)

rho_imas = profiles["rho"]
rho_eq = equilibrium["rho"]

rho_torax_profiles = np.linspace(
    0.0,
    1.0,
    len(torax_final["electron_temperature"]),
)

rho_torax_q = np.linspace(
    0.0,
    1.0,
    len(torax_final["q_profile"]),
)


def make_plot(
    x_imas,
    y_imas,
    x_torax,
    y_initial,
    y_final,
    title,
    ylabel,
    filename,
):
    plt.figure(figsize=(8, 6))

    plt.plot(
        x_imas,
        y_imas,
        linewidth=2,
        label="IMAS reference",
    )

    plt.plot(
        x_torax,
        y_initial,
        "--",
        linewidth=2,
        label="Initial TORAX",
    )

    plt.plot(
        x_torax,
        y_final,
        linewidth=2,
        label="Final TGLF",
    )

    plt.xlabel("Normalized radius rho")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        plots_dir / filename,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def make_difference_plot(
    x_imas,
    y_imas,
    x_torax,
    y_torax,
    title,
    ylabel,
    filename,
):
    torax_on_imas = np.interp(
        x_imas,
        x_torax,
        y_torax,
    )

    difference = torax_on_imas - y_imas

    plt.figure(figsize=(8, 6))

    plt.plot(
        x_imas,
        difference,
        linewidth=2,
    )

    plt.axhline(
        0.0,
        linestyle="--",
    )

    plt.xlabel("Normalized radius rho")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        diff_dir / filename,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


make_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["electron_temperature"],
    torax_final["electron_temperature"],
    "Electron Temperature: IMAS vs Initial TORAX and Final TGLF",
    "Electron temperature (keV)",
    "electron_temperature.png",
)

make_difference_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_final["electron_temperature"],
    "Difference: Final TGLF - IMAS Electron Temperature",
    "Difference in electron temperature (keV)",
    "difference_electron_temperature.png",
)

make_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["ion_temperature"],
    torax_final["ion_temperature"],
    "Ion Temperature: IMAS vs Initial TORAX and Final TGLF",
    "Ion temperature (keV)",
    "ion_temperature.png",
)

make_difference_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_final["ion_temperature"],
    "Difference: Final TGLF - IMAS Ion Temperature",
    "Difference in ion temperature (keV)",
    "difference_ion_temperature.png",
)

make_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax_initial["electron_density"],
    torax_final["electron_density"],
    "Electron Density: IMAS vs Initial TORAX and Final TGLF",
    "Electron density (m^-3)",
    "electron_density.png",
)

make_difference_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax_final["electron_density"],
    "Difference: Final TGLF - IMAS Electron Density",
    "Difference in electron density (m^-3)",
    "difference_electron_density.png",
)

make_plot(
    rho_imas,
    profiles["ion_density"],
    rho_torax_profiles,
    torax_initial["ion_density"],
    torax_final["ion_density"],
    "Ion Density: IMAS vs Initial TORAX and Final TGLF",
    "Ion density (m^-3)",
    "ion_density.png",
)

make_difference_plot(
    rho_imas,
    profiles["ion_density"],
    rho_torax_profiles,
    torax_final["ion_density"],
    "Difference: Final TGLF - IMAS Ion Density",
    "Difference in ion density (m^-3)",
    "difference_ion_density.png",
)

make_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax_initial["q_profile"],
    torax_final["q_profile"],
    "Safety Factor q: IMAS vs Initial TORAX and Final TGLF",
    "q",
    "q_profile.png",
)

make_difference_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax_final["q_profile"],
    "Difference: Final TGLF - IMAS Safety Factor q",
    "Difference in q",
    "difference_q_profile.png",
)

print("Plots created successfully in:")
print(plots_dir)

print("Difference plots created successfully in:")
print(diff_dir)