#!/usr/local/bin/python
"""
imshow: save a matrix as image.
$Id: dmshow.py,v 1.1 2023/04/16 15:28:28 daichi Exp $
"""
import sys
import putil
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
from pylab import *

def npmi (alphas):
    S = np.sum (alphas, 1)
    P = np.dot (diag(1/S), alphas)
    m = np.mean (P, 0)
    NPMI = (log(P) - log(m)) / (- log(m))
    return NPMI

def convert (alphas):
    m = np.mean (alphas, 0)
    return alphas - m

def usage ():
    print ('dmshow: show alphas in DM.')
    print ('$Id: dmshow.py,v 1.1 2023/04/16 15:28:28 daichi Exp $')
    print ('usage: imshow matrix [output] [colormap]')
    sys.exit(0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        file = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        color = sys.argv[3] if len(sys.argv) > 3 else 'binary'
        # jet, RdBu, PiYG, binary
        
    Z = np.loadtxt(sys.argv[1])[0:1000,:]
    I = npmi (Z.T)
    J = convert (Z.T)
    X,Y = np.meshgrid (np.arange(1,Z.shape[0]+1), np.arange(1,Z.shape[1]+1))
    fig = plt.figure ()
    ax = fig.add_subplot (projection='3d')
    # surf = ax.plot_surface (X, Y, I, cmap=color)
    surf = ax.plot_surface (X, Y, J, cmap=color)
    putil.simple3d (ax)
    xlabel ('Word', labelpad=8)
    ylabel ('Topic', labelpad=8)
    ax.set_zlabel (r'$\alpha-\bar{\alpha}$', labelpad=10, fontsize=20)
    ax.view_init (azim=134, elev=29)
    ax.tick_params (axis='x', pad=0)
    ax.tick_params (axis='y', pad=0)
    ax.tick_params (axis='z', pad=5)
    if output is not None:
        putil.savefig (output, dpi=300)
    show ()


if __name__ == "__main__":
    main ()
