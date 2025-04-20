#!/usr/local/bin/python
#
#    dm.py : Dirichlet Mixtures in Python.
#    $Id: dm.py,v 1.11 2023/04/11 09:22:38 daichi Exp $
#
import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from scipy.special import psi, gammaln
from numpy.random import rand
from numpy import copy
from opts import getopts
from util import converged
from rutil import logsumexp,lnormalize
from eprint import eprintf
from pylab import *

EPSILON_DEFAULT = 1e-4
MAXITER_DEFAULT = 100
INTERVAL = 100

def newton_maximize (alphas, data, p, maxiter=100):
    N = len(data)
    K,V = alphas.shape
    # prepare
    oalphas = np.zeros (V, dtype=float)
    s = np.zeros (N, dtype=float)
    for n in range(N):
        s[n] = sum (data[n].cnt)
    # main
    for k in range(K):
        for iter in range(maxiter):
            eprintf ('optimizing alphas: [%2d/%d] iteration %d\r' % (k+1,K,iter+1))
            z1 = np.zeros (V, dtype=float)
            z2 = 0
            alpha0 = sum (alphas[k])
            oalphas = copy (alphas[k])
            for n in range(N):
                doc = data[n]
                L = len(doc.id)
                for i in range(L):
                    v = doc.id[i]
                    c = doc.cnt[i]
                    z1[v] += p[n][k] * (psi (alphas[k][v] + c) - psi (alphas[k][v]))
                z2 += p[n][k] * (psi (alpha0 + s[n]) - psi (alpha0))
            for v in range(V):
                val = alphas[k][v] * z1[v] / z2
                if (val > 1e-10):
                    alphas[k][v] = val
            if (iter > 0) and vconverged (alphas[k], oalphas, 1e-2):
                break
    return alphas

def loo_maximize (alphas, data, p, maxiter=100):
    N = len(data)
    K,V = alphas.shape
    # prepare
    oalphas = np.zeros (V, dtype=float)
    s = np.zeros (N, dtype=float)
    for n in range(N):
        s[n] = sum (data[n].cnt)
    # main
    for k in range(K):
        for iter in range(maxiter):
            eprintf ('optimizing alphas: [%2d/%d] iteration %d\r' % (k+1,K,iter+1))
            z1 = np.zeros (V, dtype=float)
            z2 = 0
            alpha0 = sum (alphas[k])
            oalphas = copy (alphas[k])
            for n in range(N):
                doc = data[n]
                L = len(doc.id)
                for i in range(L):
                    v = doc.id[i]
                    c = doc.cnt[i]
                    z1[v] += p[n][k] * c / (c - 1 + alphas[k][v])
                z2 += p[n][k] * s[n] / (s[n] - 1 + alpha0)
            for v in range(V):
                val = alphas[k][v] * z1[v] / z2
                if (val > 0):
                    alphas[k][v] = val
            if (iter > 0) and vconverged (alphas[k], oalphas, 1e-2):
                break
    return alphas

def learn (data, vocab, K, epsilon=1e-3, maxiter=1):
    #
    # prepare
    #
    N = len(data)
    V = len(vocab)
    lamb = np.ones (K, dtype=float) / K
    alphas = np.zeros ((K,V), dtype=float)
    liks = np.zeros ((N,K), dtype=float)
    p = np.zeros ((N,K), dtype=float)
    # initialize
    f = np.zeros (V, dtype=float)
    for n in range(N):
        doc = data[n]
        f[doc.id] += doc.cnt
    for k in range(K):
        for v in range(V):
            if f[v] > 0:
                alphas[k][v] = (f[v] + rand() / 10) / N  # alphas[k] = f / N
    #
    # EM-Newton algorithm
    #
    pppl = 0
    for iter in range(maxiter):
        # E step
        alpha0 = np.sum (alphas, 1)
        for n in range(N):
            if ((n+1) % INTERVAL == 0):
                eprintf ('computing mixtures %3d/%d..\r' % (n+1,N))
            for k in range(K):
                liks[n][k] = log (lamb[k]) + dmlik (data[n], alphas[k], alpha0[k])
            p[n] = lnormalize (liks[n])
        # M step
        for k in range(K):
            lamb[k] = np.sum (p[:,k])
        lamb = normalize (lamb)
        alphas = loo_maximize (alphas, data, p)
        # alphas = newton_maximize (alphas, data, p)
    
        # perplexity
        ppl = perplexity (data, lamb, alphas)
        eprintf ('iter[%2d] : PPL = %.2f\n' % (iter+1, ppl))
        if converged (ppl, pppl, epsilon):
            print ('converged.')
            break
        pppl = ppl

    print (lamb)        
    print (alphas)

    return { 'K': K, 'lambda': lamb, 'alphas': alphas,
             'vocab': vocab, 'nk': np.sum (p,0) }

