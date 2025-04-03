import numpy as np

# Function implementing Sutherland's law to calculate dynamic viscosity (mu)
# Parameters:
# - T: Temperature in Kelvin (scalar or array)
# - mu_ref: Reference dynamic viscosity at reference temperature (default: 1.716e-5 Pa·s for air at 273.15 K)
# - T_ref: Reference temperature (default: 273.15 K)
# - S: Sutherland's constant (default: 110.4 K for air)
def sutherland(T, mu_ref=1.716e-5, T_ref=273.15, S=110.4):
    return mu_ref * (T / T_ref) ** (3/2) * (T_ref + S) / (T + S)

# Generate an array of temperatures from 200 K to 1000 K, with 100 points
T_values = np.linspace(200, 1000, 100)

# Calculate dynamic viscosity for each temperature using Sutherland's formula
mu_values = sutherland(T_values)

# Select data points within the temperature range of interest (200 to 600 K)
mask = (T_values >= 200) & (T_values <= 600)
T_fit = T_values[mask]    # Temperatures for fitting
mu_fit = mu_values[mask]  # Corresponding viscosities

# Perform linear regression to find the best-fit line (mu = slope * T + intercept)
slope, intercept = np.polyfit(T_fit, mu_fit, 1)
print(f"Best-fit slope: {slope}, Intercept: {intercept}")

# Perform linear regression again, forcing the intercept to zero
# This provides a simpler proportional approximation
slope_i0 = np.sum(T_fit * mu_fit) / np.sum(T_fit**2)
print(f"Slope (with intercept = 0): {slope_i0}")
