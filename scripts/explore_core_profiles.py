import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

core_profiles = db.get("core_profiles", autoconvert=False)

print("Time:")
print(core_profiles.time)

print("\nNumber of profile slices:")
print(len(core_profiles.profiles_1d))
profile = core_profiles.profiles_1d[0]

print("\nElectron temperature:")
print(profile.electrons.temperature.value)

print("\nElectron density:")
print(profile.electrons.density.value)

print("\nIon average temperature:")
print(profile.t_i_average.value)

print("\nRho grid:")
print(profile.grid.rho_tor_norm.value)