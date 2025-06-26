#!/usr/local/bin/python
#
#    sHMM.py
#    Bayesian hidden Markov model module. (simple, without marginalization)
#    $Id: shmm.py,v 1.4 2023/05/13 21:25:41 daichi Exp $
#
import sys
import gzip
import pickle
import loggings
import numpy as np
from opts import getopts
from loggings import elprintf
from collections import defaultdict
from numpy.random import dirichlet
from numpy.random import rand,randn,randint
from numpy.random import permutation as randperm
from rutil import multinom, pmultinom, lmultinom
from pylab import *

def draw_alpha (nzz, gamma):
    K = nzz.shape[0] - 1
    return np.array ([dirichlet (nzz[k] + gamma) for k in range(K+1)])

def draw_beta (nzw, eta):
    K = nzw.shape[0] - 1
    return np.array ([dirichlet (nzw[k] + eta) for k in range(K)])

def draw_gibbs (t, words, zz, alpha, beta):
    K = alpha.shape[0] - 1
    T = len(words)
    w = words[t]
    buf = np.zeros (K, dtype=float)
    # compute probabilities
    pz = zz[t-1] if t > 0 else K
    qz = zz[t+1] if t < T-1 else K
    for k in range(K):
        buf[k] = alpha[pz][k] * alpha[k][qz] * beta[k][w]
    return pmultinom (buf)

def gibbs (data, dic, K, gamma, eta, iters, model):
    loggings.start (sys.argv, model)
    N = len(data)
    V = len (dic)
    zz = [[randint(K) for i in range(len(data[n]))] for n in range(N)]
    nz = np.zeros (K+1)
    nzz = np.zeros ((K+1,K+1))
    nzw = np.zeros ((K+1,V))
    # initialization
    for n in range(N):
        T = len(data[n])
        for t in range(T):
            add_count (t, data[n], zz[n], nzz, nzw, nz, initial=True)
    print ('data: %d sequences, lexicon: %d words.' % (N, len(dic)))
    # body
    for iter in range(iters):
        # sample alpha and beta
        alpha = draw_alpha (nzz, gamma)
        beta  = draw_beta (nzw, eta)
        # sample z
        for n in randperm(N):
            T = len(data[n])
            for t in randperm(T):
                remove_count (t, data[n], zz[n], nzz, nzw, nz)                
                zz[n][t] = draw_gibbs (t, data[n], zz[n], alpha, beta)
                add_count (t, data[n], zz[n], nzz, nzw, nz)
        elprintf ('iter[%2d]: PPL = %.02f' % \
                  (iter+1, perplexity (data, zz, alpha, beta)))
    eprintf ('\n')
    # model
    model = convert_model (zz, nzz, nzw, gamma, eta, dic)
    loggings.finish ()
    return model

def convert_model (zz, nzz, nzw, gamma, eta, dic):
    alpha = rnormalize (nzz + gamma)
    beta  = rnormalize (nzw[:-1,:] + eta)
    return { 'zz': zz, 'trans': alpha, 'emit': beta, 'dic': dic }
        
def add_count (t, words, zz, nzz, nzw, nz, initial=False):
    z = zz[t]
    w = words[t]
    T = len(words)
    K = nzz.shape[0] - 1
    # observations
    nzw[z][w] += 1
    # total counts
    nz[z] += 1
    # transitions
    if t > 0:
        nzz[zz[t-1]][z] += 1
    else:
        nzz[K][z] += 1
    if t < T-1:
        if not initial:
            nzz[z][zz[t+1]] += 1
    else:
        nzz[z][K] += 1
        nz[K] += 1

def remove_count (t, words, zz, nzz, nzw, nz):
    z = zz[t]
    w = words[t]
    T = len(words)
    K = nzz.shape[0] - 1
    # observations
    nzw[z][w] -= 1
    # total counts
    nz[z] -= 1
    # transitions
    if t > 0:
        nzz[zz[t-1]][z] -= 1
    else:
        nzz[K][z] -= 1
    if t < T-1:
        nzz[z][zz[t+1]] -= 1
    else:
        nzz[z][K] -= 1
        nz[K] -= 1

