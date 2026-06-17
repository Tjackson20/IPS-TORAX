import h5py

file_path = "../data/core_profiles.h5"

def show_structure(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(f"DATASET: {name} | shape={obj.shape} | dtype={obj.dtype}")
    else:
        print(f"GROUP:   {name}")

with h5py.File(file_path, "r") as f:
    f.visititems(show_structure)