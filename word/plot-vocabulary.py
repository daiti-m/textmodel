#!/usr/local/bin/python2

import sys
import putil
import numpy as np
from pylab import *

def plot_progression (file, label):
    data = np.loadtxt (file, dtype=int)
    plot (data[:,0], data[:,1], label=label)
    
# marker=marker, markerfacecolor="white", markeredgewidth=1, markeredgecolor="black")

def usage ():
    print ('usage: % plot-vocabulary.py output file1 file2..')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    islog = 0
    fig = figure()
    putil.fontsize(20)
    output = sys.argv[1]
    labels = ["alice", "ginga", "brown", "text8.ja"]
    for i in range(len(sys.argv)-2):
        plot_progression (sys.argv[2+i], labels[i])
    if islog:
        xscale ('log')
        yscale ('log')
        text (0.06, 0.92, r'$V$', transform=fig.transFigure, fontsize=24)
        text (0.9, 0.015, r'$N$', transform=fig.transFigure, fontsize=24)
    else:
        text (0.07, 0.89, r'$V$', transform=fig.transFigure, fontsize=24)
        text (0.9, 0.035, r'$N$', transform=fig.transFigure, fontsize=24)
    legend (loc='lower right')
    putil.savefig (output)
    show ()

if __name__ == "__main__":
    main ()
