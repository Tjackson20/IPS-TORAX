from scripts.imas_torax_config import _load_ids, CONFIG
import numpy as np


def safe_len(x):
    try:
        return len(x)
    except Exception:
        return 0


def safe_max_abs(x):
    if safe_len(x) == 0:
        return None
    arr = np.asarray(x)
    if arr.size == 0:
        return None
    return float(np.max(np.abs(arr)))


ids = _load_ids("core_sources")
torax_sources = set(CONFIG["sources"].keys())

print("TORAX sources in config:")
for name in sorted(torax_sources):
    print("-", name)

print("\nIMAS source summary:")
print(
    "source | rho_pts | j_parallel_max | electron_energy_max | ion_energy_max | electron_particles_max"
)

for source in ids.source:
    name = str(source.identifier.name)
    p = source.profiles_1d[0]

    rho_len = safe_len(p.grid.rho_tor_norm)
    jmax = safe_max_abs(p.j_parallel)
    emax = safe_max_abs(p.electrons.energy)
    imax = safe_max_abs(p.total_ion_energy)
    nmax = safe_max_abs(p.electrons.particles)

    print(f"{name} | {rho_len} | {jmax} | {emax} | {imax} | {nmax}")