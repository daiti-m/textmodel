#!/usr/local/bin/python
#
#    umeval.py
#    $Id: umeval.py,v 1.2 2023/02/12 02:22:31 daichi Exp $
#

import sys
import gzip
import pickle
import fmatrix
import numpy as np
from util import divide
from rutil import lnormalize
from eprint import eprintf
from random import sample
from numpy import exp,log

def predict (doc, r, model):
    K = model['K']
    L = len(doc.id)
    beta = model['beta']
    lik = 0
    for i in range(L):
        v = doc.id[i]
        c = doc.cnt[i]
        lik += c * log (np.dot (r, beta[:,v]))
    return lik

def doclik (doc, p):
    return np.dot (doc.cnt, log (p[doc.id]))

def uminf (doc, model):
    lamb = model['lambda']
    beta = model['beta']
    K = model['K']
    liks = np.zeros (K, dtype=float)
    for k in range(K):
        liks[k] = log (lamb[k]) + doclik (doc, beta[k])
    return lnormalize (liks)

def evaluate (train, test, model):
    if len(train) != len(test):
        print ('evaluate: data length do not equal.')
        sys.exit (1)
    N = len(train)
    K = model['K']
    p = np.zeros ((N,K), dtype=float)
    liks = 0
    nwords = 0
    # body
    for n in range(N):
        eprintf ('computing %3d/%d..%s' % (n+1,N,'\n' if n==N-1 else '\r'))
        p[n] = uminf (train[n], model)
        lik = predict (test[n], p[n], model)
        # print ('lik =', lik)
        liks += lik
        nwords += sum (test[n].cnt)
    print ('PPL = %.2f' % exp(- liks / nwords))
    
def dload (file):
    train = []; test = []
    data = fmatrix.plain (file)
    N = len(data)
    for n in range(N):
        words = sample (data[n], len(data[n]))
        first,second = divide (2, words)
        train.append (fmatrix.create (first))
        test.append (fmatrix.create (second))
    return train, test

def pload (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % umeval.py model test.dat')
    print ('$Id: umeval.py,v 1.2 2023/02/12 02:22:31 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()

    model = pload (sys.argv[1])
    train,test = dload (sys.argv[2])
    evaluate (train, test, model)


if __name__ == "__main__":
    main ()
