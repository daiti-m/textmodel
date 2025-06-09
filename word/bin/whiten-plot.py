#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def usage ():
    print ('usage: % whiten-plot.py X.dat [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    putil.fontsize (20)
    X = np.loadtxt (sys.argv[1], dtype=float)
    X = X - np.mean(X,0)
    scatter (X[:,0], X[:,1], color='black')
    # xmax = 5.5; ymax = 5.5
    xmax = 0.6; ymax = 0.6
    plot ([-xmax,xmax],[0,0],linewidth=1,color='black')
    plot ([0,0],[-ymax,ymax],linewidth=1,color='black')
    axis ([-xmax,xmax,-ymax,ymax])
    # xticks (np.arange(-4,6,2))
    xticks (np.arange(-0.6,0.8,0.2))
    putil.aspect_ratio (1)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=200)
    show ()

if __name__ == "__main__":
    main ()
