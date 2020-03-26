############################
# Cythoned.py
############################
# Description:
# * Cythoned versions of expensive functions.

import numpy as np 
cimport numpy as np
import cython
from libc.stdlib cimport rand,RAND_MAX
from libc.math cimport sqrt 


cdef dict Dict
ctypedef float (*sde_type)(dict)

@cython.boundscheck(False)
cdef monte_carlo(sde_type sde, int targetParam, int numpaths, int numsteps):
    pass
