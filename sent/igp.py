#!/usr/local/bin/python
#
#    igp.py
#    Fitting with Inverse Gaussian Poisson distribution.
#    $Id: igp.py,v 1.7 2024/11/08 07:46:15 daichi Exp $
#

import sys
import putil
import numpy as np
from collections import defaultdict
from scipy.special import kv as besselk
from scipy.optimize import minimize_scalar
from jpfont import jpfont
from pylab import *

def search (fun, *args):
    res = minimize_scalar (fun, args=args)
    return res.x
    
def count (data):
    freq = defaultdict (int)
    for item in data:
        freq[item] += 1
    return freq

def igplik (a, freq, x):
    lik = 0
    for n,c in freq.items():
        lik += c * ligp (n, x, a)
    return -lik

def igp_mle (data):
    # MLE xi
    x = np.mean (data)
    # MLE alpha
    freq = count (data)
    a = search (igplik, freq, x)
    return x, a

def load (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            n = int (line.rstrip('\n'))
            data.append (n)
    return np.array (data)

def igp (n, x, a):
    y = sqrt (x*x + a*a) - x
    f = (log(2*a) - log(np.pi)) / 2 + y + n * log (x * y / a) \
        - np.sum (log (np.arange(1,n+1)))
    b = besselk (n - 1/2, a)
    if np.isinf(b):
        return exp (f) * exp (lbesselk (n - 1/2, a))
    else:
        return exp (f) * b
    # return exp (f) * besselk (n - 1/2, a)

def ligp (n, x, a):
    y = sqrt (x*x + a*a) - x
    f = (log(2*a) - log(np.pi)) / 2 + y + n * log (x * y / a) \
        - np.sum (log (np.arange(1,n+1)))
    b = besselk (n - 1/2, a)
    if np.isinf(b):
        return f + lbesselk (n - 1/2, a)
    else:
        return f + log(b)

def lbesselk (v, z):
    return 1/2 * log(np.pi) + (v - 1/2) * log(2*v) - v * (1 + log(z))
    # from https://stackoverflow.com/questions/32484696/
    #      natural-logarithm-of-bessel-function-overflow

def igp_plot (x, a, N=500):
    xx = np.arange (1,N+1)
    yy = [igp(n,x,a) for n in xx]
    plot (xx, yy, color='black')

def show_plots (data, x, a, N=500):
    putil.fontsize (20)
    fig,ax = subplots(figsize=(8,4))
    # plot for data
    ax.hist (data, bins=100, color='gray')
    ax.set_ylabel ('頻度', labelpad=10, fontsize=24, fontproperties=jpfont())
    # ax.set_ylabel ('Frequency', labelpad=14, fontsize=24)
    # plot for IGP
    ax2 = ax.twinx()
    xx = np.arange (1,N+1)
    yy = [exp(ligp(n,x,a)) for n in xx]
    ax2.plot (xx, yy, color='black')
    ax2.set_ylim (0, 0.013)
    ax2.set_yticks (np.arange(0,0.013,0.002))
    ax2.set_ylabel ('確率', labelpad=18, fontsize=24, fontproperties=jpfont())
    # ax2.set_ylabel ('Probability', labelpad=18, fontsize=24)

def usage ():
    print ('usage: % igp.py length.dat [output]')
    print ('$Id: igp.py,v 1.7 2024/11/08 07:46:15 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    data = load (sys.argv[1])
    x,a = igp_mle (data)
    print (x,a)
    show_plots (data, x, a)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=200)
    show ()


if __name__ == "__main__":
    main ()
