#!/usr/local/bin/python

import sys
import pickle
import numpy as np
from collections import defaultdict

def parse (file):
    freq = defaultdict (int)
    p = {}
    with open (file, 'r') as f:
        for line in f:
            for c in line.rstrip('\n'):
                freq[c] += 1
    Z = sum (freq.values())
    for c in freq:
        p[c] = freq[c] / Z
    return p

def usage ():
    print ('usage: unigram.py file model')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = parse (sys.argv[1])
    with open (sys.argv[2], 'wb') as out:
        pickle.dump (model, out)

if __name__ == "__main__":
    main ()
