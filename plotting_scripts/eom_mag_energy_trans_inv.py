import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from plotting_formats.plot_format_two_rows import * 

def main():
    """
Error on the mean over mean of magnetic energy as 
a function of step number and computation time when 
sampling a single plaquette vs. when sampling all plaquttes.    

Data source: Dynamic data from Ansatz 1.0
    """
    data_folder = "data/mag_trans_inv"
    
    target_g = 0.7857 

    output_pdf = "figures/eom_mag_energy_trans_inv.pdf"
    
    pattern = os.path.join(data_folder, f"dynamic_mag_ansatz_1.0*g_{target_g}*.npz")
    files = glob.glob(pattern)
    
    if not files:
        print(f"No dynamic data found for g={target_g} (Ansatz 1.0)")
        return
        
    f, axvec = plt.subplots(2, 1)
    
    # Sort/Identify files
    files_sorted = []
    for f_path in files:
        if "single" in f_path: 
            files_sorted.append((f_path, "single plaquette"))
        elif "all" in f_path: 
            files_sorted.append((f_path, "all plaquettes"))
    
    files_sorted.sort(key=lambda x: x[1], reverse=True) # puts 'single' before 'all'
    
    for f_path, label in files_sorted:
        try:
            d = np.load(f_path)
            steps = d["steps"]
            times = d["times"]
            dyn_mean = d["dyn_mean"]
            dyn_eom = d["dyn_eom"]
            
            # Skip first element (often 0 error)
            if len(steps) > 1:
                ratio = dyn_eom[1:] / dyn_mean[1:]
                
                axvec[0].plot(steps[1:], ratio, label=label)
                
                axvec[1].plot(times[1:], ratio, label=label)
                
        except Exception as e:
            print(f"Error reading {f_path}: {e}")

    axvec[0].legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
    axvec[0].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$ of mag. energy")
    axvec[0].set_xlabel("Step number")
    axvec[0].set_yscale("log")
    axvec[0].set_xscale("log")
    
    axvec[1].set_ylabel(r"$\frac{\text{EOM}}{\text{mean}}$ of mag. energy")
    axvec[1].set_yscale("log")
    axvec[1].set_xscale("log")
    axvec[1].set_xlabel("Time [sec]")

    plt.tight_layout()
    plt.savefig(output_pdf)
    plt.close()

if __name__ == "__main__":
    main()