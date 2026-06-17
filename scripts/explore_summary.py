import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

summary = db.get("summary", autoconvert=False)

print("Time:")
print(summary.time)

print("\nAvailable sections:")
print(dir(summary))

print("\nTau energy:")
print(summary.global_quantities.tau_energy.value.value[0])

print("\nPlasma duration:")
print(summary.plasma_duration.value)