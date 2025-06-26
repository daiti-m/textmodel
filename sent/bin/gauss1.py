#!/usr/local/bin/python

import sys
import numpy as np
import putil
from numpy import exp,sqrt
from pylab import *

lim = 5
ratio = 6

def gauss1 (x):
    s = 1
    return 1 / (sqrt(2*np.pi) * s) * exp (- x*x / (2 * s * s))

def add_xy ():
    ax = gca().axes
    ax.text(lim+0.3,0,r'$x$',va='center',fontsize=20)
    ax.text(0,0.53,r'$p(x)$',ha='center')

def plot_gauss (N):
    xx = np.linspace (-lim, lim, N)
    yy = [gauss1(x) for x in xx]
    plot (xx, yy)
    axis ([-lim,lim,0,0.48])
    xticks (np.arange(-lim,lim+1,1))
    yticks (np.arange(0,0.5,0.1))
    putil.simpleaxis ()
    putil.zero_origin ()
    putil.aspect_ratio (ratio)
    putil.yticklabels (("","0.1","0.2","0.3","0.4"))
    add_xy ()

def main ():
    N = 100
    plot_gauss (N)
    if len(sys.argv) > 1:
        putil.savefig (sys.argv[1])
    show ()

if __name__ == "__main__":
    main ()
