import imas


def read_transport(fpath="data"):
    db = imas.DBEntry(f"imas:hdf5?path={fpath}", "r")
    transport = db.get("core_transport", autoconvert=False)

    data = {
        "time": transport.time.value,
        "models": []
    }

    for model in transport.model:
        data["models"].append({
            "name": model.identifier.name.value,
            "description": model.identifier.description.value
        })

    return data


if __name__ == "__main__":
    data = read_transport()

    print("core_transport loaded successfully")
    print("Time:", data["time"])
    print("Number of models:", len(data["models"]))

    print("\nModels:")
    for model in data["models"]:
        print("-", model["name"])
        print("  ", model["description"])