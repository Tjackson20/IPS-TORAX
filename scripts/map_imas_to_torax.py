from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from read_imas_sources import read_sources


def build_torax_input():
    profiles = read_profiles()
    equilibrium = read_equilibrium()
    sources = read_sources()

    torax_input = {
        "time": profiles["time"],

        # Plasma profiles
        "rho": profiles["rho"],
        "electron_temperature": profiles["electron_temperature"],
        "electron_density": profiles["electron_density"],
        "ion_temperature": profiles["ion_average_temperature"],
        "zeff": profiles["zeff"],
        "electron_pressure": profiles["electron_pressure"],
        "ion_pressure_total": profiles["ion_pressure_total"],
        "pressure_thermal": profiles["pressure_thermal"],
        "volume_profile": profiles["volume"],
        "ion_species_names": profiles["ion_species_names"],

        # Equilibrium quantities
        "q_profile": equilibrium["q"],
        "psi_profile": equilibrium["psi"],
        "plasma_current": equilibrium["plasma_current"],
        "r0": equilibrium["r0"],
"b0": equilibrium["b0"],
"volume": equilibrium["volume"],
"area": equilibrium["area"],
"elongation": equilibrium["elongation"],
"triangularity_upper": equilibrium["triangularity_upper"],
"triangularity_lower": equilibrium["triangularity_lower"],

        # Source information
        "source_names": sources["source_names"],
    }

    return torax_input


if __name__ == "__main__":
    torax_input = build_torax_input()

    print("TORAX input dictionary created successfully")

    print("\nKeys:")
    for key in torax_input:
        print("-", key)
        