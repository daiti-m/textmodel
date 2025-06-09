#!/usr/local/bin/python
#
#    visualize.py
#    visualize word vectors via t-SNE.
#    $Id: visualize.py,v 1.1 2022/08/12 01:00:03 daichi Exp $
#
import sys
import putil
import numpy as np
from sklearn.manifold import TSNE
from eprint import eprintf
from pylab import *

def plot_vectors (X, words):
    putil.figsize ((10,10))
    putil.aspect_ratio (1)
    N = len(X)
    axes = [-45,50,-40,53]
    # axes = [-5,15,20,35]
    # axes = [-15,15,36,47]
    # axes = [-20,0,-35,-20]
    # axes = [-70,70,-70,70]
    for n in range(N):
        text (X[n,0], X[n,1], words[n], fontsize=6, color='black', ha='left')
#         x = X[n,0]; y = X[n,1]
#         if (x > axes[0]) and (x < axes[1]) and (y > axes[2]) and (y < axes[3]):
#             text (X[n,0], X[n,1], words[n], fontsize=24, color='black', ha='left')
    axis (axes)

def loadvec (file, N):
    eprintf ('loading from "%s".. ' % file)
    matrix = []; words = []
    lines = 0
    with open (file, 'r') as fh:
        for line in fh:
            tokens = line.rstrip('\n').split()
            if len(tokens) > 2: # possibly skip word2vec header
                lines += 1
                if lines > N:
                    break
                else:
                    matrix.append (np.array (list (map (float, tokens[1:]))))
                    words.append (tokens[0])
    eprintf ('done.\n')
    return np.array(matrix), words

def usage ():
    print ('usage: % visualize.py words.vec N [output]')
    print ('$Id: visualize.py,v 1.1 2022/08/12 01:00:03 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        N = int (sys.argv[2])

    matrix,words = loadvec (file, N)
    eprintf ('reducing dimensions ..')
    X = TSNE (n_components=2, random_state=0).fit_transform (matrix)
    eprintf ('done.\n', clear=False)
    plot_vectors (X, words)
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=200)
    show ()

if __name__ == "__main__":
    main ()
