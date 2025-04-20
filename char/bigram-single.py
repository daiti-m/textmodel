#!/usr/local/bin/python2

import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pylab import *

def make_matrix (freq, char, chars):
    Z = 0
    N = len(chars)
    M = np.zeros ((N,N), dtype=float)
    for i in range(N):
        for j in range(N):
            b = chars[i] + chars[j]
            M[i,j] = freq[b]
            Z += M[i,j]
    return M[chars.index(char)] / Z

def analyze (file):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            s = line.rstrip('\n')
            N = len(s)
            s += '$'
            for i in range(N):
                b = s[i:i+2]
                freq[b] += 1
    return freq

def hinton (matrix, char, chars, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log(np.abs(matrix).max()) / np.log(2))

    ax.set_aspect ('equal', 'box')
    ax.xaxis.set_major_locator (plt.NullLocator())
    ax.yaxis.set_major_locator (plt.NullLocator())

    M = len(matrix); x = 0
    for y in range(M):
        w = matrix[y]; 
        size = np.sqrt(np.abs(w) / max_weight)
        rect = plt.Rectangle([y - size / 2, x - size / 2], size, size,
                             facecolor='black', edgecolor='black')
        ax.add_patch (rect)

    N = len(chars)
    ax.text (-1.5, 0.2, char,
             fontsize=14, horizontalalignment='center')
    for n in range(N):
        fs = 14 if n < N - 1 else 12
        ax.text (n, -1.2, chars[n],
                 fontsize=fs, horizontalalignment='center')
    ax.text (N-2, -1.1, '""',
             fontsize=12, horizontalalignment='center')

    ax.axis ([-0.7,N-0.2,-0.7,0.7])
    ax.invert_yaxis ()

def usage ():
    print ('usage: single.py alice.txt char [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    char = sys.argv[2]
    chars = 'abcdefghijklmnopqrstuvwxyz $' 
    freq = analyze (sys.argv[1])
    M = make_matrix (freq, char, chars)
#    print (M)
    hinton (M, char, chars)
    if len(sys.argv) > 3:
        savefig (sys.argv[3], bbox_inches='tight', dpi=300)
    show ()


if __name__ == "__main__":
    main ()
