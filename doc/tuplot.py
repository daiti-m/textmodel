#!/usr/local/bin/python

import sys
import putil
import numpy as np
from pylab import *

def plot_tu (data):
    xx = data[0]
    yy1 = data[1]
    yy2 = data[2]
    zz1 = data[3]
    zz2 = data[4]

    figure (figsize=(6,4))
    putil.fontsize (20)
    plot (xx, yy2, '-', color='k', label='Wikipedia (TU++)')
    plot (xx, yy1, '--', color='k', label='Livedoor (TU++)')
    plot (xx, zz2, '-.', color='k', label='Wikipedia (TU)')
    plot (xx, zz1, ':', color='k', label='Livedoor (TU)')
    legend (loc='upper left', bbox_to_anchor=(1.05,1))
    xticks (xx)
    yticks (np.arange(0.6,1.1,0.1))
    axis ([0, xx[-1], 0.52, 1])
    xlabel (r'$K$', labelpad=8, fontsize=24)
    ylabel ('TU, TU++', labelpad=12, fontsize=24)

def usage ():
    print ('usage: % tuplot.py tu++.dat [output]')
    print ('$Id: tuplot.py,v 1.4 2023/06/19 16:06:12 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
        
    data = np.loadtxt (sys.argv[1]).T
    plot_tu (data)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
