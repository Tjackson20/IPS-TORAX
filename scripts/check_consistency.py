from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from read_imas_sources import read_sources
from read_imas_transport import read_transport


profiles = read_profiles()
equilibrium = read_equilibrium()
sources = read_sources()
transport = read_transport()

print("=== TIME CHECK ===")
print("Profiles time:", profiles["time"])
print("Equilibrium time:", equilibrium["time"])
print("Sources time:", sources["time"])
print("Transport time:", transport["time"])

print("\n=== RHO CHECK ===")
print("Profiles rho points:", len(profiles["rho"]))
print("Equilibrium rho points:", len(equilibrium["rho"]))

if len(profiles["rho"]) == len(equilibrium["rho"]):
    print("Profiles and equilibrium have the same number of rho points.")
else:
    print("Profiles and equilibrium have different rho point counts.")

print("\n=== SUMMARY ===")
print("All main IMAS readers loaded successfully.")