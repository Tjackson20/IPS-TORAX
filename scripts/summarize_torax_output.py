import xarray as xr

from map_torax_to_imas import get_latest_torax_output


output_file = get_latest_torax_output()

profiles = xr.open_dataset(output_file, group="profiles")
scalars = xr.open_dataset(output_file, group="scalars")
numerics = xr.open_dataset(output_file, group="numerics")

print("=== TORAX OUTPUT SUMMARY ===")
print("Output file:", output_file)

print("\nProfile variables:")
for var in ["T_e", "T_i", "n_e", "q", "psi", "j_total", "pressure_total"]:
    if var in profiles:
        print(f"- {var}: shape {profiles[var].shape}")

print("\nScalar variables:")
for var in ["Ip", "tau_E", "P_fusion", "Q_fusion", "q95", "q_min", "W_thermal_total"]:
    if var in scalars:
        print(f"- {var}: final value = {scalars[var].values[-1]}")

print("\nNumerics:")
print(numerics)
