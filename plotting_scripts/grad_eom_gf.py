import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import glob
import utils
from plotting_formats.plot_format import *


def process_single_file(filepath):
    """
    Loads a .npz file containing raw timeseries and computes the gradient error.
    """
    if not os.path.isfile(filepath):
        return [], []

    try:
        data = np.load(filepath)
        
        energy_ts = data["energy_ts"]
        grad_norm_ts = data["grad_norm_ts"]
        
        # Reconstruct the total energy gradient from components
        el_grad = -2 * float(data["g_el"]) * data["el_grad_ts"]
        mass_grad = float(data["g_mass"]) * data["mass_grad_ts"]
        int_grad = float(data["g_int"]) * data["int_grad_ts"]
        
        energy_grad_obsvec = el_grad + mass_grad + int_grad
        
        nlayer = int(data["nlayer"])
        nparams = int(data["nparams"])
        
        eom_arr = []
        mean_arr = []

        # Perform the calculation per layer and parameter
        for layer in range(nlayer):
            for grad_ind in range(nparams):
                
                current_grad = energy_grad_obsvec[:, layer, grad_ind]
                current_norm = grad_norm_ts[:, layer, grad_ind]

                mean = utils.compute_grad_mean(energy_ts, current_grad, current_norm)
                
                if np.isclose(mean, 0):
                    continue

                eom = utils.compute_grad_err(energy_ts, current_grad, current_norm)
                
                eom_arr.append(eom)
                mean_arr.append(mean)
                
        return eom_arr, mean_arr

    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return [], []

def get_max_grad_error_from_files(file_list):
    """
    Iterates over a list of files and aggregates the max gradient error.
    """
    all_eom = []
    all_mean = []

    for fname in file_list:
        eom, mean = process_single_file(fname)
        all_eom.extend(eom)
        all_mean.extend(mean)

    if not all_eom:
        return np.nan, np.nan

    # Compute final statistics
    ratio_arr = np.abs(np.asarray(all_eom) / np.asarray(all_mean))
    
    max_error = np.max(ratio_arr)
    std_error = np.std(ratio_arr) / np.sqrt(len(all_eom))

    return max_error, std_error


def main():
    """Maximal relative error on the mean among energy
    gradient components for different gauge fixing trees"""
    base_folder = "data/grad_gf" 
    results = {}
    
    labels = {"c": "Chessboard", "T": "Maximal Tree", "F": "No Gauge Fixing"}
    colors = {"c": "tab:orange", "T": "tab:red", "F": "tab:blue"}
    pattern = r"L_4_g_([0-9.]+)_gf_([A-Za-z0-9]+)"

    if not os.path.exists(base_folder):
        print(f"Error: Data folder '{base_folder}' not found.")
        return

    for subfolder in os.listdir(base_folder):
        match = re.match(pattern, subfolder)
        if match:
            g_value = float(match.group(1))
            c_value = match.group(2)
            if c_value not in ["c", "T", "F"]: 
                continue

            subfolder_path = os.path.join(base_folder, subfolder)
            npz_files = glob.glob(os.path.join(subfolder_path, "*.npz"))
            
            if npz_files:
                max_grad, std = get_max_grad_error_from_files(npz_files)
                if c_value not in results: results[c_value] = []
                results[c_value].append((g_value, max_grad, std))

    
    fig, ax = plt.subplots()

    plot_order = ["F", "c", "T"]
    
    for c_value in plot_order:
        if c_value in results:
            data = results[c_value]
            data.sort()
            
            g_vals = [x[0] for x in data]
            grad_vals = [x[1] for x in data]
            limit = min(len(g_vals), 12)
            
            ax.plot(
                g_vals[:limit],
                grad_vals[:limit],
                marker="o",
                label=labels[c_value],
                color=colors[c_value]
            )

    ax.set_xlabel(r"$\lambda$")
    ax.set_ylabel(r"Max $\frac{\text{EOM}}{\text{mean}}$ of gradient components")
    ax.set_xlim(0.17, 2.05)
    ax.set_ylim(0.02, 0.4)
    ax.legend(frameon=False) 
    
    output_file = "figures/eom_gf_grad.pdf"
    plt.tight_layout()
    plt.savefig(output_file)

if __name__ == "__main__":
    main()