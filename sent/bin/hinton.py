#!/usr/local/bin/python
#
#    hinton.py for Hinton diagram.
#    based on hinton_demo.py
#    $Id: hinton.py,v 1.3 2019/10/01 02:39:14 daichi Exp $
#
import numpy as np
import matplotlib.pyplot as plt

def hinton (matrix, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()
    rows,cols = matrix.shape

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

    ax.autoscale_view ()
    ax.invert_yaxis ()
    ax.set_xlim (-1, cols)
    ax.set_ylim (-1, rows)

if __name__ == '__main__':
    import sys
    X = np.loadtxt (sys.argv[1])
    hinton (X)
