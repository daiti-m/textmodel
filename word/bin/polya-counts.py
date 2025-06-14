#!/usr/local/bin/python

import sys
import putil
import numpy as np
from scipy.special import gammaln
from pylab import *

def polyalik (alpha, n):
    alpha0 = 50
    N = 100
    return gammaln (alpha + n) - gammaln (alpha)

def plot_polya (alphas, N):
    nn = np.arange (1,N+1)
    markers = ['x', '^', 'o', '>', '<']
    styles = ['solid', 'dashdot', 'dashed', 'dotted']
    putil.fontsize (24)
    for alpha,marker,style in list (zip (alphas, markers, styles)):
        yy = [polyalik (alpha, n) for n in nn]
        plot (nn, yy, color='k', linestyle=style,
              label = (r'$\alpha=%g$' % alpha))
    legend (labelspacing=0.2)
    xticks (range(1,N+1))
    xlabel (r'$n$', fontsize=32)
    ylabel (r'$\log\dfrac{\Gamma(\alpha\!+\!n)}{\Gamma(\alpha)}$')
    

def usage ():
    print ('usage: % polya-counts.py N [output]')
    print ('$Id: polya-counts.py,v 1.2 2023/04/14 22:17:35 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        N = int (sys.argv[1])
        alphas = [1, 0.1, 0.01, 0.001]

    plot_polya (alphas, N)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()



if __name__ == "__main__":
    main ()
