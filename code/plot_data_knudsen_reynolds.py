import numpy as np

# --- Constants ---
gamma = 1.47
Mm = 28.013e-3  # kg/mol (Molar mass of N2)
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
Ma_vals = np.linspace(0.0, 3.5, 100)

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

# We'll store columns:
#   Ma, Re(300,20µm), Re(300,40µm), Re(600,20µm), Re(600,40µm),
#       Kn(300,20µm), Kn(300,40µm), Kn(600,20µm), Kn(600,40µm)
header = "Ma  Re300_20  Re300_40  Re600_20  Re600_40  Kn300_20  Kn300_40  Kn600_20  Kn600_40"

with open("knre_data.dat", "w") as f:
    f.write(header + "\n")
    for Ma in Ma_vals:
        # Compute for each (T0, Lc) in a fixed order
        row_data = [Ma]
        re_data = []
        kn_data = []
        # First gather Re in the order: (300,20), (300,40), (600,20), (600,40)
        for T0 in T0_values:
            for Lc in Lc_values:
                T = local_temperature(Ma, T0)
                p = local_pressure(Ma, p0)
                Kn = knudsen_number(T, p, Lc)
                Re = reynolds_number(Ma, Kn)
                re_data.append(Re)
        # Then gather Kn in the same parameter order
        for T0 in T0_values:
            for Lc in Lc_values:
                T = local_temperature(Ma, T0)
                p = local_pressure(Ma, p0)
                Kn = knudsen_number(T, p, Lc)
                kn_data.append(Kn)

        row_data.extend(re_data + kn_data)
        line = " ".join(f"{val:.6g}" for val in row_data)
        f.write(line + "\n")

print("Wrote knre_data.dat with columns:\n" + header)
