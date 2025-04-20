#!/usr/local/bin/python
#
#    docvec-plot.py
#    $Id: docvec-plot.py,v 1.5 2023/12/12 02:00:46 daichi Exp $
#
import sys
import putil
import docvec
import numpy as np
import japanize_matplotlib
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D

def plot_docvec (model, M=100):
    docvec = model['docvec']
    wordvec = model['featvec']
    dic = rdict (model['dic'])
    # prepare
    N = docvec.shape[0]
    V = wordvec.shape[0]
    index = np.random.choice (range(N), M, replace=False)
    index2 = np.random.choice (range(V), M*2, replace=False)
    ranges = np.array ([-1,1])
    # plot
    fig = figure()
    ax = fig.add_subplot (projection='3d')
    ax.scatter (docvec[index,-2], docvec[index,-3], docvec[index,-4],
                marker='x', linewidths=0.75, s=40, color='k')
    for v in index2: # starts from 0
        ax.text (wordvec[v+1,-2], wordvec[v+1,-3], wordvec[v+1,-4],
                 dic[v+1], fontsize=8)
    # adjust
    ax.set_xlim (0.3 * ranges)
    ax.set_ylim (0.3 * ranges)
    ax.set_zlim (0.3 * ranges)
    ax.view_init (azim=-102, elev=29)
    putil.simple3d (ax)

def rdict (dic):
    rdic = {}
    for key,val in dic.items():
        rdic[val] = key
    return rdic
    
def usage ():
    print ('usage: % docvec-plot.py docvec.model [output]')
    print ('$Id: docvec-plot.py,v 1.5 2023/12/12 02:00:46 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
        
    model = docvec.load (sys.argv[1])
    plot_docvec (model)
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()


if __name__ == "__main__":
    main ()
