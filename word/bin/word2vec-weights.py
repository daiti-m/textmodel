#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def weight (p,t):
    return 1 - max (1 - sqrt(t/p), 0)

def plot_weights (t):
    M = 130
    p = 0.9
    xx = [p**n for n in range(M)]
    yy = [weight(x,t) for x in xx]
    plot (xx, yy)

def usage ():
    print ('usage: % word2vec-weights.py t [output]')
    print ('$Id: sif-weights.py,v 1.4 2022/08/31 02:30:30 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    t = float (sys.argv[1])
    putil.figsize ((7,3.5))
    putil.fontsize (20)
    plot_weights (t)
    xscale ('log')
    xlabel (r'$p$', fontsize=32, labelpad=4)
    ylabel ('Weight', labelpad=15, fontsize=24)
    xticks ([10**(-n) for n in range(6,-1,-1)])
    yticks ([0,0.25,0.5,0.75,1])
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=200)
    show ()


if __name__ == "__main__":
    main ()
