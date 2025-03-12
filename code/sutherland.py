import numpy as np

def sutherland(T, mu_ref=1.716e-5, T_ref=273.15, S=110.4):
    return mu_ref * (T / T_ref) ** (3/2) * (T_ref + S) / (T + S)

# Generate temperatures and compute dynamic viscosities
T_values = np.linspace(200, 1000, 100)
mu_values = sutherland(T_values)

# Filter data for the range between 200 and 600 K
mask = (T_values >= 200) & (T_values <= 600)
T_fit = T_values[mask]
mu_fit = mu_values[mask]

# Compute the best-fit linear regression over the selected range
slope, intercept = np.polyfit(T_fit, mu_fit, 1)
print(f"Slope: {slope}, Intercept: {intercept}")

slope_i0 = np.sum(T_fit * mu_fit) / np.sum(T_fit**2)
print(f"Slope: {slope_i0} with intercept = 0")
