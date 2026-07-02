from pathlib import Path
import xarray as xr


def get_latest_torax_output(output_dir="torax_outputs/full_baseline_nrho200"):
    output_path = Path(output_dir)
    files = sorted(output_path.glob("state_history_*.nc"))

    if not files:
        raise FileNotFoundError(
            f"No TORAX output files found in {output_dir}. "
            "Run TORAX first."
        )

    return str(files[-1])


def read_torax_output(output_file=None, time_index=-1):
    if output_file is None:
        output_file = get_latest_torax_output()

    print("Reading TORAX output file:")
    print(output_file)

    profiles = xr.open_dataset(output_file, group="profiles")
    scalars = xr.open_dataset(output_file, group="scalars")

    torax_data = {
        # Profile outputs
        "electron_temperature": profiles["T_e"].values[time_index],
        "ion_temperature": profiles["T_i"].values[time_index],
        "electron_density": profiles["n_e"].values[time_index],
        "q_profile": profiles["q"].values[time_index],
        "psi_profile": profiles["psi"].values[time_index],
        "current_profile": profiles["j_total"].values[time_index],
        "pressure_profile": profiles["pressure_total"].values[time_index],

        # Scalar outputs
        "plasma_current": scalars["Ip"].values[time_index],
        "tau_E": scalars["tau_E"].values[time_index],
        "fusion_power": scalars["P_fusion"].values[time_index],
        "fusion_gain": scalars["Q_fusion"].values[time_index],
        "q95": scalars["q95"].values[time_index],
    }

    return torax_data


if __name__ == "__main__":
    data = read_torax_output()

    print("\nTORAX output loaded successfully")

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
