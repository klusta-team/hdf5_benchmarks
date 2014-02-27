import os
import sys
import timeit
import h5py
import numpy as np

n, k, l = 500000, 50, 128

def create(filename):
    """Create a contiguous array of size (n,k,l)."""
    with h5py.File(filename, "w") as f:
        print("Creating HDF5 file...")
        a = f.create_dataset('/test',dtype=np.int16,
                             shape=(n,k,l))
        n_ = n//10
        for i in range(10):
            print i,
            a[i*n_:(i+1)*n_,...] = np.random.randint(size=(n_,k,l),
                                                     low=-32000,
                                                     high=32000)

filename = 'test.h5'
if not os.path.exists(filename):
    create(filename)

def read(a, out):
    for j, i in enumerate(ind):
        out[j:j+1,...] = a[i:i+1,...]
    return out

ind = np.random.randint(size=100, low=0, high=n)
ind = np.unique(ind)
size = len(ind)

with h5py.File(filename, "r") as f:
    a = f['/test']
    out = np.empty((len(ind),k,l), dtype=a.dtype)
    t0 = timeit.default_timer()
    read(a, out)
    t1 = timeit.default_timer()
    
d = t1-t0
bandwidth = size*k*l*2/(1024*1024.)/d

print("Elapsed: {0:.2f} s".format(d))
print("Bandwidth: {0:.1f} MB/s".format(bandwidth))

