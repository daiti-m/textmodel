#!/usr/local/bin/python

import sys
import slice
import putil
import numpy as np
from pylab import *

def gibbs (pdf, iters):
    x,y = -3,-2
    samples = [[x,y]]
    for iter in range(iters):
        # draw y
        y = slice.sample (y, lambda y: log(pdf([x,y])))
        samples.append ([x,y])
        # draw x
        x = slice.sample (x, lambda x: log(pdf([x,y])))
        samples.append ([x,y])
    return np.array (samples)
    

def xmax (pdf, y):
    N = 100
    xx = np.linspace (-5, 5, N)
    pp = [pdf([x,y]) for x in xx]
    idx = max (enumerate(pp), key=lambda x: x[1])[0]
    return xx[idx]

def ymax (pdf, x):
    N = 100
    yy = np.linspace (-5, 5, N)
    pp = [pdf([x,y]) for y in yy]
    idx = max (enumerate(pp), key=lambda x: x[1])[0]
    return yy[idx]

def icm (pdf):
    x,y = -3,-2
    samples = [[x,y]]
    # while (1):
    for iter in range(5):
        # draw x
        x = xmax (pdf, y)
        samples.append ([x,y])
        y = ymax (pdf, x)
        samples.append ([x,y])
    return np.array (samples)

#
#  pdf and plotting functions.
#

def let (val,func):
        return func (val)

def mvnpdf (mu, S):
    return (lambda x:
            let (np.array(x) - mu,
                 lambda y: exp (- np.dot(y, np.dot(inv(S), y)) / 2)
                           / (2 * np.pi * sqrt(det(S)))))

def mixture (weights, pdfs):
    return (lambda x:
            np.dot (weights,
                    list (map (lambda pdf: pdf(x), pdfs))))
    
def plot_gauss (mu, S):
    @np.vectorize
    def f (x,y):
        return mvnpdf (mu, S)([x,y])
    
    N = 100
    xx = np.linspace (-5, 5, N)
    yy = np.linspace (-5, 5, N)
    X, Y = np.meshgrid (xx, yy)
    Z = f (X, Y)
    contour (X, Y, Z)

def plot_density (density, levels=30):
    @np.vectorize
    def p(x,y):
        return log (density([x,y]))
    N = 100
    xx = np.linspace (-5, 5, N)
    yy = np.linspace (-4, 7, N)
    X, Y = np.meshgrid (xx, yy)
    Z = p (X, Y)
    #contour (X, Y, Z, levels=levels, colors='black', linestyles='dashed', linewidth=0.5)
    contour (X, Y, Z, levels=levels, colors='black', linestyles='solid', linewidths=0.5)

def usage ():
    print ('usage: % mixture-gibbs.py [levels=40] [output]')
    print ('$Id: mixture-gibbs.py,v 1.8 2024/07/30 04:36:58 daichi Exp $')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 2:
        usage ()
    
    mu1 = [1,-1]; mu2 = [-1,3]; mu3 = [3,4]
    S1 = [[2,0],[0,1]]; S2 = [[1,0],[0,1]]; S3 = [[0.5,-0.4],[-0.4,1]]
    density = mixture ([0.1,0.2,0.7],
                       [mvnpdf(mu1, S1), mvnpdf(mu2, S2), mvnpdf(mu3, S3)])
    # main
    levels = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    putil.fontsize (20)
    # plt.rcParams['lines.dashed_pattern'] = [2.0, 2.0]
    plot_density (density, levels)
    path = icm (density)
    plot (path.T[0], path.T[1], color='gray', linewidth=5)
    path = gibbs (density, 100)
    plot (path.T[0], path.T[1], color='black')
    xlabel (r'$x$',fontsize=28)
    ylabel (r'$y$',fontsize=28,rotation=0,labelpad=17)
    
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()



if __name__ == "__main__":
    main ()
