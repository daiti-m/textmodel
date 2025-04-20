#!/usr/local/bin/python
#
#    nb-word.py
#    computing word posterior p(y|w).
#    $Id: nbword.py,v 1.2 2024/04/20 02:30:05 daichi Exp $
#
import sys
import gzip
import pickle
import numpy as np
from pylab import *
from rutil import lnormalize

def infer (model, word):
    v = model['vocab'][word]
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    cats = model['cat2label']
    label2cat = revdic (cats)
    # body
    p = np.zeros (K, dtype=float)
    for k in range(K):
        p[k] = pk[k] * pkv[k][v]
    p = p / np.sum(p)
    for k in range(K):
        # print ('%-16s : %.3f' % (label2cat[k], p[k]))
        print ('%-16s : %4.1f' % (label2cat[k], p[k]*100))
    sys.exit (0)
    
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
    print ('usage: % nbword.py model word')
    print ('$Id: nbword.py,v 1.2 2024/04/20 02:30:05 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    model = pload (sys.argv[1])
    word = sys.argv[2]

    if not (word in model['vocab']):
        print ('%s not in model!' % word)
    else:
        infer (model, word)
    
    
if __name__ == "__main__":
    main ()
