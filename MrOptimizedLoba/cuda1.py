from __future__ import division
from numba import cuda
import numpy as np
import math


@cuda.jit
def cuda_elip_1(ax, circle, new_array):
    pos = cuda.grid(1)
    if pos < circle.size:
        new_array[pos] = ax * circle[pos]

# CUDA kernel
# @cuda.jit
# def something(io_array):
#     pos = cuda.grid(1)
#     if pos == 0:
#         io_array[pos] = 1
#     elif pos < 256:
#         io_array[pos] = io_array[pos-1] + 2 # do the computation
  

# Host code   
# data = numpy.ones(256)
# threadsperblock = 256
# blockspergrid = math.ceil(data.shape[0] / threadsperblock)
# something[blockspergrid, threadsperblock](data)


ax1 = 0.00001
X_circle = np.ones(5)
X = np.zeros(X_circle.size)

threads = X_circle.size
blockspergrid = 1

cuda_elip_1[threads, blockspergrid](ax1, X_circle, X)



