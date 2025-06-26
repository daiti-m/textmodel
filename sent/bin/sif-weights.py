#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def sif (p,a):
    return a / (p + a)

def plot_sif (a):
    M = 130
    p = 0.9
    xx = [p**n for n in range(M)]
    yy = [sif(x,a) for x in xx]
    plot (xx, yy)

def usage ():
    print ('usage: % sif-weights.py a [output]')
    print ('$Id: sif-weights.py,v 1.1 2022/09/11 21:21:19 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    a = float (sys.argv[1])
    putil.figsize ((7,3.5))
    putil.fontsize (20)
    plot_sif (a)
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
