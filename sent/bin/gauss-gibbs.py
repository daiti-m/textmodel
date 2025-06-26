#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def gibbs (iters):
    x,y = -1,-1
    samples = [[x,y]]
    for iter in range(iters):
        # draw y
        y = x / 2 + randn() / sqrt(2)
        samples.append ([x,y])
        # draw x
        x = (y + 3) / 2 + randn() / sqrt(2)
        samples.append ([x,y])
    return np.array (samples)

def usage ():
    print ('usage: gauss-gibbs.py iters [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    iters = int (sys.argv[1])
    samples = gibbs (iters)
    putil.fontsize (20)
    plot (samples.T[0], samples.T[1], color='black')
    axis ([-1.5,5,-1.5,3.5])
    xticks (range(-1,6))
    xlabel (r'$x$',fontsize=32)
    ylabel (r'$y$',fontsize=32,rotation=0,labelpad=17)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2])
    show ()


if __name__ == "__main__":
    main ()
