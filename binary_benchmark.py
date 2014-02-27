"""Benchmark of seek and read on Windows."""
import os
import timeit
import numpy as np

n, k, l = 500000, 50, 128
nbytes = n*k*l*2
size = 1000

if not os.path.exists('binary'):
    with open('binary', 'wb') as f:
        for _ in range(100):
            print _,
            np.random.randint(low=-32000, high=32000, size=nbytes//200).astype(np.int16).tofile(f)
    
with open('binary', 'rb') as f:
    t00 = timeit.default_timer()
    for j, i in enumerate(np.arange(0, n, n//size).astype(np.int64)+0):
        f.seek(i*k*l*2L)
        f.read(k*l*2L)
    t11 = timeit.default_timer()

d = t11-t00
bandwidth = size*k*l*2/(1024*1024.*d)

print("Elapsed: {0:.2f} s".format(d))
print("Bandwidth: {0:.1f} MB/s".format(bandwidth))
