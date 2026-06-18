import xarray as xr


def read_torax_output(
    output_file="/tmp/torax_results/state_history_20260618_102656.nc",
):
    profiles = xr.open_dataset(output_file, group="profiles")
    scalars = xr.open_dataset(output_file, group="scalars")

    torax_data = {
        # Profile outputs
        "electron_temperature": profiles["T_e"].values[-1],
        "ion_temperature": profiles["T_i"].values[-1],
        "electron_density": profiles["n_e"].values[-1],
        "q_profile": profiles["q"].values[-1],
        "psi_profile": profiles["psi"].values[-1],
        "current_profile": profiles["j_total"].values[-1],
        "pressure_profile": profiles["pressure_total"].values[-1],

        # Scalar outputs
        "plasma_current": scalars["Ip"].values[-1],
        "tau_E": scalars["tau_E"].values[-1],
        "fusion_power": scalars["P_fusion"].values[-1],
        "fusion_gain": scalars["Q_fusion"].values[-1],
        "q95": scalars["q95"].values[-1],
    }

    return torax_data


if __name__ == "__main__":
    data = read_torax_output()

    print("TORAX output loaded successfully")

    print("\nKeys:")
    for key in data:
        print("-", key)

    print("\nElectron temperature first 5:")
    print(data["electron_temperature"][:5])

    print("\nElectron density first 5:")
    print(data["electron_density"][:5])

    print("\nq profile first 5:")
    print(data["q_profile"][:5])

    print("\nFusion power:")
    print(data["fusion_power"])

    print("\nQ fusion:")
    print(data["fusion_gain"])