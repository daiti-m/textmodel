#!/usr/local/bin/python

import sys
import putil
import numpy as np
from eprint import eprintf
from pylab import *

def loadvec (file):
    eprintf ('loading from "%s".. ' % file)
    matrix = []; words = []
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                matrix.append (np.array (list (map (float, tokens[1:]))))
                words.append (tokens[0])
    eprintf ('done.\n')
    return np.array(matrix), words

def normalize (x):
    return x / np.sqrt (np.dot(x,x))

def usage ():
    print ('usage: % vcovariance.py words.vec [output] [colormap]')
    print ('$Id: vcovariance.py,v 1.5 2022/07/28 11:47:59 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    else:
        file = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        colormap = sys.argv[3] if len(sys.argv) > 3 else 'seismic'
    matrix,words = loadvec (file)
    putil.fontsize (20)
    # V = np.dot (matrix.T, matrix) / matrix.shape[0]
    # imshow (V, interpolation='none', cmap=colormap, vmin=-0.4, vmax=0.4)
    V = np.dot (matrix.T, matrix)
    imshow (V, interpolation='none', cmap='seismic', vmin=-1, vmax=1)
    xlabel (' dimension', labelpad=6)
    ylabel ('dimension', labelpad=3)
    xticks (np.arange(0,120,20))
    yticks (np.arange(0,120,20))
    putil.margins (left=0.1, bottom=0.2)
    colorbar ()
    if output is not None:
        putil.savefig (output, dpi=200)
    show ()

if __name__ == "__main__":
    main ()
