import math
import numpy as np
import matplotlib.pyplot as plt
from   mpl_toolkits.mplot3d import Axes3D

HBAR = 1.0545718e-34  # planck's constant
M_E  = 9.10938356e-31 # mass of an electron
DT   = 1              # simulation timestep
N    = 100            # number of timesteps
L    = 15             # grid size in all dimensions
EF   = 3              # exponentiation factor for point size in scatterplot

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

    ax.scatter(x_threshold, y_threshold, z_threshold, 
               c=pd_threshold, cmap='viridis', s=np.minimum((pd_threshold * 1000)**EF, 50))

    plt.show()

# constraints: n > l

n = 4  # principal quantum number
l = 3  # azimuthal quantum number
m = 0  # magnetic quantum number

plot_hydrogen_wavefunction(n, l, m, threshold = 0.001)