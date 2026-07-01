"""Minimal TORAX configuration driven directly by local IMAS HDF5 IDSs."""

import copy
import os

import imas
from torax._src.imas_tools.input import core_profiles
from torax._src.imas_tools.input import core_sources
from torax._src.imas_tools.input import loader


IMAS_URI = "imas:hdf5?path=data"
T_INITIAL = 0.0
T_FINAL = float(os.environ.get("TORAX_T_FINAL", "0.1"))
FIXED_DT = float(os.environ.get("TORAX_FIXED_DT", "0.1"))
N_RHO = int(os.environ.get("TORAX_N_RHO", "25"))
DISABLED_SOURCES = {
    source.strip()
    for source in os.environ.get("TORAX_DISABLE_SOURCES", "").split(",")
    if source.strip()
}


def _with_initial_time(value, t_initial=T_INITIAL):
    """Replace empty IMAS time scalars in TORAX tuple inputs."""
    if isinstance(value, tuple) and len(value) in (2, 3):
        return ([t_initial], *value[1:])
    if isinstance(value, dict):
        return {key: _with_initial_time(val, t_initial) for key, val in value.items()}
    return value


def _load_ids(ids_name):
    return loader.load_imas_data(
        IMAS_URI,
        ids_name,
        explicit_convert=True,
    )


def _profile_conditions_from_imas(core_profiles_ids, equilibrium_ids):
    profile_conditions = dict(
        core_profiles.profile_conditions_from_IMAS(core_profiles_ids)
    )

    equilibrium_xr = imas.util.to_xarray(equilibrium_ids)
    profile_conditions["Ip"] = float(
        -equilibrium_xr["time_slice.global_quantities.ip"][0].item()
    )
    profile_conditions["use_v_loop_lcfs_boundary_condition"] = True
    profile_conditions["v_loop_lcfs"] = 0.0

    return _with_initial_time(profile_conditions)


def _sources_from_imas(core_sources_ids):
    sources = copy.deepcopy(core_sources.sources_from_IMAS(core_sources_ids))

    sources.pop("icrh", None)

    for source_name in DISABLED_SOURCES:
        sources.pop(source_name, None)

    for source_name in list(sources):
        source_config = sources[source_name]
        prescribed_values = []

        for times, rho_norm, profile in source_config.get("prescribed_values", ()):
            if not profile or len(profile[0]) == 0:
                continue
            prescribed_values.append(([T_INITIAL], rho_norm, profile))

        if prescribed_values:
            source_config["prescribed_values"] = tuple(prescribed_values)
        else:
            del sources[source_name]

    nbi_rho = None
    nbi_electron_heat = None
    nbi_ion_heat = None
    nbi_current = None

    radiation_electron_loss = None
    synchrotron_loss = None
    bootstrap_current = None

    for source in core_sources_ids.source:
        source_name = str(source.identifier.name)
        profile = source.profiles_1d[0]

        if source_name == "nbi":
            nbi_rho = list(profile.grid.rho_tor_norm)
            nbi_electron_heat = list(profile.electrons.energy)
            nbi_ion_heat = list(profile.total_ion_energy)
            nbi_current = list(-1.0 * profile.j_parallel)

        if source_name == "radiation":
            radiation_electron_loss = list(profile.electrons.energy)

        if source_name == "synchrotron_radiation":
            synchrotron_electron_loss = list(profile.electrons.energy)

        if source_name == "bootstrap_current":
            bootstrap_current = list(-1.0 * profile.j_parallel)

           # print("Found bootstrap current")
           # print("Bootstrap first 5:", bootstrap_current[:5])

    if nbi_rho is not None:
        electron_heat = nbi_electron_heat

        if radiation_electron_loss is not None:
            electron_heat = [
                e + r for e, r in zip(electron_heat, radiation_electron_loss)
            ]

        if synchrotron_electron_loss is not None:
            electron_heat = [
                e + s for e, s in zip(electron_heat, synchrotron_electron_loss)
            ]

        sources["generic_heat"] = {
            "mode": "PRESCRIBED",
            "prescribed_values": (
                ([T_INITIAL], nbi_rho, [nbi_ion_heat]),
                ([T_INITIAL], nbi_rho, [electron_heat]),
            ),
        }

    current_profile = nbi_current

    if bootstrap_current is not None:
        current_profile = [
            n + b
            for n, b in zip(nbi_current, bootstrap_current)
        ]

       # print("NBI current first 5:", nbi_current[:5])
       #print("Bootstrap current first 5:", bootstrap_current[:5])
       # print("Combined current first 5:", current_profile[:5])

    sources["generic_current"] = {
        "mode": "PRESCRIBED",
        "prescribed_values": (
            ([T_INITIAL], nbi_rho, [current_profile]),
        ),
    }

    return sources


def build_config():
    equilibrium_ids = _load_ids("equilibrium")
    core_profiles_ids = _load_ids("core_profiles")
    core_sources_ids = _load_ids("core_sources")

    return {
        "plasma_composition": _with_initial_time(
            core_profiles.plasma_composition_from_IMAS(core_profiles_ids)
        ),
        "profile_conditions": _profile_conditions_from_imas(
            core_profiles_ids,
            equilibrium_ids,
        ),
        "geometry": {
            "geometry_type": "IMAS",
            "imas_uri": IMAS_URI,
            "explicit_convert": True,
            "n_rho": N_RHO,
            "slice_index": 0,
        },
        "sources": _sources_from_imas(core_sources_ids),
        "pedestal": {},
        "transport": {
            "model_name": "constant",
        },
        "neoclassical": {
            "bootstrap_current": {},
        },
        "numerics": {
            "t_initial": T_INITIAL,
            "t_final": T_FINAL,
            "fixed_dt": FIXED_DT,
            "evolve_current": True,
            "evolve_ion_heat": True,
            "evolve_electron_heat": True,
            "evolve_density": True,
        },
        "solver": {
            "solver_type": "linear",
        },
        "time_step_calculator": {
            "calculator_type": "fixed",
        },
    }


CONFIG = build_config()


if __name__ == "__main__":
    print("Built direct IMAS-driven TORAX config")
    print("Geometry:", CONFIG["geometry"])
    print("Numerics:", CONFIG["numerics"])
    print("Disabled sources:", sorted(DISABLED_SOURCES))
    print("Sources:", sorted(CONFIG["sources"]))
    print("Profile condition keys:", sorted(CONFIG["profile_conditions"]))
