#!/usr/local/bin/python
#
#    poch.py
#    plotting Pochhammer function.
#    $Id: poch.py,v 1.4 2023/04/09 02:46:44 daichi Exp $
#
import sys
import putil
import numpy as np
from scipy.special import gammaln
from pylab import *

def poch (alpha, n):
    return gammaln (alpha + n) - gammaln (alpha)

def plot_poch (N):
    figure (figsize=(6,4))
    alphas = [0.001, 0.01, 0.1, 0.2]
    markers = ['x', '^', 'o', '>', '<']
    styles = ['solid', 'dashed', 'dashdot', 'dotted']
    nn = np.arange (1,N+1)
    for alpha,marker in reversed (list(zip (alphas,markers))):
        yy = [poch(alpha,n) for n in nn]
        plot (nn, exp(yy), marker=marker, color='k', linewidth=1, linestyle='solid',
              label = (r'$\alpha=%g$' % alpha))
    xlabel (r'$n$',fontsize=24)
    ylabel (r'$\Gamma(\alpha\!+\!n)/\Gamma(\alpha)$')
    legend ()
    
def plot_lpoch (N):
    figure (figsize=(6,4))
    alphas = [0.001, 0.01, 0.1, 0.2]
    markers = ['x', '^', 'o', '>', '<']
    styles = ['solid', 'dashed', 'dashdot', 'dotted']
    nn = np.arange (1,N+1)
    for alpha,marker in reversed (list(zip (alphas,markers))):
        yy = [poch(alpha,n) for n in nn]
        plot (nn, yy, marker=marker, color='k', linewidth=1, linestyle='solid',
              label = (r'$\alpha=%g$' % alpha))
    xlabel (r'$n$',fontsize=24)
    ylabel (r'$\log(\Gamma(\alpha\!+\!n)/\Gamma(\alpha))$')
    legend (labelspacing=0.2) # frameon=False, edgecolor='black'


def usage ():
    print ('usage: % poch.py N [output]')
    print ('$Id: poch.py,v 1.4 2023/04/09 02:46:44 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage()
    else:
        N = int (sys.argv[1])

    plot_lpoch (N)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
