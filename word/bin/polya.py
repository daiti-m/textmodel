#!/usr/local/bin/python

import sys
import fmatrix
import numpy as np
from eprint import eprint,eprintf
from scipy.special import psi
from util import converged
from pylab import *

def newton (docs, maxiter=200):
    V = lexicon (docs)
    alpha = np.ones (V, dtype=float) * 1e-2
    eprint ('optimizing alpha (V=%d)..' % V)
    for iter in range(maxiter):
        eprintf ('iteration [%d]..\r' % (iter+1))
        z = np.zeros (V, dtype=float)
        s = 0
        salpha = np.sum (alpha)
        oldalpha = alpha
        for doc in docs:
            index = doc.id
            z[index] += psi (alpha[index] + doc.cnt) - psi (alpha[index])
            s += psi (salpha + np.sum(doc.cnt)) - psi (salpha)
        alpha = alpha * z / s
        if converged(alpha, oldalpha, 1e-4):
            eprint ('converged at iteration %d.' % (iter+1))
            break
    return alpha

def lexicon (docs):
    V = 0
    for doc in docs:
        if (max(doc.id) > V):
            V = max(doc.id)
    return V + 1

def read (file):
    return fmatrix.parse (file, 1)

def write (alphas, file):
    with open (file, 'w') as fh:
        for alpha in alphas:
            fh.write ('% .6f\n' % alpha)

def usage ():
    print ('usage: % polya.py train.dat model')
    print ('$Id: polya.py,v 1.1 2021/05/04 04:24:02 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        train = sys.argv[1]
        model = sys.argv[2]

    docs = read (train)
    alphas = newton (docs)
    write (alphas, model)


if __name__ == "__main__":
    main ()
