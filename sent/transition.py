#!/usr/local/bin/python

import sys
import gzip
import putil
import pickle
from hinton import hinton
from pylab import *

def plot_transition (model):
    trans = model['trans']
    K = trans.shape[0]
    hinton (trans)
    text (0.5, 1.06, r"$z'$", fontsize=36, transform=gca().transAxes)
    ylabel (r'$z$', fontsize=36, rotation=0, labelpad=24)

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % transition.py model [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    model = pload (sys.argv[1])
    plot_transition (model)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()

if __name__ == "__main__":
    main ()
