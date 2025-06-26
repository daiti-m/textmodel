#!/usr/local/bin/python

import sys
import numpy as np
from pylab import *

def npmi (alphas):
    S = np.sum (alphas, 1)
    P = np.dot (diag(1/S), alphas)
    m = np.mean (P, 0)
    NPMI = (log(P) - log(m)) / (- log(m))
    return NPMI

def main ():
    alphas = np.array ([[1,2,3],[2,1,4]])
    print (alphas)
    I = npmi (alphas)
    print (I)
    







if __name__ == "__main__":
    main ()
