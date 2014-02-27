import os
import sys
import time
import h5py
import json
import numpy as np

k, l = 50, 128

def create(n):
    """Create a contiguous array of size (n,k,l)."""
    n = int(n)
    filename = 'test_%d.h5' % n
    if os.path.exists(filename):
        return filename
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
    return filename

def read(a, out, ind):
    for j, i in enumerate(ind):
        out[j:j+1,...] = a[i:i+1,...]
    return out

def benchmark(n):
    filename = create(n)
    
    ind = np.random.randint(size=100, low=0, high=n)
    ind = np.unique(ind)
    size = len(ind)

    with h5py.File(filename, "r") as f:
        a = f['/test']
        out = np.empty((len(ind),k,l), dtype=a.dtype)
        t0 = time.clock()
        read(a, out, ind)
        t1 = time.clock()
        
    d = t1-t0
    bandwidth = size*k*l*2/(1024*1024.)/d

    return bandwidth
    
n_list = np.linspace(100000, 600000, 6)
bandwidth_list = []
for n in n_list:
    n = int(n)
    print "Size: ", n
    bandwidth = benchmark(n)
    bandwidth_list.append(bandwidth)
    print("Bandwidth: {0:.1f} MB/s".format(bandwidth))
    print

import matplotlib.pyplot as plt
plt.plot(n_list, bandwidth_list);
plt.ylim(0);
plt.xlabel("Number of rows");
plt.ylabel("Bandwidth (MB/s)");
plt.show()
