import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from plotting_formats.plot_format import * 

def main():
    """Relative error on the mean of the energy as a function
        of step number for different gauge fixing trees"""
    data_folder = "data/gf"
    target_g = 0.7857
    output_pdf = "figures/eom_gf.pdf"

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
        except: pass

    data_list.sort(key=lambda x: c_order.index(str(x["c"])))

    if plt.get_fignums(): plt.clf()

    for data in data_list:
        c = str(data["c"])
        steps = data["steps"]
        dyn_mean = data["energy_dyn_mean"]
        dyn_eom = data["energy_dyn_eom"]

        # Using [1:] logic exactly as original
        if len(steps) > 1:
            ratio = dyn_eom[1:] / dyn_mean[1:]
            plt.plot(
                steps[1:], 
                ratio, 
                label=labels_map[c], 
                color=colors[c]
            )

    plt.ylabel(r"$\frac{\text{EOM}}{\text{mean}}$ of energy")
    plt.xlabel("Step number")
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_pdf)

if __name__ == "__main__":
    main()