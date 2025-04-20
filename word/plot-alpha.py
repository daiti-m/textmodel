#!/usr/local/bin/python2

import sys
import putil
import numpy as np
from pylab import *

def main ():
    alphas = np.loadtxt (sys.argv[1], dtype=float)
    V = len(alphas)
    plot (range(V), alphas)
    # plot (range(V), sorted(alphas, reverse=True))
    yscale ('log')
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2])
    show ()

if __name__ == "__main__":
    main ()
