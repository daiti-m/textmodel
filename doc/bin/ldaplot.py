#!/usr/local/bin/python

import sys
import gzip
import putil
import pickle
import numpy as np
from pylab import *
from matplotlib import colors
from matplotlib.colors import Normalize

def ldaplot (p):
    N,K = p.shape
    M = 100
    # pcolor (p[0:M,:], cmap='binary', norm=Normalize(vmin=0,vmax=0.5))
    pcolor (p[0:M,:], cmap='binary', norm=colors.LogNorm(vmin=1e-2,vmax=1))
    cbar = colorbar (ticks=[1,0.5,0.2,0.1,0.01])
    cbar.ax.minorticks_off ()
    cbar.ax.set_yticklabels(['1', '0.5', '0.2', '0.1', '0.01'])
    cbar.set_label (r'$p(z|d)$', rotation=0, labelpad=30, y=0.57, fontsize=24)
    xlabel (r'Topic $z$', labelpad=8, fontsize=20)
    ylabel (r'Document $d$', labelpad=7, fontsize=20)

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % ldaplot.py model [output]')
    print ('$Id: ldaplot.py,v 1.3 2023/05/31 19:11:37 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()

    figure (figsize=(8,4))
    model = pload (sys.argv[1])
    ldaplot (model['theta'])
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()

if __name__ == "__main__":
    main ()
