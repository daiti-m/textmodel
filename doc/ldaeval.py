#!/usr/local/bin/python

import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from numpy.random import shuffle
from scipy.special import psi,gammaln
from numpy import exp,log,sum,dot,diag
from copy import copy
# private
from util import converged
from eprint import eprint, eprintf

def infer (data, model):
    beta = model['beta']
    V,K  = beta.shape
    M    = len (data)
    P    = np.zeros ((M,V), dtype=float)
    for m in range(M):
        theta = vbem (data[m], model)
        P[m] = np.dot (beta, theta)
    return P

def vbem (doc,model,emmax=100):
    alpha = model['alpha']
    beta  = model['beta']
    V, K  = beta.shape
    id    = np.array (doc.id)
    cnt   = np.array (doc.cnt)
    L     = len (id)
    nt    = np.ones(K) * L / K
    pnt   = copy (nt)
    for j in range(emmax):
        # VB-estep
        theta = exp (psi(alpha + nt))
        q = mnormalize (np.dot (beta[id,:], diag(theta)))
        # q = mnormalize (np.dot (beta[id,:], diag(exp(psi(alpha + nt)))))
        # VB-mstep
        nt = np.dot (cnt, q)
        # converged?
        if converged (nt,pnt,1e-3):
            # eprint ("converged at iteration %d." % (j+1))
            return theta / sum(theta)
        pnt = copy(nt)
    eprint ("maximum EM iteration of %d reached." % emmax)
    return theta / sum(theta)

def mnormalize (X):
    v = np.sum(X,1)
    return np.dot (np.diag(1 / v), X)

def perplexity (data, P):
    N = datalen (data)
    lik = datalik (data, P)
    return exp (- lik / N)

def datalen (data):
    z = 0
    for doc in data:
        z += sum (doc.cnt)
    return z

def datalik (data, P):
    lik = 0
    N = len (data)
    for n in range(N):
        doc = data[n]
        L   = len (doc.id)
        # for each document
        for j in range(L):
            v = doc.id[j]
            c = doc.cnt[j]
            lik += c * log (P[n][v])
    return lik

def occur (words):
    freq = {}
    for word in words:
        if not (word in freq):
            freq[word] = 1
        else:
            freq[word] += 1
    # create a document
    doc = fmatrix.document ()
    for word in freq:
        doc.id.append (word)
        doc.cnt.append (freq[word])
    return doc

def expand (doc):
    words = []
    L = len (doc.id)
    for i in range(L):
        words.extend ([doc.id[i] for j in range(doc.cnt[i])])
    return words

def sieve (data, ratio, model):
    train = []
    test  = []
    seen  = model['seen']
    for datum in data:
        # words = expand (datum)
        words = list (filter (lambda x: x in seen, expand (datum)))
        shuffle (words)
        pos = int (len(words) * ratio)
        train.append (occur (words[0:pos]))
        test.append (occur (words[pos:]))
    return train, test

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % ldaeval.py model test')
    print ('$Id: ldaeval.py,v 1.4 2023/06/11 05:33:16 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = load (sys.argv[1])
        data  = fmatrix.parse (sys.argv[2])
        seed  = os.getenv ('SEED')

    if seed is not None:
        np.random.seed (int(seed))

    train,test = sieve (data, 0.5, model)
    P = infer (train, model)
    print ('train perplexity = %.2f' % perplexity (train, P))
    print ('test perplexity  = %.2f' % perplexity (test, P))


if __name__ == "__main__":
    main ()
