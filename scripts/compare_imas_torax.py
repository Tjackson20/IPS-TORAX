from read_imas_profiles import read_profiles
from read_imas_equilibrium import read_equilibrium
from map_torax_to_imas import read_torax_output


profiles = read_profiles()
equilibrium = read_equilibrium()
torax = read_torax_output()

print("=== IMAS INPUT vs TORAX OUTPUT ===")

print("\nElectron Temperature")
print("IMAS first value, keV:", profiles["electron_temperature"][0] * 1e-3)
print("TORAX first value, keV:", torax["electron_temperature"][0])

print("\nIon Temperature")
print("IMAS first value, keV:", profiles["ion_average_temperature"][0] * 1e-3)
print("TORAX first value, keV:", torax["ion_temperature"][0])

print("\nElectron Density")
print("IMAS first value:", profiles["electron_density"][0])
print("TORAX first value:", torax["electron_density"][0])

print("\nPlasma Current")
print("IMAS Ip:", abs(equilibrium["plasma_current"]))
print("TORAX Ip:", torax["plasma_current"])

print("\nq Profile")
print("IMAS first q:", equilibrium["q"][0])
print("TORAX first q:", torax["q_profile"][0])

print("\nFusion Results")
print("TORAX fusion power:", torax["fusion_power"])
print("TORAX fusion gain:", torax["fusion_gain"])
