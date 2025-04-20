#!/usr/local/bin/python2

import sys
import numpy as np
from hinton import hinton
from collections import defaultdict
from pylab import *

def make_matrix (freq, chars):
    s = 0
    N = len(chars)
    M = np.zeros ((N,N), dtype=float)
    for i in range(N):
        for j in range(N):
            b = chars[i] + chars[j]
            M[i,j] = freq[b]
            s += M[i,j]
    return M / s

def analyze (file):
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            s = line.rstrip('\n')
            N = len(s)
            s += '$'
            for i in range(N):
                b = s[i:i+2]
                freq[b] += 1
    return freq

def usage ():
    print ('usage: joint.py alice.txt [output]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    chars = 'abcdefghijklmnopqrstuvwxyz $'
    freq = analyze (sys.argv[1])
    M = make_matrix (freq, chars)
    hinton (M, chars)
    if len(sys.argv) > 2:
        savefig (sys.argv[2], bbox_inches='tight', dpi=300)
    show ()


if __name__ == "__main__":
    main ()