# likelihood computation

def hmmlik (data, zz, alpha, beta):
    return hmmlik_zz (zz, alpha) + hmmlik_zw (data, zz, beta)

def hmmlik_zz (zz, alpha):
    N = len(zz)
    lik = 0
    for n in range(N):
        lik += zzlik (zz[n], alpha)
    return lik

def hmmlik_zw (data, zz, beta):
    N = len(zz)
    lik = 0
    for n in range(N):
        lik = zwlik (data[n], zz[n], beta)
    return lik

def zzlik (zz, alpha):
    K = alpha.shape[0] - 1
    T = len(zz)
    lik = log (alpha[zz[T-1]][K])
    for t in range(T):
        z = zz[t]
        pz = zz[t-1] if t > 0 else K
        lik += log (alpha[pz][z])
    return lik

def zwlik (words, zz, beta):
    T = len(words)
    lik = 0
    for t in range(T):
        w = words[t]
        z = zz[t]
        lik += log (beta[z][w])
    return lik

def perplexity (data, zz, alpha, beta):
    L = sum (list (map (len, data)))
    lik = hmmlik (data, zz, alpha, beta)
    return exp (- lik / L)

def rdic (dic):
    rdic = {}
    for word,id in dic.items():
        rdic[id] = word
    return rdic

def read (file, threshold):
    sys.stderr.write ('reading data from %s.. ' % file),
    sys.stderr.flush ()
    dic = lexicon (file, threshold)
    data = []
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            if len(words) > 0:
                data.append (list (map (lambda word: wordid(word, dic), words)))
    sys.stderr.write ('done.\n')
    return data, rdic(dic)

def lexicon (file, threshold):
    dic = {}
    seed = 0
    dic['_OOV_'] = seed
    freq = defaultdict (int)
    with open (file, 'r') as fh:
        for line in fh:
            words = line.rstrip('\n').split()
            for word in words:
                freq[word] += 1
    # build lexicon
    for word,count in sorted (freq.items(), key=lambda x: x[1], reverse=True):
        if (count >= threshold):
            seed += 1
            dic[word] = seed
    return dic

def wordid (word, dic):
    if (word in dic):
        return dic[word]
    else:
        return 0

def save (model, output):
    eprintf ('writing to %s.. ' % output)
    with gzip.open (output, 'wb') as gf:
        pickle.dump (model, gf, 2)
    eprintf ('done.\n')

def rnormalize (M): # row-wise normalize matrix
    return np.array ([m / np.sum(m) for m in M])

def eprint (s):
    sys.stderr.write (s + '\n')
    sys.stderr.flush ()

def eprintf (s):
    sys.stderr.write (s)
    sys.stderr.flush ()

def usage ():
    print ('usage: % shmm.py OPTIONS train model')
    print ('OPTIONS:')
    print (' -K states  number of states in HMM')
    print (' -N iters   number of MCMC iterations')
    print (' -a alpha   Dirichlet hyperparameter on transitions (default 0.1)')
    print (' -b beta    Dirichlet hyperparameter on emissions (default 0.01)')
    print (' -t thresh  Frequency threshold for lexicon (default 1)')
    print (' -h         displays this help')
    sys.exit (0)

def main ():
    opts,args = getopts (["K|states=", "N|iters=", "a|alpha=", "b|beta=",
                          "t|threshold=", "h|help"])
    if len(args) != 2:
        usage ()
    else:
        train = args[0]
        output = args[1]
        K = int (opts['K']) if 'K' in opts else 10
        iters = int (opts['N']) if 'N' in opts else 1
        alpha = float (opts['a']) if 'a' in opts else 0.1
        beta  = float (opts['b']) if 'b' in opts else 0.01
        threshold = int (opts['t']) if 't' in opts else 1

    data,dic = read (train, threshold)
    model = gibbs (data, dic, K, alpha, beta, iters, output)
    save (model, output)


if __name__ == "__main__":
    main ()
