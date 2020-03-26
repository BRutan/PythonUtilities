##########################################
# options_mc.py
##########################################
# Description:
# * Generate asset prices using Monte
# Carlo to calculate option prices.


import numpy as np 
cimport numpy as np
import cython
from libc.stdlib cimport rand,RAND_MAX
from libc.math cimport sqrt

@cython.boundscheck(False)
def MonteCarlo(sde, icdf, int targetParam, args, int numpaths, int numsteps):
    cdef int path = 0
    cdef int step
    cdef double start = args[targetParam]
    cdef np.ndarray[np.float_t,ndim=1,negative_indices=False,mode='c'] output = np.empty(shape=(numpaths, ))

    print(numsteps)
    start = args[targetParam]
    while path < numpaths:
        val = start
        step = 0
        while step < numsteps:
            args[7] = icdf(float(rand())/float(RAND_MAX))
            val = sde(args)
            if val == 0:
                break
            args[targetParam] = val
            step += 1
        output[path] = val
        path += 1
        args[targetParam] = start
    return output