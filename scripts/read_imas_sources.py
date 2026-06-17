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
        sources["source_info"][name] = {
            "description": description,
        }

    return sources


if __name__ == "__main__":
    data = read_sources()

    print("core_sources loaded successfully")
    print("Time:", data["time"])
    print("Number of sources:", len(data["source_names"]))

    print("\nSource names:")
    for name in data["source_names"]:
        print("-", name)