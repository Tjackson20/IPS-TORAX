from torax._src.imas_tools.input import loader, core_profiles

IMAS_URI = "imas:hdf5?path=data"

core_profiles_ids = loader.load_imas_data(
    IMAS_URI,
    "core_profiles",
    explicit_convert=True,
)

profile_conditions = core_profiles.profile_conditions_from_IMAS(
    core_profiles_ids
)

plasma_composition = core_profiles.plasma_composition_from_IMAS(
    core_profiles_ids
)

print("Loaded IMAS directly with TORAX tools")

print("\nProfile condition keys:")
for key in profile_conditions:
    print("-", key)

print("\nPlasma composition keys:")
for key in plasma_composition:
    print("-", key)

print("\nFirst T_e value from TORAX IMAS loader:")
print(profile_conditions["T_e"][2][0][0])

print("\nFirst n_e value from TORAX IMAS loader:")
print(profile_conditions["n_e"][2][0][0])
