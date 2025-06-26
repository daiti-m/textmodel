#!/usr/local/bin/python
#
#    apoch.py
#    Approximate Pochhammer function, according to Elkan (2006).
#    $Id: apoch.py,v 1.3 2023/04/12 00:51:01 daichi Exp $
#
import sys
import putil
import numpy as np
from scipy.special import gammaln
from pylab import *

def apoch (alpha, n):
    return log (alpha) + gammaln (n)

def poch (alpha, n):
    return gammaln (alpha + n) - gammaln (alpha)

def plot_apoch (alpha, N):
    figure (figsize=(5,3))
    putil.fontsize (20)
    nn = np.arange (1,N+1)
    yy = [poch(alpha,n) for n in nn]
    zz = [apoch(alpha,n) for n in nn]
    plot (nn, exp(yy), color='k', linestyle='solid',
          label=r'$\Gamma(\alpha\!+\!n)/\Gamma(\alpha)$')
    plot (nn, exp(zz), color='k', linestyle='dashed',
          label=r'$\alpha (x\!-\!1)!$')
    xticks (range(1,N+1))
    xlabel (r'$n$',fontsize=24)
    legend (fontsize=20)
    
def usage ():
    print ('usage: % poch.py alpha N [output]')
    print ('$Id: apoch.py,v 1.3 2023/04/12 00:51:01 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage()
    else:
        alpha = float (sys.argv[1])
        N = int (sys.argv[2])

    plot_apoch (alpha, N)
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
