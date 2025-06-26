#!/usr/local/bin/python

import sys
import numpy as np
from scipy.special import kv as besselk
from pylab import *

def igp (n, x, a):
    y = sqrt (x*x + a*a) - x
    f = (log(2*a) - log(np.pi)) / 2 + y + n * log (x * y / a) \
        - np.sum (log (np.arange(1,n+1)))
    return exp (f) * besselk (n - 1/2, a)

def usage ():
    print ('usage: % igp_plot.py xi alpha N [output]')
    print ('$Id$')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        x = float (sys.argv[1])
        a = float (sys.argv[2])
        N = int (sys.argv[3])

    xx = np.arange (1,N+1)
    yy = [igp(n,x,a) for n in xx]
    plot (xx, yy, color='black')
    show ()



if __name__ == "__main__":
    main ()
