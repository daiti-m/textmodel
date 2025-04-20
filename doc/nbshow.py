#!/usr/local/bin/python

import sys
import gzip
import pickle
import numpy as np
from util import ulen
from pylab import *

def npmi (pwk, pw):
    return 1 - log (pwk) / log (pw)

def pmi (pwk, pw):
    return log(pwk) - log(pw)

def nbshow (model, k, top=15):
    # prepare
    dic = {}
    K = model['K']
    pk = model['pk']
    pkv = model['pkv']
    vocab = model['vocab']
    for word,id in vocab.items():
        dic[id] = word
    # body
    p = np.dot (pk, pkv)
    V = len(p)
    results = sorted ([(npmi(pkv[k][v], p[v]), dic[v]) for v in range(V)],
                      key=lambda x: x[0], reverse=True)
    print ('Category[%d]: p = %.3f' % (k+1, pk[k]))
    for val,word in results[0:top]:
        width = 11 - ulen(word)
        print (word + ' ' * width + ('% .3f' % val))
        
def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % nbshow.py model [top] [k]')
    print ('$Id: nbshow.py,v 1.2 2024/04/05 23:16:13 daichi Exp $')
    sys.exit (0)
    
def main ():
    if len(sys.argv) < 2:
        usage ()

    model = pload (sys.argv[1])
    if len(sys.argv) > 2:
        top = int (sys.argv[2])
    else:
        top = 10
    
    if len(sys.argv) > 3:
        topics = list (map (int, sys.argv[3:]))
        for k in topics:
            nbshow (model, k-1, top)
    else:
        K = model['K']
        for k in range(K):
            nbshow (model, k, top)
            print ('------')

if __name__ == "__main__":
    main ()
