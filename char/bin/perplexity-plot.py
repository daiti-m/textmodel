#!/usr/local/bin/python2

import sys
import numpy as np
from pylab import *

def plot_data (data):
    keys = []
    values = []
    for (key,val) in sorted (data.items(),
                             key = lambda x: float (x[0])):
        keys.append (float(key))
        values.append (val)
    figure (figsize=(6.4,3.6))
    plot (keys, values)
    xscale ('log')
    yticks (np.arange(6.1,6.69,0.1))
    xlabel (r'$\alpha$', fontsize=24)
    ylabel ('PPL', labelpad=14, fontsize=20)
    

def load (file):
    data = {}
    with open (file, 'r') as f:
        for line in f:
            tokens = line.rstrip('\n').split()
            data[tokens[0]] = float (tokens[1])
    return data

def usage ():
    print ('usage: % perplexity-plot.py perplexity.txt [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    data = load (sys.argv[1])
    plot_data (data)
    if len(sys.argv) > 2:
        savefig (sys.argv[2], bbox_inches='tight')
    show ()







if __name__ == '__main__':
    main ()
