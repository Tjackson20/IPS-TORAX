from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


plots_dir = Path("plots/imas_vs_torax")
plots_dir.mkdir(parents=True, exist_ok=True)

profiles = read_profiles()
equilibrium = read_equilibrium()
torax = read_torax_output()

rho_imas = profiles["rho"]
rho_eq = equilibrium["rho"]

rho_torax_profiles = np.linspace(
    0.0, 1.0, len(torax["electron_temperature"])
)

rho_torax_q = np.linspace(
    0.0, 1.0, len(torax["q_profile"])
)


def make_plot(x1, y1, x2, y2, title, ylabel, filename):
    plt.figure()
    plt.plot(x1, y1, label="IMAS input")
    plt.plot(x2, y2, label="TORAX output final state")
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
    torax["electron_temperature"],
    "Electron Temperature: IMAS Input vs TORAX Final State",
    "Electron temperature (keV)",
    "electron_temperature.png",
)

make_plot(
    rho_imas,
    profiles["ion_average_temperature"] * 1e-3,
    rho_torax_profiles,
    torax["ion_temperature"],
    "Ion Temperature: IMAS Input vs TORAX Final State",
    "Ion temperature (keV)",
    "ion_temperature.png",
)

make_plot(
    rho_imas,
    profiles["electron_density"],
    rho_torax_profiles,
    torax["electron_density"],
    "Electron Density: IMAS Input vs TORAX Final State",
    "Electron density (m^-3)",
    "electron_density.png",
)

make_plot(
    rho_eq,
    equilibrium["q"],
    rho_torax_q,
    torax["q_profile"],
    "Safety Factor q: IMAS Input vs TORAX Final State",
    "q",
    "q_profile.png",
)

print("Plots created successfully in plots/imas_vs_torax/")