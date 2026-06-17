from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium


profiles = read_profiles()
equilibrium = read_equilibrium()

print("=== TIME CHECK ===")
print("Profiles time:", profiles["time"])
print("Equilibrium time:", equilibrium["time"])

print("\n=== RHO CHECK ===")
print("Profiles rho points:", len(profiles["rho"]))
print("Equilibrium rho points:", len(equilibrium["rho"]))

if len(profiles["rho"]) == len(equilibrium["rho"]):
    print("\nRho grids have the same number of points.")
else:
    print("\nRho grids are different.")