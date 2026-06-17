import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

summary = db.get("summary", autoconvert=False)

print("Summary loaded successfully")
print("Tau energy:")
print(summary.global_quantities.tau_energy.value.value[0])