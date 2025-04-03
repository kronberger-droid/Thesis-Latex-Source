import numpy as np
from scipy.optimize import fsolve

# Function defining the relationship between Mach number (M), area ratio (A/A*), and specific heat ratio (gamma)
# Used to find the Mach number given an area ratio (A/A*)
def mach_area_relation(M, A_Astar, gamma):
    return (1 / M) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**((gamma + 1) / (2 * (gamma - 1))) - A_Astar

# Function to numerically solve for Mach number given an area ratio (A/A*), specific heat ratio (gamma), and an initial guess for Mach number
# Parameters:
# - A_Astar: Area ratio (A/A*)
# - gamma: Specific heat ratio
# - M_guess: Initial guess for Mach number (default: 1.0)
def solve_mach(A_Astar, gamma, M_guess=1.0):
    M_solution = fsolve(mach_area_relation, M_guess, args=(A_Astar, gamma))
    return M_solution[0]

# Example calculation:
A_Astar = 318     # Given area ratio (A/A*)
gamma = 1.47      # Specific heat ratio for the gas

# Solve Mach number with initial guess of 0.1 (indicating expected subsonic solution)
M_solution = solve_mach(A_Astar, gamma, 0.1)
print(f"Solved Mach number: {M_solution:.5f}")
