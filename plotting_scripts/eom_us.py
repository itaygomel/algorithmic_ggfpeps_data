import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# Strict import of your custom formatting
from plotting_formats.plot_format_2_columns import *

def main():
    """Relative error on the mean of the energy as a function 
    of step number and time for different number of updated links
    per step and various lattice size"""
    data_folder = r"data/eom_us"
    output_filename = r"figures/eom_us.pdf"
    obs = "energy"


    n_labels_2 = {
        1: (r"single link", "tab:blue"),
        2: (r"$\frac{1}{4}N_{\text{links}}$", "tab:green"),
        4: (r"$\frac{1}{2}N_{\text{links}}$", "tab:red"),
        6: (r"$\frac{3}{4}N_{\text{links}}$", "tab:purple"),
        7: (r"$\frac{7}{8}N_{\text{links}}$", "tab:brown"),
        8: (r"$N_{\text{links}}$", "tab:gray"),
    }
    n_labels_4 = {
        1: (r"single link", "tab:blue"),
        4: (r"$\frac{1}{8}N_{\text{links}}$", "tab:orange"),
        8: (r"$\frac{1}{4}N_{\text{links}}$", "tab:green"),
        16: (r"$\frac{1}{2}N_{\text{links}}$", "tab:red"),
        24: (r"$\frac{3}{4}N_{\text{links}}$", "tab:purple"),
        28: (r"$\frac{7}{8}N_{\text{links}}$", "tab:brown"),
        32: (r"$N_{\text{links}}$", "tab:gray"),
    }
    n_labels_6 = {
        1: (r"single link", "tab:blue"),
        9: (r"$\frac{1}{8}N_{\text{links}}$", "tab:orange"),
        18: (r"$\frac{1}{4}N_{\text{links}}$", "tab:green"),
        36: (r"$\frac{1}{2}N_{\text{links}}$", "tab:red"),
        54: (r"$\frac{3}{4}N_{\text{links}}$", "tab:purple"),
        63: (r"$\frac{7}{8}N_{\text{links}}$", "tab:brown"),
    }

    # (L_size, labels_dict, unwanted_ns)
    columns_config = [
        (2, n_labels_2, [7, 8]),   # Col 0: L=2
        (4, n_labels_4, [28, 32]), # Col 1: L=4
        (6, n_labels_6, [63]),     # Col 2: L=6
    ]

    # Explicit figsize
    fig, axes = plt.subplots(2, 3, figsize=(6.85, 4.5), sharey="row")

    for col, (L, n_labels, unwanted_ns) in enumerate(columns_config):
        
        pattern = os.path.join(data_folder, f"L_{L}_update_size_*.npz")
        npz_files = glob.glob(pattern)
        
        if not npz_files:
            print(f"No data found for L={L}")
            continue

        # sort by n
        data_list = []
        for f in npz_files:
            try:
                d = np.load(f)
                data_list.append(d)
            except:
                pass
        
        data_list.sort(key=lambda x: int(x["n"]))
        
        for data in data_list:
            n = int(data["n"])
            
            if n in unwanted_ns:
                continue
            
            if n not in n_labels:
                continue

            label_text = n_labels[n][0]
            color = n_labels[n][1]
            
            step_numbers = data["step_numbers"]
            times = data["times"]
            dyn_mean = data["dyn_mean"]
            dyn_eom = data["dyn_eom"]

            if len(step_numbers) > 1:
                ratio = np.array(dyn_eom[1:]) / np.array(dyn_mean[1:])
                # steps
                axes[0, col].plot(
                    step_numbers[1:], 
                    ratio, 
                    label=label_text, 
                    color=color
                )
                
                # time
                axes[1, col].plot(
                    times[1:], 
                    ratio, 
                    label=label_text, 
                    color=color
                )

        N_links = 2 * (L**2)
        axes[0, col].set_title(r"$L=$" + f"{L} " + r"($N_{\text{links}}=$" + f"{N_links})")

        axes[0, col].set_xlabel("Step number")
        axes[0, col].set_yscale("log")
        axes[0, col].set_xscale("log")
        
        axes[1, col].set_xlabel("Time [sec]")
        axes[1, col].set_yscale("log")
        axes[1, col].set_xscale("log")

        if col == 0:
            axes[0, col].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$" + f" of {obs}")
            axes[1, col].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$" + f" of {obs}")

        axes[0, col].tick_params(axis="both")
        axes[1, col].tick_params(axis="both")

    
    handles, labels = axes[1, 1].get_legend_handles_labels()
    
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=len(labels),
        bbox_to_anchor=(0.5, 0.99),
        frameon=False,
    )
    
    plt.savefig(output_filename, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()