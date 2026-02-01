# Algorithmic Data for GGFPEPS

This repository stores the data for the paper *Algorithmic Aspects of Gauged Gaussian Fermionic PEPS: Gauge Fixing and Translation Invariance*.

arxiv: [https://arxiv.org/abs/2512.13812](https://arxiv.org/abs/2512.13812)

The script `paper_plots.py` generates all of the plots used in the paper. It executes the analysis scripts located in the `plotting_scripts` directory sequentially.

To run the full analysis (after installation of the required packages), use the command:

`python plotting_scripts.py`

This will save (and overwrite) the plots in the directory `figures` (or the specific output directories defined in the scripts).

## Repository Structure

* `paper_plots.py`: The main runner script. It imports and executes the `main()` function from the analysis scripts.
* `plotting_scripts/`: Contains the individual analysis scripts (e.g., `eom_gf.py`, `auto_correlation_gf.py`, etc.).
* `plotting_scripts/plotting_formats/`: Contains the formatting styles used by the plots.
* `data/`: Directory containing the simulation data (e.g., `.npz` files).

## Installation

To generate the plots, any recent version of python with the required packages should suffice (we used python 3.12).

Download this repo: either clone from github or download from Zenodo using the web interface. If needed, unzip the data (so that it is stored in the directory `data/` relative to this readme).

Create a virtual environment (`python -m venv env_name`) and then activate it (`source env_name/bin/activate`), and install the required packages (`pip install -r requirements.txt`).

You can now run the scripts as specified above.
When you are done handling the data, deactivate the environment, `deactivate`.