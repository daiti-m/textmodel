#!/usr/local/bin/python

import sys
import putil
import numpy as np
from jpfont import jpfont
from pylab import *

def sif (p,a):
    return a / (p + a)

def weight (p,t):
    return 1 - max (1 - sqrt(t/p), 0)

def plot_sif (a, style):
    M = 130
    p = 0.9
    xx = [p**n for n in range(M)]
    yy = [sif(x,a) for x in xx]
    plot (xx, yy, color='black', linestyle=style, label='SIF')

def plot_weights (t, style):
    M = 130
    p = 0.9
    xx = [p**n for n in range(M)]
    yy = [weight(x,t) for x in xx]
    plot (xx, yy, color='black', linestyle=style, label='Word2Vec')

def usage ():
    print ('usage: % sif-word2vec-weights.py a t [output]')
    print ('$Id: sif-word2vec-weights.py,v 1.5 2024/11/15 03:48:08 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    a = float (sys.argv[1])  # 1e-4
    t = float (sys.argv[2])  # 1e-5
    putil.figsize ((7,3.5))
    putil.fontsize (20)
    plot_sif (a, 'solid')
    plot_weights (t, 'dashed')
    xscale ('log')
    legend ()
    xlabel (r'$p$', fontsize=32, labelpad=3)
    ylabel ('単語重み', labelpad=61, fontsize=24, rotation=0, y=0.445,
            fontproperties=jpfont())
    xticks ([10**(-n) for n in range(6,-1,-1)])
    yticks ([0,0.25,0.5,0.75,1])
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=200)
    show ()


if __name__ == "__main__":
    main ()
