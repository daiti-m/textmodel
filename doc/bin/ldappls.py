#!/usr/local/bin/python

import sys
import putil
import numpy as np
import matplotlib as mpl
from pylab import *

def plot_ppls (data):
    xx = data[0]
    yy = data[1]
    zz = data[2]
    figure (figsize=(6,4))
    putil.fontsize (20)
    putil.usetex ()

    plot (xx, yy, '-', color='k', label=(r'$\bm{\alpha},\bm{\eta}$ Fixed'))
    plot (xx, zz, '--', color='k', label=(r'$\bm{\alpha},\bm{\eta}$ Estimated'))

    # xticks (xx)
    xticks (list(map(int, xx)))
    yticks (np.arange(1500, 2400, 200))
    axis ([0,520,1500,2350])
    legend (loc='upper right', bbox_to_anchor=(1,1), fontsize=20)
    xlabel (r'$K$', labelpad=8, fontsize=24)
    text (-180, 1890, 'PPL', fontsize=24)

def usage ():
    print ('usage: % ldappls.py ppls.txt [output]')
    print ('$Id: ldappls.py,v 1.4 2023/06/25 02:18:49 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    data = np.loadtxt (sys.argv[1]).T
    plot_ppls (data)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
