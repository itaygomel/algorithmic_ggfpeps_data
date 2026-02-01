import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import re

from plotting_formats.plot_format import * 
def main():
    """Autocorrelation of the energy as a function of step
        number for different number of updated links per step."""

    data_folder = r"data/auto_correlation_us"
    output_pdf = r"figures/auto_correlation_us.pdf"

    n_labels = {
        1:  r"1 link ($\frac{1}{72}N_{\text{links}}$)",
        9:  r"9 links ($\frac{1}{8}N_{\text{links}}$)",
        18: r"18 links ($\frac{1}{4}N_{\text{links}}$)",
        36: r"36 links ($\frac{1}{2}N_{\text{links}}$)",
        54: r"54 links ($\frac{3}{4}N_{\text{links}}$)",
        63: r"63 links ($\frac{7}{8}N_{\text{links}}$)",
    }

    npz_files = glob.glob(os.path.join(data_folder, "L_6_update_size_*.npz"))
    
    if not npz_files:
        print(f"No data found in {data_folder}")
        return

    data_list = []
    for f in npz_files:
        try:
            d = np.load(f)
            data_list.append(d)
        except Exception as e:
            print(f"Error loading {f}: {e}")
            
    data_list.sort(key=lambda x: int(x["n"]))

    has_data = False
    
    for data in data_list:
        n = int(data["n"])
        autocorr = data["autocorr"]
        obs_name = str(data["obs_name"])
        
        label = n_labels.get(n, f"update_size {n}")
        
        limit = 50
        if len(autocorr) > limit:
            y_vals = np.abs(autocorr)[0:limit]
            
            plt.plot(y_vals, label=label)
            has_data = True

    if not has_data:
        print("No valid data points to plot.")
        return

    plt.ylabel(f"Autocorrelation of {obs_name}")
    plt.xlabel("Step number")
    plt.ylim(bottom=1e-4)
    plt.yscale("log")
    
    plt.legend(loc="upper right")
    
    plt.savefig(output_pdf, dpi=300, bbox_inches="tight")
    

if __name__ == "__main__":
    main()