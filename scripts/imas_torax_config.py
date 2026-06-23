"""Minimal TORAX configuration driven directly by local IMAS HDF5 IDSs."""

import copy

import imas
from torax._src.imas_tools.input import core_profiles
from torax._src.imas_tools.input import core_sources
from torax._src.imas_tools.input import loader


IMAS_URI = "imas:hdf5?path=data"
T_INITIAL = 0.0


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

    # The default TORAX ICRH model requires a local TORIC surrogate file even
    # when the IMAS source is prescribed. Keep the minimal baseline runnable.
    sources.pop("icrh", None)

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
            "n_rho": 25,
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
            "t_final": 0.1,
            "fixed_dt": 0.1,
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
    print("Sources:", sorted(CONFIG["sources"]))
    print("Profile condition keys:", sorted(CONFIG["profile_conditions"]))
