import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from plotting_formats.plot_format_two_rows import * 

def plot_single_observable(data_folder, obs_key, ylabel_text, output_filename):
    """Error on the mean over mean for a specific observable
        as a function of step number and time for various numbers
    of links over which the electric energy is averaged."""

    n_labels = {
        1: r"1 link ($\frac{1}{32}N_{\text{links}}$)",
        4: r"4 links ($\frac{1}{8}N_{\text{links}}$)",
        8: r"8 links ($\frac{1}{4}N_{\text{links}}$)",
        16: r"16 links ($\frac{1}{2}N_{\text{links}}$)",
        26: r"16 links ($\frac{1}{2}N_{\text{links}}$)", 
    }

    npz_files = glob.glob(os.path.join(data_folder, "L_4_el_links_*.npz"))
    if not npz_files:
        print(f"No data found in {data_folder}")
        return

    data_list = []
    for f in npz_files:
        try:
            d = np.load(f)
            data_list.append(d)
        except:
            pass
    
    data_list.sort(key=lambda x: int(x["n"]))

    f, axvec = plt.subplots(2, 1)
    has_data = False
    
    for data in data_list:
        n = int(data["n"])
        
        mean_key = f"{obs_key}_mean"
        eom_key = f"{obs_key}_eom"
        
        if mean_key not in data or eom_key not in data:
            continue
            
        step_numbers = data["step_numbers"]
        times = data["times"]
        dyn_mean = data[mean_key]
        dyn_eom = data[eom_key]
        

        if len(step_numbers) > 1:
            ratio = np.array(dyn_eom[1:]) / np.array(dyn_mean[1:])
            steps_sliced = step_numbers[1:]
            times_sliced = times[1:]
            
            label = n_labels.get(n, f"{n} links")
            
            axvec[0].plot(steps_sliced, ratio, label=label)
            axvec[1].plot(times_sliced, ratio)
            has_data = True

    if not has_data:
        print(f"No valid data found for {obs_key}")
        plt.close(f)
        return

    axvec[0].legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        frameon=False,
    )
    
    axvec[0].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$" + f" of {ylabel_text}")
    axvec[0].set_xlabel(f"Step number")
    axvec[0].set_yscale("log")
    axvec[0].set_xscale("log")
    
    axvec[1].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$" + f" of {ylabel_text}")
    axvec[1].set_yscale("log")
    axvec[1].set_xscale("log")
    axvec[1].set_xlabel(f"Time [sec]")

    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close(f)

def main():
    data_folder = r"data/eom_trans_inv_el" 
    
    plot_single_observable(
        data_folder,
        obs_key="energy",
        ylabel_text="energy",
        output_filename="figures/eom_el_energy_trans_inv_total_energy.pdf"
    ) # For the energy observable

    plot_single_observable(
        data_folder,
        obs_key="el_energy",
        ylabel_text="electric energy",
        output_filename="figures/eom_el_energy_trans_inv.pdf"
    ) # For the electric energy observable

if __name__ == "__main__":
    main()