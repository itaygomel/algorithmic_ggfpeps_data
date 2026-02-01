import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "mathtext.fontset": "stix",  
        "figure.figsize": (3.38, 3.4), 
        "font.size": 8,
        "axes.labelsize": 9, 
        "axes.titlesize": 8,
        "xtick.labelsize": 8,  
        "ytick.labelsize": 8,  
        "legend.fontsize": 8, 
        "lines.linewidth": 1,
        "axes.linewidth": 0.8,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.minor.size": 2,
        "ytick.minor.size": 2,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "lines.markersize": 4,
        "savefig.dpi": 300,
        "axes.grid": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.constrained_layout.use": True,  # This prevents labels from being cut off
    }
)
