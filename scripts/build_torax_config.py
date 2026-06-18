from map_imas_to_torax import build_torax_input


def build_config():
    data = build_torax_input()

    config = {
        "plasma_composition": {
            "main_ion": {"D": 0.5, "T": 0.5},
            "impurity": "Ne",
            "Z_eff": float(data["zeff"][0]),
        },

        "profile_conditions": {
            "Ip": float(abs(data["plasma_current"])),
            "T_e": {
                0.0: {
                    0.0: float(data["electron_temperature"][0] * 1e-3),
                    1.0: float(data["electron_temperature"][-1] * 1e-3),
                }
            },
            "T_i": {
                0.0: {
                    0.0: float(data["ion_temperature"][0] * 1e-3),
                    1.0: float(data["ion_temperature"][-1] * 1e-3),
                }
            },
            "n_e": {
    0.0: {
        0.0: float(data["electron_density"][0]),
        1.0: float(data["electron_density"][-1]),
    }
},
        },

               "geometry": {
            "geometry_type": "circular",
            "R_major": float(data["r0"]),
            "B_0": float(abs(data["b0"])),
        },

        "numerics": {
            "t_final": 5,
            "fixed_dt": 0.25,
            "evolve_ion_heat": True,
            "evolve_electron_heat": True,
            "evolve_current": True,
            "evolve_density": True,
        },

        "neoclassical": {
            "bootstrap_current": {},
        },

        "sources": {
            "ohmic": {},
            "fusion": {},
            "generic_heat": {},
        },

        "pedestal": {},

        "transport": {
            "model_name": "constant",
        },

        "solver": {
            "solver_type": "linear",
        },

        "time_step_calculator": {
            "calculator_type": "chi",
        },
    }

    return config


if __name__ == "__main__":
    config = build_config()

    print("TORAX config draft created successfully")

    print("\nPlasma composition:")
    print(config["plasma_composition"])

    print("\nProfile conditions:")
    print(config["profile_conditions"])

    print("\nGeometry:")
    print(config["geometry"])

    print("\nSources:")
    print(config["sources"])
    
    print("\nNumerics:")
    print(config["numerics"])

    print("\nNeoclassical:")
    print(config["neoclassical"])

    print("\nPedestal:")
    print(config["pedestal"])

    print("\nTransport:")
    print(config["transport"])

    print("\nSolver:")
    print(config["solver"])