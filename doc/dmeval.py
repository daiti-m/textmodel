#!/usr/local/bin/python
#
#    dmeval.py
#    $Id: dmeval.py,v 1.1 2023/02/17 12:51:46 daichi Exp $
#

import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from util import divide
from rutil import logsumexp,lnormalize
from eprint import eprintf
from random import sample
from numpy import exp,log
from scipy.special import gammaln

def predict (doc, p, model):
    alphas = model['alphas']
    K = model['K']
    liks = np.zeros (K, dtype=float)
    for k in range(K):
        liks[k] = log (p[k]) + dmlik (doc, alphas[k])
    return logsumexp (liks)

def dmlik (doc, alpha):
    N = np.sum (doc.cnt)
    L = len(doc.cnt)
    alpha0 = np.sum (alpha)
    lik = gammaln (alpha0) - gammaln (alpha0 + N)
    for i in range(L):
        v = doc.id[i]
        c = doc.cnt[i]
        if alpha[v] > 0:
            lik += gammaln (alpha[v] + c) - gammaln (alpha[v])
    return lik

def dminf (doc, model):
    lamb = model['lambda']
    alphas = model['alphas']
    K = model['K']
    liks = np.zeros (K, dtype=float)
    for k in range(K):
        liks[k] = log (lamb[k]) + dmlik (doc, alphas[k])
    return lnormalize (liks)

def evaluate (train, test, model):
    if len(train) != len(test):
        print ('evaluate: data length do not equal.')
        sys.exit (1)
    N = len(train)
    K = model['K']
    p = np.zeros ((N,K), dtype=float)
    lik = 0
    nwords = 0
    # body
    for n in range(N):
        eprintf ('computing %3d/%d..%s' % (n+1,N,'\n' if n==N-1 else '\r'))
        p[n] = dminf (train[n], model)
        lik += predict (test[n], p[n], model)
        nwords += sum (test[n].cnt)
    print ('PPL = %.2f' % exp(- lik / nwords))
    
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
    if os.path.exists (file):
        with gzip.open (file, 'rb') as gf:
            model = pickle.load (gf)
            return model
    else:
        lamb = np.loadtxt (file + '.lambda', dtype=float)
        alphas = np.loadtxt (file + '.alphas', dtype=float).T
        K,V = alphas.shape
        return { 'K': K, 'lambda': lamb, 'alphas': alphas }

def usage ():
    print ('usage: % dmeval.py model test.dat')
    print ('$Id: dmeval.py,v 1.1 2023/02/17 12:51:46 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()

    model = pload (sys.argv[1])
    train,test = dload (sys.argv[2])
    evaluate (train, test, model)


if __name__ == "__main__":
    main ()
