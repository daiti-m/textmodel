#!/usr/local/bin/python

import sys
import gzip
import putil
import pickle
from pylab import *

def plot_nb (model, output):
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    vocab = model['vocab']
    index = list (map (lambda x: x[1], 
                       sorted (vocab.items(), key=lambda x: x[0])))
    for word,v in vocab.items():
        for k in range(K):
            if (pkv[k][v] > 0.01):
                pkv[k][v] = 0
    plot_pkv (pkv, index, output)

def plot_pkv (pkv, index, output):
    K,V = pkv.shape
    topics = [1,2,3]
    for i in range(len(topics)):
        k = topics[i] - 1
        fig = figure (figsize=(6,1.2))
        ax = fig.add_subplot ()
        plot_pv (pkv[k], index, ax)
        ax.axis ([0,V,0,0.01])
        ax.set_xticks ([0,5000,10000,15000])
        ax.set_yticks ([0,0.005,0.01])
        ax.set_yticklabels (["0", "0.005", "0.01"])
        if i < len(topics) - 1:
            putil.no_xticks (ax)
        else:
            ax.text (0.99, -0.35, r'$w$', fontsize=20, transform=ax.transAxes)
        print ('saving to %s-y%d.png..' % (output,k+1))
        putil.savefig ('%s-y%d.png' % (output,k+1), dpi=300)

def plot_pv (pv, index, ax):
    V = len(pv)
    ax.plot (range(V), pv[index], 'k')

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nbplot.py model output')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[1])
    plot_nb (model, sys.argv[2])


if __name__ == "__main__":
    main ()
