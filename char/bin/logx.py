#!/usr/local/bin/python2

import sys
import putil
import numpy as np
from pylab import *

M = 5

def plot_function (xx):
    yy = [log(x) for x in xx]
    putil.aspect_ratio (1)
    putil.fontsize (24)
    plot (xx, yy, 'k')
    text (M+0.25, 0, r'$x$', fontsize=32, va='center')
    text (0, 2.8, r'$y$', fontsize=32, ha='center')
    text (5.3, 1.7, r'$y=\log\, x$', fontsize=28, va='center')
    text (3.4, 2.7, r'$y=x\!-\!1$', fontsize=28, va='center')
    xticks (range(1,M))
    yticks (range(-4,3))
    xlim (0, M)
    ylim (-M+0.5, 2.3)
    putil.zero_origin ()
    putil.simpleaxis ()

def plot_tangent (xx):
    xx = np.linspace (-0.5, M, 200)
    yy = [x - 1 for x in xx]
    plot (xx, yy, 'k', linestyle='dashed')

def main ():
    N = 200
    xx = np.linspace (0, M, N)
    figure (figsize=(6,6))
    plot_tangent (xx)
    plot_function (xx)
    if len(sys.argv) > 1:
        putil.savefig (sys.argv[1])
    show ()


if __name__ == '__main__':
    main ()
