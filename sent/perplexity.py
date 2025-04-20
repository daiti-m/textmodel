#!/usr/local/bin/python

import sys
import putil
import numpy as np
from jpfont import jpfont
from pylab import *

def plot_perplexity (data):
    N = len(data)
    xx = np.arange (N)
    putil.fontsize (20)
    figure (figsize=(4,3))
    plot (xx, data, color='k')
    xticks ([1,250,500,750,1000])
    yticks ([1,4,6,8,10,12,14])
    gca().set_ylim (1, 13)
    xlabel (' 繰り返し', labelpad=10, fontsize=20, fontproperties=jpfont())
    ylabel ('PPL', rotation=0, labelpad=25, fontsize=22, y=0.45)
    # ylabel ('パープレキシティ', rotation=0, labelpad=80, fontsize=20, y=0.45,
    #         fontproperties=jpfont())

def load (file):
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            ppl = float (line.rstrip('\n'))
            data.append (ppl)
    return data

def usage ():
    print ('usage: % plot-perplexity.py data.ppl [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    data = load (sys.argv[1])
    plot_perplexity (data)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
