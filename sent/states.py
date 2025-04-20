#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from pylab import *

def show_states (text, model):
    zzs = model['zz']
    if len(zzs) != len(text):
        print ('error! inequal length of text and states.')
        sys.exit (1)
    N = len(zzs)
    for n in range(N):
        words = text[n]
        zz = zzs[n]
        if len(words) != len(zz):
            print ('error! inequal length of words and states.')
        T = len(words)
        for t in range(T):
            print ('%-13s %2d' % (words[t], 1+zz[t]))
        print ('')

def read (file):
    text = []
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                text.append (words)
    return text

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % states.py input.txt model [output]')
    print ('$Id: states.py,v 1.2 2024/07/31 02:55:45 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()

    text = read (sys.argv[1])
    model = load (sys.argv[2])

    show_states (text, model)



if __name__ == "__main__":
    main ()
