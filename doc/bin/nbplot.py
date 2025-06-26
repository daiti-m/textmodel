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
    fig = figure ()
    
    for i in range(len(topics)):
        k = topics[i] - 1
        ax = fig.add_subplot (3,1,i+1)
        plot_pv (pkv[k], index, ax)
        ax.set_ylabel (r'$p(w|y)$', rotation=0, fontsize=20, labelpad=37, y=0.35)
        ax.axis ([0,V,0,0.01])
        ax.set_xticks ([0,5000,10000,15000])
        ax.set_yticks ([0,0.005,0.01])
        ax.set_yticklabels (["0", "0.005", "0.01"])
        ax.text (20100, 0.005, (r'$y=%d$' % (i+1)), fontsize=20)
        if i < len(topics) - 1:
            putil.no_xticks (ax)
        else:
            ax.text (0.99, -0.28, r'$w$', fontsize=20, transform=ax.transAxes)
    if output is not None:
        putil.savefig (output)
    show ()

def plot_pv (pv, index, ax):
    V = len(pv)
    ax.plot (range(V), pv[index], 'k')

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nbplot.py model [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        data = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
    model = pload (data)
    plot_nb (model, output)


if __name__ == "__main__":
    main ()
