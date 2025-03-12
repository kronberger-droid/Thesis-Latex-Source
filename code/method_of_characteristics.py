import numpy as np
import matplotlib.pyplot as plt
import scipy
from typing import Tuple, List, Optional, Dict

class MOCPoint:
    def __init__(self, x: float, y: float, mach: float, angle: float, 
                 pressure: Optional[float] = None, 
                 temperature: Optional[float] = None):
        self.x = x
        self.y = y
        self.mach = mach
        self.angle = angle
        self.pressure = pressure
        self.temperature = temperature

    def __str__(self):
        return f"MOCPoint(x={self.x:.3f}, y={self.y:.3f}, mach={self.mach:.3f}, angle={np.degrees(self.angle):.2f}°)"

class MOCGrid:
    def __init__(self):
        self.points: Dict[Tuple[int, int], MOCPoint] = {}

    def add_point(self, i: int, j: int, point: MOCPoint):
        self.points[(i, j)] = point

    def get_point(self, i: int, j: int) -> Optional[MOCPoint]:
        return self.points.get((i, j))

class MOCCharacteristicSolver:
    def __init__(self, gamma: float = 1.4):
        self.gamma = gamma
        self.grid = MOCGrid()

    def generate_initial_line(self, x_start: float, y_start: float, y_end: float, 
                              mach: float, angle: float, num_points: int) -> List[MOCPoint]:
        """Generate initial line of points."""
        y_values = np.linspace(y_start, y_end, num_points)
        return [MOCPoint(x_start, y, mach, angle) for y in y_values]

    def prandtl_meyer_function(self, mach: float) -> float:
        return np.sqrt((self.gamma + 1) / (self.gamma - 1)) * \
               np.arctan(np.sqrt((self.gamma - 1) / (self.gamma + 1) * (mach**2 - 1))) - \
               np.arctan(np.sqrt(mach**2 - 1))

    def inverse_prandtl_meyer(self, nu: float, mach_guess: float = 2.0) -> float:
        def pm_diff(mach):
            return self.prandtl_meyer_function(mach) - nu

        def pm_diff_derivative(mach):
            return np.sqrt((self.gamma + 1) / (self.gamma - 1)) * \
                np.sqrt((self.gamma - 1) / (self.gamma + 1)) * \
                (2 * mach / (mach**2 - 1)) - \
                (2 * mach / (mach**2 - 1))

        # Initialize bounds
        a, b = 1.0001, 50.0
        
        # Check if the root is within the initial bounds
        if pm_diff(a) * pm_diff(b) >= 0:
            raise ValueError(f"Root is not bracketed for nu = {nu}")

        # Combine bisection and Newton's method
        max_iterations = 100
        tolerance = 1e-6
        
        for _ in range(max_iterations):
            c = (a + b) / 2  # Bisection point
            fc = pm_diff(c)
            
            if abs(fc) < tolerance:
                return c
            
            # Newton step
            newton_step = fc / pm_diff_derivative(c)
            new_c = c - newton_step
            
            # Check if Newton's method is converging and staying within bounds
            if a < new_c < b and abs(newton_step) < (b - a) / 2:
                c = new_c
            else:
                # If Newton's method fails, use bisection
                if pm_diff(a) * fc < 0:
                    b = c
                else:
                    a = c
        
        raise ValueError(f"Failed to converge for nu = {nu} after {max_iterations} iterations")

    def mach_angle(self, mach: float) -> float:
        if mach <= 1:
            raise ValueError(f"Mach number must be greater than 1 for supersonic flow. Got {mach}")
        return np.arcsin(1 / mach)

    def characteristic_equations(self, point: MOCPoint) -> Tuple[float, float]:
        if point.mach is None:
            raise ValueError(f"Mach number is None for point: {point}")
        mu = self.mach_angle(point.mach)
        return np.tan(point.angle - mu), np.tan(point.angle + mu)

    def wall_point_process(self, wall_point: MOCPoint, interior_point: MOCPoint, wall_angle: float) -> MOCPoint:
        """Calculate the next wall point using the wall point process."""
        C_minus = self.prandtl_meyer_function(interior_point.mach) + interior_point.angle
        new_angle = wall_angle
        new_nu = C_minus - new_angle
        try:
            new_mach = self.inverse_prandtl_meyer(new_nu)
        except ValueError as e:
            print(f"Error in wall_point_process: C_minus = {C_minus}, new_angle = {new_angle}, new_nu = {new_nu}")
            raise e
        
        m_minus, _ = self.characteristic_equations(interior_point)
        dx = (interior_point.y - wall_point.y) / (m_minus - np.tan(wall_angle))
        x = wall_point.x + dx
        y = wall_point.y + dx * np.tan(wall_angle)
        
        return MOCPoint(x, y, new_mach, new_angle)

    def interior_point_process(self, point1: MOCPoint, point2: MOCPoint) -> MOCPoint:
        """Calculate an interior point using the interior point process."""
        C_plus = self.prandtl_meyer_function(point1.mach) - point1.angle
        C_minus = self.prandtl_meyer_function(point2.mach) + point2.angle
        
        new_angle = (C_plus - C_minus) / 2
        new_nu = (C_plus + C_minus) / 2
        new_mach = self.inverse_prandtl_meyer(new_nu)
        
        m1, _ = self.characteristic_equations(point1)
        _, m2 = self.characteristic_equations(point2)
        
        x = (point2.y - point1.y - m2*point2.x + m1*point1.x) / (m1 - m2)
        y = point1.y + m1 * (x - point1.x)
        
        return MOCPoint(x, y, new_mach, new_angle)

    def solve_next_line(self, current_line: List[MOCPoint], wall_angle: float = 0) -> List[MOCPoint]:
        """Solve for the next line of points using appropriate unit processes."""
        next_line = []
        
        # Wall point
        next_line.append(self.wall_point_process(current_line[0], current_line[1], wall_angle))
        
        # Interior points
        for i in range(len(current_line) - 1):
            next_point = self.interior_point_process(current_line[i], current_line[i+1])
            next_line.append(next_point)
        
        return next_line

    def solve_flow_field(self, initial_line: List[MOCPoint], num_lines: int, wall_angle: float = 0) -> MOCGrid:
        """Solve the entire flow field."""
        self.grid = MOCGrid()
        current_line = initial_line
        
        for i, point in enumerate(initial_line):
            self.grid.add_point(0, i, point)
        
        for i in range(1, num_lines):
            print(f"Solving line {i}")  # Add this line
            next_line = self.solve_next_line(current_line, wall_angle)
            for j, point in enumerate(next_line):
                self.grid.add_point(i, j, point)
            current_line = next_line
        
        return self.grid
    
    def plot_flow_field(self, ax=None):
        """Plot the flow field showing characteristic lines and Mach number distribution."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))

        x_coords, y_coords, mach_values = [], [], []
        for (i, j), point in self.grid.points.items():
            x_coords.append(point.x)
            y_coords.append(point.y)
            mach_values.append(point.mach)

        # Plot characteristic lines
        for i in range(max(i for i, _ in self.grid.points.keys()) + 1):
            line_points = [self.grid.get_point(i, j) for j in range(max(j for _, j in self.grid.points.keys()) + 1) if self.grid.get_point(i, j) is not None]
            ax.plot([p.x for p in line_points], [p.y for p in line_points], 'k-', linewidth=0.5)

        # Plot Mach number distribution
        scatter = ax.scatter(x_coords, y_coords, c=mach_values, cmap='viridis', s=20)
        plt.colorbar(scatter, label='Mach Number')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Method of Characteristics Flow Field')
        ax.grid(True, linestyle='--', alpha=0.7)

        return ax

# Example usage
solver = MOCCharacteristicSolver()
initial_mach = 2.0
initial_angle = 0  # radians
x_start = 0
y_start = 0
y_end = 1
num_initial_points = 20
num_lines = 40
wall_angle = np.radians(5)  # 5 degree wall angle

initial_line = solver.generate_initial_line(x_start, y_start, y_end, initial_mach, initial_angle, num_initial_points)
flow_field = solver.solve_flow_field(initial_line, num_lines, wall_angle)

# Plot the results
fig, ax = plt.subplots(figsize=(12, 8))
solver.plot_flow_field(ax)
plt.tight_layout()
plt.show()

# Print some results
for i in range(0, num_lines, 5):  # Print every 5th line to reduce output
    point = flow_field.get_point(i, 0)  # Lower wall points
    print(f"Line {i}, Lower wall: {point}")