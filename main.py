import numpy             as np
import matplotlib.pyplot as plt

from   matplotlib import use

# set matplotlib backend to agg (which is hopefully faster?)
# use('agg')

HBAR = 1.0545718e-34  # planck's constant
M_E  = 9.10938356e-31 # mass of an electron
DT   = 1      # simulation timestep
N    = 100    # number of timesteps
L    = 30     # grid size in all dimensions

class grid():
    def __init__(self, x: float, y: float, 
                       z: float, s: float):
        assert(x == y == z)

        x_    = y_    = z_     = np.linspace(0, x, s)
        self.x, self.y, self.z = np.meshgrid(x_, y_, z_, indexing='ij')

GRID       = grid(L, L, L, L) # discretised grid w/ dimensions LxLxL
xx, yy, zz = GRID.x, GRID.y, GRID.z

psi_0 = (1 / L) * np.sin(np.pi * xx / L) * np.sin(np.pi * yy / L) * np.sin(np.pi * zz / L)
psi_0 = psi_0 / np.sqrt(np.sum(np.abs(psi_0)**2) * (L / N)**3)

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Ground State Wavefunction')

xx    = xx[::2, ::2, ::2]
yy    = yy[::2, ::2, ::2]
zz    = zz[::2, ::2, ::2]

psi_0 = psi_0[::2, ::2, ::2]

prob_density = np.abs(psi_0)**2
ax.scatter(xx, yy, zz, c=prob_density, cmap='viridis', s=10)

plt.show()