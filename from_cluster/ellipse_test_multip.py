# import multiprocessing as mp
# pool = mp.Pool(mp.cpu_count())
# print(pool)
import matplotlib.pyplot as plt
import numpy as np

import multiprocessing
#multiprocessing.freeze_support() # <- may be required on windows

def plot(datax, datay, name):
    x = datax
    y = datay**2
    plt.scatter(x, y, label=name)
    plt.legend()
    plt.show()

def multiP():
    for i in range(2):
        p = multiprocessing.Process(target=plot, args=(i, i, i))
        p.start()

if __name__ == "__main__": 
    input('Value: ') 
    multiP()
# from matplotlib.patches import Ellipse
# from matplotlib.collections import PatchCollection
# import numpy as np
# import matplotlib.pyplot as plt
# from numba import cuda
# from numba import jit
# import multip

# # @cuda.jit
# def parallel_elipse(angles):
#     pos = cuda.grid(1)
#     if pos < len(angles):
#         sm = Ellipse((0, 0), 4, 2, angle=angles[pos], alpha=0.1)
#         ax.add_artist(sm)


# angle_step = 45  # degrees
# angles = np.arange(0, 360, angle_step)


# print("ANGLES: ", angles)

# fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})


# threads = 32
# block = 2
# parallel_elipse[threads, block](angles)

# # for angle in angles:
# #     ellipse = Ellipse((0, 0), 4, 2, angle=angle, alpha=0.1)
# #     print(ellipse)
# #     ax.add_artist(ellipse)


# ax.set_xlim(-2.2, 2.2)
# ax.set_ylim(-2.2, 2.2)

# plt.show()
