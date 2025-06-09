#!/usr/local/bin/python

import sys
import numpy as np
from numpy.linalg import eig
from pylab import *

def whiten (X):
    mu = np.mean (X,0)
    X = X - mu
    eigs,P = eig (np.dot(X.T,X))
    Z = np.dot(X, np.dot(P, diag(1/sqrt(eigs))))
    return Z

def usage ():
    print ('usage: % whiten.py words.vec output')
    print ('$Id: whiten.py,v 1.1 2022/07/26 03:50:13 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()

    X = np.loadtxt (sys.argv[1], dtype=float)
    Z = whiten (X)
    np.savetxt (sys.argv[2], Z, fmt='% .7f')

if __name__ == "__main__":
    main ()
