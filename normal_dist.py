import math
import numpy as np

def standard_normal_cdf(z):
    if np.isscalar(z):
        return 0.5*(1 + math.erf(z/np.sqrt(2.0)))

    z_arr = np.asarray(z)
    erf_vec = np.vectorize(math.erf)
    return 0.5*(1 + erf_vec(z/np.sqrt(2.0)))
    
