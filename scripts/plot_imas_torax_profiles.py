from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import matplotlib.pyplot as plt
import numpy as np

from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


plots_dir = Path("plots/imas_vs_torax")
plots_dir.mkdir(parents=True, exist_ok=True)

profiles = read_profiles()
equilibrium = read_equilibrium()
torax_initial = read_torax_output(time_index=0)
torax_final = read_torax_output(time_index=-1)

rho_imas = profiles["rho"]
rho_eq = equilibrium["rho"]

rho_torax_profiles = np.linspace(
    0.0, 1.0, len(torax_initial["electron_temperature"])
)

rho_torax_q = np.linspace(
    0.0, 1.0, len(torax_initial["q_profile"])
)


def make_plot(x_imas, y_imas, x_torax, y_initial, y_final, title, ylabel, filename):
    plt.figure()
    plt.plot(x_imas, y_imas, label="IMAS input")
    plt.plot(x_torax, y_initial, "--", label="TORAX initial state")
    plt.plot(x_torax, y_final, label="TORAX final state")
    plt.xlabel("Normalized radius rho")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(plots_dir / filename, dpi=300, bbox_inches="tight")
    plt.close()


make_plot(
    rho_imas,
    profiles["electron_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["electron_temperature"],
    torax_final["electron_temperature"],
    "Electron Temperature: IMAS Input vs TORAX Initial/Final",
    "Electron temperature (keV)",
    "electron_temperature.png",
)

make_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax_initial["ion_temperature"],
    torax_final["ion_temperature"],
    "Ion Temperature: IMAS Input vs TORAX Initial/Final",
    "Ion temperature (keV)",
    "ion_temperature.png",
)

make_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax_initial["electron_density"],
    torax_final["electron_density"],
    "Electron Density: IMAS Input vs TORAX Initial/Final",
    "Electron density (m^-3)",
    "electron_density.png",
)

make_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax_initial["q_profile"],
    torax_final["q_profile"],
    "Safety Factor q: IMAS Input vs TORAX Initial/Final",
    "q",
    "q_profile.png",
)

print("Plots created successfully in plots/imas_vs_torax/")
