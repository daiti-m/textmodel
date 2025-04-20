#!/usr/local/bin/python
#
#    bum.py : Bayesian Unigram Mixtures in Python.
#    $Id: bum.py,v 1.11 2023/03/15 02:58:54 daichi Exp $
#

import os
import sys
import gzip
import pickle
import fmatrix
import numpy as np
from numpy.random import rand, randint
from numpy.random import permutation as randperm
from opts import getopts
from rutil import lmultinom
from eprint import eprintf
from pylab import *

ETA_DEFAULT = 0.01
GAMMA_DEFAULT = 1
ITERS_DEFAULT = 100
INTERVAL = 100

def doclik (doc, k, nk, nkv):
    lp = log (nk[k] / np.sum(nk))
    lnk = log (nk[k])
    return lp + np.dot (doc.cnt, log(nkv[k][doc.id]) - lnk)

def draw_gibbs (doc, nk, nkv):
    K = len(nk)
    liks = [doclik (doc, k, nk, nkv) for k in range(K)]
    return lmultinom (liks)

def learn (data, vocab, K, eta=0, gamma=0, iters=1):
    #
    # prepare
    #
    N = len(data)
    V = len(vocab)
    zz = np.zeros (N, dtype=int)
    nk = np.ones (K, dtype=float) * gamma
    nkv = np.ones ((K,V), dtype=float) * eta
    for k in range(K):
        nkv[k] = eta
    print ('UM: %d documents, %d words in vocabulary.' % (N,V))
    #
    # Gibbs sampler
    #
    for iter in range(iters):
        seq = randperm (N)
        for i in range(N):
            if ((i+1) % INTERVAL == 0):
                eprintf ('analyzing %d/%d documents..\r' % (i+1,N))
            n = seq[i]
            k = zz[n]
            doc = data[n]
            # Gibbs
            if (iter == 0):
                zz[n] = randint (K)
            else:
                nk[k] -= 1
                nkv[k][doc.id] -= doc.cnt
                zz[n] = draw_gibbs (doc, nk, nkv)
                
            k = zz[n]
            nk[k] += 1
            nkv[k][doc.id] += doc.cnt

        # perplexity
        ppl = perplexity (data, zz, nk, nkv)
        eprintf ('iter[%2d] : PPL = %.2f\n' % (iter+1, ppl))
        
    print (nk)

    return { 'K': K, 'lambda': normalize(nk), 'beta': mnormalize(nkv),
             'vocab': vocab, 'nk': nk }

def datalik (data, zz, nk, nkv):
    N = len(data)
    K = len(nk)
    lik = 0
    for n in range(N):
        lik += doclik (data[n], zz[n], nk, nkv)
    return lik

def datalen (data):
    N = len(data)
    nwords = 0
    for n in range(N):
        nwords += sum (data[n].cnt)
    return nwords

def perplexity (data, zz, nk, nkv):
    lik = datalik (data, zz, nk, nkv)
    nwords = datalen (data)
    return exp (- lik / nwords)

def normalize (xx):
    return xx / np.sum(xx)

def mnormalize (X):
    v = np.sum (X,1)
    return np.dot (np.diag (1/v), X)

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
    print ('bum: Bayesian Unigram Mixtures.')
    print ('usage: % bum.py OPTIONS train{.dat,.lex} model')
    print ('OPTIONS:')
    print ('-K mixtures   number of mixtures')
    print ('-N iters      number of MCMC iterations (default %d)' % ITERS_DEFAULT)
    print ('[-e eta]      eta hyperparameter (default %g)' % ETA_DEFAULT)
    print ('[-g gamma]    gamma hyperparameter (default %g)' % GAMMA_DEFAULT)
    print ('[-h]          displays this help')
    print ('$Id: bum.py,v 1.11 2023/03/15 02:58:54 daichi Exp $')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|mixtures=", "e|eta=", "g|gamma=", "N|iters=", "h|help"])
    if (len(args) != 2) or ('h' in opts) or ('K' not in opts):
        usage ()
    else:
        train = args[0]
        output = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        eta = float (opts['e']) if 'e' in opts else ETA_DEFAULT
        gamma = float (opts['g']) if 'g' in opts else GAMMA_DEFAULT
        iters = int (opts['N']) if 'N' in opts else ITERS_DEFAULT

    data = dload (train + '.dat')
    vocab = vload (train + '.lex')
    model = learn (data, vocab, K, eta, gamma, iters)
    save (model, output) 

if __name__ == "__main__":
    main ()
