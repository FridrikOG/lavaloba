from matplotlib.patches import Ellipse
from matplotlib.collections import PatchCollection
import numpy as np
import matplotlib.pyplot as plt
from numba import cuda
from numba import jit


@cuda.jit
def parallel_elipse(angles):
    pos = cuda.grid(1)
    if pos < len(angles):
        sm = Ellipse((0, 0), 4, 2, angle=angles[pos], alpha=0.1)
        ax.add_artist(sm)


angle_step = 45  # degrees
angles = np.arange(0, 360, angle_step)


print("ANGLES: ", angles)

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})


threads = 32
block = 2
parallel_elipse[threads, block](angles)

# for angle in angles:
#     ellipse = Ellipse((0, 0), 4, 2, angle=angle, alpha=0.1)
#     print(ellipse)
#     ax.add_artist(ellipse)


ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)

plt.show()
