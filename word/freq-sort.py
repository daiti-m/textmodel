#!/usr/local/bin/python2
#
#    freq.py
#    plots frequency distribution.
#    $Id$
#
import sys
import putil
import numpy as np
from collections import defaultdict
from pylab import *

def plot_aux (xx, yy):
    plot (xx, yy)
    # tick_params (labelsize=20)
    xlabel ('Word',labelpad=10,fontsize=24)
    ylabel ('Frequency',labelpad=10,fontsize=24)

def freq_plot (freq):
    freqs = list (map (lambda x: x[1], sorted (freq.items(), key=lambda x: x[1],
                                               reverse=True)))
    L = len (freqs)
    plot_aux (range(1,L+1), freqs)

def count_freq (file):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\verb|\|n').split()
            for word in words:
                freq[word] += 1
    return freq

def usage ():
    print ('usage: % zipf.py text [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
        
    freq = count_freq (sys.argv[1])
    freq_plot (freq)

    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2])
    show ()
    

if __name__ == "__main__":
    main ()
