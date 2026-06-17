import imas


def read_equilibrium(fpath="data"):
    db = imas.DBEntry(f"imas:hdf5?path={fpath}", "r")
    equilibrium = db.get("equilibrium", autoconvert=False)

    eq_slice = equilibrium.time_slice[0]

    equilibrium_data = {
        "time": equilibrium.time.value,
        "r0": equilibrium.vacuum_toroidal_field.r0.value,
        "b0": equilibrium.vacuum_toroidal_field.b0.value[0],
        "rho": eq_slice.profiles_1d.rho_tor_norm.value,
        "rho_tor": eq_slice.profiles_1d.rho_tor.value,
        "q": eq_slice.profiles_1d.q.value,
        "psi": eq_slice.profiles_1d.psi.value,
        "phi": eq_slice.profiles_1d.phi.value,
        "pressure": eq_slice.profiles_1d.pressure.value,
        "volume": eq_slice.profiles_1d.volume.value,
        "area": eq_slice.profiles_1d.area.value,
        "elongation": eq_slice.profiles_1d.elongation.value,
        "triangularity_upper": eq_slice.profiles_1d.triangularity_upper.value,
        "triangularity_lower": eq_slice.profiles_1d.triangularity_lower.value,
        "plasma_current": eq_slice.global_quantities.ip.value,
        "q_95": eq_slice.global_quantities.q_95.value,
        "q_min": eq_slice.global_quantities.q_min.value,
        "psi_axis": eq_slice.global_quantities.psi_axis.value,
        "psi_boundary": eq_slice.global_quantities.psi_boundary.value,
        "magnetic_axis_r": eq_slice.global_quantities.magnetic_axis.r.value,
        "magnetic_axis_z": eq_slice.global_quantities.magnetic_axis.z.value,
        "boundary_r": eq_slice.boundary.outline.r.value,
        "boundary_z": eq_slice.boundary.outline.z.value,
    }

    return equilibrium_data


if __name__ == "__main__":
    data = read_equilibrium()

    print("equilibrium loaded successfully")
    print("Time:", data["time"])
    print("Number of rho points:", len(data["rho"]))
    print("Plasma current:", data["plasma_current"])
    print("Magnetic axis R/Z:", data["magnetic_axis_r"], data["magnetic_axis_z"])
    print("R0:", data["r0"])
    print("B0:", data["b0"])
    print("q95:", data["q_95"])
    print("qmin:", data["q_min"])
    print("Volume points:", len(data["volume"]))