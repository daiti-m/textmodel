#!/usr/local/bin/python

import sys
import pickle
import numpy as np
from collections import defaultdict
from pylab import *

BOS = '_BOS_'

def likelihood (model, model1, line):
    s = [c for c in line]
    s.insert (0, BOS); s.insert (0, BOS);
    s.append (BOS)
    N = len(s)
    lik = 0
    # for each character to predict
    for i in range(2,N):
        c = s[i]; h1 = s[i-1]; h2 = s[i-2]
        h = h2 + '|' + h1
        if not (h in model):
            p = model1[c]
        else:
            p = model[h][c]
        lik += log (p)

    return lik
    

def unigram (model):
    p = defaultdict (float)
    Z = 0
    for h in model:
        for c in model[h]:
            p[c] += model[h][c]
            Z += model[h][c]
    for c in p:
        p[c] = p[c] / Z
    return p

def perplexity (model, model1, file):
    N = 0
    lik = 0
    with open (file, 'r') as f:
        for line in f:
            s = line.strip('\n')
            N += len (s) + 1
            lik += likelihood (model, model1, s)

    return exp (- lik / N)
            
def usage ():
    print ('usage: % perplexity.py model test')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        file = sys.argv[1]
        test = sys.argv[2]

    with open (file, 'rb') as f:
        model = pickle.load (f)
    model1 = unigram (model)

    print ('perplexity = %f' % perplexity (model, model1, test))

if __name__ == "__main__":
    main ()
