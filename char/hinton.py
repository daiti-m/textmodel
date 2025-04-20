#!/usr/local/bin/python
#
#    hinton.py for Hinton diagram.
#    based on hinton_demo.py
#    $Id: hinton.py,v 1.1 2020/11/07 02:48:34 daichi Exp $
#
import numpy as np
import matplotlib.pyplot as plt

def hinton (matrix, label=None, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log(np.abs(matrix).max()) / np.log(2))

    ax.set_aspect ('equal', 'box')
    ax.xaxis.set_major_locator (plt.NullLocator())
    ax.yaxis.set_major_locator (plt.NullLocator())

    for (x,y),w in np.ndenumerate(matrix):
        size = np.sqrt(np.abs(w) / max_weight)
        rect = plt.Rectangle([y - size / 2, x - size / 2], size, size,
                             facecolor='black', edgecolor='black')
        ax.add_patch (rect)

    if label:
        N = len(label)
        for n in range(N):
            fs = 12 if n < N-1 else 10
            ax.text (n, -1.4, label[n],
                     fontsize=fs, horizontalalignment='center')
        for n in range(N-1):
            ax.text (-1.9, n+0.4, label[n],
                     fontsize=12, horizontalalignment='center')
        ax.text (N-1.9, -1.1, '""',
                 fontsize=12, horizontalalignment='center')
        ax.text (-1.9, N-1.2, '" "',
                 fontsize=12, horizontalalignment='center')

    # ax.autoscale_view ()
    ax.axis ([-0.7,N-0.2,-0.7,N-1.2])
    ax.invert_yaxis ()
    # plt.show ()

if __name__ == '__main__':
    import sys
    X = np.loadtxt (sys.argv[1])
    hinton (X)
