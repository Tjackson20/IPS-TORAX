import numpy as np

from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


def normalized_rho(values):
    return np.linspace(0.0, 1.0, len(values))


def compare_profile(name, imas_values, torax_values):
    imas_values = np.asarray(imas_values, dtype=float)
    torax_values = np.asarray(torax_values, dtype=float)

    imas_rho = normalized_rho(imas_values)
    torax_rho = normalized_rho(torax_values)

    torax_on_imas = np.interp(imas_rho, torax_rho, torax_values)
    difference = torax_on_imas - imas_values

    rms = np.sqrt(np.mean(difference**2))
    max_abs = np.max(np.abs(difference))

    denominator = np.maximum(np.abs(imas_values), 1e-30)
    percent = 100.0 * difference / denominator
    max_percent = np.max(np.abs(percent))

    mid = len(imas_values) // 2

    print(f"\n{name}")
    print("-" * len(name))
    print("IMAS points:", len(imas_values))
    print("TORAX points:", len(torax_values))
    print("RMS difference:", f"{rms:.6g}")
    print("Max abs difference:", f"{max_abs:.6g}")
    print("Max percent difference:", f"{max_percent:.3f}%")
    print("Core IMAS/TORAX:", f"{imas_values[0]:.6g}", "/", f"{torax_on_imas[0]:.6g}")
    print("Mid  IMAS/TORAX:", f"{imas_values[mid]:.6g}", "/", f"{torax_on_imas[mid]:.6g}")
    print("Edge IMAS/TORAX:", f"{imas_values[-1]:.6g}", "/", f"{torax_on_imas[-1]:.6g}")


profiles = read_profiles()
equilibrium = read_equilibrium()
torax = read_torax_output()

print("=== IMAS INPUT vs TORAX FULL BASELINE ===")

compare_profile(
    "Electron Temperature (keV)",
    profiles["electron_temperature"] * 1e-3,
    torax["electron_temperature"],
)

compare_profile(
    "Ion Temperature (keV)",
    profiles["ion_average_temperature"] * 1e-3,
    torax["ion_temperature"],
)

compare_profile(
    "Electron Density (m^-3)",
    profiles["electron_density"],
    torax["electron_density"],
)

compare_profile(
    "Safety Factor q",
    equilibrium["q"],
    torax["q_profile"],
)

print("\nPlasma Current")
print("IMAS Ip:", abs(equilibrium["plasma_current"]))
print("TORAX Ip:", torax["plasma_current"])

print("\nFusion Results")
print("TORAX fusion power:", torax["fusion_power"])
print("TORAX fusion gain:", torax["fusion_gain"])