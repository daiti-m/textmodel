#!/usr/local/bin/python
import re
import sys
import putil
import numpy as np
from eprint import eprint, eprintf
from scipy.linalg import svd
from pylab import *

def compress (X, K):
    U,S,V = svd (X)
    return U[:,0:K]

def loadvec (file, words):
    ret = []
    data = {}
    if re.search (r'\.bz2$', file):
        fh = bz2.BZ2File (file, 'r')
    else:
        fh = open (file, 'r')
    lines = 0    
    for line in fh:
        lines += 1
        if (lines % 10000 == 0):
            eprintf ('reading lines %6d..\r' % lines)
        tokens = line.rstrip('\n').split()
        word = tokens[0]
        if (word in words):
            v = np.array (tokens[1:], dtype=float)
            data[word] = v / np.sqrt(np.dot(v,v))
    fh.close ()
    eprintf ('reading lines %6d..\n' % lines)
    if len(words) != len(data):
        eprint ('error! some words are not found.')
        sys.exit (1)
    for word in words:
        ret.append (data[word])
    return np.array(ret), words

def plotvec (coords, labels):
    N = coords.shape[0]
    putil.fontsize (20)
    # plot points
    scatter (coords[:,0], coords[:,1], color='black')
    # plot labels
    for n in range(N):
        label = labels[n]
        if (n % 2) == 0:
            text (coords[n,0]-0.01, coords[n,1]+0.04, label)
        else:
            text (coords[n,0]-0.005, coords[n,1]-0.08, label)
    # plot arrows
    for m in range(int(N/2)):
        diff = coords[2*m,:] - coords[2*m,:]
        annotate (text='',xytext=coords[2*m,:], xy=coords[2*m+1,:],
                  arrowprops=dict(facecolor='black',width=1.5, headwidth=7.0,
                                  headlength=7.0, shrink=0.01))

def usage ():
    print ('usage: % pca2D.py words.vec output.png word1 word2..')
    print ('$Id$')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    vecfile = sys.argv[1]
    output = sys.argv[2]
    words = sys.argv[3:]

    vectors,labels = loadvec (vecfile, words)
    coords = compress (vectors, 2)
    plotvec (coords, labels)
    savefig (output, dpi=300)
    show ()

if __name__ == "__main__":
    main ()
