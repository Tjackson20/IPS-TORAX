from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import matplotlib.pyplot as plt
import numpy as np

from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


plots_dir = Path("plots/imas_vs_qualikiz")
plots_dir.mkdir(parents=True, exist_ok=True)

diff_dir = Path("plots/imas_vs_qualikiz_difference")
diff_dir.mkdir(parents=True, exist_ok=True)

profiles = read_profiles()
equilibrium = read_equilibrium()
qualikiz_output = "torax_outputs/qualikiz/state_history_20260723_104024.nc"
torax_initial = read_torax_output(output_file=qualikiz_output, time_index=0)
torax_final = read_torax_output(output_file=qualikiz_output, time_index=-1)

rho_imas = profiles["rho"]
rho_eq = equilibrium["rho"]

rho_torax_profiles = np.linspace(0.0, 1.0, len(torax_final["electron_temperature"]))
rho_torax_q = np.linspace(0.0, 1.0, len(torax_final["q_profile"]))


def make_plot(x_imas, y_imas, x_torax, y_initial, y_final, title, ylabel, filename):
    plt.figure()
    plt.plot(x_imas, y_imas, label="IMAS input")
    plt.plot(x_torax, y_initial, "--", label="QuaLiKiz initial state")
    plt.plot(x_torax, y_final, label="QuaLiKiz final state")
    plt.xlabel("Normalized radius rho")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(plots_dir / filename, dpi=300, bbox_inches="tight")
    plt.close()


def make_difference_plot(x_imas, y_imas, x_torax, y_torax, title, ylabel, filename):
    torax_on_imas = np.interp(x_imas, x_torax, y_torax)
    difference = torax_on_imas - y_imas

    plt.figure()
    plt.plot(x_imas, difference)
    plt.axhline(0.0, linestyle="--")
    plt.xlabel("Normalized radius rho")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(diff_dir / filename, dpi=300, bbox_inches="tight")
    plt.close()


make_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["electron_temperature"],
    torax_final["electron_temperature"],
    "Electron Temperature: IMAS Input vs QuaLiKiz Initial/Final",
    "Electron temperature (keV)",
    "electron_temperature.png",
)

make_difference_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_final["electron_temperature"],
    "Difference: QuaLiKiz Final - IMAS Electron Temperature",
    "Difference in electron temperature (keV)",
    "difference_electron_temperature.png",
)

make_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["ion_temperature"],
    torax_final["ion_temperature"],
    "Ion Temperature: IMAS Input vs QuaLiKiz Initial/Final",
    "Ion temperature (keV)",
    "ion_temperature.png",
)

make_difference_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_final["ion_temperature"],
    "Difference: QuaLiKiz Final - IMAS Ion Temperature",
    "Difference in ion temperature (keV)",
    "difference_ion_temperature.png",
)

make_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax_initial["electron_density"],
    torax_final["electron_density"],
    "Electron Density: IMAS Input vs QuaLiKiz Initial/Final",
    "Electron density (m^-3)",
    "electron_density.png",
)

make_plot(
    rho_imas,
    profiles["ion_density"],
    rho_torax_profiles,
    torax_initial["ion_density"],
    torax_final["ion_density"],
    "Ion Density: IMAS Input vs QuaLiKiz Initial/Final",
    "Ion density (m^-3)",
    "ion_density.png",
)

make_plot(
    rho_imas,
    profiles["ion_density"],
    rho_torax_profiles,
    torax_initial["ion_density"],
    torax_final["ion_density"],
    "Ion Density: IMAS Input vs QuaLiKiz Initial/Final",
    "Ion density (m^-3)",
    "ion_density.png",
)
make_difference_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax_final["electron_density"],
    "Difference: QuaLiKiz Final - IMAS Electron Density",
    "Difference in electron density (m^-3)",
    "difference_electron_density.png",
)

make_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax_initial["q_profile"],
    torax_final["q_profile"],
    "Safety Factor q: IMAS Input vs QuaLiKiz Initial/Final",
    "q",
    "q_profile.png",
)

make_difference_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax_final["q_profile"],
    "Difference: QuaLiKiz Final - IMAS q",
    "Difference in q",
    "difference_q_profile.png",
)

print("Plots created successfully in plots/imas_vs_qualikiz/")
print("Difference plots created successfully in plots/imas_vs_qualikiz_difference/")
