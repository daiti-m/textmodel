#!/usr/local/bin/python2

import sys
import putil
import numpy as np
from pylab import *

def f (x):
    return 2 * log (x) + 2 * log (x+1) + log (x+2) - 5 * log (12 + 46*x)

def plot_function (xx):
    yy = [f(x) for x in xx]
    plot (xx, yy)
    xlabel (r'$\alpha$', fontsize=24)
    # ylabel (r"$\log\,p(Y'|Y,\alpha)$", fontsize=24, labelpad=50, rotation=0)
    text (-0.8, -18.9, r"$\log\,p(D'|D,\alpha)$", fontsize=24, va='center')
    yticks (np.arange(-20,-16,1))

def main ():
    N = int (sys.argv[1])
    xx = np.linspace (0, 1, N)
    figure (figsize=(5,2.5))
    plot_function (xx)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2])
    show ()




if __name__ == '__main__':
    main ()
