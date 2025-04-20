#!/usr/local/bin/python
#
#    nb-word.py
#    computing word posterior p(y|w).
#    $Id: nbwords.py,v 1.1 2024/04/20 02:40:36 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *
from rutil import lnormalize

def infer (model, words):
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    cats = model['cat2label']
    vocab = model['vocab']
    label2cat = revdic (cats)
    # body
    valids = []
    results = []
    for word in words:
        if (word in vocab):
            p = np.zeros (K, dtype=float)
            v = vocab[word]
            for k in range(K):
                p[k] = pk[k] * pkv[k][v]
            p = p / np.sum(p)
            results.append (p)
            valids.append (word)
    L = len(valids)
    print ('%-16s : ' % '[category]', end='')
    for i in range(L):
        print (' %-4s' % valids[i], end='')
    print ('')
    for k in range(K):
        print ('%-16s :' % label2cat[k], end='')
        for i in range(L):
            print ('  %4.1f' % (results[i][k] * 100), end='')
        print ('')
    
def revdic (dic):
    hash = {}
    for key in dic:
        val = dic[key]
        hash[val] = key
    return hash

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nbword.py model word..')
    print ('$Id: nbwords.py,v 1.1 2024/04/20 02:40:36 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[1])
    words = sys.argv[2:]

    infer (model, words)
    
    
if __name__ == "__main__":
    main ()
