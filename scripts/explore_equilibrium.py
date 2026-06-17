import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

equilibrium = db.get("equilibrium", autoconvert=False)

print("Time:")
print(equilibrium.time)

print("\nNumber of time slices:")
print(len(equilibrium.time_slice))
eq_slice = equilibrium.time_slice[0]

print("\nMagnetic axis R:")
print(eq_slice.global_quantities.magnetic_axis.r.value)

print("\nMagnetic axis Z:")
print(eq_slice.global_quantities.magnetic_axis.z.value)

print("\nPlasma current Ip:")
print(eq_slice.global_quantities.ip.value)

print("\nq profile:")
print(eq_slice.profiles_1d.q.value)

print("\npsi profile:")
print(eq_slice.profiles_1d.psi.value)

print("\nBoundary R points:")
print(eq_slice.boundary.outline.r.value)

print("\nBoundary Z points:")
print(eq_slice.boundary.outline.z.value)