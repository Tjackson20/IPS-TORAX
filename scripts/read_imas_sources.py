import imas


def read_sources(fpath="data"):
    db = imas.DBEntry(f"imas:hdf5?path={fpath}", "r")
    core_sources = db.get("core_sources", autoconvert=False)

    sources = {
        "time": core_sources.time.value,
        "source_names": [],
        "source_info": {},
    }

    for src in core_sources.source:
        name = src.identifier.name.value
        description = src.identifier.description.value

        sources["source_names"].append(name)

        source_data = {
            "description": description,
        }

        if len(src.profiles_1d) > 0:
            profile = src.profiles_1d[0]

            source_data["rho"] = profile.grid.rho_tor_norm.value
            source_data["j_parallel"] = profile.j_parallel.value
            source_data["electron_energy"] = profile.electrons.energy.value
            source_data["ion_energy"] = profile.total_ion_energy.value
            source_data["electron_particles"] = profile.electrons.particles.value

        sources["source_info"][name] = source_data

    return sources


if __name__ == "__main__":
    data = read_sources()

    print("core_sources loaded successfully")
    print("Time:", data["time"])
    print("Number of sources:", len(data["source_names"]))

    print("\nSource names and available data:")
    for name in data["source_names"]:
        info = data["source_info"][name]
        print(f"\n{name}")
        print("Description:", info["description"])

        if "rho" in info:
            print("Rho points:", len(info["rho"]))
            print("Has j_parallel:", len(info["j_parallel"]))
            print("Has electron_energy:", len(info["electron_energy"]))
            print("Has ion_energy:", len(info["ion_energy"]))
            print("Has electron_particles:", len(info["electron_particles"]))