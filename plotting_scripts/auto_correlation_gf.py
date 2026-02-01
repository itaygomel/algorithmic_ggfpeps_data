import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from plotting_formats.plot_format import * 

def main():
    """
    Autocorrelation of the energy as a function of step number for different gauge fixing trees
    """
    data_folder = "data/gf"
    target_g = 0.7857
    output_pdf = f"figures/auto_correlation_gf.pdf"
    
    c_order = ["F", "c", "2", "T"]
    colors = {"F": "tab:blue", "c": "tab:orange", "2": "tab:green", "T": "tab:red"}
    labels_map = {"F": "no gauge fixing", "c": "chessboard", "2": "2 fixed rows", "T": "maximal tree"}

    pattern = os.path.join(data_folder, f"L_6_g_{target_g}*.npz")
    npz_files = glob.glob(pattern)

    data_list = []
    for f in npz_files:
        try:
            d = np.load(f)
            if str(d["c"]) in c_order:
                data_list.append(d)
        except: 
            pass

    data_list.sort(key=lambda x: c_order.index(str(x["c"])))

    if plt.get_fignums(): 
        plt.clf()
    
    for data in data_list:
        c = str(data["c"])
        autocorr = data["energy_autocorr"]
        
        limit = 145
        if len(autocorr) > limit:
            plt.plot(
                np.abs(autocorr[:limit]), 
                label=labels_map[c], 
                color=colors[c]
            )

    plt.yscale("log")
    plt.ylabel(r"Autocorrelation of energy")
    plt.xlabel("Step number")
    plt.ylim(bottom=1e-3)
    plt.legend()
    plt.savefig(output_pdf)

if __name__ == "__main__":
    main()