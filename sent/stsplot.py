#!/usr/local/bin/python

import sys
import putil
import numpy as np
from numpy.linalg import solve
from jpfont import jpfont
from pylab import *

xmin = -0.3; xmax = 5.3
ymin = -0.25; ymax = 1.05

def main ():
    data = np.loadtxt (sys.argv[1]).T
    N = data.shape[1]
    x = data[0]; y = data[1]
    X = np.vstack([np.ones(N),x.T]).T
    w = solve (X.T.dot(X), X.T.dot(y))
    # point scatter
    putil.fontsize (20)
    scatter (x, y, color='gray')
    xticks (np.arange(0,6,1))
    xlabel ('正解類似度', fontsize=20, labelpad=10, fontproperties=jpfont())
    ylabel (r'$\cos$類似度', fontsize=20, labelpad=2, fontproperties=jpfont())
    # linear regression = correlation
    M = 50
    xx = linspace (-0.15, 5.15, M)
    yy = [w[0] + w[1] * t for t in xx]
    plot (xx, yy, 'k')
    axis ([xmin, xmax, ymin, ymax])
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
