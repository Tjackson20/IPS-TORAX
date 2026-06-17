import imas

db = imas.DBEntry("imas:hdf5?path=data", "r")

sources = db.get("core_sources", autoconvert=False)

print("Time:")
print(sources.time)

print("Number of sources:")
print(len(sources.source))

for i, src in enumerate(sources.source):
    print(f"\nSource {i}:")
    print("Name:", src.identifier.name)