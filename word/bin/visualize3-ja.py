#!/usr/local/bin/python
#
#    visualize.py
#    visualize word vectors via t-SNE.
#    $Id: visualize.py,v 1.1 2022/08/12 01:00:03 daichi Exp $
#
import sys
import putil
import numpy as np
import japanize_matplotlib
from sklearn.manifold import TSNE
from eprint import eprintf
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D

def plot_vectors (X, words):
    N = len(X)
    ranges = np.array ([-1,1])
    fig = figure (figsize=(10,10))
    ax = fig.add_subplot (projection='3d')
    putil.simple3d (ax)
    for n in range(N):
        ax.text (X[n,0], X[n,1], X[n,2], words[n], fontsize=8, color='black', ha='left')
    ax.set_xlim (10 * ranges)
    ax.set_ylim (10 * ranges)
    ax.set_zlim (10 * ranges)
    

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
    X = TSNE (n_components=3, random_state=0).fit_transform (matrix)
    eprintf ('done.\n', clear=False)
    plot_vectors (X, words)
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3], dpi=200)
    show ()

if __name__ == "__main__":
    main ()
