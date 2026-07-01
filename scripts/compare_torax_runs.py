from argparse import ArgumentParser
from pathlib import Path

import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


PROFILE_VARIABLES = {
    "T_e": "Electron temperature (keV)",
    "T_i": "Ion temperature (keV)",
    "n_e": "Electron density (m^-3)",
    "q": "Safety factor q",
}


def latest_output(output_dir):
    files = sorted(Path(output_dir).glob("state_history_*.nc"))
    if not files:
        raise FileNotFoundError(f"No state_history_*.nc files found in {output_dir}")
    return files[-1]


def normalized_rho(values):
    return np.linspace(0.0, 1.0, len(values))


def read_final_profile(output_file, variable):
    profiles = xr.open_dataset(output_file, group="profiles")
    return np.asarray(profiles[variable].values[-1], dtype=float)


def interpolate_to_reference(reference_values, experiment_values):
    reference_rho = normalized_rho(reference_values)
    experiment_rho = normalized_rho(experiment_values)
    return np.interp(reference_rho, experiment_rho, experiment_values)


def profile_metrics(reference_values, experiment_values):
    experiment_on_reference = interpolate_to_reference(
        reference_values,
        experiment_values,
    )
    difference = experiment_on_reference - reference_values

    rms_difference = np.sqrt(np.mean(difference**2))
    max_abs_difference = np.max(np.abs(difference))

    denominator = np.maximum(np.abs(reference_values), 1e-30)
    percent_difference = 100.0 * difference / denominator
    max_abs_percent_difference = np.max(np.abs(percent_difference))

    return {
        "difference": difference,
        "experiment_on_reference": experiment_on_reference,
        "rms_difference": rms_difference,
        "max_abs_difference": max_abs_difference,
        "max_abs_percent_difference": max_abs_percent_difference,
    }


def make_difference_plot(rho, difference, variable, label, plots_dir):
    plt.figure()
    plt.plot(rho, difference)
    plt.axhline(0.0, linestyle="--")
    plt.xlabel("Normalized radius rho")
    plt.ylabel(f"Difference in {label}")
    plt.title(f"Difference Plot: Full Baseline - Original Baseline ({variable})")
    plt.grid(True)
    plt.savefig(plots_dir / f"difference_{variable}.png", dpi=300, bbox_inches="tight")
    plt.close()


def make_overlay_plot(rho, baseline_values, experiment_values, variable, label, plots_dir):
    plt.figure()
    plt.plot(rho, baseline_values, label="Original baseline")
    plt.plot(rho, experiment_values, "--", label="Full baseline sources")
    plt.xlabel("Normalized radius rho")
    plt.ylabel(label)
    plt.title(f"Original vs Full Baseline: {label}")
    plt.legend()
    plt.grid(True)
    plt.savefig(plots_dir / f"baseline_vs_full_{variable}.png", dpi=300, bbox_inches="tight")
    plt.close()


def compare_runs(baseline_dir, experiment_dir):
    baseline_file = latest_output(baseline_dir)
    experiment_file = latest_output(experiment_dir)

    plots_dir = Path("plots/run_comparison")
    plots_dir.mkdir(parents=True, exist_ok=True)

    print("Baseline file:")
    print(baseline_file)
    print("\nExperiment file:")
    print(experiment_file)

    print("\n=== FINAL PROFILE COMPARISON ===")
    print("Profile | RMS difference | Max abs difference | Max percent difference")

    for variable, label in PROFILE_VARIABLES.items():
        baseline_values = read_final_profile(baseline_file, variable)
        experiment_values = read_final_profile(experiment_file, variable)

        metrics = profile_metrics(baseline_values, experiment_values)
        rho = normalized_rho(baseline_values)

        print(
            f"{variable} ({label}) | "
            f"{metrics['rms_difference']:.6g} | "
            f"{metrics['max_abs_difference']:.6g} | "
            f"{metrics['max_abs_percent_difference']:.3f}%"
        )

        make_overlay_plot(
            rho,
            baseline_values,
            metrics["experiment_on_reference"],
            variable,
            label,
            plots_dir,
        )

        make_difference_plot(
            rho,
            metrics["difference"],
            variable,
            label,
            plots_dir,
        )

    print(f"\nPlots saved in {plots_dir}/")


def parse_args():
    parser = ArgumentParser(
        description="Compare final TORAX profiles between two output folders."
    )
    parser.add_argument(
        "--baseline",
        default="torax_outputs/imas_direct_minimal",
        help="Baseline TORAX output directory.",
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Experiment TORAX output directory.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    compare_runs(args.baseline, args.experiment)
