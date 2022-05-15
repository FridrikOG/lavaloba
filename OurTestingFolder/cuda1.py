from __future__ import division
from numba import cuda
import numpy as np
import math
from numba import vectorize, int64, float32, float64
from numba import jit

@vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)])
def cube_formula_numba_vec(x,y):
    return x*y


@vectorize([float64(int64,int64), float32(float32,float32), float64(float64,float64)])
def arctan2(x,y):
    return math.atan2(x, y)


@vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)])
def multiply_array(n, arr):
    return n*arr

@vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)])
def add_array(n, arr):
    return n+arr

@vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)])
def sub_array(n, arr):
    return n-arr

@jit(nopython=True)
def ellipse_cuda( xc , yc , ax1 , ax2 , angle , X_circle , Y_circle ):
    cos_angle = math.cos(angle*np.pi/180)
    sin_angle = math.sin(angle*np.pi/180)

    # x1 = xc + ax1 * cos_angle
    # y1 = yc + ax1 * sin_angle

    # x2 = xc - ax2 * sin_angle
    # y2 = yc + ax2 * cos_angle

    X = multiply_array(ax1, X_circle)
    Y = multiply_array(ax2, Y_circle)
    # X = ax1 * X_circle
    # Y = ax2 * Y_circle

    xe = add_array(sub_array(multiply_array(X,cos_angle), multiply_array(Y,sin_angle)),xc)
    ye = add_array(sub_array(multiply_array(Y,cos_angle), multiply_array(X,sin_angle)),yc)
    # xe = xc + X*cos_angle - Y*sin_angle
    # ye = yc + X*sin_angle + Y*cos_angle

    out = (xe,ye)
    return out



xc = 288830.0
yc = 2150362.0
ax1 = 26.081118798477803
ax2 = 24.409220221209875
angle = 39.8274074028988
x_circle = np.full((30), 4.0)
y_circle = np.full((30), 3.0)


(xe, ye ) = ellipse_cuda(xc, yc, ax1, ax2, angle, x_circle, y_circle)

print(xe)

# @cuda.jit
# def cuda_elip_1(ax, circle, new_array):
#     pos = cuda.grid(1)
#     if pos < circle.size:
#         new_array[pos] = ax * circle[pos]


@cuda.jit
def something(io_array):
    i = cuda.grid(1)
    if i < io_array.size:
        io_array[i] = io_array[i] + i

  

 
data = np.ones(256)
threadsperblock = 256
blockspergrid = math.ceil(data.shape[0] / threadsperblock)
something[blockspergrid, threadsperblock](data)

# threads = 256
# blocks = 1
# a = [0,0]
# b = [0,0]
# c = [0,0]


# # in Python
# @cuda.jit
# def addKernel(a, b, c):
#     i = cuda.grid(1)
#     if i < a.size:
#         c[i] = a[i] + b[i]


# addKernel[threads, blocks](a, b, c)



# ax1 = 0.00001
# X_circle = np.ones(5)
# X = np.zeros(X_circle.size)

# threads = X_circle.size
# blockspergrid = 1

# cuda_elip_1[threads, blockspergrid](ax1, X_circle, X)



