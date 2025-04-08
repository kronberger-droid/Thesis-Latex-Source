import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D

# --------------------------------------------------------------------
# Global style tweaks for a bigger, less-cramped figure
# --------------------------------------------------------------------
mpl.rcParams['figure.figsize'] = (8, 5)    
mpl.rcParams['font.size'] = 9              
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['lines.linewidth'] = 1.0      
mpl.rcParams['savefig.dpi'] = 600          
# --------------------------------------------------------------------

# --- Constants ---
gamma = 1.47
Mm = 28.013e-3  
R_u = 8.314462618 
p0 = 1.5e5       

# Characteristic lengths
Lc_values = [20e-6, 40e-6]

# Stagnation temperatures
T0_values = [300.0, 600.0]

# Viscosity model constants (Sutherland's law)
S_mu = 111.0
T_ref_mu = 300.55
mu_ref = 17.81e-6

# Mach number range
Ma = np.linspace(0.0, 3.5, 300)

# --- Functions ---
def local_temperature(Ma, T0):
    return T0 / (1 + (gamma - 1) / 2 * Ma**2)

def local_pressure(Ma, p0):
    return p0 * (1 + (gamma - 1) / 2 * Ma**2) ** (-gamma / (gamma - 1))

def dynamic_viscosity(T):
    return mu_ref * (T / T_ref_mu)**1.5 * (T_ref_mu + S_mu) / (T + S_mu)

def knudsen_number(T, p, Lc):
    return (dynamic_viscosity(T) / (p * Lc)) * np.sqrt(np.pi * T * R_u / (2 * Mm))

def reynolds_number(Ma, Kn):
    return Ma * np.sqrt(gamma * np.pi / 2) / Kn

# --- Colors & line styles ---
green_color = "#2D8A56"  # Reynolds
blue_color  = "#074799"  # Knudsen
red_color   = "#B31B1B"  # ref line at Kn=0.1

# Make 20 µm dotted, 40 µm solid
lc_linestyle = {
    20e-6: "-",
    40e-6: "--",
}

# --- Compute data ---
results_kn = {}
results_re = {}
for T0 in T0_values:
    T = local_temperature(Ma, T0)
    p = local_pressure(Ma, p0)
    for Lc in Lc_values:
        kn_val = knudsen_number(T, p, Lc)
        re_val = reynolds_number(Ma, kn_val)
        results_kn[(T0, Lc)] = kn_val
        results_re[(T0, Lc)] = re_val

# --- Plotting ---
fig, ax_re = plt.subplots()        # Left axis for Reynolds
ax_kn = ax_re.twinx()              # Right axis for Knudsen

for T0 in T0_values:
    for Lc in Lc_values:
        style = lc_linestyle[Lc]
        Re_vals = results_re[(T0, Lc)]
        Kn_vals = results_kn[(T0, Lc)]

        # Plot Reynolds (left, green)
        ax_re.plot(
            Ma, Re_vals, 
            style, color=green_color, linewidth=1.1
        )
        # Plot Knudsen (right, blue)
        ax_kn.plot(
            Ma, Kn_vals, 
            style, color=blue_color, linewidth=1.1
        )

# Reference line for Kn=0.1 on right axis
ax_kn.axhline(y=0.1, color=red_color, linestyle=":", linewidth=1)

# Remove axis labels entirely (per your request)
ax_re.set_xlabel("")
ax_re.set_ylabel("")
ax_kn.set_ylabel("")

# Axis scales
ax_re.set_xlim(0.0, 3.5)
ax_re.set_yscale("log")
ax_kn.set_yscale("log")

plt.tight_layout()

# Save as PDF
plt.savefig("my_plot.pdf", format="svg", transparent=True)
plt.show()
