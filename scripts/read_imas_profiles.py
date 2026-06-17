import imas


def read_profiles(fpath="data"):
    db = imas.DBEntry(f"imas:hdf5?path={fpath}", "r")
    core_profiles = db.get("core_profiles", autoconvert=False)

    profile = core_profiles.profiles_1d[0]

    profiles = {
        "time": core_profiles.time.value,
        "rho": profile.grid.rho_tor_norm.value,
        "electron_temperature": profile.electrons.temperature.value,
        "electron_density": profile.electrons.density.value,
        "electron_pressure": profile.electrons.pressure.value,
        "electron_pressure_thermal": profile.electrons.pressure_thermal.value,
        "ion_average_temperature": profile.t_i_average.value,
        "ion_pressure_total": profile.pressure_ion_total.value,
        "pressure_thermal": profile.pressure_thermal.value,
        "volume": profile.grid.volume.value,
        "zeff": profile.zeff.value,
        "q": profile.q.value,
        "ion_species_names": [],
    }

    for ion in profile.ion:
        profiles["ion_species_names"].append(str(ion.label))

    return profiles


if __name__ == "__main__":
    data = read_profiles()

    print("core_profiles loaded successfully")
    print("Time:", data["time"])
    print("Number of rho points:", len(data["rho"]))
    print("Electron temperature first/last:", data["electron_temperature"][0], data["electron_temperature"][-1])
    print("Electron density first/last:", data["electron_density"][0], data["electron_density"][-1])
    print("Volume points:", len(data["volume"]))
    print("Ion species:", data["ion_species_names"])