import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np

class Flower:

    def __init__(self, num_petals, radius=1):
        self.num_petals = num_petals
        self.radius = radius
        self.petal_paths = []
        self.circle_path = None
    
    def draw_center(self):
        """Draw the center of the flower."""
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.radius * np.cos(theta)
        y = self.radius * np.sin(theta)
        plt.fill(x, y, linewidth=2, facecolor='white', edgecolor='black', zorder=2)
        # Return the path of the circle.
        return mpath.Path(np.column_stack((x, y)))

    def draw_petal(self, angle, width):
        """Draw a petal of the flower."""
        height = self.radius
        theta = np.linspace(0, 2 * np.pi, 100)
        r_width = width / 2
        r_height = height / 2

        x_base = r_width * np.cos(theta)
        y_base = r_height * np.sin(theta) + self.radius + r_height / 2

        x_rotated = x_base * np.cos(angle) - y_base * np.sin(angle)
        y_rotated = x_base * np.sin(angle) + y_base * np.cos(angle)

        petal_artist, = plt.fill(x_rotated, y_rotated, linewidth=2, facecolor='None', edgecolor='black', zorder=1)
        # Return the path of the petal.
        return petal_artist

    def draw(self):
        """Draw the flower.""" 
        width = 2 * np.pi * self.radius / self.num_petals
        psi = 2 * np.pi / self.num_petals
        angle = 0

        petal_paths = []
        for i in range(self.num_petals):
            petal_path = self.draw_petal(angle, width)
            petal_paths.append(petal_path)
            angle += psi

        circle_path = self.draw_center()
        self.circle_path, self.petal_paths = circle_path, petal_paths


