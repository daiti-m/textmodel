#!/usr/local/bin/python

import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from rutil import pmultinom
from eprint import eprintf
from numpy.random import shuffle, randint
from numpy.random import permutation as randperm
from pylab import *

def infer (data, model, iters):
    beta = model['beta']
    V,K  = beta.shape
    M    = len (data)
    P    = np.zeros ((M,V), dtype=float)
    for m in range(M):
        eprintf ('computing doc %d/%d..\r' % (m+1,M))
        theta = gibbs (data[m], model, iters)
        P[m] = np.dot (beta, theta)
    return P

def gibbs (words, model, iters=200):
    alpha = model['alpha']
    beta = model['beta']
    V,K  = beta.shape
    T    = len(words)
    zz   = np.zeros (T, dtype=int)
    nz   = np.zeros (K, dtype=int)
    sz   = np.zeros (K, dtype=float)
    samples = 0
    # initialize
    for t in range(T):
        zz[t] = randint (K)
        nz[zz[t]] += 1
    # gibbs
    for iter in range(iters):
        for t in randperm(T):
            w = words[t]
            z = zz[t]
            nz[z] -= 1
            z = draw_topic (w, nz, alpha, beta); zz[t] = z
            nz[z] += 1
        if iter+1 > iters / 2:
            samples += 1
            for k in range(K):
                sz[k] += (nz[k] + alpha[k])
    return (sz / np.sum(sz))

def draw_topic (w, nz, alpha, beta):
    V,K = beta.shape
    p = np.zeros (K, dtype=float)
    for k in range(K):
        p[k] = beta[w][k] * (nz[k] + alpha[k])
    return pmultinom (p)

def perplexity (data, P):
    N = datalen (data)
    lik = datalik (data, P)
    return exp (- lik / N)

def datalen (data):
    return np.sum (list (map (len, data)))

def datalik (data, P):
    lik = 0
    M = len(data)
    for m in range(M):
        p = P[m]
        words = data[m]
        liks = [log(p[w]) for w in words]
        lik += sum (liks)
    return lik

#
#   supporting functions.
#

def sieve (data, ratio, model):
    train = []
    test  = []
    seen  = model['seen']
    for datum in data:
        words = list (filter (lambda x: x in seen, expand (datum)))
        shuffle (words)
        pos = int (len(words) * ratio)
        train.append (words[0:pos])
        test.append (words[pos:])
    return train, test

def expand (doc):
    words = []
    L = len (doc.id)
    for i in range(L):
        words.extend ([doc.id[i] for j in range(doc.cnt[i])])
    return words

def load (file):
    with gzip.open (file, 'rb') as gf:
        model = pickle.load (gf)
    return model

def usage ():
    print ('usage: % ldaeval.py model test [iters]')
    print ('$Id: ldaeval-gibbs.py,v 1.1 2023/06/11 05:26:35 daichi Exp $')
    sys.exit (0)

def main ():
    if len(sys.argv) < 3:
        usage ()
    else:
        model = load (sys.argv[1])
        data  = fmatrix.parse (sys.argv[2])
        iters = int (sys.argv[3]) if len(sys.argv) > 3 else 100
        seed  = os.getenv ('SEED')

    if seed is not None:
        np.random.seed (int(seed))

    train,test = sieve (data, 0.5, model)
    P = infer (train, model, iters)
    print ('train perplexity = %.2f' % perplexity (train, P))
    print ('test perplexity  = %.2f' % perplexity (test, P))


if __name__ == "__main__":
    main ()
