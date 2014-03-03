import os
import sys
import timeit
import h5py
import numpy as np

n, k, l = 500000, 40, 40

def create(chunksize):
    """Create a contiguous array of size (n,k,l)."""
    with h5py.File('test_' + str(chunksize), "w") as f:
        a = f.create_dataset('/test',
                             dtype=np.int16,
                             shape=(n,k,l), 
                             chunks=(chunksize,k,l))
        # n_ = n//10
        for i in range(n//chunksize):
            print i,n//chunksize
            a[i*chunksize:(i+1)*chunksize,...] = np.random.randint(size=(chunksize,k,l),
                                                     low=-32000,
                                                     high=32000)
        print

def read(a, out):
    for j, i in enumerate(ind):
        out[j:j+1,...] = a[i:i+1,...]
    return out
    
SIZES = (2500, 5000, 10000, 25000)
    
size = 200
ind = np.random.randint(size=(size), low=0, high=n)
ind = np.unique(ind)

def create_all():
    for chunksize in SIZES:
        create(chunksize)

def test(chunksize):
    filename = "test_" + str(chunksize)
    
    with h5py.File(filename, "r") as f:
        a = f['/test']
        out = np.empty((size,k,l), dtype=a.dtype)
        t0 = timeit.default_timer()
        read(a, out)
        t1 = timeit.default_timer()
        
    d = t1-t0
    bandwidth = size*k*l*2/(1024*1024.*d)

    return bandwidth
    
# create_all()

for chunksize in SIZES:
    print chunksize, str(test(chunksize)) + " MB/s"
