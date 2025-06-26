#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from util import ulen
from pylab import *

def npmi (pwk, pw):
    return 1 - log (pwk) / log (pw)

def umshow (model, k, top=15):
    # prepare
    dic = {}
    K = model['K']
    nk = model['nk']
    lamb = model['lambda']
    beta = model['beta']
    vocab = model['vocab']
    for word,id in vocab.items():
        dic[id] = word
    # body
    p = np.dot (lamb, beta)
    V = len(p)
    results = sorted ([(npmi(beta[k][v],p[v]), dic[v]) for v in range(V)],
                      key=lambda x: x[0], reverse=True)
    print ('Topic[%d]: weight = %.2f (nk = %.0f, p = %.3f)' % (k+1, p[k]*K, nk[k], p[k]))
    for val,word in results[0:top]:
        width = 11 - ulen(word)
        print (word + ' ' * width + ('% .3f' % val))

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % umshow.py model [k] [top]')
    print ('$Id: umshow.py,v 1.3 2023/03/10 07:59:49 daichi Exp $')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 2:
        usage ()

    model = pload (sys.argv[1])
    
    if len(sys.argv) > 2:
        topics = list (map (int, sys.argv[2:]))
        for k in topics:
            umshow (model, k-1, 15)
    else:
        K = model['K']
        for k in range(K):
            umshow (model, k)
            print ('------')
            

if __name__ == "__main__":
    main ()
