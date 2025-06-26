#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from numpy import exp,log

def view (model, dic, p, k, n):
    beta = model['beta'].T
    npmi = 1 - log(beta[k]) / log(p)
    print ('topic [%d]' % (k+1))
    index = range (len(npmi))
    # body
    shown = 0
    for i,s in sorted (zip(index, npmi), key=lambda x: x[1], reverse=True):
        print ('%s\t%.4f' % (dic[i], s))
        shown += 1
        if shown >= n:
            break

def usage ():
    print ('usage: % ldashow.py model [k] [n]')
    sys.exit (0)

def main ():
    if len(sys.argv) < 2:
        usage ()
    model = pload (sys.argv[1])
    dic = rdic (model['lexicon'])
    p = np.mean (model['beta'], 1)

    if len(sys.argv) > 2:
        k = int (sys.argv[2]) - 1
        n = int (sys.argv[3]) if len(sys.argv) > 3 else 15
        view (model, dic, p, k, n)
    else:
        K = model['beta'].shape[1]
        for k in range(K):
            view (model, dic, p, k, 15)
            print ('------------------')

def pload (f):
    with gzip.open (f, 'rb') as gf:
        data = pickle.load (gf)
    return data

def rdic (dic):
    rdic = {}
    for word,id in dic.items():
        rdic[id] = word
    return rdic

if __name__ == "__main__":
    main ()
