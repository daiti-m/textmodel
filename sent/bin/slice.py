#!/usr/local/bin/python
#
#    Unbounded slice sampling in Python.
#    $Id: slice.py,v 1.2 2021/12/06 02:43:46 daichi Exp $
#
#  References: "Unbounded Slice Sampling", Daichi Mochihashi.
#  Research Memorandum No.1209, The Institute of Statistical Mathematics, 2020.
#  (arXiv:2010.01760)
#
import sys
from numpy import exp, log
from numpy.random import rand

A = 100
maxiter = 1000

def expand (p):
    return (- A * log (1 / p - 1))

def shrink (x):
    return  1 / (1 + exp (- x / A))

def unif (st, ed):
    return st + (ed - st) * rand()

def sample (x, loglik, *args):
    st = 0; ed = 1
    r = shrink (x)
    slice = loglik (x, *args) - log (A * r * (1 - r)) + log (rand())
    # slice = loglik (x) - log (A * r * (1 - r)) + log (rand())
    # body
    for iter in range(maxiter):
        rnew = unif (st, ed)
        xnew = expand (rnew)
        newlik = loglik (xnew, *args) - log (A * rnew * (1 - rnew))
        # newlik = loglik (xnew) - log (A * rnew * (1 - rnew))
        if (newlik > slice):
            return expand (rnew)
        elif (rnew > r):
            ed = rnew
        elif (rnew < r):
            st = rnew
        else:
            return x
    sys.stderr.write ('slice.sample: max iteration %d reached.' % maxiter)
    return x


import matplotlib.pyplot as plt

def main ():
    def f (x):
        return - x * (x - 1) * (x - 2) * (x - 3.5)
    x = 0.5
    N = int (sys.argv[1])
    result = []
    for n in range(N):
        x = sample (x, f)
        result.append (x)
    plt.hist (result, bins=int(log(N)*4))
    plt.show ()


if __name__ == "__main__":
    main ()
