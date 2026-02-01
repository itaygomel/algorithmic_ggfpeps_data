import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        # --- FONT SETTINGS (Added) ---
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "mathtext.fontset": "stix",  # Matches Times New Roman for math symbols
        # --- SIZE & LAYOUT ---
        "figure.figsize": (
            6.85,
            4.5,
        ),  # 6.85 inches is perfect for double-column (width=\textwidth)
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        # --- STYLING ---
        "lines.linewidth": 1,
        "axes.linewidth": 0.8,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.minor.size": 2,
        "ytick.minor.size": 2,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "lines.markersize": 4,
        # --- OUTPUT ---
        "savefig.dpi": 300,
        "axes.grid": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)