def dmlik (doc, alpha, alpha0):
    N = np.sum (doc.cnt)
    L = len(doc.cnt)
    lik = gammaln (alpha0) - gammaln (alpha0 + N)
    lik += np.sum (gammaln (alpha[doc.id] + doc.cnt) - gammaln (alpha[doc.id]))
    return lik
    
def datalik (data, lamb, alphas):
    N = len(data)
    K = len(lamb)
    lik = 0
    alpha0 = np.sum (alphas, 1)
    for n in range(N):
        lik += logsumexp ([log(lamb[k]) + dmlik (data[n], alphas[k], alpha0[k])
                           for k in range(K)])
    return lik

def datalen (data):
    N = len(data)
    nwords = 0
    for n in range(N):
        nwords += sum (data[n].cnt)
    return nwords

def perplexity (data, lamb, alphas):
    lik = datalik (data, lamb, alphas)
    nwords = datalen (data)
    return exp (- lik / nwords)

def normalize (xx):
    return xx / np.sum(xx)

def vconverged (u, v, threshold):
    us = np.dot (u, u)
    ds = np.dot (u-v, u-v)
    if sqrt(ds / us) < threshold:
        return True
    else:
        return False

def save (model, file):
    eprintf ('saving model to %s.. ' % file)
    with gzip.open (file, 'wb') as gf:
        pickle.dump (model, gf)
    eprintf ('done.\n', clear=False)
    
def dload (file):
    if not os.path.exists (file):
        print ('training data %s does not exist!' % file)
        sys.exit (1)
    return fmatrix.parse (file, origin=1)

def vload (file):
    if not os.path.exists (file):
        print ('vocabulary file %s does not exist!' % file)
        sys.exit (1)
    vocab = {}
    with open (file, 'r') as fh:
        for line in fh:
            id,word = line.rstrip('\n').split()
            vocab[word] = int(id) - 1
    return vocab

def usage ():
    print ('dm: Dirichlet Mixtures.')
    print ('usage: % dm.py OPTIONS train{.dat,.lex} model')
    print ('OPTIONS:')
    print ('-K mixtures   number of mixtures')
    print ('[-d epsilon]  threshold of convergence (default %g)' % EPSILON_DEFAULT)
    print ('[-I emmax]    maximum number of EM iterations (default %d)' % MAXITER_DEFAULT)
    print ('[-h]          displays this help')
    print ('$Id: dm.py,v 1.11 2023/04/11 09:22:38 daichi Exp $')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|mixtures=", "d|epsilon=", "I|emmax=", "h|help"])
    if (len(args) != 2) or ('h' in opts) or ('K' not in opts):
        usage ()
    else:
        train = args[0]
        output = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        maxiter = int (opts['I']) if 'I' in opts else MAXITER_DEFAULT
        epsilon = float (opts['d']) if 'd' in opts else EPSILON_DEFAULT

    data = dload (train + '.dat')
    vocab = vload (train + '.lex')
    model = learn (data, vocab, K, epsilon, maxiter)
    save (model, output) 

if __name__ == "__main__":
    main ()
