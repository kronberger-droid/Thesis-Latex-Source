import numpy as np
from scipy.optimize import fsolve

def mach_area_relation(M, A_Astar, gamma):
    """Equation to solve for Mach number M."""
    return (1 / M) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2))**((gamma + 1) / (2 * (gamma - 1))) - A_Astar

def solve_mach(A_Astar, gamma, M_guess=1.0):
    """Solves for Mach number M given A/A* and gamma."""
    M_solution = fsolve(mach_area_relation, M_guess, args=(A_Astar, gamma))
    return M_solution[0]

A_Astar = 318
gamma = 1.47
M_solution = solve_mach(A_Astar, gamma, 0.1)
print(f"Solved Mach number: {M_solution:.5f}")
