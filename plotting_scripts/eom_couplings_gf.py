import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from plotting_formats.plot_format import * 

def main():
    """Relative error on the mean of the energy as a function
        of step number for different gauge fixing trees"""
    data_folder = "data/gf" 
    output_pdf = "figures/eom_couplings_gf.pdf"

    c_order = ["F", "c", "2", "T"] # gauge fixing types
    colors = {
        "F": "tab:blue", "c": "tab:orange", "2": "tab:green", "T": "tab:red",
        "1": "tab:brown", "3": "tab:purple", "4": "tab:pink"
    }
    labels_map = {
        "F": "no gauge fixing", "c": "chessboard", "2": "2 fixed rows", 
        "T": "maximal tree", "1": "1 fixed row", "3": "3 fixed rows", "4": "4 fixed rows"
    }

    results = {c: [] for c in c_order}

    npz_files = glob.glob(os.path.join(data_folder, "*.npz"))
    
    for f in npz_files:
        try:
            d = np.load(f)
            c = str(d["c"])
            if c not in c_order: continue

            g = float(d["g"])
            
            scalar_eom = float(d["energy_scalar_eom"])
            scalar_mean = float(d["energy_scalar_mean"])
            
            if scalar_mean != 0:
                metric_val = scalar_eom / scalar_mean
                results[c].append((g, metric_val))
                
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if plt.get_fignums(): plt.clf()

    for c in c_order:
        data_points = results[c]
        if not data_points: continue
            
        data_points.sort(key=lambda x: x[0])
        g_arr = [p[0] for p in data_points]
        val_arr = [p[1] for p in data_points]
        
        plt.plot(
            g_arr, 
            val_arr, 
            "o-", 
            label=labels_map[c], 
            color=colors[c]
        )

    plt.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"$\frac{\text{EOM}}{\text{mean}}$ of energy")
    plt.tight_layout()
    plt.subplots_adjust(top=0.82)
    
    plt.savefig(output_pdf)

if __name__ == "__main__":
    main()