#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from pylab import *

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def main ():
    model = pload (sys.argv[1])
    if (len(sys.argv) < 3):
        print ('keys =', list(model.keys()))
        sys.exit (0)
        
    param = sys.argv[2]
    if not (param in model):
        print ('keys =', list(model.keys()))
    else:
        print (model[param])

if __name__ == "__main__":
    main ()
