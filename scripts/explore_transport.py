import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

transport = db.get("core_transport", autoconvert=False)

print("Time:")
print(transport.time)

print("Number of model entries:")
print(len(transport.model))
for i, model in enumerate(transport.model):
    print(f"\nModel {i}:")
    print("Name:", model.identifier.name)
    print("Description:", model.identifier.description)