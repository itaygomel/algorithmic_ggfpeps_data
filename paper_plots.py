import sys
import os
import importlib.util

scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plotting_scripts")
sys.path.append(scripts_dir)

scripts_to_run = [
    "auto_correlation_gf",
    "auto_correlation_us",
    "eom_couplings_gf",
    "eom_couplings_TI_energy",
    "eom_gf",
    "eom_mag_energy_trans_inv",
    "eom_trans_inv_el",
    "eom_us",
    "grad_eom_gf",
]

if __name__ == "__main__":
    for name in scripts_to_run:
        file_path = os.path.join(scripts_dir, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()