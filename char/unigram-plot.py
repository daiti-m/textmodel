#!/usr/local/bin/python2

import sys
import putil
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pylab import *

def make_matrix (freq, chars):
    N = len(chars)
    M = np.zeros (N, dtype=float)
    Z = 0
    for n in range(N):
        c = chars[n]
        M[n] = freq[c]
        Z += M[n]
    return M / Z

def unigram (file):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        s = fh.read ()
    for c in s:
        if c != '\n':
            freq[c] += 1
    return freq

def plot_bar (p, chars):
    N = len(p)
    putil.figsize ((10,2.5))
    bar (range(1,N+1), p, width=0.05, color='k')
    for n in range(N-1):
        text (n+1, -0.025, chars[n], fontsize=24, ha='center')
    text (N-1+0.6, -0.024, '" "')
    axis ([0.5,N+0.5,0,0.12])
    simpleaxis ()

def simpleaxis():
    ax = gca().axes
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks ([])
    ax.xaxis.set_ticklabels ([])
    tick_params (
        bottom = False, labelbottom = False
    )

def hinton (matrix, chars, max_weight=None, ax=None):
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
#     for n in range(N-1):
#         ax.text (n, -1.1, chars[n],
#                  fontsize=12, horizontalalignment='center')
#     ax.text (N-0.8, -1.0, '" "',
#              fontsize=12, horizontalalignment='center')

    ax.axis ([-0.9,N,-0.7,0.7])
    ax.invert_yaxis ()

def main ():
    chars = 'abcdefghijklmnopqrstuvwxyz '
    freq = unigram (sys.argv[1])
    p = make_matrix (freq, chars)
    # hinton (p, chars)
    plot_bar (p, chars)
    if len(sys.argv) > 2:
        savefig (sys.argv[2], bbox_inches='tight', dpi=300)
    show ()


if __name__ == "__main__":
    main ()
