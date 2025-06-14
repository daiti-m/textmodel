#!/usr/local/bin/python
#
#    rutil.py
#    random number utility.
#    $Id: rutil.py,v 1.7 2023/02/14 02:37:18 daichi Exp $
#
from numpy.random import rand,randn
from numpy import log, exp
from scipy.stats import gamma
import numpy as np
import time
import sys
import os

def srand ():
    if 'SEED' in os.environ:
        seed = int (os.getenv('SEED'))
    else:
        seed = int (time.time())
    np.random.seed (seed)

def dirichlet (alpha):
    xx = gamma.rvs (alpha)
    return xx / np.sum(xx)

def bernoulli (p):
    if rand() < p:
        return 1
    else:
        return 0

def multinom (p):
    K = len(p)
    r = rand()
    s = 0
    for k in range(K):
        s += p[k]
        if (r <= s):
            return k
    sys.stderr.write ('multinom: total > 1! (s=%g)\n' % s)
    return (K-1)

def pmultinom (p):
    return multinom (p / np.sum(p))

def lmultinom (lik):
    theta = exp (lik - logsumexp(lik))
    return multinom (theta)

def lnormalize (lik):
    return exp (lik - logsumexp(lik))

def logsumexp (x):
    y = max (x)
    return y + log(sum(exp(x - y)))

def unif (low, high):
    return low + rand() * (high - low)
    
def main ():
    # theta = log ([0.1,0.2,0.3,0.4])
    theta = np.array ([-24.240, -15.325, -5.236, -5.853, -7.668, -8.233])
    N = int(sys.argv[1])
    for n in range(N):
        print (lmultinom(theta))
    
if __name__ == "__main__":
    main ()
