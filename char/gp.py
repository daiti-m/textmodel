#!/usr/local/bin/python2
#
#    gp.py -- Gaussian process sampling module.
#    $Id: gp.py,v 1.2 2021/10/17 01:58:55 daichi Exp $
#
import sys
import putil
import numpy as np
from pylab import *
from numpy.random import multivariate_normal as mvnrand

N = 100
M = 4

def gp (xx, kernel):
    N = len(xx)
    K = kernel_matrix (xx, kernel)
    return mvnrand (np.zeros(N), K)

def cgp (xx, xtrain, ytrain, kernel): # conditional Gaussian process
    K = kernel_matrix (xtrain, kernel)
    Kinv = inv(K)
    k = np.array ([kv(x, xtrain, kernel) for x in xx])
    kk = np.array ([kv(x, xx, kernel) for x in xx])
    # posterior Gaussian
    mu = k.dot(Kinv).dot(ytrain)
    Knew = kk - k.dot(Kinv).dot(k.T)
    # return mu
    return mvnrand (mu, Knew)
    
def kgauss (params):
    [tau,sigma] = params
    return lambda x,y: tau * exp (-(x - y)**2 / (sigma*sigma))

def kernel_matrix (xx, kernel):
    N = len(xx)
    eta = 1e-2
    return np.array (
        [kernel (xi, xj) for xi in xx for xj in xx]
    ).reshape(N,N) + eta * np.eye(N)

def kv (x, xtrain, kernel):
    return np.array ([kernel(x,xi) for xi in xtrain])

def sigmoid (x):
    return 1 / (1 + exp (-x))

def draw_gp (kernel):
    xx = np.linspace (-M, M, N)
    plot (xx, gp (xx, kernel), 'k')

def draw_cgp (data, kernel):
    xx = np.linspace (-M, M, N)
    xtrain = np.array(data).T[0]
    ytrain = np.array(data).T[1]
    plot (xx, sigmoid (cgp (xx, xtrain, ytrain, kernel)), 'k')

def usage ():
    print 'usage: % gp.py [output]'
    sys.exit (0)

def main ():
    data = [[-4,-10], [-3,-8], [-2,-6], [0,-1], [3,-5], [4,-10]]
    kernel = kgauss ((1,1))
    figure (figsize=(6,3))
    draw_cgp (data, kernel)
    putil.simpleaxis ()
    xlim (-M,M)
    if len(sys.argv) > 1:
        putil.savefig (sys.argv[1])
    show ()

if __name__ == "__main__":
    main ()
