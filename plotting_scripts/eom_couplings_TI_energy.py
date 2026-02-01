import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from plotting_formats.plot_format import * 

def main():
    """
    Error on the mean over mean of the energy. 
    comparing cases where the magnetic energy 
    is averaged over all plaquettes versus a single plaquette

    Data source: Scalar data from Ansatz 0.5
    """
    data_folder = "data/mag_trans_inv"
    output_pdf = "figures/eom_couplings_TI_energy.pdf"
    
    colors = {"all": "tab:orange", "single": "tab:blue"}
    labels = {"all": "all plaquettes", "single": "single plaquette"}
    
    pattern = os.path.join(data_folder, "scalar_mag_ansatz_0.5*.npz")
    files = glob.glob(pattern)
    
    if not files:
        print("No scalar data found for Plot 1 (Ansatz 0.5)")
        return

    data_by_mode = {"all": [], "single": []}
    
    for f in files:
        try:
            d = np.load(f)
            mode = str(d["mode"])
            if mode in data_by_mode:
                g = float(d["g"])
                eom = float(d["eom"])
                mean = float(d["mean"])
                
                if mean != 0:
                    data_by_mode[mode].append((g, eom/mean))
        except Exception as e:
            print(f"Skipping {f}: {e}")

    if plt.get_fignums(): plt.clf()
    
    for mode in ["single", "all"]: # specific order
        points = data_by_mode[mode]
        points.sort(key=lambda x: x[0]) # Sort by g
        
        if points:
            g_arr = [p[0] for p in points]
            y_arr = [p[1] for p in points]
            
            plt.plot(
                g_arr, 
                y_arr, 
                "o-", 
                label=labels[mode], 
                color=colors[mode]
            )

    plt.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"$\frac{\text{EOM}}{\text{mean}}$ of energy") 
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.82)
    
    plt.savefig(output_pdf)

if __name__ == "__main__":
    main()