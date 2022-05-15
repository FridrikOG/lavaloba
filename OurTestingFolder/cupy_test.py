import cupy as cp
from cupyx.profiler import benchmark

def test(a):
    return cp.linalg.norm(a)

x_gpu = cp.array([1, 2, 3])
print(benchmark(test, (x_gpu,), n_repeat=20)) 