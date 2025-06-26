#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def f (x, y):
    return exp (-x**2 -y**2 + x*y + 3*x - 4) / (2*np.pi*sqrt(3))

def plot_contour ():
    N = 100
    xx = np.linspace (-1.5, 5, N)
    yy = np.linspace (-1.5, 3.5, N)
    X,Y = np.meshgrid (xx, yy)
    Z = f(X, Y)
    contour (X, Y, Z, levels=7, colors='black')
    # contour (X, Y, Z, levels=7, cmap='Greys')
    axis ([-1.5,5,-1.5,3.5])
    xlabel (r'$x$',fontsize=32)
    ylabel (r'$y$',fontsize=32,rotation=0,labelpad=17)

def main ():
    putil.fontsize (20)
    plot_contour ()
    xticks (range(-1,6))
    if len(sys.argv) > 1:
        putil.savefig (sys.argv[1])
    show ()


if __name__ == "__main__":
    main ()
