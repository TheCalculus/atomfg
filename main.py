import math
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider

import sys

if len(sys.argv) == 1:
    L    = 50             # grid size in all dimensions
    EF   = 0.1            # exponentiation factor for point size in scatterplot

    HIGH_SPEED        = False     # default (0) -> AGG (1)
    INIT_VIEW_THETA_X = 21.5
    INIT_VIEW_THETA_Y = 45

    # constraints: n > l

    n = 4  # principal quantum number
    l = 0  # azimuthal quantum number
    m = 0  # magnetic quantum number
else:
    print(sys.argv)

    L    = int(sys.argv[3])
    EF   = float(sys.argv[4])

    HIGH_SPEED = bool(sys.argv[5])
    
    INIT_VIEW_THETA_X = float(sys.argv[6])
    INIT_VIEW_THETA_Y = float(sys.argv[7])

    n = int(sys.argv[8])
    l = int(sys.argv[9])
    m = int(sys.argv[10])


if HIGH_SPEED:
    plt.switch_backend('Agg')
    plt.ioff()

class HydrogenAtom:
    def __init__(self, n, l, m):
        self.n = n
        self.l = l
        self.m = m

        x        = y      = z     = np.linspace(0, L, L)
        self.xx, self.yy, self.zz = np.meshgrid(x, y, z, indexing='ij')

        self.psi = self.calculate_wavefunction()

    def calculate_wavefunction(self):
        offset  = L / 2 # center wavefunction

        self.xx = self.xx - offset
        self.yy = self.yy - offset
        self.zz = self.zz - offset

        r     = np.sqrt(self.xx**2 + self.yy**2 + self.zz**2)
        theta = np.arccos(self.zz / r)
        phi   = np.arctan2(self.yy, self.xx)

        # https://quantummechanics.ucsd.edu/ph130a/130_notes/node233.html
        # i'm not too sure about the 'correctness' of this code
        R = (2 / self.n)**3                                           *\
            np.sqrt(1 / (2 * math.factorial(self.n - self.l - 1)))    *\
            (2 * r / self.n)**self.l * np.exp(-r / self.n)         # radial wavefunction
        
        Y_lm = self.spherical_harmonic(self.l, self.m, theta, phi) # angular wavefunction

        psi = R * Y_lm

        return psi

    def spherical_harmonic(self, l, m, theta, phi):
        from scipy.special import sph_harm

        return sph_harm(m, l, phi, theta)

def plot_hydrogen_wavefunction(n, l, m, threshold = 0.01):
    hydrogen_atom = HydrogenAtom(n, l, m)

    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')

    ax.view_init(INIT_VIEW_THETA_X, INIT_VIEW_THETA_Y)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Hydrogen Atom Wavefunction (n={n}, l={l}, m={m})')

    prob_density = np.abs(hydrogen_atom.psi)**2

    threshold_condition = prob_density > threshold
    
    x_threshold = hydrogen_atom.xx[threshold_condition]
    y_threshold = hydrogen_atom.yy[threshold_condition]
    z_threshold = hydrogen_atom.zz[threshold_condition]

    pd_threshold = prob_density[threshold_condition]

    if not HIGH_SPEED:
        ax_expo = plt.axes([0.25, 0.1, 0.65, 0.03])
        expo_slider = Slider(
            ax      = ax_expo,
            label   = 'exponentiation factor',
            valmin  = 0.0001,
            valmax  = 10,
            valinit = 3,
        )

        ax_thresh = plt.axes([0.25, 0.2, 0.65, 0.03])
        thresh_slider = Slider(
            ax      = ax_thresh,
            label   = 'minimum threshold',
            valmin  = 0.0001,
            valmax  = 1,
            valinit = threshold,
        )

    scatter = ax.scatter(x_threshold, y_threshold, z_threshold, 
                        c = pd_threshold, cmap='viridis', s = np.minimum((pd_threshold * 1000) ** EF, 50))

    last_threshold = threshold

    def update(val):
        nonlocal scatter
        nonlocal last_threshold
        nonlocal pd_threshold
        nonlocal prob_density

        global threshold

        exponent  = expo_slider.val
        threshold = thresh_slider.val
        
        if last_threshold == threshold:
            scatter.set_sizes(np.minimum((pd_threshold * 1000) ** exponent, 50))
            fig.canvas.draw_idle()
        else:
            threshold_condition = prob_density > threshold
            pd_threshold = prob_density[threshold_condition]

            # remove plot from 'scatter' and reinitialise data in it
            ax.clear()

            x_threshold = hydrogen_atom.xx[threshold_condition]
            y_threshold = hydrogen_atom.yy[threshold_condition]
            z_threshold = hydrogen_atom.zz[threshold_condition]

            scatter = ax.scatter(x_threshold, y_threshold, z_threshold, 
                                 c = pd_threshold, cmap='viridis', s = np.minimum((pd_threshold * 1000) ** exponent, 50))
        
        last_threshold = threshold

    if not HIGH_SPEED:
        expo_slider.on_changed(update) # redraw scatterplot
        thresh_slider.on_changed(update)

    plt.show() # won't do anything if HIGH_SPEED

plot_hydrogen_wavefunction(n, l, m, threshold = 0.001)

if HIGH_SPEED:
    plt.savefig(str(n) + str(l) + str(m))