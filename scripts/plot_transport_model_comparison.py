from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np

from read_imas_profiles import read_profiles
from map_torax_to_imas import read_torax_output


plots_dir = Path("plots/transport_model_comparison")
plots_dir.mkdir(parents=True, exist_ok=True)

profiles = read_profiles()

qualikiz_output = (
    "torax_outputs/qualikiz/"
    "state_history_20260723_104024.nc"
)

tglf_output = (
    "torax_outputs/tglf_modified_rho05_095/"
    "state_history_20260730_132029.nc"
)

qualikiz_initial = read_torax_output(
    output_file=qualikiz_output,
    time_index=0,
)

qualikiz_final = read_torax_output(
    output_file=qualikiz_output,
    time_index=-1,
)

tglf_final = read_torax_output(
    output_file=tglf_output,
    time_index=-1,
)

rho_imas = profiles["rho"]

rho_qualikiz = np.linspace(
    0.0,
    1.0,
    len(qualikiz_final["electron_temperature"]),
)

rho_tglf = np.linspace(
    0.0,
    1.0,
    len(tglf_final["electron_temperature"]),
)


def make_plot(
    x_imas,
    y_imas,
    x_initial,
    y_initial,
    x_qualikiz,
    y_qualikiz,
    x_tglf,
    y_tglf,
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
        x_initial,
        y_initial,
        linestyle="--",
        linewidth=2,
        label="Initial TORAX",
    )

    plt.plot(
        x_qualikiz,
        y_qualikiz,
        linewidth=2,
        label="Final QuaLiKiz",
    )

    plt.plot(
        x_tglf,
        y_tglf,
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


make_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_qualikiz,
    qualikiz_initial["electron_temperature"],
    rho_qualikiz,
    qualikiz_final["electron_temperature"],
    rho_tglf,
    tglf_final["electron_temperature"],
    "Electron Temperature Comparison",
    "Electron temperature (keV)",
    "electron_temperature_comparison.png",
)

make_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_qualikiz,
    qualikiz_initial["ion_temperature"],
    rho_qualikiz,
    qualikiz_final["ion_temperature"],
    rho_tglf,
    tglf_final["ion_temperature"],
    "Ion Temperature Comparison",
    "Ion temperature (keV)",
    "ion_temperature_comparison.png",
)

make_plot(
    rho_imas,
    profiles["electron_density"],
    rho_qualikiz,
    qualikiz_initial["electron_density"],
    rho_qualikiz,
    qualikiz_final["electron_density"],
    rho_tglf,
    tglf_final["electron_density"],
    "Electron Density Comparison",
    "Electron density (m^-3)",
    "electron_density_comparison.png",
)

make_plot(
    rho_imas,
    profiles["ion_density"],
    rho_qualikiz,
    qualikiz_initial["ion_density"],
    rho_qualikiz,
    qualikiz_final["ion_density"],
    rho_tglf,
    tglf_final["ion_density"],
    "Ion Density Comparison",
    "Ion density (m^-3)",
    "ion_density_comparison.png",
)

print("Plots created successfully in:")
print(plots_dir)