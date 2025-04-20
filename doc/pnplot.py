#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *
from matplotlib import rcParams

def main ():
    X = np.loadtxt (sys.argv[1])
    pos = X[:,1][X[:,0]==1]
    neg = X[:,1][X[:,0]==-1]
    labels = ['Negative', 'Positive']
    # body
    figure (figsize=(5,4))
    putil.fontsize (20)
    rcParams['xtick.labelsize'] = 24
    boxplot ([neg,pos], labels=labels,
             widths=0.3, medianprops=dict(color='black', linewidth=2.5))
    ylabel (r'$p(y=1|d)$', fontsize=28, labelpad=12)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=200)
    show ()


if __name__ == "__main__":
    main ()
