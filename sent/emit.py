#!/usr/local/bin/python

import sys
import gzip
import putil
import pickle
import numpy as np
from hinton import hinton
from pylab import *

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % emit.py model [output]')
    print ('$Id: emit.py,v 1.1 2024/07/30 08:23:23 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    model = load (sys.argv[1])
    beta = model['emit']
    hinton (beta[:,1:50])
    if len(sys.argv) > 2:
        putil.savefig (sys.argv[2], dpi=300)
    show ()




if __name__ == "__main__":
    main ()
