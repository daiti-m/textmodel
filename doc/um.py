#!/usr/local/bin/python
#
#    um.py : Unigram Mixtures in Python.
#    $Id: um.py,v 1.15 2023/04/03 05:01:01 daichi Exp $
#

import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from numpy.random import rand
from opts import getopts
from util import converged
from rutil import logsumexp,lnormalize,dirichlet
from eprint import eprintf
from pylab import *

ETA_DEFAULT = 0.01
GAMMA_DEFAULT = 1
EPSILON_DEFAULT = 1e-3
MAXITER_DEFAULT = 200
INTERVAL = 100

def learn (data, vocab, K, eta=0, gamma=0, epsilon=1e-3, maxiter=1):
    #
    # prepare
    #
    N = len(data)
    V = len(vocab)
    p = np.zeros ((N,K), dtype=float)
    liks = np.zeros ((N,K), dtype=float)
    lamb = log (np.ones (K, dtype=float) / K)
    beta = np.ones ((K,V), dtype=float)
    alpha = np.ones (K, dtype=float) * 5
    for k in range(K):
        beta[k] = 10 + rand (V) 
    for k in range(K):
        beta[k] = log (beta[k] / np.sum(beta[k]))
    print ('UM: %d documents, %d words in vocabulary.' % (N,V))
    #
    # EM algorithm
    #
    pppl = 0
    for iter in range(maxiter):
        # E step
        for n in range(N):
            if ((n+1) % INTERVAL == 0):
                eprintf ('Estep: %4d/%d documents..\r' % (n+1,N))
            for k in range(K):
                liks[n][k] = lamb[k] + doclik (data[n], beta[k])
            p[n] = lnormalize (liks[n])
        eprintf ('Mstep: updating parameters..\r')
        # M step
        for k in range(K):
            lamb[k] = log (gamma + np.sum(p[:,k]))
        lamb -= logsumexp (lamb)
        for k in range(K):
            beta[k] = eta  # smoothing parameter
            for n in range(N):
                doc = data[n]
                beta[k][doc.id] += p[n][k] * np.array (doc.cnt)
            beta[k] = log (normalize (beta[k]))
        # perplexity
        ppl = perplexity (data, p, lamb, beta)
        eprintf ('iter[%2d] : PPL = %.2f\n' % (iter+1, ppl))
        if converged (ppl, pppl, epsilon):
            print ('converged.')
            break
        pppl = ppl

    return { 'K': K, 'lambda': exp(lamb), 'beta': exp(beta), 'p': p, 
             'vocab': vocab , 'nk': np.sum (p,0) }

def doclik (doc, lp):
    return np.dot (doc.cnt, lp[doc.id])

def datalik (data, p, lamb, beta):
    N = len(data)
    K = len(lamb)
    lik = 0
    for n in range(N):
        doc = data[n]
        for k in range(K):
            lik += p[n][k] * (lamb[k] + doclik (doc, beta[k]))
    return lik

def datalen (data):
    N = len(data)
    nwords = 0
    for n in range(N):
        nwords += sum (data[n].cnt)
    return nwords

def perplexity (data, p, lamb, beta):
    lik = datalik (data, p, lamb, beta)
    nwords = datalen (data)
    return exp (- lik / nwords)

def normalize (xx):
    return xx / np.sum(xx)

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
    print ('um: Unigram Mixtures.')
    print ('usage: % um.py OPTIONS train{.dat,.lex} model')
    print ('OPTIONS:')
    print ('-K mixtures   number of mixtures')
    print ('[-e eta]      eta hyperparameter (default %g)' % ETA_DEFAULT)
    print ('[-g gamma]    gamma hyperparameter (default %g)' % GAMMA_DEFAULT)
    print ('[-d epsilon]  threshold of convergence (default %g)' % EPSILON_DEFAULT)
    print ('[-I emmax]    maximum number of EM iterations (default %d)' % MAXITER_DEFAULT)
    print ('[-h]          displays this help')
    print ('$Id: um.py,v 1.15 2023/04/03 05:01:01 daichi Exp $')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|mixtures=", "e|eta=", "g|gamma=", "d|epsilon=",
                          "I|emmax=", "h|help"])
    if (len(args) != 2) or ('h' in opts) or ('K' not in opts):
        usage ()
    else:
        train = args[0]
        output = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        eta = float (opts['e']) if 'e' in opts else ETA_DEFAULT
        gamma = float (opts['g']) if 'g' in opts else GAMMA_DEFAULT
        maxiter = int (opts['I']) if 'I' in opts else MAXITER_DEFAULT
        epsilon = float (opts['d']) if 'd' in opts else EPSILON_DEFAULT
        
    data = dload (train + '.dat')
    vocab = vload (train + '.lex')
    model = learn (data, vocab, K, eta, gamma, epsilon, maxiter)
    save (model, output) 

if __name__ == "__main__":
    main ()
