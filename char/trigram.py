#!/usr/local/bin/python

import sys
import pickle
import numpy as np
from collections import defaultdict

BOS = '_BOS_'

def parse (file, alpha):
    # count occurrences
    freq = {}
    chars = defaultdict (int)
    with open (file, 'r') as f:
        for line in f:
            s = [c for c in line.rstrip('\n')]
            s.insert (0, BOS); s.insert (0, BOS)
            s.append (BOS)
            N = len(s)
            for i in range(2,N):
                c = s[i]; h1 = s[i-1]; h2 = s[i-2]
                h = h2 + '|' + h1
                if not (h in freq):
                    freq[h] = defaultdict (int)
                freq[h][c] += 1
                chars[c] += 1
    # compute probabilities
    p = {}
    for h in freq:
        Z = 0
        for c in chars:
            Z += freq[h][c] + alpha
        if not (h in p):
            p[h] = {}
        for c in chars:
            p[h][c] = (freq[h][c] + alpha) / Z

    return p

def usage ():
    print ('usage: trigram.py file model alpha')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        file = sys.argv[1]
        output = sys.argv[2]
        alpha  = float (sys.argv[3])
        
    model = parse (file, alpha)
    with open (output, 'wb') as out:
        pickle.dump (model, out)
        
if __name__ == "__main__":
    main ()
