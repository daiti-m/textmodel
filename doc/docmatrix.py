#!/usr/local/bin/python

import sys
import putil
import fmatrix
import numpy as np
from pylab import *

def load (file):
    data = fmatrix.parse (file, origin=1)
    N,V = fmatrix.size (data)
    X = np.zeros ((N,V), dtype=int)
    for n in range(N):
        doc = data[n]
        X[n,doc.id] = doc.cnt
    return X

def usage ():
    print ('usage: docmatrix.py data.dat start [output]')
    print ('$Id: docmatrix.py,v 1.3 2023/02/25 10:56:27 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage()
    X = load (sys.argv[1])
    start = int (sys.argv[2])
    width = 100
    Y = X[0:width, start:start+width]
    figure (figsize=(6,4))
    pcolor (np.flipud(Y), cmap='binary')
    colorbar ().set_label ('counts', labelpad=8, fontsize=20)
    xticks (range(0,width+1,20),range(start,start+width+1,20))
    yticks (range(0,width+1,20),range(width,-1,-20))
    xlabel ('word', fontsize=20)
    ylabel ('doc', fontsize=20)

    # inner box
    plot ([0,10,10,0,0],[90,90,100,100,90],color='black',linewidth=2.5)
    
    # save
    if len(sys.argv) > 3:
        putil.savefig (sys.argv[3],dpi=300)
    show ()





if __name__ == "__main__":
    main ()
